"""Sync messages and Message Batches, each behind the budget guard and logged to usage.csv.

Claude outputs are evaluation and inference only, never training data (ROADMAP §11.3).
"""
from __future__ import annotations

import hashlib
import json
import logging
import math
import os
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from . import models, usage
from .budget import Budget, BudgetError
from .client import guarded, make_client
from .keys import Secret, load_api_key
from .paths import batch_state_dir, find_repo_root, repo_name, usage_csv

log = logging.getLogger("jzapi")

# API version 2026-10-21 (anthropic SDK >= 2.0) returns 400 for these, even at default values.
FORBIDDEN_PARAMS = ("temperature", "top_p", "top_k")
COUNT_KEYS = ("model", "messages", "system", "tools", "tool_choice", "thinking", "cache_control",
              "output_config")
COUNT_MARGIN = 1.05      # count_tokens "is an estimate and may differ slightly"
BYTES_OVERHEAD = 64      # per message, for role markers etc. on the bytes upper bound


class BatchStateError(RuntimeError):
    pass


# ----------------------------------------------------------------------------- request building
def system_blocks(system: str | list | None, *, cache: bool = False, cache_ttl: str = "5m"):
    """A system prompt as content blocks, with cache_control on the last block if cache=True.

    Caching only takes effect above 512 tokens on Haiku/Sonnet/Opus 5.5 (shorter prompts are
    processed uncached, without error).
    """
    if system is None:
        return None
    blocks = [{"type": "text", "text": system}] if isinstance(system, str) else [dict(b) for b in system]
    if cache and blocks:
        cc: dict[str, Any] = {"type": "ephemeral"}
        if cache_ttl == "1h":
            cc["ttl"] = "1h"
        elif cache_ttl != "5m":
            raise ValueError("cache_ttl must be '5m' or '1h'")
        blocks[-1] = {**blocks[-1], "cache_control": cc}
    return blocks


def build_params(*, model: str, max_tokens: int, user: str | None = None, messages: list | None = None,
                 system: str | list | None = None, cache_system: bool = False, cache_ttl: str = "5m",
                 **extra) -> dict:
    """Messages API params with the model resolved to its pinned ID."""
    bad = [k for k in FORBIDDEN_PARAMS if k in extra]
    if bad:
        raise ValueError(f"{bad} are rejected by API version 2026-10-21; Claude samples at the "
                         f"default. Record 'api_default' in your results instead.")
    if (user is None) == (messages is None):
        raise ValueError("give exactly one of user= or messages=")
    if int(max_tokens) < 1:
        raise ValueError("max_tokens must be >= 1")
    params: dict[str, Any] = {"model": models.resolve(model), "max_tokens": int(max_tokens),
                              "messages": messages if messages is not None else
                              [{"role": "user", "content": user}]}
    sb = system_blocks(system, cache=cache_system, cache_ttl=cache_ttl)
    if sb is not None:
        params["system"] = sb
    params.update(extra)
    return params


def request(custom_id: str, **kw) -> dict:
    """One Message Batches request: {'custom_id', 'params'}. kw as for build_params."""
    import re
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", custom_id):
        raise ValueError(f"custom_id must match ^[a-zA-Z0-9_-]{{1,64}}$: {custom_id!r}")
    return {"custom_id": custom_id, "params": build_params(**kw)}


def _validate_params(params: dict) -> dict:
    bad = [k for k in FORBIDDEN_PARAMS if k in params]
    if bad:
        raise ValueError(f"{bad} are rejected by API version 2026-10-21")
    if params.get("stream"):
        raise ValueError("stream is not supported here")
    p = dict(params)
    p["model"] = models.resolve(p["model"])
    if int(p.get("max_tokens") or 0) < 1:
        raise ValueError("max_tokens must be >= 1")
    return p


def cache_ttl_of(params: dict) -> str | None:
    """None if the request has no cache_control; '1h' if any breakpoint uses it; else '5m'."""
    s = json.dumps(params, ensure_ascii=False)
    if '"cache_control"' not in s:
        return None
    return "1h" if '"ttl": "1h"' in s else "5m"


def bytes_upper_bound(params: dict) -> int:
    """Prompt tokens can't exceed UTF-8 bytes (+ per-message overhead): a safe offline bound."""
    payload = {k: params.get(k) for k in ("system", "messages", "tools") if params.get(k) is not None}
    n_msgs = len(params.get("messages") or []) + 1
    return len(json.dumps(payload, ensure_ascii=False).encode("utf-8")) + BYTES_OVERHEAD * n_msgs


# ----------------------------------------------------------------------------- results
@dataclass
class MessageResult:
    text: str
    model_id: str
    request_id: str | None
    stop_reason: str | None
    usage: dict
    cost_usd: float
    raw: Any = field(default=None, repr=False)


@dataclass
class BatchItem:
    custom_id: str
    type: str                    # succeeded | errored | canceled | expired
    text: str | None
    model_id: str | None
    stop_reason: str | None
    usage: dict
    cost_usd: float
    error: str | None = None


def _usage_dict(u: Any) -> dict:
    def g(obj, k):
        return obj.get(k) if isinstance(obj, dict) else getattr(obj, k, None)
    cc = g(u, "cache_creation")
    return {"input_tokens": int(g(u, "input_tokens") or 0),
            "output_tokens": int(g(u, "output_tokens") or 0),
            "cache_creation_input_tokens": int(g(u, "cache_creation_input_tokens") or 0),
            "cache_read_input_tokens": int(g(u, "cache_read_input_tokens") or 0),
            "cache_write_1h_tokens": int((g(cc, "ephemeral_1h_input_tokens") if cc is not None else 0) or 0)}


def _text_of(msg: Any) -> str:
    content = msg.get("content") if isinstance(msg, dict) else getattr(msg, "content", [])
    out = []
    for b in content or []:
        t = b.get("type") if isinstance(b, dict) else getattr(b, "type", None)
        if t == "text":
            out.append(b.get("text") if isinstance(b, dict) else b.text)
    return "".join(out)


def _attr(obj, k, default=None):
    return obj.get(k, default) if isinstance(obj, dict) else getattr(obj, k, default)


# ----------------------------------------------------------------------------- session
class Session:
    """One job in one repo: client + budget + usage log + batch state.

    repo_dir defaults to the git repo containing the cwd (JZ_REPO_DIR overrides); usage goes to
    <repo>/results/usage.csv and batch state to <repo>/results/jzapi_batches/.
    token_estimate: 'count' (free count_tokens endpoint, x1.05) or 'bytes' (offline upper bound).
    """

    def __init__(self, job: str, *, repo_dir: str | Path | None = None, client: Any = None,
                 cap_usd: float | None = None, budgets_path: str | Path | None = None,
                 token_estimate: str = "count", count_workers: int = 8, secret: Secret | None = None):
        if token_estimate not in ("count", "bytes"):
            raise ValueError("token_estimate must be 'count' or 'bytes'")
        self.repo_dir = Path(repo_dir).resolve() if repo_dir else find_repo_root()
        self.repo = repo_name(self.repo_dir)
        self.usage_csv = usage_csv(self.repo_dir)
        self.batch_dir = batch_state_dir(self.repo_dir)
        self.budget = Budget(job, cap_usd, self.usage_csv, budgets_path=budgets_path, batch_dir=self.batch_dir)
        self.job = job
        self.token_estimate = token_estimate
        self.count_workers = count_workers
        self._secret = secret
        self._client = client

    def __repr__(self) -> str:
        return f"Session(job={self.job!r}, repo={self.repo!r}, cap_usd={self.budget.cap_usd})"

    @property
    def client(self):
        if self._client is None:
            self._secret = self._secret or load_api_key()
            self._client = make_client(self._secret)
        return self._client

    # -- estimates
    def prompt_tokens(self, params: dict) -> int:
        if self.token_estimate == "bytes":
            return bytes_upper_bound(params)
        args = {k: params[k] for k in COUNT_KEYS if k in params}
        with guarded(self._secret):
            n = _attr(self.client.messages.count_tokens(**args), "input_tokens")
        return math.ceil(int(n) * COUNT_MARGIN)

    def worst_case(self, params: dict, *, batch: bool, prompt_tokens: int | None = None) -> float:
        pt = self.prompt_tokens(params) if prompt_tokens is None else prompt_tokens
        return models.worst_case_usd(params["model"], prompt_tokens=pt, max_tokens=int(params["max_tokens"]),
                                     cache_ttl=cache_ttl_of(params), batch=batch)

    # -- sync
    def message(self, *, model: str = "haiku", max_tokens: int, note: str = "", **kw) -> MessageResult:
        """One Messages API call (dev runs; use Haiku). kw: user= or messages=, system=,
        cache_system=, cache_ttl=, and other Messages params (not temperature/top_p/top_k)."""
        params = build_params(model=model, max_tokens=max_tokens, **kw)
        worst = self.worst_case(params, batch=False)
        token = self.budget.reserve(worst, what=f"{params['model']} message")
        try:
            with guarded(self._secret):
                resp = self.client.messages.create(**params)
            u = _usage_dict(resp.usage)
            mid = _attr(resp, "model") or params["model"]
            cost = models.cost_usd(params["model"], batch=False, **u)
            rid = getattr(resp, "_request_id", None) or _attr(resp, "id")
            usage.append_rows(self.usage_csv, [{
                "job": self.job, "repo": self.repo, "model_id": mid, "mode": "sync", "request_id": rid,
                "input_tokens": u["input_tokens"], "cache_creation_input_tokens": u["cache_creation_input_tokens"],
                "cache_read_input_tokens": u["cache_read_input_tokens"], "output_tokens": u["output_tokens"],
                "cost_usd": cost, "note": note}])
        finally:
            self.budget.release(token)
        return MessageResult(text=_text_of(resp), model_id=mid, request_id=rid,
                             stop_reason=_attr(resp, "stop_reason"), usage=u, cost_usd=cost, raw=resp)

    # -- batch
    def _state_path(self, name: str) -> Path:
        import re
        if not re.fullmatch(r"[A-Za-z0-9_.-]{1,100}", name):
            raise ValueError(f"batch name must be [A-Za-z0-9_.-]{{1,100}}: {name!r}")
        return self.batch_dir / f"{self.job}__{name}.json"

    def _read_state(self, name: str) -> dict | None:
        p = self._state_path(name)
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None

    def _write_state(self, name: str, st: dict) -> None:
        p = self._state_path(name)
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(st, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(tmp, p)

    def batch_submit(self, requests: Iterable[dict], *, name: str | None = None) -> dict:
        """Submit a Message Batch once. Re-running with the same requests (and name) returns the saved
        state instead of resubmitting. name defaults to a hash of the requests."""
        reqs = [{"custom_id": r["custom_id"], "params": _validate_params(r["params"])} for r in requests]
        if not reqs:
            raise ValueError("no requests")
        ids = [r["custom_id"] for r in reqs]
        if len(set(ids)) != len(ids):
            raise ValueError("custom_id values must be unique within a batch")
        if len(reqs) > 100_000:
            raise ValueError("a batch holds at most 100,000 requests")
        digest = hashlib.sha256(json.dumps(reqs, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        name = name or f"b{digest[:12]}"
        st = self._read_state(name)
        if st is not None:
            if st.get("requests_sha256") != digest:
                raise BatchStateError(f"batch {name!r} for job {self.job!r} already exists with different "
                                      f"requests; pick another name")
            if not st.get("batch_id"):
                raise BatchStateError(
                    f"batch {name!r} was being submitted when a previous run stopped, and its id was not "
                    f"saved. Check the Console (or client.messages.batches.list()) before resubmitting; "
                    f"then put the id in {self._state_path(name)} or move that file away.")
            log.info("batch %s already submitted (%s); not resubmitting", name, st["batch_id"])
            return st
        # Worst case of the whole batch, counted before anything is sent.
        if self.token_estimate == "count" and len(reqs) > 1:
            with ThreadPoolExecutor(max_workers=self.count_workers) as ex:
                pts = list(ex.map(lambda r: self.prompt_tokens(r["params"]), reqs))
        else:
            pts = [self.prompt_tokens(r["params"]) for r in reqs]
        worst = sum(self.worst_case(r["params"], batch=True, prompt_tokens=pt) for r, pt in zip(reqs, pts))
        model_ids = sorted({r["params"]["model"] for r in reqs})
        st = {"job": self.job, "repo": self.repo, "name": name, "requests_sha256": digest,
              "n_requests": len(reqs), "model_ids": model_ids, "worst_case_usd": round(worst, 6),
              "status": "submitting", "batch_id": None, "created_utc": usage.now_utc()}
        with self.budget._lock:  # check and claim atomically against other threads of this process
            self.budget._check_locked(worst, what=f"batch {name} ({len(reqs)} requests)")
            self._write_state(name, st)  # from here the worst case counts as reserved
        try:
            with guarded(self._secret):
                b = self.client.messages.batches.create(requests=reqs)
        except Exception as e:
            code = getattr(e, "status_code", None)
            if isinstance(code, int) and 400 <= code < 500:
                # The API refused the request, so no batch exists: release the reservation.
                st.update(status="failed_to_submit", worst_case_usd=0.0, error=f"HTTP {code}")
                self._write_state(name, st)
                self._state_path(name).replace(self._state_path(name).with_suffix(".failed.json"))
            # Otherwise (timeout, 5xx, network) a batch may exist: keep "submitting", which holds the
            # reservation and makes a re-run stop and ask for a manual check instead of paying twice.
            raise
        st.update(batch_id=_attr(b, "id"), status="submitted",
                  processing_status=_attr(b, "processing_status"))
        self._write_state(name, st)
        log.info("submitted batch %s: %s (%d requests, worst case $%.4f)", name, st["batch_id"], len(reqs), worst)
        return st

    def batch_poll(self, name: str, *, wait: bool = False, interval: float = 60.0,
                   timeout: float | None = None, sleep=time.sleep) -> dict:
        """Refresh the batch's status from the API. With wait=True, poll until it has ended."""
        st = self._read_state(name)
        if st is None or not st.get("batch_id"):
            raise BatchStateError(f"no submitted batch {name!r} for job {self.job!r}")
        if st["status"] in ("ended", "logged"):
            return st
        start = time.monotonic()
        while True:
            with guarded(self._secret):
                b = self.client.messages.batches.retrieve(st["batch_id"])
            ps = _attr(b, "processing_status")
            rc = _attr(b, "request_counts")
            st["processing_status"] = ps
            st["request_counts"] = ({k: _attr(rc, k) for k in ("processing", "succeeded", "errored",
                                                                 "canceled", "expired")} if rc is not None else None)
            if ps == "ended":
                st["status"] = "ended"
            self._write_state(name, st)
            if ps == "ended" or not wait:
                return st
            if timeout is not None and time.monotonic() - start > timeout:
                return st
            sleep(interval)

    def batch_results(self, name: str) -> list[BatchItem]:
        """Results of an ended batch. The first call downloads them to
        results/jzapi_batches/<job>__<name>.results.jsonl and logs one usage row per result; later
        calls read that file and log nothing."""
        st = self._read_state(name)
        if st is None or not st.get("batch_id"):
            raise BatchStateError(f"no submitted batch {name!r} for job {self.job!r}")
        out_path = self._state_path(name).with_suffix(".results.jsonl")
        if st["status"] == "logged":
            return [BatchItem(**json.loads(line)) for line in out_path.read_text(encoding="utf-8").splitlines() if line]
        if st["status"] != "ended":
            st = self.batch_poll(name)
            if st["status"] != "ended":
                raise BatchStateError(f"batch {name!r} has not ended yet ({st.get('processing_status')})")
        items: list[BatchItem] = []
        with guarded(self._secret):
            for r in self.client.messages.batches.results(st["batch_id"]):
                res = _attr(r, "result")
                typ = _attr(res, "type")
                if typ == "succeeded":
                    msg = _attr(res, "message")
                    u = _usage_dict(_attr(msg, "usage"))
                    mid = _attr(msg, "model")
                    items.append(BatchItem(custom_id=_attr(r, "custom_id"), type=typ, text=_text_of(msg),
                                           model_id=mid, stop_reason=_attr(msg, "stop_reason"), usage=u,
                                           cost_usd=models.cost_usd(mid, batch=True, **u)))
                else:  # errored / canceled / expired are not billed
                    err = _attr(res, "error")
                    items.append(BatchItem(custom_id=_attr(r, "custom_id"), type=typ, text=None, model_id=None,
                                           stop_reason=None, usage={}, cost_usd=0.0,
                                           error=json.dumps(err, default=lambda o: getattr(o, "__dict__", str(o)))
                                           if err is not None else None))
        tmp = out_path.with_suffix(".jsonl.tmp")
        tmp.write_text("".join(json.dumps(it.__dict__, ensure_ascii=False) + "\n" for it in items), encoding="utf-8")
        os.replace(tmp, out_path)
        # Log, skipping rows a crashed earlier run already wrote for this batch.
        tag = f"batch={st['batch_id']}"
        logged = {r["request_id"] for r in usage.read_rows(self.usage_csv)
                  if r.get("job") == self.job and tag in (r.get("note") or "")}
        rows = []
        for it in items:
            if it.custom_id in logged:
                continue
            u = it.usage
            rows.append({"job": self.job, "repo": self.repo, "model_id": it.model_id or ",".join(st["model_ids"]),
                         "mode": "batch", "request_id": it.custom_id,
                         "input_tokens": u.get("input_tokens", 0),
                         "cache_creation_input_tokens": u.get("cache_creation_input_tokens", 0),
                         "cache_read_input_tokens": u.get("cache_read_input_tokens", 0),
                         "output_tokens": u.get("output_tokens", 0), "cost_usd": it.cost_usd,
                         "note": tag if it.type == "succeeded" else f"{tag} {it.type} (not billed)"})
        usage.append_rows(self.usage_csv, rows)
        st["status"] = "logged"
        st["logged_utc"] = usage.now_utc()
        st["actual_cost_usd"] = round(sum(it.cost_usd for it in items), 6)
        self._write_state(name, st)
        return items


# ----------------------------------------------------------------------------- module-level helpers
_sessions: dict[tuple, Session] = {}


def session(job: str, **kw) -> Session:
    """A cached Session per (job, repo_dir). kw as for Session (only used on first creation)."""
    repo = Path(kw["repo_dir"]).resolve() if kw.get("repo_dir") else find_repo_root()
    key = (job, str(repo))
    if key not in _sessions:
        _sessions[key] = Session(job, **{**kw, "repo_dir": repo})
    return _sessions[key]


def message(job: str, *, model: str = "haiku", max_tokens: int, note: str = "", repo_dir=None, **kw) -> MessageResult:
    return session(job, repo_dir=repo_dir).message(model=model, max_tokens=max_tokens, note=note, **kw)


def batch_submit(job: str, requests: Iterable[dict], *, name: str | None = None, repo_dir=None) -> dict:
    return session(job, repo_dir=repo_dir).batch_submit(requests, name=name)


def batch_poll(job: str, name: str, *, wait: bool = False, interval: float = 60.0, timeout: float | None = None,
               repo_dir=None) -> dict:
    return session(job, repo_dir=repo_dir).batch_poll(name, wait=wait, interval=interval, timeout=timeout)


def batch_results(job: str, name: str, *, repo_dir=None) -> list[BatchItem]:
    return session(job, repo_dir=repo_dir).batch_results(name)


__all__ = ["Session", "session", "message", "batch_submit", "batch_poll", "batch_results", "request",
           "build_params", "system_blocks", "MessageResult", "BatchItem", "BatchStateError", "BudgetError"]

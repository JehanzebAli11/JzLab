"""results/usage.csv: one row per sync call and per batch result. Appends are locked."""
from __future__ import annotations

import csv
import fcntl
import io
import os
import threading
from datetime import datetime, timezone
from pathlib import Path

COLUMNS = ["timestamp_utc", "job", "repo", "model_id", "mode", "request_id", "input_tokens",
           "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens", "cost_usd",
           "note"]

_thread_lock = threading.Lock()


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _format(row: dict) -> dict:
    out = {c: row.get(c, "") for c in COLUMNS}
    unknown = set(row) - set(COLUMNS)
    if unknown:
        raise ValueError(f"unknown usage columns: {sorted(unknown)}")
    if not out["timestamp_utc"]:
        out["timestamp_utc"] = now_utc()
    for c in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens",
              "output_tokens"):
        out[c] = int(out[c] or 0)
    out["cost_usd"] = f"{float(out['cost_usd'] or 0):.6f}"
    return out


def append_rows(path: str | Path, rows: list[dict]) -> None:
    """Append rows under an exclusive file lock (threads and processes); header if the file is new."""
    if not rows:
        return
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLUMNS, lineterminator="\n")
    for r in rows:
        w.writerow(_format(r))
    with _thread_lock:
        with open(path, "a+", encoding="utf-8", newline="") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                f.seek(0, os.SEEK_END)
                if f.tell() == 0:
                    f.write(",".join(COLUMNS) + "\n")
                f.write(buf.getvalue())
                f.flush()
                os.fsync(f.fileno())
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def read_rows(path: str | Path) -> list[dict]:
    path = Path(path)
    if not path.exists():
        return []
    with _thread_lock:
        with open(path, encoding="utf-8", newline="") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_SH)
            try:
                return list(csv.DictReader(f))
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def spent_usd(path: str | Path, job: str) -> float:
    return sum(float(r.get("cost_usd") or 0) for r in read_rows(path) if r.get("job") == job)

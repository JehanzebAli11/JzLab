"""Offline stand-ins for the anthropic SDK client (no network, no key)."""
from __future__ import annotations

from types import SimpleNamespace as NS


def usage(inp=10, out=5, cc=0, cr=0, cc1h=0):
    return NS(input_tokens=inp, output_tokens=out, cache_creation_input_tokens=cc, cache_read_input_tokens=cr,
              cache_creation=NS(ephemeral_5m_input_tokens=cc - cc1h, ephemeral_1h_input_tokens=cc1h))


def message(text="ok", model="claude-haiku-5-5", **u):
    m = NS(id="msg_fake", model=model, stop_reason="end_turn", content=[NS(type="text", text=text)],
           usage=usage(**u))
    m._request_id = "req_fake"
    return m


class FakeMessages:
    def __init__(self, parent):
        self.p = parent
        self.batches = FakeBatches(parent)

    def create(self, **params):
        self.p.calls.append(("create", params))
        if self.p.raise_on_create is not None:
            raise self.p.raise_on_create
        return self.p.next_message or message(model=params["model"])

    def count_tokens(self, **params):
        self.p.calls.append(("count_tokens", params))
        assert "max_tokens" not in params
        return NS(input_tokens=self.p.count_value)


class FakeBatches:
    def __init__(self, parent):
        self.p = parent

    def create(self, *, requests):
        self.p.calls.append(("batch_create", requests))
        if self.p.raise_on_batch_create is not None:
            raise self.p.raise_on_batch_create
        self.p.batch_requests = list(requests)
        return NS(id="msgbatch_fake1", processing_status="in_progress")

    def retrieve(self, batch_id):
        self.p.calls.append(("batch_retrieve", batch_id))
        status = self.p.statuses.pop(0) if self.p.statuses else "ended"
        return NS(id=batch_id, processing_status=status,
                  request_counts=NS(processing=0, succeeded=len(self.p.batch_requests or []), errored=0,
                                    canceled=0, expired=0))

    def results(self, batch_id):
        self.p.calls.append(("batch_results", batch_id))
        out = []
        for r in self.p.batch_requests:
            cid = r["custom_id"]
            if cid in self.p.errored:
                out.append(NS(custom_id=cid, result=NS(type="errored", error={"type": "error", "error": {
                    "type": "api_error", "message": "boom"}})))
            else:
                out.append(NS(custom_id=cid, result=NS(type="succeeded", message=message(
                    text=f"answer {cid}", model=r["params"]["model"], **self.p.batch_usage))))
        return iter(out)


class FakeClient:
    def __init__(self, count_value=100):
        self.calls = []
        self.count_value = count_value
        self.next_message = None
        self.raise_on_create = None
        self.raise_on_batch_create = None
        self.batch_requests = None
        self.statuses = []
        self.errored = set()
        self.batch_usage = {"inp": 100, "out": 50}
        self.messages = FakeMessages(self)
        self.models = NS(list=lambda **kw: [NS(id="claude-opus-5-5"), NS(id="claude-sonnet-5-5"),
                                            NS(id="claude-haiku-5-5")])

    def n(self, kind):
        return sum(1 for c in self.calls if c[0] == kind)


class StatusError(Exception):
    def __init__(self, code, msg="error"):
        super().__init__(msg)
        self.status_code = code

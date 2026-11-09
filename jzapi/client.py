"""SDK client construction and a guard that keeps the key out of exceptions."""
from __future__ import annotations

from .keys import Secret, load_api_key, scrub


class JzApiError(RuntimeError):
    """An API/SDK error, re-raised with the key scrubbed from its message."""


def make_client(secret: Secret | None = None, *, timeout: float = 120.0, max_retries: int = 2):
    import anthropic  # imported lazily so offline tests never need the SDK's network stack

    secret = secret or load_api_key()
    # One credential per client (anthropic SDK >= 2.0 raises if more than one is given).
    return anthropic.Anthropic(api_key=secret.reveal(), timeout=timeout, max_retries=max_retries)


class guarded:
    """Context manager: re-raise any exception whose text contains the key as a JzApiError without it.

    The new error is raised `from None` (tracebacks do not show the original), and the original's
    args and string attributes are scrubbed in place too. Other exceptions pass through unchanged.
    """

    def __init__(self, secret: Secret | None):
        self.secret = secret

    def __enter__(self):
        return self

    def __exit__(self, et, e, tb):
        if e is None or self.secret is None or not self.secret.reveal() or not isinstance(e, Exception):
            return False
        v = self.secret.reveal()
        attrs = {k: a for k, a in vars(e).items() if isinstance(a, str)} if hasattr(e, "__dict__") else {}
        text = f"{e} {e.args!r} {attrs!r}"
        if v not in text:
            return False
        msg = scrub(f"{type(e).__name__}: {e}", self.secret)
        e.args = tuple(scrub(a, self.secret) if isinstance(a, str) else
                       (scrub(repr(a), self.secret) if v in repr(a) else a) for a in e.args)
        for k, a in attrs.items():
            try:
                setattr(e, k, scrub(a, self.secret))
            except Exception:  # noqa: BLE001
                pass
        e.__traceback__ = None
        raise JzApiError(msg) from None

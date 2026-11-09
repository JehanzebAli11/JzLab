"""Pinned model IDs and prices. Change them only after re-checking the sources below.

Prices: https://platform.claude.com/docs/en/about-claude/pricing (checked 2026-11-09)
  "Model pricing" table, "Batch processing" (50% off input and output; "Batch API and
  prompt caching discounts can be combined"), and the Haiku 5.5 prompt-length tiers
  ("a request whose prompt is over 100,000 tokens pays higher prices. A request's prompt
  length counts all of its input tokens, including cache reads and cache writes").
Cache multipliers: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
  (checked 2026-11-09): 5m write 1.25x, 1h write 2x, read 0.1x (0.05x on Opus 5.5 and
  Sonnet 5.5). The per-model dollar figures below are the table values; they match those
  multipliers.
Model IDs: https://platform.claude.com/docs/en/about-claude/models/overview (checked
  2026-11-09), and verified live with GET /v1/models (`python -m jzapi.models --verify`).
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass

PRICE_SOURCE = "https://platform.claude.com/docs/en/about-claude/pricing"
PRICE_CHECKED = "2026-11-09"
MODELS_SOURCE = "https://platform.claude.com/docs/en/about-claude/models/overview"
BATCH_MULTIPLIER = 0.5  # applied to every token class in a batch (input, output, cache write/read)

ROLES: dict[str, str] = {
    "haiku": "claude-haiku-5-5",    # dev runs
    "sonnet": "claude-sonnet-5-5",  # default
    "opus": "claude-opus-5-5",      # final sets, red-teaming
}


@dataclass(frozen=True)
class Tier:
    """USD per million tokens, standard (non-batch) prices."""
    input: float
    output: float
    cache_write_5m: float
    cache_write_1h: float
    cache_read: float
    max_prompt_tokens: int | None = None  # tier applies to prompts <= this; None = no limit


PRICES: dict[str, tuple[Tier, ...]] = {
    "claude-opus-5-5": (Tier(4.00, 20.00, 5.00, 8.00, 0.20),),
    "claude-sonnet-5-5": (Tier(2.00, 10.00, 2.50, 4.00, 0.10),),
    "claude-haiku-5-5": (
        Tier(0.10, 0.50, 0.125, 0.20, 0.01, max_prompt_tokens=100_000),
        Tier(0.50, 2.50, 0.625, 1.00, 0.05),
    ),
}


class UnknownModel(ValueError):
    pass


def resolve(model: str) -> str:
    """Role name ('haiku'/'sonnet'/'opus') or a pinned ID -> pinned ID. Anything else is refused."""
    if model in ROLES:
        return ROLES[model]
    if model in PRICES:
        return model
    for mid in PRICES:  # a dated snapshot of a pinned model, as a response may report it
        if model.startswith(mid + "-") and model[len(mid) + 1:].isdigit():
            return mid
    raise UnknownModel(f"model {model!r} is not pinned in jzapi.models (roles: {sorted(ROLES)}); "
                       f"add it with a checked price first")


def tier_for(model_id: str, prompt_tokens: int) -> Tier:
    for t in PRICES[resolve(model_id)]:
        if t.max_prompt_tokens is None or prompt_tokens <= t.max_prompt_tokens:
            return t
    raise AssertionError("price table has no open-ended tier")


def cost_usd(model: str, *, input_tokens: int = 0, output_tokens: int = 0,
             cache_creation_input_tokens: int = 0, cache_read_input_tokens: int = 0,
             cache_write_1h_tokens: int = 0, batch: bool = False) -> float:
    """Billed cost of one request from its usage numbers.

    input_tokens is the uncached part (after the last cache breakpoint), as the API reports
    it. cache_write_1h_tokens is the part of cache_creation_input_tokens written with a 1h
    TTL (usage.cache_creation.ephemeral_1h_input_tokens); the rest is billed as 5m writes.
    """
    mid = resolve(model)
    prompt = input_tokens + cache_creation_input_tokens + cache_read_input_tokens
    t = tier_for(mid, prompt)
    w1h = min(cache_write_1h_tokens, cache_creation_input_tokens)
    w5m = cache_creation_input_tokens - w1h
    usd = (input_tokens * t.input + output_tokens * t.output + w5m * t.cache_write_5m
           + w1h * t.cache_write_1h + cache_read_input_tokens * t.cache_read) / 1_000_000
    return usd * (BATCH_MULTIPLIER if batch else 1.0)


def worst_case_usd(model: str, *, prompt_tokens: int, max_tokens: int, cache_ttl: str | None = None,
                   batch: bool = False) -> float:
    """Upper bound for one request: every prompt token at the dearest input rate the request can
    incur (a cache write if it caches, else plain input), plus max_tokens of output."""
    mid = resolve(model)
    t = tier_for(mid, prompt_tokens)
    rate = {None: t.input, "5m": t.cache_write_5m, "1h": t.cache_write_1h}[cache_ttl]
    usd = (prompt_tokens * max(rate, t.input) + max_tokens * t.output) / 1_000_000
    return usd * (BATCH_MULTIPLIER if batch else 1.0)


def verify_live(client=None) -> dict:
    """GET /v1/models (free). Returns {'available': [...ids], 'missing': [...pinned ids not listed]}."""
    if client is None:
        from .client import make_client
        client = make_client()
    ids = sorted(m.id for m in client.models.list(limit=1000))
    return {"available": ids, "missing": sorted(set(ROLES.values()) - set(ids))}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Show the pinned models and prices; --verify checks "
                                             "the IDs with the free GET /v1/models call.")
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args(argv)
    print(f"prices: {PRICE_SOURCE} (checked {PRICE_CHECKED}); batch x{BATCH_MULTIPLIER}")
    for role, mid in ROLES.items():
        for t in PRICES[mid]:
            lim = f" (prompt <= {t.max_prompt_tokens:,})" if t.max_prompt_tokens else ""
            print(f"  {role:6s} {mid}{lim}: in ${t.input} out ${t.output} cw5m ${t.cache_write_5m} "
                  f"cw1h ${t.cache_write_1h} cr ${t.cache_read} per MTok")
    if args.verify:
        res = verify_live()
        print("GET /v1/models returned:", ", ".join(res["available"]))
        if res["missing"]:
            print("MISSING pinned IDs:", ", ".join(res["missing"]))
            return 1
        print("all pinned IDs are listed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

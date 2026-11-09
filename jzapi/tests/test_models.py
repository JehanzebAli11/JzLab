import random

import pytest

from jzapi import models
from jzapi.budget import load_budgets


def test_roles_pinned():
    assert models.ROLES == {"haiku": "claude-haiku-5-5", "sonnet": "claude-sonnet-5-5", "opus": "claude-opus-5-5"}
    assert models.resolve("sonnet") == "claude-sonnet-5-5"
    assert models.resolve("claude-opus-5-5") == "claude-opus-5-5"
    assert models.resolve("claude-sonnet-5-5-20261001") == "claude-sonnet-5-5"
    for bad in ("claude-sonnet-4-5", "claude-sonnet-5-5-preview", "claude-sonnet-5"):
        with pytest.raises(models.UnknownModel):
            models.resolve(bad)
    assert models.PRICE_SOURCE.startswith("https://") and models.PRICE_CHECKED == "2026-11-09"


def test_prices_follow_documented_multipliers():
    for mid, tiers in models.PRICES.items():
        for t in tiers:
            assert t.cache_write_5m == pytest.approx(1.25 * t.input)
            assert t.cache_write_1h == pytest.approx(2 * t.input)
            read = 0.05 if mid in ("claude-opus-5-5", "claude-sonnet-5-5") else 0.1
            assert t.cache_read == pytest.approx(read * t.input)


def test_cost_sync_and_batch():
    c = models.cost_usd("sonnet", input_tokens=1_000_000, output_tokens=1_000_000)
    assert c == pytest.approx(12.0)
    assert models.cost_usd("sonnet", input_tokens=1_000_000, output_tokens=1_000_000, batch=True) == pytest.approx(6.0)
    assert models.cost_usd("opus", input_tokens=1_000_000, output_tokens=1_000_000, batch=True) == pytest.approx(12.0)


def test_cost_cache_tokens():
    c = models.cost_usd("opus", input_tokens=0, cache_creation_input_tokens=1_000_000, cache_write_1h_tokens=400_000,
                        cache_read_input_tokens=1_000_000)
    assert c == pytest.approx(0.6 * 5 + 0.4 * 8 + 0.20)


def test_haiku_long_prompt_tier_counts_cache_tokens():
    short = models.cost_usd("haiku", input_tokens=100_000, output_tokens=0)
    assert short == pytest.approx(0.01)
    long_ = models.cost_usd("haiku", input_tokens=50_000, cache_read_input_tokens=50_001, output_tokens=0)
    assert long_ == pytest.approx((50_000 * 0.50 + 50_001 * 0.05) / 1e6)


def test_worst_case_bounds_any_real_cost():
    rng = random.Random(0)
    for _ in range(2000):
        model = rng.choice(list(models.ROLES))
        batch = rng.random() < 0.5
        ttl = rng.choice([None, "5m", "1h"])
        prompt = rng.randint(1, 300_000)
        max_tokens = rng.randint(1, 8000)
        cc = 0 if ttl is None else rng.randint(0, prompt)
        cr = 0 if ttl is None else rng.randint(0, prompt - cc)
        inp = prompt - cc - cr
        c = models.cost_usd(model, input_tokens=inp, output_tokens=rng.randint(0, max_tokens),
                            cache_creation_input_tokens=cc, cache_read_input_tokens=cr,
                            cache_write_1h_tokens=cc if ttl == "1h" else 0, batch=batch)
        w = models.worst_case_usd(model, prompt_tokens=prompt, max_tokens=max_tokens, cache_ttl=ttl, batch=batch)
        assert c <= w + 1e-12


def test_budgets_yaml_mirrors_roadmap():
    jobs = load_budgets()
    caps = {j: b.cap_usd for j, b in jobs.items()}
    assert caps == {"lit_rq3": 20, "validator_redteam": 25, "firewall_part2": 40, "architect_ladder": 90,
                    "p1_player": 60, "m3_explorer": 30, "m4_safety": 50, "applications": 15, "reserve": 70}
    assert sum(caps.values()) == 400
    assert [j for j, b in jobs.items() if b.approved] == ["lit_rq3"]


def test_verify_live_with_fake(fake):
    res = models.verify_live(fake)
    assert res["missing"] == [] and "claude-opus-5-5" in res["available"]

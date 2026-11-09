import csv

import pytest

import jzapi
from jzapi import Session, request
from jzapi.api import COUNT_MARGIN, build_params, bytes_upper_bound, cache_ttl_of
from jzapi.budget import BudgetExceeded, JobNotApproved

from .fakes import message as fake_message


def rows(repo):
    return list(csv.DictReader((repo / "results/usage.csv").open()))


def test_message_logs_one_row_with_cost(repo, fake):
    fake.next_message = fake_message(text="hello", model="claude-haiku-5-5", inp=1000, out=200, cc=600, cr=400)
    r = Session("lit_rq3", repo_dir=repo, client=fake).message(user="hi", system="sys", max_tokens=300, note="dev")
    assert r.text == "hello" and r.request_id == "req_fake"
    expected = (1000 * 0.10 + 200 * 0.50 + 600 * 0.125 + 400 * 0.01) / 1e6
    assert r.cost_usd == pytest.approx(expected)
    (row,) = rows(repo)
    assert row["job"] == "lit_rq3" and row["repo"] == "fake-repo" and row["mode"] == "sync"
    assert row["model_id"] == "claude-haiku-5-5" and row["note"] == "dev"
    assert (row["input_tokens"], row["cache_creation_input_tokens"], row["cache_read_input_tokens"],
            row["output_tokens"]) == ("1000", "600", "400", "200")
    assert float(row["cost_usd"]) == pytest.approx(expected, abs=1e-6)


def test_count_tokens_used_for_worst_case(repo, fake):
    fake.count_value = 1000
    s = Session("lit_rq3", repo_dir=repo, client=fake)
    p = build_params(model="opus", user="x", max_tokens=100)
    assert s.prompt_tokens(p) == int(1000 * COUNT_MARGIN)
    (_, sent) = [c for c in fake.calls if c[0] == "count_tokens"][0]
    assert set(sent) == {"model", "messages"}


def test_budget_refuses_before_calling(repo, fake):
    fake.count_value = 900_000
    s = Session("lit_rq3", repo_dir=repo, client=fake, cap_usd=1)
    with pytest.raises(BudgetExceeded):
        s.message(model="opus", user="big", max_tokens=1000)
    assert fake.n("create") == 0
    assert not (repo / "results/usage.csv").exists()


def test_unapproved_job_never_calls(repo, fake):
    with pytest.raises(JobNotApproved):
        Session("architect_ladder", repo_dir=repo, client=fake).message(user="x", max_tokens=5)
    assert fake.calls == []


def test_temperature_refused(repo, fake):
    with pytest.raises(ValueError, match="2026-10-21"):
        Session("lit_rq3", repo_dir=repo, client=fake).message(user="x", max_tokens=5, temperature=0)
    with pytest.raises(ValueError):
        request("a", model="sonnet", user="x", max_tokens=5, top_p=0.9)


def test_unknown_model_refused(repo, fake):
    with pytest.raises(ValueError, match="not pinned"):
        Session("lit_rq3", repo_dir=repo, client=fake).message(model="claude-3-haiku", user="x", max_tokens=5)


def test_failed_call_releases_reservation_and_logs_nothing(repo, fake):
    s = Session("lit_rq3", repo_dir=repo, client=fake)
    fake.raise_on_create = RuntimeError("503")
    with pytest.raises(RuntimeError):
        s.message(user="x", max_tokens=5)
    assert s.budget._inflight == {}
    assert not (repo / "results/usage.csv").exists()


def test_cache_control_on_system_block():
    p = build_params(model="sonnet", system="long shared prompt", cache_system=True, user="doc", max_tokens=10)
    assert p["system"] == [{"type": "text", "text": "long shared prompt", "cache_control": {"type": "ephemeral"}}]
    assert cache_ttl_of(p) == "5m"
    p1h = build_params(model="sonnet", system="s", cache_system=True, cache_ttl="1h", user="d", max_tokens=10)
    assert p1h["system"][-1]["cache_control"] == {"type": "ephemeral", "ttl": "1h"}
    assert cache_ttl_of(p1h) == "1h"
    assert cache_ttl_of(build_params(model="sonnet", system="s", user="d", max_tokens=10)) is None


def test_bytes_bound_needs_no_network(repo, fake):
    s = Session("lit_rq3", repo_dir=repo, client=fake, token_estimate="bytes")
    p = build_params(model="sonnet", system="سسٹم", user="اردو متن " * 50, max_tokens=10)
    assert s.prompt_tokens(p) == bytes_upper_bound(p) > len("اردو متن " * 50)
    assert fake.n("count_tokens") == 0


def test_module_level_message_uses_cwd_repo(repo, fake, monkeypatch):
    monkeypatch.chdir(repo)
    jzapi.session("lit_rq3", client=fake)
    jzapi.message("lit_rq3", user="x", max_tokens=5)
    assert len(rows(repo)) == 1

import csv
import json

import pytest

from jzapi import Session, request
from jzapi.api import BatchStateError
from jzapi.budget import BudgetExceeded

from .fakes import StatusError

SYSTEM = "You are a helpful assistant. Summarise the user's document in 2-3 sentences."


def rq3_requests(model, n=3):
    # The shape the LIT RQ3 run needs: one shared (cached) system prompt, one document per request.
    return [request(f"{model}-same-item{i}-ur", model=model, system=SYSTEM, cache_system=True,
                    user=f"Please summarise this document:\n\nدستاویز {i}", max_tokens=200) for i in range(n)]


def usage_rows(repo):
    p = repo / "results/usage.csv"
    return list(csv.DictReader(p.open())) if p.exists() else []


def test_submit_is_resumable(repo, fake):
    s = Session("lit_rq3", repo_dir=repo, client=fake)
    st = s.batch_submit(rq3_requests("sonnet"), name="rq3_sonnet")
    assert st["batch_id"] == "msgbatch_fake1" and st["status"] == "submitted" and st["n_requests"] == 3
    assert st["model_ids"] == ["claude-sonnet-5-5"] and st["worst_case_usd"] > 0
    sent = fake.batch_requests[0]["params"]
    assert sent["model"] == "claude-sonnet-5-5" and sent["system"][0]["cache_control"] == {"type": "ephemeral"}
    s2 = Session("lit_rq3", repo_dir=repo, client=fake)  # a re-run of the script
    assert s2.batch_submit(rq3_requests("sonnet"), name="rq3_sonnet")["batch_id"] == "msgbatch_fake1"
    assert fake.n("batch_create") == 1
    with pytest.raises(BatchStateError, match="different requests"):
        s2.batch_submit(rq3_requests("sonnet", n=4), name="rq3_sonnet")


def test_default_name_is_request_hash(repo, fake):
    s = Session("lit_rq3", repo_dir=repo, client=fake)
    a = s.batch_submit(rq3_requests("opus"))
    b = s.batch_submit(rq3_requests("opus"))
    assert a["name"] == b["name"] and fake.n("batch_create") == 1


def test_batch_budget_refused_before_submit(repo, fake):
    fake.count_value = 200_000
    s = Session("lit_rq3", repo_dir=repo, client=fake)
    with pytest.raises(BudgetExceeded):
        s.batch_submit(rq3_requests("opus", n=60), name="huge")  # 60 x 200k x $5/MTok x 0.5 x 1.05 > $20
    assert fake.n("batch_create") == 0
    assert not list((repo / "results").rglob("*.json")) if (repo / "results").exists() else True


def test_pending_batch_reserves_budget(repo, fake):
    fake.count_value = 30_000
    s = Session("lit_rq3", repo_dir=repo, client=fake)
    s.batch_submit(rq3_requests("opus", n=50), name="first")   # worst ~ 50 x (31.5k x $2.5 + 200 x $10)/1e6 ~ $4.04
    with pytest.raises(BudgetExceeded):
        for i in range(10):
            s.batch_submit(rq3_requests("opus", n=50 + i), name=f"more{i}")
    assert fake.n("batch_create") < 6


def test_poll_wait_and_results_logged_once(repo, fake):
    s = Session("lit_rq3", repo_dir=repo, client=fake)
    reqs = rq3_requests("sonnet")
    s.batch_submit(reqs, name="r")
    fake.statuses = ["in_progress", "in_progress", "ended"]
    sleeps = []
    st = s.batch_poll("r", wait=True, interval=5, sleep=sleeps.append)
    assert st["status"] == "ended" and sleeps == [5, 5] and st["request_counts"]["succeeded"] == 3
    fake.errored = {reqs[1]["custom_id"]}
    fake.batch_usage = {"inp": 1000, "out": 100, "cc": 0, "cr": 600}
    items = s.batch_results("r")
    assert [i.type for i in items] == ["succeeded", "errored", "succeeded"]
    ok = items[0]
    assert ok.text.startswith("answer") and ok.cost_usd == pytest.approx((1000 * 2 + 100 * 10 + 600 * 0.10) / 1e6 * 0.5)
    assert items[1].cost_usd == 0 and "boom" in items[1].error
    rows = usage_rows(repo)
    assert len(rows) == 3 and all(r["mode"] == "batch" for r in rows)
    assert [r["request_id"] for r in rows] == [r["custom_id"] for r in reqs]
    assert "not billed" in rows[1]["note"] and rows[0]["note"] == "batch=msgbatch_fake1"
    again = s.batch_results("r")  # a re-run reads the saved file and logs nothing
    assert [i.custom_id for i in again] == [i.custom_id for i in items]
    assert len(usage_rows(repo)) == 3 and fake.n("batch_results") == 1
    state = json.loads((repo / "results/jzapi_batches/lit_rq3__r.json").read_text())
    assert state["status"] == "logged" and state["actual_cost_usd"] == pytest.approx(2 * ok.cost_usd, abs=1e-6)
    assert s.budget.reserved_batches() == 0


def test_results_after_crash_do_not_double_log(repo, fake):
    s = Session("lit_rq3", repo_dir=repo, client=fake)
    reqs = rq3_requests("sonnet")
    s.batch_submit(reqs, name="r")
    s.batch_poll("r")
    s.batch_results("r")
    p = repo / "results/jzapi_batches/lit_rq3__r.json"
    st = json.loads(p.read_text())
    st["status"] = "ended"  # pretend the run died after logging but before marking "logged"
    p.write_text(json.dumps(st))
    s.batch_results("r")
    assert len(usage_rows(repo)) == 3


def test_results_before_end_refused(repo, fake):
    s = Session("lit_rq3", repo_dir=repo, client=fake)
    s.batch_submit(rq3_requests("sonnet"), name="r")
    fake.statuses = ["in_progress"]
    with pytest.raises(BatchStateError, match="not ended"):
        s.batch_results("r")


def test_client_error_on_submit_releases_reservation(repo, fake):
    s = Session("lit_rq3", repo_dir=repo, client=fake)
    fake.raise_on_batch_create = StatusError(400, "invalid")
    with pytest.raises(StatusError):
        s.batch_submit(rq3_requests("sonnet"), name="r")
    assert s.budget.reserved_batches() == 0
    fake.raise_on_batch_create = None
    assert s.batch_submit(rq3_requests("sonnet"), name="r")["status"] == "submitted"


def test_ambiguous_submit_failure_blocks_resubmission(repo, fake):
    s = Session("lit_rq3", repo_dir=repo, client=fake)
    fake.raise_on_batch_create = StatusError(503, "overloaded")
    with pytest.raises(StatusError):
        s.batch_submit(rq3_requests("sonnet"), name="r")
    assert s.budget.reserved_batches() > 0
    fake.raise_on_batch_create = None
    with pytest.raises(BatchStateError, match="Console"):
        s.batch_submit(rq3_requests("sonnet"), name="r")
    assert fake.n("batch_create") == 1


def test_bad_custom_id_and_duplicates(repo, fake):
    with pytest.raises(ValueError):
        request("has space", model="sonnet", user="x", max_tokens=5)
    s = Session("lit_rq3", repo_dir=repo, client=fake)
    r = request("a", model="sonnet", user="x", max_tokens=5)
    with pytest.raises(ValueError, match="unique"):
        s.batch_submit([r, r])

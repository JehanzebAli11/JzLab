import csv
import json
import multiprocessing as mp
import threading

import pytest

from jzapi import usage
from jzapi.budget import Budget, BudgetError, BudgetExceeded, JobNotApproved
from jzapi.paths import repo_name


def _row(job="lit_rq3", cost=1.0, **kw):
    return {"job": job, "repo": "r", "model_id": "claude-sonnet-5-5", "mode": "sync", "request_id": "x",
            "input_tokens": 1, "output_tokens": 1, "cost_usd": cost, **kw}


def test_unapproved_and_unknown_jobs_refused(repo):
    with pytest.raises(JobNotApproved, match="not approved"):
        Budget("architect_ladder", None, repo / "results/usage.csv")
    with pytest.raises(JobNotApproved, match="not in budgets.yaml"):
        Budget("made_up", None, repo / "results/usage.csv")


def test_cap_can_be_lowered_not_raised(repo):
    assert Budget("lit_rq3", 5, repo / "results/usage.csv").cap_usd == 5
    with pytest.raises(BudgetError):
        Budget("lit_rq3", 25, repo / "results/usage.csv")


def test_spent_from_csv_and_refusal(repo):
    csvp = repo / "results/usage.csv"
    usage.append_rows(csvp, [_row(cost=12.5), _row(job="other", cost=100)])
    b = Budget("lit_rq3", None, csvp)
    assert b.spent_so_far() == pytest.approx(12.5)
    b.check(7.5)
    with pytest.raises(BudgetExceeded):
        b.check(7.51)


def test_inflight_reservations_are_thread_safe(repo):
    b = Budget("lit_rq3", 10, repo / "results/usage.csv")
    ok, refused = [], []

    def go():
        try:
            ok.append(b.reserve(1.0))
        except BudgetExceeded:
            refused.append(1)
    ts = [threading.Thread(target=go) for _ in range(25)]
    [t.start() for t in ts]
    [t.join() for t in ts]
    assert len(ok) == 10 and len(refused) == 15
    b.release(ok[0])
    b.check(1.0)


def test_unlogged_batches_count_as_reserved(repo):
    d = repo / "results/jzapi_batches"
    d.mkdir(parents=True)
    (d / "lit_rq3__a.json").write_text(json.dumps({"job": "lit_rq3", "status": "submitted", "worst_case_usd": 15}))
    (d / "lit_rq3__b.json").write_text(json.dumps({"job": "lit_rq3", "status": "logged", "worst_case_usd": 15}))
    b = Budget("lit_rq3", None, repo / "results/usage.csv")
    assert b.reserved_batches() == 15
    with pytest.raises(BudgetExceeded):
        b.check(5.01)


def test_usage_header_once_and_columns(tmp_path):
    p = tmp_path / "results" / "usage.csv"
    usage.append_rows(p, [_row(cost=0.1234567)])
    usage.append_rows(p, [_row(), _row()])
    lines = p.read_text().splitlines()
    assert lines[0] == ("timestamp_utc,job,repo,model_id,mode,request_id,input_tokens,cache_creation_input_tokens,"
                        "cache_read_input_tokens,output_tokens,cost_usd,note")
    assert len(lines) == 4
    rows = list(csv.DictReader(p.open()))
    assert rows[0]["cost_usd"] == "0.123457" and rows[0]["timestamp_utc"].endswith("Z")
    with pytest.raises(ValueError):
        usage.append_rows(p, [{"job": "x", "api_key": "nope"}])


def _proc_append(path, n):
    for i in range(n):
        usage.append_rows(path, [_row(request_id=f"p{i}")])


def test_concurrent_appends_threads_and_processes(tmp_path):
    p = tmp_path / "results" / "usage.csv"
    # spawn (the macOS default), not fork: forking while a thread holds a lock deadlocks the child.
    ps = [mp.get_context("spawn").Process(target=_proc_append, args=(p, 50)) for _ in range(3)]
    ts = [threading.Thread(target=_proc_append, args=(p, 50)) for _ in range(4)]
    [x.start() for x in ps + ts]
    [x.join(60) for x in ps + ts]
    assert [x.exitcode for x in ps] == [0, 0, 0]
    rows = usage.read_rows(p)
    assert len(rows) == 350
    assert p.read_text().count("timestamp_utc") == 1


def test_repo_name_for_worktree(tmp_path):
    wt = tmp_path / "wt" / "heal"
    wt.mkdir(parents=True)
    (wt / ".git").write_text("gitdir: /Users/j/lab/spark-lab/.git/worktrees/heal\n")
    assert repo_name(wt) == "spark-lab"
    plain = tmp_path / "worldsmith"
    (plain / ".git").mkdir(parents=True)
    assert repo_name(plain) == "worldsmith"

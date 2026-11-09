from pathlib import Path

from jzapi import spend, usage

REAL_SPEND = Path(__file__).resolve().parents[2] / "state" / "SPEND.md"


def _row(job, cost):
    return {"job": job, "repo": "r", "model_id": "claude-sonnet-5-5", "mode": "batch", "request_id": "x",
            "cost_usd": cost}


def test_rollup_rewrites_spent_and_total(tmp_path):
    lit, ws = tmp_path / "lit", tmp_path / "worldsmith"
    usage.append_rows(lit / "results/usage.csv", [_row("lit_rq3", 1.234), _row("lit_rq3", 2.0)])
    usage.append_rows(ws / "results/usage.csv", [_row("architect_ladder", 10.5)])
    sf = tmp_path / "SPEND.md"
    original = REAL_SPEND.read_text()
    sf.write_text(original)
    assert spend.main(["--repos", str(lit), str(ws), str(tmp_path / "no-results-yet"),
                       "--spend-file", str(sf), "--date", "2026-11-13"]) == 0
    new = sf.read_text()
    assert "| LIT (RQ3 Sonnet/Opus) | $20 (inside LIT's $40 cap) | yes, 2026-11-09 | $3.23 | 2026-11-13 |" in new
    assert "| Architect ladder | $90 | no | $10.50 | 2026-11-13 |" in new
    assert "| Validator red-team | $25 | no | $0.00 | — |" in new
    assert "| **Total** | **$400** | | **$13.73** | |" in new
    assert new.splitlines()[:4] == original.splitlines()[:4]          # heading and text kept
    assert len(new.splitlines()) == len(original.splitlines())


def test_unplaced_job_reported(tmp_path, capsys):
    usage.append_rows(tmp_path / "x/results/usage.csv", [_row("mystery_job", 1)])
    sf = tmp_path / "SPEND.md"
    sf.write_text(REAL_SPEND.read_text())
    assert spend.main(["--repos", str(tmp_path / "x"), "--spend-file", str(sf), "--dry-run"]) == 1
    assert "NOT IN SPEND.md" in capsys.readouterr().err
    assert sf.read_text() == REAL_SPEND.read_text()  # dry run writes nothing


def test_no_usage_leaves_file_byte_identical(tmp_path):
    sf = tmp_path / "SPEND.md"
    sf.write_text(REAL_SPEND.read_text())
    assert spend.main(["--repos", str(tmp_path / "empty"), "--spend-file", str(sf)]) == 0
    assert sf.read_text() == REAL_SPEND.read_text()

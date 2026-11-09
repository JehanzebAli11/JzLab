"""Roll up every repo's results/usage.csv into state/SPEND.md (Spent column and total).

    python -m jzapi.spend --repos ~/lab/lost-in-transliteration ~/lab/worldsmith ...

Only jobs that appear in a usage.csv are rewritten (their Spent and Last updated cells); the
Total row is the sum of the Spent column. Jobs in a usage.csv that budgets.yaml does not map to a
SPEND.md row are reported, and the exit code is 1.
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

from . import usage
from .budget import load_budgets
from .keys import PACKAGE_ROOT
from .paths import usage_csv


def default_spend_file() -> Path:
    return PACKAGE_ROOT / "state" / "SPEND.md"


def collect(repos: list[str | Path]) -> dict[str, float]:
    per_job: dict[str, float] = defaultdict(float)
    for repo in repos:
        for r in usage.read_rows(usage_csv(Path(repo).expanduser())):
            per_job[r["job"]] += float(r.get("cost_usd") or 0)
    return dict(per_job)


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _row(cells: list[str]) -> str:
    return "|" + "|".join(f" {c} " if c else " " for c in cells) + "|"


def _money(x: float) -> str:
    return f"${x:,.2f}"


def _parse_money(cell: str) -> float:
    c = cell.replace("*", "").replace("$", "").replace(",", "").strip()
    try:
        return float(c)
    except ValueError:
        return 0.0


def rewrite(text: str, per_job: dict[str, float], spend_rows: dict[str, str], today: str) -> tuple[str, list[str]]:
    """Return the new SPEND.md text and the jobs that could not be placed."""
    label_to_job = {v: k for k, v in spend_rows.items()}
    unplaced = sorted(j for j in per_job if j not in spend_rows)
    lines = text.splitlines()
    hdr = next((i for i, l in enumerate(lines) if l.lstrip().startswith("|") and "Spent" in _cells(l)), None)
    if hdr is None:
        raise ValueError("SPEND.md has no table with a 'Spent' column")
    cols = _cells(lines[hdr])
    i_spent, i_upd = cols.index("Spent"), cols.index("Last updated") if "Last updated" in cols else None
    body = []
    i = hdr + 2  # skip the separator row
    total_idx = None
    while i < len(lines) and lines[i].lstrip().startswith("|"):
        cells = _cells(lines[i])
        label = cells[0]
        if label.replace("*", "").strip().lower() == "total":
            total_idx = i
        else:
            job = label_to_job.get(label)
            if job is not None and job in per_job:
                cells[i_spent] = _money(per_job[job])
                if i_upd is not None:
                    cells[i_upd] = today
                lines[i] = _row(cells)
            body.append(i)
        i += 1
    if total_idx is not None:
        total = sum(_parse_money(_cells(lines[j])[i_spent]) for j in body)
        cells = _cells(lines[total_idx])
        cells[i_spent] = f"**{_money(total)}**"
        lines[total_idx] = _row(cells)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else ""), unplaced


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repos", nargs="+", required=True, help="repo folders whose results/usage.csv to read")
    ap.add_argument("--spend-file", default=None, help="default: <JzLab>/state/SPEND.md")
    ap.add_argument("--budgets", default=None, help="default: <JzLab>/budgets.yaml (or JZ_BUDGETS_FILE)")
    ap.add_argument("--date", default=None, help="Last updated value (default: today)")
    ap.add_argument("--dry-run", action="store_true", help="print the new file instead of writing it")
    args = ap.parse_args(argv)
    spend_file = Path(args.spend_file) if args.spend_file else default_spend_file()
    jobs = load_budgets(args.budgets)
    spend_rows = {j: b.spend_row for j, b in jobs.items() if b.spend_row}
    per_job = collect(args.repos)
    new, unplaced = rewrite(spend_file.read_text(encoding="utf-8"), per_job, spend_rows,
                            args.date or date.today().isoformat())
    if args.dry_run:
        sys.stdout.write(new)
    else:
        spend_file.write_text(new, encoding="utf-8")
    for j, usd in sorted(per_job.items()):
        print(f"{j}: {_money(usd)}" + ("  (NOT IN SPEND.md: add spend_row in budgets.yaml)" if j in unplaced else ""),
              file=sys.stderr)
    return 1 if unplaced else 0


if __name__ == "__main__":
    sys.exit(main())

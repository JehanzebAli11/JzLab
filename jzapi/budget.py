"""Per-job caps from budgets.yaml (mirrors ROADMAP §9) and the pre-call guard."""
from __future__ import annotations

import json
import threading
from dataclasses import dataclass
from pathlib import Path

import yaml

from . import usage
from .paths import batch_state_dir, budgets_file


class BudgetError(RuntimeError):
    pass


class BudgetExceeded(BudgetError):
    pass


class JobNotApproved(BudgetError):
    pass


@dataclass(frozen=True)
class JobBudget:
    job: str
    cap_usd: float
    approved: bool
    spend_row: str | None = None
    approved_on: str | None = None


def load_budgets(path: str | Path | None = None) -> dict[str, JobBudget]:
    path = Path(path) if path else budgets_file()
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    jobs = {}
    for name, d in (data.get("jobs") or {}).items():
        jobs[name] = JobBudget(job=name, cap_usd=float(d["cap_usd"]), approved=d.get("approved") is True,
                               spend_row=d.get("spend_row"),
                               approved_on=str(d["approved_on"]) if d.get("approved_on") else None)
    total = data.get("total_usd")
    if total is not None and sum(j.cap_usd for j in jobs.values()) > float(total) + 1e-9:
        raise BudgetError(f"job caps in {path} add up to more than total_usd {total}")
    return jobs


class Budget:
    """Guard for one job. Refuses unapproved jobs at construction; refuses any request or batch whose
    worst case would take spent (usage.csv) + reserved (in-flight calls, unlogged batches) over the cap.

    cap_usd may lower the budgets.yaml cap for a run, never raise it.
    """

    def __init__(self, job: str, cap_usd: float | None = None, usage_csv: str | Path | None = None,
                 *, budgets_path: str | Path | None = None, batch_dir: str | Path | None = None):
        jobs = load_budgets(budgets_path)
        if job not in jobs:
            raise JobNotApproved(f"job {job!r} is not in budgets.yaml; known jobs: {sorted(jobs)}")
        jb = jobs[job]
        if not jb.approved:
            raise JobNotApproved(f"job {job!r} is not approved in budgets.yaml (approved: false); "
                                 f"Jehanzeb must approve it first")
        if cap_usd is not None and float(cap_usd) > jb.cap_usd:
            raise BudgetError(f"cap_usd {cap_usd} is above the budgets.yaml cap {jb.cap_usd} for {job!r}")
        self.job = job
        self.cap_usd = float(cap_usd) if cap_usd is not None else jb.cap_usd
        self.usage_csv = Path(usage_csv) if usage_csv else None
        self.batch_dir = Path(batch_dir) if batch_dir else (
            batch_state_dir(self.usage_csv.parent.parent) if self.usage_csv else None)
        self._lock = threading.Lock()
        self._inflight: dict[int, float] = {}
        self._next = 0

    def __repr__(self) -> str:
        return f"Budget(job={self.job!r}, cap_usd={self.cap_usd})"

    def spent_so_far(self) -> float:
        return usage.spent_usd(self.usage_csv, self.job) if self.usage_csv else 0.0

    def reserved_batches(self) -> float:
        """Worst case of this job's submitted batches whose results are not yet in usage.csv."""
        if not self.batch_dir or not self.batch_dir.exists():
            return 0.0
        total = 0.0
        for p in self.batch_dir.glob("*.json"):
            try:
                st = json.loads(p.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if st.get("job") == self.job and st.get("status") != "logged":
                total += float(st.get("worst_case_usd") or 0)
        return total

    def remaining(self) -> float:
        with self._lock:
            return self.cap_usd - self.spent_so_far() - self.reserved_batches() - sum(self._inflight.values())

    def check(self, worst_case_usd: float, what: str = "request") -> None:
        with self._lock:
            self._check_locked(worst_case_usd, what)

    def _check_locked(self, worst: float, what: str) -> None:
        spent = self.spent_so_far()
        held = self.reserved_batches() + sum(self._inflight.values())
        if spent + held + worst > self.cap_usd + 1e-12:
            raise BudgetExceeded(
                f"{self.job}: {what} worst case ${worst:.4f} + spent ${spent:.4f} + reserved ${held:.4f} "
                f"> cap ${self.cap_usd:.2f}")

    def reserve(self, worst_case_usd: float, what: str = "request") -> int:
        """Check and hold worst_case_usd for an in-flight sync call; release() after logging."""
        with self._lock:
            self._check_locked(worst_case_usd, what)
            self._next += 1
            self._inflight[self._next] = worst_case_usd
            return self._next

    def release(self, token: int) -> None:
        with self._lock:
            self._inflight.pop(token, None)

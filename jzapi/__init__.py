"""jzapi: one guarded way to call the Claude API from any of Jehanzeb's repos.

Every call is checked against the job's cap and approval in JzLab/budgets.yaml (ROADMAP §9)
and logged to the calling repo's results/usage.csv. Claude outputs are evaluation and
inference only, never training data (ROADMAP §11.3).
"""
from .api import (BatchItem, BatchStateError, MessageResult, Session, batch_poll, batch_results,
                  batch_submit, build_params, message, request, session, system_blocks)
from .budget import Budget, BudgetError, BudgetExceeded, JobNotApproved, load_budgets
from .client import JzApiError
from .keys import MissingKey, load_api_key
from .models import BATCH_MULTIPLIER, PRICE_CHECKED, PRICE_SOURCE, PRICES, ROLES, cost_usd, resolve, worst_case_usd

__all__ = ["Session", "session", "message", "batch_submit", "batch_poll", "batch_results", "request",
           "build_params", "system_blocks", "MessageResult", "BatchItem", "BatchStateError",
           "Budget", "BudgetError", "BudgetExceeded", "JobNotApproved", "load_budgets", "JzApiError",
           "MissingKey", "load_api_key", "ROLES", "PRICES", "PRICE_SOURCE", "PRICE_CHECKED",
           "BATCH_MULTIPLIER", "cost_usd", "worst_case_usd", "resolve"]

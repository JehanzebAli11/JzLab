"""Where the calling repo, its results/ folder and JzLab's own files are."""
from __future__ import annotations

import os
from pathlib import Path

from .keys import PACKAGE_ROOT

BUDGETS_VAR = "JZ_BUDGETS_FILE"
REPO_VAR = "JZ_REPO_DIR"


def budgets_file() -> Path:
    o = os.environ.get(BUDGETS_VAR)
    return Path(o).expanduser() if o else PACKAGE_ROOT / "budgets.yaml"


def find_repo_root(start: str | Path | None = None) -> Path:
    """JZ_REPO_DIR if set, else the nearest folder (from cwd up) holding .git (a git worktree
    has a .git file, and counts), else cwd."""
    o = os.environ.get(REPO_VAR)
    if start is None and o:
        return Path(o).expanduser().resolve()
    here = Path(start or os.getcwd()).resolve()
    for p in (here, *here.parents):
        if (p / ".git").exists():
            return p
    return here


def repo_name(repo_dir: Path) -> str:
    """The repo's name; for a git worktree, the name of the main checkout it belongs to."""
    git = repo_dir / ".git"
    if git.is_file():
        try:
            line = git.read_text(encoding="utf-8").strip()
        except OSError:
            line = ""
        if line.startswith("gitdir:"):
            gd = Path(line.split(":", 1)[1].strip())
            parts = gd.parts
            if "worktrees" in parts:
                i = len(parts) - 1 - parts[::-1].index("worktrees")
                if i >= 1 and parts[i - 1] == ".git" and i >= 2:
                    return parts[i - 2]
    return repo_dir.name


def results_dir(repo_dir: Path) -> Path:
    return repo_dir / "results"


def usage_csv(repo_dir: Path) -> Path:
    return results_dir(repo_dir) / "usage.csv"


def batch_state_dir(repo_dir: Path) -> Path:
    return results_dir(repo_dir) / "jzapi_batches"

import socket
from pathlib import Path

import pytest

from .fakes import FakeClient

FAKE_KEY = "sk-ant-test-FAKEKEY-0123456789abcdef-never-real"
REAL_BUDGETS = Path(__file__).resolve().parents[2] / "budgets.yaml"


@pytest.fixture(autouse=True)
def offline(monkeypatch, tmp_path):
    """No network, no real key, no writes outside tmp_path."""
    def refuse(*a, **k):
        raise RuntimeError("network is disabled in jzapi tests")
    monkeypatch.setattr(socket.socket, "connect", refuse)
    monkeypatch.delenv("JZ_ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("JZ_REPO_DIR", raising=False)
    env = tmp_path / "test.env"
    env.write_text(f"OTHER=1\nJZ_ANTHROPIC_API_KEY={FAKE_KEY}\n")
    monkeypatch.setenv("JZ_ENV_FILE", str(env))
    monkeypatch.setenv("JZ_BUDGETS_FILE", str(REAL_BUDGETS))
    from jzapi import api
    api._sessions.clear()
    yield


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "fake-repo"
    (r / ".git").mkdir(parents=True)
    return r


@pytest.fixture
def fake():
    return FakeClient()

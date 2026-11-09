import logging
import pickle
import traceback

import pytest

from jzapi import Session, keys
from jzapi.client import JzApiError, guarded
from jzapi.keys import MissingKey, Secret, load_api_key

from .conftest import FAKE_KEY


def test_env_var_wins(monkeypatch):
    monkeypatch.setenv("JZ_ANTHROPIC_API_KEY", "sk-from-env")
    assert load_api_key().reveal() == "sk-from-env"


def test_env_file_parsing(tmp_path, monkeypatch):
    f = tmp_path / ".env"
    f.write_text("# c\nexport JZ_ANTHROPIC_API_KEY='sk-quoted'\n")
    assert load_api_key(f).reveal() == "sk-quoted"
    f.write_text("JZ_ANTHROPIC_API_KEY=sk-plain # comment\n")
    assert load_api_key(f).reveal() == "sk-plain"
    monkeypatch.setenv("JZ_ENV_FILE", str(f))
    assert load_api_key().reveal() == "sk-plain"


def test_default_env_file_is_next_to_package(monkeypatch):
    monkeypatch.delenv("JZ_ENV_FILE")
    assert keys.default_env_file() == keys.PACKAGE_ROOT / ".env"
    assert (keys.PACKAGE_ROOT / "jzapi").is_dir()


def test_missing_key_names_variable_and_path_only(tmp_path):
    f = tmp_path / "none.env"
    f.write_text("OTHER=1\n")
    with pytest.raises(MissingKey) as e:
        load_api_key(f)
    assert "JZ_ANTHROPIC_API_KEY" in str(e.value) and str(f) in str(e.value)


def test_secret_never_shows():
    s = Secret(FAKE_KEY)
    for shown in (str(s), repr(s), f"{s}", f"{s!r}", "%s" % s, repr([s]), repr({"k": s})):
        assert FAKE_KEY not in shown
    with pytest.raises(TypeError):
        pickle.dumps(s)


def test_guard_scrubs_key_from_exceptions():
    s = Secret(FAKE_KEY)
    with pytest.raises(JzApiError) as e:
        with guarded(s):
            raise ValueError(f"bad header x-api-key: {FAKE_KEY}")
    tb = "".join(traceback.format_exception(type(e.value), e.value, e.value.__traceback__))
    assert FAKE_KEY not in tb and "<redacted>" in tb
    assert e.value.__cause__ is None and e.value.__suppress_context__
    assert FAKE_KEY not in str(e.value.__context__) and FAKE_KEY not in repr(e.value.__context__.args)
    with pytest.raises(KeyError):  # unrelated errors pass through unchanged
        with guarded(s):
            raise KeyError("x")


def test_key_absent_from_logs_reprs_files_and_errors(repo, fake, caplog, capsys):
    caplog.set_level(logging.DEBUG)
    s = Session("lit_rq3", repo_dir=repo, client=fake)
    s._secret = load_api_key()
    s.message(user="hi", max_tokens=10)
    from jzapi import request
    s.batch_submit([request("a1", model="sonnet", user="x", max_tokens=5)], name="t")
    s.batch_results("t")
    fake.raise_on_create = RuntimeError(f"echo {FAKE_KEY}")
    with pytest.raises(JzApiError) as e:
        s.message(user="hi", max_tokens=10)
    out = capsys.readouterr()
    blobs = [caplog.text, out.out, out.err, repr(s), repr(s.budget), str(e.value), repr(e.value)]
    blobs += [p.read_text() for p in (repo / "results").rglob("*") if p.is_file()]
    for b in blobs:
        assert FAKE_KEY not in b

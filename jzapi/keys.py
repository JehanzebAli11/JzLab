"""API key loading. The key is never printed, logged, repr'd or put in an exception.

Order: the JZ_ANTHROPIC_API_KEY environment variable, else the git-ignored .env file at
JZ_ENV_FILE (default: the .env next to this package, i.e. ~/lab/JzLab/.env).
"""
from __future__ import annotations

import os
from pathlib import Path

KEY_VAR = "JZ_ANTHROPIC_API_KEY"
ENV_FILE_VAR = "JZ_ENV_FILE"
PACKAGE_ROOT = Path(__file__).resolve().parent.parent  # the JzLab checkout


class MissingKey(RuntimeError):
    """Raised when no key is found. Says only which variable and which file were checked."""


class Secret:
    """Holds the key. str()/repr()/format() never show it; call .reveal() only at the SDK boundary."""

    __slots__ = ("_value",)

    def __init__(self, value: str):
        self._value = value

    def reveal(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return "Secret(<redacted>)"

    __str__ = __repr__

    def __format__(self, spec: str) -> str:
        return repr(self)

    def __reduce__(self):  # refuse pickling, so the key cannot leak into a cache or state file
        raise TypeError("Secret cannot be pickled")

    def __eq__(self, other):
        return isinstance(other, Secret) and other._value == self._value

    def __hash__(self):
        return hash(("Secret", len(self._value)))


def default_env_file() -> Path:
    override = os.environ.get(ENV_FILE_VAR)
    return Path(override).expanduser() if override else PACKAGE_ROOT / ".env"


def _parse_env_value(path: Path, name: str) -> str | None:
    try:
        text = path.read_text(encoding="utf-8")
    except (FileNotFoundError, IsADirectoryError, PermissionError):
        return None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].lstrip()
        k, sep, v = line.partition("=")
        if not sep or k.strip() != name:
            continue
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
            v = v[1:-1]
        else:
            v = v.split(" #", 1)[0].strip()  # inline comment after an unquoted value
        return v or None
    return None


def load_api_key(env_file: str | Path | None = None) -> Secret:
    value = os.environ.get(KEY_VAR) or None
    path = Path(env_file).expanduser() if env_file else default_env_file()
    if value is None:
        value = _parse_env_value(path, KEY_VAR)
    if not value:
        raise MissingKey(f"{KEY_VAR} not found: checked the environment variable {KEY_VAR} "
                         f"and the file {path}")
    return Secret(value)


def scrub(text: str, secret: Secret | None) -> str:
    """Replace the key (if present) in a string."""
    if secret is None:
        return text
    v = secret.reveal()
    return text.replace(v, "<redacted>") if v and v in text else text

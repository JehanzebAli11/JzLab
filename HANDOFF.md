# HANDOFF (JzLab)

## 2026-11-09 18:55 PKT · jzapi

**Done**
- `jzapi/` package + `pyproject.toml` (install: `pip install -e ~/lab/JzLab`) + `budgets.yaml`
  (ROADMAP §9 caps, total $400; only `lit_rq3` $20 approved, 2026-11-09).
- Key from `JZ_ANTHROPIC_API_KEY` env, else `JZ_ENV_FILE` / `<JzLab>/.env`; held in a `Secret`
  that never prints; exceptions containing it are re-raised scrubbed.
- Pinned roles: haiku `claude-haiku-5-5`, sonnet `claude-sonnet-5-5`, opus `claude-opus-5-5`, with
  prices from https://platform.claude.com/docs/en/about-claude/pricing (checked 2026-11-09).
- `Budget` guard (approval, cap, spent from usage.csv + reserved in-flight/unlogged batches +
  worst case), `message()` sync, `batch_submit/poll/results` (resumable via
  `results/jzapi_batches/`), locked `results/usage.csv` logging, `python -m jzapi.spend` roll-up,
  `jzapi/README.md`.

**Verified**
- `pytest` from the JzLab root: 46 passed (offline, fake client; Python 3.10.12 in the Cowork VM).
- `python -m jzapi.spend --repos ~/lab/lost-in-transliteration --dry-run` leaves SPEND.md
  byte-identical (no usage.csv exists yet).
- NOT verified: the live `GET /v1/models` check. From the Cowork VM, every request to
  api.anthropic.com that carries an API-key header gets a plain-text `401 Unauthorized` from the
  VM's egress proxy (same for a made-up key; no Cloudflare/Request-Id headers, so Anthropic never
  saw it). Requests without a key reach Anthropic. Model IDs are pinned from the models overview
  page instead. No paid call was made.

**Next**
- On the Mac (not the VM): `pip install -e ~/lab/JzLab && python -m jzapi.models --verify`
  (free) to confirm the three IDs.
- LIT thread: route RQ3 Sonnet/Opus through `jzapi.request(...)` + `batch_submit("lit_rq3", ...)`
  with `cache_system=True`; one `name` per model so re-runs resume.
- Friday: `python -m jzapi.spend --repos ~/lab/<each repo with API jobs>`.

**Open questions**
- Paid runs from Cowork VM workers will hit the same proxy 401: API jobs must run in a Mac
  terminal (or the VM egress policy changed to allow the key header to api.anthropic.com)?
- LIT keeps its own `src/budget.py` ($40 cap, 95% stop). Should RQ3 log to both, or switch to
  jzapi only? (Left to the LIT thread; LIT repo not edited.)
- Batch discount is applied to cache write/read prices too ("discounts can be combined"); confirm
  against the first real invoice line.

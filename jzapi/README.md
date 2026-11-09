# jzapi

One guarded way to call the Claude API from any of Jehanzeb's repos. Every call is checked
against its job's cap and approval in `JzLab/budgets.yaml` (ROADMAP §9) and logged to the calling
repo's `results/usage.csv`.

**Rule (ROADMAP §11.3): Claude outputs are evaluation and inference only, never training data.**
Do not train, fine-tune or label training data with anything jzapi returns.

## Install

On the MacBook, in the venv of the repo that uses it:

```bash
pip install -e ~/lab/JzLab        # editable: JzLab updates take effect without reinstalling
```

This is the supported way. (Adding `~/lab/JzLab` to `sys.path` also works, but then install
`anthropic>=2.0` and `PyYAML` yourself.) Run scripts from inside the consuming repo: jzapi finds
the repo from the current folder (the nearest `.git`, worktrees included), or from `JZ_REPO_DIR`.

## The key

`JZ_ANTHROPIC_API_KEY` is read from the environment, else from the git-ignored `~/lab/JzLab/.env`
(override the file with `JZ_ENV_FILE`). jzapi never prints, logs or repr's it, and scrubs it from
any exception. If it is missing, the error names only the variable and the file it checked.
Never paste the key into chat or a prompt.

## Models and prices

`jzapi.ROLES`: `haiku` -> `claude-haiku-5-5` (dev runs), `sonnet` -> `claude-sonnet-5-5`
(default), `opus` -> `claude-opus-5-5` (final sets, red-teaming). Only these IDs (and dated
snapshots of them) are accepted. Prices, cache multipliers and the batch discount are pinned in
`jzapi/models.py` with their source URL and check date; `python -m jzapi.models` prints them, and
`python -m jzapi.models --verify` checks the IDs with the free `GET /v1/models` call.

API version 2026-10-21 rejects `temperature`, `top_p` and `top_k` (HTTP 400), so jzapi refuses
them too. Claude samples at the API default; record `api_default` in your results.

## Budgets and approval

`budgets.yaml` holds one entry per job: `cap_usd`, `approved`, and the `spend_row` label in
`state/SPEND.md`. jzapi refuses:

- a job not in the file, or with `approved: false` (`JobNotApproved`), before any request;
- any request or batch whose worst case would take `spent + reserved + worst case` over the cap
  (`BudgetExceeded`), before it is sent.

*Spent* is the sum of `cost_usd` for the job in the repo's `results/usage.csv`. *Reserved* is the
worst case of in-flight sync calls plus every submitted batch whose results are not logged yet.
*Worst case* = every prompt token at the dearest input rate the request can incur (the cache-write
rate if it caches, else plain input) + `max_tokens` x output price, with the 50% batch discount
only for batches. Prompt tokens come from the free token-counting endpoint (x1.05 margin), or,
with `token_estimate="bytes"`, from the UTF-8 byte length of the prompt (an offline upper bound).

A run may lower its cap (`cap_usd=` on `Session`), never raise it. Raising a cap or approving a
job needs Jehanzeb's yes, recorded in `state/DECISIONS.md`, then an edit to `budgets.yaml`.
Today only `lit_rq3` ($20) is approved (9 Nov 2026).

## Using it

```python
import jzapi

# Sync, for dev runs with Haiku. One usage.csv row per call.
r = jzapi.message("lit_rq3", model="haiku", system=SYSTEM, user=doc, max_tokens=200, note="smoke")
r.text, r.cost_usd, r.usage

# Batch (50% off). Build requests, submit once, poll, read results.
reqs = [jzapi.request(f"sonnet-{key}", model="sonnet", system=SYSTEM, cache_system=True,
                      user=doc, max_tokens=200) for key, doc in docs]
jzapi.batch_submit("lit_rq3", reqs, name="rq3_sonnet")      # re-running polls, never resubmits
st = jzapi.batch_poll("lit_rq3", "rq3_sonnet", wait=True)    # every 60 s until ended
for item in jzapi.batch_results("lit_rq3", "rq3_sonnet"):     # one usage row per result, once
    item.custom_id, item.type, item.text, item.cost_usd
```

Or hold one `jzapi.Session("lit_rq3")` and call `.message`, `.batch_submit`, `.batch_poll`,
`.batch_results` on it (`token_estimate=`, `cap_usd=`, `repo_dir=` are options there).

- `custom_id`: 1-64 characters of `[A-Za-z0-9_-]`, unique in the batch. Results come back in any
  order: match on `custom_id`.
- `cache_system=True` puts `cache_control` on the (last) system block; `cache_ttl="1h"` for long
  batches. Caching needs at least 512 tokens of prefix on these models; shorter prefixes are
  simply not cached. In batches, cache hits are best effort.
- Batch state lives in `results/jzapi_batches/<job>__<name>.json` (the batch id, worst case and
  status). `batch_results` also saves `<job>__<name>.results.jsonl`, so a re-run reads that file
  and logs nothing twice. If a submit failed ambiguously (timeout, 5xx), the state stays
  `submitting` and a re-run stops: check the Console for the batch before resubmitting.
- Errored, canceled and expired batch results are not billed: logged with cost 0.

## usage.csv

`results/usage.csv` in the calling repo, one row per sync call or batch result:
`timestamp_utc, job, repo, model_id, mode (sync|batch), request_id (or custom_id), input_tokens,
cache_creation_input_tokens, cache_read_input_tokens, output_tokens, cost_usd, note`. Appends are
locked (threads and processes). Cost is computed from the pinned price table, including Haiku
5.5's higher prices for prompts over 100,000 tokens and 1h cache writes.

## SPEND roll-up

```bash
python -m jzapi.spend --repos ~/lab/lost-in-transliteration ~/lab/worldsmith   # --dry-run to preview
```

Rewrites the Spent and Last updated cells of every job found in those usage.csv files, and the
Total, in `JzLab/state/SPEND.md`. A job without a `spend_row` is reported (exit code 1).

## Tests

`pytest` from the JzLab root (offline, with a fake client; no key, no network).

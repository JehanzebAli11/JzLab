# Task: finish Lost in Transliteration (phase B, deadline-critical)

Repo: `~/lab/lost-in-transliteration`, push to `main`. Read `PLAN.md`, `RUNBOOK.md` and
`LOG.md` first. The Anthropic Research Residency application closes **22 Nov 2026**. The owner
submits on 19 Nov, so the write-up must be drafted by **Sat 14 Nov**.

Already done (see LOG.md): the full dataset, built with open-weight models on OpenRouter
(owner-approved profile `cloud_openrouter`, $0.18); the 20-item Roman Urdu check, all rated OK;
and the §4.1 classifier eval (6 classifiers × 2,908 inputs). Do not regenerate the data. Re-score
the classifiers only if config or code changed.

Work in this order:

1. RUNBOOK step 0 on the Spark: venv, torch for ARM64 + CUDA (NGC container if the wheel fails),
   `make setup`, `make test` (61 passed). Check `torch.cuda.is_available()`.
2. RUNBOOK step 1: `make todos` until empty. Model IDs and prices must be looked up and dated.
   `.env` is the owner's; if a key is missing, say so with `JZ-NEED:`.
3. Step 4: `make eval-models-sanity`, read the responses, then `make eval-models` (the $40 cap
   stays). It is API-bound, so start it in the background first.
4. Step 5: Phase 2 detector training (`make train`) next to the teacher. The detectors are
   small; if memory gets tight, set `detector.conditions: [0, 25, 100]` and `seeds: [1]` as the
   RUNBOOK says. Then `make eval-detector`.
5. Step 6: keep the MCP phase small. Use 2 local scanners at most; never create accounts. A large
   reproducible bypass of a vendor's tool means a disclosure note before any public post (PLAN §0.5).
6. Step 7, `make analyze`: every figure is produced, and `skipped` is empty.
7. Step 8: draft `writeup/post.md`, `writeup/application_blurb.md`, `README.md` and `SUMMARY.md`.
   Every number comes from `results/`; `results/headline_numbers.json` collects them. Then
   `JZ-NEED: owner review of writeup/`.

Rule 8 is strict: only open-weight models create or translate data; Claude and other API models
are only evaluated. Claude's temperature limitation (LOG, 2026-11-03) goes in the limitations
section. Log everything in LOG.md, commit and push often, and print `JZ-STATUS:` after each step.

# Task: LIT Phase 2 detector training on the Mac (MPS), then analysis and write-up draft

Folder: `~/lab/lost-in-transliteration` (native Claude Code session on the MacBook, not the Spark).
Read first: `PLAN.md`, `RUNBOOK.md`, `LOG.md`, then `~/lab/JzLab/agents/lit/prompt.md` (steps 2-4;
ignore its Spark/CUDA/teacher parts) and `~/lab/JzLab/prompts/threads/lit-writeup-draft.md`.
Deadlines: training ETA known by Tue 10 Nov evening; training done by Thu 12 Nov 12:00 PKT;
write-up draft by Sat 14 Nov. The owner submits the Residency on 19 Nov.

## Steps
1. **Setup.** `python3 -m venv .venv && source .venv/bin/activate`, `pip install torch` (macOS arm64
   wheel), `make setup`, `make test` (all must pass). Print `torch.backends.mps.is_available()`.
2. **MPS support (tests first).** `src/train_detector.py` `pick_device("auto")` only returns cuda or
   cpu. Write a test (monkeypatch availability), then make auto pick cuda → mps → cpu. bf16 stays
   CUDA-only; MPS runs fp32. Check `src/eval_detector.py` for the same logic. `make test` passes.
3. **Verify detector IDs.** Clear the two `TODO_VERIFY` `detector.base_models.hf_id` entries in
   `config.yaml` (FacebookAI/xlm-roberta-base, distilbert/distilbert-base-multilingual-cased):
   confirm each exists on Hugging Face and its licence; log the date and licence in LOG.md.
4. **Reduced config** (PLAN §11, RUNBOOK step 5): `detector.conditions: [0, 25, 100]`,
   `seeds: [1]`. Log why (Mac MPS, deadline).
5. **Train.** `caffeinate -i make train`, then follow `logs/train.log` / `make train-status`.
   After the first epoch of the first run, print `JZ-STATUS: ETA <time> for 6 runs`.
   **If the ETA is later than Thu 12 Nov 12:00 PKT, print `JZ-NEED: training won't finish by Thu;
   owner to set up the Spark` at once and keep training running.** Then `make eval-detector`.
   Weights stay in `models/` (git-ignored). Never upload them.
6. **HANDOFF** (see format below), commit, push.
7. **Analysis.** `make analyze`: every figure produced and `skipped` empty, or explain each skip.
8. **Write-up draft.** `writeup/post.md`, `writeup/application_blurb.md`, `README.md`, `SUMMARY.md`,
   and `results/headline_numbers.json`. Every number comes from `results/`, with n. Claude's
   temperature limitation (LOG, 2026-11-03) goes in the limitations section. A large reproducible
   vendor bypass needs a disclosure note before any public post (PLAN §0.5). Then HANDOFF and
   `JZ-NEED: owner review of writeup/`.

## Working alongside another worker
A control-session worker will add Claude Sonnet 5.5 and Opus 5.5 to RQ3 through the Batch API in
this same folder this week. Do **not** edit `src/eval_models.py`, the `models` section of
`config.yaml` or `results/models_*`, and don't run `make eval-models`. If those results aren't
there when you draft, write `[PENDING: RQ3 Sonnet/Opus, results/models_summary.csv]` where they go,
and re-run `make analyze` once they land. Stage only your own paths (`git add <paths>`, never
`git add -A`). If git reports `index.lock`, wait 30 s and retry once.

## Rules
- Rule 8: only open-weight models create or translate data; Claude and other API models are only
  evaluated. No new data generation in this task.
- No paid API calls in this session.
- Git identity `Jehanzeb Ali <jehanzeb1111@icloud.com>`. Push to this repo's `main` after tests pass;
  never force-push.
- Log everything in LOG.md. Print `JZ-STATUS:` after each step.

## HANDOFF entry (append to `HANDOFF.md`, create it if missing)
`## <date time PKT> · <step>` then **Done** · **Verified** (commands run, files that prove it) ·
**Next** · **Open questions**.

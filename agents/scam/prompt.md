# Task: train and export the Scam Radar model (phase C)

Repo: `~/lab/scam-radar`. Read `HANDOVER.md` (on `main`, or on the `android-app` branch if
PR #1 is not merged yet) and `~/lab/spark-lab/CLAUDE.md` first.

The model is `google/gemma-3-270m-it`. It fits next to the teacher, so run it overnight through
the spark-lab queue.

1. Set up the env on the Spark and run the tests.
2. "Next steps" 1: train with `scamradar train`, as a spark-lab job with checkpoints and resume.
   Serve the checkpoint and run `scamradar eval --strict`. Compare with the TF-IDF baseline and
   continue only if it wins. If it doesn't, write down why, print `JZ-NEED:` with the options,
   and stop.
3. "Next steps" 2: the export experiment in `export/README.md` section 4 (int8, int8 + int4
   embeddings, int4; cache 4096 vs 512). Use `scamradar predict-litertlm`, then
   `scamradar compare-exports`. Pick the smallest export that still passes `--strict`, and check
   the per-type numbers.
4. Commit reports and charts, not weights. Put the chosen `.litertlm` file under `runs/exp/` for
   the owner, then `JZ-NEED: phone test` with the exact `adb push` command from `app/README.md`.
5. Update HANDOVER.md "Verified vs not verified" and the LinkedIn plan's "after training"
   numbers, from files only.

No messages from `eval/locked/`, and no real messages without consent. All advice text stays
pre-written; the model never writes text a user sees.

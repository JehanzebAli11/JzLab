# Task: verify the self-healing queue on the real Spark (phase D)

You work in a git worktree of spark-lab on the `self-healing` branch (PR #2, draft), not in
`~/lab/spark-lab` itself. The live worker and the nightly run use that main checkout, so don't
touch it.

Read `CLAUDE.md`, `README.md` and `HANDOFF.md` here, then follow HANDOFF.md section 5:

1. `python3 -m pytest -q` (expect 39 passed).
2. Step 1: verify the healer with the `jobs/chaos/heal-*.json` jobs. Compare with
   `results/demo/queue_report.md`. Use a separate queue directory or `--once` runs so you don't
   disturb the live queue; if the CLI can't do that, say so with `JZ-NEED:`.
3. Step 2 (real GPU chaos jobs) crashes the GPU on purpose. Before it, print
   `JZ-NEED: teacher stopped for self-healing Step 2 (about 1-2 h)` and wait. When it's done,
   print `JZ-NEED: teacher can start again`. Check `dmesg` access after the first real OOM; if
   it needs sudo, ask.
4. Steps 3-5: retrain the classifier with real logs, the VLM doctor through the Gemma teacher,
   and serve the classifier. Skip `lab-triage.service` installation unless the owner says yes:
   that is a systemd change.
5. After each step, move rows from "tested only against fakes" to "verified" with the result
   file as evidence, commit, and push to `self-healing`. When Step 1 matches, print
   `JZ-NEED: PR #2 can be marked ready and merged`.

Step 6 (pointing real jobs at the healer) waits until the owner has merged PR #2.

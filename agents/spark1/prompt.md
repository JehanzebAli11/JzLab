# Task: build and evaluate Spark-1 (phase F)

Repo: `~/lab/spark-one`, push to `main`. Read `HANDOFF.md`, `README.md` and
`~/lab/spark-lab/CLAUDE.md` first. HANDOFF.md section 5 is your brief: work through section 3
in order, from step 0.

Coordination specific to this machine:

- Steps 3-4 (teacher scoring) share the teacher with other agents. Run step 3 with
  `--limit 20000` first, measure rows/hour, and write it in HANDOFF.md before the full split.
- Step 6 (LoRA training) needs the teacher stopped. Print
  `JZ-NEED: teacher stopped for spark-one LoRA training (estimate <h> h)` and wait. Do steps 5
  and 8-10 that don't need the GPU exclusively while you wait. Print
  `JZ-NEED: teacher can start again` when training ends.
- Verify the HANDOFF section 4 risks as you reach them: prefix-cache equivalence on GPU, the
  teacher's first-token format, LoRA target modules, and Box vocabulary. Record what you find.
- Step 9: after training, serve Spark-1 at `http://localhost:8001/v1/systemone` (a spark-lab job
  or a tmux session, not a systemd unit), so the firewall agent can use it as a judge. Print
  `JZ-STATUS: Spark-1 served on :8001` and write the exact request/response contract into
  `docs/` for that agent.
- Step 10 (eval-only OpenRouter and Jev) keeps its caps ($3 and $5). Those outputs are never
  training data.
- Eval-only OpenAI Decisions API baseline: once `spark_one/adapters/decisions.py` and
  `jobs/spark-one-12-eval-decisions.json` exist (a cloud thread writes them, see
  JzLab `prompts/threads/spark1-decisions-baseline.md`), run that job early (6-7 Nov, $3 cap) so the
  12 Nov teaser post can compare it with gpt-4o-mini and zero-shot E2B. Its outputs are never
  training data.

Commit reports and figures, not checkpoints or generated images. The adapter goes only to a
**private** Hugging Face repo, and only after the owner says yes (`JZ-NEED:`).

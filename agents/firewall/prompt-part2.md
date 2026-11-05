# Task: agent firewall, part 2: Spark-1 as the judge (phase G)

Repo: `~/lab/agent-firewall`, push to `main`. Part 1 (Steps 0, 2, 3, 4) is done; read
HANDOFF.md for its results. Spark-1 is now served at `http://localhost:8001/v1/systemone`
(check with the curl in HANDOFF.md Step 1; if it isn't up, `JZ-NEED: serve Spark-1 on :8001`).

1. Step 1: verify the real Spark-1 request and response contract, adapt
   `afw/judges/remote.py` (`_payload`, `_parse_prob`) with a test, then run
   `scripts/eval_remote_judge.py --judge spark1` (with and without `--wallet`).
2. Step 5: calibrate on val, set thresholds with `budget_thresholds`, wrap it in
   `Firewall(SparkOneJudge(), T, th)`, re-run the demo GIF and the wallet eval.
3. Step 6: the eval-only LLM-judge comparison with the local Gemma. Other providers' models
   only as evaluation, never as training data.
4. Regenerate `results/RESULTS.md`, update the README from result files, and update HANDOFF.md.
   Print `JZ-DONE:` with Spark-1's catch rate and false-block rate next to the best CPU judge's.

Then keep working down the HANDOFF stretch list until told to stop.

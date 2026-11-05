# Task: get the Spark ready for every other agent (phase A)

Repo: `~/lab/spark-lab` (github.com/JehanzebAli11/spark-lab). Read `CLAUDE.md`, `README.md` and
`docs/HANDOVER.md` first.

The owner runs `bash scripts/bootstrap.sh` himself, because it asks for his ntfy topic and
Hugging Face token and prints sudo steps for him. Your job is to make that go smoothly and then
prove the whole stack works.

1. If PR #1 (`bootstrap`) is not merged yet, check out that branch. Run `pytest -q` (expect 51
   passed) and `bash scripts/setup_spark.sh` (read-only checks). Print what it finds, and the
   exact commands the owner must run, as one `JZ-NEED:` block.
2. While he runs bootstrap, read `systemd/` and the env example so you can check his result.
3. When he says it's done, verify, and fix any bug you find on the `bootstrap` branch (with a test):
   - `curl -s http://localhost:8000/v1/models` lists `google/gemma-4-31B-it`;
   - `journalctl --user -u vllm-teacher` shows the KV cache size (record it in docs/HANDOVER.md);
   - `python3 -m lab teacher-smoke` passes the 3 Roman Urdu prompts;
   - the worker service is active and the 23:00 nightly timer is listed (`systemctl --user list-timers`);
   - the smoke job runs: `python3 -m lab enqueue jobs/nightly.d/example-smoke.json && python3 -m lab worker --once`;
   - `python3 -m lab notify "Spark is up"` reaches the phone.
4. Measure teacher throughput once, with a batch of 16 short prompts. Write tokens/s and the
   wall time to docs/HANDOVER.md; other agents use it to size their jobs.
5. Push fixes to the `bootstrap` branch, then print `JZ-NEED: merge spark-lab PR #1`.
6. Print `JZ-DONE:` with the teacher id, its tokens/s, and the KV cache line.

Don't touch `self-healing` or `claude/dgx-spark-bootstrap-73xdyl`; other agents own those.

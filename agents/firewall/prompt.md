# Task: agent firewall, part 1, on real hardware (phase E)

Repo: `~/lab/agent-firewall`, push to `main`. Read `HANDOFF.md` and `results/RESULTS.md` first.
HANDOFF.md section 5 is your brief, with one change: **do Steps 0, 2, 3 and 4 only. Skip Step 1
and Step 5.** Spark-1 is not served on `localhost:8001` yet. Part 2 comes later, from
`agents/firewall/prompt-part2.md`.

- Step 0: reproduce the CPU study. Numbers should be within noise of `results/metrics.json`.
- Step 2: real Gemma agents through the teacher. Do 50 episodes first and read the raw replies,
  then 3,000. Record refusals as refusals, not as "safe". If more than ~10% of actions are
  unlabeled, extend `label_action` first.
- Step 3: teacher-written injection wrappers. Code still fills the goals and attacker values, so
  the labels stay exact.
- Step 4: retrain on all trainable records and re-run `scripts/external_eval.py`. The headline is
  BIPIA AUROC; today it is 0.41.

The HANDOFF's job JSONs use guessed fields. Map them onto spark-lab's real schema (spark-lab
README, "Job format") before you enqueue them.

Never report full-view random-split numbers as the headline (HANDOFF risk 4). Use held-out,
blind, real-agent and external numbers. Everything runs against the local fake sites and the
local anvil chain with throwaway keys. After Step 4, print
`JZ-STATUS: BIPIA AUROC before 0.41 -> after <x> (results/<file>)`, then `JZ-DONE:`.

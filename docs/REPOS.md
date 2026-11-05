# Repos (as of 5 Nov 2026)

All repos are under github.com/JehanzebAli11 and cloned to `~/lab/<folder>` on the Spark by
`bin/jz sync`. Autopilot also lives on the MacBook.

| Repo | Agent | Done (from the repo's own files) | Open PRs / branches | Next |
| --- | --- | --- | --- | --- |
| [spark-lab](https://github.com/JehanzebAli11/spark-lab) | `setup`, `heal` | Queue, worker, nightly report and systemd units on main. Self-healing CPU results: auto-fix rescued 458 of 780 broken runs | #1 bootstrap (open), #2 self-healing (draft), #3 guard/ tooling (open) | Merge #1, run it; merge #2 after Step 1; decide #3 |
| [lost-in-transliteration](https://github.com/JehanzebAli11/lost-in-transliteration) | `lit` | Full dataset (open-weight, $0.18); Phase 1 classifier eval (6 × 2,908 inputs) | research PR merged | RUNBOOK steps 4-8 |
| [scam-radar](https://github.com/JehanzebAli11/scam-radar) | `scam` | Pipeline; Android app builds and its logic tests pass; model not trained; never run on a phone | #1 android-app (open) | Merge #1, train, export, phone test |
| [spark-one](https://github.com/JehanzebAli11/spark-one) | `spark1` | 91,975-item bank, 2,400 illusions, E2B CPU smoke and LoRA resume, gpt-4o-mini eval-only | main only | HANDOFF steps 0-10 |
| [agent-firewall](https://github.com/JehanzebAli11/agent-firewall) | `firewall` | CPU study on 120k episodes; wallet firewall on anvil; BIPIA transfer 0.41 AUROC | stale `claude/agent-firewall-judge-wt2592` | HANDOFF steps 0-6 |
| [autopilot](https://github.com/JehanzebAli11/autopilot) | `autopilot` (Mac) | evolve merged; Prism Gauntlet, learning curve and Gauntlet suite on `roblox-engine` | #2 football-place (open); default branch still `main` | Make `roblox-engine` default; run the curve |
| [urdu-token-tax](https://github.com/JehanzebAli11/urdu-token-tax) | - | Unchanged since 3 Nov | - | Parked |
| [cricket-shot-coach](https://github.com/JehanzebAli11/cricket-shot-coach) | - | Unchanged since 3 Nov | - | Parked |

**Overlap to settle:** spark-lab PR #3 adds a firewall harness and wallet decoder under
`guard/`, which agent-firewall already has. Merge #3's screen-injection dataset and Chrome
extension, then move or drop its firewall and wallet pieces so each lives in one repo.

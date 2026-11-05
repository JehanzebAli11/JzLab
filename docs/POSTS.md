# LinkedIn post plan

Two posts a week, Tuesday and Thursday. A post goes out only when its gate is met; if one
slips, the next ready post takes its slot. The orchestrator drafts into `posts/` (see
`prompts/linkedin-post.md`). Jehanzeb edits and posts them himself.

| Date | Project | Hook (first line) | Visual | Post only when |
| --- | --- | --- | --- | --- |
| 5 Nov | Autopilot | [Posted](https://www.linkedin.com/feed/update/urn:li:activity:7523997421778087936/) | - | - |
| 10 Nov | Scam Radar | "I'm building a scam checker for Urdu and Roman Urdu texts that can't leak your messages: the app has no internet permission." | The demo video (rendered app screens, labelled demo mode) | PR #1 merged; say "prototype"; edit the launch draft in scam-radar `HANDOVER.md` |
| 12 Nov | Self-healing spark-lab | "My GPU box fixes its own crashes overnight. On 780 broken training runs, the auto-fix rescued 458. Plain retries rescued 1.3%." | The Self-healing section of a real nightly report | Phase D Steps 1-2 ran on the Spark; say which numbers are simulated and which are from real GPU faults |
| 17 Nov | Lost in Transliteration | "Meta's Prompt Guard 2 catches 48.5% of my English prompt-injection attacks. Write the same attacks in Roman Urdu and it catches 11.5%." | The detection-drop chart by script, from `results/table_detection_drop` | Write-up on GitHub; model evals done; Meta and ProtectAI told a few days before (PLAN §0.5) |
| 19 Nov | Agent firewall | "My agent firewall scored 0.9999 AUROC in its own sandbox and 0.41 on real emails. Here's what fixed it, or didn't." | Before/after bar: sandbox vs BIPIA AUROC | Phase E Step 4 done, so there is an "after" number |
| 24 Nov | Spark-1 (teaser) | "Reorder the options and gpt-4o-mini changes its answer 31% of the time." | One question shown twice, options swapped, two different answers | Spark-1 step 5 (E2B baseline) is in; state n = 300 |
| 26 Nov | Scam Radar on a phone | "A 270M-parameter model checking scam texts on a phone, offline: here's the memory it takes." | `results.mp4` chart from real `device.json` files | The phone test ran and the model beat TF-IDF; otherwise post the honest miss |
| 1 Dec | Spark-1 results | Lead with calibration: does Spark-1 know when it's wrong? (from `report.json`) | Reliability diagram: Spark-1 vs E2B base vs gpt-4o-mini | Step 7 report exists; adapter stays private unless Jehanzeb decides |
| 3 Dec | Autopilot follow-up | "Week 4 of letting an agent learn my obby": the Prism Gauntlet learning curve | The game-scored curve plus a short screen recording | The curve shows a trend; move this earlier if it's ready first |

Where today's numbers come from:

| Number | File |
| --- | --- |
| 48.5% / 11.5% | lost-in-transliteration `LOG.md` (prompt-guard-2 en vs roman_ur TPR), `results/classifiers*` |
| 458 / 780, 1.3% | spark-lab PR #2 `results/` (doctor auto-fix) |
| 0.9999 / 0.41 | agent-firewall `results/RESULTS.md`, `results/external_eval.json` |
| 31% (order agreement 0.690, n = 300) | spark-one `runs/eval-only/gpt-4o-mini/eval/report.md` |

## Rules

- Numbers come only from result files. If a number isn't in a file yet, the post waits.
- Say what is simulated, synthetic, CPU-only or a prototype in the post itself.
- Failures are posts too.
- Tell a vendor a few days before a post names their tool's weakness.
- No Voldex or NFL material, nothing from `eval/locked/`, no real messages without consent.
- Format: a hook line, 3-5 short lines and one visual. Put the repo link in the first comment.
  Reply to comments for the first hour.
- Credit the open models (Gemma, Qwen), and say Claude Code wrote much of the code.

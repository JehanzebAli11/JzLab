# LinkedIn post plan

Two posts a week, Tuesday and Thursday. A post goes out only when its gate is met; if one
slips, the next ready post takes its slot. The orchestrator drafts into `posts/` (see
`prompts/linkedin-post.md`). Jehanzeb edits and posts them himself.

| Date | Project | Hook (first line) | Visual | Post only when |
| --- | --- | --- | --- | --- |
| 5 Nov | Autopilot | [Posted](https://www.linkedin.com/feed/update/urn:li:activity:7523997421778087936/) | - | - |
| Tue 10 Nov | Agent firewall | "One hidden line on a page can turn an AI agent against its user. So I built an action firewall." | `linkedin_card.png` or the wallet-drainer GIF | `prompts/threads/firewall-post-check.md` passed; says "scripted agents, synthetic attacks" |
| Thu 12 Nov | Spark-1 teaser | "Decision models are here. Reorder the options and gpt-4o-mini changes its answer 31% of the time." | One question shown twice, options swapped | Decisions API baseline run; n stated |
| Tue 17 Nov | Lost in Transliteration | "Meta's Prompt Guard 2 catches 48.5% of my English prompt-injection attacks. In Roman Urdu it catches 11.5%." | The detection-drop chart by script | Write-up public; vendors told 13 Nov |
| Thu 19 Nov | Scam Radar launch | "A scam checker for Urdu and Roman Urdu texts that can't leak your messages: the app has no internet permission." | The demo video (labelled demo mode) | PR #1 merged; says "prototype" |
| Tue 24 Nov | Self-healing spark-lab | "My GPU box fixes its own crashes overnight." plus real GPU numbers | A real nightly report's Self-healing section | heal Steps 1-2 ran on the Spark |
| Thu 26 Nov | Agent firewall, part 2 | "Last time my firewall worked on scripted agents. Here's what happened with real ones." | Before/after: scripted vs real agents, BIPIA AUROC | firewall part 1 and 2 results exist |
| Tue 1 Dec | Spark-1 results | Does a 5B model know when it's wrong? (calibration first) | Reliability diagram: Spark-1, E2B base, gpt-4o-mini, Decisions API | Step-7 report exists |
| Thu 3 Dec | Scam Radar on a phone | "A 270M model checking scam texts on a phone, offline: here's the memory it takes." | `results.mp4` from real `device.json` files | Phone test ran |
| Tue 8 Dec | Autopilot learning curve | "I let an agent learn my obby for a month" | Game-scored curve plus a recording | The curve shows a trend |
| Thu 10 Dec | Prompt injection in strange places | "Prompt injection hides in strange places: Wi-Fi names, Bluetooth names, 3D files." | A short video on your own network | W8 results exist; own network and agent only |
| Tue 15 Dec | Spark-1 v2 in 3D | "Can a 5B model tell which chair is bigger from one photo? I built thousands of rooms to find out." | Rendered rooms with v1 vs v2 answers, plus one 3D illusion | 3D eval report exists; ABO credited (CC BY 4.0) |

Where today's numbers come from:

| Number | File |
| --- | --- |
| 48.5% / 11.5% | lost-in-transliteration `LOG.md` (prompt-guard-2 en vs roman_ur TPR), `results/classifiers*` |
| 458 / 780, 1.3% | spark-lab PR #2 `results/` (doctor auto-fix) |
| 0.9999 / 0.41 | agent-firewall `results/RESULTS.md`, `results/external_eval.json` |
| 31% (order agreement 0.690, n = 300) | spark-one `runs/eval-only/gpt-4o-mini/eval/report.md` |
| 0.564 accuracy, ECE 0.399 (zero-shot E2B, 133 graded items) | spark-one zero-shot E2B report (see HANDOFF.md status table) |

## Rules

- Numbers come only from result files. If a number isn't in a file yet, the post waits.
- Say what is simulated, synthetic, CPU-only or a prototype in the post itself.
- Failures are posts too.
- Tell a vendor a few days before a post names their tool's weakness.
- No Voldex or NFL material, nothing from `eval/locked/`, no real messages without consent.
- Format: a hook line, 3-5 short lines and one visual. Put the repo link in the first comment.
  Reply to comments for the first hour.
- Credit the open models (Gemma, Qwen), and say Claude Code wrote much of the code.

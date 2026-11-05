# Run order, November-December 2026

The full plan, with the timeline drawing, risks and handover, is the doc
[JzLab Master Plan](https://claude.ai/artifact/GbA5WRgV3QSNm6orwoh69W). This file is the
coordinator's working copy. The coordinator updates "State"; dates move only when Jehanzeb agrees.

Lost in Transliteration gets the Spark by day until 16 Nov: the Anthropic Research Residency
closes **22 Nov** and Jehanzeb submits on **Thu 19 Nov**. Smaller jobs fill the nights.

## Workstreams

| # | Workstream | Thread | Start prompt | Window | Teacher | Done when |
| --- | --- | --- | --- | --- | --- | --- |
| W0 | Spark and JzLab setup | Spark (setup) | `agents/setup/prompt.md` | 5-6 Nov | starts it | teacher serves, smoke job passes, phone alert, `jz rc status` all serving |
| W1 | Lost in Transliteration + application | Spark (lit) + cloud | `agents/lit/prompt.md`; `prompts/threads/lit-*.md`; `prompts/residency-application.md` | 5-19 Nov | shares | write-up public, every number traced, application submitted 19 Nov |
| W2 | Research vault `jz-brain` | cloud | `prompts/threads/brain-setup.md` | 5-6 Nov | none | test question answered with page citations |
| W3 | Spark-1 | cloud + Spark (spark1) | `prompts/threads/spark1-*.md`; `agents/spark1/prompt.md` | 6 Nov-21 Nov | shares; **off** for LoRA 17-18 Nov | step-7 eval report; served on :8001 |
| W4 | Agent firewall | cloud + Spark (firewall) | `prompts/threads/firewall-post-check.md`; `agents/firewall/prompt.md`, then `prompt-part2.md` | 6-12 Nov, 22-25 Nov | shares | real-agent and BIPIA numbers; Spark-1 judge results |
| W5 | Scam Radar | Spark (scam) + phone | `agents/scam/prompt.md` | nights 6-7 Nov; phone 14-15 Nov | shares | export passes `--strict`, runs on the phone with measured memory |
| W6 | spark-lab | Spark (heal) + cloud | `agents/heal/prompt.md`; `prompts/threads/pr3-split.md` | 7 Nov; PR #3 this week | **off** about 2 h on 7 Nov | heal Steps 1-5 verified, #2 and #3 merged |
| W7 | Autopilot | Mac | `agents/autopilot/prompt.md` | any time | none | learning curve in `docs/results-gauntlet.md` |
| W8 | Prompt injection in strange places (Wi-Fi, Bluetooth, captive portal, 3D asset files); later Air IDS, status pane, CI eval gates | cloud + Spark + owner | `prompts/threads/injection-strange-places.md` | 27 Nov-10 Dec | shares | `results/CHANNELS.md` per channel, with and without the firewall |
| W9 | Spark-1 v2 sees in 3D (ABO furniture rendered with 67.js; size, count, depth, Box, 3D illusions) | cloud + Spark | `prompts/threads/spark1-3d-bank.md` | 2-15 Dec | shares; maybe off for v2 training | 3D eval report: v1 vs v2, plus the 3D illusion set |

## Key dates

| Date | What |
| --- | --- |
| Thu 5 Nov | Spark set up; project created; vault, write-up draft and PR #3 split start in the cloud |
| Fri 6 Nov | lit detector training starts; Scam Radar trains overnight; Decisions API adapter |
| Sat 7 Nov | heal Steps 1-2 (teacher off about 2 h) |
| Tue 10 Nov | Post: agent firewall |
| Wed 11 Nov | Spark-1 steps 0-2 and teacher scoring start |
| Thu 12 Nov | Post: Spark-1 teaser |
| Fri 13 Nov | Write-up draft complete; vendor heads-ups sent; Urdu review sample rated |
| Sat 14 Nov | Fresh-eyes review; Scam Radar phone test |
| Sun 15 Nov | Jehanzeb edits the write-up |
| Mon 16 Nov | Write-up public; Residency answers drafted |
| Tue 17 Nov | Post: Lost in Transliteration; Spark-1 LoRA (teacher off, 17-18 Nov) |
| Thu 19 Nov | **Submit the application**; post: Scam Radar launch |
| 20-21 Nov | Spark-1 evals; served on :8001 |
| 22-25 Nov | Firewall part 2 (Spark-1 as judge); Tue 24 post: self-healing |
| Thu 26 Nov | Post: agent firewall part 2 |
| 27-29 Nov | W8 injection lab code |
| 1, 3, 8, 10 Dec | Posts: Spark-1 results, Scam Radar on a phone, Autopilot curve, prompt injection in strange places |
| 2-13 Dec | W9: 3D generator (cloud), render and train v2 (Spark) |
| Tue 15 Dec | Post: Spark-1 v2 in 3D |

## Concurrency

- At most 3 Spark threads at once, plus about 2 cloud threads.
- The teacher is off only for heal Step 2 (7 Nov) and Spark-1 LoRA (17-18 Nov), never both on
  one day, and only after Jehanzeb says yes.

## State

| Workstream | State | Last checked |
| --- | --- | --- |
| W0 setup | not started | - |
| W1 lit | cloud phases done; GPU training, analysis, write-up left | 5 Nov |
| W2 vault | not started | - |
| W3 Spark-1 | CPU baselines done; GPU work not started | 5 Nov |
| W4 firewall | CPU results and post draft done | 5 Nov |
| W5 Scam Radar | pipeline and app done; not trained | 5 Nov |
| W6 spark-lab | PRs #1-#3 open, CI green | 5 Nov |
| W7 Autopilot | Gauntlet built; curve not run | 5 Nov |
| W8 injection lab | planned | 5 Nov |
| W9 Spark-1 v2 in 3D | planned | 5 Nov |

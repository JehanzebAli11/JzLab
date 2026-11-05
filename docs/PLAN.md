# Run order, November 2026

The living version, with the timeline drawing, is the doc
[Spark & LinkedIn Plan](https://claude.ai/artifact/4pwZnw44HKt5AH9u4Cfypp). This file is the
orchestrator's copy. The orchestrator updates the "State" column; dates move only when
Jehanzeb agrees.

Lost in Transliteration gets the Spark by day until 16 Nov, because the Anthropic Research
Residency closes **22 Nov** and Jehanzeb submits on **19 Nov**. Smaller jobs fill the nights.

| Phase | Agent | Window | Starts when | Teacher | Done when |
| --- | --- | --- | --- | --- | --- |
| A | `setup` | Nov 5-6 | now | starts it | teacher serves, smoke job passes, phone alert arrives, PR #1 merged |
| B | `lit` | Nov 6-16 | A done | shares | write-up drafted (14 Nov); owner reviews 15 Nov; application in 19 Nov |
| C | `scam` | nights Nov 6-8, phone test Nov 14-15 | A done | shares | export chosen, phone numbers in `device.json` |
| D | `heal` | Nov 7 (daytime) | A done | **off** during Step 2 | Steps 1-5 verified; PR #2 merged |
| E | `firewall` | nights Nov 9-12 | A done | shares | Steps 0, 2, 3, 4; BIPIA AUROC after retraining |
| F | `spark1` | Nov 11-21 | B's GPU work done (detectors trained) | shares, **off** for LoRA (about Nov 17-18) | eval report (step 7), served on :8001 |
| G | `firewall` (`--prompt agents/firewall/prompt-part2.md`) | Nov 22-25 | F serving on :8001 | shares | Spark-1 judge results |
| - | `autopilot` (Mac) | all month | anytime | none | learning curve in `docs/results-gauntlet.md` |

## Concurrency

- Up to 3 Spark agents at once. Suggested sets:
  - Nov 6-8: `lit` + `scam` + `heal`
  - Nov 9-12: `lit` + `firewall` + `spark1` (steps 0-2)
  - Nov 13-21: `lit` (write-up) + `spark1`
  - Nov 22+: `spark1` + `firewall` part 2
- Teacher off windows: only `heal` Step 2 (1-2 h, daytime Nov 7) and `spark1` step 6
  (3-6 h). Never both on the same day.

## State

| Agent | State | Last checked |
| --- | --- | --- |
| setup | not started | - |
| lit | not started | - |
| scam | not started | - |
| heal | not started | - |
| firewall | not started | - |
| spark1 | not started | - |
| autopilot | not started | - |

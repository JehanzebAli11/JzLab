# Sprint threads

One row per worker thread. "bridge" = control-session worker using the Mac bridge VM (code, tests, docs, Claude API).
"native Mac" = a Claude Code session Jehanzeb opens in Terminal. "Spark" = waiting until he says the Spark is set up.

| ID | Where | Folder | Ticket / source | State | Last verified result | Next step |
| --- | --- | --- | --- | --- | --- | --- |
| a | bridge | ~/lab/worldsmith | SPEC WS-01 | done, pushed d01968a | make test 49 passed (control re-ran); CI run in progress | — |
| a2 | bridge | ~/lab/worldsmith | SPEC WS-02 | started 2026-11-09 19:10 | — | HANDOFF after WS-02, then WS-03 needs Studio |
| b | native Mac | ~/lab/lost-in-transliteration | prompts/threads/lit-native-mac.md (RUNBOOK step 5, 7, 8) | prompt sent 2026-11-09 18:45, waiting for owner to open | — | MPS check, first-epoch ETA |
| c | bridge | ~/lab/agent-firewall | prompts/threads/firewall-post-check.md | done 2026-11-09 18:55 (agent-firewall 6e49626) | every post number re-computed from results/*.json by control | owner: card says 8 hiding tricks (files: 7); headline choice |
| d | bridge | ~/lab/JzLab | ROADMAP §8 CV v5 | drafted 2026-11-09 19:20 in a private doc (claude.ai/artifact/KsA12BK42bzMuj7sjmBPY3); drafts/ git-ignored (JzLab is public) | AI-work numbers re-checked against results files | owner fills 7 placeholders, confirms [CHECK] items |
| e | control | — | ROADMAP §4.5 World Labs ask | drafted 2026-11-09, with owner to send | — | owner sends by 12 Nov |
| f | bridge | ~/lab/JzLab | jzapi helper + state/SPEND.md | done 2026-11-09 (5d33838) | 46 passed (control re-ran); prices match pricing page 9 Nov; model IDs not live-checked (VM proxy blocks keyed API calls) | owner: `python -m jzapi.models --verify` on the Mac |
| f2 | bridge (code) + native Mac (paid run) | ~/lab/lost-in-transliteration | RQ3 Sonnet 5.5 + Opus 5.5 via Batch, ≤ $20 | code started 2026-11-09 19:40 | — | owner runs sanity (20 tasks) in Terminal |
| g | bridge | ~/lab/JzLab | Thu 12 Nov kickoff post | queued (Wed) | — | — |
| — | Spark | — | LIT training fallback, B4 Gemma (wk 4) | waiting for Spark | — | — |

# Sprint threads

One row per worker thread. "bridge" = control-session worker using the Mac bridge VM (code, tests, docs, Claude API).
"native Mac" = a Claude Code session Jehanzeb opens in Terminal. "Spark" = waiting until he says the Spark is set up.

| ID | Where | Folder | Ticket / source | State | Last verified result | Next step |
| --- | --- | --- | --- | --- | --- | --- |
| a | bridge | ~/lab/worldsmith | SPEC WS-01 | done, pushed d01968a | make test 49 passed (control re-ran); CI run in progress | — |
| a4 | bridge + Studio MCP | ~/lab/worldsmith | SPEC WS-04 / M0 gate | done 2026-11-09, M0 PASS (bundles/m0/gate.json) | F1-A FELL 3/3, fix SUCCESS 3/3, same controller 3743d998; config committed 15:52:55Z before first gate call 15:53:15Z; 852 passed (control re-ran) | owner: re-save place; restart Claude app for built-in Studio MCP; plan WS-05..08 |
| a2 | bridge | ~/lab/worldsmith | SPEC WS-02 | done, pushed 0f0aa37 | 606 passed (control re-ran); HASHES.md --check ok; fix.json differs only in bridge_1.length | WS-03: owner opens Studio; decide BRIDGE_CROSSED trigger placement |
| b | native Mac | ~/lab/lost-in-transliteration | prompts/threads/lit-native-mac.md (RUNBOOK step 5, 7, 8) | done 2026-11-09 (commits 929a10d, 900ec4b, 31980f6, pushed by the session) | 6 detector runs trained on MPS + evaluated; analyze: all figures except fig9 (RQ7 probe, never run); write-up drafted | fresh-eyes review running; owner reviews writeup/ |
| c | bridge | ~/lab/agent-firewall | prompts/threads/firewall-post-check.md | done 2026-11-09 18:55 (agent-firewall 6e49626) | every post number re-computed from results/*.json by control | owner: card says 8 hiding tricks (files: 7); headline choice |
| c2 | bridge | ~/lab/agent-firewall | card 8→7 + headline switch (owner 1A, Switch) | done, pushed 78f3d76 | card regenerated on Mac, checked by control | owner posts Tue 10 Nov |
| a3 | bridge + Studio MCP | ~/lab/worldsmith | SPEC WS-03 (+ BRIDGE_CROSSED ADR, P0 route test) | done 2026-11-09, pushed 3fd28cd | 771 passed (control re-ran); live F1-A/F1-E read-back 26/26, 0 diffs (bundles/ws03); route (a) probe n=1 each | owner: ADR 0004 decisions, then WS-04 |
| f3 | bridge (code) + native Mac (paid) | ~/lab/lost-in-transliteration | RQ3 uniform 1024 rerun + REVIEW analysis fixes | done 2026-11-09 (7f47dcd) | 5 models x 927 at 1024, 0 at cap; Haiku ur +0.14 Holm p 0.011 | — |
| w2 | bridge | ~/lab/lost-in-transliteration | write-up revision vs REVIEW.md | done 2026-11-09 (27062ce) | REVISION.md maps every review item | owner reads writeup/, rewrites blurb's last line; vendor heads-up 13 Nov |
| a9/a10 | bridge | ~/lab/worldsmith | SPEC WS-09 random sampler + WS-10 architect client | done 2026-11-10 | 1421 passed (control re-ran); B2 offline: accepted+connected M0 16/600, M1 1/600 | owner: approve architect_ladder ($90) for live smoke call |
| a7/a8 | bridge | ~/lab/worldsmith | SPEC WS-07 nav + WS-08 classifier | done 2026-11-09 | 1301 passed (control re-ran); M0 F1-A labelled BRIDGE_SHORT_HYPOTHESIS with evidence | M1 done: WS-09 architect client next (needs approval for live calls) |
| a6 | bridge | ~/lab/worldsmith | SPEC WS-06 validator | done 2026-11-09 (dcf444b) | 1212 passed (control re-ran); 69 abuse rejected, 13 legit pass; 28 stable codes | WS-07, WS-08 started |
| a5 | bridge | ~/lab/worldsmith | SPEC WS-05 patch apply | done 2026-11-09 (f43f41a) | 1026 passed (control re-ran); M0 fix reproduced as a patch | WS-06 validator next |
| g | bridge | ~/lab/JzLab | Thu 12 Nov kickoff post + shot list | drafted, committed a897db6 | numbers traced to bundles/m0 | owner records clip Wed (fresh logged runs) |
| v1 | bridge | ~/lab/lost-in-transliteration | vendor heads-up drafts | done 2026-11-10 (local only, git-ignored) | 6 notes; 3 main (Meta, Patronus Protect, Protect AI) | owner sends 13 Nov |
| d | bridge | ~/lab/JzLab | ROADMAP §8 CV v5 | drafted 2026-11-09 19:20 in a private doc (claude.ai/artifact/KsA12BK42bzMuj7sjmBPY3); drafts/ git-ignored (JzLab is public) | AI-work numbers re-checked against results files | owner fills 7 placeholders, confirms [CHECK] items |
| e | control | — | ROADMAP §4.5 World Labs ask | drafted 2026-11-09, with owner to send | — | owner sends by 12 Nov |
| f | bridge | ~/lab/JzLab | jzapi helper + state/SPEND.md | done 2026-11-09 (5d33838) | 46 passed (control re-ran); prices match pricing page 9 Nov; model IDs not live-checked (VM proxy blocks keyed API calls) | owner: `python -m jzapi.models --verify` on the Mac |
| f2 | bridge (code) + native Mac (paid run) | ~/lab/lost-in-transliteration | RQ3 Sonnet 5.5 + Opus 5.5 via Batch, ≤ $20 | done 2026-11-09, pushed 39ea748 | 927 rows each; Sonnet 0.105 at cap, Opus 0; 0 empty; $4.79 (usage.csv) | — |
| g | bridge | ~/lab/JzLab | Thu 12 Nov kickoff post | queued (Wed) | — | — |
| — | Spark | — | LIT training fallback, B4 Gemma (wk 4) | waiting for Spark | — | — |
| a14 | VM (control) | p0.v3 spawn check + close m2_f1a_pilot + configs smoke_f1e_p0v3 / m2_f1a_b3 | running | pilot B0-B2 valid; B3 SYSTEM_ERROR (harness flake) | then: restart Studio, smoke 6/6, run m2_f1a_b3 (<= $2.96) |

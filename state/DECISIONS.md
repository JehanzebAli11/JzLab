# Decisions and approvals

One line per approval, redirect or teacher change, newest last:
`YYYY-MM-DD HH:MM  agent  what was approved or said  (why)`

2026-11-09 18:32  owner  Licence for worldsmith: Apache-2.0  (matches Autopilot)
2026-11-09 18:32  owner  Credit evolve as PR #39, merged into ramenvr/autopilot staging 7 Nov 2026 04:48 PKT (68ab39b)  (verified on upstream staging)
2026-11-09 18:32  owner  Send the World Labs credit ask by 12 Nov: ~$50 (optionally $100) on his own account, 3 questions in writing  (control drafts, owner sends)
2026-11-09 18:32  owner  LIT detector training runs in a native Claude Code session on the Mac (MPS); Spark is the fallback if it can't finish by Thu 12 Nov  (bridge VM has 3 GB RAM, no MPS, HF blocked)
2026-11-09 18:32  owner  File deletion enabled in ~/lab, only for git's own lock files and files the control thread creates; anything else needs his yes
2026-11-09 18:32  owner  Up to $20 of Claude API for LIT RQ3 (Sonnet 5.5, Opus 5.5 via Batch), inside the $40 LIT cap  (sanity run first; stop before $20)
2026-11-09 18:32  owner  Push to his own repos only (worldsmith, LIT, agent-firewall, JzLab) after tests pass; never force-push; never push to ramenvr
2026-11-09 18:32  owner  ROADMAP §2: BIPIA transfer corrected from 0.41 to 0.398 AUROC (n = 350)
2026-11-09 18:32  owner  Bridge VM does code, tests, docs, Claude API runs. Real-Mac work (MPS training, HF downloads, Autopilot roblox-mcp, Godot, recordings) goes to native Claude Code sessions he opens; tracked as "native Mac" in state/SPRINT.md
2026-11-09 18:32  owner  WS-04 risk: before WS-03 ends, test (a) server-script MoveTo via run_script_in_play_mode and (b) Autopilot roblox-mcp natively; recommend one with evidence; same test decides if P1 (Claude player) is possible
2026-11-09 18:40  control  JzLab main had unrelated history vs origin (same trees). Rebased the one unpushed local commit (ROADMAP) onto origin/main; backup branch backup/pre-rebase-2026-11-09. No force-push.
2026-11-09 19:25  control  CV v5 kept out of git (phone/email; JzLab is public); drafts/ added to .gitignore; CV draft lives in a private doc
2026-11-09 19:40  control  Bridge VM's proxy blocks keyed calls to api.anthropic.com (401 from proxy). Paid Claude API runs move to the Mac terminal; bridge workers write and test code only. Key not moved.

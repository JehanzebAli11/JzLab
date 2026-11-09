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
2026-11-09 19:56  owner  LIT RQ3: keep Opus 5.5 (thinking on, effort low, max_tokens 1024) as its own labelled condition (A)
2026-11-09 19:56  owner  Firewall post: fix the card's "8 hiding tricks" to 7 and regenerate (1A); lead with held-out attack styles 23.3% → 0.2% (2 Switch)
2026-11-09 19:56  owner  state/APPLICATIONS.md stays local only (git-ignored); JzLab stays public (A)
2026-11-09 19:56  owner  BRIDGE_CROSSED trigger anchored to the far side of gap_1 (first 2 studs of plat_b), not the bridge's far half (A); WS-03 records an ADR
2026-11-09 20:16  owner  LIT RQ3: Sonnet 5.5 max_tokens raised to 400 (A); sanity round 2 first, then full run (worst case $14.62)
2026-11-09 20:29  owner  WS-04 (ADR 0004): P0 = server-scripted Humanoid:MoveTo waypoints (route a); SPEC §9 P0 wording updated and disclosed in every clip
2026-11-09 20:29  owner  Enable Studio's built-in MCP server alongside WS-04 for route (b) / P1 (owner toggles it in Studio)
2026-11-09 20:29  owner  Dedicated saved place for Worldsmith with a fixed standard character (LoadCharacterAppearance off / StarterCharacter)
2026-11-09 20:29  owner  F1-A 10-stud hole kept for M0 (P0 never jumps); widen to >= 14 studs before any jumping player (P1/P2)
2026-11-09 20:29  owner  T_attempt = 60 s, declared in config before any comparison
2026-11-09 20:29  owner  Disable the "UI Workflow" and "robloxstudio-mcp" Studio plugins if unused (owner's action)
2026-11-09 20:29  owner  LIT detector training session started natively on the Mac
2026-11-09 21:10  control  M0 PASS verified (gate.json, config hash, commit time before first gate call, 852 tests). Defaults for a4's open questions: keep bundles/m0 and smoke runs committed as evidence; accept unenforceable run_code timeouts for M0 (revisit WS-11 / route b); BRIDGE_SHORT_HYPOTHESIS left to WS-08's classifier
2026-11-09 21:13  owner  LIT RQ3 option A: re-run Haiku, Sonnet, nano (and Gemma) at a shared max_tokens 1024 to remove truncation; within lit_rq3 $20 cap; owner runs paid steps on the Mac. Write-up fixes per writeup/REVIEW.md
2026-11-09 21:30  control  WS-05 done (1026 tests). Defaults for its questions: patch bumps version (ADR 0006); WS-06 rejects no-op patches as wasted revisions; malformed-before-stale order kept; schema in grammar/, code in validator/

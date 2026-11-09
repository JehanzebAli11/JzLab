# Task: route (b) probe — Studio's built-in MCP server from a native Claude Code session

Folder: `~/lab/worldsmith` (native Claude Code session on the MacBook). Read `docs/ADR/0004-p0-driver.md`,
`docs/ADR/0005*.md`, `docs/M0.md` and the latest `docs/HANDOFF.md` entry first.

Setup (owner, once): in Roblox Studio → Assistant settings → MCP Servers, "Enable Studio as MCP server" is on;
click "Claude Code CLI" under Quick connect and follow its instructions (it adds the server to Claude Code),
then start this session with `cd ~/lab/worldsmith && claude` and open `places/worldsmith-lab.rbxl` in Studio.

Steps (feasibility only — not an M0/M2 result; one run each; no paid calls):
1. `/mcp`: list the Studio server's tools. Record names and descriptions in `docs/ADR/0006-route-b.md`.
2. In Edit mode, build F1-E with `python -m worldsmith.runner ...` as WS-04 does, or via the Studio tools; confirm read-back.
3. Start play. Check, once each: can you run Luau in the RUNNING game (server and client), read console output
   during play, send keyboard/mouse input to the character, and capture a screen still? Save any still to
   `bundles/routeb/` (git-ignored if > 1 MB).
4. Try to walk the F1-E route with keyboard input only (W held, camera fixed) for a few seconds; record whether
   the character moves and whether WS events print with the nonce.
5. Verdict in ADR 0006: can an outside Claude agent (P1) play through these tools? What's missing?
Rules: owned place only; no published or live games; never lower the M0 bar; commit small with
`Jehanzeb Ali <jehanzeb1111@icloud.com>`; append a HANDOFF entry (Done · Verified · Next · Open questions); don't push to
anyone else's repo; stop after step 5.

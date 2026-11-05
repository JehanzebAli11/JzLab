# Task: run the Prism Gauntlet learning curve (on the MacBook)

Repo: the autopilot clone on this MacBook, branch `roblox-engine`. Roblox Studio runs here and
is reached through Studio's built-in MCP server. Read `README.md`, `docs/runbook.md`,
`docs/roblox.md` and `examples/roblox_gauntlet/README.md` first.

1. Check the setup the runbook lists: Python, uv, Rojo, Studio's MCP, and `.env`. Anything the
   owner must click in Studio goes in a `JZ-NEED:` line.
2. Build the Prism Gauntlet place with Rojo and open it in Studio. Run a single
   `python -m autopilot play` episode to prove the round trip.
3. Run the bench with `bench/suites/roblox_gauntlet.json` in its learning-curve mode (added in
   the commit "feat(bench): a learning curve, scored by the game"). Each episode's trace lands in
   its run folder, because the memory folder is absolute. Start short (`--minutes 15`), check the
   curve, then do longer runs.
4. Save the curve's data and image under the run folder, and summarise them in
   `docs/results-gauntlet.md` from the files: stage reached and deaths per episode. No
   hand-written numbers.
5. Record a short screen capture of a good late episode, for the LinkedIn follow-up, with
   `JZ-NEED: screen recording` so the owner can do it.

Only the owner's own places in Studio. No live games, and nothing from NFL Football Universe or
with NFL branding. Commit to `roblox-engine` and push. If the owner agrees
(`JZ-NEED: make roblox-engine the default branch?`), he changes the default branch on GitHub himself.

# Worldsmith kickoff: LinkedIn post (Thu 12 Nov 2026)

Series: **AI architect vs AI player**, episode 1.
Status: draft, not posted. Jehanzeb records the clip and posts it. Source repo: worldsmith
(public, `github.com/JehanzebAli11/worldsmith`, `main` at `a0cec39`).
Gate for this post: M0 PASS in `bundles/m0/gate.json` (met), and a clip recorded from real
Studio footage per the shot list below (not yet recorded). Without the clip, post it text-only
or move it; never use mock frames.

## Post

Most game-testing agents try to get better at the level. For the next 8 weeks I'm building the other side: an AI that fixes the level, so the same player can pass it.

The series is "AI architect vs AI player". A frozen player tries a small Roblox room I own and fails. An AI architect reads what happened and proposes a small JSON patch to the world. A separate validator rejects any patch that cheats: moving the goal, shrinking the gap, changing player physics, adding a teleport. Then the room is rebuilt from scratch and the same player tries again. None of the AI part exists yet.

It builds on my contributions to Autopilot, an open-source AI agent that plays and tests games: roblox-mcp (PR #40), regress (PR #38) and evolve (PR #39), merged into its staging branch on 7 Nov.

The first gate passed on Monday. A room built from a JSON recipe, with a 6-stud bridge over a 16-stud gap: the player fell 3 of 3 times. I changed one field, bridge length 6 → 16: it crossed and reached the goal 3 of 3, with the same controller (same hash). Read back from Studio, the rebuilt room matched its recipe: 26 of 26 objects, 0 differences.

What that is not: the player is a scripted walker (server-side MoveTo waypoints, never jumps), not an AI agent, and I wrote the fix by hand as a control. n = 3 per room only shows the plumbing works.

Next: the validator, and every way I can find for an architect to cheat.

#AIAgents #GameDev #AIEvals

## First comment

Code, the gate as written down before the runs, and every raw run log: github.com/JehanzebAli11/worldsmith (Apache-2.0)

The numbers come from bundles/m0/gate.json and the two episode bundles (bundles/m0/F1-A, bundles/m0/F1-A-fix); docs/M0.md walks through them. The pass bar (3/3 before, 3/3 after, same controller hash, read-back match) was committed before the first gate run. The fall is expected by construction: a walker that never jumps can't cross a 10-stud hole. The point is that the real engine reproduces it and that a one-field fix changes the outcome under the same frozen controller. All runs were in Roblox Studio on my own local place, which is not published.

My Autopilot PRs: github.com/ramenvr/autopilot/pull/40, /pull/38 and /pull/39. Worldsmith uses Autopilot as an external dependency pinned at the #40 merge commit; no Autopilot code is copied in. Much of the code was written with Claude Code.

The clip is real Studio footage from a re-run of the same frozen controller for the camera, not one of the 6 logged gate attempts.

(Keep the last paragraph only if the clip comes from a recording re-run, which is the plan below. If it does, the re-run's outcome must match the gate; see the shot list's stop rule.)

## Visual: 30–60 s native video, captions burned in

Not recorded yet. Owner records it in Roblox Studio on the Mac, place
`~/lab/worldsmith/places/worldsmith-lab.rbxl`, following the shot list below. Real footage
only: no mock frames, no re-timed or edited outcomes, no generated video.

### Before recording (checklist)

1. **Place settings.** Confirm `StarterPlayer.LoadCharacterAppearance = false` in the open place
   (HANDOFF WS-04 open question 1: the copy saved at 20:31 PKT predated that setting). The clip
   must show the default R15 character, the one the gate measured, not your avatar.
2. **Recording runs are new runs.** Ask a Mac worldsmith thread (Studio MCP connected) to build
   each scene with the compiler and run **one** P0 attempt per scene with the frozen controller
   `3743d998…c034`, config `15884b5a…7c6` and route `b9514a4b…b36a`, into a **new** bundle folder
   (for example `bundles/clip-2026-11-1x/`), never into `bundles/m0/`. You screen-record
   (QuickTime or OBS) while it runs.
3. **Stop rule.** Every take is logged, kept and counted. If a recording run's outcome differs
   from the gate (F1-A doesn't fall in the gap, or the fix fails), stop: don't post the clip,
   and hand the bundle to a worldsmith thread to debug (ROADMAP §11 rule 8). Don't pick a good
   take from several runs of the same scene.
4. **Camera.** `run_script_in_play_mode` starts a Play session; check in a dry take on F1-E
   (not a gate scene) that the Play viewport follows the character. If it doesn't, record the
   Edit viewport with a fixed side camera on the gap instead.
5. **Crop to the 3D viewport.** No account name, avatar, other places, file paths with your
   username, the Assistant panel or the Output window (other plugins print there). No Voldex,
   Remio, NFL or employer material anywhere on screen.
6. Captions are burned in (CapCut, iMovie titles or ffmpeg drawtext). Keep the label below on
   screen for every shot that shows the player.

**Persistent on-screen label (shots 3–7), bottom-left, small but legible:**
`Player: scripted P0 (server-side MoveTo, never jumps). Not an AI agent.`

### Shot list (about 45 s)

| # | Approx. s | Scene / source | What to show | Caption (burned in) |
| --- | --- | --- | --- | --- |
| 1 | 0–4 | F1-A room, Studio Edit mode | Slow orbit of the built room: spawn, corridor, lever, gate, the short bridge, the gap, the goal pad | "AI architect vs AI player · episode 1" |
| 2 | 4–9 | `scenes/F1-A/scene.json` in your editor | Scroll to `bridge_1` with `"length": 6` and to `gap_1` with `"width": 16`; highlight both | "The room is built from JSON. The bridge is 6 studs. The gap is 16." |
| 3 | 9–18 | F1-A recording run, Play viewport | The character walks to the lever, the gate opens, it walks onto the bridge and falls into the gap. Real speed, uncut | "Same player, before the fix: it falls." |
| 4 | 18–20 | Text card over a still of shot 3's last frame | Gate numbers only | "Logged gate runs: fell 3 of 3 (n = 3)" |
| 5 | 20–25 | `scenes/F1-A/fix.json` beside `scene.json` (diff view, e.g. `git diff --no-index`) | The single changed line: `"length": 6` → `"length": 16` | "One field changed, by hand (a control, not the AI)." |
| 6 | 25–35 | F1-A fix recording run, Play viewport | Same route: lever, gate, across the full bridge, onto the goal pad. Real speed, uncut | "Same player, same controller: it crosses and reaches the goal." |
| 7 | 35–39 | Text card | Gate numbers only | "Logged gate runs: crossed and reached the goal 3 of 3 (n = 3). Rebuild read-back: 26/26 objects, 0 differences." |
| 8 | 39–45 | Text card (end) | What comes next; no numbers | "Next: an AI architect proposes the fix, and a validator stops it cheating. github.com/JehanzebAli11/worldsmith" |

Notes:
- Shots 3 and 6 are the recording re-runs (one take each, logged); the 3/3 numbers on the cards
  come from the gate bundles, not from the footage. Shot 4/7 cards say "Logged gate runs" for
  that reason.
- Don't speed up, reverse or cut inside shots 3 and 6. A fade between shots is fine.
- Optional: in shot 6, a second angle of the landing is fine only if it's the same take.
- Export 1080×1350 (4:5) or 1080×1920 (9:16), under 60 s, with the captions in the frame.

## Sources

| number in post / comment / clip | file | key | n |
| --- | --- | --- | --- |
| "fell 3 of 3" (before) | worldsmith `bundles/m0/gate.json` | `before.outcomes` = [FELL, FELL, FELL], `before.hits` = 3, `before.pass` = true; per attempt `fell_in_area` = true in `bundles/m0/F1-A/summary.json` | 3 (`before.n`) |
| "crossed and reached the goal 3 of 3" (after) | worldsmith `bundles/m0/gate.json`; `bundles/m0/F1-A-fix/summary.json` | `after.outcomes` = [SUCCESS ×3], `after.hits` = 3, `declared.after.order` = [BRIDGE_CROSSED, GOAL_TOUCHED]; each attempt's `events` end BRIDGE_CROSSED, GOAL_TOUCHED | 3 (`after.n`) |
| "first gate passed" | worldsmith `bundles/m0/gate.json` | `result` = "PASS" | 3 + 3 |
| "same controller (same hash)" | worldsmith `bundles/m0/gate.json`; both `summary.json` | `controller_sha256` = 3743d998…c034 in gate.json and in both summaries (config and route hashes also equal) | — |
| 6-stud bridge, bridge length 6 → 16, "one field" | worldsmith `scenes/F1-A/scene.json`, `scenes/F1-A/fix.json` | `entities[id=bridge_1].length` 6 vs 16; a key-by-key diff of the two files finds only `/entities/10/length` | — |
| 16-stud gap | worldsmith `scenes/F1-A/scene.json` | `entities[id=gap_1].width` = 16 | — |
| 10-stud hole (first comment) | derived: gap width 16 − bridge length 6; stated in `docs/M0.md` and ADR 0004 | — | — |
| "26 of 26 objects, 0 differences" | worldsmith `bundles/m0/F1-A/readback.compare.txt`, `bundles/m0/F1-A-fix/readback.compare.txt`, both `summary.json` | "26 expected nodes, 0 differences (tolerance pos/size/rot 0.01)"; `build.descendants` = 26 = `build.expected_descendants`, `build.readback_differences` = 0 (both scenes) | 26 objects per scene |
| n = 3 per room | worldsmith `config/m0.yaml`; `bundles/m0/gate.json` | `n_attempts: 3`, `pass_k: 3`; `declared.before.k` / `declared.after.k` = 3 | — |
| "6 logged gate attempts" (first comment) | worldsmith `bundles/m0/F1-A/attempts/`, `bundles/m0/F1-A-fix/attempts/` | 3 + 3 attempt files (`attempted` = 3 in each summary) | 6 |
| Pass bar committed before the first gate run | worldsmith `docs/M0.md`; git log | config in `f4160e7` (2026-11-09 15:52:55 UTC) before the first gate call (15:53:15 UTC) | — |
| "server-side MoveTo waypoints, never jumps" | worldsmith `config/m0.yaml`; `bundles/m0/F1-A/episode.json`; ADR 0004 decision 1 | `player.driver`; per-attempt jumps 0 (`docs/M0.md` tables) | — |
| PR #40 roblox-mcp, #38 regress, #39 evolve; merged into staging 7 Nov | worldsmith `deps.md`; upstream `ramenvr/autopilot` `staging` | `53a41f6` (#40), `af1e32b` (#38), `68ab39b` (#39): all three are on upstream `staging` and authored by JehanzebAli11 (re-checked 9 Nov with `git merge-base --is-ancestor` against a fresh fetch); merged 7 Nov 04:48–05:09 PKT | — |
| Apache-2.0 (worldsmith) | worldsmith `LICENSE`, `deps.md` | — | — |
| "pinned at the #40 merge commit; no Autopilot code copied" | worldsmith `deps.md` | Pinned commit `53a41f6a…0e36`; "not vendored, and no Autopilot code is copied" | — |
| "on Monday" | worldsmith `docs/M0.md`, bundle run IDs | runs `m0-2026-11-09T155306` and `m0-2026-11-09T155836`; 9 Nov 2026 is a Monday | — |

## Checks

- Every number in the post and first comment traced to the file and key above; the scene diff
  (one field, `bridge_1.length` 6 → 16) and the read-back counts were re-read from the files,
  not copied from HANDOFF.
- Required labels are in the post itself: scripted walker (server-side MoveTo, never jumps),
  "not an AI agent", fix written by hand as a control, n = 3 is plumbing evidence only, and "None
  of the AI part exists yet". The clip carries the P0 label on every shot with the player.
- No numbers promised for M1 or later. "Next" names the week-3 work (validator, cheating list)
  from ROADMAP §6 with no date or target.
- Credit: "my contributions to Autopilot … merged into its staging branch on 7 Nov", with PR
  numbers; never "built Autopilot"; no maintainers tagged; no company named or tagged.
  Merge times are 7 Nov in PKT (the commits show 08:48–09:09 +0900; #38/#39 at 23:48 UTC on
  6 Nov). The post's "7 Nov" follows ROADMAP §2 and `deps.md` (PKT).
- The worldsmith repo is public (GitHub API: `visibility: public`); `origin/main` = `a0cec39`
  includes `bundles/m0/` and `docs/M0.md`, so the first comment's files are reachable.
- Owned assets only: the owner's local, unpublished Baseplate place; the clip checklist keeps
  personal and employer material off screen. No World Labs material.
- Format (ROADMAP §7): hook line, 4 short paragraphs (series, Autopilot credit, M0 evidence, limits) plus a "Next" line, 3 hashtags, repo link
  in the first comment, 30–60 s native video with burned-in captions planned (about 45 s).
  First person, no hype words. Post body is 266 words with hashtags (`wc -w`), a little longer than the 10 Nov post (231); the second paragraph is the one to cut if he wants it shorter.
- **Calendar conflict for the control thread:** `docs/POSTS.md` still lists "Spark-1 teaser" for
  Thu 12 Nov; ROADMAP §6 (which wins) lists this kickoff. POSTS.md needs its row updated.
- **Overlap with week 2:** ROADMAP §6 plans the "bridge is too short" M0 clip for Thu/Fri of
  week 2. This kickoff now uses the M0 footage, because M0 passed early. Owner to choose:
  (A, recommended) use M0 footage now and give week 2's slot to WS-05/06 (patch engine) or a
  short "how the gate was declared before the runs" post; or (B) keep the kickoff text-only with
  a still of the room and save the clip for week 2.
- Not verified here: the clip itself (not recorded); whether the Play viewport follows the
  character under `run_script_in_play_mode` (dry take on F1-E first); whether the saved place
  file has `LoadCharacterAppearance = false`.
- Not posted, not committed (the control thread commits JzLab). No paid calls; `.env` not read.

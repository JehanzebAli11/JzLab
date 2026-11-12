# Worldsmith kickoff: LinkedIn post (Thu 12 Nov 2026)

Series: **AI architect vs AI player**, episode 1.
Status: FINAL, ready to post Thu 12 Nov (11 Nov 15:45 PKT). Not posted: Jehanzeb posts it.
Attach: `~/lab/worldsmith/docs/media/episode1.mp4` (53 s, 1080x1350, worldsmith `5fede75`).
Gate for this post: M0 PASS in `bundles/m0/gate.json` (met); clip made from real Studio footage
(met, with the replay disclosure in the first comment; see bundles/clip-2026-11-11/README.md).

## Post

I'm a Roblox and VR game developer. Now I'm building an AI that fixes broken levels.

Most AI game testers try to get better at playing a level. I'm going the other way. When a player gets stuck, can an AI change the level so the same player gets through, without cheating?

Here's how it works. A scripted player walks through a small Roblox room I built and fails. Claude looks at what went wrong and suggests a change to the room. A separate checker throws out anything that cheats, like moving the goal closer or giving the player a teleport. Then the room gets rebuilt and the same player tries again.

First test this week: a bridge that's too short over a gap. The player fell in 3 times out of 3. I made the bridge longer by hand, and it crossed 3 out of 3. Then I gave the broken room to Claude Haiku, Sonnet and Opus. All three suggested the same fix on their first try, and the player made it across every time.

To be clear about what this is: the player is a simple script that never jumps, not an AI. And this room was easy. A random change fixes it too. So all this shows is that the whole loop works in a real game engine. It says nothing yet about which model is better.

Next week: harder rooms, where guessing doesn't work.

It builds on what I contributed to Autopilot, an open-source agent that plays and tests games. My three PRs were merged last week.

The video is the actual room in Roblox Studio.

#AIAgents #GameDev #AIEvals

## First comment

Code and every run log: github.com/JehanzebAli11/worldsmith

I wrote the pass/fail rules down before running anything. The numbers in the post come from bundles/m0/gate.json and bundles/experiments/m2_f1a_b3.

About the video: it's real Studio footage of the same rooms and the same scripted route. I filmed it in normal Play mode because the logged test mode doesn't show the player on screen, so the 3/3 counts come from the logged runs, not the clip.

My Autopilot PRs: github.com/ramenvr/autopilot/pull/40, /pull/38 and /pull/39. I wrote a lot of the code with Claude Code.

More of my work: jz.business

## Visual: 30–60 s native video, captions burned in

Done 11 Nov: `docs/media/episode1.mp4` in worldsmith (53 s). Original plan kept below for the record. Owner records it in Roblox Studio on the Mac, place
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
| "Haiku, Sonnet and Opus … same one-field patch on its first call … completed 3 of 3" | worldsmith `bundles/experiments/m2_f1a_b3/results.json` | per condition: `revisions.verdicts` = [ACCEPTED], `revisions.used` = 1, v2 `outcomes` = [SUCCESS ×3]; each reply's `response_text` = `set bridge_1.length 16` (`<episode>/architect/replies/*.json`) | 1 episode per model; 3 attempts per version |
| "On Tuesday" | worldsmith `results/usage.csv` | architect rows 16:41, 16:57 and 17:22 UTC on 2026-11-10 (a Tuesday) | 3 calls |
| "a random valid patch also fixes it, in 3 tries" | worldsmith `bundles/experiments/m2_f1a_pilot/B2/ep0/summary.json` | verdicts [REJECTED, REJECTED, ACCEPTED]; v2 SUCCESS ×3 (player p0.v2) | 1 episode |
| Clip re-runs: fell 3 of 3, crossed 3 of 3 (first comment) | worldsmith `bundles/clip-2026-11-11/F1-A/summary.json`, `F1-A-fix/summary.json` | counts FELL 3; SUCCESS 3 | 3 + 3 |
| Apache-2.0 (worldsmith) | worldsmith `LICENSE`, `deps.md` | — | — |
| "pinned at the #40 merge commit; no Autopilot code copied" | worldsmith `deps.md` | Pinned commit `53a41f6a…0e36`; "not vendored, and no Autopilot code is copied" | — |
| "on Monday" | worldsmith `docs/M0.md`, bundle run IDs | runs `m0-2026-11-09T155306` and `m0-2026-11-09T155836`; 9 Nov 2026 is a Monday | — |

## Checks

- **12 Nov rewrite (plain voice, owner asked for "less AI-written").** Dropped from the post:
  controller hash, 26/26 read-back, stud sizes, PR names. New wording checked: "this week" (gate
  Mon 9 Nov, AI runs Tue 10 Nov); "every time" (each model's v2 SUCCESS ×3, 1 episode each);
  "A random change fixes it too" (pilot B2 ep0: 2 rejected, 3rd accepted, SUCCESS ×3, player
  p0.v2); "three PRs merged last week" (#40, #38, #39 on staging, 7 Nov PKT); "Next week: harder
  rooms" (harder-rooms post planned Fri 20 Nov). Labels kept: scripted, never jumps, not an AI;
  easy room; says nothing about which model is better. Post ~250 words.

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

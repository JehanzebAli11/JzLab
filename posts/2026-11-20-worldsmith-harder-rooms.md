# Worldsmith harder rooms: LinkedIn post (Fri 20 Nov 2026)

Series: **AI architect vs AI player**, episode 2.
Status: DRAFT, ready to post Fri 20 Nov. Not posted: Jehanzeb posts it.
Slot: ROADMAP §6 week 2 "Thu/Fri" (the M0 clip already went out in the 12 Nov kickoff). Thu 19 Nov
is the Residency deadline, so Fri 20.
Attach: `posts/2026-11-20-worldsmith-harder-rooms.png` (1080x1350; source `posts/src/2026-11-20-harder-rooms-card.html`).
Gate: m2_hard complete with results files committed (met, worldsmith `892a6ec`).

## Post

Last week every Claude model fixed my broken Roblox room. So did a random patch. A test that random guessing passes doesn't tell you much, so I built harder rooms.

Same loop as before. A scripted player fails a small room. An AI architect reads the failed run and proposes a JSON patch. A validator rejects patches that cheat, like moving the goal or shrinking the gap. The room is rebuilt and the same player tries again.

This time the architect can change the bridge, the lever, the gate and the walls, and there are four rooms: a bridge too short, a bridge off to the side of the path, a lever walled off, and both problems at once.

Rooms repaired, out of 3 runs per model per room:
- Random valid patch: 0/12
- Claude Haiku: 6/12 (both bridge rooms, neither lever room)
- Claude Sonnet: 12/12
- Claude Opus: 12/12, fixed on the first call in 11 of 12

Haiku's misses on the lever rooms were the interesting part. Six times it put the lever too close to the path (the rules require a real detour), and four times it also moved the gate out of the way, which the validator counts as bypassing the puzzle. Sonnet and Opus never touched the gate.

The whole run cost $0.98 in API calls.

What this isn't: the player is a scripted walker, not an AI agent. Three runs per model per room are counts, not rates, and four hand-built rooms aren't a benchmark.

Next: more rooms, and checking whether models reach for a cheat when the honest fix gets hard.

#AIAgents #AIEvals #GameDev

## First comment

Code, configs declared before the runs, and every raw run: github.com/JehanzebAli11/worldsmith

The table is in the README ("Harder rooms: m2_hard"); per-room results are in bundles/experiments/m2_hard_f1a … m2_hard_f1d/results.json, and every proposal with its validator verdict is in each episode's proposals.json. The random baseline uses fixed seeds chosen before the run. A few architect replies were relayed by hand rather than live when my session dropped; each one is listed in that room's RELAY_NOTE.md.

More of my work: jz.business

## Sources

| number in post / card | file | key | n |
| --- | --- | --- | --- |
| Random valid patch 0/12 | worldsmith `bundles/experiments/m2_hard_f1{a,b,c,d}/results.json` | condition `B2`, `episodes[].repaired` all false; every B2 proposal REJECTED | 4 rooms × 3 episodes |
| Haiku 6/12; both bridge rooms (F1-A, F1-B) 3/3, lever rooms (F1-C, F1-D) 0/3 | same | condition `B3-haiku`, `repaired` | 12 episodes |
| Sonnet 12/12 | same | condition `B3-sonnet`, `repaired` | 12 |
| Opus 12/12; first call in 11 of 12 | same | condition `B3-opus`, `model_calls` = [1,1,1], [1,1,1], [1,1,1], [1,1,3] | 12 |
| "Six times … too close" | `m2_hard_f1{c,d}/B3-haiku/ep*/proposals.json` | `codes` contains DETOUR_TOO_SHORT in 6 of Haiku's 18 lever-room proposals | 18 proposals |
| "four times it also moved the gate" | same | 4 proposals with an op on `gate_1`, each with code GATE_BYPASSED (all in F1-C) | 18 |
| "Sonnet and Opus never touched the gate" | `m2_hard_f1*/B3-{sonnet,opus}/ep*/proposals.json` | 0 of 19 Sonnet and 0 of 14 Opus proposals have an op on `gate_1` | 33 |
| $0.98, 59 calls (card) | worldsmith `README.md` (from `results/usage.csv`); sum of `cost_usd_reported` over all episodes = 0.983524 | Haiku 26 + Sonnet 19 + Opus 14 = 59 `model_calls` | 59 calls |
| "bridge off to the side of the path" | worldsmith `scenes/F1-B/scene.json` | `bridge_1.lateral_offset` = 10 | — |
| Architect can change bridge, lever, gate, walls | worldsmith README "Harder rooms" (M1 stage, ADR 0007) | — | — |
| "Last week … So did a random patch" | `bundles/experiments/m2_f1a_b3/results.json`; `bundles/experiments/m2_f1a_pilot/B2/ep0/summary.json` | earlier easy stage (M0 ops, player p0.v2 for the random pilot) | 1 episode each |
| Fixed seeds chosen before the run | worldsmith `config/experiments/m2_hard.yaml` (commit before the paid run) | B2 seeds 0–2 | — |

## Checks

- Numbers re-read from the results/proposals files on 12 Nov, not copied from HANDOFF.
- The comparison to last week mixes stages on purpose and says so: the F1-A room is the same, but
  the architect's allowed changes widened (M0 → M1), which is why a random patch now misses it
  (offline: accepted and walk-connected 16/200 at M0 vs 1/200 at M1, worldsmith `docs/TICKETS.md`
  WS-14; not a play result, so not in the post).
- Required labels in the post: scripted walker, not an AI agent; counts not rates; not a benchmark.
- "Cheat" is used only for what the validator rejects. GATE_BYPASSED is a validator code, not a
  claim about the model's intent; the post says "moved the gate out of the way".
- Relay disclosure in the first comment (RELAY_NOTE.md in f1b, f1c, f1d).
- Owned assets only; no company named or tagged; no World Labs material.
- Not posted. No paid calls made for this draft.

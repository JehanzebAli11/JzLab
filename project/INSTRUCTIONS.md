JzLab: Jehanzeb Ali's AI lab. The goal for November 2026 is to finish the Lost in Transliteration
study and submit the Anthropic Research Residency application on Thu 19 Nov (it closes 22 Nov),
then train and evaluate Spark-1, the agent firewall and Scam Radar on his NVIDIA DGX Spark, and
turn real results into LinkedIn posts (Tuesdays and Thursdays).

The plan is the doc "JzLab Master Plan" (https://claude.ai/artifact/GbA5WRgV3QSNm6orwoh69W);
its working copy is in the JzLab repo: docs/PLAN.md (workstreams W0-W8, dates, state), docs/POSTS.md
(posts and their gates), docs/REPOS.md (repo status). Start prompts: agents/<name>/prompt.md for
Spark workstreams, prompts/threads/<task>.md for single cloud tasks. Read the matching prompt
before starting a thread, and name it in the thread's first message.

WHERE WORK RUNS
- Cloud threads: code, tests, docs, CPU experiments, reviews, post drafts. They cannot reach the
  Spark, its GPU, the Gemma teacher or anything on Tailscale.
- Threads on the DGX Spark ("Work locally", folder "<repo> @ <spark hostname>"): anything that
  needs the GPU, the Gemma 4 31B teacher at http://localhost:8000/v1, the spark-lab queue, or real
  results. Always use a worktree. Long jobs go through the spark-lab queue
  (cd ~/lab/spark-lab && python3 -m lab enqueue <job.json>), not a foreground command.
- Threads on the MacBook: only autopilot (Roblox Studio is there).

REPOSITORIES (github.com/JehanzebAli11)
- lost-in-transliteration: the Urdu safety study. Push to main. Brief: RUNBOOK.md, LOG.md.
- spark-lab: job queue, nightly report, systemd units. PRs: #1 bootstrap, #2 self-healing, #3 guard.
- spark-one: Spark-1, a System One model on Gemma 4 E2B. Push to main. Brief: HANDOFF.md.
- agent-firewall: agent action firewall. Push to main. Brief: HANDOFF.md.
- scam-radar: on-device scam checker (Gemma 3 270M + Android app). PR #1 android-app.
- autopilot: Aura Autopilot Roblox engine, branch roblox-engine. Brief: docs/runbook.md.
- jz-brain (private): research vault with cited pages; use it for related work, the application
  and posts. Brief: prompts/threads/brain-setup.md.
- JzLab: this plan. Keep docs/PLAN.md and state/STATUS.md current when phases move.
Each repo's HANDOFF/RUNBOOK is the brief for its work; update it after every milestone (what ran,
timings, result file paths), commit and push.

THE SPARK IS SHARED
- At most 3 Spark threads at once. lost-in-transliteration has priority until 16 Nov.
- The teacher holds about 89 GB of 128 GB and serves every thread. Never stop, restart or
  reconfigure it, and never start a second vLLM. If a step needs it stopped (spark-one LoRA
  training, self-healing GPU chaos tests), stop and ask Jehanzeb; he decides when.
- Never touch another thread's worktree or another repo's checkout.
- Check disk (df -h ~/lab) before big jobs; prune your own checkpoints only.

GROUND RULES (no exceptions)
1. Training data comes only from open-weight models served on the Spark, from code with exact
   ground truth, or from consented real data. Claude, OpenAI, Gemini and Jev outputs may be
   evaluated, never trained on. (Lost in Transliteration's data stages also ran on open-weight
   models via OpenRouter under the owner-approved cloud_openrouter profile.)
2. eval/locked/ is human-only: never read, list, edit or prompt with it.
3. Never invent numbers. Every number in a README, HANDOFF, report or post draft comes from a file
   the code wrote; cite the file. Say plainly what is synthetic, simulated or CPU-only.
4. Hugging Face uploads stay private and only after Jehanzeb says yes. Never run publish/.
5. No personal data leaves the Spark. Fake secrets and throwaway keys, local sandboxes only.
6. Nothing from NFL Football Universe or with NFL branding; no agents on live games.
7. Security work is defensive and on his own devices, networks and agents only.
8. Git identity: Jehanzeb Ali <jehanzeb1111@icloud.com>.

ASK JEHANZEB FIRST
- sudo, systemctl, docker or any service change; stopping or starting the teacher
- merging pull requests, force-pushes, history rewrites
- deleting anything outside a repo's runs/
- API spend beyond a repo's own cap (Lost in Transliteration: $40 total)
- any upload, and anything public (LinkedIn posts are drafted into JzLab/posts/, never posted)

DONE MEANS
Tests pass (paste the summary line), result files are committed (reports and figures, not
checkpoints or weights), the repo's HANDOFF says what changed, and the final message lists every
number with the file it came from.

HOW TO RUN THIS PROJECT
- Propose threads before starting them; run a few at a time.
- Each morning: read the latest spark-lab nightly report (reports/<date>.md) via a Spark thread
  and tell Jehanzeb what failed.
- Fridays: list open PRs with a merge/wait/close recommendation each, check progress against
  docs/PLAN.md, and say which posts in docs/POSTS.md have their gates met.
- Talk to Jehanzeb in short, plain lines: what moved, what needs him (as yes/no questions), what's next.

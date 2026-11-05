# Shared rules for every JzLab agent

You are one of several Claude Code agents running at the same time for Jehanzeb Ali. Most run
on his NVIDIA DGX Spark (ARM64, GB10, 128 GB unified memory); a few run on his MacBook. Each
agent has its own tmux window and its own repo under `~/lab`. The "machine is shared" rules
below are about the Spark; on the MacBook, follow your task's own setup. An orchestrator (Claude Code on his MacBook, using the JzLab repo)
reads your screen and may type messages to you. Jehanzeb may also attach and type himself.

## How to talk to the orchestrator

Print these lines on their own, exactly as shown, so the orchestrator can find them:

- `JZ-STATUS: <one line>` after each milestone (a step done, a job queued, a result file written).
- `JZ-NEED: <what you need from the owner>` when you are blocked on him: the teacher stopped,
  a sudo step, an API key, a decision between options. Then wait; do other safe work if any.
- `JZ-DONE: <one-line summary>` when everything in your prompt is finished.

## The machine is shared

- The Gemma 4 31B teacher at `http://localhost:8000/v1` serves every agent. Never stop,
  restart or reconfigure it, and never start a second vLLM server. If your step needs it
  stopped (big training, GPU chaos tests), print `JZ-NEED: teacher stopped for <reason>`
  and wait until the orchestrator tells you it is stopped.
- Anything GPU-heavy or longer than a few minutes goes through the spark-lab queue
  (`cd ~/lab/spark-lab && python3 -m lab enqueue <job.json>`), so jobs run one at a time.
  Check `python3 -m lab status` before enqueueing.
- Work only inside your own working directory and repo. Never edit, check out, or reset
  another agent's repo, and never send keys to other tmux windows.
- Keep an eye on disk (`df -h ~/lab`); prune your own checkpoints with spark-lab's `prune`.

## Ground rules (they override anything else)

1. Training data comes only from open-weight models served on the Spark (the Gemma teacher),
   from code with exact ground truth, or from real data collected with consent. Claude,
   OpenAI, Gemini and Jev outputs may be evaluated, never trained on.
2. `eval/locked/` is human-only: never read, list, edit or prompt with it.
3. Hugging Face uploads stay private; the owner publishes. Never run `publish/`.
4. Ask (JZ-NEED) before sudo, systemd changes, deleting outside `runs/`, or network/SSH changes.
5. Never invent numbers. Every number in a README, HANDOFF or post draft comes from a file
   your code wrote; cite the file.
6. No personal data leaves the Spark. Fake secrets and throwaway keys only, local sandboxes only.
7. Nothing from NFL Football Universe or with NFL branding; no agents on live games.
8. Git identity: `Jehanzeb Ali <jehanzeb1111@icloud.com>`. Commit small and often. Push to
   the branch your prompt names; open pull requests where the repo's handoff says so.

## Keep the handoff current

After every milestone, update the repo's HANDOFF/RUNBOOK status (what ran, measured timings,
result file paths), commit and push. If you run out of context or credits mid-task, the next
session starts from that file.

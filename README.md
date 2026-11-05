# JzLab

The control room for my AI projects. Claude Code on my MacBook opens this repo and steers
several Claude Code agents at once. Each agent works on one project, in its own tmux window:
most run on my NVIDIA DGX Spark, reached over SSH and Tailscale, and one runs on the Mac.

```
MacBook                                        DGX Spark (~/lab)
┌──────────────────────────────┐   ssh    ┌──────────────────────────────────────────────┐
│ Claude Code (orchestrator)   │ ───────► │ tmux session "jzlab"                         │
│   reads CLAUDE.md            │  bin/jz  │  ├─ setup     claude  spark-lab              │
│   bin/jz brief / say / start │          │  ├─ lit       claude  lost-in-transliteration│
│                              │          │  ├─ scam      claude  scam-radar             │
│ tmux "jzlab-mac"             │          │  ├─ heal      claude  spark-lab (worktree)   │
│  └─ autopilot  claude  Studio│          │  ├─ firewall  claude  agent-firewall         │
└──────────────────────────────┘          │  └─ spark1    claude  spark-one              │
                                          │ Gemma 4 31B teacher :8000 · spark-lab queue  │
                                          └──────────────────────────────────────────────┘
```

Each agent starts from `templates/agent-preamble.md` (shared rules) plus its own
`agents/<name>/prompt.md`, which points it at that repo's HANDOFF file. Agents report with
`JZ-STATUS:`, `JZ-NEED:` and `JZ-DONE:` lines, which `bin/jz ls` picks up. The orchestrator
answers what the plan already covers and asks me about everything else.

## Use it

```bash
cd ~/lab/JzLab
bin/jz brief                 # what's happening everywhere
bin/jz start lit             # start an agent
bin/jz peek lit 80           # read its screen
bin/jz say lit "skip the MCP phase for now"
bin/jz attach lit            # watch it live in this terminal (Ctrl-b d to leave)
claude                       # the orchestrator; paste prompts/orchestrator-start.md once
```

First time: [docs/SETUP.md](docs/SETUP.md).

## What's here

| Path | What |
| --- | --- |
| `CLAUDE.md` | Rules and check-in routine for the orchestrator |
| `bin/jz` | Mac-side CLI (SSH to the Spark, or local for Mac agents) |
| `spark/jzd` | Host-side CLI: tmux windows, logs, teacher control, sync |
| `agents/<name>/` | `agent.env` (repo, branch, phase, window, teacher use) and `prompt.md` |
| `templates/` | Shared agent rules; the agents' Claude Code permission rules |
| `prompts/` | Tasks for the orchestrator: start, check-in, weekly review, LinkedIn drafts, Residency application, new agent |
| `docs/` | Run order and dates, post plan, repo status, setup |
| `state/` | Status board and decision log, kept by the orchestrator |
| `posts/` | LinkedIn drafts (I post them myself) |

## Safety

- Agents run in `acceptEdits` mode, with the allow/ask/deny rules in
  `templates/claude-settings.json`: `sudo` is denied, `eval/locked/` and `.env` can't be read,
  and systemd, docker, `rm -rf`, force-pushes and uploads always ask.
- Only I stop the Gemma teacher (`jz teacher stop` asks to confirm), merge pull requests,
  publish anything, or post anything.
- Training data comes only from open-weight models on the Spark, code with exact labels, or
  consented data. Claude, OpenAI and Gemini outputs are evaluated, never trained on.

`tests/test_jz.sh` runs the whole CLI locally against a fake `claude` in tmux.

# Run JzLab as a Claude Project

A Claude Project (beta, claude.ai/code → Projects) is one conversation that runs a thread per
task. Cloud threads do code work; through Remote Control, threads can also run **on the DGX
Spark itself**, with the GPU, the teacher and the queue, and you steer every thread live from
claude.ai or the phone. No SSH needed once it's set up.

```
claude.ai/code → Project "JzLab"  (coordinator + threads, phone or browser)
   ├─ cloud threads ── GitHub repos (code, tests, docs, PRs)
   ├─ "Work locally" ─► DGX Spark: claude remote-control in ~/lab/<repo>  (jz rc up)
   └─ "Work locally" ─► MacBook: desktop app, folder ~/lab/autopilot (Roblox Studio)
```

## 1. On the Spark: start one Remote Control server per repo

Needs Claude Code v2.1.280 or later on the Spark, signed in with your Claude account (not an API
key). From the Mac:

```bash
cd ~/lab/JzLab
bin/jz sync          # repos cloned into ~/lab on the Spark
bin/jz rc up         # tmux session "jzrc": one `claude remote-control --spawn worktree` per repo
bin/jz attach-rc     # first time only: answer "Enable Remote Control? (y/n)" and "Trust <folder>?"
                     # in each window (Ctrl-b n for the next window, Ctrl-b d to leave)
bin/jz rc status     # each repo should say "serving"
```

Each server shows up as `<repo> @ <spark hostname>`. `--spawn worktree` gives every thread its
own git worktree, so threads in the same repo don't overwrite each other. The servers restart by
themselves after a crash; `bin/jz rc down` stops them. They survive your SSH session ending, but
not a Spark reboot: run `bin/jz rc up` again after one.

Agents' permission rules (`templates/claude-settings.json`: sudo denied, `eval/locked/` and
`.env` unreadable, systemd/docker/uploads ask) are installed in each repo and apply to local
threads too.

## 2. On the MacBook: share the autopilot folder

Claude desktop app → **Settings → Claude Code** → turn on **Use this computer from your phone and
claude.ai**, add `~/lab/autopilot` (your autopilot clone), and turn on **Keep this computer awake
for Remote Control** while Studio runs are going.

## 3. Create the project

1. Install the [Claude GitHub App](https://github.com/apps/claude) on these repos (once):
   JzLab, lost-in-transliteration, spark-lab, spark-one, agent-firewall, scam-radar, autopilot.
2. claude.ai/code → **Projects** (or **More → Projects**) → **New project**.
   Name: `JzLab`. Goal: "Finish Lost in Transliteration by 19 Nov, then Spark-1, agent firewall
   and Scam Radar on the DGX Spark, with LinkedIn posts from real results."
   Context: add JzLab and lost-in-transliteration first; add the others in
   **Project settings → Environment** as their phases start (docs/PLAN.md).
3. **Project settings → Memory → Project instructions**: paste `project/INSTRUCTIONS.md`.
4. Make sure **Require trusted devices** is off in your account settings; with it on, a project
   can't run threads on your computers.

## 4. Use it

- In the project conversation, ask for work. For anything that needs the GPU or the teacher,
  choose **Work locally** in the **+** menu (or say "run this on the Spark"), then pick the folder
  `<repo> @ <spark>` on the **Allow Claude to work in a folder on your device** card and keep
  **Worktree** on.
- First messages that map to the plan:
  - "Start a Spark thread in lost-in-transliteration following JzLab/agents/lit/prompt.md."
  - "Start a Spark thread in spark-lab following JzLab/agents/setup/prompt.md."
  - "Start a cloud thread to review spark-lab PR #3 and say what to merge."
- **Overview** shows every thread and which are waiting on you. Approvals happen inside each
  thread. Threads on the Spark pause if Remote Control drops and pick up when it's back.

## Where `bin/jz` still fits

- `jz brief`, `jz report`, `jz teacher status`: a quick look at the machine from a terminal.
- `jz teacher stop|start`: only you change the teacher; a thread that needs it stopped asks.
- `jz start <agent>`: the tmux agents still work if you'd rather run something outside the project.

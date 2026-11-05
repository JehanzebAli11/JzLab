# One-time setup

About 30 minutes. Do it in this order: Mac, then Spark, then the first check.

## 1. MacBook

```bash
# SSH alias for the Spark, so `ssh spark` works with no password prompt
cat >> ~/.ssh/config <<'EOF'
Host spark
  HostName <the Spark's Tailscale name, e.g. spark-xxxx>
  User <your Spark username>
  ServerAliveInterval 30
EOF
ssh-copy-id spark                 # once, if key login isn't set up yet
ssh -o BatchMode=yes spark true && echo "ssh ok"   # must print "ssh ok" with no prompt

# JzLab itself
mkdir -p ~/lab && cd ~/lab
git clone https://github.com/JehanzebAli11/JzLab && cd JzLab
cp .env.example .env              # edit SPARK_HOST if your alias isn't "spark"
brew install tmux gh              # gh: for `jz prs`; tmux: for the Mac agents
gh auth status || gh auth login
bin/jz help
```

For a short `jz` command, add this line to `~/.zshrc`:
`alias jz=~/lab/JzLab/bin/jz`

## 2. DGX Spark (over SSH from the Mac)

```bash
ssh spark
sudo apt-get install -y tmux git curl          # usually present already
curl -fsSL https://claude.ai/install.sh | bash  # Claude Code (Linux ARM64 is supported)
claude                                           # sign in once with your Claude account, then /exit
gh auth login && gh auth setup-git               # so agents can push and open PRs
git config --global user.name  "Jehanzeb Ali"
git config --global user.email "jehanzeb1111@icloud.com"
mkdir -p ~/lab && cd ~/lab && git clone https://github.com/JehanzebAli11/JzLab
exit
```

When `claude` asks you to sign in, it shows a link. Open the link on the Mac.

## 3. First check, from the Mac

```bash
cd ~/lab/JzLab
bin/jz sync      # clones every project repo into ~/lab on the Spark
bin/jz doctor    # every line should say "ok"; the teacher is "down" until bootstrap runs
```

## 4. Bootstrap spark-lab (you, once)

spark-lab's bootstrap asks for your ntfy topic and Hugging Face token, and prints the sudo
steps for you to run. Run it yourself in the Spark's tmux, with the `setup` agent beside it to
check the result:

```bash
bin/jz start setup        # the agent reads PR #1 and tells you what to run
bin/jz attach             # Ctrl-b n / p to switch windows; Ctrl-b d to detach
# in the "home" window:
cd ~/lab/spark-lab && git checkout bootstrap && bash scripts/bootstrap.sh
```

## 5. Hand over to the orchestrator

```bash
cd ~/lab/JzLab && claude
```

Then paste `prompts/orchestrator-start.md`.

## Secrets

Each repo's `.env` lives only on the Spark (`chmod 600`). Agents are denied reading it; their
code loads it. Keys used today: `ANTHROPIC_API_KEY` and `OPENROUTER_API_KEY` (evaluation only),
`HF_TOKEN` (read-only), and optionally `TYPESAFE_API_KEY` (Jev evaluation).

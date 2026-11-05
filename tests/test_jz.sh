#!/usr/bin/env bash
# End-to-end test of bin/jz + spark/jzd on this machine: a fake `claude` in real tmux,
# fake repos, no SSH (JZ_LOCAL=1). Run: bash tests/test_jz.sh
set -u
ROOT=$(cd "$(dirname "$0")/.." && pwd)
T=$(mktemp -d)
trap 'tmux -L jztest kill-server 2>/dev/null; rm -rf "$T"' EXIT

export JZ_LOCAL=1 LAB_DIR="$T/lab" MAC_LAB_DIR="$T/maclab" JZ_STATE="$T/lab/.jzlab"
export TEACHER_URL="http://127.0.0.1:9/v1" TEACHER_UNIT=none
export JZ_SESSION=jztest
export CLAUDE_BIN="$T/bin/claude"
# a private tmux server, so the test never touches real sessions
mkdir -p "$T/bin"
cat > "$T/bin/tmux" <<EOF
#!/usr/bin/env bash
exec $(command -v tmux) -L jztest "\$@"
EOF
chmod +x "$T/bin/tmux"
export PATH="$T/bin:$PATH"

cat > "$CLAUDE_BIN" <<'EOF'
#!/usr/bin/env bash
case "$*" in --version) echo "9.9.9 (fake)"; exit 0 ;; *--continue*) echo "JZ-STATUS: resumed" ;; esac
printf 'fake-claude mode=%s\n' "$2"
echo "JZ-STATUS: started fine"
while IFS= read -r line; do
  echo "got: $line"
  case "$line" in
    need) echo "JZ-NEED: teacher stopped for a test" ;;
    approve) echo "Do you want to proceed?" ;;
    quit) exit 0 ;;
  esac
done
EOF
chmod +x "$CLAUDE_BIN"

for d in spark-lab lost-in-transliteration scam-radar agent-firewall spark-one; do
  mkdir -p "$LAB_DIR/$d"
  git -C "$LAB_DIR/$d" init -q -b main
  git -C "$LAB_DIR/$d" -c user.name=t -c user.email=t@t commit -q --allow-empty -m init
done
git -C "$LAB_DIR/spark-lab" branch self-healing
mkdir -p "$MAC_LAB_DIR/autopilot"
git -C "$MAC_LAB_DIR/autopilot" init -q -b roblox-engine
git -C "$MAC_LAB_DIR/autopilot" -c user.name=t -c user.email=t@t commit -q --allow-empty -m init
mkdir -p "$LAB_DIR/spark-lab/reports" && echo "# report 2026-11-05" > "$LAB_DIR/spark-lab/reports/2026-11-05.md"

JZ="$ROOT/bin/jz"
fails=0
check() {  # check <description> <command...>: passes if the command succeeds
  local what="$1"
  shift
  if "$@" >/dev/null 2>&1; then echo "PASS $what"; else echo "FAIL $what"; fails=$((fails + 1)); fi
}
has() { grep -q -- "$2" <<<"$1"; }
wait_for() {  # wait_for <agent> <text>
  local _
  for _ in $(seq 1 30); do
    "$JZ" peek "$1" 200 2>/dev/null | grep -q -- "$2" && return 0
    sleep 0.2
  done
  return 1
}

out=$("$JZ" agents); check "agents lists all 7" test "$(echo "$out" | tail -n +2 | wc -l)" -eq 7
check "agents shows heal on its worktree branch" has "$out" "spark-lab@self-healing"

check "start lit" "$JZ" start lit
check "lit shows the fake claude" wait_for lit "JZ-STATUS: started fine"
check "lit runs in acceptEdits mode" wait_for lit "mode=acceptEdits"
pf="$JZ_STATE/run/lit.prompt.md"
check "prompt has the shared preamble" grep -q "Shared rules for every JzLab agent" "$pf"
check "prompt has the lit task" grep -q "finish Lost in Transliteration" "$pf"
check "settings installed in the repo" test -f "$LAB_DIR/lost-in-transliteration/.claude/settings.local.json"
check "second start is refused" bash -c "! '$JZ' start lit"

check "say reaches the agent" "$JZ" say lit "hello there"
check "agent got the message" wait_for lit "got: hello there"
out=$("$JZ" ls); check "ls shows lit running with its marker" has "$out" "lit .*running .*JZ-STATUS: started fine"

"$JZ" say lit need >/dev/null; wait_for lit "JZ-NEED" >/dev/null
out=$("$JZ" ls); check "ls flags NEEDS-YOU" has "$out" "lit .*NEEDS-YOU"
"$JZ" say lit approve >/dev/null; wait_for lit "Do you want to proceed" >/dev/null
out=$("$JZ" ls); check "ls flags APPROVAL" has "$out" "lit .*APPROVAL"

check "start heal (worktree)" "$JZ" start heal
check "heal worktree exists on self-healing" test "$(git -C "$LAB_DIR/wt/heal" rev-parse --abbrev-ref HEAD)" = self-healing
check "heal runs in its worktree" wait_for heal "JZ-STATUS: started fine"

tmpp="$T/custom.md"; echo "Custom task: say hi" > "$tmpp"
check "start firewall with a custom prompt" "$JZ" start firewall --prompt "$tmpp"
check "custom prompt used" grep -q "Custom task: say hi" "$JZ_STATE/run/firewall.prompt.md"

check "start autopilot on the Mac side" "$JZ" start autopilot
check "autopilot runs" wait_for autopilot "JZ-STATUS: started fine"
check "a mac agent can't start on the spark" bash -c "! JZ_WHERE=spark bash '$ROOT/spark/jzd' start autopilot"

out=$("$JZ" brief 5); check "brief shows lit's screen" has "$out" "== lit (last 5 lines)"
check "brief shows the teacher down" has "$out" "teacher: down"

check "key sends raw keys" "$JZ" key lit Escape
check "stop lit" "$JZ" stop lit
out=$("$JZ" ls); check "lit is gone after stop" has "$out" "lit .*none"
check "start lit --continue" "$JZ" start lit --continue
check "continue resumes" wait_for lit "JZ-STATUS: resumed"

"$JZ" say lit quit >/dev/null; wait_for lit "agent exited with code 0" >/dev/null
out=$("$JZ" ls); check "exited agent shows exited" has "$out" "lit .*exited"
check "an exited agent can be restarted" "$JZ" start lit

out=$("$JZ" report); check "report prints the latest" has "$out" "report 2026-11-05"
out=$("$JZ" events 50); check "events log the says" has "$out" "say lit: hello there"
out=$("$JZ" doctor 2>&1); check "doctor sees the repos" has "$out" "ok   repo lost-in-transliteration"
check "teacher stop needs the owner when not a tty" bash -c "! '$JZ' teacher stop testing </dev/null"
check "unknown agent fails" bash -c "! '$JZ' start nosuch"

# The real path: bin/jz -> ssh -> jzd, with the remote shell's own clean environment.
# A fake ssh drops its options and host and runs the command the way sshd would.
cat > "$T/bin/ssh" <<FAKESSH
#!/usr/bin/env bash
while [ \$# -gt 1 ]; do shift; done
exec env -i HOME="$T/home" PATH="$T/bin:/usr/bin:/bin" bash -c "\$1"
FAKESSH
chmod +x "$T/bin/ssh"   # the fake claude is already $T/bin/claude
mkdir -p "$T/home" && ln -s "$LAB_DIR" "$T/home/lab" && ln -s "$ROOT" "$LAB_DIR/JzLab"
"$JZ" stop lit >/dev/null 2>&1
(
  unset LAB_DIR JZ_STATE JZ_SESSION CLAUDE_BIN TEACHER_URL TEACHER_UNIT
  export JZ_LOCAL=0 SPARK_HOST=fake
  check "over ssh: start lit" "$JZ" start lit
  check "over ssh: lit runs" wait_for lit "JZ-STATUS: started fine"
  # shellcheck disable=SC2016  # the dollar sign must arrive unexpanded
  msg='it'"'"'s $HOME & "quoted" ; ls'
  check "over ssh: say with quotes and dollars" "$JZ" say lit "$msg"
  check "over ssh: message arrives literally" wait_for lit "got: $msg"
  out=$("$JZ" ls); check "over ssh: ls" has "$out" "lit .*running"
  check "over ssh: custom prompt is uploaded" "$JZ" start scam --prompt "$tmpp"
  check "over ssh: uploaded prompt used" grep -q "Custom task: say hi" "$T/home/lab/.jzlab/run/scam.prompt.md"
  exit "$fails"
) || fails=$((fails + $?))

echo
if [ "$fails" -eq 0 ]; then echo "all passed"; else echo "$fails failed"; exit 1; fi

Read CLAUDE.md, docs/PLAN.md, docs/REPOS.md and state/STATUS.md. You are the JzLab orchestrator.

1. Run `bin/jz doctor` and `bin/jz sync`. If anything is missing, tell me exactly what to fix
   and stop there.
2. Run `bin/jz brief`. Work out which phases in docs/PLAN.md can start today, given what is
   already running and done.
3. Start those agents (at most 3 on the Spark), plus `autopilot` on this Mac if Studio is open.
   After each start, wait about a minute, `peek` it, and check it understood its task.
4. Write state/STATUS.md and commit.
5. Tell me in a few lines: what is running, what needs me, and when you'll check again.

After that, on each check-in, follow "A check-in" in CLAUDE.md. If I say "check the lab",
do one check-in.

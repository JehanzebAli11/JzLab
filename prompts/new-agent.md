Add a new agent to JzLab for: <describe the task and the repo>.

1. Create agents/<name>/agent.env (copy the fields of an existing one: NAME, TITLE, WHERE,
   REPO, DIR, BRANCH, WORKTREE, TEACHER, PHASE, WINDOW, HANDOFF) and agents/<name>/prompt.md.
   Use WORKTREE=1 if another agent already works in the same repo.
2. The prompt names the repo's own handoff file as the brief, the order of work, what needs
   the teacher stopped, and what counts as done. Keep it under 40 lines.
3. Add a row to docs/PLAN.md, commit, push, `bin/jz sync`, and ask me before starting it.

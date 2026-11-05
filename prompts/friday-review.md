Weekly review (Friday).

1. `bin/jz say <agent> "Update your HANDOFF/RUNBOOK status now (what ran, timings, result
   files), commit and push, then print JZ-STATUS."` to every running agent.
2. `bin/jz prs`: list the open PRs with a one-line recommendation each (merge, wait, close),
   using their CI status and the agents' notes. Don't merge anything.
3. Compare progress with docs/PLAN.md. Propose date changes if a phase slipped, and say which
   posts in docs/POSTS.md have their gates met for next week.
4. Look at disk and the nightly reports of the week (`bin/jz report <date>`). Flag anything
   that failed more than once.
5. Update docs/PLAN.md's State table and state/STATUS.md, commit, push, and give me a summary
   I can read in one minute.

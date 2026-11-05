# Task: check the agent firewall LinkedIn post before it goes out on Tue 10 Nov (W4)

Repo: agent-firewall. Read `docs/linkedin_post.md` and the result files it cites.

1. For every number in the post, find it in `results/metrics.json`, `results/wallet_metrics.json`
   or `results/external_eval.json`, and confirm its value, its split and its denominator. Fix any
   mismatch in the post, not in the results.
2. Check the post says plainly: scripted agents and synthetic attacks; the 41% false blocks on
   unseen tasks; no transfer to BIPIA yet.
3. Tighten it: a hook line, 3-5 short lines, one visual, at most 3 hashtags, and the repo link
   in the first comment. Keep it in the owner's voice, first person, no hype.
4. Check the visual (`results/figures/linkedin_card.png`) shows only numbers from the files.
5. Save the final post as JzLab `posts/2026-11-10-agent-firewall.md` with a "Sources" list of
   number and file. Commit both repos. Don't post.

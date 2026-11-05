# Task: split spark-lab PR #3 so each piece lives in one repo (W6)

Repo: spark-lab, PR #3 (branch `claude/dgx-spark-bootstrap-73xdyl`). agent-firewall already has
an action-firewall harness and a wallet decoder, so PR #3's `guard.firewall` and `guard.wallet`
duplicate them.

1. Compare PR #3's `guard/firewall`, `guard/wallet` and `guard/media/{firewall,wallet}.py` with
   agent-firewall's `afw/` harness and `afw/wallet/`. List what PR #3 has that agent-firewall
   lacks (e.g. Permit2, Seaport, SIWE decoding).
2. Keep in PR #3: `guard.screen_injection`, `guard/media` (minus the duplicate parts),
   `extension/` and `guard.extension_stub`, and `docs/linkedin-posts.md`.
3. Move the missing wallet and firewall features into a new agent-firewall branch and open a PR
   there (tests included), then remove them from PR #3. Rebase PR #3 on main once spark-lab #1 is
   merged. All tests and CI must pass.
4. Comment on both PRs with what moved where. Don't merge; the owner does.

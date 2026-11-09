# Agent firewall: LinkedIn post (Tue 10 Nov 2026)

Status: checked draft, not posted. Jehanzeb posts it. Source repo: agent-firewall (`docs/linkedin_post.md` holds the same text).

## Post

One hidden line in an email can make an AI agent pay, forward or sign something its user never asked for.

I built an action firewall for that: before an agent sends, pays or signs, a calibrated judge asks "does this action follow from the user's request?", and plain code allows, asks or blocks.

On scripted agents and synthetic attacks (6 languages including Roman Urdu, 10 styles, 7 hiding tricks), injection success fell from 22.4% to 0.0% (2 of 16,666 attacked episodes), with 0.9% of legitimate actions blocked. The test attacks come from the same generator it trained on.

On a local test chain, wallet drains fell from 97.9% to 0% across 1,102 malicious requests, measured by actually running the drainer.

The weak part: on 7 tasks it never saw, it blocks 41% of legitimate actions. And it doesn't transfer to real injected emails yet: it flags 0 of 300 injected BIPIA emails (AUROC 0.40, n = 350: 300 injected, 50 clean).

Next, part 2: real Claude agents (Haiku and Sonnet) in the same harness, with a local Gemma agent as a second arm, and work on that unseen-task gap.

Code and every result file in the first comment.

#AIAgents #AISafety #PromptInjection

## First comment

Code, data generator and every result file: github.com/JehanzebAli11/agent-firewall

The numbers are from results/metrics.json, results/wallet_metrics.json and results/external_eval.json (test split, TF-IDF + logistic-regression judge; "ask" decisions are resolved by a simulated user who denies injected actions). The 41% is 2,230 of 5,484 legitimate actions on the 7 held-out tasks. The other two judges I tried did worse there.

## Visual (file path)

`agent-firewall/results/figures/linkedin_card.png` (1200x627 card, rendered at 2400x1254).

**Fix before posting:** the card's footer says "8 hiding tricks"; the generator has 7 (`TRICKS` in `afw/sandbox/injection.py` lists 8 entries, one of them `none`, and `metrics.json` breakdown `trick` has 7 tricks plus `none`). "8" is a hard-coded literal in `scripts/make_summary_card.py`, not read from a result file. Change it to 7 and re-run `python scripts/make_summary_card.py`, or attach `results/figures/demo_blocked_exfiltration.gif` (1100x640, 8 frames, 277 KB) instead. Every other number on the card matches the files.

## Sources

| number in post / comment | file | key path (row) | n |
|---|---|---|---|
| 6 languages | results/metrics.json | `[0].breakdown.lang` (de, en, es, fr, ur_rom, zh; plus `none`) | — |
| 10 styles | results/metrics.json | `[0].breakdown.style` (10 styles plus `none`) | — |
| 7 hiding tricks | results/metrics.json | `[0].breakdown.trick` (alt_text, base64, css_hidden, html_comment, tiny_font, white_text, zero_width; plus `none`) | — |
| 22.4% (attack success, no firewall) | results/metrics.json | `[0]` random / tfidf_lr / full → `episodes.asr_no_firewall` = 0.2238 | 16,666 injected test episodes (`episodes.injected_episodes`) |
| 0.0% and "2 of 16,666" (attack success, firewall) | results/metrics.json | `[0]` → `episodes.asr_firewall` = 0.00012 (= 2 / 16,666) | 16,666 |
| 0.9% legitimate actions blocked | results/metrics.json | `[0]` → `overall.false_block` = 0.00933 | 21,662 legitimate test actions (`overall.n_neg`) |
| 97.9% (wallet drain, no firewall) | results/wallet_metrics.json | `[0]` random / tfidf_lr / wallet → `episodes.drain_success_no_fw` = 0.9791 | 1,102 malicious test requests (`overall.n_pos`) |
| 0% (wallet drain, firewall) | results/wallet_metrics.json | `[0]` → `episodes.drain_success_fw` = 0.0 | 1,102 |
| 7 unseen tasks | results/metrics.json | `[24]` heldout_task / tfidf_lr / full → `breakdown.task_id` (T16–T20, T25, T26) | — |
| 41% false blocks on unseen tasks; "2,230 of 5,484" | results/metrics.json | `[24]` → `overall.false_block` = 0.4066 (RESULTS.md: 40.7%) | 5,484 legitimate test actions (`overall.n_neg`) |
| "other two judges did worse" | results/metrics.json | `[25]` mlp/full 0.964, `[26]` gbm/full 0.671 (`overall.false_block`) | 5,484 each |
| 0 of 300 injected BIPIA emails flagged | results/external_eval.json | `bipia_email.flag_rate_injected_block_or_ask` = 0.0, `bipia_email.n_injected` = 300 | 300 |
| AUROC 0.40 on BIPIA | results/external_eval.json | `bipia_email.auroc` = 0.3977 | 350 (300 injected, 50 clean: `n_injected`, `n_clean`) |

## Checks

- Every number in the post and first comment traced to the key above; values and rounding re-computed from the JSON with Python (not copied from RESULTS.md).
- All headline rows are the test split (seed % 10 in {8, 9}, per RESULTS.md); thresholds set on the validation split with the 1% false-block budget (`BUDGETS` in `afw/calibration.py`; a design setting, not a result, so the post doesn't quote it as one).
- "Measured by actually running the drainer": `afw/wallet/core.py` `attack_execute` executes the request on an anvil snapshot, runs the drainer contract and measures attacker holdings; `scripts/wallet_train_eval.py` turns that into `drain_success_*`.
- 0.0% attack success relies on "ask" being resolved by a simulated user who denies injected actions (`RESULTS.md` header; `wallet_train_eval.py` comment). Said in the first comment.
- The 22.4% / 0.9% row is the in-distribution (random split, full view) result. HANDOFF §4 risk 4 warns that scripted injections sit verbatim in the evidence, so the post says the test attacks come from the same generator, and the unseen-task and BIPIA results sit next to it.
- The required plain statements are in: scripted agents and synthetic attacks; 41% false blocks on unseen tasks (n = 5,484); no transfer to BIPIA (AUROC 0.40, n = 350).
- "Next" follows ROADMAP §5 (part 2 on Claude Haiku and Sonnet via the Claude API, Gemma as the local arm). No dates or target numbers.
- Visual: linkedin_card.png opened and read. The card shows 22.4% → 0.0%, 97.9% → 0.0%, 41%, 0.9%, 1% budget, 6 languages, 10 styles: all match. **Mismatch: "8 hiding tricks" should be 7** (see Visual). Not regenerated.
- GIFs exist: demo_blocked_exfiltration.gif (1100x640, 8 frames, 277,080 bytes); demo_wallet_drainer_blocked.gif (1100x640, 6 frames, 468,121 bytes). Their contents were not checked frame by frame.
- Format: hook line, 5 short paragraphs, closing line, 3 hashtags, repo link moved to the first comment. Not posted.

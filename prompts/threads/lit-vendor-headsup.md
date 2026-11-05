# Task: draft heads-up notes to vendors before the 17 Nov post (W1, step 4)

Repo: lost-in-transliteration. PLAN §0.5: a vendor hears about a large, reproducible weakness in
their tool before it is posted publicly.

1. From `results/classifiers_summary.csv` (and `results/mcp_summary.csv` for scanners), find each
   vendor tool with a large drop for Urdu, Roman Urdu or mixed text, or a large false-positive
   rate on benign Urdu. Today that includes Meta's Prompt Guard 2 (86M and 22M) and ProtectAI's
   deberta-v3 prompt-injection v2; check the others too.
2. For each, draft a short, polite note in `writeup/disclosure/<vendor>.md`: what was tested,
   the numbers with sample sizes and CIs, how to reproduce (repo link, commands), the planned
   public date (17 Nov), and an offer to share data. No exploit text beyond what's in the public
   repo.
3. Find the right contact for each (security page, GitHub issues or model card), and list it.
   The owner sends them on 13 Nov.

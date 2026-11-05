# Task: draft the Lost in Transliteration write-up from existing results (W1, step 2)

Repo: lost-in-transliteration, push to main. Read PLAN.md (§7-8), RUNBOOK.md, LOG.md and
`writeup/` first. The application is submitted on 19 Nov; the draft is due 13 Nov.

Results that exist now: the classifier eval (`results/classifiers*`), the model evals
(`results/models_*.csv`), the MCP scanners (`results/mcp_summary.csv`) and the data reports
(`translation_report.json`, `native_gate_report.json`). The detector results (RQ4) come later from
the Spark; leave a clearly marked placeholder for them.

1. Run the analysis that doesn't need detectors (`make analyze`, or the subset that works
   without `results/detector*`), so the tables and figures exist.
2. Fill `writeup/post.md` (2,000-3,000 words) and `writeup/application_blurb.md`:
   TL;DR, motivation, setup, results per RQ with confidence intervals, what surprised us,
   limitations, and what's next. Keep a comment with the source file next to every number.
3. Limitations must include: translations and the native set are model-written (open-weight),
   not human-written; Claude is sampled at the API default temperature; the sizes of the MCP
   and native sets; and anything LOG.md flags.
4. Related work: use the `research/` notes (and jz-brain if it exists), with links.
5. No hype words. Null results are fine. Never invent a number. Update LOG.md, commit and push.

Done when the draft reads end to end, the only gap is the RQ4 placeholder, and every number has
its source comment.

# Task: set up jz-brain, the research vault (W2)

Repo: JehanzebAli11/jz-brain (private; the owner creates it empty). Base it on the vault template
and skills of https://github.com/undefined-ui/second-brain-os (MIT: keep its licence notice and
credit it in the README).

1. Copy `vault-template/` to the repo root, and its `second-brain-ingest` and
   `second-brain-query` skills to `.claude/skills/`. Keep the vault's CLAUDE.md rules: `raw/` is
   never edited; claims are recorded as "this source says X"; nothing is ingested until it is linked;
   every answer cites wiki pages.
2. Put these in `raw/` and ingest them:
   - lost-in-transliteration `research/` notes (related work, classifier and scanner notes) and
     the papers they cite (abstracts and links; full PDFs only where the licence allows);
   - a one-page results summary per repo (lost-in-transliteration, spark-one, agent-firewall,
     scam-radar, spark-lab, autopilot), each number with its source file path;
   - the relevant items from second-brain-os's README "New this month" list: OpenAI Decisions
     API, Frozen Judges Moving Agents, The Unreliable Progress Bar, Harness², Elephant-Goldfish
     Model. Open each source before writing its page; a list entry is not a source.
3. Write `wiki/index.md`, then answer as a test, with page citations:
   "What is the evidence that Roman Urdu weakens prompt-injection classifiers?"
4. No personal data, no keys, nothing from `eval/locked/`. Commit and push to main.

Done when the test answer cites at least three pages and each claim traces to a source page.

# Task: an eval-only OpenAI Decisions API baseline for Spark-1 (W3)

Repo: spark-one, push to main. Read HANDOFF.md and `spark_one/adapters/` (the Jev and OpenRouter
adapters are the pattern). OpenAI's Decisions API (generally available 22 Oct 2026) returns typed
answers: Predicate (a probability a condition is true), Choice (one of given options) and Score
(against ordered levels), with text, image and JSON inputs; model `gpt-6-luna`. Look up the
current API reference and price before writing code, and record the date you checked.

1. Write `spark_one/adapters/decisions.py`: Noul maps to Predicate, Choice to Choice, Score to
   Score; Box is unsupported (record it as unsupported, never guessed). Read whatever confidence
   the API returns; where it returns none (Choice, Score), say so in the report instead of inventing
   a probability.
2. Add a cost cap ($3) and a response cache, like the other adapters. Test it with
   `httpx.MockTransport` (no real calls in tests).
3. Add a spark-lab job file `jobs/spark-one-12-eval-decisions.json` that runs it on the same 300
   test items and variants as the gpt-4o-mini run, so the reports line up.
4. The real run happens on the Spark, where `OPENAI_API_KEY` lives in `.env`. If this thread runs
   in the cloud, stop after the tests and print the exact command for the Spark thread.

This is evaluation only. Decisions API outputs are never training data (ground rule 1).

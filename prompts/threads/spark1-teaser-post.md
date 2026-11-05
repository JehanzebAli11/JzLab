# Task: draft the Spark-1 teaser post for Thu 12 Nov (W3)

Read from spark-one: `runs/eval-only/gpt-4o-mini/eval/report.md`, the zero-shot Gemma 4 E2B
report, and the Decisions API report if it exists. Use only numbers from these files.

The angle: typed "decision models" are a real product category now (OpenAI's Decisions API,
TypeSafe's Jev), and the question is whether they know when they're wrong. Lead with one
concrete, checkable failure: reordering the options changes gpt-4o-mini's answer in 31% of items
(option-order agreement 0.690, n = 300). Then name what Spark-1 is (a 5B Gemma 4 E2B fine-tuned on
the Spark to give calibrated typed answers, trained only on code labels and an open-weight
teacher) and what comes on 1 Dec.

Write JzLab `posts/2026-11-12-spark1-teaser.md`: the post, the first comment (repo link), the
visual (one question shown twice with options swapped and the two answers; render it as a PNG
from a real test item), and a Sources list. Say n for every number. Don't post.

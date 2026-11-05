# Task: a 3D question bank for Spark-1 v2 (W9, from 2 Dec)

Repo: spark-one, push to main. Start only after the Spark-1 v1 results (1 Dec): v1's bank and
its item ids stay frozen, and 3D items are appended as a new bank version.

Inputs (check each licence before use and record it in the dataset card):
- ABO furniture as GLB: https://huggingface.co/datasets/codepawl/abo-glb (7,953 models, sizes in
  metres, Y up, `metadata.jsonl` with measured sizes; CC BY 4.0: credit Amazon.com and cite the
  ABO paper; CodePawl is not affiliated with Amazon). Download only what you need (the
  thumbnails, metadata and a few hundred models to start).
- 67.js: https://github.com/codepawl/67.js (MIT), a WebGL2 renderer with headless PNG export
  on GPU or CPU, GLB import (meshopt and KTX2 decoders are passed in).

1. Generator `spark_one/generators/rooms3d.py` (+ a small Node renderer script): a room (floor,
   walls, light), 2-6 ABO objects placed by code on the floor (re-ground the 1,338 models that sit
   below Y = 0), a camera placed by code. Every label comes from the scene: object sizes from
   metadata or measured bounds, distances from the camera, counts, and Box targets from
   projected bounds (with occlusion recorded).
2. Questions in the existing schema (choice, noul, score, box), English and Roman Urdu like the
   v1 generators: which is taller or wider; how many chairs; which is closer; is X larger than Y;
   where is the sofa (Box). Add none-fits items as in v1.
3. 3D illusions with known truth: an Ames room, forced perspective (equal objects at different
   depths, unequal objects that look equal). Keep them a separate test set, like the 2D ones.
4. Deterministic from seed, a manifest with item counts and a hash, a sample in `data/sample/`,
   tests (the labels match the scene; the same seed gives the same images), CI green.
5. A spark-lab job to render the full set on the Spark (check headless Chromium on ARM64 first; the
   CPU backend is the fallback) and a v2 train/eval job pair. Then update HANDOFF.md.

Labels come only from code and the scene, never from a model. Don't commit the GLB files or
rendered images; commit the code, the manifest and the sample.

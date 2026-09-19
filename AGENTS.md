# Project continuity

Read PROJECT_LOG.txt, IMPLEMENTATION_PLAN.md, docs/V0_STATUS.md and the original specs before changing architecture. The 19 source documents define the project, with precedence in specs/00_MASTER_PROJECT_PACK.txt.

Maintain PROJECT_LOG.txt in plain language after meaningful work. Distinguish infrastructure tests, real-model evaluations, and untested capabilities. Never claim full V0 acceptance based on scripted-model tests alone.

Run relevant unittest tests for core changes. Real-model evaluation: python scripts/evaluate_local.py. This requires a running local Ollama server and installed model; its narrowly restricted approval callback must not be reused for arbitrary user projects.

Keep production commands explicitly approved and describe the lack of OS sandbox isolation truthfully. Keep runtime downloads/models/evaluation outputs out of Git. Source specs remain preserved; record implementation decisions in docs.

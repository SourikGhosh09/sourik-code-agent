# Project continuity

Read PROJECT_LOG.txt, IMPLEMENTATION_PLAN.md, docs/V0_STATUS.md and the original specs before changing architecture. The 19 source documents define the project, with precedence in specs/00_MASTER_PROJECT_PACK.txt.

Maintain PROJECT_LOG.txt in plain language after meaningful work. Distinguish infrastructure tests, real-model evaluations, and untested capabilities. Never claim full V0 acceptance based on scripted-model tests alone.

Run relevant unittest tests for core changes. Real-model evaluation: python scripts/evaluate_local.py. This requires a running local Ollama server and installed model; its narrowly restricted approval callback must not be reused for arbitrary user projects.

Keep production commands explicitly approved and describe the lack of OS sandbox isolation truthfully. Keep runtime downloads/models/evaluation outputs out of Git. Source specs remain preserved; record implementation decisions in docs.

## Working on Sourik Code Agent

This local desktop agent helps its owner and non-programmers complete verified coding tasks without mandatory paid APIs. Keep the Python/Tk/SQLite architecture and local_agent/ package. tests/ holds unittest coverage, scripts/ runtime/evaluation helpers, docs/ current behavior and specs/ original requirements. src/ is only a pack placeholder.

Read current source and relevant PRD/features/contracts, inspect Git status, plan the smallest correct change, implement, test, diagnose/repair, review Git diff and document. Prefer deleting proven unnecessary code, reusing, modifying, then creating. Never weaken correctness, safety, accessibility, compatibility or useful tests for size. Search existing code, stdlib, native platform and installed dependencies before adding packages or abstractions.

Follow existing Python style: snake_case modules/functions, PascalCase classes, unittest test_ methods. Keep behavior beside its current owner; avoid speculative layers/relocation. Preserve model-independent policy and approval boundaries. No cloud API/accounts/web backend/ORM is implied. Change SQLite deliberately with backup/compatibility consideration; logical relationships are not enforced foreign keys. Validate tool/model/UI input and keep local-only HTTP restrictions.

UI must be understandable, keyboard-accessible and explicit about permissions/errors. Never claim OS sandboxing. Never use fixture auto-approval in production. Exclude real .env, metadata/checkpoints, models/runtimes/raw evaluations from Git. No dotenv loader/required env values exist; document actual configuration before adding settings.

Run relevant unittest checks for core changes and full suite before release. Model acceptance needs real-model evidence/hashes, not scripted tests alone. Review diff for duplication, unnecessary files/dependencies/abstractions. Commit coherent changes preserving unrelated user work; never force-push. Ask only for required intent unavailable in code/context, unauthorized irreversible actions or blocking product decisions.

Update PROJECT_LOG after meaningful work, HANDOVER/TASKS for current status, relevant PRD/features/flows/UI/API/data docs for behavior, SECURITY/operations for boundaries/setup, and docs/DECISIONS for permanent architecture choices. README is the navigation entry. Preserve original specs and distinguish implemented, partial, planned and untested.

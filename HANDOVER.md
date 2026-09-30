# Current handover

Current release: **V1.9.1 preview**, reviewed 2026-09-30. Full Windows suite: **113 passed, two symlink skips (115 total)**. Both V1.9.1 native tag trials passed; intermittent native repair remains unresolved. V1.9.0 compatible tag/invoice trials passed through local Ollama only. Other compatible servers, broad reliability, manual accessibility, clean-machine setup and physical memory-pressure acceptance remain open.

Start Agent.cmd opens Start V1.9.1.cmd. Source commit 8faece3 and tag v1.9.1 are published. [Release CI](https://github.com/SourikGhosh09/sourik-code-agent/actions/runs/36614142137) passed. Later documentation commits do not change the tested runtime. The current local source package is dist/sourik-code-agent-v1.9.1-preview.zip; runtime/models/raw evaluations stay out of Git.

## Implemented and validated scope

- Python/Tk/SQLite local desktop, bounded tools, explicit command approvals, checkpoint recovery, repository indexing, memory and deterministic simplicity policy.
- Background startup discovery and settings snapshots; keyboard shortcuts and improved settings layout. Full manual accessibility acceptance is still open.
- Read-only setup checks for local endpoints/model IDs. Compatible generation forwards state schemas; only Ollama's compatible protocol has real inference evidence.
- V1.9.1 evaluator reports denial reasons and distinguishes failed independent checks from checks not run on untrusted fixtures. Production repair logic and approval rules were not changed.

## Evidence and remaining repair work

Latest [native tag results](docs/evaluation-v1.9.1.json), [compatible trials and native failure](docs/evaluation-v1.9.0.json), and [rejected recovery experiments](docs/evaluation-v1.9.1-candidates.json) retain exact hashes. Historical calculator/invoice acceptance remains bounded to its fixtures and source versions.

Two experimental recovery prompts were rejected and removed with explicit user approval. Cleanup is complete; there is no pending restore approval or candidate code. A local backup remains under .runtime/rejected-v1.9.1-candidate-backup.zip. Three failed candidate trials violated the expression-only AST contract; static inspection suggests equivalent redundant code, but it was not executed and is not independently verified. The V1.9.0 native trial that repeatedly patched normalization.py while catalog.py stayed wrong is a separate genuine repair failure.

Next: capture a genuine failing repair state and compare behavior under controlled inputs before another recovery change. Preserve every outcome; do not loosen fixture approval to obtain a pass. Manual startup/approval/recovery journeys, screen-reader/scaling, clean-machine setup, physical pressure and OS isolation remain separate roadmap items.

No new dependencies, database migration, paid API or mandatory cloud service. Commands have user OS rights; no OS sandbox or hard resource caps. Read current source, PROJECT_LOG.txt and original specs before work. Historical checkpoints belong in the log, changelog and versioned evidence, not current-status claims.

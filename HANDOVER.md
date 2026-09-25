# Current handover

2026-09-25: V1 preview with deterministic Simplicity Engine; not full V1 acceptance.

Completed: local desktop/task loop, V0 narrow acceptance, V1 mapping/memory/profiles and simplicity checks. Latest recorded infrastructure result: 50 passed, one skipped symlink fixture. Four local 7B calculator cases passed; [evidence](docs/evaluation-simplicity.json) identifies source/model hashes.

Current work: requested current-state documentation, source ZIP and private GitHub publication. No new application behavior for this pack. Working files: README/AGENTS, requested docs/operations/ADRs, TASKS/SECURITY/CHANGELOG, environment example, CI, ignore rules and PROJECT_LOG. Check actual remote for publication status rather than assuming it from this note.

Next: EVAL-001 in [tasks](TASKS.md), then responsive discovery/accessibility. Limits: no OS sandbox/hard resource caps; heuristic JS/TS/simplicity; blocking discovery; narrow model evidence; no installer/plugins/custom model. Fresh clones lack runtime/models and generated V0 snapshot.

Open: benchmark projects, hardware/OS, license/distribution, isolation and reporting channel. Next agent: read PROJECT_LOG, IMPLEMENTATION_PLAN, specs and current code; preserve user work/specs; test and review diff; update log; exclude runtime/task data. Move permanent decisions into docs/DECISIONS, not this handover.

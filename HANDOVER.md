# Current handover

2026-09-26: current V1 preview retained. Removed old V0 release directory, release ZIP and Start V0.cmd at user request. Original specs, Git history and historical acceptance evidence remain. Current launchers share the same V1 implementation.

Completed EVAL-001: added a controlled multi-file invoice fixture and three harness tests. Full suite: 53 passed, one skipped Windows symlink fixture. Real local 7B evaluation: one failed run (repeated patch loop after repairing one module), one successful run (two source files repaired, original tests/validation preserved, independent assertions passed). See docs/evaluation-multifile.json. This is not reliable multi-file acceptance. Production application code was unchanged.

Next: REPAIR-001 in TASKS.md, focused action-format validation and repeated-patch recovery, followed by the same local-model trials. Then UI-001 responsive discovery and accessibility checks. Avoid speculative architecture, dependencies or a new model-based policy layer.

Repository: https://github.com/SourikGhosh09/sourik-code-agent (private). Prior publication commits passed hosted CI; check current commit separately. Runtime/models and task outputs remain local-only. Source ZIP is regenerated from committed files.

Read current repository before implementing; choose the smallest correct solution. Preserve specs/user work, explicit production command approval and meaningful tests. No OS sandbox or hard resource caps exist. Update PROJECT_LOG and relevant docs; permanent decisions belong in docs/DECISIONS.

# V1 preview implementation plan

Source precedence remains specs/00_MASTER_PROJECT_PACK.txt. V0 is preserved at commit 462a311 and in releases/v0-462a311 for side-by-side testing.

The first V1 preview follows phase 2 of specs/16_ROADMAP.txt:

1. Task-ranked repository intelligence: safe bounded scans, Python symbols/imports, basic JavaScript/TypeScript symbols/imports, dependency manifests, persistent content-hash cache and deleted-file removal.
2. Inspectable memory: attributable verified results, user notes, stale-evidence exclusion, local add/forget controls. Existing V0 data remains intact.
3. Resource profiles: quality/speed preference, optional CPU/context targets, periodic available-RAM checks between model turns, conservative backoff.
4. Usability: recent projects, task history, reuse a previous goal as a fresh inspected task, separate V0 and V1 launchers.
5. Recovery: durable post-edit fingerprints, warnings for later user changes and legacy checkpoints, explicit overwrite confirmation.
6. Verification: existing regression suite, dedicated V1 behavior tests, real local-model creation/repair and cluttered-repository evaluation. Scripted tests remain separate from real model evidence.

This is a testable V1 preview, not full phase-2 acceptance. Further V1 work includes broader multi-file/language evaluations, project-specific profile overrides, nonblocking startup, fuller ignore/import semantics, and richer pressure handling. Plugin installation, advanced workers and training belong to subsequent roadmap phases. Exact OS resource caps and OS sandbox isolation are not claimed.

## Minimal-change policy increment

Reuse the existing scanner, guarded tools, checkpoints and event store. Add one deterministic policy module, planning estimates and short justifications for flagged growth/dependencies/abstractions. Supply the task diff to the existing model before completion; preserve verification and command permissions. Validate with focused policy tests, the existing suite and local-model calculator/no-change cases. See docs/SIMPLICITY.md for current-code findings and limitations.

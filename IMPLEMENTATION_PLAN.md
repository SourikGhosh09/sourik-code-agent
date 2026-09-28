# V1 preview implementation plan

Source precedence remains specs/00_MASTER_PROJECT_PACK.txt. V0 history remains at commit 462a311; obsolete local release copies and launcher were removed at the user's request. Only current V1 is maintained locally.

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

## V1.1.0 preview

Introduce explicit version labels and make the smallest repair to observed action-contract failures: per-tool required arguments, runtime completeness/no-op validation, and preserved failing-command evidence during repeated-error recovery. Keep architecture, permissions, local models and resource controls. Infrastructure tests and repeated real-model outcomes must be reported separately; no broad reliability claim follows from these fixes.

## V1.1.1 preview

Continue REPAIR-001 within the current architecture. Route repeated unchanged writes through existing evidence refresh; retain the last failed command until successful verification, and clear repeated-failure comparison on actual edits. Keep unchanged writes revision-neutral. Clarify budget feedback and leave inspection/test schema branches free of unrelated explanation requirements, while retaining runtime dependency checks and all command approvals. Regression checks are implemented; real-model acceptance and Windows desktop validation remain pending. Do not expand to UI-001 based on scripted model results alone.

## V1.2.0 preview

After the request to proceed, implement UI-001 independently while retaining the unresolved REPAIR-001 acceptance gate. Reuse threading and the existing event queue: capture UI inputs, discover hardware/models in a daemon thread, handle success/error/cancellation on the Tk thread, and create a task only from a live non-cancelled result. Prevent duplicate startup and keep settings edits for future tasks. No new runtime abstraction or dependency. Eleven automated cases pass; native desktop validation and model acceptance are still required before their respective milestones close.

## V1.3.0 preview

Proceed with INDEX-001 while user-run desktop/model tests are deferred. Reproduce rooted-ignore and relative-import gaps, extend the existing scanner with a documented scoped pattern subset and preserve hard path exclusions. Preserve relative Python import information and boost actual existing module candidates. Invalidate old disposable index records with a parser-versioned fingerprint rather than changing SQLite tables. Keep fixed scan/map bounds and no project execution during indexing. Targeted fixture acceptance is complete; platform/model release acceptance remains separate. Next independent work: RESOURCE-001.

## V1.4.0 resource baseline

Integrate the supplied V1.3.0 source, verify on Windows, then reuse existing telemetry and backoff policy in a bounded read-only diagnostic command. Record actual snapshots separately from simulations. Keep RESOURCE-001 open for inference-load/pressure measurements; do not expand resource control before evidence requires it.

## V1.5.0 setup readiness

Reuse the existing launcher script and local model discovery to diagnose Python/Tk and default Ollama/model availability. Keep checks read-only, no automatic installs and no new dependencies. Verify missing requirements with focused tests and run setup/full regressions from a fresh source copy. Keep clean-machine acceptance separate from same-host checks; do not change the agent loop or broaden model-reliability claims.

## V1.6.0 non-arithmetic evaluation

Add one tag normalization/order fixture to the existing real-model evaluator. Reuse its approval and reporting logic, retaining the original invoice contract. Prove both defects and partial repairs independently; allow only trusted AST variants, preserve tests/validation/README and report exact source/model/evaluator hashes. Run two sequential tag trials and the original invoice regression. Do not modify production reasoning or claim general reliability based on these guided cases.

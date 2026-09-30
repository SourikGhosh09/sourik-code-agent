# Current handover

Published release: **V1.9.2 preview**, 2026-09-30, commit 225af13 and tag v1.9.2. Start Agent.cmd opens Start V1.9.2.cmd. Hosted release CI passed.

V1.9.2 removes obsolete diff text from failed-check model feedback while preserving current source, failure output and review metadata. Full diffs remain in recorded events, the Changes view and successful verification/final review. The new regression fails before the fix and passes after it. Full suite: 114 passed, two symlink skips (116 total). Four native tag trials, two native invoice trials and two compatible tag trials passed on the exact final source. This addresses the reproduced stale-patch trigger, not general repair reliability.

## Diagnosis and evidence

The V1.9.0 native failure was reconstructed from its first two recorded model actions in a fresh trusted fixture. Three identical-input probes repeated the stale normalization patch. Removing only the trailing failed-check diff fields made all three probes target the remaining catalog repair. The historical full wire request was not saved; this is a reconstructed-state comparison. Probe responses were not executed. Exact request/source/model hashes and all final task outcomes: [V1.9.2 evidence](docs/evaluation-v1.9.2.json).

Earlier rejected recovery prompts remain separate historical evidence in [candidate report](docs/evaluation-v1.9.1-candidates.json); cleanup is complete and no approval remains pending. Their three AST-contract failures do not prove incorrect functional output. No broader claim follows from the new narrow fixture results.

## Architecture and remaining work

Python/Tk/SQLite, local-only model adapters, deterministic simplicity policy, background discovery, keyboard navigation, scoped indexing, memory and recovery remain unchanged. No dependencies or database migration. Commands still require approval and have user OS rights; there is no OS sandbox or hard resource cap. Fixture approval must never be reused for arbitrary projects.

Next: validate another representative real project and retain any intermittent failures. Full manual startup/approval/recovery journeys, screen-reader/scaling, clean-machine setup, other compatible servers, physical pressure and OS isolation remain open. Runtime/models/raw evaluations and the rejected-candidate backup stay local. Original specs and prior evidence remain preserved.

## Less-guided evaluation checkpoint

Two new local 7B trials described desired tag behavior without naming repair expressions. Both exhausted the step budget. The model alternated normalization expressions and left catalog.py unchanged; the final normalization AST was outside the trusted variants. Independent checks did not run. Tests, validation and README were preserved. This exposes a limitation of both task completion and the fixed-variant evaluator; it is not an independent measurement of rejected code correctness. All 11 evaluator tests passed. No production changes, dependency additions or new release. Exact prompt, harness, hashes and both outcomes: [evidence](docs/evaluation-v1.9.2-behavior.json). Next: distinguish approval-rejection recovery from repair accuracy with a controlled comparison before changing production prompts; broader projects need separately reviewed execution.

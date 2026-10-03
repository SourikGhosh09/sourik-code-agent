# Current handover

Published release: **V1.10.0 preview**, 2026-10-03, tested commit 20b274c and tag v1.10.0. Start Agent.cmd opens Start V1.10.0.cmd. [Hosted release CI passed](https://github.com/SourikGhosh09/sourik-code-agent/actions/runs/37089341731). Full local suite: 116 passed, two Windows symlink skips (118 total); both guided tag trials passed with Custom set to 12 threads and 8192 context tokens. Choose AI power -> Custom to edit these targets. Current source ZIP: dist/sourik-code-agent-v1.10.0-preview.zip.

The earlier V1.9.2 checkpoint removed obsolete diff text from failed-check model feedback while preserving current source, failure output and review metadata. Full diffs remain in recorded events, the Changes view and successful verification/final review. Its regression failed before the fix and passed after it. That checkpoint's full suite: 114 passed, two symlink skips (116 total). Four native tag trials, two native invoice trials and two compatible tag trials passed on that exact source. This addresses the reproduced stale-patch trigger, not general repair reliability.

## Diagnosis and evidence

The V1.9.0 native failure was reconstructed from its first two recorded model actions in a fresh trusted fixture. Three identical-input probes repeated the stale normalization patch. Removing only the trailing failed-check diff fields made all three probes target the remaining catalog repair. The historical full wire request was not saved; this is a reconstructed-state comparison. Probe responses were not executed. Exact request/source/model hashes and all final task outcomes: [V1.9.2 evidence](docs/evaluation-v1.9.2.json).

Earlier rejected recovery prompts remain separate historical evidence in [candidate report](docs/evaluation-v1.9.1-candidates.json); cleanup is complete and no approval remains pending. Their three AST-contract failures do not prove incorrect functional output. No broader claim follows from the new narrow fixture results.

## Architecture and remaining work

Python/Tk/SQLite, local-only model adapters, deterministic simplicity policy, background discovery, keyboard navigation, scoped indexing, memory and recovery remain unchanged. No dependencies or database migration. Commands still require approval and have user OS rights; there is no OS sandbox or hard resource cap. Fixture approval must never be reused for arbitrary projects.

Next: validate another representative real project and retain any intermittent failures. Full manual startup/approval/recovery journeys, screen-reader/scaling, clean-machine setup, other compatible servers, physical pressure and OS isolation remain open. Runtime/models/raw evaluations and the rejected-candidate backup stay local. Original specs and prior evidence remain preserved.

## Less-guided evaluation checkpoint

Two new local 7B trials described desired tag behavior without naming repair expressions. Both exhausted the step budget. The model alternated normalization expressions and left catalog.py unchanged; the final normalization AST was outside the trusted variants. Independent checks did not run. Tests, validation and README were preserved. This exposes a limitation of both task completion and the fixed-variant evaluator; it is not an independent measurement of rejected code correctness. All 11 evaluator tests passed. No production changes, dependency additions or new release. Exact prompt, harness, hashes and both outcomes: [evidence](docs/evaluation-v1.9.2-behavior.json). Next: distinguish approval-rejection recovery from repair accuracy with a controlled comparison before changing production prompts; broader projects need separately reviewed execution.

## Approval-recovery comparison - 2026-10-01

The four follow-up trials ran on September 30 and were collected after an approval-service usage limit interrupted inspection. Exposing the existing fixture denial reason passed 0/2 trials. Pre-fixing normalization while retaining original denial feedback also passed 0/2. All four hit the step limit and ended outside approved variants, so independent checks did not run. Static inspection found remaining sorting, input processing before validation, and one catalog indentation error. These observations do not establish a complete root cause, but clearer rejection wording alone is not a demonstrated fix. All 24 evaluator/controller tests passed. Production source, evaluator, permissions and dependencies remain unchanged; V1.9.2 remains current. Full prompts, harnesses, final source and hashes: [comparison evidence](docs/evaluation-v1.9.2-denial-comparison.json). Next: establish separately reviewed execution or a validated isolation boundary before expanding behavior-based evaluation. Do not broaden the existing fixture auto-approval.

## Custom power increment

V1.10.0 adds Custom AI power using the existing CPU-thread and context fields. Custom permits 1 through the detected logical CPU count and 2048–16384 context tokens; blanks use half the logical CPUs (at least one) and 8192 tokens. Other presets retain their caps. Speed caps context at 4096. Low-memory startup caps context at 4096; existing between-turn pressure backoff may lower targets to two threads and 2048 tokens. Custom retains one worker and 40 steps. These targets are forwarded to Ollama; compatible servers manage their own thread/context settings. No hard CPU, RAM or GPU limits or OS sandbox are provided. No dependencies, new settings keys or database migration.
Full local suite: 116 passed, two Windows symlink skips (118 total). Added resource-boundary/backoff and native reveal/focus checks; extended settings snapshot/persistence coverage. Less-guided repair limitations remain open and are not repaired by this feature.

V1.10.0 real-model check: both guided tag trials passed independent assertions with Custom set to 12 threads and 8192 context tokens. Protected files stayed intact; exact source/model/evaluator hashes are in docs/evaluation-v1.10.0.json. This does not close less-guided reliability or physical-pressure acceptance.

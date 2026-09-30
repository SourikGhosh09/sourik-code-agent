# Minimal-change policy

Documentation reviewed 2026-09-30 against V1.9.1. [Current status](../HANDOVER.md) governs present acceptance; dated checkpoints below are historical evidence.

## Historical integration baseline (2026-09-24)

The current code is a Python standard-library V1 desktop preview, despite V0 wording in some package metadata. The console entry point and `python -m local_agent` both open the Tk application; there is no separate headless task CLI. Git was clean before this change.

Implemented code paths: bounded planning/action/test/repair loop; Ollama and local OpenAI-compatible adapters; project-scoped file tools; explicit command approval; cancellation and timeouts; SQLite tasks/events and inspectable memory; ranked repository summaries; resource targets and RAM-pressure backoff; durable checkpoints and conflict-aware recovery. The unmodified suite was rerun: 37 passed, one Windows symlink fixture skipped.

Partial capabilities: Python indexing plus heuristic JS/TS extraction; conservative ignore handling; bounded, basic memory retrieval; best-effort process cleanup; resource targets rather than hard OS caps. A verification command passing is not proof of complete requirement coverage. Approved commands execute with user privileges, without OS isolation.

Planned, not implemented: executable skill/plugin installation, model training, specialized multi-agent workers, broad language/framework acceptance, hard resource isolation and a production distribution pipeline. Existing documentation and old evaluation reports were treated as historical evidence, not proof of the new code.

## Research and selection

Reviewed Ponytail's [README](https://github.com/DietrichGebert/ponytail), [core skill](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail/SKILL.md) and [diff-review skill](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail-review/SKILL.md). Useful principles are inspection before choosing a solution, reuse/native capabilities before invention, and a separate check for unnecessary complexity. Its benchmark results were not reproduced and are not evidence about this agent.

Our policy is independently written. No Ponytail package, hooks, code, cloud service or additional model is installed or required. We do not adopt code golfing, arbitrary line-reduction scores, reduced requested scope, or test minimization that loses coverage.

## Integration

`Agent -> existing repository map/read/search -> plan + estimate -> SimplicityEngine.before -> existing Tools -> test/repair -> task diff review -> completion`

One module, `local_agent/simplicity.py`, contains deterministic checks and a short model-neutral instruction. It uses existing Tools and repository metadata. Policy reports use the existing SQLite event stream and desktop Progress/Technical details tabs; no new database, worker or plugin architecture is introduced.

The decision preference is: no change if already satisfied; delete proven unnecessary code; reuse project code; use standard library, platform/framework or existing dependencies; modify current files; create only what is needed. Correctness, requested behavior, validation, accessibility, security, data integrity, compatibility and useful tests take precedence.

- Before planning, read bounded relevant excerpts and search callers when a mapped symbol appears in the goal. Other relevant code can be searched/read using existing tools. This is evidence collection, not proof of complete comprehension.
- Plans declare expected total files, new files, dependencies and approximate complexity. Existing scripted/custom adapters without a budget remain compatible; missing estimates mean the count gate cannot apply. Production structured schemas request the estimate.
- Existing files outside the initial inspection must be read before mutation. Fresh model-written files do not require an unnecessary second read just to make a repair.
- Matching symbol names suggest potential reuse. New manager/factory/wrapper/adapter/service/interface names flag a possible abstraction. These are hints, not proof that the code is redundant.
- Recognized package-install commands and added names in package.json, pyproject.toml and requirements*.txt require reconsideration. Version-only changes do not count as new packages. Declarations do not prove a package is installed or suitable.
- Flagged actions are withheld until the model changes its approach or supplies a nonempty `simplicity` explanation. Counts can be exceeded for a justified feature; there are no automatic deletions or fixed line ceilings. Normal command approval still happens afterward.
- Reviews report actual changed/new files, added dependency declarations, estimate overages and a bounded diff. They appear after file changes and command runs, and are supplied to the existing model with successful verification before completion. Repairs still invalidate verification and must be retested. Completion above the estimate requires an explanation.

The automatic review reuses the existing **task checkpoint diff**, not a new Git subprocess. It includes new files and isolates changes from the task's starting state, including in folders without Git. A broader Git diff can be requested through the existing approved command tool. We reviewed this integration's actual Git diff during development. The automatic policy does not claim to inspect staged history, run Git silently, or include unrelated pre-task changes.

## Limits and extension boundary

The policy checks are deterministic; whether an explanation is true and a smaller implementation is equally correct still requires the coding model, tests and review. A nonempty explanation is auditable reasoning, not a semantic proof. It cannot discover every duplicate implementation, infer all native alternatives, detect every installer hidden in shell/script commands, or guarantee necessary security/accessibility code was preserved. It never authorizes a command or suppresses an existing verification gate.

Inspection, scan and file-size limits from the existing tool layer still apply. Added excerpts/diffs and the prompt map are bounded according to the context profile; the full checkpoint diff remains available in Changes. Truncation is disclosed. This adds no separate inference service, though reconsideration can use extra turns within the existing task budget.

Any model implementing the existing `generate(messages, config)` protocol receives the same policy/evidence and returns the same JSON actions. A future skill can contribute repository knowledge through the existing context boundary, as untrusted evidence; it must not override safety or grant permissions. A plugin rule registry, learned scoring, semantic duplicate analysis and automatic refactoring are deferred until there is a demonstrated need.

## Verification

Infrastructure tests cover repository reuse/callers, dependency declarations and install gates, justified larger changes, inspection before editing, diff scope, secret/path boundaries, no-change completion with verification, review delivery to the model, and the existing desktop entry point.

Real-model evaluation: `python scripts/evaluate_local.py qwen2.5-coder:7b --simplicity`. This extends the existing calculator fixtures with an already-satisfied request that must complete without code changes. Its restricted approval callback remains confined to these fixtures.

Final verification on 2026-09-25: 51 unittest cases ran, with 50 passed and one Windows symbolic-link fixture skipped. Real junction boundary tests passed. All four real-model cases completed and passed independent assertions; repair cases preserved original tests, and the already-satisfied case left zero code changes. Exact model/source hashes and timings are in [evaluation-simplicity.json](evaluation-simplicity.json). The final source hash was checked against the working files. Original run: evaluation-results/20260925-101953; local logs: .runtime/simplicity-acceptance.log and .runtime/simplicity-regression.log. Earlier attempts exposed planning loops, missing required justification fields and unwanted review-file creation; those failures were used to repair the integration rather than reported as success. This is not a broad efficiency benchmark or a claim of measured code/token savings.

## V1.1.1 feedback correction

Budget counts are estimates of actual change, not quotas to fill. Review and pre-action messages explicitly distinguish them from test failures and direct necessary explanations into the JSON `simplicity` field, not project files. After a flagged action, read/search/list/run schema branches stay available without an unrelated required explanation. Mutation/completion branches still request it; runtime installation/dependency checks and command approval remain enforced. The model can still disregard task instructions: no new README protection or semantic guarantee is claimed. Retesting was pending at that checkpoint; see [historical evidence](evaluation-v1.1.1.json) and [current status](../HANDOVER.md).

## V1.4.2 repair policy

File-count estimates for patches/writes to existing files are checked at final review rather than repeatedly blocking each repair. Completion still requires justification for exceeded estimates. New-file, dependency, inspection and abstraction gates remain. Reviews are recorded after changes; the repair prompt uses current source, while verification/final review receives the diff.

An explicit English clause beginning with Preserve (at the start of a request or after a period, semicolon or newline) and containing tests before the next period/newline marks existing test_ files, *_test.py files and files below a tests directory read-only for file tools. Example: Preserve validation, README and existing tests. This is a narrow literal convention, not a general natural-language constraint parser; it does not infer that all named files are immutable. New test files and reading remain allowed.

Current V1.9.1 policy remains deterministic and model-independent. Later calculator/invoice/tag evidence supplements the historical integration baseline; it does not prove general minimality or reliability. The rejected recovery prompt experiments are not part of the policy. See [current status](../HANDOVER.md) and [candidate findings](evaluation-v1.9.1-candidates.json).

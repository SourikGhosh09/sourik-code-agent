# Test plan

Preserve meaningful correctness/safety tests; do not delete tests to improve code-size metrics. Infrastructure and real-model evaluations answer different questions.

## Commands and recorded evidence

- python -m unittest discover -v: latest recorded 57 tests, 56 passed, one skipped because Windows could not create a symlink fixture. Real junction checks passed.
- python -m compileall -q local_agent scripts tests: syntax/bytecode compilation, not type checking or an installer build.
- python scripts/evaluate_local.py qwen2.5-coder:7b --simplicity: requires local Ollama/model; four calculator cases passed independent assertions. [Exact source/model evidence](evaluation-simplicity.json).

Real cases: empty-project creation, broken-project repair, repair among 110 unrelated files with stale memory, and already-correct code with zero changes. Repair preserves original tests. These narrow cases are not broad reliability, accessibility, isolation or efficiency benchmarks.

| Requirements | Required coverage |
|---|---|
| R01 | Path/ignore/link boundaries, bounded reads/maps, index refresh, empty/unreadable/binary data |
| R02 | Failed baseline, zero-test rejection, edits invalidate verification, bad model output, repair evidence, limits/cancel and independent behavior checks |
| R03 | Denial, argv/no implicit shell, time/output limits, atomic writes, crash manifests, conflicting later edits and explicit overwrite |
| R04 | SQLite recovery/persistence, note validation/redaction/forget, stale evidence exclusion, fresh history reuse |
| R05,R08 | Local-only endpoints, errors, profiles, installed model choice, low-RAM backoff; no hard-cap claim |
| R06 | Existing/caller inspection, dependency/layer/growth warnings, justification, tests unblocked by budgets, task diff excludes prior edits, no-change completion |
| R07 | Tk construction/error display; manual keyboard, screen-reader, scaling, approvals/history/recovery still pending |

No account-authentication or API-server tests apply. Authorization covers commands/files. CI runs Windows Python versions without models. No formatter, linter or type checker is configured; compilation is not a substitute claim.

Done means: inspect relevant code, implement minimally, run relevant regressions, review Git diff, repair failures and update PROJECT_LOG with evidence and limits. Model-behavior changes need real-model hashes/independent outcomes for acceptance. Keep raw outputs/downloads out of Git. Never reuse the evaluator's fixture-only approval on arbitrary projects.

Pending: multi-file/language cases, repeated controlled comparison, fresh-machine setup, manual accessibility journeys, pressure/OOM and future isolation tests. Measure before expanding architecture.

## Initial multi-file evaluation - 2026-09-26

Run `python scripts/evaluate_local.py qwen2.5-coder:7b --multifile` for two fresh invoice projects. Separate validation, line-item and invoice modules exercise imported behavior and two arithmetic defects. Existing tests/validation/README must remain intact; independent checks cover zero quantities, full discount and invalid inputs.

Result: one run failed at the step limit after repeatedly patching the already-correct invoice function; one completed in 30.96 seconds, changing exactly line_items.py and invoice.py. Both preserved tests/validation; no extra files or dependencies were accepted. [Exact results and hashes](evaluation-multifile.json). The first failure took 76.67 seconds. This is mixed evidence, not reliable multi-file acceptance or a broad benchmark.

Automated approval only permits unittest discovery on AST-identical known buggy/fixed fixture variants. It rejects changed tests/validation, extra executable files and arbitrary commands. This intentionally constrained harness cannot evaluate unrestricted implementations and must never be used on user projects. Production code and its permissions did not change in this stage.

## V1.1.0 preview verification

Three new contract regressions verify required per-tool schema arguments, missing-field recovery retaining failed-test evidence, identical-text patch rejection, and package/application version consistency. Full suite: 56 passed, one Windows symlink fixture skipped. Command approval and path protection remain unchanged. Real-model outcomes for this exact version are recorded separately; the older calculator evidence is historical, not proof of the changed version.

Final V1.1.0 real-model result: both invoice trials failed (140.03 and 132.06 seconds). Both arithmetic files were repaired, but the model also changed the required-unchanged README and repeated writes; fixture execution was denied and the step budget exhausted. The combined tests_and_validation_preserved field includes README preservation; the original test and validation files themselves were unchanged. Independent execution was skipped after the fixture failed its trust check. See [versioned evidence](evaluation-v1.1.0.json). No reliability improvement is claimed.

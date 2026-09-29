# Test plan

Preserve meaningful correctness/safety tests; do not delete tests to improve code-size metrics. Infrastructure and real-model evaluations answer different questions.

## Commands and recorded evidence

- python -m unittest discover -v: current V1.7.1 Windows run has 104 tests: 102 passed and two symlink-fixture skips. Native Tk and junction checks pass; teardown callback diagnostics and manual UI checks remain documented below. Historical platform results are retained in their versioned sections.
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

## V1.1.1 preview verification — 2026-09-26

- Added four regressions: scripted invoice repair after repeated unchanged writes (existing trusted fixture, original README/tests/validation intact); successful verification clears old failure output and survives an unchanged write; repeated unchanged writes cannot fabricate verification or approval and stop at the step limit; budget reconsideration permits inspection/testing with no unnecessary files.
- Updated schema assertions to require explanations for mutations/completion while preserving runtime installation gates. Existing approval, zero-test, file-boundary, post-edit verification and fixture tests remain intact.
- Focused command: `python -m unittest tests.test_contracts tests.test_simplicity tests.test_failures tests.test_evaluation -v` — 32 passed.
- Full suite: 61 run, 57 passed, two platform skips (Windows runtime launcher and junction), two errors (`test_task_failure_display`, `test_desktop_memory_and_history`) because Tk cannot connect to a display. Baseline ZIP had the same two errors. Tests were not modified to skip the display requirement.
- `python -m compileall -q local_agent scripts tests` passed. Two new recovery/schema regressions fail on the unchanged original app and pass on V1.1.1.
- Real-model command attempted unchanged: `python scripts/evaluate_local.py qwen2.5-coder:7b --multifile`. It stopped during `/api/tags` discovery with connection refused. Zero trials ran; no model digest or independent model result is available. The evaluator and all original fixture text are byte-for-byte unchanged.

Rerun the full suite on the Windows desktop and the same two invoice trials with Ollama. Keep REPAIR-001 open until evidence meets its acceptance criteria. See [machine-readable checkpoint](evaluation-v1.1.1.json).

## V1.2.0 preview verification — 2026-09-26

`python -m unittest tests.test_ui.Startup -v`: 11 passed. Tests use real background threads and queues; UI doubles assert main-thread access. One runs the actual display-free Tcl event loop and handles a callback while hardware discovery is paused. Covers delayed hardware, duplicate Run, cancellation during discovery and after the result is queued, close during model discovery, failure/retry, settings snapshots, invalid input, auto model selection, preference-write failure cleanup, and a real Agent with scripted failed-task output. These tests do not certify native Tk rendering, Windows integration or real-model coding quality.

Full suite: 72 run, 68 passed, two skips (Windows portable launcher and junction checks), two errors at Tk construction (no display). These are the same pre-existing environment limits. Compilation passed. The real-model evaluator, original fixtures, agent loop and approval policies are unchanged from V1.1.1; no new Ollama run was possible in this environment. Evidence: [evaluation-v1.2.0.json](evaluation-v1.2.0.json).

### Pending native Windows startup smoke checks

| Check | Expected result | Recorded status |
|---|---|---|
| Open Start Agent.cmd with local Ollama running | V1.2.0 preview window opens and controls work | Pending |
| Run with Auto model enabled | Preparing is visible; window can be moved/edited; task starts with selected model | Pending |
| Stop while Preparing | No task/command begins from the cancelled discovery; Run becomes available after check returns | Pending |
| Close while Preparing | Window closes; no task starts later | Pending |
| Set server to an unused loopback port and Run with Auto model | Window stays available; error appears; restoring correct server permits retry | Pending |
| Edit goal/model/project while Preparing | Current run uses captured values; edited values stay for the next run | Pending |
| Start a normal task and close during execution | Existing Stop-and-wait behavior and command approval remain intact | Pending |

Run `python -m unittest discover -v` on the Windows desktop, then the unchanged two-trial invoice evaluation with Ollama. Keep UI-001 and REPAIR-001 acceptance separate. UI-002 keyboard/screen-reader/scaling journeys remain pending.

## V1.3.0 indexing verification — 2026-09-26

Ten new tests in tests/test_indexing.py cover rooted/nested/directory-only patterns, component/recursive globs, ordered negation, pruned parents, hard secret guards, linked ignore/source rejection, relative import metadata, an integrated checkout repair-context fixture with misleading same-name modules, ordinary src/package candidates, legacy cache refresh/removal and map limits. The two focused ignore/import cases fail against V1.2.0 and pass after correction.

`python -m unittest tests.test_indexing tests.test_agent tests.test_recovery tests.test_simplicity -v`: 40 passed. A separate development comparison with local Git 2.51.1 matched 12 supported rule scenarios over 17 paths each; Git is not called by production or required by unit tests. Full suite: 82 run, 78 passed, two Windows-only skips and the same two no-display Tk construction errors. Compilation passed. See [evidence](evaluation-v1.3.0.json). No new real-model run was attempted.

## Deferred user validation — requested 2026-09-26

These are queued for later; do not require the user to run them before further independent development or claim they passed.

- Windows full suite on the eventual combined preview, including native Tk, junctions and launcher behavior.
- UI-001 native startup/cancel/close/retry matrix above, plus UI-002 keyboard/screen-reader/scaling journey.
- Both unchanged real-model invoice trials (REPAIR-001), with source/model/evaluator hashes and independent preservation/behavior outcomes.
- A representative real user project to assess context relevance; passing static fixtures does not establish coding reliability.

INDEX-001's bounded fixture acceptance is complete. RESOURCE-001 can proceed independently; final release acceptance remains contingent on the pending evidence. No immediate testing action is required from the user.

## V1.4.0 Windows and resource baseline

The supplied V1.3.0 source was run on the actual Windows workspace: 82 tests, 80 passed, two symlink-fixture skips. Its previous no-display GUI errors did not occur. V1.4.0 adds three resource-diagnostic tests: separation of host samples/simulations, low-memory then recovery without raising targets, unknown telemetry and invalid sampling rejection. Combined suite: 85 tests, 83 passed, two symlink skips; native Tk/junction checks and compilation passed.

Run `python scripts/measure_resources.py --samples 3 --interval 1 --output evaluation-results/resource-baseline.json` with a new output filename. Recorded real available RAM was approximately 6.50-6.66 GiB; actual backoff did not occur. Simulated 1 GiB availability reduces future targets, but this does not prove behavior under physical pressure. Raw GPU values are nvidia-smi readings, not model-process usage. [Evidence](evaluation-v1.4.0.json).

The Windows automated full-suite item above is now satisfied for this source. Manual startup/accessibility and real-model invoice checks remain pending. RESOURCE-001 still needs a reproducible inference-load measurement; this baseline induces no workload and cannot establish OOM safety or hard caps.

## V1.4.0 actual inference workload - 2026-09-27

Ran the unchanged two-trial invoice evaluator with qwen2.5-coder:7b while a read-only observer called the existing hardware detector before, during and after execution. Sampling waited five seconds between detections, capped at 180 during-workload samples; the cap was not reached. Recorded 42 snapshots, including before/after. Available RAM: 4.793-7.543 GiB; NVIDIA GPU free memory: 6,663-11,761 MiB. No sampled RAM reading crossed the 2 GiB backoff threshold. This completes a normal inference-load measurement, not forced low-memory or OOM acceptance.

Both trials failed at their step limit (102.45 and 94.79 seconds), changing only invoice.py. Existing tests, validation and README remained intact, and the trusted-fixture checks passed; independent behavior checks failed because the other arithmetic defect remained. Repeated patch/unchanged-edit reasoning is still unresolved. [Exact results and measurement summary](evaluation-v1.4.0-workload.json). Raw report/log are under ignored evaluation-results/workload-20260927-094016/; trial fixtures are in evaluation-results/20260927-094016/.

To repeat the workload, run `python scripts/evaluate_local.py qwen2.5-coder:7b --multifile` with the same installed model. In a second terminal, start `python scripts/measure_resources.py --samples 60 --interval 5 --output evaluation-results/resource-inference-repeat.json` using a new output filename before launching the evaluator. Record the start/end times and evaluate only overlapping samples. The sampler itself starts no workload; its baseline labels must not be interpreted as proof that external model activity was absent. Keep simulated policy checks separate from host samples. Whole-host memory includes other applications, samples can miss peaks, and free VRAM is not per-process model allocation.

Hosted CI for the path-alias correction 743320f passed. No production source changed during this measurement stage; a new app version is unnecessary. Native manual accessibility/startup checks and real-model repair acceptance remain open.

## V1.4.1 recovery checkpoint - 2026-09-27

V1.4.1 removes stale initial source/memory excerpts from repeated-failure recovery while retaining the goal, system policy, current bounded file evidence and explicitly stale last-test output. The strengthened regression fails before the fix and passes after it. Seven focused tests passed; full Windows suite: 83 passed, two symlink skips (85 total). Compilation passed. Both unchanged 7B invoice trials failed at the step limit (111.51 and 51.03 seconds). Trial one changed line_items.py and test_invoice.py, failing fixture trust; trial two changed only line_items.py, preserving tests/validation/README but leaving invoice arithmetic incorrect. REPAIR-001 remains open; no model-reliability improvement is established. Evidence: docs/evaluation-v1.4.1.json.

## V1.4.2 verification - 2026-09-28

V1.4.2 passed four consecutive unchanged invoice trials on the exact final source, plus all four calculator/no-change cases. Every invoice trial preserved tests, validation and README, changed only invoice.py and line_items.py, and passed independent assertions. Full Windows suite: 88 passed, two symlink skips (90 total). Evidence and source/model/evaluator hashes: docs/evaluation-v1.4.2.json. This closes the narrow REPAIR-001 fixture milestone, not broad coding reliability.

New/strengthened regressions cover fresh source/goal and verified-review context, completion schema and runtime revision gating, freshly approved/denied scheduled checks, existing-test write/patch/delete/move and ancestor-move rejection, negated preservation requests, and deferred existing-file count review with new-file gates intact. Existing native Tk tests pass but emit teardown callback diagnostics; manual accessibility acceptance is still pending. Raw results remain ignored; intermediate failures are summarized in the versioned evidence rather than discarded.

## V1.4.3 checkpoint - 2026-09-28

V1.4.3 prevents same-timestamp checkpoint collisions using atomic standard-library directory creation. The forced-clock regression fails on V1.4.2 and passes after the fix, including independent rollback. Final Windows suite: 89 passed, two skips (91 total). Both unchanged invoice trials and all four calculator/no-change cases passed independent checks on the exact V1.4.3 source; invoice tests, validation and README remained intact. See docs/evaluation-v1.4.3.json.

## V1.5.0 setup verification - 2026-09-28

Seven launcher tests pass, including the original wait-for-readiness case and six new checks covering an external server without portable files, missing/invalid models, unavailable/malformed discovery, unavailable Tk, old Python, actionable missing-runtime errors and proxy/redirect restrictions. Mocked setup checks assert no process launch or files created in the checkout. Actual readiness and all 97 tests (95 passed, two symlink skips) also ran from a fresh source copy on the current Windows machine using its existing Ollama server. This is not a clean-machine, manual accessibility or real-model coding evaluation. Pre-existing Tk teardown callback diagnostics remain. No agent-flow or evaluator change; latest model results remain V1.4.3.

## V1.6.0 tag catalog verification - 2026-09-28

Run `python scripts/evaluate_local.py qwen2.5-coder:7b --tags`. Two disposable fixtures require Unicode casefolding and stable deduplication across imported modules. The goal names the expected expression repairs; the approval callback accepts only original/fixed AST variants and unchanged tests/validation/README. It rejects additional executable files and unrelated commands. This intentionally restricted approval is not an OS sandbox and must never be used for user projects.

Seven evaluator unit tests pass: three original invoice cases plus four tag cases. Both fixture defects and each partial repair fail independent assertions; the combined fix passes Unicode equivalence, first-seen order, input preservation, iterator, empty and invalid-tag checks. Full Windows suite: 99 passed, two symlink skips (101 total), with the pre-existing Tk teardown diagnostics. Two real-model tag trials passed; exact hashes and invoice regression results are recorded in evaluation-v1.6.0.json. These runs do not certify general coding reliability, manual accessibility, low-memory pressure or clean-machine setup.

## V1.7.0 native keyboard/layout verification

V1.7.0 adds keyboard navigation and compact model settings. Tab/Shift+Tab leave the request field without editing it; Ctrl+Enter runs through the existing task action, Esc requests Stop, and Ctrl+L focuses the project field. Ctrl+Tab/Ctrl+Shift+Tab cycle output tabs. Full Windows suite: 102 passed, two symlink skips (104 total). No dependencies or agent/approval changes. Manual screen-reader, full scaling and approval/recovery journeys remain pending.

The original settings row requested 1048 pixels with 732 available at 780x600 and Tk scaling 2.0. Three native tests cover horizontal fit, forward/backward focus without text changes, Run/Stop/project shortcuts and forward/backward output traversal. They reproduced newline insertion before Ctrl+Enter and failed notebook traversal during implementation; both were corrected. Compilation passed. Pre-existing Tk teardown callback diagnostics remain; no new model evaluation was required for these UI changes.

## V1.7.1 cleanup verification

V1.7.1 repairs native test teardown: close through App.close, release UI references and collect cycles on the main thread before later worker tests. Ten sequential UI/history repetitions passed (240 tests), followed by the full suite: 102 passed, two symlink skips (104 total). No Tk teardown diagnostics appeared in those runs. Production behavior, existing timeouts and dependencies are unchanged. Latest real-model evidence remains V1.6.0; manual accessibility and clean-machine acceptance remain open.

A GC-disabled probe showed a plain destroyed window released its variable immediately, while a real Agent approval callback retained it through an App/Agent cycle. Main-thread collection released the cycle. Weak-reference teardown assertions now verify release in native task and keyboard tests. This reproduces retention and removes the observed cleanup diagnostics; the exact historical Python 3.12 scheduling failure was not deterministically reproduced locally. Hosted CI remains an additional check, not proof that all timing failures are impossible.

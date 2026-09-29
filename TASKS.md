# Implementation roadmap

Historical candidate checkpoint (cleanup subsequently completed): rejected V1.9.1 prompt candidates await explicit cleanup approval following automatic-review rejection. Evidence: docs/evaluation-v1.9.1-candidates.json. No new release; V1.9.0 remains current. Next diagnose repair repetition separately from narrow fixture approval failures, without weakening approval or acceptance tests.

Statuses follow code/evidence, not roadmap promises. References: [PRD](docs/PRD.md), [testing](docs/TEST_PLAN.md), original specification precedence.

## Foundation and preview

- [x] BASE-001 - Local desktop task loop. Depends: none. Ref: R01-R03,R07,R08, [architecture](docs/ARCHITECTURE.md). Acceptance: bounded tools, approval, revision verification and recovery. Tests: regressions and recorded V0 calculator cases.
- [x] V1-001 - Repository evidence, memory and profiles. Depends: BASE-001. Ref: R04-R05, [data](docs/DATA_MODEL.md). Acceptance: preview behavior/limits documented. Tests: V1 regressions/indexed repair; full resource control remains incomplete.
- [x] SIM-001 - Minimal-change policy. Depends: V1-001. Ref: R06, [simplicity](docs/SIMPLICITY.md). Acceptance: inspection/gates/diff preserve permissions/tests. Tests: 13 policy tests, four real-model cases.
- [x] DOC-001 - Current documentation pack. Depends: SIM-001. Ref: [README](README.md). Acceptance: requested files match source and preserve specs. Tests: references, inventory and diff review.

## Next V1 work

- [x] EVAL-001 - One representative multi-file Python repair fixture. Depends: SIM-001. Ref: R02,R06. Acceptance: independent assertions, original tests, source/model hashes and edit/dependency observations. Tests: fixture validation and repeated model runs; no broad claims from one case.
- [ ] UI-001 - Nonblocking startup discovery (implemented in V1.2.0; native manual acceptance pending). Depends: BASE-001. Ref: R07, [UI](docs/UI_SPEC.md). Acceptance: responsive window with slow/failed discovery and safe close. Tests: delayed/failing discovery and manual launch/close.
- [ ] UI-002 - Keyboard/screen-reader journey validation. Depends: UI-001. Ref: R07,F01-F05. Acceptance: record focus/labels/scaling/approval/recovery and repair demonstrated barriers. Tests: manual matrix and focused regressions.
- [x] INDEX-001 - Representative ignore/import fixture (V1.3.0; documented subset). Depends: V1-001. Ref: R01. Acceptance: reproduce limitation, smallest justified fix. Tests: ranking/ignore boundaries without weaker secret protection.
- [ ] RESOURCE-001 - Repeatable pressure measurement (V1.4.0 baseline sampler and simulated checks implemented; normal inference load measured; low-memory/physical-pressure validation pending). Depends: V1-001. Ref: R05. Acceptance: record RAM/VRAM behavior before changes; no hard-cap claim. Tests: simulated telemetry and measured run.

- [x] REPAIR-001 - Action/repeated-repair correction; narrow invoice acceptance met in V1.4.2. Depends: EVAL-001. Four final-source invoice trials passed independent assertions without changing the fixture, tests, validation, README or approvals. Calculator/no-change regression also passed. Broader reliability remains unaccepted. See [evidence](docs/evaluation-v1.4.2.json).

## Security and distribution

- [ ] SEC-001 - Select bounded OS-isolation approach. Depends: EVAL-001. Ref: R03, [security](SECURITY.md). Acceptance: ADR compares threat boundary/compatibility/cost; no implementation claim before boundary tests. Tests: proof-of-concept escape/permission checks after decision.
- [ ] DIST-001 - Clean-machine source setup (V1.5.0 readiness check and fresh-source-copy tests implemented; genuinely clean-machine acceptance pending). Depends: DOC-001. Ref: [deployment](docs/operations/DEPLOYMENT.md). Acceptance: setup works without original machine files. Tests: fresh checkout launch, regressions and disposable task.
- [ ] RELEASE-001 - Distribution/license and release gates. Depends: EVAL-001,UI-002,DIST-001,SEC-001. Ref: [PRD](docs/PRD.md). Acceptance: owner-approved scope/support, reporting channel and evidence. Tests: exact-release acceptance rerun.

Plugins, advanced workers and training remain later original roadmap phases, not scheduled implementation. Do not build speculative managers/dependencies before concrete tasks.

## V1.1.1 repair checkpoint — 2026-09-26

REPAIR-001 remains open. Implemented repeated-unchanged-write recovery and clearer budget feedback with four additional regression cases. Infrastructure: 57 passed, two Windows-only skips, two no-display Tk errors out of 61 tests. Real-model evaluation stopped before trials because Ollama is unavailable; no acceptance result exists for this version. Run the unchanged two-trial evaluation and the complete suite on the Windows desktop before closing this task. The later V1.2.0 increment implements independent UI work while keeping this acceptance gate open. See [current evidence](docs/evaluation-v1.1.1.json).

## V1.2.0 UI checkpoint — 2026-09-26

UI-001 implementation and 11 automated startup tests are complete. The event loop remains available during delayed hardware/model discovery; cancellation/close discard late results and errors permit retry. Full suite: 68 passed, two Windows-only skips, two no-display Tk errors (72 total). Native Windows slow/failed discovery and close smoke checks remain pending, so UI-001 stays unchecked. REPAIR-001 still awaits both real-model invoice trials. No release acceptance gate has been closed. See [current evidence](docs/evaluation-v1.2.0.json).

## V1.3.0 indexing checkpoint — 2026-09-26

INDEX-001's scoped acceptance is met by reproduced rooted-ignore/relative-import failures, bounded fixes and representative regression coverage. Ten new cases passed; 40 focused checks passed. A Git comparison matches the 12 supported fixture scenarios; full Git/import semantics are not claimed. Full suite: 78 passed, two Windows-only skips, two no-display Tk errors (82 total). See [evidence](docs/evaluation-v1.3.0.json).

User explicitly deferred their testing while development continues. Leave UI-001 native acceptance, UI-002 and REPAIR-001 pending, without blocking independent work. Next independent item is RESOURCE-001: repeatable pressure/telemetry measurement with clearly labeled simulated versus actual evidence. No release gate is waived.

## V1.4.0 Windows checkpoint

Imported V1.3.0 passed 80 tests with two symlink skips on Windows. The combined V1.4.0 suite passed 83 with the same two skips, including native Tk construction/startup and real junction tests. Three actual host snapshots were collected with no induced workload; low-RAM/recovery behavior is simulated separately. RESOURCE-001 remains open for a repeatable inference workload and measured pressure; no hard-cap or OOM protection is claimed. Manual UI-001/UI-002 and real-model REPAIR-001 remain pending. See [evidence](docs/evaluation-v1.4.0.json).

## Measured workload checkpoint - 2026-09-27

RESOURCE-001: normal real-model workload measured using 42 snapshots; RAM stayed above the backoff threshold. Physical low-memory validation remains open. Both unchanged invoice trials failed despite preserving original tests/validation/README. Next priority is REPAIR-001: diagnose repeated selection of the already-modified invoice file while the line-item defect remains. Preserve the failed runs and unchanged evaluation; do not widen resource controls without evidence. See docs/evaluation-v1.4.0-workload.json.

## V1.4.1 recovery checkpoint - 2026-09-27

V1.4.1 removes stale initial source/memory excerpts from repeated-failure recovery while retaining the goal, system policy, current bounded file evidence and explicitly stale last-test output. The strengthened regression fails before the fix and passes after it. Seven focused tests passed; full Windows suite: 83 passed, two symlink skips (85 total). Compilation passed. Both unchanged 7B invoice trials failed at the step limit (111.51 and 51.03 seconds). Trial one changed line_items.py and test_invoice.py, failing fixture trust; trial two changed only line_items.py, preserving tests/validation/README but leaving invoice arithmetic incorrect. REPAIR-001 remains open; no model-reliability improvement is established. Evidence: docs/evaluation-v1.4.1.json.

## V1.4.2 checkpoint - 2026-09-28

V1.4.2 passed four consecutive unchanged invoice trials on the exact final source, plus all four calculator/no-change cases. Every invoice trial preserved tests, validation and README, changed only invoice.py and line_items.py, and passed independent assertions. Full Windows suite: 88 passed, two symlink skips (90 total). Evidence and source/model/evaluator hashes: docs/evaluation-v1.4.2.json. This closes the narrow REPAIR-001 fixture milestone, not broad coding reliability.

## V1.4.3 checkpoint - 2026-09-28

V1.4.3 prevents same-timestamp checkpoint collisions using atomic standard-library directory creation. The forced-clock regression fails on V1.4.2 and passes after the fix, including independent rollback. Final Windows suite: 89 passed, two skips (91 total). Both unchanged invoice trials and all four calculator/no-change cases passed independent checks on the exact V1.4.3 source; invoice tests, validation and README remained intact. See docs/evaluation-v1.4.3.json.

## V1.5.0 setup checkpoint - 2026-09-28

The existing launcher helper now checks Python/Tk and default Ollama model discovery without starting a server or inference. Six new failure/readiness regressions pass; full suite: 95 passed, two symlink skips (97 total). A fresh source copy works with the existing host server and no bundled runtime/models. DIST-001 remains open for a clean computer and disposable real task. Latest real-model evidence remains V1.4.3; no new reliability claim.

## V1.6.0 text-repair checkpoint - 2026-09-28

- [x] EVAL-002 - Non-arithmetic multi-file fixture. Depends: EVAL-001. Unicode casefold normalization and first-seen deduplication use the existing bounded runner/approval checks. Two real 7B trials passed with original tests, validation and README preserved, changing only normalization.py and catalog.py. Both independent partial-fix checks fail until the two repairs are present. See docs/evaluation-v1.6.0.json. This is a constrained, explicitly guided fixture, not broad reliability acceptance.

Infrastructure: 99 passed, two symlink skips (101 total). No production agent behavior, dependencies or resource/permission boundaries changed. Next: complete pending manual UI/accessibility and clean-machine acceptance before adding more architecture. Broader user-project evaluation remains open.

## V1.7.0 desktop checkpoint

V1.7.0 adds keyboard navigation and compact model settings. Tab/Shift+Tab leave the request field without editing it; Ctrl+Enter runs through the existing task action, Esc requests Stop, and Ctrl+L focuses the project field. Ctrl+Tab/Ctrl+Shift+Tab cycle output tabs. Full Windows suite: 102 passed, two symlink skips (104 total). No dependencies or agent/approval changes. Manual screen-reader, full scaling and approval/recovery journeys remain pending. UI-002 remains open for manual acceptance.

## V1.7.1 cleanup verification

V1.7.1 repairs native test teardown: close through App.close, release UI references and collect cycles on the main thread before later worker tests. Ten sequential UI/history repetitions passed (240 tests), followed by the full suite: 102 passed, two symlink skips (104 total). No Tk teardown diagnostics appeared in those runs. Production behavior, existing timeouts and dependencies are unchanged. Latest real-model evidence remains V1.6.0; manual accessibility and clean-machine acceptance remain open.

A GC-disabled probe showed a plain destroyed window released its variable immediately, while a real Agent approval callback retained it through an App/Agent cycle. Main-thread collection released the cycle. Weak-reference teardown assertions now verify release in native task and keyboard tests. This reproduces retention and removes the observed cleanup diagnostics; the exact historical Python 3.12 scheduling failure was not deterministically reproduced locally. Hosted CI remains an additional check, not proof that all timing failures are impossible.

## V1.8.0 configured setup check

V1.8.0 extends the existing read-only setup check with --endpoint, --backend and --model. It discovers local OpenAI-compatible model IDs through /v1/models, checks an exact requested ID, and rejects unknown backends and remote endpoints. No server start, download, inference or settings write occurs in check mode. Full suite: 108 passed, two symlink skips (110 total). Actual Ollama discovery and a loopback compatible HTTP fixture passed; no real compatible-runtime inference is claimed. Manual accessibility, clean-machine and physical-pressure gates remain open. Six new automated cases cover ID matching, option restrictions, configuration forwarding, malformed/oversized responses and backend validation. Existing local-only proxy/redirect controls are reused.

## V1.9.0 compatible inference checkpoint

V1.9.0 forwards the existing state-dependent response schema to local OpenAI-compatible chat requests. The evaluator now accepts --backend and --endpoint while retaining the original Ollama defaults and restricted fixture approvals. Full suite: 111 passed, two Windows symlink skips (113 total). Before the fix, one compatible tag trial passed and one failed. After the fix, both compatible tag trials, both compatible invoice trials passed independent checks. Native Ollama tag regression had one failure and one success, preserving tests, validation and README. See docs/evaluation-v1.9.0.json for all results and exact hashes. Compatible inference was tested through local Ollama only; other implementations, general coding reliability and clean-machine acceptance remain unverified.

Cleanup completed with explicit user approval on 2026-09-30. Rejected candidate code, tests, version metadata and launcher restored to V1.9.0. Candidate backup and all evaluation evidence preserved. Earlier pending-cleanup notices are historical; no cleanup approval remains outstanding.

## V1.9.1 diagnostics checkpoint

V1.9.1 is an evaluator diagnostics patch, not a repair-loop improvement. Restricted invoice/tag results now distinguish independent checks that passed, failed, or did not run because the fixture was untrusted. Approval denials and final trust failures carry concrete reasons. Boolean approval, fixed AST variants, fixture goals, independent assertions and pass criteria are unchanged. Full suite: 113 passed, two Windows symlink skips (115 total). Fresh native tag trials: 2 of two passed; exact outcomes and hashes are in docs/evaluation-v1.9.1.json. Production agent behavior is unchanged; intermittent repair reliability remains open.

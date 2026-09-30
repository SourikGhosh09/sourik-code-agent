# Implementation roadmap

Current release: **V1.9.2 preview**, reviewed 2026-09-30. Full Windows suite: **114 passed, two symlink skips (116 total)**. V1.9.2 passed four native tag, two invoice and two compatible tag trials after correcting the reproduced obsolete-diff trigger; broader reliability remains unaccepted. V1.9.0 compatible tag/invoice trials passed through local Ollama only. Other compatible servers, broad reliability, manual accessibility, clean-machine setup and physical memory-pressure acceptance remain open.

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

## Current next action

- [x] REPAIR-002 - V1.9.2 reconstructed-state comparison reproduced obsolete-diff interference; focused fix, regression and eight full fixture trials passed. Scope is this trigger, not universal repair reliability.
- [x] EVAL-002 - V1.9.1 rejection diagnostics and independent-check status. Approval rules and pass criteria unchanged; tests prove untrusted code is not executed.
- [x] Candidate cleanup - Rejected recovery code removed with explicit approval; backup and all evidence preserved. No approval remains pending.

V1.9.2 final-source trials passed; prior intermittent failures remain recorded. Narrow REPAIR-001 invoice acceptance does not close REPAIR-002 or general coding reliability. See [handover](HANDOVER.md), [current evidence](docs/evaluation-v1.9.1.json), [candidate evidence](docs/evaluation-v1.9.1-candidates.json) and PROJECT_LOG.txt for dated history. User-deferred manual testing remains pending without blocking independent development.


Next: broader representative real-project acceptance, plus the independent manual/clean-machine/physical-pressure gates above.

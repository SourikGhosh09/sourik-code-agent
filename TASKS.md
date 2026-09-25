# Implementation roadmap

Statuses follow code/evidence, not roadmap promises. References: [PRD](docs/PRD.md), [testing](docs/TEST_PLAN.md), original specification precedence.

## Foundation and preview

- [x] BASE-001 - Local desktop task loop. Depends: none. Ref: R01-R03,R07,R08, [architecture](docs/ARCHITECTURE.md). Acceptance: bounded tools, approval, revision verification and recovery. Tests: regressions and recorded V0 calculator cases.
- [x] V1-001 - Repository evidence, memory and profiles. Depends: BASE-001. Ref: R04-R05, [data](docs/DATA_MODEL.md). Acceptance: preview behavior/limits documented. Tests: V1 regressions/indexed repair; full resource control remains incomplete.
- [x] SIM-001 - Minimal-change policy. Depends: V1-001. Ref: R06, [simplicity](docs/SIMPLICITY.md). Acceptance: inspection/gates/diff preserve permissions/tests. Tests: 13 policy tests, four real-model cases.
- [x] DOC-001 - Current documentation pack. Depends: SIM-001. Ref: [README](README.md). Acceptance: requested files match source and preserve specs. Tests: references, inventory and diff review.

## Next V1 work

- [x] EVAL-001 - One representative multi-file Python repair fixture. Depends: SIM-001. Ref: R02,R06. Acceptance: independent assertions, original tests, source/model hashes and edit/dependency observations. Tests: fixture validation and repeated model runs; no broad claims from one case.
- [ ] UI-001 - Nonblocking startup discovery. Depends: BASE-001. Ref: R07, [UI](docs/UI_SPEC.md). Acceptance: responsive window with slow/failed discovery and safe close. Tests: delayed/failing discovery and manual launch/close.
- [ ] UI-002 - Keyboard/screen-reader journey validation. Depends: UI-001. Ref: R07,F01-F05. Acceptance: record focus/labels/scaling/approval/recovery and repair demonstrated barriers. Tests: manual matrix and focused regressions.
- [ ] INDEX-001 - Representative ignore/import fixture. Depends: V1-001. Ref: R01. Acceptance: reproduce limitation, smallest justified fix. Tests: ranking/ignore boundaries without weaker secret protection.
- [ ] RESOURCE-001 - Repeatable pressure measurement. Depends: V1-001. Ref: R05. Acceptance: record RAM/VRAM behavior before changes; no hard-cap claim. Tests: simulated telemetry and measured run.

- [ ] REPAIR-001 - Improve action-format validation and repeated-patch recovery. Depends: EVAL-001. Ref: R02, [multi-file evidence](docs/evaluation-multifile.json). Acceptance: reject incomplete tool actions clearly, preserve current failure context, rerun the same two invoice trials without weakening fixture/tests/permissions. Tests: focused regression plus repeated real-model evaluation. Initial EVAL-001 result was one pass and one failure; reliability is not accepted.

## Security and distribution

- [ ] SEC-001 - Select bounded OS-isolation approach. Depends: EVAL-001. Ref: R03, [security](SECURITY.md). Acceptance: ADR compares threat boundary/compatibility/cost; no implementation claim before boundary tests. Tests: proof-of-concept escape/permission checks after decision.
- [ ] DIST-001 - Clean-machine source setup. Depends: DOC-001. Ref: [deployment](docs/operations/DEPLOYMENT.md). Acceptance: setup works without original machine files. Tests: fresh checkout launch, regressions and disposable task.
- [ ] RELEASE-001 - Distribution/license and release gates. Depends: EVAL-001,UI-002,DIST-001,SEC-001. Ref: [PRD](docs/PRD.md). Acceptance: owner-approved scope/support, reporting channel and evidence. Tests: exact-release acceptance rerun.

Plugins, advanced workers and training remain later original roadmap phases, not scheduled implementation. Do not build speculative managers/dependencies before concrete tasks.

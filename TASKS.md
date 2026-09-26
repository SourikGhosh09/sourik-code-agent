# Implementation roadmap

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
- [ ] RESOURCE-001 - Repeatable pressure measurement (V1.4.0 baseline sampler and simulated checks implemented; inference-load/pressure measurement pending). Depends: V1-001. Ref: R05. Acceptance: record RAM/VRAM behavior before changes; no hard-cap claim. Tests: simulated telemetry and measured run.

- [ ] REPAIR-001 - Improve action-format validation and repeated-patch recovery. Depends: EVAL-001. Ref: R02, [multi-file evidence](docs/evaluation-multifile.json). Acceptance: reject incomplete tool actions clearly, preserve current failure context, rerun the same two invoice trials without weakening fixture/tests/permissions. Tests: focused regression plus repeated real-model evaluation. Initial EVAL-001 result was one pass and one failure; reliability is not accepted. V1.1.0 adds required-field/no-op checks and retains failing-command evidence, but the broader repeated-reasoning issue remains open pending consistent model acceptance.

## Security and distribution

- [ ] SEC-001 - Select bounded OS-isolation approach. Depends: EVAL-001. Ref: R03, [security](SECURITY.md). Acceptance: ADR compares threat boundary/compatibility/cost; no implementation claim before boundary tests. Tests: proof-of-concept escape/permission checks after decision.
- [ ] DIST-001 - Clean-machine source setup. Depends: DOC-001. Ref: [deployment](docs/operations/DEPLOYMENT.md). Acceptance: setup works without original machine files. Tests: fresh checkout launch, regressions and disposable task.
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

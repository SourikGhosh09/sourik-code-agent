# Feature inventory

IDs refer to [PRD](PRD.md) and [flows](USER_FLOWS.md). P0 is essential current use; P1 is a V1 improvement.

| Feature/status | Value, priority, requirement/flow | Acceptance, edges and testing | Dependencies |
|---|---|---|---|
| Inspection/current | Relevant context; P0; R01/F01,F02 | Bound scans, reject linked/outside paths, handle empty/unreadable files; index/boundary tests | Tools, context |
| Plan/edit/test/repair/current | Finish tasks; P0; R02/F02 | Failed or zero tests cannot verify; edits invalidate verification; limits/cancel terminate; scripted plus independent real-model tests | Model, Tools, Store |
| Approval/recovery/current | Control and undo; P0; R03/F02,F04 | Denial prevents execution; later edits require conflict confirmation; crash/rollback tests | OS, checkpoints |
| History/memory/preview | Reuse evidence; P1; R04/F03 | Goal reuse starts fresh; stale fingerprints excluded; blank notes rejected; persistence/add/forget tests | SQLite, context |
| Model/resource settings/partial | Fit hardware; P1; R05,R08/F01,F05 | Validate targets, choose installed model, back off low RAM; adapter/profile tests; no hard caps | Runtime, telemetry |
| Simplicity/current heuristics | Avoid excess; P1; R06/F02 | Inspect unread targets, flag deps/layers/growth, allow justification, never budget-block test commands; 13 tests and no-change model case | Existing map/tools/diff |
| Desktop feedback/preview | Understand work; P0; R07/F01-F05 | Show progress/errors and exact approval args; Tk tests; full accessibility journey pending | Tk |

Post-MVP: multi-file acceptance (R02), nonblocking discovery (R07), richer pressure handling (R05), fuller ignore/import behavior (R01), stronger isolation (R03). See [tasks](../TASKS.md). Later/optional roadmap: plugin installation, advanced workers and training; no interfaces or delivery dates are committed. No cloud/billing/authentication feature is implied.

V1.1.1 repair increment (R02/R06): repeated unchanged writes trigger current-file recovery; successful verification clears stale failure evidence. Budget messages identify estimates as counts, not remaining work, and keep explanations in JSON. Inspection/testing remain available after a budget gate. Four new scripted regressions cover these paths, bounded stopping and verification preservation. Model-level improvement is unverified; REPAIR-001 stays open.

V1.2.0 desktop feedback (R07/F01,F02,F05): background hardware/model discovery, visible Preparing state, duplicate-run prevention, startup Stop, safe close/discard of late results and error/retry. Settings are captured for the current run; later edits remain for future work. Eleven automated tests pass, but native Windows smoke checks remain pending (UI-001 partial acceptance). This is separate from the open REPAIR-001 real-model gate.

V1.3.0 repository inspection (R01/INDEX-001): representative rooted/nested ignore and relative-import cases are implemented and covered by 10 new regression tests. Scope includes a documented gitignore subset, actual Python module/package candidates, ordinary src/ layouts, cache refresh and unchanged hard secret/link protections. Full language/Git semantics and cross-platform/model acceptance are not claimed. User testing is deferred; RESOURCE-001 is the next independent development item.

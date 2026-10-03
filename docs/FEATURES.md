# Feature inventory

Documentation reviewed 2026-10-03 against V1.11.0. [Current status](../HANDOVER.md) governs present acceptance; dated checkpoints below are historical evidence.

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

Implemented preview increments include background discovery, scoped ignore/import handling and narrow invoice/tag acceptance. Remaining: broad multi-file reliability (R02), manual desktop acceptance (R07), physical-pressure handling (R05), fuller ignore/import semantics (R01), stronger isolation (R03). See [tasks](../TASKS.md). Later/optional roadmap: plugin installation, advanced workers and training; no interfaces or delivery dates are committed. No cloud/billing/authentication feature is implied.

V1.1.1 repair increment (R02/R06): repeated unchanged writes trigger current-file recovery; successful verification clears stale failure evidence. Budget messages identify estimates as counts, not remaining work, and keep explanations in JSON. Inspection/testing remain available after a budget gate. Four new scripted regressions cover these paths, bounded stopping and verification preservation. Model-level improvement is unverified; REPAIR-001 stays open.

V1.2.0 desktop feedback (R07/F01,F02,F05): background hardware/model discovery, visible Preparing state, duplicate-run prevention, startup Stop, safe close/discard of late results and error/retry. Settings are captured for the current run; later edits remain for future work. Eleven automated tests pass, but native Windows smoke checks remain pending (UI-001 partial acceptance). This is separate from the open REPAIR-001 real-model gate.

V1.3.0 repository inspection (R01/INDEX-001): representative rooted/nested ignore and relative-import cases are implemented and covered by 10 new regression tests. Scope includes a documented gitignore subset, actual Python module/package candidates, ordinary src/ layouts, cache refresh and unchanged hard secret/link protections. Full language/Git semantics and cross-platform/model acceptance are not claimed. User testing is deferred; RESOURCE-001 is the next independent development item.

V1.4.1 recovery correction (R02): repeated-failure recovery now keeps the original task and system policy but drops original inspection/memory excerpts before supplying fresh bounded file evidence. The last failed command remains explicitly marked potentially stale until retested. Approval and verification rules are unchanged. Scripted regression checks both the retained goal/current code and absence of the obsolete arithmetic expression.

V1.4.2 (R02/R06): current-source prompts after edits/failed checks, explicit not-executed feedback for withheld actions and a verified finish action address repeated repairs and completion loops. Task diff review and all verification/approval gates remain. These changes do not enforce arbitrary natural-language file-preservation rules as an OS boundary.

V1.9.0: local compatible generation now forwards the existing state schema; evaluator backend/endpoint options allow testing configured loopback runtimes. Narrow real Ollama compatible-protocol tag/invoice acceptance is recorded in evaluation-v1.9.0.json. Other compatible servers and general reliability remain unaccepted; permission and resource boundaries are unchanged.

V1.9.1 evaluator diagnostics report the first failed trust condition and whether independent checks ran. This tooling does not change the production repair loop. Rejected recovery experiments were removed; intermittent native repair remains open. Latest suite and acceptance scope: [handover](../HANDOVER.md).

## V1.9.2 failed-check context

V1.9.2 removes obsolete diff text from failed-check model feedback while preserving current source, failure output and review metadata. Full diffs remain in recorded events, the Changes view and successful verification/final review. The new regression fails before the fix and passes after it. Full suite: 114 passed, two symlink skips (116 total). Four native tag trials, two native invoice trials and two compatible tag trials passed on the exact final source. This addresses the reproduced stale-patch trigger, not general repair reliability.

## Custom PC power — V1.10.0

V1.10.0 adds Custom AI power using the existing CPU-thread and context fields. Custom permits 1 through the detected logical CPU count and 2048–16384 context tokens; blanks use half the logical CPUs (at least one) and 8192 tokens. Other presets retain their caps. Speed caps context at 4096. Low-memory startup caps context at 4096; existing between-turn pressure backoff may lower targets to two threads and 2048 tokens. Custom retains one worker and 40 steps. These targets are forwarded to Ollama; compatible servers manage their own thread/context settings. No hard CPU, RAM or GPU limits or OS sandbox are provided. No dependencies, new settings keys or database migration.

Choose **Custom** in AI power to reveal Resource settings. Enter CPU threads and context tokens, then start a task. Settings are saved on successful startup; edits during a run apply to the next task. Selection opens the fields and moves keyboard focus to CPU threads.

## Audited UI — V1.11.0

V1.11.0 implements the audited desktop redesign: compact light workspace, clear project/priority/backend labels, visible recovery, readable results and a separate nonmodal Settings window. Custom focuses CPU threads; Back/Escape/close withdraw Settings without stopping work. Internal event/view names, saved keys, approvals and runtime controls are unchanged. No dependency or database migration. See [design and verification](UI_DESIGN.md).

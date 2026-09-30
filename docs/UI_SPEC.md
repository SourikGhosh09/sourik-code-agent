# Desktop UI specification

Documentation reviewed 2026-09-30 against V1.9.2. [Current status](../HANDOVER.md) governs present acceptance; dated checkpoints below are historical evidence.

Tk desktop, initially 1000x760 with 780x600 minimum. Product name is Sourik Code Agent; the window title shows Sourik Code Agent - V1.9.2 preview from the application version. No new visual branding or web/mobile interface is specified.

| Surface/flow | Purpose and controls | States and interactions |
|---|---|---|
| Main/F01,F02 | Project chooser/recents, goal, Run/Stop | Empty/idle, preparing, active task, cancelled startup, retryable error, completed result |
| Output/F02 | Progress, Changes, What changed?, Technical details | Empty before work, incremental events, bounded diff, readable result and inspectable errors |
| Settings/F05 | Power, Quality/Speed, collapsed backend/model/endpoint and CPU/context | Validate numeric targets, absent-runtime/model errors, apply future settings |
| Memory/F03 | Inspect/add note/forget | Empty list valid, blank note rejected, evidence inspectable, delete selected entry |
| History/F03 | Select earlier goal | Empty valid; selection loads goal, new Run required; no execution resumption |
| Approval/recovery/F02,F04 | Exact command/directory; separate conflict confirmation | Deny/cancel grants no authority; explicit later-edit conflicts |

Keep primary actions clear, advanced settings disclosed, failures understandable and technical details accessible. Show command scope. Labels/focus must support keyboard use and must not rely only on color. Validate input before work and preserve useful context on errors.

Task work and hardware/model discovery use workers and the existing event queue. During discovery the window stays available, duplicate Run is disabled, Stop cancels the pending handoff and close cancels timers/discards late results. Error dialogs restore Run for retry. UI inputs are captured before discovery; later edits are for the next request. Project history/database access, preferences and initial agent setup remain synchronous. Model loading can take time; Stop is not immediate during a model request. Desktop resizing is supported; mobile behavior is out of scope. Tk construction and selected failure states are tested, but screen-reader, focus order, scaling and full keyboard approval/recovery journeys remain manual validation in [tasks](../TASKS.md).

V1.2.0 has 11 automated startup checks, including a display-free Tcl event-loop check with paused discovery. Later native layout/navigation tests were added in V1.7.0 and teardown checks in V1.7.1. Full manual Windows keyboard/screen-reader/scaling journeys remain pending.

## V1.7.0 keyboard controls

| Keys | Action |
|---|---|
| Tab / Shift+Tab in request | Move to next / previous control without editing text |
| Ctrl+Enter | Run through existing validation and duplicate-task guards |
| Esc | Request Stop; existing cancellation timing applies |
| Ctrl+L | Focus the project field |
| Ctrl+Tab / Ctrl+Shift+Tab in output | Select next / previous tab |

Run/Stop buttons show their shortcuts. Native dialogs retain their own keyboard handling; shortcuts never approve commands or recovery. Model/server fields use separate expanding rows beneath Auto model/backend.

Native tests check horizontal settings/control fit at 780x600 with Tk scaling 2.0. Output-tab keyboard tests use 1000x900 so panes are visible at that scale. Full vertical fit at every scale, screen-reader support and manual approval/recovery journeys remain unvalidated. UI-002 remains open.

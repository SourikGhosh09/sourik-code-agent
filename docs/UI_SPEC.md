# Desktop UI specification

Tk desktop, initially 1000x760 with 780x600 minimum. Product name is Sourik Code Agent; the window title shows Sourik Code Agent - V1.4.1 preview from the application version. No new visual branding or web/mobile interface is specified.

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

V1.2.0 has 11 automated startup checks, including a display-free Tcl event-loop check with paused discovery. Full native Tk layout/interaction tests and manual Windows keyboard/screen-reader/scale journeys remain pending. Existing controls/layout are retained.

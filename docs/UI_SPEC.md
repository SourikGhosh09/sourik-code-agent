# Desktop UI specification

Tk desktop, initially 1000x760 with 780x600 minimum. Product name is Sourik Code Agent; the current window title still says Local Coding Agent - V1 preview. No new visual branding or web/mobile interface is specified.

| Surface/flow | Purpose and controls | States and interactions |
|---|---|---|
| Main/F01,F02 | Project chooser/recents, goal, Run/Stop | Empty/idle, active task, cancel, readable error, completed result |
| Output/F02 | Progress, Changes, What changed?, Technical details | Empty before work, incremental events, bounded diff, readable result and inspectable errors |
| Settings/F05 | Power, Quality/Speed, collapsed backend/model/endpoint and CPU/context | Validate numeric targets, absent-runtime/model errors, apply future settings |
| Memory/F03 | Inspect/add note/forget | Empty list valid, blank note rejected, evidence inspectable, delete selected entry |
| History/F03 | Select earlier goal | Empty valid; selection loads goal, new Run required; no execution resumption |
| Approval/recovery/F02,F04 | Exact command/directory; separate conflict confirmation | Deny/cancel grants no authority; explicit later-edit conflicts |

Keep primary actions clear, advanced settings disclosed, failures understandable and technical details accessible. Show command scope. Labels/focus must support keyboard use and must not rely only on color. Validate input before work and preserve useful context on errors.

Task work uses a worker/event queue; startup discovery can still block. Model loading can take time; Stop is not immediate during a model request. Desktop resizing is supported; mobile behavior is out of scope. Tk construction and selected failure states are tested, but screen-reader, focus order, scaling and full keyboard approval/recovery journeys remain manual validation in [tasks](../TASKS.md).

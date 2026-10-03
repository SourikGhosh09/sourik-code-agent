# Product requirements

Documentation reviewed 2026-10-03 against V1.10.0. [Current status](../HANDOVER.md) governs present acceptance; dated checkpoints below are historical evidence.

Current-state specification, reviewed 2026-09-30 for V1.9.1. Original requirements remain under specs/ with precedence defined by [the master](../specs/00_MASTER_PROJECT_PACK.txt). Status follows repository code and evidence.

## Vision, users and scope

Build an owned local Codex-like agent. Users need natural-language goals turned into verified changes without managing every edit, while understanding permissions and recovery. Primary users are the owner and non-programmers seeking approachable help; developers can inspect details. No commercial accounts, billing or hosted collaboration product is specified.

Goals: useful autonomy, understandable progress, replaceable local models, safe recovery and resource-aware operation. Minimum necessary change must never reduce correctness, security, validation, accessibility, data integrity, useful tests, compatibility or requested functionality.

| ID | Requirement and acceptance | Current scope |
|---|---|---|
| R01 | Select project and nonempty goal; inspect bounded repository evidence before planning | Implemented |
| R02 | Plan, implement, test, diagnose, repair and retest within limits; reject completion without current-revision verification | Implemented; narrow model evidence |
| R03 | Approve each command; guard direct file paths; checkpoint changes and confirm recovery conflicts | Implemented; no OS isolation |
| R04 | Keep local history and inspectable/removable notes; exclude stale verified evidence from reuse | V1 preview |
| R05 | Offer power/quality preferences, validate targets, choose installed models and back off future requests on low RAM | Partial resource control |
| R06 | Prefer no change/reuse/native facilities/small edits; justify flagged growth/dependencies/abstractions; review task diff | Implemented heuristics |
| R07 | Show progress, changes, readable results and technical errors; Stop requests cancellation | Preview; pending HTTP call can take 120 seconds |
| R08 | Keep inference local and model interface replaceable without paid APIs | Local adapters implemented |

## Quality, rules and phases

Use bounded scans/context, one worker per app instance, explicit errors and redacted logs. Command approval is not OS isolation. SQLite/checkpoints may contain private material and require local access protection. Keyboard/screen-reader accessibility is required quality but awaits full validation. No hard resource or latency guarantees exist.

MVP/V0 covers small-project creation/repair with tests, permissions, history and recovery. V1 adds repository evidence, memory, preferences and simplicity checks. Background discovery and scoped ignore/import indexing are implemented. Remaining work includes broader acceptance, fuller indexing and isolation. Plugins, advanced workers and trained models are later roadmap phases. Web hosting, accounts and mobile clients are out of current scope.

Success requires meaningful verification of requested behavior without weakened tests or bypassed approval. Four calculator cases establish a narrow slice, not broad reliability/efficiency. Assumption: local Windows desktop is the initial target. Open: benchmark projects, OS/hardware matrix, packaging/license, isolation mechanism and later plugin trust. Documentation templates do not require new application features.

V1.1.1 checkpoint (2026-09-26): R02/R06 gain repeated-unchanged-write recovery and clarified budget handling. Acceptance is still pending real-model trials and desktop validation; infrastructure coverage is not a reliability claim. No scope or architecture expansion.

V1.2.0 checkpoint (2026-09-26): R07 startup hardware/model discovery runs off-thread with cancellation/error handling. Settings snapshot isolation keeps the current request stable. Automated startup coverage is complete; native desktop acceptance and real-model REPAIR-001 evidence are still pending. No paid/cloud service or new dependency was introduced.

V1.3.0 checkpoint (2026-09-26): R01 gains a documented ignore-pattern subset and static local Python import candidate ranking under existing scan/context bounds. INDEX-001's representative fixture acceptance is met. At the user's request, Windows/UI/model acceptance is deferred while independent development continues; release status remains preview.

## Custom PC power — V1.10.0

V1.10.0 adds Custom AI power using the existing CPU-thread and context fields. Custom permits 1 through the detected logical CPU count and 2048–16384 context tokens; blanks use half the logical CPUs (at least one) and 8192 tokens. Other presets retain their caps. Speed caps context at 4096. Low-memory startup caps context at 4096; existing between-turn pressure backoff may lower targets to two threads and 2048 tokens. Custom retains one worker and 40 steps. These targets are forwarded to Ollama; compatible servers manage their own thread/context settings. No hard CPU, RAM or GPU limits or OS sandbox are provided. No dependencies, new settings keys or database migration.

Choose **Custom** in AI power to reveal Resource settings. Enter CPU threads and context tokens, then start a task. Settings are saved on successful startup; edits during a run apply to the next task. Selection opens the fields and moves keyboard focus to CPU threads.

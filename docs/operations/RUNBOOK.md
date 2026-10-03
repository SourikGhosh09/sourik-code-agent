# Operations runbook

Documentation reviewed 2026-10-03 against V1.11.0. [Current status](../../HANDOVER.md) governs present acceptance; dated checkpoints below are historical evidence.

Diagnose on disposable copies. Do not approve unfamiliar commands merely to clear errors.

| Symptom | Procedure |
|---|---|
| App unavailable | Run python -m local_agent from checkout to see error; verify Python/Tk and local runtime/model. Fresh clones lack portable runtime files. |
| Model/API error | Verify loopback server, installed model and UI backend/endpoint. Inspect error; do not disable localhost checks or expose server publicly. |
| Slow startup | Hardware/model discovery runs in a background worker with Preparing status. Check runtime readiness and error details; Stop discards the late startup result. History/preferences/database operations can still be synchronous. |
| Slow inference/pressure | Run one task; choose Eco/Speed or smaller targets/model. Backoff affects later requests, does not unload weights or guarantee no OOM. |
| Task/test failure | Inspect details/diff, preserve original tests, verify behavior independently, diagnose before a narrower retry. Failure is not verified success. |
| Delayed Stop | Pending model call can take 120 seconds; child termination is best effort. Inspect work before restart; avoid another project writer. |
| Database locked/corrupt | Close all project app instances. Back up project and full .agent/ including WAL before diagnosis. Restore consistent backup, not deletion to hide errors. |
| Interrupted/unwanted edits | Inspect checkpoint/diff, copy project, use recovery. Later conflicts need separate confirmation. External effects are outside recovery. |
| Failed source update | Close app, preserve state, restore known Git revision, run tests and disposable smoke task. No installer/migration service exists. |
| Bad configuration | Correct UI settings; if editing preferences manually, close app and back up first. |
| Secret exposure | Stop sharing artifacts, identify affected credential without posting it, rotate with issuer and inspect history. Redaction is not guaranteed. |

Account authentication, hosted APIs, scheduled jobs and versioned migrations do not exist, so those incident procedures do not apply. Approved commands use OS rights. Backups, private storage and human command review remain needed. See [security](../../SECURITY.md).

## V1.2.0 startup troubleshooting

Preparing means hardware/model discovery is running in the background. Stop discards the result once the current check returns; closing during preparation exits without launching a task later. If discovery fails, inspect the error, confirm the local server/model settings and press Run again. The Windows launcher may wait for its portable server before opening the UI; that separate helper is unchanged. Source ZIPs contain no runtime/models. A frozen project-history/database operation is outside this discovery fix and should be reported separately.

For resource diagnosis, run `python scripts/measure_resources.py --samples 3 --interval 1 --output evaluation-results/resource-baseline.json` with a new output filename. Compare actual snapshots separately from simulated policy checks. No model or stress workload is started; do not infer CPU utilization or hard-cap guarantees from configured targets.

## Evaluation failures

V1.9.1 invoice/tag results include approval_denials, final_trust_reasons and independent_check_status. not_run_untrusted_fixture means assertions were not executed; it does not prove incorrect output. untrusted_ast identifies code outside the deliberately fixed original/repaired variants. Preserve the result and inspect source statically; do not widen approval or execute rejected code to clear the failure. Even passed trials establish only narrow fixture evidence. See [test plan](../TEST_PLAN.md) and [current status](../../HANDOVER.md).

## Custom PC power — V1.10.0

V1.10.0 adds Custom AI power using the existing CPU-thread and context fields. Custom permits 1 through the detected logical CPU count and 2048–16384 context tokens; blanks use half the logical CPUs (at least one) and 8192 tokens. Other presets retain their caps. Speed caps context at 4096. Low-memory startup caps context at 4096; existing between-turn pressure backoff may lower targets to two threads and 2048 tokens. Custom retains one worker and 40 steps. These targets are forwarded to Ollama; compatible servers manage their own thread/context settings. No hard CPU, RAM or GPU limits or OS sandbox are provided. No dependencies, new settings keys or database migration.

Choose **Custom** in AI power to reveal Resource settings. Enter CPU threads and context tokens, then start a task. Settings are saved on successful startup; edits during a run apply to the next task. Selection opens the fields and moves keyboard focus to CPU threads.

## Audited UI — V1.11.0

V1.11.0 implements the audited desktop redesign: compact light workspace, clear project/priority/backend labels, visible recovery, readable results and a separate nonmodal Settings window. Custom focuses CPU threads; Back/Escape/close withdraw Settings without stopping work. Internal event/view names, saved keys, approvals and runtime controls are unchanged. No dependency or database migration. See [design and verification](../UI_DESIGN.md).

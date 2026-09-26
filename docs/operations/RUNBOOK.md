# Operations runbook

Diagnose on disposable copies. Do not approve unfamiliar commands merely to clear errors.

| Symptom | Procedure |
|---|---|
| App unavailable | Run python -m local_agent from checkout to see error; verify Python/Tk and local runtime/model. Fresh clones lack portable runtime files. |
| Model/API error | Verify loopback server, installed model and UI backend/endpoint. Inspect error; do not disable localhost checks or expose server publicly. |
| Slow startup | Discovery currently runs synchronously. Wait for return and check runtime readiness; nonblocking discovery remains pending. |
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

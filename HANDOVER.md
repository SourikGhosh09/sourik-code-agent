# Current handover

Current version: V1.4.0 preview. Imported the user-supplied V1.3.0 archive into the existing Git checkout, preserving its improvements. The unfinished earlier local V1.1.1 diff is retained in ignored .runtime/before-v1.3.0-import.patch. Only the current version launcher is retained; Start Agent.cmd opens Start V1.4.0.cmd.

New work: scripts/measure_resources.py provides bounded read-only snapshots using existing telemetry/backoff functions, with a separate deterministic low-memory/recovery sequence. It needs no model, induces no stress, refuses output overwrite and changes no production policy. No dependencies or migrations.

Validation: imported V1.3.0 Windows baseline: 80 passed, two symlink skips. Final V1.4.0: 83 passed, two symlink skips (85 total); native Tk/startup and junction checks passed. Compilation passed. Three actual host snapshots recorded available RAM around 6.50-6.66 GiB and NVIDIA GPU readings; no actual low-memory backoff. See docs/evaluation-v1.4.0.json. Simulated pressure is not real workload evidence.

Latest measurement (2026-09-27): 42 real host snapshots during two unchanged invoice trials; available RAM 4.793-7.543 GiB and GPU free memory 6,663-11,761 MiB. No sampled low-memory threshold crossing. Both trials failed at step limits (102.45/94.79 seconds), changed only invoice.py and preserved tests/validation/README. Evidence: docs/evaluation-v1.4.0-workload.json. The CI path-alias fix 743320f passed hosted CI.

Next priority: REPAIR-001, diagnose repeated patch selection that leaves the line-item defect unresolved. RESOURCE-001 normal load measurement is done, but actual low-memory validation remains open. Manual startup/accessibility remains pending. No production changes or version bump in this evidence-only stage; no new acceptance or hard-cap guarantee.

Read current source, PROJECT_LOG and original specs before changes; use the smallest correct solution. Preserve command approvals, local data and source specs. Runtime/models/raw outputs remain excluded from Git. Permanent decisions go in docs/DECISIONS. Publication target is the existing private GitHub repository.

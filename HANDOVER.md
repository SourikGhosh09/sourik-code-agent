# Current handover

Current version: V1.4.0 preview. Imported the user-supplied V1.3.0 archive into the existing Git checkout, preserving its improvements. The unfinished earlier local V1.1.1 diff is retained in ignored .runtime/before-v1.3.0-import.patch. Only the current version launcher is retained; Start Agent.cmd opens Start V1.4.0.cmd.

New work: scripts/measure_resources.py provides bounded read-only snapshots using existing telemetry/backoff functions, with a separate deterministic low-memory/recovery sequence. It needs no model, induces no stress, refuses output overwrite and changes no production policy. No dependencies or migrations.

Validation: imported V1.3.0 Windows baseline: 80 passed, two symlink skips. Final V1.4.0: 83 passed, two symlink skips (85 total); native Tk/startup and junction checks passed. Compilation passed. Three actual host snapshots recorded available RAM around 6.50-6.66 GiB and NVIDIA GPU readings; no actual low-memory backoff. See docs/evaluation-v1.4.0.json. Simulated pressure is not real workload evidence.

Next: RESOURCE-001 remains open for repeatable inference-load/physical-pressure measurement; manual startup/accessibility and real-model invoice acceptance remain pending. Historical failures are preserved. No full release, OOM safety, hard CPU/RAM/VRAM cap or model-quality improvement is claimed.

Read current source, PROJECT_LOG and original specs before changes; use the smallest correct solution. Preserve command approvals, local data and source specs. Runtime/models/raw outputs remain excluded from Git. Permanent decisions go in docs/DECISIONS. Publication target is the existing private GitHub repository.

# V1 preview: available for comparison

Validated on 2026-09-19. This is the first testable V1 increment, not full phase-2 acceptance or a broad coding benchmark. The preserved V0 remains available independently.

## What is implemented

- Task-ranked repository map with persistent hash-based parsing cache, Python symbol/import metadata, basic JS/TS symbol/import extraction and dependency manifests. Deleted entries are removed on refresh.
- Project memory UI for user notes and attributable verified-task memories. Changed scanned file evidence excludes old verified memories from the prompt. Records are removable; V0 records are preserved separately.
- Quality/Speed preference, optional thread/context targets and periodic available-RAM backoff between model calls. These are runtime targets, not OS-enforced caps.
- Recent projects, inspectable task history and loading a prior request into a fresh task.
- Durable after-change fingerprints, conflict detection and explicit confirmation before recovery overwrites later edits.
- Separate Start V0.cmd and Start V1.cmd launchers. Start Agent.cmd starts V1.

## Evidence

38 automated tests ran: **37 passed, 1 skipped** because Windows denied symbolic-link fixture creation. Real junction boundary tests passed. Tests cover incremental indexing, ranking a relevant file beyond the original 100-file cutoff, deleted entries, stale memory, redaction, V0 database migration, viewing history without interrupting a task, integrated RAM backoff, desktop memory/history interactions and recovery conflicts, plus the existing V0 regression suite.

Real local-model evaluation used **qwen2.5-coder:7b**, with independent assertions outside the model's tests:

| Case | Result |
|---|---|
| Empty project, Eco envelope | Created calculator and tests; completed; independent checks passed |
| Broken project, Balanced envelope | Observed failed tests, repaired source, preserved original tests; independent checks passed |
| Repository with 110 unrelated files and stale verified memory, Balanced envelope | Found and repaired calculator bug; preserved original tests; independent checks passed |

Exact source hash, model digest, timings and runtime envelopes: [evaluation-v1.json](evaluation-v1.json). Original evidence: evaluation-results/20260919-233606. Full local logs: .runtime/evaluation-v1.log and .runtime/regression-v1.log. V0's ten Python source files were compared byte-for-byte against the archive of commit 462a311.

Desktop controls were exercised through Tk tests. A full manual GUI session has not been claimed. The calculator evaluations do not establish broad repository, language or framework reliability; the clutter case tests retrieval in a small synthetic repository, not large-project engineering.

## Comparing versions

Use Start V0.cmd and Start V1.cmd with separate copies of a small project. Do not run both against the same folder. For a speed comparison, run sequentially because both use the same local model server. Auto + Quality is recommended in V1; Speed and Eco may select the less reliable 3B model.

The V0 snapshot lives under releases/v0-462a311 and is excluded from Git. It is reproducible from local Git commit 462a311 using git archive. Local runtime and models are shared; neither launcher changes system model settings.

## Remaining V1 work

Per-project resource overrides, nonblocking hardware/model startup, richer memory editing and error/fix retrieval, fuller ignore/import semantics, broader multi-file/language evaluation, and GPU-pressure handling remain unfinished. CPU/context controls and RAM backoff do not enforce RAM/VRAM limits or prevent every OOM. Commands require approval and run with the user's Windows rights; there is no OS sandbox. Plugin installation, multi-agent workers and training remain later roadmap phases.

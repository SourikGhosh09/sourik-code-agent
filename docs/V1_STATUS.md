# V1 preview status

Current release: **V1.9.1 preview**, reviewed 2026-09-30. Full Windows suite: **113 passed, two symlink skips (115 total)**. Both V1.9.1 native tag trials passed; intermittent native repair remains unresolved. V1.9.0 compatible tag/invoice trials passed through local Ollama only. Other compatible servers, broad reliability, manual accessibility, clean-machine setup and physical memory-pressure acceptance remain open.

Use Start Agent.cmd or Start V1.9.1.cmd. Old V0/V1 launchers and local release copies were removed; historical source remains in Git. See [handover](../HANDOVER.md), [changelog](../CHANGELOG.md) and [latest evidence](evaluation-v1.9.1.json).

## Historical first V1 increment (2026-09-19)

The following describes that earlier snapshot, not current launcher availability or current test totals.

## What is implemented

- Task-ranked repository map with persistent hash-based parsing cache, Python symbol/import metadata, basic JS/TS symbol/import extraction and dependency manifests. Deleted entries are removed on refresh.
- Project memory UI for user notes and attributable verified-task memories. Changed scanned file evidence excludes old verified memories from the prompt. Records are removable; V0 records are preserved separately.
- Quality/Speed preference, optional thread/context targets and periodic available-RAM backoff between model calls. These are runtime targets, not OS-enforced caps.
- Recent projects, inspectable task history and loading a prior request into a fresh task.
- Durable after-change fingerprints, conflict detection and explicit confirmation before recovery overwrites later edits.
- At that historical snapshot, separate V0/V1 launchers existed; current distribution uses only the versioned current launcher.

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

## Current remaining work

Background discovery and scoped ignore/import handling are implemented. Richer memory editing/error retrieval, fuller language semantics, physical RAM/VRAM pressure acceptance, manual accessibility, clean-machine distribution and stronger OS isolation remain unfinished. CPU/context targets and RAM backoff are not hard caps. Plugin installation, advanced workers and training are later roadmap phases. For comparisons, use historical Git revisions in separate disposable project copies and run sequentially against the local server.

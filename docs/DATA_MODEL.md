# Data model

Documentation reviewed 2026-10-03 against V1.11.0. [Current status](../HANDOVER.md) governs present acceptance; dated checkpoints below are historical evidence.

Source: local_agent/storage.py and checkpoint code in tools.py. Each project's .agent/state.sqlite uses SQLite WAL; this is the existing schema, not a proposed hosted database.

| Table | Columns and SQLite types | Keys/relationships |
|---|---|---|
| tasks | id TEXT, goal TEXT, state TEXT | id PRIMARY KEY; app-generated UUID hex |
| events | task TEXT, time REAL, kind TEXT, data TEXT | task logically references tasks.id; data JSON; time epoch seconds |
| memory | key TEXT, value TEXT | key PRIMARY KEY; legacy V0 store |
| repository_index | path TEXT, digest TEXT, data TEXT | path PRIMARY KEY; digest fingerprint; data JSON |
| memories_v1 | id TEXT, kind TEXT, value TEXT, task TEXT, evidence TEXT, created REAL | id PRIMARY KEY; logical task reference, empty for notes; evidence JSON; created epoch seconds |

No declared foreign keys, NOT NULL clauses, secondary indexes or soft-delete fields exist. SQLite TEXT primary keys alone do not imply NOT NULL. Application code supplies expected values; do not describe logical relations as enforced SQL constraints.

Validation: memory kind is note or verified_task; nonblank text required, redacted/truncated to 4,000 characters, latest 100 records retained. History returns latest 30 tasks by insertion order. Forget physically deletes. Verified evidence is compared with scanned file fingerprints; unsupported/unscanned files do not establish full-filesystem integrity.

Lifecycle: tasks start QUEUED and receive state events. Recovery opening marks unfinished tasks INTERRUPTED; history viewers avoid this mutation. Index replacement removes deleted paths. Legacy memories are preserved, not automatically promoted to verified V1 evidence. Schema initialization uses CREATE TABLE IF NOT EXISTS; no versioned migration system exists.

Other persisted data: checkpoint manifests/original bytes and expected-after hashes under project .agent/, project PROJECT_LOG.txt and app .agent/preferences.json. Checkpoints may contain private source even if display logs are redacted. Back up a closed app/project including metadata; see [runbook](operations/RUNBOOK.md). Formal migrations, retention and encryption remain open decisions.

V1.3.0: repository_index.digest includes a parser revision (`index-v2`, NUL separator, raw bytes) before hashing. Existing rows are re-described on the next scan and reused thereafter; no SQLite table migration is required. Python import strings retain relative dots and from-import candidates. Ignored files are removed alongside deleted files when the disposable index is replaced. Verified-memory evidence format is unchanged; a changed scan set can make earlier evidence stale without deleting notes/history.

V1.4.3 checkpoint folders retain a timestamp prefix and add an atomically generated unique suffix. Existing timestamp-only folders and manifests still load; no stored-data migration is required.

## Custom PC power — V1.10.0

V1.10.0 adds Custom AI power using the existing CPU-thread and context fields. Custom permits 1 through the detected logical CPU count and 2048–16384 context tokens; blanks use half the logical CPUs (at least one) and 8192 tokens. Other presets retain their caps. Speed caps context at 4096. Low-memory startup caps context at 4096; existing between-turn pressure backoff may lower targets to two threads and 2048 tokens. Custom retains one worker and 40 steps. These targets are forwarded to Ollama; compatible servers manage their own thread/context settings. No hard CPU, RAM or GPU limits or OS sandbox are provided. No dependencies, new settings keys or database migration.

Choose **Custom** in AI power to reveal Resource settings. Enter CPU threads and context tokens, then start a task. Settings are saved on successful startup; edits during a run apply to the next task. Selection opens the fields and moves keyboard focus to CPU threads.

## Audited UI — V1.11.0

V1.11.0 implements the audited desktop redesign: compact light workspace, clear project/priority/backend labels, visible recovery, readable results and a separate nonmodal Settings window. Custom focuses CPU threads; Back/Escape/close withdraw Settings without stopping work. Internal event/view names, saved keys, approvals and runtime controls are unchanged. No dependency or database migration. See [design and verification](UI_DESIGN.md).

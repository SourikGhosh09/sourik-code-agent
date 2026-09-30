# Data model

Documentation reviewed 2026-09-30 against V1.9.2. [Current status](../HANDOVER.md) governs present acceptance; dated checkpoints below are historical evidence.

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

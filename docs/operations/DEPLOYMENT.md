# Local deployment

Documentation reviewed 2026-10-03 against V1.11.0. [Current status](../../HANDOVER.md) governs present acceptance; dated checkpoints below are historical evidence.

Requires a desktop, Python >=3.12 with Tk, writable project storage and separately installed local model runtime/model. Windows is the verified preview environment. No provider, domain, HTTPS certificate, hosted database or background-job service is needed. Keep inference on loopback.

## Install and verify

1. Obtain source checkout or extract project ZIP.
2. Check python --version and python -m tkinter.
3. Install/start Ollama separately and install a suitable coding model. Recorded evaluations use qwen2.5-coder:7b; hardware/disk needs depend on model.
4. Run `python scripts/start_local_runtime.py --check` from the root. It reports Python/Tk, the optional portable runtime, and installed models on the default Ollama server. Exit 0 means these checks passed; exit 1 includes instructions for the missing requirements. It creates a hidden Tk window briefly but starts no model server/inference and saves no settings.
5. Run python -m unittest discover -v, then python -m local_agent from the root.
6. Use a disposable small project; verify command denial and inspect changes before valuable work.

No required environment values or third-party Python dependencies exist. Settings are in the UI and local .agent/preferences.json. SQLite tables initialize automatically in each project's .agent/. There is no versioned migration runner; back up before storage changes.

No packaged application build exists. python -m compileall -q local_agent scripts tests checks syntax only. Wheel/package installation is unvalidated; checkout execution is the supported preview path.

## Windows launchers

Start V1.11.0.cmd and Start Agent.cmd use an already-running server or the expected .runtime/ollama/ollama.exe installation. Git/ZIP exclude runtime/models. With a separately running server, use direct Python launch on fresh machines.

Only current V1 is retained locally. The obsolete V0 launcher and release copies have been removed; historical source and acceptance records remain in Git.

## Updates, backups and rollback

Close tasks/app before updates and backups. Preserve project source and entire project .agent/ plus app preferences if desired. Closing SQLite avoids inconsistent WAL copies. Update to reviewed source, run regressions, smoke-test a disposable project. Restore known source for app rollback; task checkpoints are separate and cannot undo arbitrary external effects. Do not blindly downgrade storage after future schema changes.

Monitor Progress/Technical details and local history. Model acceptance needs the separate restricted evaluation, not CI alone. License, signing, supported platforms and stronger isolation remain open.

## Readiness limitations

The setup check defaults to http://127.0.0.1:11434. V1.8.0 accepts --endpoint, --backend ollama|openai-compatible and --model in check mode. HTTP proxies and redirects remain disabled; only loopback HTTP is accepted. It does not read or change UI preferences. Enter the same configuration in Model settings yourself. Use a base URL without /v1; model IDs must match exactly. A model appearing in the installed list does not prove that it fits memory or can complete coding tasks. No software is installed automatically. If Ollama is unavailable, start your existing installation; if no model is installed, install a suitable model separately and repeat the check. See the UI settings for non-default endpoints.

V1.5.0 was checked from a fresh source copy on the existing Windows host without copying .runtime or models. Its existing server supplied model discovery. A genuinely clean computer, packaged installation and manual desktop journeys remain unvalidated; DIST-001 stays open.

V1.8.0 compatible discovery uses GET /v1/models, not chat generation. A server requiring authentication or lacking this endpoint can fail discovery; no credential support is added. Discovery was initially tested with a local HTTP fixture. Later V1.9.0 inference trials used Ollama's compatible API; other compatible implementations and a clean computer remain unvalidated.

V1.9.0 adds actual compatible inference evidence using the existing local Ollama server. Use the same endpoint/backend/model settings in the UI and evaluator; the evaluator does not change saved settings. Compatible servers must support JSON-schema response_format. No new runtime download, API key or dependency is required. Other server implementations and clean-machine acceptance remain open. See ../evaluation-v1.9.0.json.

## Custom PC power — V1.10.0

V1.10.0 adds Custom AI power using the existing CPU-thread and context fields. Custom permits 1 through the detected logical CPU count and 2048–16384 context tokens; blanks use half the logical CPUs (at least one) and 8192 tokens. Other presets retain their caps. Speed caps context at 4096. Low-memory startup caps context at 4096; existing between-turn pressure backoff may lower targets to two threads and 2048 tokens. Custom retains one worker and 40 steps. These targets are forwarded to Ollama; compatible servers manage their own thread/context settings. No hard CPU, RAM or GPU limits or OS sandbox are provided. No dependencies, new settings keys or database migration.

Choose **Custom** in AI power to reveal Resource settings. Enter CPU threads and context tokens, then start a task. Settings are saved on successful startup; edits during a run apply to the next task. Selection opens the fields and moves keyboard focus to CPU threads.

## Audited UI — V1.11.0

V1.11.0 implements the audited desktop redesign: compact light workspace, clear project/priority/backend labels, visible recovery, readable results and a separate nonmodal Settings window. Custom focuses CPU threads; Back/Escape/close withdraw Settings without stopping work. Internal event/view names, saved keys, approvals and runtime controls are unchanged. No dependency or database migration. See [design and verification](../UI_DESIGN.md).

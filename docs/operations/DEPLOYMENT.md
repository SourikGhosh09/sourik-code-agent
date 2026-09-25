# Local deployment

Requires a desktop, Python >=3.12 with Tk, writable project storage and separately installed local model runtime/model. Windows is the verified preview environment. No provider, domain, HTTPS certificate, hosted database or background-job service is needed. Keep inference on loopback.

## Install and verify

1. Obtain source checkout or extract project ZIP.
2. Check python --version and python -m tkinter.
3. Install/start Ollama separately and install a suitable coding model. Recorded evaluations use qwen2.5-coder:7b; hardware/disk needs depend on model.
4. Run python -m unittest discover -v, then python -m local_agent from the root.
5. Use a disposable small project; verify command denial and inspect changes before valuable work.

No required environment values or third-party Python dependencies exist. Settings are in the UI and local .agent/preferences.json. SQLite tables initialize automatically in each project's .agent/. There is no versioned migration runner; back up before storage changes.

No packaged application build exists. python -m compileall -q local_agent scripts tests checks syntax only. Wheel/package installation is unvalidated; checkout execution is the supported preview path.

## Windows launchers and V0

Start V1.cmd and Start Agent.cmd use an already-running server or the expected .runtime/ollama/ollama.exe installation. Git/ZIP exclude runtime/models. With a separately running server, use direct Python launch on fresh machines.

Start V0.cmd needs releases/v0-462a311, also excluded. With full Git history, generate that directory from git archive 462a311 and extract it there. Source ZIP lacks Git history; use the repository for this comparison. Run versions sequentially on separate copies of a project.

## Updates, backups and rollback

Close tasks/app before updates and backups. Preserve project source and entire project .agent/ plus app preferences if desired. Closing SQLite avoids inconsistent WAL copies. Update to reviewed source, run regressions, smoke-test a disposable project. Restore known source for app rollback; task checkpoints are separate and cannot undo arbitrary external effects. Do not blindly downgrade storage after future schema changes.

Monitor Progress/Technical details and local history. Model acceptance needs the separate restricted evaluation, not CI alone. License, signing, supported platforms and stronger isolation remain open.

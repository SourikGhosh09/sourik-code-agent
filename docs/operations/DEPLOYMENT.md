# Local deployment

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

Start V1.5.0.cmd and Start Agent.cmd use an already-running server or the expected .runtime/ollama/ollama.exe installation. Git/ZIP exclude runtime/models. With a separately running server, use direct Python launch on fresh machines.

Only current V1 is retained locally. The obsolete V0 launcher and release copies have been removed; historical source and acceptance records remain in Git.

## Updates, backups and rollback

Close tasks/app before updates and backups. Preserve project source and entire project .agent/ plus app preferences if desired. Closing SQLite avoids inconsistent WAL copies. Update to reviewed source, run regressions, smoke-test a disposable project. Restore known source for app rollback; task checkpoints are separate and cannot undo arbitrary external effects. Do not blindly downgrade storage after future schema changes.

Monitor Progress/Technical details and local history. Model acceptance needs the separate restricted evaluation, not CI alone. License, signing, supported platforms and stronger isolation remain open.

## Readiness limitations

The setup check targets http://127.0.0.1:11434 only, bypasses HTTP proxies and rejects redirects. It does not read UI preferences or validate custom OpenAI-compatible backends. A model appearing in the installed list does not prove that it fits memory or can complete coding tasks. No software is installed automatically. If Ollama is unavailable, start your existing installation; if no model is installed, install a suitable model separately and repeat the check. See the UI settings for non-default endpoints.

V1.5.0 was checked from a fresh source copy on the existing Windows host without copying .runtime or models. Its existing server supplied model discovery. A genuinely clean computer, packaged installation and manual desktop journeys remain unvalidated; DIST-001 stays open.

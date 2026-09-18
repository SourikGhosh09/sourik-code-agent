# Local Coding Agent — V0 development build

Double-click **Start Agent.cmd**. Choose or create a project folder, describe a small task, and click **Run task**. The app shows the plan, command results, changed files, and a plain-language project history. **Stop** cancels tools; an outstanding model request can take up to 120 seconds to return.

The model server must be running locally. The default connection is Ollama on port 11434; local OpenAI-compatible runtimes are also supported. No paid inference API is needed. If the workspace-local runtime has been downloaded, the launcher starts it automatically.

## Permissions and recovery

File tools reject paths outside the selected project, linked paths, model metadata, and common secret files. Each command asks for approval and runs with your operating-system permissions. **V0 is not an operating-system sandbox**: approved code can use the network or reach other files. Only approve commands for projects you trust. File edits receive recovery copies; the Changes tab shows a diff. Restore the current task or a saved checkpoint using the buttons below the task view. External command effects outside tracked project files cannot be undone by this app.

Project history is in `PROJECT_LOG.txt`. Task state, technical events, memory and checkpoints live in the project's `.agent` directory. Interrupted tasks are marked as interrupted when reopened; they are not silently resumed.

## Resource controls

Eco, Balanced and High change model thread targets, context size and step budget. Available-memory pressure reduces context. Model runtime settings are targets, not guaranteed OS-wide CPU/RAM/VRAM caps. V0 uses one worker. GPU model placement is delegated to Ollama; exact GPU caps, continuous pressure adaptation and automatic model switching remain future work. The OpenAI-compatible adapter cannot enforce Ollama-specific thread/context controls.

## Verification

Run `python -m unittest discover -v` for infrastructure tests. Scripted-model tests verify orchestration, including repair, but do not measure model intelligence. Real-model acceptance results are recorded separately in `evaluation-results`. Completion requires a successful verification command after the last edit; review test coverage because a passing command alone cannot prove every requested behavior.

Source requirements are preserved in `specs`. See `IMPLEMENTATION_PLAN.md` and `PROJECT_LOG.txt` for scope and current evidence. Advanced plugins, training, richer memory and distribution are later roadmap phases.

## Development verification limits

Repository scanning is bounded to 2,000 files, context mapping to 100 files, file writes to 200 KB, and individual checkpoint files to 2 MB. Root `.gitignore` patterns are supported conservatively; nested ignore files and negation patterns are not fully implemented. Use V0 on small projects. Secret filtering covers common paths and key/value patterns, not every possible secret format. Stop kills the direct process with best-effort child cleanup on Windows.

# Local Coding Agent - V1 preview

Double-click **Start V1.cmd** for the new preview or **Start V0.cmd** for the preserved, verified V0 build. **Start Agent.cmd** also starts the current V1 code. Both use the installed local Ollama runtime and models; no paid API is required. Python 3.12 or newer is required (3.14 is installed here).

For a fair comparison, use two separate copies of the same small project, one per version. Do not let both versions edit the same folder at once. They share the model server, so run tasks one after the other when comparing speed. Keep **Auto + Quality** in V1 for the recommended 7B model. Speed or Eco can select the less reliable 3B model.

## Try V1

1. Open or create a project folder and describe a small coding task.
2. Click Run task. Review each command approval; the app shows the project directory and exact arguments.
3. Review Progress, Changes and What changed? after the task finishes.
4. In Project memory, add a project note, inspect a saved verified result, or forget an entry.
5. In Task history, select an earlier request to load it as a new task. It starts with fresh inspection and a new checkpoint.

The first model request may take a minute while weights load. Stop cancels tools; a pending model request can take up to 120 seconds to return. Hardware/model discovery at startup can briefly block the window in this preview.

## What changed from V0

- Repository summaries are ranked against the task, with a persistent hash cache, Python imports/symbols, basic JavaScript/TypeScript symbols/imports, and dependency manifests.
- Verified task memories include their source task and file fingerprints. Changed evidence prevents automatic reuse. User notes remain visible and removable, and never grant permissions.
- Quality/Speed preference and optional CPU/context targets sit alongside AI power. RAM pressure is sampled between model requests, at most once per 15 seconds; low available RAM reduces subsequent context/thread targets.
- Recent projects and task history help return to work. Recovery checks saved fingerprints and asks separately before overwriting later edits.

## Permissions and limits

Commands require explicit approval and execute with your Windows permissions. **Neither version is an OS sandbox.** Approved programs may access files or the network outside the project. Recovery only covers tracked project files.

Repository scans are bounded to 2,000 files, the model map to 100 ranked entries / 12,000 characters, source indexing to 100 KB per file, writes to 200 KB, and checkpoint files to 2 MB. Root ignore rules are conservative; full nested/negation semantics are not implemented. JavaScript/TypeScript extraction is heuristic, not a language-server index. Hash caching saves parsing work; files are still read to check their content. Binary and unreadable files may be omitted.

Memory is local in the project's .agent/state.sqlite, capped at 100 V1 records. Verified memories compare scanned text-sized files up to 200 KB, not the entire filesystem. V0's legacy memory is preserved but not treated as verified V1 evidence. User notes may become stale; current files take precedence. This is not a guarantee against all secret formats or malicious repository text.

Resource settings are targets rather than exact CPU/RAM/VRAM caps. One worker runs per app instance. Speed prefers a smaller fitting installed model; Quality prefers the largest fitting model unless Eco is selected. RAM backoff only affects later requests, does not unload model weights, and is not a hard OOM guard. GPU telemetry is detected, but automatic GPU-pressure control remains unfinished. Ollama supports the thread/context targets; the OpenAI-compatible adapter does not enforce them.

## Verification and continuity

Run `python -m unittest discover -v` for infrastructure tests. Run `python scripts/evaluate_local.py qwen2.5-coder:7b` for the restricted calculator evaluations. That fixture's approval callback must never be used for arbitrary projects.

See [V1_STATUS.md](docs/V1_STATUS.md), [V0_STATUS.md](docs/V0_STATUS.md), and PROJECT_LOG.txt for exact evidence and remaining work. V0's source snapshot is generated from commit 462a311; runtime files and release copies remain excluded from Git. V1 is a preview, with broader phase-2 work still pending. Plugins and model training remain later roadmap phases.

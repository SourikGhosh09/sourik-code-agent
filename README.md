# Sourik Code Agent

Repository: https://github.com/SourikGhosh09/sourik-code-agent (private).

A local-first desktop coding agent that inspects projects, makes bounded changes, runs approved tests, and repairs failures.

Built for the owner and people seeking approachable coding assistance without mandatory paid inference APIs. Current status: **V1.4.0 preview**, with verified V0 calculator acceptance and a deterministic Simplicity Engine. This is not broad coding-reliability or production-security acceptance.

## Setup and commands

1. Install Python 3.12 or newer with Tk; check with `python -m tkinter`.
2. Install and run a local Ollama server and a suitable coding model. Recorded evaluations used `qwen2.5-coder:7b`; downloads are separate from this repository.
3. From the checkout run `python -m local_agent`.
4. Select a small project copy, enter a goal and review every command approval. Auto + Quality selects among installed models according to detected resources.

There are no third-party Python dependencies or required environment variables. The app does not load `.env`; configure it through the UI. No package installation is needed to run from the checkout. A distributable installer/build pipeline is not implemented.

```powershell
python -m local_agent
python -m unittest discover -v
python -m compileall -q local_agent scripts tests
python scripts/evaluate_local.py qwen2.5-coder:7b --simplicity
python scripts/evaluate_local.py qwen2.5-coder:7b --multifile
```

The evaluation commands need Ollama and the model. Their fixture-only approval callbacks must never be reused for arbitrary projects. Compilation checks syntax; it is not an installer build. CI runs infrastructure tests without downloading models and cannot certify model quality.

`Start V1.4.0.cmd` and `Start Agent.cmd` also support the original Windows machine's portable runtime under `.runtime/`. A fresh clone contains no runtime/models. Only the current V1 build is kept locally. The obsolete V0 launcher and release copies were removed; historical source remains in Git. See [deployment](docs/operations/DEPLOYMENT.md).

## Capabilities and limits

Implemented: project mapping, planning, guarded file tools, approved commands, test/repair loops, checkpoints, conflict-aware recovery, local history/memory, resource targets and minimal-change checks. V1.3.0 adds scoped ignore rules and more accurate local Python import context, while retaining background startup discovery. Current Windows validation: **83 passed, two symlink-fixture skips (85 total)**, including native Tk and junction checks. V1.4.0 adds read-only resource diagnostics using existing telemetry. Three actual host snapshots and a separate simulated low-memory sequence are recorded in [V1.4.0 evidence](docs/evaluation-v1.4.0.json). Actual RAM stayed above the backoff threshold; this is a baseline, not stress/inference acceptance. Manual accessibility and real-model checks remain pending.

Commands run with your OS rights: **there is no OS sandbox or network isolation**. Resource settings are targets, not hard CPU/RAM/VRAM caps. Scans/context are bounded; JS/TS indexing and simplicity checks are heuristic. Hardware/model discovery runs in the background; project history/database access and initial agent setup remain synchronous. Broader multi-file/language reliability, pressure handling, plugins and model training remain unfinished.

## Stack and layout

Confirmed stack: Python standard library, Tkinter, SQLite and local Ollama or OpenAI-compatible model endpoints. No web frontend, hosted backend, accounts or cloud database.

| Location | Purpose |
|---|---|
| `local_agent/` | Existing application package |
| `tests/`, `scripts/` | Regression tests, restricted evaluations, runtime helper |
| `specs/` | All 19 preserved original documents |
| `docs/` | Current specifications, decisions, operations, evidence |
| `src/.gitkeep` | Requested pack placeholder; not another application |
| `.agent/`, `.runtime/`, `evaluation-results/`, `releases/`, `dist/` | Local/generated data excluded from Git |

## Documentation index

- [PRD](docs/PRD.md), [features](docs/FEATURES.md), [flows](docs/USER_FLOWS.md), [UI](docs/UI_SPEC.md)
- [Architecture](docs/ARCHITECTURE.md), [data](docs/DATA_MODEL.md), [communication](docs/API_SPEC.md), [tests](docs/TEST_PLAN.md)
- [Security](SECURITY.md), [deployment](docs/operations/DEPLOYMENT.md), [runbook](docs/operations/RUNBOOK.md)
- [Desktop decision](docs/DECISIONS/001-local-desktop.md), [simplicity decision](docs/DECISIONS/002-deterministic-simplicity.md)
- [Tasks](TASKS.md), [handover](HANDOVER.md), [agent instructions](AGENTS.md), [changelog](CHANGELOG.md)
- [Simplicity details](docs/SIMPLICITY.md), [extension boundaries](docs/EXTENSIONS.md), [plan](IMPLEMENTATION_PLAN.md), [log](PROJECT_LOG.txt)
- Historical [V0](docs/V0_STATUS.md) and [V1](docs/V1_STATUS.md) reports describe their tested revisions.

## Rules, assumptions and questions

Original precedence remains in [the master pack](specs/00_MASTER_PROJECT_PACK.txt). Inspect current code; prefer the smallest correct change without weakening quality, permissions or tests. Preserve source specs and exclude local data/secrets from Git. Update PROJECT_LOG after meaningful work.

Assumption: Windows remains the primary preview target; other platforms need validation. Future ideas are not delivered features. Open: representative acceptance projects, supported hardware/OS, distribution/license and stronger OS isolation. Next: diagnose repeated patch selection in REPAIR-001. Normal inference load has been measured; low-memory pressure and manual desktop acceptance remain open.

## Version naming

Starting with **V1.1.0**, releases use MAJOR.MINOR.PATCH: major for breaking changes, minor for compatible features, patch for compatible fixes. Preview status remains explicit until broader acceptance. The application exposes local_agent.__version__; pyproject metadata must match it. Release tags use v1.1.0-style names; packaged source ZIPs include the version. Start Agent.cmd always opens the current version; the named launcher is Start V1.4.0.cmd. Historical V0/V1 labels remain in their original evidence.

## Updating to V1.4.0

1. Close the agent and extract this ZIP into a separate folder. Keep your current app folder, project folders and their `.agent` data. The ZIP contains source, not Ollama or models.
2. When you are ready to test later, start your existing Ollama server. Open PowerShell in the extracted project folder and run `python -m unittest discover -v`, then `python scripts/evaluate_local.py qwen2.5-coder:7b --multifile`. The second command creates two disposable invoice projects under `evaluation-results`; it does not modify your working projects.
3. Open `Start Agent.cmd` (or run `python -m local_agent`). Confirm the title says V1.4.0 preview and try a disposable project copy. Reuse your existing installed model; another model download is unnecessary if it is already installed.

Both invoice trials must finish with `passed: true` before accepting this repair milestone. If either fails, retain the generated results/events for diagnosis. The supplied source ZIP has been integrated into the existing Git repository for this update.

During startup, the status shows **Preparing**. Run is disabled until startup/task completion; Stop cancels task handoff after the current check returns. Closing during discovery exits the window without starting a task later. Changes you type into settings while preparing apply to the next run. If preparation fails, correct the settings and press Run again. There is no visual redesign in this increment.

Repository context now understands common rooted/nested ignore patterns and relative Python imports, helping it omit generated files and find the related local modules. Existing cached import metadata refreshes automatically. This is a documented subset, not complete Git or Python import resolution; see [architecture](docs/ARCHITECTURE.md). Direct file permissions and command approvals are unchanged.

## Resource baseline (V1.4.0)

```powershell
python scripts/measure_resources.py --samples 3 --interval 1 --power Balanced --output evaluation-results/resource-baseline.json
```

This read-only command needs no model. It samples existing host RAM/disk/NVIDIA telemetry and shows resource targets before/after the current backoff policy. Simulated low-memory checks are separately labeled and allocate no stress workload. Unknown readings remain null/empty rather than invented zeroes. The output path must be new; existing files are never overwritten. Sampling is bounded to 1-60 observations and intervals of 0-60 seconds. Detection itself can take time, so the interval is not a fixed sampling frequency. CPU utilization, temperature, process memory and hard caps are not measured. Raw reports stay under ignored evaluation-results/.

Latest real-model workload check (2026-09-27): 42 host snapshots stayed above the low-RAM threshold, but both invoice trials failed due to repeated edits with the second defect left unresolved. No model-reliability improvement is claimed. See [workload evidence](docs/evaluation-v1.4.0-workload.json).

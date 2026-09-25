# Sourik Code Agent

Repository: https://github.com/SourikGhosh09/sourik-code-agent (private).

A local-first desktop coding agent that inspects projects, makes bounded changes, runs approved tests, and repairs failures.

Built for the owner and people seeking approachable coding assistance without mandatory paid inference APIs. Current status: **V1 preview**, with verified V0 calculator acceptance and a deterministic Simplicity Engine. This is not broad coding-reliability or production-security acceptance.

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
```

The final command needs Ollama and the model. Its calculator-only approval callback must never be reused for arbitrary projects. Compilation checks syntax; it is not an installer build. CI runs infrastructure tests without downloading models and cannot certify model quality.

`Start V1.cmd` and `Start Agent.cmd` also support the original Windows machine's portable runtime under `.runtime/`. A fresh clone contains no runtime/models. `Start V0.cmd` additionally needs the generated `releases/v0-462a311` snapshot; see [deployment](docs/operations/DEPLOYMENT.md). Compare versions on separate project copies, sequentially, because they share the model server.

## Capabilities and limits

Implemented: project mapping, planning, guarded file tools, approved commands, test/repair loops, checkpoints, conflict-aware recovery, local history/memory, resource targets and minimal-change checks. Latest recorded evidence: 50 automated tests passed, one Windows symlink fixture skipped, and four real-model calculator cases passed. See [testing](docs/TEST_PLAN.md) and [evidence](docs/evaluation-simplicity.json).

Commands run with your OS rights: **there is no OS sandbox or network isolation**. Resource settings are targets, not hard CPU/RAM/VRAM caps. Scans/context are bounded; JS/TS indexing and simplicity checks are heuristic. Startup discovery can block the window. Broader multi-file/language reliability, pressure handling, plugins and model training remain unfinished.

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

Assumption: Windows remains the primary preview target; other platforms need validation. Future ideas are not delivered features. Open: representative acceptance projects, supported hardware/OS, distribution/license and stronger OS isolation. Next step: evaluate realistic multi-file projects before expanding architecture.

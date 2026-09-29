# Sourik Code Agent

Repository: https://github.com/SourikGhosh09/sourik-code-agent (private).

A local-first desktop coding agent that inspects projects, makes bounded changes, runs approved tests, and repairs failures.

Built for the owner and people seeking approachable coding assistance without mandatory paid inference APIs. Current status: **V1.9.0 preview**, with verified V0 calculator acceptance and a deterministic Simplicity Engine. This is not broad coding-reliability or production-security acceptance.

## Setup and commands

1. Install Python 3.12 or newer with Tk; check with `python -m tkinter`.
2. Install and run a local Ollama server and a suitable coding model. Recorded evaluations used `qwen2.5-coder:7b`; downloads are separate from this repository.
3. From the checkout run `python scripts/start_local_runtime.py --check`. Resolve any reported missing requirements, then run `python -m local_agent`.
4. Select a small project copy, enter a goal and review every command approval. Auto + Quality selects among installed models according to detected resources.

There are no third-party Python dependencies or required environment variables. The app does not load `.env`; configure it through the UI. No package installation is needed to run from the checkout. A distributable installer/build pipeline is not implemented.

```powershell
python -m local_agent
python -m unittest discover -v
python -m compileall -q local_agent scripts tests
python scripts/evaluate_local.py qwen2.5-coder:7b --simplicity
python scripts/evaluate_local.py qwen2.5-coder:7b --multifile
python scripts/evaluate_local.py qwen2.5-coder:7b --tags
```

The evaluation commands need Ollama and the model. Their fixture-only approval callbacks must never be reused for arbitrary projects. Compilation checks syntax; it is not an installer build. CI runs infrastructure tests without downloading models and cannot certify model quality.

`Start V1.9.0.cmd` and `Start Agent.cmd` also support the original Windows machine's portable runtime under `.runtime/`. A fresh clone contains no runtime/models. Only the current V1 build is kept locally. The obsolete V0 launcher and release copies were removed; historical source remains in Git. See [deployment](docs/operations/DEPLOYMENT.md).

## Capabilities and limits

Implemented: project mapping, planning, guarded file tools, approved commands, test/repair loops, checkpoints, conflict-aware recovery, local history/memory, resource targets and minimal-change checks. V1.3.0 adds scoped ignore rules and more accurate local Python import context, while retaining background startup discovery. Current Windows validation: **108 passed, two symlink-fixture skips (110 total)**, including native Tk and junction checks. V1.4.0 adds read-only resource diagnostics using existing telemetry. Three actual host snapshots and a separate simulated low-memory sequence are recorded in [V1.4.0 evidence](docs/evaluation-v1.4.0.json). Actual RAM stayed above the backoff threshold; this is a baseline, not stress/inference acceptance. Manual accessibility and broader real-model acceptance remain pending.

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

Assumption: Windows remains the primary preview target; other platforms need validation. Future ideas are not delivered features. Open: representative acceptance projects, supported hardware/OS, distribution/license and stronger OS isolation. Next: broader representative-task evaluation and pending manual UI checks. Normal inference load has been measured; low-memory pressure and manual desktop acceptance remain open.

## Version naming

Starting with **V1.1.0**, releases use MAJOR.MINOR.PATCH: major for breaking changes, minor for compatible features, patch for compatible fixes. Preview status remains explicit until broader acceptance. The application exposes local_agent.__version__; pyproject metadata must match it. Release tags use v1.1.0-style names; packaged source ZIPs include the version. Start Agent.cmd always opens the current version; the named launcher is Start V1.9.0.cmd. Historical V0/V1 labels remain in their original evidence.

## Updating to V1.9.0

1. Close the agent and extract this ZIP into a separate folder. Keep your current app folder, project folders and their `.agent` data. The ZIP contains source, not Ollama or models.
2. When you are ready to test later, start your existing Ollama server. Open PowerShell in the extracted project folder and run `python scripts/start_local_runtime.py --check`, then `python -m unittest discover -v`. The setup check explains any missing requirements.
3. Open `Start Agent.cmd` (or run `python -m local_agent`). Confirm the title says V1.9.0 preview and try a disposable project copy. Reuse your existing installed model; another model download is unnecessary if it is already installed.

To repeat the separate repair benchmark, run `python scripts/evaluate_local.py qwen2.5-coder:7b --multifile`. It creates two disposable invoice projects under `evaluation-results`. Both must report `passed: true`; retain results/events if either fails. Setup readiness alone does not establish coding reliability.

During startup, the status shows **Preparing**. Run is disabled until startup/task completion; Stop cancels task handoff after the current check returns. Closing during discovery exits the window without starting a task later. Changes you type into settings while preparing apply to the next run. If preparation fails, correct the settings and press Run again. There is no visual redesign in this increment.

Repository context now understands common rooted/nested ignore patterns and relative Python imports, helping it omit generated files and find the related local modules. Existing cached import metadata refreshes automatically. This is a documented subset, not complete Git or Python import resolution; see [architecture](docs/ARCHITECTURE.md). Direct file permissions and command approvals are unchanged.

## Resource baseline (V1.4.0)

```powershell
python scripts/measure_resources.py --samples 3 --interval 1 --power Balanced --output evaluation-results/resource-baseline.json
```

This read-only command needs no model. It samples existing host RAM/disk/NVIDIA telemetry and shows resource targets before/after the current backoff policy. Simulated low-memory checks are separately labeled and allocate no stress workload. Unknown readings remain null/empty rather than invented zeroes. The output path must be new; existing files are never overwritten. Sampling is bounded to 1-60 observations and intervals of 0-60 seconds. Detection itself can take time, so the interval is not a fixed sampling frequency. CPU utilization, temperature, process memory and hard caps are not measured. Raw reports stay under ignored evaluation-results/.

V1.4.0 real-model workload check (2026-09-27): 42 host snapshots stayed above the low-RAM threshold, but both invoice trials failed due to repeated edits with the second defect left unresolved. No model-reliability improvement is claimed. See [workload evidence](docs/evaluation-v1.4.0-workload.json).

V1.4.1 corrects stale source excerpts in repeated-failure recovery. Its 85-test suite passed with two skips, but both unchanged real-model invoice trials failed; one also altered a protected test file and failed fixture trust. Reliable multi-file repair remains unaccepted. See [V1.4.1 evidence](docs/evaluation-v1.4.1.json).

## V1.4.2 repair result

Four consecutive invoice trials on the final source passed, preserving original tests, validation and README and changing only the two source modules. All four calculator/no-change cases also passed independent checks. Existing-file estimates are reviewed at completion; edits trigger the prior verification command with fresh approval. Explicit Preserve ... tests clauses protect recognized existing tests from file-tool mutations. See [exact evidence and intermediate failures](docs/evaluation-v1.4.2.json) and [policy limits](docs/SIMPLICITY.md). This completes the narrow invoice milestone, not general coding reliability.

V1.4.3 added a Windows checkpoint-collision fix. Both invoice trials and all four calculator/no-change cases passed on that source. [Latest real-model evidence](docs/evaluation-v1.4.3.json).

## V1.5.0 setup check

Run `python scripts/start_local_runtime.py --check` to check Python, creation of a hidden Tk window, and model discovery at the default Ollama endpoint. Exit code 0 means these checks passed; 1 means setup needs attention. The command does not start a server, download models, run inference or save settings. A separately running Ollama server works without a portable runtime in the checkout. Custom UI endpoints/backends and coding quality are not evaluated.

The setup check and full suite also passed from a fresh source copy without bundled runtime/models on this Windows machine, using its existing server. This is not a clean-machine or manual accessibility acceptance. Agent/model behavior is unchanged; no new real-model evaluation was run for V1.5.0.

## V1.6.0 text-repair evaluation

The new `--tags` evaluation creates two disposable tag catalogs with Unicode normalization and stable deduplication defects. Both local 7B trials passed independent checks and preserved tests, validation and README while changing only the two source modules. Independent assertions also cover Unicode equivalence, input preservation, iterators, empty input and invalid tags. Exact source/model/evaluator hashes and outcomes are in [V1.6.0 evidence](docs/evaluation-v1.6.0.json).

This extends evaluation coverage; it adds no new production agent behavior. The fixture explicitly specifies the expected expression repairs, and automatic approval accepts only known original/fixed AST variants. It is a constrained repair demonstration, not unrestricted text-processing or general coding acceptance. Never use fixture approval callbacks on user projects. Manual UI/accessibility, genuinely clean-machine setup and physical-pressure validation remain open.

## V1.7.0 keyboard and settings update

V1.7.0 adds keyboard navigation and compact model settings. Tab/Shift+Tab leave the request field without editing it; Ctrl+Enter runs through the existing task action, Esc requests Stop, and Ctrl+L focuses the project field. Ctrl+Tab/Ctrl+Shift+Tab cycle output tabs. Full Windows suite: 102 passed, two symlink skips (104 total). No dependencies or agent/approval changes. Manual screen-reader, full scaling and approval/recovery journeys remain pending.

No new model trial was run for this UI-only increment; latest recorded model evidence remains V1.6.0. See [keyboard details](docs/UI_SPEC.md).

## V1.7.1 test-cleanup patch

V1.7.1 repairs native test teardown: close through App.close, release UI references and collect cycles on the main thread before later worker tests. Ten sequential UI/history repetitions passed (240 tests), followed by the full suite: 102 passed, two symlink skips (104 total). No Tk teardown diagnostics appeared in those runs. Production behavior, existing timeouts and dependencies are unchanged. Latest real-model evidence remains V1.6.0; manual accessibility and clean-machine acceptance remain open.

## V1.8.0 configured local-model checks

V1.8.0 extends the existing read-only setup check with --endpoint, --backend and --model. It discovers local OpenAI-compatible model IDs through /v1/models, checks an exact requested ID, and rejects unknown backends and remote endpoints. No server start, download, inference or settings write occurs in check mode. Full suite: 108 passed, two symlink skips (110 total). Actual Ollama discovery and a loopback compatible HTTP fixture passed; no real compatible-runtime inference is claimed.

```powershell
python scripts/start_local_runtime.py --check --endpoint http://127.0.0.1:11434 --backend ollama --model qwen2.5-coder:7b
python scripts/start_local_runtime.py --check --endpoint http://127.0.0.1:1234 --backend openai-compatible --model YOUR_MODEL_ID
```

Use the server base URL without `/v1` and an exact advertised ID. These options require `--check`; normal portable startup is unchanged. Copy the same configuration into the UI manually. Discovery does not prove memory fit or coding quality.

## V1.9.0 compatible inference

V1.9.0 forwards the existing state-dependent response schema to local OpenAI-compatible chat requests. The evaluator now accepts --backend and --endpoint while retaining the original Ollama defaults and restricted fixture approvals. Full suite: 111 passed, two Windows symlink skips (113 total). Before the fix, one compatible tag trial passed and one failed. After the fix, both compatible tag trials, both compatible invoice trials passed independent checks. Native Ollama tag regression had one failure and one success, preserving tests, validation and README. See docs/evaluation-v1.9.0.json for all results and exact hashes. Compatible inference was tested through local Ollama only; other implementations, general coding reliability and clean-machine acceptance remain unverified.

Repeat locally: `python scripts/evaluate_local.py qwen2.5-coder:7b --tags --backend openai-compatible --endpoint http://127.0.0.1:11434`. Use the server base URL without `/v1`. The server must support JSON-schema response_format; authentication and cloud endpoints are not supported.

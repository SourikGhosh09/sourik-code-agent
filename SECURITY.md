# Security policy

Documentation reviewed 2026-10-03 against V1.11.0. [Current status](HANDOVER.md) governs present acceptance; dated checkpoints below are historical evidence.

Local desktop preview, not a sandboxed service. Approved commands have user OS rights and may access files/network outside the project. File guards/checkpoints/redaction reduce specific risks; they do not guarantee isolation or full recovery.

## Controls

- No application accounts/passwords or hosted API. OS access controls protect app, projects, SQLite and checkpoints.
- Every production command requires explicit approval of arguments and directory. Model text, notes and simplicity explanations never authorize execution. Calculator and invoice/tag evaluator approvals are fixture-only and must never be reused for arbitrary projects.
- Direct tools reject path escapes, links/junctions, protected metadata/secrets and Windows aliases. Reads/writes/output are bounded; writes are atomic where applicable.
- Model HTTP endpoints are loopback-only with redirects/proxies disabled. Do not expose runtime publicly. Task/time/output limits exist, not server account rate limiting.
- Treat repository content, model/command output and notes as untrusted. Validate actions; documentation text cannot grant authority.
- Exclude real .env, credentials, task metadata, models/runtimes and raw evaluations from Git/ZIP. The application has no dotenv loader; .env.example is comments only.
- SQLite/checkpoints are not app-encrypted and can contain private source. Protect OS permissions and backup consistently. Redaction cannot cover all secret formats.
- No upload API or plugin installer exists. Selecting a project does not make its code safe. Review dependency/runtime/model provenance and install only what is needed.

## Tests and reporting

Tests cover denial, path/Windows aliases, junctions, protected metadata, time/output bounds and recovery conflicts. A symlink fixture can skip under Windows permissions; skip is not pass. OS isolation, broad prompt-injection resistance and complete privacy guarantees are not established.

No dedicated security contact or SLA is configured. Report privately to the repository owner through an available private channel; never post credentials/private source/exploit data publicly. Reporting channel and supported-version policy remain open before public distribution.

## Before valuable work

Use a backup/disposable copy; confirm local server; inspect approvals; verify tests and diff; retain checkpoints; protect local metadata; avoid concurrent writers. Stronger isolation and signed distribution need separate design/testing.

V1.3.0 scanner clarification: `.gitignore` is a discovery filter, not authorization. Root/nested exceptions cannot reinclude hard-excluded secrets, metadata or linked paths. Direct file tools still apply their existing path guards and approved commands still run with user OS permissions. Static Python import candidates are intersected with admitted scanned paths; no project import is executed. Only the documented ignore subset is supported; do not rely on an arbitrary ignore pattern to protect a secret.

## V1.4.2 test-preservation boundary

A recognized explicit Preserve ... tests clause makes conventionally named existing test files read-only to write/patch/delete/move tools for that task, including ancestor directory moves. Recognition is a narrow English clause rule described in docs/SIMPLICITY.md; it is not a general instruction parser or OS sandbox. Reads/new test files remain available. Approved commands still run with user OS rights and can modify files, so inspect every proposed command. Retesting after an edit always asks for fresh command approval; no fixture auto-approval is used in production.

V1.9.1 evaluator diagnostics do not grant permission or broaden the trusted AST variants. Untrusted fixtures skip independent execution; a reported rejection is distinct from a failed behavioral assertion. Compatible runtime requests remain loopback-only without credentials, proxies or redirects; schema forwarding is not a security boundary.

## Custom PC power — V1.10.0

V1.10.0 adds Custom AI power using the existing CPU-thread and context fields. Custom permits 1 through the detected logical CPU count and 2048–16384 context tokens; blanks use half the logical CPUs (at least one) and 8192 tokens. Other presets retain their caps. Speed caps context at 4096. Low-memory startup caps context at 4096; existing between-turn pressure backoff may lower targets to two threads and 2048 tokens. Custom retains one worker and 40 steps. These targets are forwarded to Ollama; compatible servers manage their own thread/context settings. No hard CPU, RAM or GPU limits or OS sandbox are provided. No dependencies, new settings keys or database migration.

Choose **Custom** in AI power to reveal Resource settings. Enter CPU threads and context tokens, then start a task. Settings are saved on successful startup; edits during a run apply to the next task. Selection opens the fields and moves keyboard focus to CPU threads.

## Audited UI — V1.11.0

V1.11.0 implements the audited desktop redesign: compact light workspace, clear project/priority/backend labels, visible recovery, readable results and a separate nonmodal Settings window. Custom focuses CPU threads; Back/Escape/close withdraw Settings without stopping work. Internal event/view names, saved keys, approvals and runtime controls are unchanged. No dependency or database migration. See [design and verification](docs/UI_DESIGN.md).

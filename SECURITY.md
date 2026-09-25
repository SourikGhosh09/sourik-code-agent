# Security policy

Local desktop preview, not a sandboxed service. Approved commands have user OS rights and may access files/network outside the project. File guards/checkpoints/redaction reduce specific risks; they do not guarantee isolation or full recovery.

## Controls

- No application accounts/passwords or hosted API. OS access controls protect app, projects, SQLite and checkpoints.
- Every production command requires explicit approval of arguments and directory. Model text, notes and simplicity explanations never authorize execution. Calculator evaluator approval is fixture-only.
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

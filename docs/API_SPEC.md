# Communication contracts

Documentation reviewed 2026-10-03 against V1.10.0. [Current status](../HANDOVER.md) governs present acceptance; dated checkpoints below are historical evidence.

No application REST API, public server, accounts or hosted backend exists. The desktop calls Python objects and receives task events through a queue. SQLite is local. Do not invent pagination, filtering or role-based endpoints.

## Local model boundary

Model.generate(messages, config) returns a dict. LocalModel calls a loopback HTTP server; only localhost/127.0.0.1/::1 are allowed, redirects/proxies disabled. No API credential is required by the application. Access is local-machine access, not a remote user session.

| Backend/request | Purpose and shape |
|---|---|
| Ollama GET /api/tags and GET /api/ps | Discover installed/loaded models |
| Ollama POST /api/chat | Model, messages, JSON schema, nonstreaming generation and local thread/context options |
| Local OpenAI-compatible GET /v1/models | Discover advertised IDs from data[].id; five-second timeout, one-million-byte limit |
| Local OpenAI-compatible POST /v1/chat/completions | Model/messages and state JSON schema when supplied, otherwise JSON-object response; adapter does not enforce resource targets |

These endpoints belong to the runtime, not Sourik Code Agent. The adapter uses a 120-second timeout and bounded generation. HTTP/network failures and malformed/non-JSON output fail requests; provider status codes are not an app-specific HTTP error contract. One worker per instance and task limits apply, not server account rate limiting. Do not expose the server publicly to bypass localhost restrictions.

## Agent contract

contracts.response_schema narrows responses by state. Planning returns plan strings and a change budget with nonnegative file/new-file/dependency counts and a complexity explanation. Actions carry tool arguments and a reason. Flagged reconsideration requires a nonempty simplicity explanation. Legacy scripted/custom plans without budgets remain runtime-compatible.

Tool-specific path/content/patch/query or argv/timeout/verify fields are defined in contracts.py and tools.py. Successful tools produce bounded observations; errors are observations for diagnosis and cannot verify a task. Completion is available only after current-revision verification; later edits invalidate it. Over-budget completion may require justification. No justification bypasses approval or validation.

This internal schema is not a versioned public SDK. Before changing adapters or contracts, validate state/error behavior against [testing](TEST_PLAN.md) and keep the policy independent of model vendors.

V1.1.0: each tool has its own response-schema branch with required arguments. Runtime checks reject missing fields before simplicity checks or file actions. Existing tool-level argument/path/permission validation remains in place.

V1.1.1: after simplicity reconsideration, required explanation fields apply to mutation branches and completion, not list/read/search/run. Runtime installation gates still require justification before command approval. `unchanged` observations now include `last_failing_command` (text or null), a stale-evidence note and a retest/completion instruction. Repeated unchanged writes use existing recovery events and bounded current-file context; successful verification clears old command failures. No new persisted schema or public API was introduced.

V1.2.0 desktop-only event: `startup` carries captured root/goal/options, a local model object and either resource config or error text through the in-process queue. It is not a persisted agent event, a serializable public API, or a permission grant. The UI consumes it only while preparing and not closed; cancelled results cannot construct an Agent. Worker discovery never accesses Tk. Existing model HTTP contracts/timeouts and task command approval are unchanged.

V1.3.0 repository metadata: Python `imports` strings retain leading dots and imported-name candidates. The existing map/list/search operations observe scoped ignore rules; model actions and command permissions are unchanged. Cached import metadata is refreshed automatically through a parser-versioned fingerprint. No new endpoint or public API.

V1.4.2: after successful current-revision verification the model may return a finish action with reason, tool=finish, content (summary) and optional simplicity explanation. It is normalized to the existing done path, retaining verification and budget checks; legacy done responses remain supported. Failed checks refresh bounded current evidence immediately. Successful edits discard obsolete assistant attempts/excerpts from the next prompt; full diffs remain recorded and supplied at verification/review. No new tool permissions or storage format.

After an edit, the controller schedules the last verification action that actually ran (including a failing approved baseline). It requests command approval again through the existing Tools path and consumes a normal task step. With no previous verification action, no command is invented. Scheduled requests have controller_check events; model completion still requires current-revision verification and final review. Protected test paths are in-memory task state, not an SQLite migration.

V1.8.0 validates the backend name and adds read-only compatible model discovery. A malformed, oversized or missing data list fails clearly; each ID must be a nonblank string. Returned records expose name only and do not invent sizes or memory estimates. Ollama discovery and generation formats remain unchanged. Reference: [LM Studio compatible model discovery](https://lmstudio.ai/docs/developer/openai-compat/models). Local HTTP fixture validation does not establish real-provider inference support.

## V1.9.0 schema forwarding

The compatible adapter sends response_format.type=json_schema and json_schema={name: agent_response, schema: existing response_schema}. No schema is rewritten and no silent JSON-object fallback occurs on provider errors. Calls without response_schema retain json_object. Runtime validation, completion gates, approvals and loopback/proxy/redirect restrictions remain independent of server enforcement. The server must implement this schema format; tested with local Ollama only. See [Ollama structured outputs](https://docs.ollama.com/capabilities/structured-outputs). Compatible num_thread/num_ctx enforcement and authentication are not implemented.

## V1.9.1 evaluator reporting

Restricted invoice/tag results retain independent_pass and add independent_check_status: passed, failed or not_run_untrusted_fixture. approval_denials records first-failure reasons encountered during task commands; final_trust_reasons records the final fixture check. Optional reasons collection does not change approval Booleans. evaluation_approval_denied is emitted by the evaluator to its local output/events list, not injected into the model prompt or stored as a new production event contract. The pass expression, fixture contents and allowed variants are unchanged.

V1.9.2: nonzero-exit check feedback omits diff and diff_truncated from the model-facing simplicity review. Current file evidence, failing output, counts and findings remain. Recorded simplicity events and successful verification/final review retain full bounded diffs. This prevents obsolete removed lines from being reintroduced after the recovery context refresh. Permissions, evaluator approval and completion gates are unchanged.

## Custom PC power — V1.10.0

V1.10.0 adds Custom AI power using the existing CPU-thread and context fields. Custom permits 1 through the detected logical CPU count and 2048–16384 context tokens; blanks use half the logical CPUs (at least one) and 8192 tokens. Other presets retain their caps. Speed caps context at 4096. Low-memory startup caps context at 4096; existing between-turn pressure backoff may lower targets to two threads and 2048 tokens. Custom retains one worker and 40 steps. These targets are forwarded to Ollama; compatible servers manage their own thread/context settings. No hard CPU, RAM or GPU limits or OS sandbox are provided. No dependencies, new settings keys or database migration.

Choose **Custom** in AI power to reveal Resource settings. Enter CPU threads and context tokens, then start a task. Settings are saved on successful startup; edits during a run apply to the next task. Selection opens the fields and moves keyboard focus to CPU threads.

# Communication contracts

No application REST API, public server, accounts or hosted backend exists. The desktop calls Python objects and receives task events through a queue. SQLite is local. Do not invent pagination, filtering or role-based endpoints.

## Local model boundary

Model.generate(messages, config) returns a dict. LocalModel calls a loopback HTTP server; only localhost/127.0.0.1/::1 are allowed, redirects/proxies disabled. No API credential is required by the application. Access is local-machine access, not a remote user session.

| Backend/request | Purpose and shape |
|---|---|
| Ollama GET /api/tags and GET /api/ps | Discover installed/loaded models |
| Ollama POST /api/chat | Model, messages, JSON schema, nonstreaming generation and local thread/context options |
| Local OpenAI-compatible POST /v1/chat/completions | Model/messages and JSON-object response; adapter does not enforce resource targets |

These endpoints belong to the runtime, not Sourik Code Agent. The adapter uses a 120-second timeout and bounded generation. HTTP/network failures and malformed/non-JSON output fail requests; provider status codes are not an app-specific HTTP error contract. One worker per instance and task limits apply, not server account rate limiting. Do not expose the server publicly to bypass localhost restrictions.

## Agent contract

contracts.response_schema narrows responses by state. Planning returns plan strings and a change budget with nonnegative file/new-file/dependency counts and a complexity explanation. Actions carry tool arguments and a reason. Flagged reconsideration requires a nonempty simplicity explanation. Legacy scripted/custom plans without budgets remain runtime-compatible.

Tool-specific path/content/patch/query or argv/timeout/verify fields are defined in contracts.py and tools.py. Successful tools produce bounded observations; errors are observations for diagnosis and cannot verify a task. Completion is available only after current-revision verification; later edits invalidate it. Over-budget completion may require justification. No justification bypasses approval or validation.

This internal schema is not a versioned public SDK. Before changing adapters or contracts, validate state/error behavior against [testing](TEST_PLAN.md) and keep the policy independent of model vendors.

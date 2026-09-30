# 001 - Preserve the local desktop architecture

Documentation reviewed 2026-09-30 against V1.9.1. [Current status](../../HANDOVER.md) governs present acceptance; dated checkpoints below are historical evidence.

Status: Accepted; records current implementation. Date: 2026-09-25.

Context: The user wants an owned local agent without paid API requirements; Python/Tk/SQLite code already works.

Decision: Retain the single-process desktop, local_agent/ package, project storage and replaceable loopback model adapter. Runtime/models install separately. Add no hosted backend/accounts for this documentation pack.

Alternatives considered: cloud/browser architecture, external database, relocation to src/. They add cost without a current requirement.

Consequences: Low dependencies and local inference after setup. Packaging/cross-platform support need work. Approval is not OS isolation, which remains an open decision.

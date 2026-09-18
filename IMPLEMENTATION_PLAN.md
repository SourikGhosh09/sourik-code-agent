# V0 implementation and acceptance

The original 19 documents in specs are authoritative. This document records implementation decisions, not replacement requirements.

1. Python standard-library desktop application (Tk), SQLite task/events/memory persistence.
2. Model protocol with Ollama and local OpenAI-compatible adapters. No paid service required.
3. Project-scoped file tools, excluded secrets, checkpoint/diff/rollback, bounded command execution with explicit approval. Commands execute with the user's OS rights: this is a permission boundary, not an OS sandbox.
4. Bounded understand/inspect/plan/act/verify/repair loop. Completion requires a successful approved verification after the last edit.
5. Hardware-derived context/thread budgets, Eco/Balanced/High controls; exact memory/GPU caps are not claimed.
6. Native project picker, progress, stop, permission requests, changed files and recovery.
7. Unit/integration acceptance: empty project, broken project, failure, two resource profiles, traversal, secrets, rollback, cancellation. Scripted adapters test infrastructure only. Real local-model evaluations are separate release gates.

V1 and later: OS process isolation, advanced indexes, richer hardware monitoring, installed plugins, training and distribution. Extension contracts are defined now; no training capability is claimed for V0.

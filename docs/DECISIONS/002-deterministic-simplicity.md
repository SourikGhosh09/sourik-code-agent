# 002 - Deterministic simplicity using existing evidence

Documentation reviewed 2026-09-30 against V1.9.1. [Current status](../../HANDOVER.md) governs present acceptance; dated checkpoints below are historical evidence.

Status: Accepted; records current implementation. Date: 2026-09-25.

Context: Agents can duplicate code or add speculative layers; existing mapping/tools/checkpoints already provide useful evidence.

Decision: One lightweight model-independent module performs inspection, budget/justification checks and checkpoint-diff review. Prefer no change, reuse and modification before creation. Correctness/safety outrank size. Reuse the existing model for reasoning; add no model, dependency or Ponytail coupling.

Alternatives considered: copied external architecture, second critic model, plugin registry, semantic scoring, automatic deletion. None is justified by current evidence.

Consequences: Works without Git, includes new files and excludes pre-task edits. Heuristics and nonempty explanations do not prove necessity. Commands retain approval; semantic analysis and efficiency claims wait for representative evaluation. See [details](../SIMPLICITY.md).

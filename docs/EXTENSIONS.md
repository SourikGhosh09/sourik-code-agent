# Extension contracts (future milestones)

Documentation reviewed 2026-09-30 against V1.9.1. [Current status](../HANDOVER.md) governs present acceptance; dated checkpoints below are historical evidence.

Model: `generate(messages, config) -> dict`; the orchestrator validates actions and the tool runtime enforces permission decisions. Implement this protocol to integrate a user-trained model.

Skills: planned manifest fields `id`, `version`, `instructions`, `required_tools`, `compatibility`, `provenance`. Instructions are untrusted context, never authority to grant permissions.

Plugins: planned manifest fields `id`, `version`, `actions`, `input_schema`, `permissions`, `entrypoint`. The current V1.9.1 preview does not load executable plugins. A future isolated runtime must enforce permissions before activation.

Training: future dataset manifests include license, source, version, content hashes, and train/validation/evaluation split. Candidate promotion requires separate reproducible evaluations against the baseline. No training feature is implemented in the current preview.

Memory: V1 stores project notes and attributable verified results through Store.add_memory, memory_records and delete_memory, with add/inspect/forget controls in the desktop UI. Legacy remember/memories/forget APIs remain compatible. Current repository observations take precedence. Rich error/fix retrieval and in-place note editing remain future work.

Simplicity policy: implemented in local_agent/simplicity.py and called by the existing Agent. It consumes repository metadata and Tools, with no model-specific dependency. Future skills may supply contextual evidence through the existing context boundary; they cannot grant permissions or disable correctness requirements. No policy registry or executable plugin loader is added. See SIMPLICITY.md.

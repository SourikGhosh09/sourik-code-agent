# Extension contracts (future milestones)

Model: `generate(messages, config) -> dict`; the orchestrator validates actions and the tool runtime enforces permission decisions. Implement this protocol to integrate a user-trained model.

Skills: planned manifest fields `id`, `version`, `instructions`, `required_tools`, `compatibility`, `provenance`. Instructions are untrusted context, never authority to grant permissions.

Plugins: planned manifest fields `id`, `version`, `actions`, `input_schema`, `permissions`, `entrypoint`. V0 does not load executable plugins. A future isolated runtime must enforce permissions before activation.

Training: future dataset manifests include license, source, version, content hashes, and train/validation/evaluation split. Candidate promotion requires separate reproducible evaluations against the baseline. No training feature is implemented in V0.

Memory: SQLite stores editable/removable project facts through Store.remember, memories, forget. Current repository observations take precedence. Rich episodic retrieval and memory editing UI are future work.

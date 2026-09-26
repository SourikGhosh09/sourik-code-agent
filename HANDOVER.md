# Current handover

Current version: V1.1.0 preview, 2026-09-26. Version appears in app title, local_agent.__version__, package metadata and Start V1.1.0.cmd. Start Agent.cmd opens the current version. Use MAJOR.MINOR.PATCH naming from now on; historical evidence retains original labels.

Implemented: tool-specific required response fields, runtime rejection of incomplete/identical-text patches, and retained failing-command evidence during repeated-error recovery. No dependencies, architecture or permission changes. Full suite: 56 passed and one skipped Windows symlink fixture.

Acceptance warning: both final invoice real-model trials failed. The model repaired arithmetic but edited the protected-by-task README and repeated writes. The fixture correctly refused execution and the step budget stopped work. Tests/validation files remained intact; the combined preservation metric failed because README changed. Independent checks were not executed on untrusted fixture content. Exact evidence: docs/evaluation-v1.1.0.json. Earlier intermediate trial was one pass/one failure; no reliability improvement is established.

Next: continue REPAIR-001, diagnose budget-feedback confusion and repeated no-op writes with a bounded fix and unchanged evaluation. Do not expand architecture or weaken approval/tests to obtain a pass. UI responsiveness work follows reliability diagnosis.

Only current local app is retained; old V0 copies/launcher are removed. Runtime/models/task outputs are excluded from Git. Read repository/log/specs before changes and prefer the smallest correct solution. No OS sandbox or hard resource caps. Keep permanent decisions in docs/DECISIONS.

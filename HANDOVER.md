# Current handover

Current version: V1.7.0 preview. Start Agent.cmd opens Start V1.7.0.cmd.

V1.7.0 adds keyboard navigation and compact model settings. Tab/Shift+Tab leave the request field without editing it; Ctrl+Enter runs through the existing task action, Esc requests Stop, and Ctrl+L focuses the project field. Ctrl+Tab/Ctrl+Shift+Tab cycle output tabs. Full Windows suite: 102 passed, two symlink skips (104 total). No dependencies or agent/approval changes. Manual screen-reader, full scaling and approval/recovery journeys remain pending. Latest model evidence remains V1.6.0.

V1.6.0 adds the --tags real-model evaluation in scripts/evaluate_local.py. Both 7B trials repaired Unicode normalization and stable deduplication, preserving tests/validation/README and changing only two source modules. Full suite: 99 passed, two symlink skips (101 total). Source/model/evaluator hashes and original invoice regression results are in docs/evaluation-v1.6.0.json. Production agent behavior is unchanged; this is guided fixture evidence, not a new general-reliability claim.

V1.5.0 adds a read-only setup check in the existing runtime helper. Run python scripts/start_local_runtime.py --check for Python/Tk and default Ollama/model readiness. No server/model download, inference, settings migration or dependency was added. Full suite: 95 passed, two symlink skips (97 total). The check and tests passed from a fresh source copy using the existing Windows host/server; a truly clean machine remains untested. Agent behavior is unchanged; latest real-model evidence is V1.4.3, not a V1.5.0 trial.

Previous V1.4.2 passed four consecutive unchanged invoice trials on the exact final source, plus all four calculator/no-change cases. Every invoice trial preserved tests, validation and README, changed only invoice.py and line_items.py, and passed independent assertions. Full Windows suite: 88 passed, two symlink skips (90 total). Evidence and source/model/evaluator hashes: docs/evaluation-v1.4.2.json. This closes the narrow REPAIR-001 fixture milestone, not broad coding reliability.

V1.4.3 prevents same-timestamp checkpoint collisions using atomic standard-library directory creation. The forced-clock regression fails on V1.4.2 and passes after the fix, including independent rollback. Final Windows suite: 89 passed, two skips (91 total). Both unchanged invoice trials and all four calculator/no-change cases passed independent checks on the exact V1.4.3 source; invoice tests, validation and README remained intact. See docs/evaluation-v1.4.3.json.

Implemented: current-source context at repair/edit/verified review; compatible finish action through existing gates; freshly approved retesting using the prior verification command; existing-file estimate review at completion; file-tool protection for explicit Preserve ... tests clauses. No dependencies, new runtime module, storage migration or mandatory cloud service.

Next: complete UI-001/UI-002 manual startup/accessibility checks when the owner is ready, and validate genuinely clean-machine setup. The non-arithmetic tag fixture is now evaluated, but broader real user-project reliability remains unaccepted. Physical low-memory validation, clean-machine distribution and stronger OS isolation remain open. Normal resource workload was measured previously; no hard caps are claimed.

Several intermediate experiments failed, including one passing pair followed by failures; their outcomes are retained in the versioned report. The final acceptance uses two sequential passing invoice pairs on the same source, with calculator regression checks between them. Runtime/models/raw fixtures stay ignored; original specs/history remain preserved. Read PROJECT_LOG and source before further changes.

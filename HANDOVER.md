# Current handover

Current version: V1.4.3 preview. Start Agent.cmd opens Start V1.4.3.cmd.

Previous V1.4.2 passed four consecutive unchanged invoice trials on the exact final source, plus all four calculator/no-change cases. Every invoice trial preserved tests, validation and README, changed only invoice.py and line_items.py, and passed independent assertions. Full Windows suite: 88 passed, two symlink skips (90 total). Evidence and source/model/evaluator hashes: docs/evaluation-v1.4.2.json. This closes the narrow REPAIR-001 fixture milestone, not broad coding reliability.

V1.4.3 prevents same-timestamp checkpoint collisions using atomic standard-library directory creation. The forced-clock regression fails on V1.4.2 and passes after the fix, including independent rollback. Final Windows suite: 89 passed, two skips (91 total). Both unchanged invoice trials and all four calculator/no-change cases passed independent checks on the exact V1.4.3 source; invoice tests, validation and README remained intact. See docs/evaluation-v1.4.3.json.

Implemented: current-source context at repair/edit/verified review; compatible finish action through existing gates; freshly approved retesting using the prior verification command; existing-file estimate review at completion; file-tool protection for explicit Preserve ... tests clauses. No dependencies, new runtime module, storage migration or mandatory cloud service.

Next: evaluate a different representative task before expanding reliability claims, and complete UI-001/UI-002 manual startup/accessibility checks when the owner is ready. Physical low-memory validation, clean-machine distribution and stronger OS isolation remain open. Normal resource workload was measured previously; no hard caps are claimed.

Several intermediate experiments failed, including one passing pair followed by failures; their outcomes are retained in the versioned report. The final acceptance uses two sequential passing invoice pairs on the same source, with calculator regression checks between them. Runtime/models/raw fixtures stay ignored; original specs/history remain preserved. Read PROJECT_LOG and source before further changes.

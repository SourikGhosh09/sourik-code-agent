# Current handover

Current version: V1.4.1 preview. Start Agent.cmd opens Start V1.4.1.cmd.

V1.4.1 removes stale initial source/memory excerpts from repeated-failure recovery while retaining the goal, system policy, current bounded file evidence and explicitly stale last-test output. The strengthened regression fails before the fix and passes after it. Seven focused tests passed; full Windows suite: 83 passed, two symlink skips (85 total). Compilation passed. Both unchanged 7B invoice trials failed at the step limit (111.51 and 51.03 seconds). Trial one changed line_items.py and test_invoice.py, failing fixture trust; trial two changed only line_items.py, preserving tests/validation/README but leaving invoice arithmetic incorrect. REPAIR-001 remains open; no model-reliability improvement is established. Evidence: docs/evaluation-v1.4.1.json.

Next: diagnose repeated nonmatching patch/search selection and preservation of explicitly protected task files using the retained failed traces. Keep the evaluator and approval boundaries unchanged. Avoid broader agent architecture until evidence justifies it. Normal resource workload has been measured; physical low-memory and manual startup/accessibility acceptance remain pending.

No dependency, storage migration or permission change. Commands still run with OS rights; resource settings are targets. Original specs/history remain preserved. Raw fixtures, runtimes/models and the earlier local backup patch remain ignored. Publication target is the existing private GitHub repository.

# V0 acceptance tracking

| Requirement | Implemented evidence | Gate |
|---|---|---|
| Task, inspection, plan, file generation | SQLite task state, repository map, model action protocol | Scripted integration passes; 3B new-project evaluation fails |
| Commands, errors, repairs | Approval callback, bounded subprocess, observation loop | Real 3B bug repair passes with baseline failure and independent checks |
| Verification and completion | Successful command required after final edit; failed actions invalidate proof | Regression tests pass; independent task assertions pending |
| Changed files, history, checkpoint | Unified diffs, PROJECT_LOG.txt, durable snapshots and restore | Tests pass |
| Existing broken repository | Separate real-model calculator bug fixture | Real 3B repair passes |
| Two resource profiles | Eco/Balanced/High thread and context targets | Unit test passes; real model pending |
| Forced failure | Nonzero exit, timeout, denied command, cancellation, invalid JSON | Tests pass |
| Desktop workflow | Native folder picker, goal, Run/Stop, status, approval, diff/history | Construction and failure-display tests pass |

The application is a development prototype, not yet an accepted V0 release. No training or plugin execution is claimed. CPU/context controls are runtime targets; hard memory/GPU limits are not implemented. Command approval is not an OS sandbox. Read README.md before running untrusted projects.

Source: all 19 v1.1 project-pack documents in specs. Their requirements remain unchanged.

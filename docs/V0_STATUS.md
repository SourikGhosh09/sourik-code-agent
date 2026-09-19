# V0 thin-slice acceptance: passed

Verified on 2026-09-19 with local **qwen2.5-coder:7b**. This passes the documented small-project demonstration, not a broad coding-quality benchmark or production-security certification.

| Check | Evidence |
|---|---|
| Empty project from natural-language request | Created calculator source and five unittest tests; tests and independent behavior assertions passed |
| Existing broken project | Observed failing baseline, patched arithmetic bug, retained original tests, passed tests and independent assertions |
| Two resource envelopes | Same 7B model: Eco 5 threads / 4,096 context; Balanced 10 threads / 8,192 context |
| Failure handling | Failed commands, timeout, denied permissions, cancellation, invalid model output and false completion covered by regression tests |
| History and recovery | Project log, SQLite events, diffs, durable checkpoints and rollback tested |
| Desktop | Window construction, task failure display and runtime-readiness waiting tested; Auto selection confirmed against installed models |
| Regression suite | 28 tests passed; one real symbolic-link fixture skipped because Windows denied link creation; real junction boundary tests passed |

Latest measured task times: 72.82 seconds for new-project creation and 10.96 seconds for repair. These include runtime conditions and are not controlled speed comparisons.

Machine-readable results: [evaluation-v0.json](evaluation-v0.json). Original run: `evaluation-results\20260919-144653`. Model digest and exact agent-code digest are recorded in both reports.

## Recommended use

Double-click `Start Agent.cmd`, leave AI power on **Auto**, choose a small project folder, describe the task and click Run task. The model and runtime are already installed locally. Commands still require explicit approval.

The smaller 3B model passed bug repair but repeatedly failed new-project generation. Eco with automatic model selection chooses that smaller model; use Auto for the verified default, or manually select 7B when testing the Eco resource envelope.

## Remaining roadmap work

V1 and later: stronger OS isolation, richer repository indexing and memory, advanced resource controls/continuous adaptation, executable plugins, model training and polished distribution. Commands run with user OS permissions; V0 is not an OS sandbox. Exact CPU/RAM/VRAM percentage limits are not guaranteed. See README.md for bounded file/context limits.

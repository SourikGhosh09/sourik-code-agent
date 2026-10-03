# Current handover

Published release: **V1.11.0 preview**, 2026-10-03. Start Agent.cmd opens Start V1.11.0.cmd. Tested source: b425e312f20a55c57f37b1b8bb5ef991c3250e86, tag v1.11.0. [GitHub CI passed](https://github.com/SourikGhosh09/sourik-code-agent/actions/runs/37140619076). The current source ZIP includes final publication notes; its code and evaluator hashes match all four recorded model trials.

V1.11.0 implements the audited desktop redesign: compact light workspace, clear project/priority/backend labels, visible recovery, readable results and a separate nonmodal Settings window. Custom focuses CPU threads; Back/Escape/close withdraw Settings without stopping work. Internal event/view names, saved keys, approvals and runtime controls are unchanged. No dependency or database migration.

## Verification

Full local suite: 118 passed, two Windows symlink skips (120 total); 28 focused UI/resource checks passed. New native regressions reproduced hidden recovery/output and Settings clipping, then passed after repairs. [Audit](docs/UI_AUDIT.md) and [built design](docs/UI_DESIGN.md) preserve findings, choices and previews.

Real local 7B regression: three of four guided tag trials passed. Initial trial returned HTTP 500 before a model response or edit; second passed. One bounded repeat pair passed. All outcomes/hashes are retained in [evidence](docs/evaluation-v1.11.0.json). Runtime root cause is unconfirmed; the inspected old log does not establish it. Less-guided task reliability remains unaccepted; these guided tasks do not repair that gap.

## Boundaries and next work

Python/Tk/SQLite, local models, deterministic simplicity policy and approvals remain. Commands have user OS rights; no OS sandbox or hard resource caps. Fixture approval must never be used for arbitrary projects. No dependencies, schema changes, mandatory cloud service or paid API.

Manual Narrator/high-contrast/DPI/full keyboard approval/recovery journeys, clean-machine setup, physical pressure, other compatible servers and OS isolation remain open. Next UI step is those manual journeys or measuring a demonstrated slow UI operation before adding concurrency. Broader behavior-based tasks need separately reviewed execution or validated isolation.

Prior acceptance and unsuccessful recovery investigations remain in PROJECT_LOG.txt and versioned evidence, including [V1.9.2](docs/evaluation-v1.9.2.json), [less-guided baseline](docs/evaluation-v1.9.2-behavior.json) and [denial comparison](docs/evaluation-v1.9.2-denial-comparison.json). Original specs remain preserved; raw evaluations, runtimes and models stay outside Git.

# Current handover

Current candidate: **V1.11.0 preview**, 2026-10-03. Start Agent.cmd opens Start V1.11.0.cmd. Published predecessor: V1.10.0 at 20b274c, tag v1.10.0, successful hosted CI. V1.11.0 publication awaits final diff/CI; do not confuse local verification with hosted acceptance.

V1.11.0 implements the audited desktop redesign: compact light workspace, clear project/priority/backend labels, visible recovery, readable results and a separate nonmodal Settings window. Custom focuses CPU threads; Back/Escape/close withdraw Settings without stopping work. Internal event/view names, saved keys, approvals and runtime controls are unchanged. No dependency or database migration.

## Verification

Full local suite: 118 passed, two Windows symlink skips (120 total); 28 focused UI/resource checks passed. New native regressions reproduced hidden recovery/output and Settings clipping, then passed after repairs. [Audit](docs/UI_AUDIT.md) and [built design](docs/UI_DESIGN.md) preserve findings, choices and previews.

Real local 7B regression: three of four guided tag trials passed. Initial trial returned HTTP 500 before a model response or edit; second passed. One bounded repeat pair passed. All outcomes/hashes are retained in [evidence](docs/evaluation-v1.11.0.json). Runtime root cause is unconfirmed; the inspected old log does not establish it. Less-guided task reliability remains unaccepted; these guided tasks do not repair that gap.

## Boundaries and next work

Python/Tk/SQLite, local models, deterministic simplicity policy and approvals remain. Commands have user OS rights; no OS sandbox or hard resource caps. Fixture approval must never be used for arbitrary projects. No dependencies, schema changes, mandatory cloud service or paid API.

Manual Narrator/high-contrast/DPI/full keyboard approval/recovery journeys, clean-machine setup, physical pressure, other compatible servers and OS isolation remain open. Next UI step is those manual journeys or measuring a demonstrated slow UI operation before adding concurrency. Broader behavior-based tasks need separately reviewed execution or validated isolation.

Prior acceptance and unsuccessful recovery investigations remain in PROJECT_LOG.txt and versioned evidence, including [V1.9.2](docs/evaluation-v1.9.2.json), [less-guided baseline](docs/evaluation-v1.9.2-behavior.json) and [denial comparison](docs/evaluation-v1.9.2-denial-comparison.json). Original specs remain preserved; raw evaluations, runtimes and models stay outside Git.

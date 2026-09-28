# Changelog

## 1.4.2 - 2026-09-28 (preview)

- Refresh current-source and review context, clarify rejected actions, and support a finish action through existing verification/budget gates.
- Schedule the previously used verification command after edits with fresh approval; never invent a command or auto-approve it.
- Enforce explicit Preserve ... tests clauses in file tools. Defer existing-file count estimates to final review while preserving new-file/dependency/abstraction gates.
- Validation: 88 passed, two skips; four final-source invoice trials and four calculator/no-change cases passed independent checks. No dependencies or architecture migration. Broader reliability and manual UI acceptance remain open.

## 1.4.1 - 2026-09-27 (preview)

- Remove stale initial excerpts when refreshing repeated-failure context; retain the task and current evidence.
- Strengthened the existing invoice recovery regression; 83 tests passed, two skipped. No dependencies or permission changes.
- Both unchanged real-model invoice trials failed. This patch corrects stale context but does not establish reliable autonomous repair. See docs/evaluation-v1.4.1.json.

## 1.4.0 - 2026-09-26 (preview)

- Integrated the supplied V1.3.0 source into the existing Git checkout; retained its startup, repair-feedback and indexing improvements.
- Added bounded read-only resource sampling and separate deterministic low-memory/recovery checks using existing policy functions. Reports refuse overwriting files; no resource control or dependency changed.
- Windows baseline for imported V1.3.0: 80 passed, two symlink skips. V1.4.0: 83 passed, two skips; native Tk and junction checks passed. Compilation and three actual host samples completed.
- Actual memory stayed above the low-RAM threshold. Inference-load/pressure acceptance, manual accessibility and real-model repair remain pending.


## 1.3.0 - 2026-09-26 (preview; user validation deferred)

- Added scoped root/nested ignore rules with a documented wildcard/negation subset and deterministic traversal. Hard secret/link protections remain prior to exceptions.
- Preserved relative Python import depth and rank existing local module/package candidates, including ordinary src/ layouts. No project imports are executed.
- Refresh old cached import metadata automatically using a parser-versioned fingerprint; no SQLite migration or dependency.
- Added 10 indexing regressions. Forty focused checks passed; full suite: 78 passed, two Windows-only skips, two no-display GUI errors (82 total). Compilation passed.
- User requested testing later. Windows/native UI and real-model acceptance remain pending; development can continue independently.

## 1.2.0 - 2026-09-26 (preview; native and model acceptance pending)

- Hardware/model discovery now runs in a background worker. Preparing, duplicate-run prevention, startup Stop, safe close and error/retry use the existing controls/event queue.
- Current runs capture settings before discovery; subsequent UI edits stay for future runs. Cancelled/closed results cannot launch a task.
- Added 11 startup tests, including real Tcl event dispatch during delayed discovery. Updated the native Tk task test for asynchronous startup.
- Validation: 68 passed, two Windows-only skips and two no-display Tk errors (72 total). Compilation passed. Native Windows checks and real-model invoice acceptance remain pending.
- No dependency, storage migration, model/approval policy or agent-loop change.

## 1.1.1 - 2026-09-26 (preview; model acceptance pending)

- Repeated unchanged writes now refresh current-file evidence and retain the last failed command until verification succeeds. Actual edits reset the repeat comparison.
- Unchanged writes preserve revisions and existing verification; repeated attempts remain bounded by the existing step limit.
- Budget feedback distinguishes estimates from remaining work and keeps explanations in JSON. Inspection and test schemas no longer require unrelated explanations; runtime installation gates and command approval remain intact.
- Added four regression cases; updated launcher/version and project records. No dependencies, storage migrations or architecture changes.
- Validation: 57 passed, two Windows-only skips, two GUI errors due to no display. Real-model trials could not start without Ollama; no reliability improvement is claimed.

## 1.1.0 - 2026-09-26 (preview)

### Added

- Explicit MAJOR.MINOR.PATCH naming in the app, package metadata and launcher.
- Focused regression checks for required tool fields, no-op patches and recovery evidence.

### Fixed

- Model action schemas now require the fields for the selected tool.
- Incomplete and identical-text patches are rejected before mutation with actionable feedback.
- Repeated-error recovery retains the last failing command output alongside current source evidence.

### Compatibility and limits

- No dependencies or production permission changes; existing projects and local settings remain compatible.
- Infrastructure: 56 passed, one skipped. Both final invoice model trials failed after unrequested README edits and repeated writes; multi-file acceptance is not met. See docs/evaluation-v1.1.0.json. This preview is not a verified autonomous-repair release.

## Earlier documentation pack

### Added

- Initial current-state project specification/documentation pack, development guidance, operations, security, roadmap and basic CI for Sourik Code Agent.

### Changed

### Fixed

### Removed

### Security

Earlier implementation history remains in PROJECT_LOG.txt and is not reconstructed here.

# Changelog

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

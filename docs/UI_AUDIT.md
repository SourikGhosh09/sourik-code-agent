# Desktop UI technical audit

Audited 2026-10-03. Baseline: V1.10.0, commit `657784c58dcb9c5e0b03d0f78d6ddc63973f4444`.

## Platform verdict

The application is a Windows Tk desktop workspace with standard toolkit controls, a file chooser, dialogs and keyboard shortcuts. It does not present as a website. The forced `clam` theme is a Tk theme; this audit does not certify Windows theme integration, high contrast or Narrator support.

The UIAudit plugin's native technical checklist was adapted to Windows desktop concerns. iOS/Android touch targets, system gestures, display insets and mobile orientation rules do not apply and were not scored. No browser audit or mobile acceptance is implied.

## Evidence and limits

- Source: `local_agent/ui.py`, `local_agent/storage.py`, `local_agent/tools.py` and `tests/test_ui.py` at the baseline revision. Line numbers below refer to that revision, so later changes do not alter the historical evidence.
- Native geometry and captures collected by the implementation task at Tk scaling 2.0: `.runtime/ui-captures/before/default.png`, `.runtime/ui-captures/before/custom-small.png` and `.runtime/ui-captures/before/geometry.json`. These ignored artifacts are local evidence, not release files.
- At 1000x760, the baseline output viewport was approximately 90 pixels high and the Undo/Restore controls were not mapped. At 780x600 with Custom power and model settings opened, some resource fields extended below the window and output, status and recovery controls were not mapped.
- Existing native tests check minimum-width fit, request-field Tab/Shift+Tab, keyboard shortcuts, output-tab traversal and Custom field reveal/focus. They do not check vertical fit with both settings groups visible.
- This technical audit did not perform a Narrator session, contrast measurement, full keyboard approval/recovery journey, multiple-monitor DPI transition or slow-storage timing benchmark. Scores are provisional, not accessibility certification.

## Baseline health score

| Dimension | Score (0-4) | Evidence or limitation |
|---|---:|---|
| Accessibility | 2 | Keyboard support exists; several fields lack visible labels and expanded settings break reachability at the supported minimum size. Screen-reader behavior is untested. |
| Performance | 3 | Hardware/model discovery and agent work use workers; history is bounded. Some database, diff and checkpoint work remains synchronous without measured latency evidence. |
| Appearance and theming | 3 | Consistent toolkit styling and text hierarchy; forced theme and fixed fonts have unverified Windows appearance/high-contrast behavior. |
| Desktop platform conformance | 3 | Familiar file chooser, dialogs, notebook and shortcuts; disclosure buttons do not expose their current state. |
| Adaptivity | 1 | Observed vertical clipping hides output/recovery and resource controls at supported window sizes. |
| **Total** | **12/20** | **Acceptable: significant layout work needed.** |

Three verified findings: one P1, two P2; no P0 or P3 finding. Resize is a workaround for the major issue, so it is not scored as a total task blocker.

## Findings

### UI-01 [P1] Expanded settings displace essential output and recovery controls

**Location:** Main window and Custom power settings; `local_agent/ui.py:25`, `:58`, `:80`, `:98`, `:100`, `:131`. Category: adaptivity/accessibility.

The project/request area and both settings groups consume vertical space above the expanding output notebook. Recovery buttons are packed after that notebook. The observed baseline geometry confirms hidden controls, not just a large requested size. A user at the advertised 780x600 minimum can select Custom and lose access to settings, progress and recovery. The default 1000x760 layout also hides recovery at the tested text scale.

**Recommendation:** Put advanced settings in a reachable dedicated surface within the existing notebook, preserve a useful output viewport, and keep primary status/actions and recovery available. Verify every relevant mapped control lies inside its visible container at the supported minimum size. Preserve keyboard access when Custom selects its fields.

**Suggested follow-up:** `/impeccable adapt` for the layout constraint; implementation is handled separately from this audit.

### UI-02 [P2] Project, preference and backend selectors have no explicit visible labels

**Location:** `local_agent/ui.py:37`, `:54`, `:76`. Category: accessibility/clarity.

The project combo relies on a neighboring action button for context. Quality/Speed has no field label. The backend combo sits next to Auto model in a row without a label explaining its role. Current values are not durable field labels, especially after a user edits the project path or uses keyboard traversal. Adding visible labels improves interpretation; it alone does not prove screen-reader association in Tk.

**Recommendation:** Add short, stable labels for the project folder, preference and backend, preserving the existing setting values and runtime behavior. Check reading/focus order and validate actual Narrator announcements manually before claiming assistive-technology acceptance.

**Suggested follow-up:** `/impeccable clarify` for labels.

### UI-03 [P2] Settings disclosure buttons do not show their current state

**Location:** `local_agent/ui.py:61`, `:66`, `:81`, `:84`. Category: desktop conformance/accessibility.

The Model settings and Resource settings buttons retain the same text after showing or hiding their groups. Their current open/closed state is represented only by the nearby group's presence. Keyboard users get no explicit state from the control, and the expanded groups can move output beyond the window.

**Recommendation:** Use an existing notebook Settings tab or make disclosure labels explicitly show/hide and retain a logical focus destination. If a Settings tab replaces the disclosures, keep its selected state visible through the toolkit and preserve entry focus for Custom.

**Suggested follow-up:** `/impeccable clarify` for control state and navigation.

## Performance observations requiring measurement

These are source-based risks, not verified stalls and are not counted as defects:

- `App.refresh_project` (`ui.py:316`) opens SQLite and fills the history/memory lists on the UI thread. History is capped at 30 rows (`storage.py:76`); normal memory writes retain 100 records (`storage.py:58`). This is not an unbounded-list finding.
- Task completion calls `Tools.diff()` from `App.poll` (`ui.py:397`), reading tracked files and building their unified diff synchronously (`tools.py:174`). Checkpoint conflict checks/restoration also read and write tracked files synchronously (`ui.py:282`, `:296`, `:310`; `tools.py:159`, `:190`, `:199`). Large tracked files or slow storage could delay input. No timed reproduction establishes the impact yet.
- `App.poll` drains the whole event queue before rescheduling (`ui.py:379`), while output text accumulates during the application session (`ui.py:167`). Test a long representative task before introducing batching, pruning or another worker layer.

Keep these in a measured follow-up; do not add speculative concurrency or pagination merely to improve an audit score.

## Positive findings to preserve

- Slow discovery and agent execution already run off the Tk thread, with queue-based handoff and startup cancellation. A Tcl event-loop test verifies callbacks continue while discovery waits.
- Settings are captured on the UI thread before discovery. Later edits apply to a later task and do not rewrite the running task's configuration.
- Task Run is guarded while work is active; startup failures restore retry access and display the actual error.
- Request-field Tab and Shift+Tab move focus without changing the request. Run, Stop, project focus and output-tab shortcuts have native tests.
- Command approval shows the exact arguments and working folder and truthfully states Windows permission/network exposure. Recovery warns about overwriting later edits and separately detects conflicts.
- Custom resources explain defaulting, backoff, backend scope and the absence of hard resource limits. No visual-only indicator grants permissions.

## Follow-up order

1. Fix UI-01 and add native vertical-boundary coverage alongside the existing width/focus checks.
2. Fix UI-02 and UI-03 within the same existing UI owner; retain task, approval and recovery behavior.
3. Confirm the revised window at default/minimum sizes and the tested larger text scale, including Custom, both settings categories, output and recovery. Record the result separately from this baseline score.
4. Perform the pending manual Narrator, high-contrast, DPI and full keyboard journeys before claiming full accessibility acceptance.

After fixes, a new technical `/impeccable audit` can verify resolved findings; `/impeccable polish` is only a final bounded review. This report does not require a new dependency, design framework or platform rewrite.

## V1.11.0 implementation verification

UI-01 is resolved for the tested 780x600 / Tk scaling 2.0 workspace: recovery remains mapped/in bounds, output has at least 70 pixels, and Settings has its own 660x590 window with all controls in bounds. The two new native regressions failed before the repairs and passed afterward. No browser/mobile detector was applied to Tk.

UI-02 now has explicit Project folder, Priority and Backend labels. This verifies visual comprehension, not Narrator association. UI-03 inline disclosures were replaced by direct window navigation with Back, Escape and window close; Custom retains a focus destination. Existing startup snapshot, cancellation, approval and recovery behavior is preserved.

All 28 focused UI/resource tests passed. Full suite: 118 passed, two Windows symlink skips (120 total). Follow-up source review found no actionable permission/state/cleanup regression. The baseline score remains historical; no inflated post-fix score or manual accessibility acceptance is claimed. The [built design](UI_DESIGN.md) records the choices and previews. Synchronous UI operations remain measured follow-up work rather than speculative worker changes.

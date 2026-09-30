# User flows

Documentation reviewed 2026-09-30 against V1.9.2. [Current status](../HANDOVER.md) governs present acceptance; dated checkpoints below are historical evidence.

No sign-in exists. OS access to the desktop/project is the current access boundary. Stored notes never grant permission.

## F01 - Launch and select (R01,R05,R07,R08)

Preconditions: Python/Tk, running local server and installed model. Launch, choose project, inspect Auto/Quality or local settings, enter goal. Empty recent history is normal. Missing model/runtime, invalid endpoint and inaccessible folder must show errors. Run starts hardware/model discovery in a background worker with a Preparing status. The window remains available; Stop prevents task startup and close exits without accepting late discovery results. Success: selected project ready for work; automatic download is not promised.

## F02 - Complete task (R01,R02,R03,R06,R07)

From an idle selected project enter a nonempty goal and Run. The agent inspects files/memory, plans, checks simplicity and invokes tools. Read exact command arguments/directory and approve or deny. Denial cannot count as verification. Failed tests lead to diagnosis, smallest correct repair and retest. Review Changes and What changed? An already-satisfied task can verify with zero code changes.

```mermaid
flowchart LR
  Request --> Inspect --> Plan --> Simplicity --> Implement --> Test
  Test -->|fail| Diagnose --> Repair --> Test
  Test -->|pass current revision| Review --> Result
```

Stop requests cancellation; a pending model call can take 120 seconds. Invalid responses, limits or persistent failure end as errors, not fabricated success. Empty projects are supported; zero discovered tests do not verify. Approved commands have user OS rights.

## F03 - Memory/history (R04)

Open memory, inspect a note/verified result, add a nonblank note or forget an entry. Empty lists are valid. Changed evidence excludes verified reuse; notes can be stale. Select a history goal and Run to start a fresh task/checkpoint, not resume paused execution. Surface database errors. Current files and permissions override memory.

## F04 - Recovery (R03)

After unwanted/interrupted work, inspect checkpoint/diff and request rollback. Compare fingerprints; separately confirm overwriting later conflicting edits. Cancel and back up if unsure. Missing/legacy evidence is not proof of safe overwrite. Recovery covers captured project files, not arbitrary external command effects.

## F05 - Settings (R05,R08)

Choose power and Quality/Speed; optionally set CPU/context, backend, endpoint and model. Reject invalid numeric targets. If no suitable installed model exists, install separately or select a compatible existing one. Low RAM reduces future targets, not necessarily loaded weights. Success: valid settings applied to later work; exact resource percentages are not guaranteed. Compare versions sequentially on separate project copies.

V1.1.1 F02 recovery detail: an unchanged write keeps the current file/revision, supplies earlier failing-command evidence to the model, and repeated unchanged writes refresh source context. The normal command approval prompt still applies to retesting. Successful verification clears stale failure evidence. Simplicity estimates do not request new files or documentation; explanations stay in the action response. These are controller-feedback changes, with no new user interaction.

V1.2.0 F01/F02/F05 detail: project, goal and settings are captured when Run is clicked. Edits while Preparing apply to the next Run. A slow check does not enable a second startup. On discovery error, Run becomes available again and the error is shown. Stop may wait for the current discovery call to return; no agent task/command starts from a cancelled result. Closing during discovery need not wait for the call. A new project folder may already have been created; cancellation does not remove it. During an active agent task, close still requests Stop and asks the user to close again after the task ends.

V1.3.0 F02 inspection: common generated/ignored paths are filtered using root and nested project rules before ranking. Python files related through local relative imports are prioritized by actual candidate path. Existing cached metadata refreshes automatically; no settings or migration action is required. Ignore rules do not replace direct-file access checks. Native automated and recorded Ollama checks have since run; full user-run manual journeys remain deferred.

V1.4.2 F02: successful edits and failed checks refresh the model context with current source. After approved verification, completion uses the existing final review and result flow. There is no new user approval shortcut or automatic claim of completion from passing tests alone.

V1.4.2 retesting: after an edit, an already-used verification command may be proposed automatically. The usual approval prompt appears again; denying it does not verify the task. An explicit Preserve ... tests clause also prevents file-tool edits/deletes/moves of recognized existing tests, including moves of their containing directory. This does not constrain an approved command at the OS level.

Current launch uses Start Agent.cmd / Start V1.9.2.cmd. Read-only setup checks accept backend/endpoint/model without saving UI settings. Compatible model settings require an exact advertised ID and a server supporting schema response_format; automatic model memory selection is an Ollama capability. V1.9.1 diagnostic fields belong to the developer evaluator, not a new desktop permission or user workflow.

V1.9.2: nonzero-exit check feedback omits diff and diff_truncated from the model-facing simplicity review. Current file evidence, failing output, counts and findings remain. Recorded simplicity events and successful verification/final review retain full bounded diffs. This prevents obsolete removed lines from being reintroduced after the recovery context refresh. Permissions, evaluator approval and completion gates are unchanged.

# Adam Acquisition v8.3.4.3 — Durable Owner Continuity Memory Across Upgrades

## Why this fix was required
v8.3.4.2 retained the Universal Assistant thread only in browser JavaScript memory and meeting context only for the current meeting session. After a refresh, restart, new extracted version, or new session, Adam could not reliably recall an earlier-version correction such as:

`I didn't say third-water part. I said Empower request channel for chilled water.`

## v8.3.4.3 changes
- Added **durable owner continuity memory** stored in Adam's per-user runtime data location, outside the extracted application folder, so it survives Adam version upgrades.
- Durable writes are deliberately narrow: Adam persists only an **explicit owner correction** or an explicit **remember / don't forget** instruction when persistent owner memory is enabled. Ordinary Q&A is not silently stored.
- Added relevance-scored recall so an old HVAC/Empower correction is not injected into an unrelated stock, software, electrical, or general question.
- Newer explicit corrections are instructed to override older conflicting wording.
- Real Meeting Attendance can use relevant durable owner corrections while keeping ordinary meeting transcript memory ephemeral.
- Added a visible, default-on local-memory control in both Meeting Attendance and Universal Assistant.
- Added browser `localStorage` continuity for the current Universal Assistant task/thread and task-focus field across refresh/restart/version extraction on the same `127.0.0.1:8770` origin.
- **Start New Task** clears the current task thread but does not erase relevant durable owner corrections.
- Added **old software test/release history recall** from packaged `ACQUISITION_V*_NOTES.md`. Release-note examples are clearly marked as software-test history and must never be treated as project facts or approvals.
- The prior Empower correction test is therefore recoverable immediately from v8.3.4.1/v8.3.4.2 release notes, even though arbitrary old session text that was never persisted cannot be reconstructed.

## Safety / privacy boundaries preserved
- Durable owner memory is local-only and performs no network or external action.
- Secret/credential-like memory is rejected by the continuity-memory module.
- Meeting Focus, project isolation, question coverage, no-silent-turn behavior, and owner approval for consequential external actions remain unchanged.
- Release/test history is non-project evidence and cannot establish project approval, cost, date, instruction, or contractual position.

## Verification
- New continuity-memory tests: 5 PASS.
- Preserved v8.3.4.0/v8.3.4.1/v8.3.4.2 affected-behavior tests excluding obsolete exact-version assertions: 10 PASS.
- Python compile: PASS for modified Python files.
- Real Meeting Attendance JavaScript syntax: PASS with Node.
- Full Flask runtime import was not executed in the build container because Flask is not installed in that container; this is an environment limitation, not a syntax failure.

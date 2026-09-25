# Adam Acquisition v1.1.2 — Workflow Planning Fix

This is a focused acceptance repair build, not a new feature phase.

## Fixed
- Restored the missing `ai_text()` compatibility helper used by Follow-Ups, Documents and draft revision.
- Follow-Up Email no longer remains indefinitely on “Preparing professional follow-up email…”.
- Follow-Up draft API now returns structured JSON errors and the `body` / `subject` fields expected by the UI.
- Follow-Up UI now handles server/non-JSON errors visibly instead of appearing frozen.
- Verified Test 13 phrase deterministically maps to Analyze Source → Prepare Response → Outlook Owner Review.
- Version advanced to v1.1.2.

## Internal verification
- Python compile: PASS
- Orchestration tests: PASS
- v1.1.2 static acceptance-fix tests: PASS

Owner acceptance remains required before this version is marked APPROVED.

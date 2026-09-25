# Adam Acquisition v8.3.4.1 — Natural Meeting Corrections, Comments & Orders Fix

## Physical-test correction
- Fixed the case where a meaningful participant correction/comment was transcribed but Adam stayed silent because it was not phrased as a direct question.
- `Professional conversation — questions / corrections / orders` now responds to direct questions, explicit corrections, actionable requests/orders, and substantive comments addressed to Adam while preserving Meeting Focus Lock.
- Example correction: `I didn't say the third water part. I said Empower request channel for chilled water.` Adam should acknowledge the correction, use the corrected wording, and continue the same task.
- Corrections and orders are not falsely counted as direct questions in Question Coverage.
- Hard project isolation still runs before the conversational response gate.
- Consequential external actions still require owner approval.
- Wake-name hold (`Adam...`) and question-preamble hold remain unchanged.

## Preserved
- v8.3.4.0 Universal AI Assistant / one-task focus.
- v8.3.3.x selective listening and project isolation.
- Meeting memory, report, question coverage, full-duplex/barge-in, and owner approval boundaries.

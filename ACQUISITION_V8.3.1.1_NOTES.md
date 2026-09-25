# Adam Acquisition v8.3.1.1 — Owner Representative Auto-Response Fix

Physical v8.3.1 testing showed that Adam transcribed a participant addressing “Adam” but did not answer. The response path was gated by two extra UI controls (`autoRespond` and `conversationApproved`) even after the owner had explicitly approved Owner Representative mode.

## Fix
- Owner Representative mode now treats the explicit **Owner Approval — allow Adam to act as my disclosed AI representative** as the meeting-session authorization for normal conversation.
- When that approval is checked, auto-response is armed automatically.
- A final transcript that addresses `Adam`, `آدم`, or `ادم` now calls the meeting conversation AI automatically and speaks the answer.
- Active Participant mode retains its separate conversation approval.
- Consequential actions/commitments remain blocked and still require separate exact owner approval.
- Multilingual understanding, English-default replies, participant-requested language switching, and cross-disciplinary professional behavior are preserved.

# Adam Acquisition v8.3.4.2 — No-Silent-Turn / Noisy-Room Auto-Reply Fix

## Physical-test correction
- Fixed the case where a meaningful correction, order, addressed comment, or direct question was successfully transcribed and displayed but Adam never replied.
- Root cause: the reply scheduler could wait indefinitely on raw microphone/VAD activity from room noise or a new recording chunk even after the accepted participant transcript was complete.
- Auto-response stability now follows **accepted transcript timing**, not continuous raw microphone energy.
- A 6-second response watchdog guarantees that a meaningful accepted interaction cannot remain queued forever because of noisy-room VAD.
- New accepted continuation text resets the stability timer so Adam can still wait for the participant to finish a multi-part thought.
- Server-marked completed turns continue to dispatch immediately after the natural end-of-turn boundary.
- Meeting Focus Lock, hard active-project isolation, wake-name/question-preamble hold, owner-approval boundaries, and the separate Universal AI Assistant remain preserved.

## Expected regression test
When the live transcript contains: `I didn't say third water part, I said Empower request channel for chilled water.` Adam must acknowledge the correction and continue using the corrected subject; background room energy must not keep him silent.

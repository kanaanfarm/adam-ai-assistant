# Adam Acquisition v8.4.1.11 — Immediate Voice Start / TTS Latency Fix

Purpose: reduce the measured meeting `voice prep` delay without changing the already approved end-of-turn, clarification, approval, transcript, or meeting-session isolation behavior.

## Changes

- Adds **Instant factual voice** (enabled by default) for the existing short, self-contained factual fast path.
- When a reply is already classified by the existing v8.4.1.9 fast factual path, Adam starts the browser/device speech engine immediately instead of waiting for `/api/tts` to finish generating server audio.
- Approval/change/proceed questions, clarification turns, contextual follow-ups, and other governed meeting replies continue to use the professional server TTS path.
- If instant device speech is unavailable, Adam automatically falls back to the existing professional server voice path.
- Browser speech latency is now stamped on the actual `SpeechSynthesisUtterance.onstart` event, with a short fallback for browsers that do not reliably fire `onstart`.
- Existing speaker-echo protection remains active.

## Locked behavior preserved

- v8.4.1.6 end-of-turn / technical transcript accuracy.
- v8.4.1.7 approval-status consistency.
- v8.4.1.8 clarification classification and new-meeting context isolation.
- v8.4.1.10 fast/protected turn timing and complete latency telemetry.

## Physical acceptance target

Ask once: `Adam, what is the function of a balancing valve?`

Expected:
- latency line shows `fast factual path`;
- `voice prep` should be substantially below the previous ~3.3 s on a browser with working Web Speech synthesis;
- Adam still waits for the natural end of the user's turn before replying;
- no governance/approval path should use the instant factual voice optimization.

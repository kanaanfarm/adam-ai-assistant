# Adam Acquisition v8.4.1.11.2 — End-Turn Timestamp Accuracy Fix

## Scope
Narrow latency-telemetry correction after v8.4.1.11.1.

## Fix
- Detects the first confirmed participant speech frames after a completed prior Adam turn and starts a fresh latency trace for that utterance.
- Prevents the previous turn's frozen `speechEndAt`, `questionId`, or AI timestamps from leaking into the next utterance.
- Corrects impossible end-turn displays such as `62.6s` for a short question while preserving the v8.4.1.11.1 total-to-voice-start timestamp freeze.
- Keeps the 2.4 s fast silence boundary and 4.2 s protected natural-pause boundary unchanged.
- No change to STT transport, focus/merge, AI provider logic, instant factual voice, clarification/approval governance, meeting memory, or meeting-session isolation.

## Expected display
For a new short question after Adam has already completed a previous reply, `end-turn` should reflect only the current utterance silence boundary (normally about 2–3 s on the fast path), never the age of the previous turn.

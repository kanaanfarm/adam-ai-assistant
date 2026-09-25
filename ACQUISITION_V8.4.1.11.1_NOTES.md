# Adam Acquisition v8.4.1.11.1 — Total-to-Voice-Start Timestamp Fix

## Scope
Narrow telemetry-only correction after v8.4.1.11.

## Fix
- Freezes the participant `speechEndAt` timestamp once STT/AI dispatch begins.
- Prevents Adam's own immediate browser/device speech from overwriting the participant speech-end timestamp during the tiny interval before browser `speechSynthesis.onstart` enables speaker protection.
- This removes the false `total to voice start 0.0s` and false `voice prep 0.0s` caused by negative deltas being clamped to zero.
- No change to end-of-turn timing, STT transport, focus/merge, AI provider logic, clarification/governance, meeting isolation, or voice delivery behavior.

## Expected display
A run like `end-turn 2.5s | STT 0.8s | focus/merge 0.4s | AI 2.9s` should report approximately `total to voice start 6.6s` plus the true measured voice-prep interval.

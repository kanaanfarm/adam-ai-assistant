# Adam Acquisition v8.4.1.10

## Stable Short-Question End-of-Turn + Complete Latency Telemetry Fix

This is a narrow follow-up to v8.4.1.9 based on physical meeting tests where the same short balancing-valve question sometimes used the fast 2.5 s boundary and sometimes fell back to the protected 4.3 s boundary, while the latency line sometimes lost the AI/voice stages after the reply completed.

### Changes
- Keeps the protected natural-pause boundary at 4200 ms for longer turns.
- Keeps the fast silence boundary at 2400 ms, but extends the short-turn speech-span eligibility from 6500 ms to 12000 ms so a normally spoken short question does not fall back merely because the speaker talks slowly.
- Preserves the in-flight latency trace while Adam is already dispatching/processing a question. Re-armed microphone activity can no longer wipe AI/provider/voice timing for the active reply.
- Adds `turn fast` / `turn protected` to the latency line so the selected end-of-turn path is visible.
- Exposes the fast boundary, 12 s fast-turn eligibility, and in-flight latency-trace preservation in the representative status endpoint.

### Intentionally unchanged / locked behavior
- v8.4.1.6 natural-pause protection for longer/incomplete turns remains available through the protected 4200 ms path.
- v8.4.1.7 owner-approval consistency is unchanged.
- v8.4.1.8 clarification classification and new-meeting context isolation are unchanged.
- v8.4.1.9 AI fast factual path and fast voice chunking are unchanged.
- AI provider transport is unchanged.

### Physical acceptance test
Ask once: `Adam, what is the function of a balancing valve?`

Expected latency line should remain visible after spoken reply completion and include, when available: total to voice start, end-turn, STT, focus/merge, AI, voice prep, provider, plus `turn fast` for this short question. A deliberately long/incomplete turn must remain eligible for `turn protected`.

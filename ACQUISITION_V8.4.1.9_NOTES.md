# Adam Acquisition v8.4.1.9 — Meeting Response Latency Fast Path + Timing Diagnostics

## Purpose
This focused upgrade addresses the live-meeting response delay reported after v8.4.1.8. A short meeting question was taking about 12 seconds before Adam began speaking.

The upgrade reduces avoidable delay while preserving the previously approved v8.4.1.6 protection against answering before the participant finishes speaking.

## Changes
- Added **Fast meeting response** mode, enabled by default.
- The original v8.4.1.6 full natural-pause boundary of **4200 ms** remains in the code and is still used for longer turns.
- Short spoken turns may use an adaptive **2400 ms** silence boundary; once the spoken turn becomes longer than 6.5 seconds, Adam automatically falls back to the full 4200 ms pause protection.
- After server transcription, a clearly complete direct question can use a **350 ms** final merge grace instead of the normal 1500 ms continuation grace. Incomplete/non-question turns retain the longer merge protection.
- Added a narrow **low-latency factual-question server path** for short self-contained questions such as “What is the function of a balancing valve?”
- Approval, proceed/change, cost, variation, commitment, contextual follow-up, clarification, and proactive-intervention turns are excluded from the compact path and continue using the full meeting prompt/governance logic.
- The compact factual path keeps the same configured AI provider/model but reduces the normal response budget to 320 tokens and sends a smaller, governance-preserving prompt/context package.
- Added **Meeting response latency** diagnostics showing, when available:
  - total time from participant speech end to Adam voice start;
  - end-of-turn wait;
  - speech transcription time;
  - focus/merge time;
  - AI round-trip time;
  - provider time returned by the server; and
  - TTS/voice preparation time.
- Activated the existing **Fast meeting voice** behavior for real replies: long answers are now synthesized in short speech chunks so Adam can begin speaking after the first short chunk is ready rather than waiting for the entire answer audio to be generated.
- Voice playback timing is recorded at the moment actual speaker playback begins, not when TTS preparation starts.
- Existing five-stage meeting reply trace remains unchanged, ending with **spoken reply completed**.
- v8.4.1.5 AI-response, v8.4.1.6 end-of-turn/transcription, v8.4.1.7 approval consistency, and v8.4.1.8 clarification/session-isolation behavior remain present.

## Targeted owner acceptance test
Do not repeat previous locked acceptance tests.

Start a clean meeting, keep **Fast meeting response** and **Fast meeting voice** enabled, then ask only:

> Adam, what is the function of a balancing valve?

PASS requires:
- Adam does not interrupt before the sentence is finished.
- One direct question is recorded, with one reply and no duplicate.
- Adam begins speaking materially faster than the previously observed ~12 seconds.
- The new **Meeting response latency** line shows the measured breakdown.
- The normal five-stage trace still reaches **spoken reply completed**.

The first physical run is used to establish the real machine/network result. If the total is still high, use the displayed stage timings to optimize only the slow stage in the next focused version rather than weakening turn-completion protection.

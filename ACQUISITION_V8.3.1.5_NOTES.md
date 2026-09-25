# Adam Acquisition v8.3.1.5 — Completed-Turn Auto-Answer Dispatch

This focused patch fixes a physical-test regression where a complete participant question was transcribed but Adam remained in “waiting for the participant to finish the full turn” and never dispatched the answer.

## Changes
- The MediaRecorder now records why a capture stopped (`end_of_turn`, `silence`, or `max_utterance`).
- A capture stopped by the sustained-silence end-of-turn boundary is explicitly marked as a completed participant turn.
- Completed server-transcribed turns dispatch directly to Adam instead of waiting on the VAD state of the next recorder.
- Exact duplicate completed transcripts within a short window are ignored for transcript, meeting memory, and auto-response.
- Consecutive duplicate lines returned inside one STT result are collapsed.
- Participant barge-in, persistent meeting memory after Clear Screen, multilingual STT, and owner consequential-action boundaries are preserved.

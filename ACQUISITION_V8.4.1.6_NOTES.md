# Adam Acquisition v8.4.1.6 — Meeting End-of-Turn Segmentation + Technical Transcript Accuracy Fix

## Purpose
This focused upgrade addresses the two remaining issues observed after the chilled-water context test:

1. one spoken participant turn could be split into multiple accepted/direct-question records when the speaker used natural pauses;
2. the technical word **flow** could be transcribed as **floor** in hydronic/MEP discussion.

## Changes
- Increased the server-capture end-of-turn silence boundary from 3.2 s to 4.2 s.
- Added a 1.5 s final-turn merge grace before Adam dispatches a microphone turn.
- Added continuation-speech holding so Adam does not answer while the participant has resumed speaking.
- Reuses one stable question ID for contiguous fragments of the same buffered participant turn, preventing focus/question counters from counting one sentence as multiple questions.
- Keeps typed meeting queries immediate; the extra merge grace applies only to microphone/server-transcribed turns.
- Filters transient low-information STT fragments before they inflate Meeting Focus counters.
- Sends a bounded local technical-context hint with server transcription processing.
- Adds a conservative hydronic transcript repair for narrow **flow/floor** confusions such as “the floor is unchanged” → “the flow is unchanged” only when chilled-water/hydraulic context is present.
- Explicitly does **not** rewrite a legitimate phrase such as “floor level is unchanged.”
- All prior v8.4.1.5 provider-response, spoken-reply, accepted-turn persistence, single-pairing, and owner-approval boundaries remain preserved.

## Targeted owner acceptance test
Do not repeat the earlier five-question chilled-water test.

Speak only this one sentence, with natural pauses between the clauses:

> Adam, regarding the same chilled water line… the contractor says the flow is unchanged… and they want to proceed with 100 mm… what is your recommendation?

PASS requires:
- Adam waits until the complete sentence is finished.
- The transcript retains **flow is unchanged**, not “floor.”
- Exactly **1** direct participant question is created for this spoken turn.
- Exactly **1** Adam answer and **1** paired discussion record are created.
- No duplicate response is produced.
- The response remains technically professional and does not approve the pipe size without hydraulic verification.

Previously approved tests stay locked PASS unless this change directly affects them.

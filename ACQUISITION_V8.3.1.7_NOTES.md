# Adam Acquisition v8.3.1.7 — Smart Direct Meeting Response

This focused meeting upgrade improves natural professional conversation without weakening owner controls.

- Faster balanced end-of-turn detection: about 3.2 seconds of sustained silence instead of 5 seconds.
- No extra stability delay for server-completed turns; completed questions dispatch directly after transcription.
- Direct-answer preference: minor STT/accent errors do not cause unnecessary clarification when intent is clear from context.
- Clarification is reserved for materially ambiguous questions or missing referents.
- Clarification follow-up is bounded to a 45-second window and ignores greetings/repeated stray words instead of creating clarification loops.
- Meaningful participant questions/requests are retained in a separate meeting Q&A history; Clear Screen does not remove them.
- Background/no-question fragments can be routed as IGNORE and are not spoken or added to Adam reply history.
- Normal replies are concise by default for lower latency; detailed answers remain available when requested.
- Persistent meeting memory, full-duplex listening, barge-in, multilingual speech, technical-term preservation, and consequential-action owner gates remain preserved.

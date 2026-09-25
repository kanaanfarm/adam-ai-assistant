# Adam Acquisition v8.3.0.3 — Meeting STT Hallucination / Prompt-Leak Guard

Focused fix for the physical v8.3.0.2 bilingual meeting test.

- Removes the long transcription instruction/glossary that could leak into provider output on quiet audio.
- Uses automatic language detection for Lebanese Arabic + English code-switching.
- Prefers `gpt-4o-transcribe` with compatibility fallback to `gpt-4o-mini-transcribe`.
- Adds client-side voice-activity gating so silent 8-second chunks are not uploaded.
- Adds server-side prompt-leak, glossary-echo, and implausibly-long chunk guards.
- Preserves genuine speech that occurs before an accidental `Context: ###` / prompt echo marker.
- Owner approval and representative authority boundaries are unchanged.

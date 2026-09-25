# Adam Acquisition v8.2.0.1 — Guest Microphone Compatibility Fix

- Preserves v8.2.0 advanced intelligence/research routing.
- Keeps native Web Speech recognition where supported.
- Adds MediaRecorder + server transcription fallback for Safari/iPhone and browsers without SpeechRecognition.
- Guest audio is accepted only for an active guest token, size-bounded, transcribed through the configured OpenAI provider, and raw audio is not persisted by this route.
- Finish Speaking stops fallback recording and submits the transcript to the normal guest ask pipeline.
- Existing owner privacy and consequential-action boundaries are unchanged.

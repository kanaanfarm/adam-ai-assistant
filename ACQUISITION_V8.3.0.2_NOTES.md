# Adam Acquisition v8.3.0.2 — Mixed Arabic/English Meeting STT Fix

## Physical issue fixed
The v8.3.0.1 browser SpeechRecognition path was biased to one locale. In a Lebanese Arabic + English sentence it could keep Arabic while dropping or corrupting English technical terms.

## Fix
- Auto — Lebanese Arabic + English now prefers Adam server-side audio transcription instead of single-locale browser speech recognition.
- Uses independent bounded microphone audio chunks and queues transcription in order.
- Transcription prompt explicitly preserves Lebanese Arabic/English code-switching and engineering/project terms.
- Browser SpeechRecognition remains as fallback and for single-language modes.
- Owner approval is required by the server transcription endpoint before audio is accepted.
- Audio/text payloads are not written to audit metadata.
- Meeting representative authority and consequential-action boundaries are unchanged.

## Physical acceptance test
Say: «آدم، شو صار بالـ mechanical drawing وهل الـ consultant approved the latest revision؟»
The transcript should preserve the Arabic meaning plus the English technical terms before testing Adam's answer.

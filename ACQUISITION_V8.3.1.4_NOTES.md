# Adam Acquisition v8.3.1.4 — Persistent Meeting Memory + Full-Duplex Barge-In

## Corrected after physical owner test

1. **Do not answer before the participant finishes**
   - End-of-turn silence threshold increased to 5 seconds.
   - Adam also waits while a recorder contains speech or any transcription is still queued/in flight.
   - Split speech segments are merged before an automatic response is started.

2. **Clear Screen no longer deletes Adam's meeting memory**
   - `Clear Screen` removes only visible transcript/response fields.
   - The current live meeting session keeps ephemeral server-side transcript memory and conversation history.
   - `End Meeting / New Session` is the explicit control that clears the temporary meeting memory and starts a fresh session.

3. **Adam keeps listening while Adam is speaking**
   - Microphone remains active with browser echo-cancellation/noise-suppression requests.
   - Participant speech is still transcribed and remembered while Adam's TTS is playing.
   - Normal statements are captured as notes.
   - A direct question/interruption can stop Adam's current speech and is queued for the next answer rather than being dropped.
   - Adam's own loudspeaker echo is filtered when it closely matches his current/just-spoken response.

4. **No overlapping Adam answers**
   - TTS now waits for actual audio playback completion instead of returning immediately after playback begins.
   - Follow-up questions are queued while Adam is thinking/speaking.

## Preserved boundaries
- Multilingual/cross-disciplinary professional representative behavior remains enabled.
- English remains the default reply language unless a participant requests another language.
- Consequential commitments (costs, variations, contractual changes, payments, purchases, committed-date changes) remain blocked without separate owner approval.
- Real autonomous Teams/Zoom/Google Meet joining is still not claimed until an approved platform adapter exists.

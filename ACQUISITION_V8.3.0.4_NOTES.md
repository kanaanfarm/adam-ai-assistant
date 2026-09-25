# Adam Acquisition v8.3.0.4 — Meeting Microphone Voice-Activity Fix

Focused correction for the physical v8.3.0.3 test where the UI stayed on `Microphone: listening — waiting for speech` and no transcript was produced.

- Fixes an uninitialized JavaScript VAD state (`meetingNoiseFloor`) that prevented speech frames from being counted.
- Explicitly initializes all meeting WebAudio/VAD variables.
- Uses an adaptive threshold suitable for normal/quiet laptop microphones.
- Shows `speech detected` as soon as Adam detects real voice energy.
- If browser WebAudio VAD is unavailable, recording now fails open to server transcription instead of silently making Adam deaf.
- Preserves v8.3.0.3 silence/prompt-leak protections and bilingual Lebanese Arabic + English server STT.
- Owner approval and representative authority boundaries are unchanged.

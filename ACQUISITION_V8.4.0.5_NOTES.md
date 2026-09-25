# Adam Acquisition v8.4.1.0 — Laptop Speaker Echo Protection + Real Voice Delivery

This patch targets the physical failure where the short “voice ready” sample could play, but a real meeting answer was shown as text and then failed to remain audible while the meeting microphone was listening.

## Changes
- Adds **Laptop speaker protection** (ON by default). While Adam is audibly speaking, Adam's own speaker output is ignored by meeting VAD/transcription so it cannot be mistaken for a participant interruption and cancel his reply.
- Recorder chunks contaminated by Adam's own speaker audio are discarded and a clean capture segment is restarted after playback.
- Browser SpeechRecognition fallback also ignores final transcripts while Adam's protected speaker output is active.
- Long meeting voice chunks reduced to ~180 characters for faster TTS start and more reliable playback.
- Typed meeting status no longer falsely says voice delivery completed unless playback actually completed.
- Existing project isolation, meeting memory, correction isolation, question coverage, and consequential owner-approval boundaries are unchanged.

## Trade-off
With laptop speaker protection ON, participant barge-in during Adam's own audible reply is intentionally suppressed because a single laptop microphone cannot reliably distinguish the participant from Adam's speaker output. Turn protection can be disabled from the UI when using headphones/echo-controlled hardware and interruption capture is preferred.

## Physical test
1. Start Listening.
2. Keep Laptop speaker protection checked.
3. Ask: “Adam, the contractor wants to increase the chilled-water pipe from 100 mm to 125 mm. What do you think?”
4. Expected: text answer appears and Adam remains audibly speaking through the response instead of being cancelled by his own microphone echo.

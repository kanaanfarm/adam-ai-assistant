# Adam Acquisition v8.4.1.1 — Meeting Autoplay Unlock Fix

Physical result from v8.4.1.0: the short **Test / Enable Meeting Voice** sample could speak, but the later real Meeting Representative answer still stayed text-only.

## Root cause addressed
A button-click voice test can satisfy browser media autoplay rules, while a later asynchronous response (microphone -> transcription -> GPT -> TTS) may lose that user-gesture permission before `HTMLAudioElement.play()` is called.

## Fix
- `Start Listening`, `Send Typed Query`, and `Test / Enable Meeting Voice` continue to prime/resume a persistent Web Audio `AudioContext` from a direct user gesture.
- Real meeting TTS audio is now decoded and played through that already-unlocked `AudioContext` first.
- HTML `<audio>` remains a second fallback.
- Browser `speechSynthesis` remains the third fallback.
- Meeting barge-in can stop the Web Audio source cleanly.
- Existing project isolation, owner approval, meeting memory, transcript, and report behavior are unchanged.

## Physical acceptance test
1. Click **Test / Enable Meeting Voice** once and confirm the sample speaks.
2. Click **Start Listening**.
3. Ask: “Adam, the contractor wants to increase the chilled-water pipe from 100 mm to 125 mm. What do you think?”
4. Adam must show the answer and speak the actual answer automatically without another click.

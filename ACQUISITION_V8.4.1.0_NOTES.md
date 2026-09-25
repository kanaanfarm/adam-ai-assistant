# Adam Acquisition v8.4.1.0 — Simple Meeting Voice Core

Targeted correction after physical Windows testing showed v8.4.0.5 still produced meeting text replies without audible automatic speech.

## Change
- Removes the complex meeting-only chunk/job/cancellation playback path from automatic meeting replies.
- Automatic Meeting Representative replies now use the same simple `/api/tts -> Audio.play()` pattern proven on Adam's Universal Assistant/main-page voice path.
- If server TTS/audio playback fails, browser `speechSynthesis` is used as fallback.
- Meeting microphone echo flags remain active while Adam is actually speaking, then clear after playback.
- Typed and microphone meeting queries still share the same Meeting Representative response path.
- Existing project isolation, meeting memory, question coverage, correction isolation, and owner-approval boundaries are unchanged.

## Physical test still required
Browser/laptop speaker playback cannot be physically verified in automated tests. After installation, use Test / Enable Meeting Voice once, then ask one normal Meeting Representative question and confirm Adam speaks automatically.

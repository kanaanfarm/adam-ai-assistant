# Adam Acquisition v8.1.0.1 — Guest Voice Playback + Lebanese Session Hotfix

This hotfix targets only the guest voice behavior observed during owner runtime acceptance.

- Every guest reply now follows one enforced path: text response -> TTS playback -> automatic return to continuous listening.
- Stale speech-recognition events are ignored while Adam is thinking or speaking, preventing a just-started TTS reply from being cancelled.
- Browser speech fallback now selects an Arabic voice when Lebanese Arabic is active.
- "Speak Arabic" and Arabic input set the guest session preference to ar-LB and preserve it in the browser session.
- The guest AI prompt explicitly requests natural everyday Lebanese Arabic rather than Modern Standard Arabic when ar-LB is selected.
- Approval-blocked guest requests also return a speakable Lebanese reply; no external action is executed.
- Prior v8.1.0 controls remain unchanged and locked; only this affected behavior requires runtime retest.

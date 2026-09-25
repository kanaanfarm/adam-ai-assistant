# Adam Acquisition v8.3.0.5 — Meeting Technical-Term Preservation Fix

## Physical issue fixed
The bilingual server transcription correctly heard mixed Arabic/English speech but could render English project terminology phonetically in Arabic script, e.g. `ميكانيكال دروينغ`.

## Fix
- Preserves the v8.3.0.4 microphone/VAD correction.
- Preserves the v8.3.0.3 hallucination and prompt-leak guards.
- Adds deterministic canonicalization for established meeting terms such as `mechanical drawing`, `shop drawing`, `RFI`, `HVAC`, `MEP`, `consultant`, `approved`, `revision`, `submission`, `contractor`, and `variation`.
- Does not translate or rewrite normal Arabic speech.
- Owner approval and meeting representative governance remain unchanged.

## Acceptance test
Say: `آدم شو صار بالـ mechanical drawing؟`
Expected transcript contains the literal English words `mechanical drawing`, not an Arabic-script phonetic rendering.

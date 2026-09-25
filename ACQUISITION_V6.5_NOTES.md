# Adam Acquisition v6.5.0 — Voice-First Adam

Adds a privacy-safe voice-first review boundary for personal use and buyer demos.

- Preserves Adam Lebanese Voice 2 + 4 identity across Lebanese Arabic, English, French and Spanish.
- Voice requests can be reviewed as read-only plans.
- Consequential voice requests require Owner Approval and explicit visible Text Confirmation before handoff to the existing governed execution boundary.
- The acceptance layer never executes a real external action.
- Existing `/api/tts` provider + Windows fallback remain the audio path.

Acceptance Tests: 206–207 only. Tests 1–205 remain locked PASS.

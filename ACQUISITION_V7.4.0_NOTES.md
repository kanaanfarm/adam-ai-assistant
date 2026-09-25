# Adam Acquisition v7.4.0 — Meeting Conversation Agent

- Adds Active Participant to the accepted Meeting Attendance UI.
- Keeps Listen Only and Take Notes modes.
- Active Participant uses preview-first response preparation.
- A separate Owner Approval is required before speech is authorized.
- Spoken responses are prefixed with Adam's AI identity when needed.
- Uses the existing `/api/tts` voice path with browser speech fallback.
- Does not claim or perform autonomous Teams/Zoom/Google Meet joining.
- Tests 233–234 cover the new/affected behavior only; earlier locked PASS tests are carried forward.

# Adam Acquisition v8.1.0.2 — Single Introduction Fix

- Guest conversations: Adam introduces himself only on the first Adam reply of the session.
- Later guest replies explicitly suppress repeated name / AI-role introductions unless the guest asks who Adam is.
- Meeting speaking flow: Adam declares AI identity on the first authorized speaking turn, then does not prepend the identity again during the same meeting session.
- Existing guest privacy, owner-approval, external-action, Lebanese Arabic, TTS, and continuous-listening safeguards remain unchanged.
- Focused regression: 4 tests passed.

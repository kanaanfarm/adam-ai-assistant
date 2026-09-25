# Adam Acquisition v8.1.0 — Secure Guest Voice Conversation

## Added

- Owner-approved temporary guest voice sessions with unguessable links and bounded expiry.
- Separate guest page for a second browser, phone, or computer on the same Wi-Fi.
- Topic-bounded AI conversation with ephemeral per-session context.
- Owner summary and manual session closure.
- Continuous speech recognition with interim transcription, a three-second silence window, manual Finish Speaking, automatic listening resume, and barge-in.

## Safety

- Guest sessions cannot access owner memory, contacts, messages, files, credentials, connectors, or trading.
- Consequential action requests are blocked and recorded for owner review.
- No session exists until Owner Approval creates a server-side token.
- Sessions and conversation history are process-local; restarting Adam revokes all links.
- No external action or network operation is performed by automated acceptance tests.

## Verification

- Only new and affected guest-session and continuous-listening behavior receives new acceptance tests.
- All earlier approved tests remain locked and are carried forward without repetition.

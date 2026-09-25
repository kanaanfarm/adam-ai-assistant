# Adam Acquisition v7.6.0 — Cross-App Personal Operator

This release adds one governed workflow surface spanning Contacts, Documents, Email, Calendar, WhatsApp, and Follow-up.

## What changed
- New **Cross-App Operator** entry on Adam main navigation.
- One workflow preview composes the selected contact, document reference, email, meeting, WhatsApp message, and follow-up.
- Preview is non-executing.
- Email, Calendar, WhatsApp, and Follow-up each retain a separate Owner Approval gate.
- Real Microsoft and WhatsApp actions only hand off when the connector is actually configured/connected.
- Document handling in this release is a reference/preparation step; it does not silently upload or transmit a document.
- Privacy-safe execution receipts contain domain/status only, not private message bodies or credentials.

## Acceptance boundary
Internal tests are synthetic and make no external network calls. Owner runtime acceptance should first verify preview and approval gating. Live external execution is optional and should only be used when the owner intentionally wants the action performed.

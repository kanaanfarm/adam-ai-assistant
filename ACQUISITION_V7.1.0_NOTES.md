# Adam Acquisition v7.1.0 — Real Services Connection

- Reuses the existing Microsoft/Outlook and WhatsApp connection implementations; no credential reset or connector rebuild.
- Adds a buyer-safe, presence-only status endpoint for Microsoft Outlook and WhatsApp Business.
- Adds a synthetic self-test proving connection-state projection, Owner Approval preservation, and live-trading block preservation.
- Status endpoint does not expose tokens, credentials, contacts, or message bodies and does not send email/WhatsApp messages.

Acceptance:
- Test 227: internal self-test/regression.
- Test 228: owner runtime status confirms the intended real services report CONNECTED/configured without sending a message.

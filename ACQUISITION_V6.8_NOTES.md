# Adam Acquisition v6.8.0 — WhatsApp Production Integration

Adds a governed production-integration layer over the existing WhatsApp Cloud transport.

- Separate Owner Approval and Live Execute gates.
- Blocks live handoff when WhatsApp configuration is not ready.
- Rejects credential-like content in the governed review boundary.
- Acceptance self-test uses synthetic inputs only and never contacts Meta or sends a real WhatsApp message.
- Existing WhatsApp Cloud transport and `/api/whatsapp/send` remain the actual execution boundary.

Acceptance: Tests 212–213.

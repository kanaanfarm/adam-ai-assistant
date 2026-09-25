# Adam Acquisition v2.3.0 — WhatsApp Cloud Transport Boundary

- Extracted WhatsApp Cloud API HTTP transport from `app.py` into `adam_core.whatsapp_cloud_transport`.
- Existing owner-approval adapter remains mandatory for `/api/whatsapp/send`.
- Existing WhatsApp configuration/webhook boundary remains unchanged.
- Added buyer-safe manifest, network-free self-test and download evidence endpoints.
- No access tokens, phone-number IDs, recipient values or message bodies are exposed by buyer evidence.

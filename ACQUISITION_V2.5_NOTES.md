# Adam Acquisition v2.5.0 — AI Provider Transport Boundary

- Extracted general text AI request construction and HTTP execution to `adam_core.ai_provider_transport`.
- Existing `call_ai` / `ai_text` callers remain compatible and delegate to the extracted transport.
- Added bounded token normalization and GPT-5 completion-token compatibility.
- Added buyer-safe manifest, self-test and downloadable evidence endpoints.
- Self-test uses injected fake HTTP transport: no API credential and no external network operation required.
- Buyer evidence excludes API keys, user/system prompt values, model response values and private memory.

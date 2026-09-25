# Adam Acquisition v2.4.0 — Vision AI Transport Boundary

- Extracts vision model selection, multimodal payload construction, image data-URL encoding, provider HTTP transport and response validation into `adam_core.vision_ai_transport`.
- Preserves existing camera and image attachment behavior.
- Uses injected HTTP transport so the boundary can be tested without a live AI provider or network operation.
- Buyer evidence exposes no API key, image bytes/data URLs, instruction values, model response values or private memory.
- Adds buyer-safe manifest, self-test and downloadable evidence endpoints plus Acquisition Center controls.

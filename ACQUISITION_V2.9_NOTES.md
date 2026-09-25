# Adam Acquisition v2.9.0 — Configuration Service Boundary

- Extracted AI provider configuration load/save from `app.py` into `adam_core.configuration`.
- Preserved environment fallback and existing AI Settings UI/API behavior.
- Added bounded 64 KB configuration files and atomic replacement writes.
- Malformed configuration safely falls back to environment configuration.
- Added buyer-safe manifest, network/application-data-free self-test, download endpoint and Acquisition Center controls.
- Evidence exposes configuration state/controls only, never API keys or configuration values.

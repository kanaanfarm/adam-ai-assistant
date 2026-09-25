# Adam Acquisition v2.7.0 — Workflow Persistence Service Boundary

- Extracted workflow JSON persistence into `adam_core.workflow_persistence`.
- Added bounded retention, bounded file size, atomic writes, malformed-store recovery and injected persistence path.
- Preserved legacy workflow load/save callers and orchestration behavior.
- Added buyer-safe manifest, SHA-256 fingerprint, network/application-data-free self-test and Acquisition Center controls.
- Buyer evidence exposes no workflow contents, instructions, attachment context, contacts, credentials or private memory.

# Adam Acquisition v2.6.0 — Audit Event Service Boundary

This release extracts Adam's legacy audit event record construction and JSONL persistence into `adam_core.audit_events` while preserving the existing `audit(event, details)` caller contract.

Buyer-safe evidence is provided by `adam_core.audit_boundary`. The evidence describes controls and fingerprints only; it does not expose operational audit-file contents, event-detail values, contacts, messages, credentials, or private memory.

New acceptance endpoints:
- `/api/acquisition/audit-event-boundary`
- `/api/acquisition/audit-event-boundary/self-test`
- `/api/acquisition/audit-event-boundary/download`

Next extraction targets: workflow persistence service boundary, voice AI transport boundary, configuration service boundary.

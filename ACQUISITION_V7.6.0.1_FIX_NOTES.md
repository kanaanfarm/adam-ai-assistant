# Adam Acquisition v7.6.0.1 — Cross-App Workflow Preview Validation Fix

- Separates planning-preview validity from execution readiness.
- Preview no longer fails merely because Microsoft/WhatsApp connectors are disconnected or Owner Approval is not yet granted.
- Incomplete execution-only details are reported under `execution_blockers` while the workflow plan can still return `ok: true`.
- Real execution remains strict: required action details, connector readiness, and per-action Owner Approval are still enforced.
- Preview remains non-executing and privacy-safe.

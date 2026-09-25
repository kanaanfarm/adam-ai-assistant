# Adam Acquisition v1.4.0 — Buyer Evidence Pack

## Purpose
Turn Adam's acquisition-readiness and governance data into a single buyer-safe diligence artifact that can be viewed or downloaded during a demo.

## Added
- `adam_core/evidence.py`
  - Privacy-safe evidence-pack builder
  - SHA-256 evidence fingerprint
  - Defensive privacy scan
- `GET /api/acquisition/evidence-pack`
- `GET /api/acquisition/evidence-pack/download`
- Acquisition Center buttons for viewing and downloading the evidence pack
- Buyer Evidence Pack explanation in the Acquisition Center

## Privacy boundary
The evidence pack deliberately excludes credentials, contact details, message bodies, attachment contents, prompts and private-memory values. Workflow evidence is limited to IDs, state/counters and existing receipt fingerprints.

## Acceptance focus
Only the new v1.4 evidence-pack functionality requires owner testing. Earlier approved checks should be carried forward rather than repeated.

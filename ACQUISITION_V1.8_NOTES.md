# Adam Acquisition v1.8.0 — Connector Execution Adapters

## Goal
Reduce buyer architecture risk by extracting owner-controlled execution validation for Outlook email, Outlook calendar and WhatsApp into pure tested core adapters while preserving the existing external transport callbacks.

## Changes
- Added `adam_core/connectors.py` with approval-gated, transport-injected email/calendar/WhatsApp adapters.
- Existing Flask routes remain the owner-facing API surface but delegate validation/execution control to the extracted module.
- Existing Outlook/Graph and WhatsApp Cloud transport implementations remain unchanged and are injected as callbacks.
- Added privacy-safe connector-boundary evidence and SHA-256 fingerprint.
- Added `/api/acquisition/connector-boundaries` and `/api/acquisition/connector-boundaries/download`.
- Added Connector Execution Adapters section to Acquisition Center.

## Safety
- No credentials are bundled or exposed by the new manifest.
- Consequential email/calendar/WhatsApp execution still requires explicit owner approval.
- Pure adapter policy can be tested without external credentials.

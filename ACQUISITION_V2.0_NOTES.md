# Adam Acquisition v2.0.0 — WhatsApp Configuration + Webhook Boundary

## Goal
Extract WhatsApp configuration persistence and webhook security/parsing from the legacy Flask application into tested `adam_core` services without changing the existing owner-facing WhatsApp routes.

## Added
- `adam_core/whatsapp_boundary.py`
  - configuration load/save with environment override support
  - masked-token preservation
  - public safe connection state
  - international number normalization
  - webhook verification challenge
  - HMAC SHA-256 webhook signature verification
  - incoming message projection
  - JSONL append helper
- `adam_core/whatsapp_boundary_evidence.py`
  - buyer-safe boundary manifest
  - privacy scan
  - credential-free/network-free self-test
- Buyer evidence routes:
  - `/api/acquisition/whatsapp-boundary`
  - `/api/acquisition/whatsapp-boundary/self-test`
  - `/api/acquisition/whatsapp-boundary/download`
- Acquisition Center section and controls for the new boundary.

## Preserved
- `/whatsapp`
- `/api/whatsapp/config`
- `/api/whatsapp/test`
- `/webhooks/whatsapp`
- `/api/whatsapp/inbox`
- `/api/whatsapp/draft`
- `/api/whatsapp/send`
- Existing WhatsApp Cloud transport remains in the legacy app for the next extraction step.

## Privacy / buyer evidence
The buyer-facing manifest exposes only safe booleans and API version state. It deliberately excludes access-token values, verify-token values, app-secret values, WhatsApp identifiers, contacts, message bodies, and private memory.

## Internal verification
Full test suite: **61 PASS, 2 skipped**. The skipped tests are Flask runtime integration checks unavailable in this build environment.

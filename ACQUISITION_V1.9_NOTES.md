# Adam Acquisition v1.9.0 — Microsoft Identity Boundary

## Goal
Continue reducing the legacy `app.py` boundary by isolating Microsoft identity persistence and device-flow state from Flask/MSAL transport logic.

## Changes
- Added `adam_core/microsoft_identity.py` for Microsoft client configuration persistence, serialized token-cache persistence and thread-safe device-flow state projection.
- Existing MSAL transport remains in `app.py`, but config/cache storage now delegates to the extracted core service.
- Added `adam_core/identity_boundary.py` with privacy-safe buyer evidence and SHA-256 fingerprinting.
- Added `/api/acquisition/identity-boundary`, `/api/acquisition/identity-boundary/self-test`, and `/api/acquisition/identity-boundary/download`.
- Added Microsoft Identity Boundary section and controls to the Acquisition Center.
- Updated architecture evidence to show the extraction and the next targets.

## Safety
- Buyer evidence exposes only boolean configuration state; never token values, client IDs, usernames, message content or credentials.
- The self-test performs no Microsoft login and no external network operation.
- Existing Microsoft connection, email and calendar routes remain preserved.

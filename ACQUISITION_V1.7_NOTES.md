# Adam Acquisition v1.7.0 — Service Boundary Extraction

## Objective
Continue architecture de-risking by moving stable Contacts and Follow-Up data behavior out of the legacy Flask application into independently testable core services.

## Changes
- Added `adam_core/contacts.py` for contact persistence validation and safe upsert behavior.
- Added `adam_core/followups.py` for follow-up persistence, due parsing, status calculation and public projection.
- Existing Flask routes now delegate to those service boundaries, preserving owner-facing behavior.
- Added `adam_core/service_boundaries.py` with privacy-safe, fingerprinted extraction evidence.
- Added `/api/acquisition/service-boundaries` and `/api/acquisition/service-boundaries/download`.
- Added Service Boundary Extraction evidence and controls to the Acquisition Center.
- Architecture manifest now tracks the extracted Contacts and Follow-Up services and identifies connector execution adapters as the next extraction target.

## Safety
The service-boundary evidence exposes no credentials, contact values, message bodies, attachment contents, prompts or private-memory values.

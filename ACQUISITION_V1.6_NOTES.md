# Adam Acquisition v1.6.0 — Architecture De-risking

## Objective
Reduce technical-diligence risk without disturbing the owner-approved operating workflows.

## Changes
- Added `adam_core/acquisition_facade.py` to centralize buyer-facing readiness, evidence and diligence assembly outside Flask route handlers.
- Added `adam_core/architecture.py` with a privacy-safe, fingerprinted architecture migration manifest.
- Added `/api/acquisition/architecture` and `/api/acquisition/architecture/download`.
- Added Architecture De-risking evidence to the Acquisition Center.
- Updated the diligence risk register to reference measurable modularization evidence while honestly keeping the remaining monolithic boundary as an attention item.
- Acquisition routes are now thin adapters over tested core services.

## Safety
No credentials, contacts, message bodies, attachment contents, prompts, or private-memory values are included in architecture evidence.

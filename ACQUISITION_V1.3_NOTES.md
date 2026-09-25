# Adam Acquisition v1.3.0 — Acquisition Demo + Readiness Layer

## Purpose
Turn the approved governance foundation into a buyer-facing diligence/demo surface that demonstrates Adam's product position, safety controls, governance evidence, integration readiness and three acquisition demo scenarios without exposing private data.

## Added
- `/acquisition` Acquisition Center UI.
- `/api/acquisition/readiness` buyer-safe capability/readiness manifest.
- `/api/acquisition/demo-scenarios` structured demo catalog.
- Three demo scenarios: Email + Document Operator, Cross-App Meeting Operator, Controlled Business Operator.
- Explicit privacy boundary for buyer-facing output.
- Updated architecture document for the current acquisition branch.

## Safety / privacy
The new layer exposes capability-level status only. It does not expose credentials, contact details, message bodies, attachment contents, prompts or private memory.

## Acceptance target
The Acquisition Center must load, report v1.3.0, show core readiness checks, governance evidence, privacy protections and all three demo scenarios. Existing v1.2.1 governance behavior must remain unchanged.

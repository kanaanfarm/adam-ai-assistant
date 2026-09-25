# Adam Acquisition v1.3.0 Architecture

## Runtime and product shell
- Flask application shell and cross-platform browser/PWA UI.
- Per-user runtime secret managed by `adam_core.runtime`; no predictable packaged Flask secret.
- AI-provider adapter and owner-controlled integration configuration.

## Core modules
- `adam_core.orchestration` — multi-step workflow lifecycle and approval/execution separation.
- `adam_core.governance` — buyer-safe policy manifest, workflow receipts, SHA-256 fingerprints and privacy filtering.
- `adam_core.acquisition` — buyer-facing readiness manifest and acquisition demo scenarios.
- `adam_core.diagnostics` — non-secret runtime/health status.

## Specialist capabilities
- Assistant, Email, Calendar, Contacts, Follow-Ups, Documents, Translation, Sales, WhatsApp, Calls, Voice and paper-market tools.

## Consequential-action controls
- Email review, WhatsApp review and calendar review require explicit owner approval.
- Approval and successful execution are separate recorded states.
- Follow-up-after-send requires successful delivery.
- Live-money trading remains blocked in the acquisition build.

## Buyer-safe evidence surfaces
- `/api/health`
- `/api/workflows`
- `/api/governance`
- `/api/governance/policy`
- `/api/governance/workflows/<workflow_id>`
- `/api/acquisition/readiness`
- `/api/acquisition/demo-scenarios`
- `/acquisition`

## Privacy boundary
The buyer-facing evidence layer does not expose credentials, contact details, message bodies, attachment contents, or private memory.

## v1.4 Buyer Evidence Layer
`adam_core/evidence.py` produces a privacy-safe diligence snapshot over readiness and governance metadata. The evidence pack has its own SHA-256 fingerprint and can be viewed or downloaded without exposing connector payloads or private user content.


## v1.6 Architecture De-risking
Acquisition payload assembly is centralized in `adam_core/acquisition_facade.py`. A buyer-safe architecture manifest in `adam_core/architecture.py` documents extracted modules, the remaining legacy boundary, migration controls and next extraction targets.

## v1.8.0 service-boundary extraction
Contacts persistence/upsert and Follow-Up persistence/due/status projection have been extracted into `adam_core.contacts` and `adam_core.followups`. The legacy Flask routes remain compatibility adapters so previously approved behavior is preserved while buyer-critical data services become independently testable. The next architecture target is connector execution isolation for email, calendar and WhatsApp.

## v1.9 Microsoft Identity Boundary
Microsoft client configuration persistence, serialized MSAL cache persistence and device-flow state projection have been moved behind `adam_core.microsoft_identity`. Flask/MSAL transport remains compatible with the existing routes while buyer evidence exposes only boolean configuration state and a privacy-safe fingerprint. Remaining extraction priorities: WhatsApp configuration/webhooks, document processing, then Microsoft Graph transport.

## v1.9 Microsoft Identity Boundary
Microsoft client configuration persistence, serialized MSAL cache persistence and device-flow state projection have been moved behind `adam_core.microsoft_identity`. Flask/MSAL transport remains compatible with the existing routes while buyer evidence exposes only boolean configuration state and a privacy-safe fingerprint. Remaining extraction priorities: WhatsApp configuration/webhooks, document processing, then Microsoft Graph transport.

## v2.0.0 — WhatsApp Configuration + Webhook Boundary
The WhatsApp configuration/webhook responsibility has been extracted from `app.py` into `adam_core.whatsapp_boundary`. Configuration persistence, environment overrides, challenge verification, HMAC signature verification and event projection are independently testable. The Cloud API network transport intentionally remains a separate future extraction target.

## v2.1.0 — Document Processing Boundary
Document and attachment classification, bounded local extraction, PDF/DOCX/XLSX/XLSM/text processing, DOCX rendering and analysis-prompt construction are now delegated to tested `adam_core.document_processing` services. Buyer-safe evidence and self-test routes are included.

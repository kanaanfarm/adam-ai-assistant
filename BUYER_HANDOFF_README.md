# Adam Acquisition — Buyer Handoff

Start with `ACQUISITION_V3.6_NOTES.md`, `ARCHITECTURE.md`, `AUDIT_STATUS.md`, and `.env.example`.

Buyer-safe evidence endpoints:
- `/api/acquisition/buyer-handoff`
- `/api/acquisition/buyer-handoff/self-test`
- `/api/acquisition/release-candidate`
- `/api/acquisition/technical-diligence-closeout`
- `/api/acquisition/demo-hardening`

Do not add deployment credentials to the distribution package. Buyer/deployer credentials belong only in the buyer-controlled deployment environment.

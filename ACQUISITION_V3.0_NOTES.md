# Adam Acquisition v3.0.0 — Owner Approval Persistence Boundary

- Added `adam_core.approval_persistence` with injected path, bounded retention/file size, malformed-store recovery and atomic writes.
- Explicit workflow approvals now also create a minimal persistent approval receipt.
- Existing workflow approval state remains authoritative for backward compatibility; no previously approved workflow is broken.
- Added privacy-safe buyer evidence, network/application-data-free self-test and JSON download routes.
- Buyer evidence exposes no workflow IDs, approval values, messages, contacts, credentials, private memory or approval-file contents.

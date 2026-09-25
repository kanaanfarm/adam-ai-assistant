# Adam Acquisition v1.2.0 — Governance + Auditability

This release builds on the owner-approved v1.1.3 checkpoint without changing the approved execution/approval behavior.

## Added
- Provider-neutral governance module (`adam_core/governance.py`).
- Buyer-safe `/api/governance` summary.
- `/api/governance/policy` showing Adam's consequential-action policy.
- Per-workflow `/api/governance/workflows/<id>` audit receipt.
- SHA-256 receipt fingerprint over privacy-safe workflow state and event metadata.
- Governance views intentionally exclude attachment bodies, credentials, arbitrary event details, email bodies, phone numbers and contact details.

## Acquisition value
This makes Adam's human-in-the-loop controls inspectable rather than only implicit in UI behavior. A buyer can see what requires owner approval, what completed, and a stable fingerprint of the privacy-safe execution record.

## Approval status
UNAPPROVED until owner acceptance. All 20 owner-approved v1.1.3 tests are carried forward; only the new v1.2 governance tests need owner verification.

# Adam Acquisition v1.2.1 — Governance Workflow Integration Fix

## Purpose
Fix the acceptance issue where real activity in Adam's Follow-Up Queue was not represented in `/api/governance`, leaving `workflow_count` at 0 and `receipts` empty.

## Changes
- Governance now combines orchestration workflows with Follow-Up Queue activity.
- Follow-ups are converted to privacy-safe workflow-shaped records.
- Follow-up governance IDs are prefixed with `followup_`.
- `/api/governance/workflows/<workflow_id>` can retrieve either an orchestration workflow receipt or a follow-up governance receipt.
- Added `record_sources` counts so buyers can distinguish orchestration workflows from follow-ups.
- Follow-up title, contact name, email, phone, message/draft body, and source are not exposed in governance receipts.
- Existing Follow-Up UI/behavior is unchanged.

## Acceptance target
After creating a follow-up, `/api/governance` must show `workflow_count >= 1`, `record_sources.followups >= 1`, and at least one receipt. Copy the returned `workflow_id` (for a follow-up it begins with `followup_`) into `/api/governance/workflows/<workflow_id>` and verify a 64-character `receipt_sha256`.

# Adam Acquisition v7.3.0.1 — Meeting Action Item Extraction Fix

## Affected behavior only
- Fixed manual meeting notes where valid action items could return `action_item_count: 0`.
- Recognizes explicit markers such as `Action:`, `Action item:`, `Todo:`, and `Follow-up:`.
- Recognizes natural commitments such as `Mohamad will send ...`.
- Recognizes concise manual imperative notes such as `provide latest shop drawing ...`.
- No external AI/network call is required for this deterministic extraction.
- Owner Approval, privacy boundaries, and the truthful no-autonomous-platform-join boundary are unchanged.

## Acceptance target
`Action: Mohamad will provide the latest HVAC shop drawing tomorrow.` must produce at least one action item.

## Regression
- 221 passed, 3 skipped, 0 failed.

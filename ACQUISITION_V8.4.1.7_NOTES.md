# Adam Acquisition v8.4.1.7 — Meeting Approval-Status Consistency Fix

## Purpose
This focused upgrade corrects the inconsistency observed in the v8.4.1.6 meeting report where the report could state **Owner approval required: No** while also saying the same technical change must be verified before Mohamad approves it.

## Changes
- Added an evidence-bounded owner-approval gate detector for paired meeting exchanges.
- Explicit references such as **before Mohamad approves**, **Mohamad's approval**, **owner approval**, **pending approval**, and approval-gated technical changes now set the retained meeting register to **Owner approval required = Yes**.
- A normal technical explanation does not create an owner-approval gate.
- Added aggregate owner-approval governance evidence to the report-generation prompt.
- Report generation is instructed to treat retained `Owner approval required: Yes/No` evidence as authoritative and not produce contradictory approval statements.
- Deterministic/fallback meeting reports use the same governance evidence.
- Meeting report API now returns `owner_approval_required_any`, `owner_approval_required_count`, and `approval_status_consistency_guard=true` for diagnostics.
- The working v8.4.1.5 AI-response path and v8.4.1.6 end-of-turn / technical transcript fixes are unchanged.

## Targeted owner acceptance test
Do not repeat the earlier speech/provider tests.

Use one meeting statement/question:

> Adam, the contractor wants to proceed with the 100 mm chilled-water pipe after hydraulic verification. Record it for my approval. What is your recommendation?

PASS requires:
- one direct question and one Adam response;
- no duplicate turn;
- the report must not say `Owner approval required: No` if it also says Mohamad approval is required;
- the item should remain open / pending verification and owner approval;
- no false technical approval is created.

Previously approved tests remain locked PASS unless directly affected by this reporting/classification change.

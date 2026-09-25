# Adam Acquisition v1.1.3 — Contact + Workflow Status Fix

## Acceptance focus
This patch is limited to the two remaining v1.1.2 acceptance items.

1. Follow-Up contact resolution now checks Adam Contacts when a natural-language follow-up is created.
2. Existing follow-ups with no linked email attempt a safe late contact resolution when **Prepare Follow-Up Email** is used.
3. Follow-Up cards explicitly show the linked contact or **Not linked to Adam Contacts**.
4. `/api/workflows` now returns the build version, workflow count, workflow state/events, and an explicit privacy flag confirming attachment context is not exposed.
5. Existing owner-approved PASS results remain carried forward.

Status: UNAPPROVED until owner retests Tests 18 and 20.

# Adam Acquisition v8.4.0.1 — Correction Isolation + Context Precision

## Why this fix was required
During the GPT validation, Adam correctly handled general knowledge, engineering reasoning, topic switching, short-term memory, missing-information behavior, disagreement, multi-topic separation and the owner's previously selected Arabic response language.

One issue remained: after the owner said:

> I didn't say third-water part. I said Empower request channel for chilled water.

Adam incorrectly attached the earlier `100 mm → 125 mm` pipe-size discussion to that correction even though the correction itself did not confirm that relationship.

## New affected behavior
- Explicit owner corrections are now treated as a **correction boundary** in `/api/chat`.
- A correction changes only the point the owner explicitly corrected.
- Adam must not attach nearby historical numbers, sizes, dates, people, projects, causes, approvals, scopes, actions or technical details unless the owner explicitly reconnects them.
- Conversation adjacency is not treated as confirmation.
- A fresh correction should be acknowledged minimally, using the owner's corrected wording without embellishing it with older details.
- Later summaries retain the newest correction boundary and must not reintroduce a superseded or unconfirmed association.
- The correction guard applies to the main Adam chat and to the Universal AI Assistant because both use `/api/chat`.
- Existing durable correction memory remains available, but durable correction text is not project evidence for associations the owner did not confirm.

## Expected behavior for the reported case
For:

> I didn't say third-water part. I said Empower request channel for chilled water.

A suitable reply is:

> Understood. The corrected point is: Empower request channel for chilled water. I will keep that wording and will not assume it is the same as the earlier 100 mm to 125 mm pipe-size discussion unless you confirm that link.

The exact wording may vary, but Adam must **not state that Empower requested the 100 mm to 125 mm change unless the owner explicitly confirms it**.

## Preserved behavior
- Language persistence remains unchanged and is not part of this fix.
- General GPT answers and topic switching remain unchanged.
- Generator capacity / other missing project data must not be invented.
- Durable owner memory remains explicit-only.
- Autonomous Meeting Attendance v8.4.0 preparation remains unchanged.
- Consequential actions and external commitments remain owner-approval gated.

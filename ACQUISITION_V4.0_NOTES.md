# Adam Acquisition v4.1.0 — Computer Use Agent Foundation

This upgrade starts Adam Computer Use without weakening the locked owner-control architecture.

## Added
- Computer-use action contract for observe/open/click/scroll/read/search.
- Consequential actions (submit/send/delete/purchase/confirm/upload/financial action) require explicit owner approval.
- Bounded task/action inputs.
- Injected driver interface so browser/desktop drivers can be added without putting policy inside the driver.
- Synthetic no-network self-test.
- Buyer-safe Acquisition Center evidence.

## Deliberately not enabled yet
Live desktop/browser control. The next build connects this governed boundary to a live browser driver and screen-perception loop.

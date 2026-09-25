# Adam Acquisition v4.3.0 — Cross-App Execution Orchestrator

## New capability
- Bounded cross-application workflow planning and execution foundation.
- Supported connector classes: browser, documents, email, calendar, WhatsApp.
- Read/prepare actions can execute through injected adapters.
- Consequential actions are blocked at the exact step unless Owner Approved.
- Buyer-safe receipts expose action classes/status only, not private values.

## Reliability cleanup
- The adaptive-recovery fixture URL now derives from Adam's actual runtime host/port instead of hard-coding port 8765.

## Acceptance policy
- Tests 1–161 remain locked PASS and are not repeated.
- Only new v4.3 behavior is tested in Tests 162–163.

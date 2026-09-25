# Adam Acquisition v4.8.1 — Acquisition Center UI + v4.8 Route Fix

Corrective build only. No new product capability phase and no duplicate acceptance tests.

Fixes:
- Repairs malformed Acquisition Center markup that closed the main wrapper/body before later evidence cards.
- Uses a wider responsive buyer-review layout so cards remain readable on large desktop displays and mobile screens.
- Adds the missing v4.8 Post-Meeting Cross-App Follow-Up card and interactive acceptance control.
- Registers the v4.8 acquisition endpoints before `app.run()` so they are available when Adam is launched directly on Windows.
- Keeps v4.8 Tests 172–173 as the only acceptance tests for this feature phase.

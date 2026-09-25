# Adam Acquisition v7.2.0.1 — Daily Assistant Route / Microsoft Status Fix

- Fixed the v7.2.0 route-registration defect that caused `/api/personal-assistant/real-daily-assistant` to return 404 even while `/api/health` reported v7.2.0.
- Moved Flask startup to the end of `app.py`, after the v7.2 Daily Assistant routes are registered.
- `/api/health` now reports `microsoft_client_configured` from the same persisted Microsoft connector configuration used by Adam, rather than relying only on an environment variable.
- Existing Microsoft/Outlook authentication and token mechanisms are reused unchanged; no credential values are exposed.
- No consequential action is performed by the Daily Assistant endpoint.

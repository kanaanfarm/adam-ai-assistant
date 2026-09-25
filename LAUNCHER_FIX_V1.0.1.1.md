# Adam Acquisition v1.0.1.1 — Launcher Fix

This patch changes only Windows startup behavior.

- Waits for `/api/health` to return HTTP 200 before opening the browser.
- Opens `http://127.0.0.1:8770/` automatically when Adam is actually ready.
- Keeps `app.py` and all Adam workflows unchanged.
- Includes a fallback browser open if a local health probe is blocked.

Use `START_ADAM_ACQUISITION.bat` to launch Adam.

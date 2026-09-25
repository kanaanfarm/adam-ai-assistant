# Adam Acquisition v8.2.0.6 — Guest Gateway Launch Fix

- Fixes Windows launcher quoting that could prevent guest_gateway.py from starting.
- Starts the gateway directly with Python using an absolute path.
- Verifies http://127.0.0.1:8771/health before starting cloudflared.
- If gateway startup fails, opens a visible diagnostic window instead of silently waiting.
- Preserves v8.2.0 intelligence, Guest Voice privacy boundaries, and trusted HTTPS tunnel design.

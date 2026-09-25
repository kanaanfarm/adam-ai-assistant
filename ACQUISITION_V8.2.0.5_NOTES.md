# Adam Acquisition v8.2.0.5 — Mobile HTTPS Tunnel Startup Fix

- Makes the Cloudflare Guest Voice tunnel launcher visible instead of hidden.
- Uses installed cloudflared when available; otherwise tries curl.exe then PowerShell download.
- Validates the tunnel helper and Guest Voice gateway before exposure.
- Publishes explicit tunnel states: starting, downloading, ready, or error.
- Guest Voice owner page shows the exact failure instead of remaining at “Starting…” forever.
- Secure mobile guest link creation waits for trusted HTTPS READY.
- Owner UI remains local HTTP on 127.0.0.1:8770.
- Guest-only gateway remains isolated on 127.0.0.1:8771.

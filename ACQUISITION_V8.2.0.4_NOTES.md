# Adam Acquisition v8.2.0.4 — Mobile Guest Voice Access Fix

This release corrects the remaining iPhone Guest Voice blocker without forcing self-signed HTTPS on the owner laptop.

## Architecture
- Owner UI stays local: `http://127.0.0.1:8770`.
- A separate Guest Voice-only gateway runs on `127.0.0.1:8771`.
- A Cloudflare Quick Tunnel creates a normal browser-trusted `https://*.trycloudflare.com` URL for mobile testing.
- Adam reads the generated HTTPS base URL from `data/guest_public_base_url.txt` and uses it when creating guest sessions.
- The public gateway blocks the owner UI and every non-Guest-Voice route.
- `/api/tts` on the gateway requires an active temporary guest token.

## First run
The helper downloads `cloudflared.exe` from Cloudflare's official GitHub release if it is not already present. Internet access is required for this test tunnel.

Quick Tunnels are for testing. A commercial deployment should use a controlled domain/tunnel configuration rather than the temporary `trycloudflare.com` URL.

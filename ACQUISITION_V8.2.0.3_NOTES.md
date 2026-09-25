# Adam Acquisition v8.2.0.3 — Trusted Guest Voice Access

- Restores owner UI to `http://127.0.0.1:8770` so the laptop opens without self-signed certificate warnings.
- Keeps the v8.2.0.2 local HTTPS code available only when explicitly enabled with `ADAM_LOCAL_HTTPS=true`.
- Adds `ADAM_GUEST_PUBLIC_BASE_URL` for a normal publicly trusted HTTPS reverse-proxy/tunnel/domain.
- Guest Voice session creation prefers `trusted_guest_url` when configured.
- Does not pretend an HTTP LAN URL can provide iPhone microphone access.
- Preserves v8.2.0 advanced intelligence, voice fallback, privacy, and owner-approval boundaries.

Example environment value (must be your real trusted HTTPS endpoint):
`ADAM_GUEST_PUBLIC_BASE_URL=https://your-real-trusted-host.example`

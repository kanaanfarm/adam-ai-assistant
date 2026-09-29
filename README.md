# ADAM Telnyx Public Webhook Fix V2

Fixes the `Unauthorized` response after the first Telnyx two-way voice upgrade.

This does NOT disable ADAM authentication globally. It bypasses the existing browser/owner auth guard only for:
- `/api/telnyx/voice/webhook`
- `/api/telnyx/voice/readiness`

The webhook itself remains protected by `TELNYX_WEBHOOK_TOKEN`.

## Apply
1. Put `APPLY_TELNYX_PUBLIC_WEBHOOK_FIX.py` in the current ADAM repository root.
2. Run: `python APPLY_TELNYX_PUBLIC_WEBHOOK_FIX.py`
3. Upload/commit the modified `app.py` to GitHub.
4. Wait for Render deployment success.

## Verify — no paid call yet
Open:
`https://adam-ai-assistant.onrender.com/api/telnyx/voice/readiness`

Expected:
- `two_way_voice_code_installed: true`
- `webhook_token_configured: true`

Do not put your Telnyx API key or webhook token in GitHub.

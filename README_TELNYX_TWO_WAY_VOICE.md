# ADAM Telnyx Two-Way Voice Upgrade

## Apply
1. Download your current ADAM repository from GitHub.
2. Copy this ZIP's contents into the repository root.
3. Run: `python APPLY_TELNYX_VOICE_UPGRADE.py`
4. Upload/commit the changed repository to GitHub and let Render redeploy.

## Render variables
Keep your existing TELNYX_API_KEY, TELNYX_CONNECTION_ID and TELNYX_FROM_NUMBER.

Add:
- TELNYX_WEBHOOK_TOKEN = a long random private value
- TELNYX_STT_LANGUAGE = en
- TELNYX_TTS_LANGUAGE = en-US
- TELNYX_TTS_VOICE = Polly.Brian

Never put API keys or the webhook token in GitHub.

## Telnyx Voice API Application webhook
After deployment set the webhook to:
`https://YOUR-RENDER-HOST/api/telnyx/voice/webhook?token=YOUR_PRIVATE_WEBHOOK_TOKEN`

Use POST and Webhook API V2.

## Check before another paid call
Open:
`https://YOUR-RENDER-HOST/api/telnyx/voice/readiness`

Confirm:
- two_way_voice_code_installed = true
- webhook_token_configured = true

Then make only one short test call and say:
`Hello Adam, can you hear me?`

This first version uses Telnyx Call Control transcription + Speak, not raw WebSocket audio. It is intentionally simpler for the first two-way voice test and may incur Telnyx transcription/call usage charges.

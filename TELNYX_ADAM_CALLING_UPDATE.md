# ADAM Telnyx Outbound Calling Update

Added safe outbound call origination through Telnyx.

Required Render environment variables:
- TELNYX_API_KEY
- TELNYX_OUTBOUND_PROFILE_ID
- TELNYX_FROM_NUMBER

Main chat now recognizes explicit call/dial requests, resolves a saved contact phone number (or an explicit international number), and displays an Owner Review card. No call is placed until the owner checks approval and presses **Call Now**.

This release provides the outbound dialing foundation only. Full two-way live AI conversation (remote caller speech recognition + ADAM voice responses over the phone media stream) is the next stage and is not falsely claimed by this package.

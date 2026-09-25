# Adam Acquisition v3.1.0 — Windows Speech Fallback Boundary

This release extracts the local Windows `System.Speech` fallback from the Flask application into `adam_core.windows_speech_fallback`.

## New in v3.1.0
- Bounded local speech input (4096 characters).
- Windows-only platform guard.
- Injected subprocess runner for network-free, PowerShell-free automated testing.
- Temporary input/output files are cleaned after success or failure.
- WAV output is validated before returning audio.
- Provider/subprocess error details are sanitized.
- Buyer-safe manifest, self-test and download endpoints are available in Acquisition Center.

## Acceptance scope
No previously approved workflow, connector, document, configuration, approval or cloud voice tests are repeated. Owner retest is limited to the newly extracted Windows speech fallback and its buyer-evidence controls.

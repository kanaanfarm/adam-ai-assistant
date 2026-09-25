# Adam Acquisition v7.0.1 — Stock Notification Stability Fix

This maintenance release fixes repeated stock voice updates before Production Readiness begins.

## Changes
- Default notification mode is **Once per signal**.
- The same important signal is not spoken repeatedly every two-minute refresh.
- A temporary no-alert cycle does not reset/re-arm the previous important signal.
- User-selectable modes: Off, Once per signal, Status changes only, Every check (explicit opt-in).
- Voice alerts remain independently switchable; visual stock status continues updating.
- Automatic dashboard refresh is silent by default; repeated voice is never forced by the timer.
- Preferences persist in browser localStorage.
- No change to trading execution: PAPER-only controls remain and live trading remains blocked.

## Acceptance boundary
Synthetic notification-policy self-test only. No real market access or order submission is required.

# Adam Acquisition v7.0.1.2 — Manual Trade Override UI Fix

Fixes the Stock page so the governed Manual Trade Override panel is always mounted visibly in the full Stock workspace.

- Dedicated Manual Trade mount on `/stock`.
- FORCE BUY / FORCE SELL panel forced visible after page relocation.
- Explicit `Alpaca Paper Account: CONNECTED / NOT CONNECTED` indicator.
- Existing Owner Approval + Final Confirmation gates preserved.
- PAPER-only enforcement preserved; live trading remains blocked.
- No new execution capability added.

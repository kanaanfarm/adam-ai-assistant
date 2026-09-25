# Adam Acquisition v8.0.0.1

## Stock Once-per-Signal Voice Fix

- Fixes repeated voice announcements for the same stock action during the automatic two-minute refresh.
- Uses a stable `SYMBOL + ACTION` identity, so changing prices, percentages, and reason text update visually without re-triggering speech.
- Persists a bounded set of the latest 200 announced signal identities in browser storage.
- Speaks all genuinely new signals in one notification and suppresses previously announced signals.
- Preserves owner-selected notification modes: Off, Once per signal, Status change, and Every check.
- Does not place orders, access live trading, or weaken Owner Approval controls.

## Verification

- Owner runtime confirmation: MSFT and TSLA alerts were not repeated after automatic refresh.
- Test 219: PASS & LOCKED.
- Automated regression: 256 passed, 3 skipped, 0 failed.

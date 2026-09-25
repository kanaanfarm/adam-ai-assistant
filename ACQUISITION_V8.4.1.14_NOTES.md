# Adam Acquisition v8.4.1.14 — Dynamic Stock Universe & Custom Ticker Scan

## Purpose
Remove the fixed AAPL/MSFT/NVDA/TSLA-style scan limitation from the Stock Command Center while preserving paper-trading and owner-approval controls.

## Changes
- Added selectable stock scan universes: **Core 10**, **Broad 50**, and **Broad 100**.
- Added an **Add symbols** field so the owner can scan arbitrary Alpaca-compatible tickers (for example AMZN, META, PLTR, SHOP, CRWD).
- Existing held positions are automatically included in the scan even if they are outside the selected universe.
- SPY remains a market-regime reference and is not treated as a normal buy candidate.
- Broad scans now run concurrently (up to 12 workers) instead of one symbol at a time.
- `/api/stock/main-summary` accepts `universe` and optional `watchlist` parameters.
- `/api/stock/agent-cycle` accepts the same dynamic universe selection.
- Dashboard reports the selected universe and requested scan-symbol count.

## Governance preserved
- Paper mode only.
- Explicit owner approval is still required before any order.
- Existing $500 paper safety limit, $100 max new position, max-position and stop/take-profit rules remain unchanged.
- No autonomous live order execution was added.

## Verification
- 6/6 v8.4.1.14 targeted tests PASS.
- Python compile PASS.
- Stock page JavaScript syntax PASS.
- Main page JavaScript syntax PASS.
- Previous locked meeting/voice/report PASS behavior was not changed.

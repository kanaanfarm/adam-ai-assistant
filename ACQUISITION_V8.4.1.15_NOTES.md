# Adam Acquisition v8.4.1.15 — Top Opportunity Ranking & BUY-Readiness Score

Built from the owner-approved v8.4.1.14 dynamic-universe baseline.

## What changed
- Adam now computes an `opportunity_score` (0–100) for each scanned stock candidate.
- The score is a ranking/triage aid only; it does not replace or override the existing BUY / WAIT / HOLD signal rules.
- Ranking considers existing confidence, SMA5/SMA20 trend and spread, RSI quality, existing BUY signal, and SPY market regime.
- New-stock candidates are sorted by Opportunity Score so the strongest/closest setups appear first even when all candidates remain WAIT.
- The Stock page now shows the Top 10 opportunities instead of 8.
- Each card displays `Opportunity Score N/100` plus a readiness label: VERY CLOSE, CLOSE, WATCH, or WEAK.
- Held positions and SPY remain visible in the returned scan data but do not displace the strongest new-stock opportunities.

## Safety / governance preserved
- Paper trading only.
- No order is placed by the ranking score.
- Explicit owner approval remains required for paper orders.
- Existing $500 exposure cap, $100 max new position, max-position rules, take-profit/stop-loss logic, and dynamic stock universe behavior are unchanged.
- v8.4.1.13.2 remains the locked meeting baseline carried forward unchanged.

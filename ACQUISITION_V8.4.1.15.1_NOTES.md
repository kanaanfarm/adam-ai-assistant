# Adam Acquisition v8.4.1.15.1 — Opportunity Score Normalization Fix

Built from the owner-approved v8.4.1.15 Top Opportunity Ranking baseline.

## Fix
The v8.4.1.15 opportunity score could saturate at 100/100 for many different stocks because the raw confidence value was used as the base and then multiple bonuses were added before clamping at 100. This made the ranking visually misleading even though BUY/WAIT/HOLD governance remained correct.

v8.4.1.15.1 replaces that with bounded sub-scores:
- Confidence: up to 55 points
- SMA trend/separation: up to 20 points
- RSI quality: up to 15 points
- Existing BUY signal: up to 5 points
- Market regime: +5 bullish / 0 mixed / -8 bearish

The score remains presentation/triage only. It does not create a BUY signal, bypass WAIT/HOLD logic, alter paper-trading mode, or change owner approval and safety limits.

## Preserved
- v8.4.1.14 dynamic Core 10 / Broad 50 / Broad 100 universe
- Custom ticker scan
- Held-position inclusion
- Top 10 opportunity display
- Existing BUY/WAIT/HOLD rules
- Paper trading only
- Explicit owner approval
- $500 exposure cap
- $100 max new position
- Existing stop-loss / take-profit / max-position governance

## Verification
Targeted normalization tests plus syntax/package checks are included with this build.

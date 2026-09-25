# Adam Acquisition — Pre-Sale Audit

Status: PASS after sanitation
Source release: v3.6.0 (locked 154/154 owner acceptance)
Purpose: buyer-distribution privacy, credential, stock-safety, and regression gate.

## Findings and actions
- No `.env`, private key, token cache, database, log, or credential file is bundled.
- No live Alpaca credentials were found in the distribution.
- A personal contact example was found in README and was replaced with synthetic buyer-safe data.
- Personal-name examples in comments/UI placeholders were replaced with synthetic examples.
- Alpaca stock execution remains hard-bound to `https://paper-api.alpaca.markets`.
- The application raises `Real-money trading is blocked. Only Alpaca Paper Trading is allowed.` for a non-paper base URL.
- Automated regression after sanitation: 116 passed, 3 skipped, 0 failures.

## Distribution rule
Buyer/deployer credentials must be supplied only in the buyer deployment environment. Do not add local `.env` or token/cache/data files to this package.

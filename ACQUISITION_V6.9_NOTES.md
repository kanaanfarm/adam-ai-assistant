# Adam Acquisition v6.9.0 — Stock Intelligence Assistant

Adds a governed read-only stock intelligence layer above Adam's existing Alpaca PAPER market/trading module.

- Computes deterministic SMA5, SMA20 and RSI14 from supplied market history.
- Adds position/average-entry context and an intelligence recommendation.
- Buy/sell instructions require Owner Approval before a separate PAPER-trade review handoff.
- This v6.9 boundary has no order-submission capability.
- Live trading remains explicitly blocked.
- Acceptance self-test uses synthetic market/portfolio inputs only; no network or market API calls.
- Sensitive credential-like instructions are rejected.

Acceptance: Tests 214–215.

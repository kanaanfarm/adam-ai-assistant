# Adam Acquisition v7.0.1.1 — Manual Trade Override

Adds an owner-directed FORCE BUY / FORCE SELL control to the Stock page for **Alpaca Paper Trading only**.

Safety and behavior:
- Manual override is clearly marked as overriding Adam's recommendation.
- Owner Approval checkbox is mandatory.
- A separate browser final confirmation is mandatory.
- FORCE BUY supports $1–$500 notional through the existing PAPER-only order endpoint.
- FORCE SELL uses the existing governed paper agent-action endpoint and cannot exceed the open paper position.
- Live-money trading remains blocked by `require_paper_alpaca()`.
- Acceptance self-test is synthetic and submits no order / performs no network access.

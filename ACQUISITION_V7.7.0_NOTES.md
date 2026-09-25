# Adam Acquisition v7.7.0 — Production Reliability

- Adds bounded retry and reconnect recovery for read-only connector probes.
- Adds explicit timeout and maximum-attempt policy reporting.
- Prevents automatic replay of consequential actions after ambiguous timeouts, avoiding duplicate email, calendar, WhatsApp, call, or trade actions.
- Adds a bounded long-running stability window with success-rate and p95 latency evidence.
- Adds a Production Reliability page with a synthetic, no-network self-test.
- Preserves Owner Approval, live-trading protection, and all existing Microsoft/WhatsApp connector configuration.

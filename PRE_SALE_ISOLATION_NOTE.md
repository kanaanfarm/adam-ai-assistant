# Pre-Sale Buyer Isolation

This buyer distribution uses an isolated local application-data namespace: `Adam_Acquisition`.

By default it does **not** import contacts, Microsoft client configuration, Microsoft token caches, or other legacy owner state from prior Personal AI Assistant / Adam installations.

Legacy migration is disabled by default. It can only be intentionally enabled by the deployer with `ADAM_ALLOW_LEGACY_MIGRATION=true`.

Expected first-run state on a clean buyer installation:
- Microsoft: not connected; buyer supplies their own application/client configuration and signs in.
- Alpaca: not configured; buyer supplies Paper Trading credentials only.
- AI provider: not configured until buyer supplies configuration.
- Contacts: empty unless buyer creates/imports their own data.

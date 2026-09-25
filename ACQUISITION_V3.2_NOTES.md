# Adam Acquisition v3.2.0 — Runtime Configuration Consolidation

This release centralizes runtime environment lookups for AI provider defaults, vision model selection, Alpaca credentials and Microsoft client ID behind `adam_core.runtime_configuration`. Buyer-facing evidence reports configuration presence only and never secret values.

## Acceptance scope
Only the new runtime-configuration consolidation needs owner acceptance. Previously approved voice, workflow, connector, document, approval and persistence tests are not repeated.

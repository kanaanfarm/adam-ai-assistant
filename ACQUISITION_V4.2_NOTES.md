# Adam Acquisition v4.2.0 — Screen Perception + Adaptive Recovery

New behavior only:
- Semantic inventory of visible interactive browser elements.
- Does not read form/input values.
- Adaptive click recovery when a primary CSS selector is missing.
- Bounded fallback selectors and visible-text hint recovery.
- Owner approval is re-evaluated on the recovered target; recovery never bypasses the consequential-action gate.
- Buyer evidence exposes capabilities and booleans only, not page contents, URLs, typed values or credentials.

Previously approved v4.1 live-browser behavior remains locked and is not retested as an acceptance requirement.


## v4.2.1 corrective build
- Replaced brittle third-party acceptance dependency with deterministic local recovery fixture.
- Added local fixture URL `/computer-use-recovery-fixture` and success page.
- Added privacy-safe diagnostic booleans (`text_hint_used`, selector candidate count) on recovery results.
- Test 160 remains locked PASS; only affected Test 161 is repeated.

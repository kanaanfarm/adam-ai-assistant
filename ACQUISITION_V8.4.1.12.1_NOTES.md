# Adam Acquisition v8.4.1.12.1 — Supported Reasoning Effort Compatibility Fix

## Physical failure isolated
The v8.4.1.12 factual fast path sent `reasoning.effort = minimal`. The deployed GPT-5.6 provider rejected that value with HTTP 400 and explicitly reported these supported values: `none`, `low`, `medium`, `high`, `xhigh`.

## Narrow fix
- Fast self-contained factual meeting path now uses `reasoning.effort = none`.
- Governed/non-fast meeting path remains `low`.
- The 160-token factual output budget remains unchanged.
- No changes to end-of-turn timing, STT, focus/merge, prompt classification, approval/clarification governance, meeting memory/session isolation, or voice delivery.

## Acceptance
Repeat one short factual meeting question. Expected: no provider 400; trace reaches AI response and spoken reply; latency line remains populated.

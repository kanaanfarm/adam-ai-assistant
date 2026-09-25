# Adam Acquisition v8.4.1.5 — Meeting Prompt Runtime Fix

## Why this upgrade
The v8.4.1.4 screenshot proved the AI provider connection itself was healthy while the meeting request failed. Source inspection identified the exact meeting-only defect: two places inside the representative prompt expression had a trailing binary `+` followed immediately by another leading `+`. Python interpreted the second operator as unary plus on a string and raised `TypeError` before `call_ai()` could run.

## Changes
- Removed both duplicate `+` boundaries in the meeting prompt construction path.
- The accepted participant turn remains persisted before AI dispatch.
- Provider transport, GPT-5.x Responses handling, persistent AI settings, duplicate suppression, owner approval, and voice behavior are unchanged.
- Updated the owner-facing generic diagnostic wording so a passing AI connection test identifies a meeting server-path failure rather than blaming provider configuration.
- Added a runtime prompt-expression regression test that executes the actual prompt expression for three affected paths: direct question, correction/order-style interaction, and proactive addressed comment.
- Added an AST guard that fails if unary `+` appears anywhere in the meeting prompt expression.

## Targeted owner test only
1. Start v8.4.1.5.
2. If AI Settings already shows `AI connection successful`, do not change the provider settings.
3. Open Real Meeting Attendance and ask once: `Adam, what is the function of a water pump?`
4. PASS trace: `1 speech accepted -> 2 representative dispatch started -> 3 waiting for AI provider -> 4 AI response received -> 5 spoken reply completed`.
5. PASS record: one accepted question, one Adam reply, one paired discussion record, no duplicate and no false background filtering.

Previously approved tests stay locked. Retest only this affected meeting-response path.

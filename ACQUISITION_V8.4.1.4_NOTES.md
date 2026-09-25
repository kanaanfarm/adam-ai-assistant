# Adam Acquisition v8.4.1.4 — Persistent AI Settings + Provider Diagnostic Fix

## Why this upgrade
The v8.4.1.3 meeting trace now correctly retained the accepted question but the browser still reported a generic `AI request failed`, which did not identify whether the failure was caused by a missing migrated API key, an old full endpoint URL, model/access, authentication, quota, or a server-side meeting-only failure.

## Changes
- AI provider settings now live in Adam's per-user runtime root and survive extracted-folder upgrades.
- One-time bounded migration recovers an existing `data/ai_settings.json` from the current or sibling Adam package when available.
- Provider URLs are normalized: saved `/chat/completions`, `/responses`, or `/completions` suffixes are stripped before Adam appends the endpoint required by the selected model.
- Official OpenAI Responses requests explicitly use `store: false`.
- `Test Connection` returns owner-safe diagnostics (configured flags, model, error type/message) without returning the API key.
- If a meeting request fails generically, the meeting page automatically runs the provider test and shows the actual provider error.
- Existing accepted-turn persistence, duplicate suppression, question retention, owner approval boundaries, and provider watchdog remain unchanged.

## Targeted owner test only
1. Start v8.4.1.4.
2. Open AI Settings and click **Test Connection** once. It must show `AI connection successful`.
3. Open Real Meeting Attendance and ask once: `Adam, what is the function of a water pump?`
4. PASS: one accepted question, one AI response, one spoken reply, one paired record, no duplicate, no false background filtering.
5. If it fails, photograph the visible provider diagnostic; the exact cause will now be shown.

# Adam Acquisition v8.4.1.3 — Meeting AI Provider Responses Fix

This is a focused affected-path upgrade on top of v8.4.1.2.

## Fixed
- Official OpenAI GPT-5.x text calls now use the **Responses API** instead of forcing GPT-5.6 through the legacy Chat Completions path.
- GPT-5.x provider calls use low reasoning effort for live-meeting latency while preserving the configured model.
- Custom OpenAI-compatible providers keep the legacy Chat Completions transport for compatibility.
- The meeting browser now has a 30-second request watchdog, so the UI cannot remain indefinitely at `waiting for AI provider`.
- Provider timeout/error states are shown explicitly and the accepted question remains retained without creating a duplicate.

## Targeted owner test only
Ask once: `Adam, what is the function of a chilled water pump?`

PASS requires:
1. speech accepted,
2. representative dispatch started,
3. AI response received,
4. spoken reply completed (or reply recorded if audio is unavailable),
5. one question and one paired Adam response,
6. no duplicate question,
7. no false background filtering.

If the provider itself is unavailable, the trace must end in an explicit timeout/error instead of remaining permanently at step 3.

Previously approved tests remain locked PASS and should not be repeated.

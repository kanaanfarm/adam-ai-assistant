# Adam Acquisition v8.4.1.13.2 — Adam Recommendation Count Consistency Fix

## Scope
This is a narrow reporting-metadata fix built on v8.4.1.13.1.

## Fix
- The Analyze Meeting Notes status summary previously counted Adam recommendations only from retained `action_origin` records.
- A professional report could therefore visibly contain several bullets under **ADAM RECOMMENDATIONS** while the summary still displayed `0 Adam recommendation(s)`.
- v8.4.1.13.2 now counts the concrete bullet/numbered entries rendered under **ADAM RECOMMENDATIONS** in the final reconciled report.
- If the report section has no list entries, the retained-record count remains the fallback.
- Diagnostic fields expose the visible count, retained-record count, and which source supplied the displayed count.

## Preserved behavior
No changes to microphone/STT, end-turn detection, latency fast path, AI reasoning profile, TTS/voice, focused-order coverage, clarification/approval governance, meeting memory/session isolation, report display, or participant action attribution.

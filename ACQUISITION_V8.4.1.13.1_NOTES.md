# Adam Acquisition v8.4.1.13.1

## Analyze Meeting Notes Report Display Fix

### Problem
In v8.4.1.13, the **Analyze Meeting Notes** button ran the attendance-processing endpoint and displayed only the diagnostic JSON result (for example `status: attendance_processed`). The professional meeting report already existed behind `/api/personal-assistant/meeting-conversation/report`, but the Analyze button did not call it or show it.

### Fix
The Analyze Meeting Notes button now:
1. Runs the existing attendance processing step.
2. Calls the existing governed meeting-report endpoint for the active meeting session.
3. Places the full professional report into the existing **Professional Meeting Report** box.
4. Replaces the raw attendance JSON display with a concise report-ready status summary.
5. Scrolls the report into view automatically.

The report includes the existing sections such as EXECUTIVE SUMMARY, ACTION ITEMS, ADAM RECOMMENDATIONS, OPEN / UNRESOLVED ITEMS, QUESTION COVERAGE / UNANSWERED ITEMS, and NEXT STEPS.

### Preserved behavior
No changes were made to microphone capture, STT, end-of-turn timing, fast factual AI path, reasoning effort, TTS/voice, focused-order/recommendation coverage, owner-approval/clarification governance, meeting memory, project/session isolation, or the v8.4.1.13 action-attribution reconciliation.

### Verification
- 9/9 new targeted tests PASS
- Python compile PASS
- Meeting-page JavaScript syntax PASS
- Locked 4200 ms protected silence boundary preserved
- Locked 2400 ms fast silence boundary preserved
- 12000 ms fast-turn speech span preserved
- Fast factual reasoning compatibility (`none` / governed `low`) preserved
- v8.4.1.13 ACTION ITEMS / NEXT STEPS attribution markers preserved

# Adam Acquisition v8.4.1.13

## Meeting Report Action Attribution Consistency Fix

This upgrade closes the remaining report-consistency issue seen during contractor/meeting tests: a report could say **No participant-assigned actions were recorded** while wording under **NEXT STEPS** appeared to assign work to Adam.

### Changes
- Added deterministic report post-processing based on retained `action_origin` evidence.
- `ACTION ITEMS` now contains only records explicitly classified as **Participant-assigned action**.
- If there are no participant-assigned actions, the section is forced to: `No participant-assigned actions were recorded.`
- `NEXT STEPS` is explicitly labeled as recommended follow-up, not a participant-assigned action, when no participant action exists.
- Added report metadata:
  - `participant_assigned_action_count`
  - `adam_recommendation_count`
  - `action_attribution_consistent=true`
  - `report_action_attribution_consistency_guard=true`

### Preserved behavior
No changes were made to microphone/STT, end-of-turn detection, fast factual AI path, reasoning effort, TTS/voice playback, focused order/recommendation coverage, clarification handling, approval governance, meeting memory, or session isolation.

### Physical acceptance test
Generate a meeting report after a discussion where Adam makes recommendations but the participant assigns no explicit action. Confirm:
1. `ACTION ITEMS` says no participant-assigned actions were recorded.
2. `NEXT STEPS` is clearly marked as recommended follow-up only, not an assigned action.

Previous owner-approved tests remain locked PASS and do not need to be repeated.

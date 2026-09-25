# Adam Acquisition v8.4.0.2 — Typed Meeting Query Dispatch Fix

## Why this fix was required
On the Real Meeting Attendance page, the **Live transcript / manual notes** box can display or hold text, but manually typing a question into that transcript box did not itself dispatch the question to Adam. This could look like Adam heard the query but did not answer.

## New behavior
- A dedicated **Typed meeting query / comment / order** field is now placed directly below the live transcript.
- Press **Enter** or click **Send Typed Query**.
- Typed meeting input enters the same meeting pipeline as accepted microphone speech:
  - Meeting Focus / project isolation
  - wake-name and question-preamble turn awareness
  - meeting memory
  - question coverage
  - correction/order classification
  - representative owner-approval gate
  - consequential-action safety boundaries
- Voice operation is unchanged.
- The original transcript box remains available for transcript/manual notes and is not treated as an automatic command surface.

## Physical test
1. Select **Owner Representative — Rehearsal**.
2. Check the top **Owner Approval** box.
3. In **Typed meeting query / comment / order**, type:
   `The contractor wants to increase the chilled-water pipe from 100 mm to 125 mm. What do you think?`
4. Press Enter or click **Send Typed Query**.
5. Adam should answer and the turn should appear in the meeting discussion/coverage records.

No previous approved behavior was intentionally changed.

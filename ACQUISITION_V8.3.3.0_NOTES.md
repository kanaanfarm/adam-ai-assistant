# Adam Acquisition v8.3.3.0

## Human Meeting Presence + Intelligent Meeting Focus

This release moves Adam from “hear every room sentence and decide whether to answer” toward a professional representative who stays anchored to the meeting he is attending.

### New: Meeting Focus Lock

- **Meeting Focus Lock is ON by default in Owner Representative mode.**
- Default sensitivity is **Strict — shared room / nearby conversations**.
- Adam evaluates each transcribed utterance against:
  - meeting title,
  - project/reference,
  - declared participants/companies,
  - optional meeting focus/agenda keywords,
  - owner briefing,
  - the current accepted meeting discussion,
  - immediate follow-up context,
  - a weak near-field audio signal hint.
- Likely side-room / other-project speech is filtered **before it is added to the formal meeting transcript, retained meeting memory, Q&A history, question coverage, or report**.
- Rejected focus-history events retain only decision metadata (score/reason), not the rejected conversation text.

### New: Shared-room microphone behavior

- Requests browser **voice isolation** when the browser/device exposes that capability.
- Keeps echo cancellation and noise suppression enabled.
- Disables automatic microphone gain in Focus Lock capture so distant speech is less likely to be boosted to the same level as nearby speech.
- Uses measured RMS/noise-floor only as a weak near-field hint; it never treats loudness alone as speaker identity.

### New: Meeting identity bound into Adam's reasoning

Adam's professional response engine now receives the current:

- meeting title,
- project/reference,
- declared participants/companies,
- meeting focus/agenda.

This helps Adam remain anchored to the correct meeting when answering and following discussions.

### New: Selective Listening Monitor

The meeting page shows:

- accepted utterance count,
- filtered side-room/background count,
- latest focus decision score and reason.

Filtered background text is not shown or retained by the focus monitor.

### Important safety behavior preserved

Focus filtering does **not** suppress material meeting statements merely because they are not phrased as questions. The focus engine explicitly protects:

- variation / approval / cost / commitment statements,
- action items and deadlines,
- active MEP/HVAC coordination topics,
- short contextual follow-ups such as “Why?” and “Did you check it?”,
- direct speech addressed to Adam.

Owner approval boundaries for costs, variations, contractual positions, purchases, payments, committed dates, and external actions remain unchanged.

### Meeting report enhancement

The professional meeting report now includes **MEETING FOCUS / FILTERING** with counts of accepted meeting utterances and filtered side-room/background candidates. Rejected conversation text is not included.

## Honest technical boundary

v8.3.3.0 does **not** claim biometric voice identification or perfect physical source separation. On a normal laptop/browser microphone, audio must still be captured and may be transiently sent to the configured speech-to-text provider before semantic meeting-focus filtering can decide whether the utterance belongs to the active meeting. This release prevents rejected speech from entering Adam's formal meeting memory/response/report pipeline, but true per-speaker voiceprint isolation would require an additional diarization/speaker-enrollment layer and suitable audio hardware/model support.

## Focused acceptance tests added for this release

1. Adam-addressed meeting question is accepted.
2. Immediate “Why?” follow-up remains in the active meeting thread.
3. Explicit other-project side conversation is rejected.
4. Unrelated room question is rejected.
5. Active MEP topic is accepted.
6. Open-room mode can intentionally accept all detected speech.
7. Rejected text is not retained by focus history.
8. No biometric speaker-recognition claim is made.
9. Material owner/variation commitment language is not accidentally filtered.
10. Meeting action/deadline language is not accidentally filtered.
11. Other-project MEP side talk is still rejected.
12. Focus gate occurs before formal transcript/memory insertion.
13. Browser voice-isolation request is present when supported.
14. Automatic gain is disabled for Focus Lock capture.

Previous approved meeting behaviors are carried forward; they were not re-opened as new acceptance items.

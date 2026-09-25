# Adam Acquisition v8.3.2.1

## Direct-Question Coverage Assurance + Smart Retry

- Adds a retained Question Coverage Monitor for every direct participant question/request routed to Adam.
- Each direct question is explicitly classified as Answered, Clarification requested, or Unanswered; direct questions are never silently discarded as background audio.
- Adds one bounded automatic retry for temporary AI/provider or empty-response failures. The same question ID is reused so the retry does not create duplicate meeting records.
- Failed direct questions remain visible as unresolved instead of being lost, and a participant can repeat them immediately without the previous 15-second duplicate suppression blocking the retry.
- The server-side routing prompt explicitly forbids IGNORE for direct participant questions. If the provider nevertheless returns IGNORE, Adam converts the turn into a concise clarification request.

## Meeting Report Coverage

- Generate Meeting Report now includes a QUESTION COVERAGE / UNANSWERED ITEMS section.
- The report states answered/direct-question totals and lists clarification-required or unanswered questions without inventing an answer.
- Coverage memory survives Clear Screen and is reset only by End Meeting / New Session.

## Preserved behavior

- Natural professional dialogue, multilingual/code-switched speech, topic-thread follow-ups, full-duplex listening, barge-in, live register, autopilot participation styles, native DOCX report export, and owner approval boundaries are preserved.
- No autonomous meeting-platform joining is claimed.

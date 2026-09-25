# Adam Acquisition v8.4.0.3 — Reliable Meeting Voice Auto-Reply

## Why this patch exists
Physical testing of v8.4.0.2 confirmed that Adam could receive meeting input by microphone and typed meeting query, generate the correct text response, and retain the meeting discussion — but the reply was not reliably audible through the browser.

## New / affected behavior
- Adds an explicit **Speak Adam's meeting answers automatically** control, enabled by default.
- The setting applies equally to microphone questions and typed meeting queries in Active Participant / Owner Representative meeting conversation.
- **Start Listening**, **Send Typed Query**, and **Ask Adam & Speak** prime/unlock browser audio from a user gesture before asynchronous AI/TTS work begins.
- Adds **Test / Enable Meeting Voice** so the physical speaker path can be verified independently from speech recognition and AI reasoning.
- Server `/api/tts` remains the preferred Adam voice path.
- If server voice playback fails, Adam automatically falls back to browser speech synthesis using the requested reply locale and a matching installed browser voice when available.
- Meeting voice playback has a bounded watchdog so a failed media event cannot leave the conversation permanently stuck in “speaking”.
- The UI exposes a separate **Meeting voice** status so text-generation success is not confused with audio-playback success.
- Continuous microphone capture, barge-in handling, echo filtering, question coverage, Meeting Focus/project isolation, meeting memory, report generation, and owner-approval boundaries are preserved.

## Physical acceptance test
1. Open Real Meeting Attendance and choose **Owner Representative — Rehearsal**.
2. Check the main Owner Approval and leave **Speak Adam's meeting answers automatically** checked.
3. Click **Test / Enable Meeting Voice**. You should hear “Adam meeting voice is ready.” (or the Arabic equivalent when Arabic is selected).
4. Click **Start Listening** and ask a normal meeting question aloud. Adam should answer in text **and voice**.
5. Enter the same type of question in **Typed meeting query / comment / order** and press Enter. Adam should again answer in text **and voice**.
6. If server TTS playback is unavailable, the Meeting voice status should show browser fallback rather than silently dropping audio.

## Safety
This patch changes meeting reply audio delivery only. It does not authorize variations, costs, payments, purchases, contractual commitments, or committed date changes. Consequential actions remain separately owner-approval gated.

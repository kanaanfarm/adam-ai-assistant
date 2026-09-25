# Adam Acquisition v8.4.0.4 — Meeting Long-Answer Voice Streaming Fix

## Physical issue addressed
The short **Test / Enable Meeting Voice** sample could be heard, but a real meeting answer was shown in text without audible playback.

## Targeted changes
- Real meeting answers now use short TTS chunks instead of waiting for one long audio file.
- Each server-TTS chunk has a bounded wait; if it is slow/unavailable, Adam falls back to the browser voice for that chunk.
- Markdown symbols are removed from speech while visible technical text remains unchanged.
- Typed meeting queries now await the full Meeting Representative response/voice path.
- Completed microphone turns use the same awaitable representative dispatch path.
- Voice job IDs stop the remaining chunks after a real participant barge-in.
- The Meeting Representative panel is moved before Universal Assistant so meeting replies are clearly separated from old Universal Assistant history.
- Project isolation, correction isolation, question coverage, and owner-approval boundaries are unchanged.

## Physical acceptance test
Click **Test / Enable Meeting Voice**, then Start Listening and ask: “Adam, the contractor wants to increase the chilled-water pipe from 100 mm to 125 mm. What do you think?” Adam should show the Meeting Representative answer and start speaking it automatically in short chunks.

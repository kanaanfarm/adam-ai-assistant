# Adam Acquisition v8.3.1.3 — Meeting End-of-Turn / No-Interruption Fix

Physical issue corrected: Adam could answer after a fixed recorder chunk while the participant was still speaking.

## Changes
- Removed the fixed 8-second speech cut for active participant turns.
- Voice capture now continues until approximately 4 seconds of sustained silence after speech.
- Silent microphone windows remain bounded and discarded; a spoken turn is bounded to 60 seconds.
- Adam's automatic response waits for a stable end-of-turn signal instead of responding to a partial chunk.
- If the participant resumes speaking while a reply is pending, Adam keeps waiting.
- Adjacent final transcript parts are combined before the automatic representative response.
- Server transcript plausibility limits now scale with the bounded capture duration so longer legitimate meeting questions are not rejected.
- Existing multilingual, technical-term, owner-authority, and consequential-action protections remain unchanged.

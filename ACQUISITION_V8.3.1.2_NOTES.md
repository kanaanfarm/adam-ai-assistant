# Adam Acquisition v8.3.1.2 — Professional Representative Auto-Answer Reliability Fix

Physical v8.3.1.1 testing showed a participant question was transcribed, but Adam did not answer. Two practical causes were visible in the UI path: the main listen/capture approval and the separate representative approval could become unsynchronized, and multilingual STT can occasionally misrecognize the spoken wake name “Adam / آدم”. A strict exact wake-word gate therefore could miss a real direct question.

## Fix
- In **Owner Representative** mode, the main meeting approval is now the single session-level approval for normal listening/capture + disclosed representative conversation.
- The old representative approval control remains only as a hidden synchronized compatibility field; the user no longer has to find and tick a second approval.
- Owner Representative mode uses a new recommended trigger: **Professional representative — Adam / direct questions**.
- Adam answers when the wake name is recognized OR when the approved representative receives a clear direct question (question punctuation/common question forms), so a wake-name STT miss does not leave Adam silent.
- STT remains **prompt-free**. Wake-name misses are handled by the direct-question trigger instead of injecting prompt text, preserving the hallucination/prompt-leak guard.
- Added duplicate/busy suppression so repeated microphone chunks do not make Adam answer the same question twice.
- Manual per-response speaking approval is hidden in Owner Representative mode; it remains for Active Participant mode.
- Consequential commitments (costs, variations, contracts, payments, purchases, committed dates, external actions) still require their own separate owner approval.

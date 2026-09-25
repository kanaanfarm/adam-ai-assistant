# Adam Acquisition v8.4.1.2 — Meeting Accepted-Turn Persistence & Single-Pairing Fix

## Purpose
Fix the meeting failure where the live trace showed **speech accepted → representative dispatch started → waiting for AI provider**, but the final report later showed **0 accepted utterances**, duplicated the same direct question, and contained no paired Adam answer.

## Root cause corrected
The accepted speech, coverage row, AI dispatch, and paired discussion record could be created by separate asynchronous callbacks. A duplicate completed STT callback could enter the pipeline before the first callback finished, and the report did not classify `Processing` as an explicit coverage state. This could produce duplicate direct questions and contradictory meeting-focus totals.

## Changes in v8.4.1.2
- **Immediate accepted-turn persistence:** once Meeting Focus accepts a turn, it is stored in ephemeral formal meeting memory before the AI provider call begins.
- **Stable turn ID end-to-end:** the same `question_id` is carried through focus check, transcript note, representative dispatch, question coverage, Adam response, and paired discussion record.
- **Duplicate STT suppression:** the browser rejects the same completed transcript before the asynchronous focus request; the server also collapses the same normalized accepted turn within a short 12-second window.
- **Single-flight AI dispatch:** the same session/question pair cannot launch a second AI-provider call while the first is in flight.
- **Bounded meeting AI wait:** the meeting AI call now has a 25-second timeout. On timeout the accepted question is retained as `Unanswered — AI provider timeout` instead of remaining indefinitely in a silent waiting state.
- **Monotonic turn state:** a delayed transcript-note callback cannot regress `Processing` or a completed answer back to `Accepted`.
- **Completed-turn idempotency:** a late duplicate callback cannot call the AI provider again after that same stable turn is already Answered, Clarification requested, or Ignored.
- **Single paired discussion record:** a repeated result with the same question ID updates the existing pair rather than appending a duplicate.
- **Processing is now a real report state:** meeting reports explicitly count `Answered`, `Clarification requested`, `Processing`, and `Unanswered`.
- **Report cannot say 0 accepted while an accepted answer is in flight:** focus accepted count is reconciled with the accepted-turn ledger. While an answer is Processing, a deterministic report is returned instead of asking the report AI to infer state.
- **Visible reply trace retained/enhanced:** `speech accepted → representative dispatch started → waiting for AI provider → AI response received → spoken reply completed`.
- **Ephemeral reset preserved:** End Meeting / New Session clears the new accepted-turn and in-flight state.
- **Governance unchanged:** no variation approval, cost acceptance, contractual commitment, external action, or owner impersonation was added.

## Locked baseline
Built from the latest archived **v8.4.1.1 Meeting Autoplay Unlock Fix** baseline. Previously approved tests remain locked PASS and should not be repeated.

## Only affected physical acceptance test
1. Open Meeting Representative mode with the same owner approval used in the previous test.
2. Ask **once**: `Adam, what is the function of a chilled water pump?`
3. Wait for Adam's spoken answer.
4. Generate the meeting report.

### PASS
- Exactly **1** accepted participant turn.
- Exactly **1** direct-question coverage row.
- Exactly **1** Adam answer.
- Exactly **1** paired discussion record.
- No duplicate Processing question.
- The accepted question is **not** counted as side-room/background speech.
- Final coverage after the answer: **1 answered / 1 direct question; 0 processing; 0 unanswered**.
- Adam's reply is visible and spoken.

### Optional in-flight check
If the report is generated while Adam is still waiting for the provider, it must show the question as **1 Processing** and show at least **1 accepted** utterance; it must never report `0 accepted / 0 unanswered` while the question is still in flight.

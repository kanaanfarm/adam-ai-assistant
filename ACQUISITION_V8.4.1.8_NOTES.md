# Adam Acquisition v8.4.1.8 — Clarification Classification + New Meeting Context Isolation Fix

## Purpose
This focused upgrade fixes the two issues exposed by the clarification test after v8.4.1.7:

1. A direct request to approve/proceed with an under-specified chilled-water pump change was counted as **Answered** instead of **Clarification required**.
2. A supposedly new meeting report carried forward the previous 100 mm chilled-water pipe topic, indicating that late transcription/AI callbacks could cross the End Meeting / New Session boundary.

## Changes
- Added a deterministic **decision-critical material-change clarification gate** before the AI-provider call.
- When a direct question asks whether a chilled-water pump change may proceed and the proposal does not contain the decision-critical duty/reference information, Adam now returns a concise **CLARIFY** response instead of a conditional answer classified as completed.
- The clarification asks for the proposed pump duty point (flow and head), approved pump reference/proposed submittal, and reason for the change.
- Updated the meeting prompt with a **MATERIAL-CHANGE EXCEPTION**: missing routine project data is normally handled as an answer-with-required-documents, but missing characteristics of the proposed material change itself require clarification before a proceed/approval recommendation.
- A participant reply to Adam's clarification is now treated as a **clarification follow-up**, not automatically as a new direct question. It still receives a response, but question-coverage totals are not inflated merely because Adam was waiting for clarification.
- Added clarification-parent tracking so follow-up dialogue stays tied to the same unresolved issue.
- Added a browser **meeting session epoch**. Each microphone chunk, browser-recognition result, and AI request is bound to the session/epoch active when it started.
- End Meeting increments the epoch before stopping capture, waits for queued transcription/memory work, clears client meeting state, rotates to a new session id, and prevents late old-session callbacks from mutating the new meeting.
- Added server-side **closed-session tombstones**. Late focus, note, or ask requests for a session that has already ended are rejected with `meeting_session_closed` rather than recreating that session state.
- Client conversation-history recovery is accepted by the server only when `client_history_session_id` matches the current meeting session.
- Previous v8.4.1.5 AI response, v8.4.1.6 end-of-turn/technical transcription, and v8.4.1.7 approval-status fixes remain unchanged.

## Targeted owner acceptance test
Do not repeat the already-approved provider, end-of-turn, transcription, or approval-status tests.

### Part A — clarification classification
Start a clean new meeting and say:

> Adam, the contractor wants to change the chilled-water pump. Can they proceed?

PASS requires:
- Adam must **not approve** the change.
- Adam must ask for the missing decision-critical pump information.
- Question coverage must show the direct question as **Clarification required / Clarification requested**, not Answered.

Then say:

> They only said the new pump is bigger.

PASS requires:
- Adam must say that “bigger” is not sufficient technical justification and continue requesting the actual duty/submittal information.
- This clarification reply must not be counted as a second direct question solely because Adam was awaiting clarification.

### Part B — new-meeting isolation
Click **End Meeting** and confirm the reset. Start a new meeting and ask only the two pump-change lines above.

PASS requires:
- The new report contains no prior 100 mm / 125 mm chilled-water pipe discussion unless you explicitly mention it again.
- No late prior-session audio or AI response appears in the new meeting.
- The report remains limited to the current meeting session.

Previously approved tests remain locked PASS unless a later change directly affects those paths.

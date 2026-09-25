# Adam Acquisition v8.4.1.12 — Fast AI Dispatch + Lower-Latency Factual Response Path

## Purpose
Reduce the measured AI stage for short, self-contained factual meeting questions while preserving every governed/approval/change/clarification path.

## Changes
- Keeps the existing narrow fast-factual eligibility gate. Approval/proceed/change/revision/cost/variation questions, contextual follow-ups, clarification follow-ups and proactive interventions stay on the full governed meeting path.
- Reduces fast factual response budget from 320 to 160 output tokens.
- Uses `minimal` reasoning effort only for the eligible fast factual path; all existing normal `call_ai` callers remain on the historical `low` reasoning default.
- Removes owner briefing and live meeting history from the fast factual prompt because that path is explicitly limited to self-contained questions. This cuts request size without weakening project/governance behavior.
- Keeps the normal 700-token / low-reasoning meeting path unchanged.
- Keeps v8.4.1.11 immediate factual voice, v8.4.1.11.1 total voice-start timing, and v8.4.1.11.2 end-turn timestamp fixes unchanged.

## Acceptance test
Ask once: `Adam, what is the function of a balancing valve?`

Target: AI stage materially lower than the prior 4.9 s reading, ideally near 2–3 s on the same machine/network, with the same correct concise answer and no regression to owner-approval behavior.

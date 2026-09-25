# Adam Acquisition v1.1 — Agent Orchestration

## Purpose
Turn Adam's existing compound-workflow capability into a buyer-demonstrable orchestration layer with explicit separation between planning, owner approval, execution confirmation, and audit history.

## Added
- Provider-neutral `adam_core/orchestration.py`.
- Approval-gated consequential workflow steps.
- Separate workflow events for `owner_approved` and `step_completed`.
- Buyer-safe workflow status APIs:
  - `GET /api/workflows`
  - `GET /api/workflows/<id>`
- Explicit approval API:
  - `POST /api/workflows/<id>/approve-step`
- Consequential steps cannot be marked complete until approval is recorded and execution success is confirmed.
- Outlook compound-workflow UI now records approval before sending, then records successful execution.
- Regression tests for approval gates and safe workflow summaries.

## Acquisition demo target
Owner asks Adam to review source material, prepare a response, send it through Outlook, and create a follow-up. Adam plans the workflow, prepares the non-consequential work, stops at Owner Review, records explicit approval, executes through the connected service, records confirmed success, then schedules the follow-up.

## Safety invariant
Approval is not execution. Execution is not inferred from a click. Adam records completion only after the connected action reports success.

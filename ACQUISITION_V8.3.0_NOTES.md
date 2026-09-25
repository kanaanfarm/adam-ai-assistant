# Adam Acquisition v8.3.0 — Autonomous Meeting Representative

Adds an owner-controlled **Owner Representative — Rehearsal** mode to Meeting Attendance.

## New behavior
- Adam can listen to meeting audio through the browser microphone, maintain transcript context, answer questions, ask clarifying questions, take notes, and speak responses.
- A pre-meeting **Owner Briefing** defines factual positions Adam may state on the owner's behalf.
- Adam must identify itself as the owner's AI representative and may not impersonate the owner.
- Consequential commitments remain blocked: no variation/cost acceptance, contractual change, purchase/payment authorization, committed-date change, sending, scheduling, or other external action without the existing separate owner approval path.
- Arabic meeting responses default to natural Lebanese Arabic. The Meeting Language selector can force ar-LB recognition and Adam/آدم is recognized as an auto-answer wake name.

## Important boundary
This release provides the meeting intelligence and rehearsal/companion workflow. It does **not** falsely claim autonomous Microsoft Teams/Zoom/Google Meet joining. A real approved platform adapter is still required for Adam to enter those services as its own participant.

## Acceptance test
Use two people/devices: owner configures briefing + approvals; participant asks Adam normal, technical, clarification, and consequential questions. Adam should answer the first three and route consequential commitments back to Mohamad for approval.

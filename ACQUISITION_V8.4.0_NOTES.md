# Adam Acquisition v8.4.0 — Autonomous Meeting Attendance Preparation

## Goal
Prepare Adam to attend a pre-authorized meeting later without Mohamad having to open or operate the Real Meeting Attendance page at meeting time.

## New affected behavior
- **Autonomous Meeting Attendance Control Center** at `/autonomous-meeting-attendance`.
- **Persistent attendance missions** survive Adam restarts and extracted-version upgrades using Adam's per-user runtime storage.
- **Per-meeting owner pre-approval** can authorize Adam in advance to join/listen/speak/take notes/professionally represent Mohamad when the meeting starts.
- **Standing attendance policy** can be enabled once by the owner to allow read-only Outlook calendar discovery and automatic preparation of matching future online meetings.
- **Unattended scheduler** starts with `python app.py` / `START_ADAM_ACQUISITION.bat` and evaluates missions every 30 seconds.
- **Pre-meeting briefing** combines the meeting title, project/reference, participants, owner briefing, participation style and relevant durable owner corrections.
- **Authority isolation** is hard-coded: attendance pre-approval never grants variation, cost/payment, contractual, purchase, committed-date or external-send authority.
- **Outlook calendar read transport** added through Microsoft Graph `/me/calendarView` using the existing Microsoft connection; no credentials are stored by the transport.
- **Calendar project/title keyword filter** supports narrowing standing auto-discovery to meetings such as `Tower`, `MEP`, etc.
- **Main navigation and Acquisition Center** now expose Autonomous Meeting Attendance.
- Windows launcher text updated to v8.4.0 and confirms that the autonomous scheduler starts automatically.

## Live-platform boundary
v8.4.0 does **not** falsely claim a real Teams / Zoom / Google Meet join. The package contains the unattended scheduler, policy, mission persistence, calendar discovery and briefing orchestration, but `live_meeting_platform_adapter_ready` remains false until a real tested platform join adapter is connected.

When a mission reaches its join window without that adapter, its status becomes:

`blocked_platform_adapter — live_meeting_platform_adapter_not_configured`

This is intentional evidence that Adam did not claim to attend a meeting he could not actually join.

## Preserved behavior
- Adam remains a disclosed AI representative; no human impersonation.
- Real Meeting Attendance, Meeting Focus, project isolation, natural corrections/orders, no-silent-turn watchdog, Universal Assistant and durable owner memory remain unchanged.
- Consequential external commitments remain owner-gated.
- Guest Voice privacy boundaries remain unchanged.

## New focused acceptance checks
- owner pre-approval gate;
- attendance mission persistence and scheduling;
- consequential authority cannot be granted by autonomous attendance policy;
- preparation-window calculation;
- hard live-platform block when adapter is absent;
- readiness transition when an injected live adapter is theoretically available;
- standing-policy owner approval gate;
- Outlook calendar auto-discovery matching;
- AI identity disclosure;
- Graph calendar read transport is bounded/read-only in the transport test;
- control-center UI exposes the required unattended-attendance controls.

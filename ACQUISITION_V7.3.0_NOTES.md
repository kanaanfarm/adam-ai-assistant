# Adam Acquisition v7.3.0 — Real Meeting Attendance

## New behavior
- Adds `/meeting-attendance` owner-controlled meeting companion UI.
- Supports Microsoft Teams, Zoom, Google Meet, in-person and other meetings as companion contexts.
- Browser microphone speech-recognition capture when the browser supports it and the owner grants permission.
- Manual transcript fallback.
- Listen Only and Take Notes modes.
- Meeting transcript can be processed into bounded notes and action items.
- Owner Approval is required before microphone/listening capture.
- Adam AI identity is explicit; user impersonation is not allowed.

## Important production boundary
This release does **not** claim autonomous platform joining. The existing Teams/Zoom/Meet platform adapter remains non-live until a real approved platform adapter/credential flow is configured. v7.3.0 therefore delivers real companion attendance and note capture while preserving truthful platform capability reporting.

## Acceptance
- Test 231: internal v7.3.0 meeting-attendance integration/regression.
- Test 232: owner runtime acceptance of meeting companion UI + microphone/manual transcript + notes/action items.

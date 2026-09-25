# Adam Acquisition v6.7.0 — Browser/Computer Operator

## Added
- Screen-aware browser/computer task planning boundary layered on Adam's existing Selenium live-browser control.
- Explicit screen perception, adaptive recovery and audit-evidence contract.
- Owner Approval gate before consequential browser/computer handoff.
- Credential-like task rejection.
- Safe synthetic acceptance mode: no external network or real computer action during Tests 210–211.
- Acquisition Center card and interactive operator page.

## Acceptance
- Test 210: `/api/personal-assistant/browser-computer-operator/self-test`
- Test 211: `/browser-computer-operator` → **Run Safe Acceptance Example** with Owner Approval OFF. Expected `status=owner_approval_required`, `ready_for_browser_boundary=false`, `execution_performed=false`.

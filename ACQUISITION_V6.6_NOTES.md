# Adam Acquisition v6.6.0 — Camera, Vision & Attachment Operator

## Added
- Governed camera/vision/attachment operator boundary.
- Live browser camera preview and capture with **natural unmirrored orientation** (no left/right CSS mirroring).
- Front/rear camera switch control.
- Multi-file attachment picker connected to the existing `/api/main/attachments/analyze` document/vision service.
- Conversion of observed attachment/camera context into a governed workflow handoff.
- Consequential handoff requires Owner Approval and never executes from the v6.6 boundary itself.
- Sensitive credential-like content is rejected by the operator boundary.
- Synthetic no-network acceptance flow for Tests 208–209.

## Acceptance
- Test 208: `/api/personal-assistant/camera-vision-attachment/self-test`
- Test 209: `/camera-vision-attachment-operator` → **Run Safe Acceptance Example** with Owner Approval OFF. Expected `status=owner_approval_required`, `execution_performed=false`.

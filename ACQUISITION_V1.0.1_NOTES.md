# Adam Acquisition v1.0.1 — Core Stabilization

Baseline engine: Personal AI Assistant v0.8.0.1.

## Changes in this acquisition-only copy

- Removed the predictable Flask secret fallback. A cryptographically strong per-user secret is now generated and persisted when no environment secret is configured.
- Added `adam_core/` as the first safe modularization boundary. Existing workflows remain in `app.py` for now to avoid destabilizing working behavior.
- Added `/api/health`, a buyer/demo-safe health endpoint that reports readiness without exposing credentials.
- Added a dedicated Windows launcher with Python/dependency preflight checks and delayed browser opening.
- Added `DIAGNOSTICS.bat` for Python/package/port checks.
- Added smoke tests for import/startup and health endpoint safety.
- Acquisition build now identifies itself separately as Adam Acquisition v1.0.1 while retaining the v0.8.0.1 baseline engine.

## Deliberately unchanged

Email, Outlook, contacts, calendar, WhatsApp, voice, documents, sales, stock/paper-trading, camera, attachments, owner approvals, and existing UI workflows were not redesigned in this stabilization build.

## Next target

v1.1 — Agent Orchestration Layer: one controlled multi-step workflow spanning source retrieval, reasoning/drafting, owner approval, execution, audit trail, and memory update.

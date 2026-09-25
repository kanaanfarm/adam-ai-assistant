# Adam Acquisition v6.4.0 — Persistent Personal Context & Memory

Adds a local, owner-approved personal context store for preferences, contact context, project context and follow-ups.

Safety contract:
- Writing memory requires Owner Approval.
- Credential-like content (passwords, tokens, API keys, secrets, private keys) is rejected.
- Recall is read-only and performs no external action/network access.
- Acceptance self-test uses a temporary synthetic store and does not expose real private memory.

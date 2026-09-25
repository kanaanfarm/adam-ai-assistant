# Adam Acquisition v1.0 — Baseline

Source baseline: Personal_AI_Assistant_v0.8.0.1_SEND_IT_MEMORY_FIX_FULL_PACKAGE.zip
Baseline date: 2026-08-31

## Rule
This acquisition branch is separate from the personal Adam build. The source baseline is preserved and must not be overwritten by acquisition-specific experiments.

## What already exists
- Main conversational assistant and multilingual voice identity
- Outlook email and Microsoft calendar integration
- Contacts and follow-up workflows
- Documents drafting and file analysis
- WhatsApp Business Cloud API workflow with owner approval
- Sales drafting workflow
- Translation
- Vision and attachments
- Alpaca paper-market data / paper-trading module
- Owner Control / approval gates
- Multi-step workflow and context-memory logic
- Desktop/PWA/Android wrapper assets

## First audit findings
1. Python source compiles successfully.
2. Core backend is concentrated in a large single app.py; modularization is a priority for diligence quality.
3. README history is extensive but its top heading is stale compared with runtime version v0.8.0.1.
4. Security hardening is needed before external diligence; Flask has a development fallback secret when FLASK_SECRET_KEY is absent.
5. The acquisition story should focus on secure cross-application execution, persistent context, and human approval rather than generic chat features.

## Acquisition preparation gates
- Gate A: Stable baseline and regression tests
- Gate B: Modular agent/action architecture
- Gate C: Three buyer-grade end-to-end demos
- Gate D: Security, secrets, permissions, and audit hardening
- Gate E: IP/dependency inventory and architecture documentation
- Gate F: Benchmark evidence and differentiation
- Gate G: Demo/pitch/data-room package

## Initial target demos
1. Email + document operator: understand incoming request, locate/analyze supporting material, draft response, request approval, send, remember follow-up.
2. Cross-app meeting operator: resolve contact, check calendar, draft communication, request approval, send, create meeting, track follow-up.
3. Controlled business operator: use approved company facts to prepare a customer response/action while enforcing owner policies and logging every step.

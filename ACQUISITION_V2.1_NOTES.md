# Adam Acquisition v2.1.0 — Document Processing Boundary

Extracts attachment classification, bounded local extraction, PDF/DOCX/XLSX/XLSM/text processing, analysis-prompt construction and DOCX rendering into tested `adam_core` services while preserving existing Documents, attachment and camera workflows.

Buyer evidence endpoints:
- `/api/acquisition/document-boundary`
- `/api/acquisition/document-boundary/self-test`
- `/api/acquisition/document-boundary/download`

The buyer evidence contains no attachment content, extracted document text, filenames, AI prompt content, credentials, contact values or private-memory values. Extraction self-tests require no AI provider and no external network operation.

Next extraction targets: Microsoft Graph transport, WhatsApp Cloud transport, then vision AI transport.

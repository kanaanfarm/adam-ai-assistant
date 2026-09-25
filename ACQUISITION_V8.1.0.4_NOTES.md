# Adam Acquisition v8.1.0.4 — Reliable Voice + Factual Grounding

- One voice-delivery controller now handles every guest reply.
- Long speech is word-safe chunked, each chunk waits for completion, server TTS retries once, then browser TTS fallback is used.
- Voice jobs have IDs so stale recognition/audio events cannot cancel the active reply.
- Visible speaking/finished/failed status and in-session voice audit fields track reply_id, chunks_total, chunks_spoken and completion.
- Guest factual-grounding rule forbids invented local/niche facts and requires uncertainty/verification language when evidence is insufficient.
- Guest corrections can guide the current conversation but are not described as permanent retraining.
- Existing privacy, owner approval, single-introduction, Lebanese Arabic and external-action boundaries remain unchanged.

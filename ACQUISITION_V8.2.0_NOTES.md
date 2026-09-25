# Adam Acquisition v8.2.0 — Advanced Intelligence & Research Routing

## Goal
Make Adam substantially more capable for normal knowledge and research questions without weakening the owner/guest security boundary.

## New behavior
- Adds an Advanced Intelligence Router for normal reasoning vs. public research.
- Explicit search requests, local/niche facts, and time-sensitive questions can use OpenAI Responses API web search.
- Uses a stronger advanced model path (`ADAM_ADVANCED_MODEL` when set; otherwise a flagship-model attempt with compatibility fallback).
- Prevents "guest mode" from unnecessarily reducing normal knowledge/reasoning capability.
- Keeps private owner data unavailable to guests and keeps consequential actions approval-gated.
- Research failures gracefully fall back to model reasoning instead of breaking the conversation.
- Guest API exposes non-sensitive diagnostics: intelligence mode, research reason, web-search attempted/used, and model path.

## Important
Live web research requires an OpenAI account/model with Responses API web-search access. If unavailable, Adam falls back to the configured text model and clearly avoids pretending that a search occurred.

"""Text AI provider transport boundary for Adam Acquisition.

Constructs OpenAI-compatible text requests and executes them through an injected
HTTP provider. GPT-5 family models on the official OpenAI API use the Responses
API; legacy/custom OpenAI-compatible providers continue to use Chat Completions.
This module does not persist credentials, prompts, or model responses.
"""

class AIProviderTransportError(RuntimeError):
    pass


def _normalized_limit(max_tokens=1200):
    return max(1, min(int(max_tokens or 1200), 8192))


def _system_text(language, master_prompt):
    return (
        str(master_prompt or "").strip() + "\n\n"
        "For this request, respond in " + str(language or "English") + ". "
        "When the user asks for translation, return an accurate natural translation without changing the meaning."
    ).strip()


def build_chat_payload(prompt, language, model, master_prompt, max_tokens=1200):
    text = "" if prompt is None else str(prompt).strip()
    if not text:
        raise AIProviderTransportError("AI instruction is empty.")
    model = str(model or "gpt-4o-mini").strip() or "gpt-4o-mini"
    payload = {"model": model, "messages": [
        {"role": "system", "content": _system_text(language, master_prompt)},
        {"role": "user", "content": text},
    ]}
    limit = _normalized_limit(max_tokens)
    if model.lower().startswith("gpt-5"):
        payload["max_completion_tokens"] = limit
    else:
        payload["max_tokens"] = limit
    return payload


def build_responses_payload(prompt, language, model, master_prompt, max_tokens=1200, reasoning_effort="low"):
    text = "" if prompt is None else str(prompt).strip()
    if not text:
        raise AIProviderTransportError("AI instruction is empty.")
    selected_model = str(model or "gpt-5.6").strip() or "gpt-5.6"
    payload = {
        "model": selected_model,
        "instructions": _system_text(language, master_prompt),
        "input": text,
        "max_output_tokens": _normalized_limit(max_tokens),
        "store": False,
    }
    if selected_model.lower().startswith("gpt-5") and reasoning_effort:
        payload["reasoning"] = {"effort": str(reasoning_effort)}
    return payload


def _extract_responses_text(data):
    """Extract assistant text from an OpenAI Responses API payload."""
    if not isinstance(data, dict):
        return ""
    direct = str(data.get("output_text") or "").strip()
    if direct:
        return direct
    parts = []
    for item in data.get("output") or []:
        if not isinstance(item, dict) or item.get("type") != "message":
            continue
        for content in item.get("content") or []:
            if not isinstance(content, dict):
                continue
            if content.get("type") in {"output_text", "text"}:
                text = content.get("text")
                if isinstance(text, dict):
                    text = text.get("value") or text.get("text") or ""
                text = str(text or "").strip()
                if text:
                    parts.append(text)
    return "\n".join(parts).strip()


def _is_official_openai(api_base):
    return "api.openai.com" in str(api_base or "").lower()

def _normalize_api_root(api_base):
    base = str(api_base or "https://api.openai.com/v1").strip().rstrip("/")
    low = base.lower()
    for suffix in ("/chat/completions", "/responses", "/completions"):
        if low.endswith(suffix):
            base = base[:-len(suffix)].rstrip("/")
            low = base.lower()
            break
    if low in {"https://api.openai.com", "http://api.openai.com"}:
        base += "/v1"
    return base


def _post_chat(api_base, api_key, model, prompt, language, master_prompt, *, http, max_tokens, timeout):
    payload = build_chat_payload(prompt, language, model, master_prompt, max_tokens=max_tokens)
    url = _normalize_api_root(api_base) + "/chat/completions"
    r = http.post(url, headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, json=payload, timeout=timeout)
    if not getattr(r, "ok", False):
        raise AIProviderTransportError(f"AI provider chat error {getattr(r, 'status_code', 'unknown')}: {str(getattr(r, 'text', ''))[:300]}")
    try:
        data = r.json()
        answer = str((((data.get("choices") or [{}])[0].get("message") or {}).get("content") or "")).strip()
    except Exception as exc:
        raise AIProviderTransportError("AI provider returned invalid Chat Completions JSON.") from exc
    if not answer:
        raise AIProviderTransportError("AI provider returned an empty Chat Completions result.")
    return answer


def _post_responses(api_base, api_key, model, prompt, language, master_prompt, *, http, max_tokens, timeout, reasoning_effort="low"):
    payload = build_responses_payload(prompt, language, model, master_prompt, max_tokens=max_tokens, reasoning_effort=reasoning_effort)
    url = _normalize_api_root(api_base) + "/responses"
    r = http.post(url, headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, json=payload, timeout=timeout)
    if not getattr(r, "ok", False):
        err = AIProviderTransportError(f"AI provider Responses error {getattr(r, 'status_code', 'unknown')}: {str(getattr(r, 'text', ''))[:300]}")
        err.status_code = getattr(r, "status_code", None)
        raise err
    try:
        data = r.json()
    except Exception as exc:
        raise AIProviderTransportError("AI provider returned invalid Responses API JSON.") from exc
    answer = _extract_responses_text(data)
    if not answer:
        raise AIProviderTransportError("AI provider returned an empty Responses API result.")
    return answer


def complete_text(api_base, api_key, model, prompt, language, master_prompt, *, http, max_tokens=1200, timeout=60, reasoning_effort="low"):
    """Complete a text request using the provider path appropriate to the model.

    Official OpenAI GPT-5.x models use /responses. This avoids the old meeting
    failure where Adam sent GPT-5.6 through /chat/completions and could remain
    waiting without a usable meeting reply. Custom OpenAI-compatible providers
    retain the legacy chat path for compatibility.
    """
    key = str(api_key or "").strip()
    if not key:
        raise AIProviderTransportError("AI API key is missing. Open AI Settings and save the provider URL, API key and model.")
    selected_model = str(model or "gpt-4o-mini").strip() or "gpt-4o-mini"
    base = _normalize_api_root(api_base)
    if selected_model.lower().startswith("gpt-5") and _is_official_openai(base):
        try:
            return _post_responses(base, key, selected_model, prompt, language, master_prompt, http=http, max_tokens=max_tokens, timeout=timeout, reasoning_effort=reasoning_effort)
        except AIProviderTransportError as exc:
            # Compatibility escape hatch only when the provider explicitly says the
            # endpoint is not present/method not allowed. Do not hide auth, quota,
            # model-access, validation, or server errors behind a second request.
            if getattr(exc, "status_code", None) not in {404, 405, 501}:
                raise
    return _post_chat(base, key, selected_model, prompt, language, master_prompt, http=http, max_tokens=max_tokens, timeout=timeout)


def complete_text_with_web_search(api_base, api_key, model, prompt, language, master_prompt, *, http, max_tokens=1600, timeout=90):
    """Use the OpenAI Responses API with web_search, without persisting provider data.

    Returns (answer, metadata). The caller can fall back to normal text completion
    when the configured provider/model does not support Responses web search.
    """
    key = str(api_key or "").strip()
    if not key:
        raise AIProviderTransportError("AI API key is missing. Open AI Settings and save the provider URL, API key and model.")
    text = "" if prompt is None else str(prompt).strip()
    if not text:
        raise AIProviderTransportError("AI instruction is empty.")
    selected_model = str(model or "gpt-5.6").strip() or "gpt-5.6"
    system = (
        str(master_prompt or "").strip() + "\n\n"
        + "For this request, respond in " + str(language or "English") + ". "
        + "Use web search when it materially improves accuracy. Distinguish verified facts from uncertainty. "
        + "Never invent a source, citation, person, family, business, address, date, statistic, or local fact."
    ).strip()
    payload = {
        "model": selected_model,
        "instructions": system,
        "input": text,
        "tools": [{"type": "web_search"}],
        "max_output_tokens": _normalized_limit(max_tokens),
    }
    if selected_model.lower().startswith("gpt-5"):
        payload["reasoning"] = {"effort": "low"}
    url = _normalize_api_root(api_base) + "/responses"
    r = http.post(url, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}, json=payload, timeout=timeout)
    if not getattr(r, "ok", False):
        raise AIProviderTransportError(f"AI web-search provider error {getattr(r, 'status_code', 'unknown')}: {str(getattr(r, 'text', ''))[:300]}")
    try:
        data = r.json()
    except Exception as exc:
        raise AIProviderTransportError("AI web-search provider returned invalid JSON.") from exc
    answer = _extract_responses_text(data)
    if not answer:
        raise AIProviderTransportError("AI web-search provider returned an empty result.")
    output = data.get("output") or []
    web_used = any(isinstance(x, dict) and x.get("type") == "web_search_call" for x in output)
    return answer, {"web_search_used": bool(web_used), "provider_path": "responses_web_search", "model": selected_model}

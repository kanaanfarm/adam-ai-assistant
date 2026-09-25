"""Vision AI transport boundary for Adam Acquisition.

Builds OpenAI-compatible multimodal requests and executes them through an injected
HTTP provider. It does not persist API keys, images, prompts, or model responses.
"""
import base64

class VisionTransportError(RuntimeError):
    pass

VISION_MARKERS = ("gpt-4o", "gpt-4.1", "gpt-5", "vision", "gemini", "claude-3", "claude-4")

def select_vision_model(configured_model, explicit_model=""):
    explicit = str(explicit_model or "").strip()
    if explicit:
        return explicit
    configured = str(configured_model or "").strip()
    low = configured.lower()
    return configured if configured and any(x in low for x in VISION_MARKERS) else "gpt-4o-mini"

def build_vision_payload(image_items, instruction, model):
    content=[{"type":"text","text":(
        "You are Adam. You CAN see the attached image(s). Analyze the actual visual content carefully. "
        "State only what is visible; do not invent hidden details. Read visible text when useful. "
        "If the user asks what is in the photo, directly describe it. User instruction: "
        + (instruction or "Describe and analyze the attached image.")
    )}]
    for item in list(image_items or [])[:6]:
        raw=item.get("bytes") or b""
        if not isinstance(raw,(bytes,bytearray)):
            raise VisionTransportError("Image payload must contain bytes.")
        encoded=base64.b64encode(bytes(raw)).decode("ascii")
        mime=str(item.get("mime") or "image/jpeg")
        content.append({"type":"image_url","image_url":{"url":f"data:{mime};base64,{encoded}","detail":"auto"}})
    if len(content)==1:
        raise VisionTransportError("At least one image is required.")
    payload={"model":str(model or "gpt-4o-mini"),"messages":[{"role":"user","content":content}]}
    if str(model or "").lower().startswith("gpt-5"):
        payload["max_completion_tokens"]=1200
    else:
        payload["temperature"]=0.2
        payload["max_tokens"]=1200
    return payload

def analyze_images(api_base, api_key, model, image_items, instruction, *, http):
    key=str(api_key or "").strip()
    if not key:
        raise VisionTransportError("AI provider is not configured.")
    payload=build_vision_payload(image_items,instruction,model)
    r=http.post(str(api_base or "https://api.openai.com/v1").rstrip("/")+"/chat/completions",
        headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"},json=payload,timeout=120)
    if not getattr(r,"ok",False):
        try: detail=(r.json().get("error") or {}).get("message") or getattr(r,"text","")
        except Exception: detail=getattr(r,"text","")
        raise VisionTransportError(f"Camera/image recognition failed using model {model}: {detail}. Set AI_VISION_MODEL to a vision-capable model available on your AI provider.")
    try: data=r.json()
    except Exception as exc: raise VisionTransportError("Vision provider returned invalid JSON.") from exc
    answer=str((((data.get("choices") or [{}])[0].get("message") or {}).get("content") or "")).strip()
    if not answer:
        raise VisionTransportError("Camera/image recognition returned an empty result.")
    return answer

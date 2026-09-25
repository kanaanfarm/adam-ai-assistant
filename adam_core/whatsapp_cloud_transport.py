"""WhatsApp Cloud API transport boundary for Adam Acquisition.

Pure HTTP transport with injected configuration and HTTP client. This module does
not persist credentials, owner contacts, or message content.
"""
GRAPH_HOST = "https://graph.facebook.com"

class WhatsAppTransportError(RuntimeError):
    pass

def _config(cfg):
    cfg = cfg or {}
    token = str(cfg.get("access_token") or "").strip()
    phone_id = str(cfg.get("phone_number_id") or "").strip()
    api_version = str(cfg.get("api_version") or "v21.0").strip()
    if not token or not phone_id:
        raise WhatsAppTransportError("WhatsApp Business is not configured.")
    return token, phone_id, api_version

def _detail(response):
    try:
        data=response.json()
        return ((data.get("error") or {}).get("message") or str(data))
    except Exception:
        return getattr(response,"text","")

def send_text(cfg, http, phone_number, message_text, *, normalize_func):
    token, phone_id, api_version = _config(cfg)
    to_number = normalize_func(phone_number)
    if not to_number:
        raise WhatsAppTransportError("Recipient WhatsApp number is empty.")
    payload={"messaging_product":"whatsapp","recipient_type":"individual","to":to_number,"type":"text","text":{"preview_url":False,"body":str(message_text or "")}}
    r=http.post(f"{GRAPH_HOST}/{api_version}/{phone_id}/messages",headers={"Authorization":f"Bearer {token}","Content-Type":"application/json"},json=payload,timeout=60)
    if not getattr(r,"ok",False):
        raise WhatsAppTransportError(f"WhatsApp Cloud API error {r.status_code}: {_detail(r)}")
    try: return r.json()
    except Exception: return {}

def get_identity(cfg, http):
    token, phone_id, api_version = _config(cfg)
    r=http.get(f"{GRAPH_HOST}/{api_version}/{phone_id}",params={"fields":"display_phone_number,verified_name,quality_rating"},headers={"Authorization":f"Bearer {token}"},timeout=30)
    if not getattr(r,"ok",False):
        raise WhatsAppTransportError(f"WhatsApp Cloud API error {r.status_code}: {_detail(r)}")
    return r.json()

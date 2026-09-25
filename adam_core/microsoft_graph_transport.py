"""Microsoft Graph transport boundary for Adam Acquisition.

Pure request construction/response validation with injected HTTP transport and token getter.
No credentials are stored by this module.
"""
from urllib.parse import quote

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
TIMEZONE = "Arabian Standard Time"

class GraphTransportError(RuntimeError): pass

def _token(token_getter):
    token = str(token_getter() or "").strip()
    if not token: raise GraphTransportError("Microsoft Outlook is not connected.")
    return token

def _detail(response):
    try: return (response.json().get("error") or {}).get("message") or response.text
    except Exception: return getattr(response, "text", "")

def sender_label(token_getter, http):
    token=_token(token_getter)
    r=http.get(GRAPH_BASE+"/me",headers={"Authorization":f"Bearer {token}"},timeout=30)
    if not getattr(r,"ok",False): raise GraphTransportError(f"Microsoft Graph error {r.status_code}: {_detail(r)}")
    d=r.json(); return d.get("mail") or d.get("userPrincipalName") or d.get("displayName") or ""

def send_mail(token_getter,http,to_email,subject,body,cc=None,bcc=None):
    token=_token(token_getter)
    msg={"subject":subject,"body":{"contentType":"Text","content":body},"toRecipients":[{"emailAddress":{"address":to_email}}]}
    if cc: msg["ccRecipients"]=[{"emailAddress":{"address":str(x).strip()}} for x in cc if str(x).strip()]
    if bcc: msg["bccRecipients"]=[{"emailAddress":{"address":str(x).strip()}} for x in bcc if str(x).strip()]
    r=http.post(GRAPH_BASE+"/me/sendMail",headers={"Authorization":f"Bearer {token}","Content-Type":"application/json"},json={"message":msg,"saveToSentItems":True},timeout=60)
    if r.status_code not in (200,202): raise GraphTransportError(f"Microsoft Graph error {r.status_code}: {_detail(r)}")
    return True

def create_event(token_getter,http,event):
    token=_token(token_getter)
    r=http.post(GRAPH_BASE+"/me/events",headers={"Authorization":f"Bearer {token}","Content-Type":"application/json"},json=event,timeout=60)
    if r.status_code not in (200,201,202): raise GraphTransportError(f"Microsoft Calendar error {r.status_code}: {_detail(r)}")
    return r.json() if getattr(r,"text","") else {}

def list_inbox(token_getter,http,top=20):
    token=_token(token_getter); top=max(1,min(int(top),50))
    params={"$top":top,"$orderby":"receivedDateTime desc","$select":"id,subject,from,receivedDateTime,isRead,importance,bodyPreview,hasAttachments,webLink"}
    r=http.get(GRAPH_BASE+"/me/mailFolders/inbox/messages",headers={"Authorization":f"Bearer {token}"},params=params,timeout=60)
    if not getattr(r,"ok",False): raise GraphTransportError(f"Microsoft Inbox error {r.status_code}: {_detail(r)}")
    return r.json().get("value",[])

def get_message(token_getter,http,message_id):
    token=_token(token_getter)
    r=http.get(GRAPH_BASE+"/me/messages/"+quote(str(message_id),safe=""),headers={"Authorization":f"Bearer {token}","Prefer":'outlook.body-content-type="text"'},params={"$select":"id,subject,from,toRecipients,ccRecipients,receivedDateTime,isRead,importance,body,bodyPreview,webLink"},timeout=60)
    if not getattr(r,"ok",False): raise GraphTransportError(f"Microsoft message error {r.status_code}: {_detail(r)}")
    return r.json()

def send_reply(token_getter,http,message_id,reply_text):
    token=_token(token_getter)
    r=http.post(GRAPH_BASE+"/me/messages/"+quote(str(message_id),safe="")+"/reply",headers={"Authorization":f"Bearer {token}","Content-Type":"application/json"},json={"comment":reply_text},timeout=60)
    if r.status_code not in (200,202,204): raise GraphTransportError(f"Microsoft reply error {r.status_code}: {_detail(r)}")
    return True

def list_calendar_view(token_getter, http, start_iso, end_iso, top=50):
    """Read upcoming Outlook/Teams calendar events for an owner-approved local workflow.

    Read-only Graph call. The caller decides whether private event details may be shown
    in the owner UI. No credentials are stored here.
    """
    token = _token(token_getter)
    top = max(1, min(int(top), 100))
    params = {
        "startDateTime": str(start_iso),
        "endDateTime": str(end_iso),
        "$top": top,
        "$orderby": "start/dateTime",
        "$select": "id,subject,start,end,location,attendees,isOnlineMeeting,onlineMeeting,webLink,bodyPreview",
    }
    r = http.get(
        GRAPH_BASE + "/me/calendarView",
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        timeout=60,
    )
    if not getattr(r, "ok", False):
        raise GraphTransportError(f"Microsoft Calendar error {r.status_code}: {_detail(r)}")
    data = r.json() if getattr(r, "text", "") else {}
    return list((data or {}).get("value") or [])[:top]

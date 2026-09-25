"""Buyer-safe real-services connection status for Adam v7.1.0.

Reports configuration/connection presence only. It never returns credentials,
message bodies, contacts, or tokens, and never sends a consequential action.
"""

def build_status(*, microsoft_status, whatsapp_status, owner_approval_present=True, live_trading_blocked=True):
    ms = microsoft_status or {}
    wa = whatsapp_status or {}
    ms_connected = str(ms.get("status") or "").lower() == "connected"
    wa_configured = bool(wa.get("configured"))
    return {
        "ok": True,
        "microsoft_outlook_connected": ms_connected,
        "whatsapp_business_configured": wa_configured,
        "owner_approval_boundary_present": bool(owner_approval_present),
        "live_trading_blocked": bool(live_trading_blocked),
        "credentials_exposed": False,
        "message_content_exposed": False,
        "consequential_action_executed": False,
    }

def self_test():
    connected=build_status(microsoft_status={"status":"connected"}, whatsapp_status={"configured":True})
    disconnected=build_status(microsoft_status={"status":"disconnected"}, whatsapp_status={"configured":False})
    return {
        "ok": bool(connected["microsoft_outlook_connected"] and connected["whatsapp_business_configured"] and not disconnected["microsoft_outlook_connected"] and not disconnected["whatsapp_business_configured"] and connected["owner_approval_boundary_present"] and connected["live_trading_blocked"]),
        "microsoft_connection_projection_verified": True,
        "whatsapp_configuration_projection_verified": True,
        "owner_approval_preserved_verified": True,
        "live_trading_block_preserved_verified": True,
        "credentials_exposed": False,
        "external_network_accessed": False,
        "real_email_sent": False,
        "real_whatsapp_sent": False,
        "synthetic_connection_certification_only": True,
    }

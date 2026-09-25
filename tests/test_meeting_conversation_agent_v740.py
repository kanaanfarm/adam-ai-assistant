from adam_core.meeting_conversation_agent import build_conversation_status, prepare_response, authorize_speaking, self_test


def test_233_modes_and_preview_are_governed():
    status=build_conversation_status()
    assert set(status["supported_modes"]) == {"listen_only","take_notes","active_participant"}
    p=prepare_response({"mode":"active_participant","context":"HVAC drawing discussed","response":"The HVAC drawing is noted."})
    assert p["ok"] and p["response_ready"] and not p["spoken"]
    assert p["owner_approval_required_to_speak"] is True


def test_234_speaking_requires_approval_and_ai_identity():
    blocked=authorize_speaking({"response":"The HVAC drawing is noted.","owner_approved":False})
    assert blocked["status"] == "approval_required" and blocked["spoken"] is False
    approved=authorize_speaking({"response":"The HVAC drawing is noted.","owner_approved":True})
    assert approved["speak_authorized"] is True
    assert approved["ai_identity_declared"] is True
    assert approved["response"].lower().startswith("i am adam")
    assert approved["user_impersonation_allowed"] is False
    assert self_test()["ok"] is True

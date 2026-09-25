from adam_core.connectors import (
    ConnectorValidationError,
    execute_email,
    execute_calendar,
    execute_whatsapp,
)
from adam_core.connector_boundaries import (
    build_connector_boundary_manifest,
    connector_boundaries_are_privacy_safe,
)


def test_email_blocks_without_approval():
    try:
        execute_email(approved=False, to_email="a@example.com", subject="S", body="B", send_func=lambda **k: None)
        assert False
    except ConnectorValidationError as e:
        assert "approval" in str(e).lower()


def test_email_executes_injected_transport_after_validation():
    calls=[]
    def send_func(**kwargs): calls.append(kwargs); return {"ok": True}
    out=execute_email(approved=True,to_email="a@example.com",subject="Hi",body="Body",cc_raw="c@example.com",send_func=send_func)
    assert out["sent"] is True and calls[0]["cc"] == ["c@example.com"]


def test_calendar_blocks_without_approval():
    try:
        execute_calendar(approved=False,subject="M",start_local="2026-09-01T10:00",duration_minutes=60,attendee_email="a@example.com",attendee_name="A",create_func=lambda *a: {})
        assert False
    except ConnectorValidationError as e:
        assert "approval" in str(e).lower()


def test_calendar_executes_injected_transport():
    out=execute_calendar(approved=True,subject="M",start_local="2026-09-01T10:00",duration_minutes=60,attendee_email="a@example.com",attendee_name="A",create_func=lambda *a: {"id":"evt1","webLink":"https://example.invalid/e"})
    assert out["created"] and out["event_id"] == "evt1"


def test_whatsapp_blocks_without_approval():
    try:
        execute_whatsapp(approved=False,phone="+971 50 123 4567",message="Hi",send_func=lambda p,m: {})
        assert False
    except ConnectorValidationError as e:
        assert "approval" in str(e).lower()


def test_whatsapp_executes_injected_transport():
    out=execute_whatsapp(approved=True,phone="+971 50 123 4567",message="Hi",send_func=lambda p,m: {"messages":[{"id":"wamid.1"}]})
    assert out["sent"] and out["phone_normalized"] == "971501234567" and out["message_id"] == "wamid.1"


def test_connector_manifest_is_buyer_safe():
    m=build_connector_boundary_manifest(version="v1.8.0")
    core=m["connector_boundaries"]
    assert core["adapter_count"] == 3
    assert core["controls"]["approval_policy_testable_without_credentials"] is True
    assert connector_boundaries_are_privacy_safe(m) is True
    assert len(m["connector_boundaries_sha256"]) == 64


def test_connector_self_test_is_credential_free_and_passes():
    from adam_core.connectors import self_test
    result = self_test()
    assert result["ok"] is True
    assert result["external_execution_performed"] is False
    assert all(result["checks"].values())

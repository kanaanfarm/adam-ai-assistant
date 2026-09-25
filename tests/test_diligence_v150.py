from adam_core.diligence import build_diligence_manifest, diligence_is_privacy_safe


def sample():
    acquisition={
        "positioning":"Operator",
        "all_core_checks_pass":True,
        "integration_configuration":{"ai_provider_configured":True,"microsoft_client_configured":False,"whatsapp_configured":False,"alpaca_paper_configured":False},
    }
    governance={"workflow_count":2,"approval_events":1,"completion_events":1,"policy":{"owner_approval_required_for":["email_review","whatsapp_review","calendar_review"]}}
    return build_diligence_manifest(version="v1.5.0",acquisition=acquisition,governance=governance)


def test_manifest_is_versioned_and_fingerprinted():
    d=sample()
    assert d["manifest"]["version"]=="v1.5.0"
    assert d["manifest"]["schema"]=="adam-acquisition-diligence/v1"
    assert len(d["manifest_sha256"])==64


def test_manifest_has_capabilities_and_risks():
    m=sample()["manifest"]
    assert len(m["capabilities"])>=8
    assert any(x["id"]=="governance" for x in m["capabilities"])
    assert any(x["id"]=="architecture" and x["severity"]=="attention" for x in m["risks"])


def test_manifest_privacy_safe():
    assert diligence_is_privacy_safe(sample()) is True


def test_privacy_check_rejects_secret_keys():
    assert diligence_is_privacy_safe({"client_secret":"bad"}) is False

from adam_core.perception_recovery_boundary import build_perception_recovery_manifest, perception_recovery_is_privacy_safe, perception_recovery_self_test
from adam_core.screen_perception_recovery import adaptive_click, perceive_interactive_elements


def test_v420_manifest_privacy_and_capabilities():
    p = build_perception_recovery_manifest("v4.2.0")
    assert perception_recovery_is_privacy_safe(p)
    c = p["perception_recovery"]["capabilities"]
    assert c["semantic_page_perception"] is True
    assert c["adaptive_selector_recovery"] is True
    assert c["owner_gate_preserved_during_recovery"] is True
    assert c["privacy"]["form_values_read"] is False


def test_v420_self_test_is_synthetic_and_owner_gated():
    r = perception_recovery_self_test()
    assert r["ok"] is True
    assert r["missing_primary_selector_recovered"] is True
    assert r["owner_gate_preserved_during_recovery"] is True
    assert r["external_network_accessed"] is False
    assert r["real_application_controlled"] is False


def test_v420_recovery_does_not_need_approval_for_link():
    class E:
        tag_name = "a"; text = "Learn more"
        def get_attribute(self, name): return ""
        def is_displayed(self): return True
        def is_enabled(self): return True
        def click(self): self.clicked = True
    class D:
        def __init__(self): self.e=E()
        def find_element(self, by, selector):
            if selector == "a": return self.e
            raise LookupError
        def find_elements(self, by, selector): return [self.e]
    d=D()
    r=adaptive_click(d, ".moved", fallback_selectors=["a"])
    assert r["ok"] and r["recovered"] and r["matched_by"] == "fallback_selector"
    assert perceive_interactive_elements(d)["input_values_read"] is False

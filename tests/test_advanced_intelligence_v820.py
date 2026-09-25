from pathlib import Path


def test_router_researches_explicit_and_local_questions():
    from adam_core.advanced_intelligence_router import route_question
    assert route_question("search the websites for Al Alak village families")["needs_web_search"] is True
    assert route_question("شو العائلات المعروفة ببلدة العلاق بالبقاع؟")["needs_web_search"] is True
    assert route_question("explain what a heat exchanger does")["needs_web_search"] is False


def test_router_never_changes_private_or_action_boundaries():
    from adam_core.advanced_intelligence_router import route_question
    r = route_question("search online")
    assert r["owner_private_data_allowed"] is False
    assert r["consequential_action_allowed"] is False


def test_responses_web_search_transport_shape():
    from adam_core.ai_provider_transport import complete_text_with_web_search
    class R:
        ok=True
        status_code=200
        text=""
        def json(self):
            return {"output":[{"type":"web_search_call"},{"type":"message","content":[{"type":"output_text","text":"verified answer"}]}]}
    class H:
        def __init__(self): self.call=None
        def post(self,*a,**k): self.call=(a,k); return R()
    h=H()
    ans, meta=complete_text_with_web_search("https://api.openai.com/v1","secret","gpt-5.6","question","English","system",http=h)
    assert ans == "verified answer"
    assert meta["web_search_used"] is True
    url=h.call[0][0]
    payload=h.call[1]["json"]
    assert url.endswith("/responses")
    assert {"type":"web_search"} in payload["tools"]
    assert "secret" not in str(payload)


def test_guest_route_uses_advanced_router_and_preserves_security():
    s=Path('app.py').read_text(encoding='utf-8')
    assert 'VERSION = "v8.2.0"' in s
    assert 'core_route_question(question, session.topic)' in s
    assert 'call_ai_advanced(' in s
    assert "Never expose or infer the owner's memory" in s
    assert 'Never expose or infer the owner' in s
    assert 'Never claim to have sent, called, scheduled, purchased, traded' in s
    assert 'web_search_attempted' in s

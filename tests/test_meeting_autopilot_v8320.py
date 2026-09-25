from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "app.py").read_text(encoding="utf-8")
HTML = (ROOT / "templates" / "real_meeting_attendance.html").read_text(encoding="utf-8")


def test_version_and_autopilot_policy():
    assert 'VERSION = "v8.3.2.0"' in APP
    assert 'PROFESSIONAL REPRESENTATIVE AUTOPILOT' in APP
    assert 'id="participationStyle"' in HTML
    assert 'Balanced — questions + material approval/commitment risks' in HTML
    assert 'Proactive — also flag material technical/commercial risks and owner actions' in HTML


def test_proactive_routing_is_bounded():
    assert 'function proactiveInterventionReason' in HTML
    assert "if(style==='conservative')return '';" in HTML
    assert 'If that reason is not actually material after considering the meeting context, return IGNORE:' in APP
    assert 'Do not interrupt merely to show knowledge' in APP


def test_live_register_present_and_retained():
    assert 'id="meetingRegister"' in HTML
    assert '_meeting_register_classification' in APP
    assert 'owner_approval_required' in APP
    assert 'live_meeting_register_retained' in APP
    clear_handler = HTML.split("document.getElementById('clear').onclick",1)[1].split("document.getElementById('endMeeting').onclick",1)[0]
    assert "meetingRegister').value=''" not in clear_handler
    end_handler = HTML.split("document.getElementById('endMeeting').onclick",1)[1].split("document.getElementById('analyze').onclick",1)[0]
    assert "meetingRegister').value=''" in end_handler


def test_report_metadata_and_native_docx():
    for field in ('meetingTitle','projectReference','meetingParticipants','meetingDateTime'):
        assert f'id="{field}"' in HTML
    assert '/api/personal-assistant/meeting-conversation/report.docx' in APP
    assert 'meeting_conversation_report_docx_v8320' in APP
    assert 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in APP
    assert 'Download Word (.docx)' in HTML


def test_report_uses_register_without_inventing():
    assert 'Register:' in APP and 'Owner approval required:' in APP
    assert 'Do not invent attendees, dates, approvals, decisions, costs, due dates, document numbers, or facts.' in APP
    assert 'live_register_included' in APP


def test_consequential_boundaries_preserved():
    assert 'must NOT approve variations' in APP
    assert 'separate owner approval mechanism' in APP
    assert 'Never pretend to be the owner or a human' in APP
    assert 'external_action_executed' in APP


def test_prior_thread_and_natural_dialogue_preserved():
    assert 'IMMEDIATE THREAD PRIORITY' in APP
    assert 'NATURAL PROFESSIONAL DIALOGUE' in APP
    assert 'followup_bound_to_immediate_thread' in APP
    assert 'meetingAdamSpeaking' in HTML and 'stopAdamSpeechForBargeIn' in HTML


def _load_helper(name):
    import ast
    tree = ast.parse(APP)
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    mod = ast.Module(body=[node], type_ignores=[])
    ns = {}
    exec(compile(mod, '<helper>', 'exec'), ns)
    return ns[name]


def test_live_register_classification_examples():
    classify = _load_helper('_meeting_register_classification')
    r = classify('Approve the variation cost with the contractor.', 'I cannot approve that.', 'Not approved')
    assert r['owner_approval_required'] is True
    assert r['register_type'] == 'Owner approval required'
    r = classify('What do we need next?', 'Please provide the hydraulic calculation.', 'Information required')
    assert r['action_candidate'] is True
    assert r['register_type'] == 'Information required'
    r = classify('There is a duct clash above the corridor.', 'We should review the coordination.', 'Explained', 'material technical risk')
    assert r['risk_flag'] is True
    assert r['register_type'] == 'Risk / intervention'

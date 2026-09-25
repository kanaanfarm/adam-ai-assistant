from pathlib import Path
import ast
import re

ROOT = Path(__file__).resolve().parents[1]
APP_TEXT = (ROOT / 'app.py').read_text(encoding='utf-8')


def _load_register_functions():
    tree = ast.parse(APP_TEXT)
    wanted = {'_meeting_explicit_owner_approval_gate', '_meeting_register_classification'}
    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in wanted]
    assert {f.name for f in funcs} == wanted
    module = ast.Module(body=funcs, type_ignores=[])
    ast.fix_missing_locations(module)
    ns = {'re': re}
    exec(compile(module, str(ROOT / 'app.py'), 'exec'), ns, ns)
    return ns


def test_version_bumped():
    assert 'VERSION = "v8.4.1.7"' in APP_TEXT


def test_explicit_mohamad_approval_is_owner_approval_required():
    ns = _load_register_functions()
    r = ns['_meeting_register_classification'](
        'Adam, the flow is unchanged and they want to proceed with 100 mm. What is your recommendation?',
        'Do not confirm the 100 mm size solely on unchanged flow. Verify the hydraulic calculation before Mohamad approves it.',
        'Recommendation',
    )
    assert r['owner_approval_required'] is True
    assert r['register_type'] == 'Owner approval required'
    assert r['register_state'] == 'Open / not approved'


def test_approval_gated_technical_change_is_consistent_even_without_name():
    ns = _load_register_functions()
    r = ns['_meeting_register_classification'](
        'Can the chilled water pipe proceed with 100 mm?',
        'Verify the hydraulic calculation before any change is approved.',
        'Recommendation',
    )
    assert r['owner_approval_required'] is True


def test_normal_technical_explanation_does_not_create_owner_gate():
    ns = _load_register_functions()
    r = ns['_meeting_register_classification'](
        'What is the function of a chilled water pump?',
        'It circulates chilled water through the system and provides the required flow and pressure.',
        'Explained',
    )
    assert r['owner_approval_required'] is False
    assert r['register_type'] in {'Discussion', 'Risk / intervention'}


def test_report_prompt_has_authoritative_approval_consistency_rule():
    assert "OWNER-APPROVAL GOVERNANCE EVIDENCE" in APP_TEXT
    assert "Never state 'Owner approval required: No' for an item whose retained evidence says Yes" in APP_TEXT
    assert 'approval_status_consistency_guard' in APP_TEXT
    assert 'owner_approval_required_count' in APP_TEXT


def test_deterministic_report_uses_same_governance_evidence():
    assert '## ITEMS NOT APPROVED / OWNER APPROVAL REQUIRED\\n" + governance_evidence' in APP_TEXT

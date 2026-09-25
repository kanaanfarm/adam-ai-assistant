import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / 'app.py'
APP = APP_PATH.read_text(encoding='utf-8')


def _load_selected_functions():
    tree = ast.parse(APP)
    names = {
        '_meeting_replace_report_section',
        '_meeting_count_report_list_items',
        '_meeting_reconcile_report_action_attribution',
    }
    body = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names]
    module = ast.Module(body=body, type_ignores=[])
    ast.fix_missing_locations(module)
    ns = {}
    exec(compile(module, str(APP_PATH), 'exec'), ns)
    return ns


def test_version_bumped():
    assert 'VERSION = "v8.4.1.13.2"' in APP


def test_visible_recommendation_counter_present():
    assert 'def _meeting_count_report_list_items' in APP
    assert 'adam_recommendation_visible_count' in APP
    assert 'adam_recommendation_count_source' in APP


def test_counts_four_visible_recommendations():
    ns = _load_selected_functions()
    report = '''## ACTION ITEMS\nNo participant-assigned actions were recorded.\n\n## ADAM RECOMMENDATIONS\n- Check filters.\n- Verify dampers.\n- Measure static pressure.\n- Confirm airflow.\n\n## NEXT STEPS\nRecommended follow-up only.\n'''
    reconciled, meta = ns['_meeting_reconcile_report_action_attribution'](report, [])
    assert meta['adam_recommendation_count'] == 4
    assert meta['adam_recommendation_visible_count'] == 4
    assert meta['adam_recommendation_count_source'] == 'report_section'
    assert 'No participant-assigned actions were recorded.' in reconciled


def test_numbered_recommendations_are_counted():
    ns = _load_selected_functions()
    report = '''## ADAM RECOMMENDATIONS\n1. Check filter.\n2. Verify fan speed.\n\n## OPEN / UNRESOLVED ITEMS\nNone.\n'''
    assert ns['_meeting_count_report_list_items'](report, 'ADAM RECOMMENDATIONS') == 2


def test_record_fallback_remains_available():
    ns = _load_selected_functions()
    report = '''## ADAM RECOMMENDATIONS\nRecommendation retained in paired evidence.\n\n## NEXT STEPS\nNone.\n'''
    records = [{'action_origin':'Adam recommendation'}]
    _, meta = ns['_meeting_reconcile_report_action_attribution'](report, records)
    assert meta['adam_recommendation_count'] == 1
    assert meta['adam_recommendation_visible_count'] == 0
    assert meta['adam_recommendation_count_source'] == 'retained_record'


def test_participant_action_count_unchanged():
    ns = _load_selected_functions()
    report = '''## ACTION ITEMS\nAnything.\n\n## ADAM RECOMMENDATIONS\n- Check filter.\n\n## NEXT STEPS\nAnything.\n'''
    records = [{'action_origin':'Participant-assigned action','question':'Please submit the calculation','topic':'HVAC'}]
    reconciled, meta = ns['_meeting_reconcile_report_action_attribution'](report, records)
    assert meta['participant_assigned_action_count'] == 1
    assert 'Participant-assigned action: Please submit the calculation' in reconciled

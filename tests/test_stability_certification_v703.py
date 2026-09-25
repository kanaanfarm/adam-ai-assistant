from pathlib import Path
from adam_core.stability_certification import stability_certification_self_test
ROOT=Path(__file__).resolve().parents[1]

def test_v703_stability_certification_is_synthetic_and_passes():
    r=stability_certification_self_test(ROOT)
    assert r['ok'] is True
    assert r['external_network_accessed'] is False
    assert r['real_consequential_action_executed'] is False
    assert r['critical_files_present_verified'] is True
    assert r['camera_left_right_orientation_verified'] is True

def test_v703_route_and_version_present():
    a=(ROOT/'app.py').read_text(encoding='utf-8')
    assert 'VERSION = "v8.1.0.1"' in a
    assert '/api/personal-assistant/stability-certification/self-test' in a

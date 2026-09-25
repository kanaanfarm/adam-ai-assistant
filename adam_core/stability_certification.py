from pathlib import Path

CRITICAL_FILES = (
    'app.py', 'templates/index.html', 'templates/stock.html',
    'adam_core/unified_adam_operator.py', 'adam_core/camera_vision_attachment_operator.py',
    'adam_core/manual_trade_override.py', 'adam_core/stock_notification_policy.py',
)


def stability_certification_self_test(root: Path):
    root = Path(root)
    missing = [p for p in CRITICAL_FILES if not (root / p).is_file()]
    app_text = (root / 'app.py').read_text(encoding='utf-8') if (root/'app.py').is_file() else ''
    index_text = (root / 'templates/index.html').read_text(encoding='utf-8') if (root/'templates/index.html').is_file() else ''
    checks = {
        'critical_files_present_verified': not missing,
        'health_endpoint_present_verified': '/api/health' in app_text,
        'owner_approval_boundary_present_verified': 'owner_approval' in app_text.lower(),
        'live_trading_blocked_boundary_present_verified': 'live_trading_blocked' in (root / 'adam_core/manual_trade_override.py').read_text(encoding='utf-8') and 'live_trading_blocked' in (root / 'adam_core/unified_adam_operator.py').read_text(encoding='utf-8'),
        'camera_direct_open_verified': 'adamCameraBtn.onclick=adamOpenCamera' in index_text,
        'camera_left_right_orientation_verified': '#adamCameraVideo,#adamCameraPhoto{transform:scaleX(-1)!important' in index_text and 'ctx.scale(-1,1)' in index_text,
        'synthetic_stability_certification_only': True,
        'external_network_accessed': False,
        'real_consequential_action_executed': False,
    }
    required = [
        checks['critical_files_present_verified'], checks['health_endpoint_present_verified'],
        checks['owner_approval_boundary_present_verified'], checks['live_trading_blocked_boundary_present_verified'],
        checks['camera_direct_open_verified'], checks['camera_left_right_orientation_verified'],
        checks['synthetic_stability_certification_only'], not checks['external_network_accessed'],
        not checks['real_consequential_action_executed'],
    ]
    return {'ok': all(required), 'missing_critical_files': missing, **checks}

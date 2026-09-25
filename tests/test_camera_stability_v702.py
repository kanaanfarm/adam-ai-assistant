from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_camera_ui_stability_fix():
    t=(ROOT/'templates/index.html').read_text(encoding='utf-8')
    assert 'adamCameraBtn.onclick=adamOpenCamera' in t
    assert "setTimeout(()=>{ if(adamCameraPicker)adamCameraPicker.click(); },250)" not in t
    assert '#adamCameraVideo,#adamCameraPhoto{transform:scaleX(-1)!important' in t
    assert 'ctx.scale(-1,1)' in t
    assert 'ctx.setTransform(-1' not in t
    assert 'adamSwitchCameraBtn' in t
    assert "adamCameraFacing==='environment'?'user':'environment'" in t
    assert 'adamCameraFallbackBtn' in t

def test_v702_version_and_self_test_route():
    a=(ROOT/'app.py').read_text(encoding='utf-8')
    assert 'VERSION = "v8.1.0.1"' in a
    assert '/api/personal-assistant/camera-stability/self-test' in a

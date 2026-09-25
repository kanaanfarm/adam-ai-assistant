from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_main_navigation_exposes_meeting_attendance():
    html = (ROOT / "templates" / "index.html").read_text(encoding="utf-8")
    assert 'href="/meeting-attendance"' in html
    assert '>Meeting Attendance</a>' in html

def test_meeting_attendance_route_remains_registered():
    app = (ROOT / "app.py").read_text(encoding="utf-8")
    assert 'VERSION = "v8.1.0.1"' in app
    assert '@app.route("/meeting-attendance", methods=["GET"])' in app
    assert 'render_template("real_meeting_attendance.html"' in app

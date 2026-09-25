from pathlib import Path
import tempfile

from adam_core.upgrade_continuity_memory import (
    remember_explicit_owner_turn,
    recall_owner_memory,
    recall_release_history,
    self_test,
)


def test_durable_owner_memory_only_explicit():
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "memory.json"
        saved = remember_explicit_owner_turn(
            path,
            "I didn't say third-water part. I said Empower request channel for chilled water.",
            task_focus="Tower MEP",
            version="v8.3.4.3",
        )
        ordinary = remember_explicit_owner_turn(path, "What is the generator capacity?")
        assert saved["stored"] is True
        assert ordinary["stored"] is False
        rows = recall_owner_memory(path, "What did I correct about Empower chilled water?", task_focus="Tower MEP")
        assert rows
        assert "Empower request channel" in rows[0]["text"]


def test_unrelated_task_does_not_import_old_correction():
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "memory.json"
        remember_explicit_owner_turn(
            path,
            "I didn't say third-water part. I said Empower request channel for chilled water.",
            task_focus="Tower MEP",
        )
        assert recall_owner_memory(path, "Explain RSI for stocks", task_focus="Stock analysis") == []


def test_old_release_test_is_recoverable_now():
    base = Path(__file__).resolve().parents[1]
    rows = recall_release_history(base, "old version correction test Empower request channel chilled water", limit=3)
    assert rows
    assert any("Empower request channel" in x["snippet"] for x in rows)
    assert any("8.3.4.1" in x["file"] or "8.3.4.2" in x["file"] for x in rows)


def test_module_self_test():
    assert self_test()["ok"] is True


def test_ui_and_routes_wired_for_continuity():
    base = Path(__file__).resolve().parents[1]
    app = (base / "app.py").read_text(encoding="utf-8")
    tpl = (base / "templates" / "real_meeting_attendance.html").read_text(encoding="utf-8")
    assert 'VERSION = "v8.3.4.3"' in app
    assert 'OWNER_CONTINUITY_MEMORY_FILE = owner_memory_path(BASE_DIR)' in app
    assert 'continuity_memory_enabled = body.get("continuity_memory") is True' in app
    assert 'Relevant durable owner continuity memory' in app
    assert 'Adam software test/release history' in app
    assert 'meetingContinuityMemory' in tpl
    assert 'universalContinuityMemory' in tpl
    assert 'localStorage' in tpl
    assert 'continuity_memory:document.getElementById' in tpl

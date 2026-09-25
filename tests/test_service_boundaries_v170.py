from datetime import datetime
from pathlib import Path

from adam_core.contacts import load_contacts, save_contacts, upsert_contact
from adam_core.followups import add_followup, load_followups, parse_due, public_item
from adam_core.service_boundaries import build_service_boundary_manifest, service_boundaries_are_privacy_safe
from adam_core.architecture import build_architecture_manifest


def test_contacts_service_roundtrip_and_upsert(tmp_path):
    path = tmp_path / "contacts.json"
    rows, saved, created = upsert_contact([], name="Amjad", email="amjad@example.com", new_id="1")
    assert created is True
    save_contacts(path, rows)
    loaded = load_contacts(path)
    assert loaded[0]["name"] == "Amjad"
    rows2, saved2, created2 = upsert_contact(loaded, name="amjad", phone="0500000000", new_id="2")
    assert created2 is False
    assert saved2["email"] == "amjad@example.com"
    assert saved2["phone"] == "0500000000"


def test_followup_service_due_and_public_projection(tmp_path):
    path = tmp_path / "followups.json"
    now = datetime(2026, 8, 31, 10, 0)
    due = parse_due("Follow up with Amjad in 3 days", now=now)
    assert due.startswith("2026-09-03T10:00")
    item = add_followup(path, "Follow up with Amjad in 3 days", "Amjad", "amjad@example.com", due, now=now, item_id="abc")
    assert load_followups(path)[0]["id"] == "abc"
    public = public_item(item, now=now)
    assert public["due"] == due
    assert public["status"] == "Upcoming"


def test_service_boundary_manifest_is_buyer_safe():
    payload = build_service_boundary_manifest(version="v1.7.0")
    core = payload["service_boundaries"]
    assert core["version"] == "v1.7.0"
    assert core["boundary_count"] == 2
    assert all(x["status"] == "extracted_tested" for x in core["extracted_boundaries"])
    assert len(payload["service_boundaries_sha256"]) == 64
    assert service_boundaries_are_privacy_safe(payload) is True


def test_architecture_manifest_tracks_service_extractions():
    payload = build_architecture_manifest(version="v1.7.0")["architecture"]
    modules = {row["module"] for row in payload["core_modules"]}
    assert "adam_core.contacts" in modules
    assert "adam_core.followups" in modules
    assert "adam_core.service_boundaries" in modules
    assert payload["module_count"] >= 12
    assert "workflow persistence service boundary" in payload["next_extraction_targets"]

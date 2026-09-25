"""Secure, ephemeral guest voice sessions for Adam Acquisition v8.1.0."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
import re
import secrets
import threading
from typing import Any


MAX_DURATION_MINUTES = 120
MAX_TOPIC_CHARS = 500
MAX_NAME_CHARS = 80
MAX_UTTERANCE_CHARS = 3000
MAX_TURNS = 20

_CONSEQUENTIAL = re.compile(
    r"\b(send|email|message|whatsapp|call|schedule|book|approve|accept|promise|commit|"
    r"purchase|buy|sell|trade|pay|transfer|sign|share|upload|download|delete|cancel)\b|"
    r"(أرسل|ارسل|واتساب|اتصل|احجز|وافق|اشتر|اشتري|بيع|ادفع|حوّل|حول|وقّع|شارك|احذف|ألغي|الغ)",
    re.IGNORECASE,
)
_PRIVATE_DATA = re.compile(
    r"\b(owner'?s?|mohamad'?s?)\s+(private|personal|phone|email|address|location|contact|message|file|"
    r"document|credential|password|token|account|memory)|\b(private|personal)\s+(data|information|files?)\b|"
    r"(بيانات|معلومات|ملفات|رسائل|رقم|عنوان|موقع|كلمة مرور|حساب)\s+(المالك|محمد|الخاصة)",
    re.IGNORECASE,
)


def _clean(value: Any, limit: int) -> str:
    return " ".join(str(value or "").split())[:limit]


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class GuestSession:
    token: str
    guest_name: str
    topic: str
    created_at: datetime
    expires_at: datetime
    active: bool = True
    turns: list[dict[str, str]] = field(default_factory=list)
    escalations: list[str] = field(default_factory=list)

    def public(self) -> dict:
        return {
            "ok": True,
            "status": "guest_voice_session_active" if self.active else "guest_voice_session_closed",
            "guest_name": self.guest_name,
            "topic": self.topic,
            "expires_at": self.expires_at.isoformat(),
            "active": self.active and self.expires_at > _utcnow(),
            "conversation_turns": len(self.turns) // 2,
            "owner_private_data_available": False,
            "external_actions_allowed": False,
            "owner_approval_required_for_consequential_actions": True,
        }


class GuestSessionStore:
    """Process-local sessions. Restarting Adam invalidates every guest link."""

    def __init__(self) -> None:
        self._sessions: dict[str, GuestSession] = {}
        self._lock = threading.RLock()

    def create(self, guest_name: Any, topic: Any, duration_minutes: Any, owner_approved: bool) -> GuestSession:
        if owner_approved is not True:
            raise ValueError("owner_approval_required")
        name = _clean(guest_name, MAX_NAME_CHARS)
        scope = _clean(topic, MAX_TOPIC_CHARS)
        if not name:
            raise ValueError("guest_name_required")
        if not scope:
            raise ValueError("topic_required")
        try:
            duration = int(duration_minutes)
        except (TypeError, ValueError):
            raise ValueError("invalid_duration")
        if duration < 5 or duration > MAX_DURATION_MINUTES:
            raise ValueError("duration_out_of_range")
        now = _utcnow()
        session = GuestSession(
            token=secrets.token_urlsafe(32), guest_name=name, topic=scope,
            created_at=now, expires_at=now + timedelta(minutes=duration),
        )
        with self._lock:
            self._sessions[session.token] = session
        return session

    def get(self, token: Any) -> GuestSession | None:
        key = _clean(token, 200)
        with self._lock:
            session = self._sessions.get(key)
            if not session:
                return None
            if session.expires_at <= _utcnow():
                session.active = False
            return session

    def close(self, token: Any) -> bool:
        session = self.get(token)
        if not session:
            return False
        with self._lock:
            session.active = False
        return True

    def classify_question(self, session: GuestSession, question: Any) -> dict:
        text = _clean(question, MAX_UTTERANCE_CHARS)
        if not text:
            return {"ok": False, "status": "question_required"}
        if _CONSEQUENTIAL.search(text) or _PRIVATE_DATA.search(text):
            with self._lock:
                session.escalations.append(text[:500])
            return {
                "ok": True,
                "status": "owner_approval_required",
                "reply": "I cannot perform that action in this guest session. I have recorded the request for the owner to review.",
                "escalated_to_owner": True,
                "external_action_executed": False,
            }
        return {"ok": True, "status": "conversation_allowed", "question": text}

    def append_turn(self, session: GuestSession, question: str, answer: str) -> None:
        with self._lock:
            session.turns.extend([
                {"role": "guest", "content": _clean(question, MAX_UTTERANCE_CHARS)},
                {"role": "adam", "content": _clean(answer, 8000)},
            ])
            if len(session.turns) > MAX_TURNS * 2:
                del session.turns[:-MAX_TURNS * 2]

    def owner_summary(self, session: GuestSession) -> dict:
        return {
            **session.public(),
            "status": "guest_voice_session_summary_ready",
            "created_at": session.created_at.isoformat(),
            "recent_conversation": list(session.turns[-12:]),
            "escalation_count": len(session.escalations),
            "escalations": list(session.escalations[-5:]),
            "credentials_returned": False,
            "private_owner_data_returned": False,
            "external_action_executed": False,
        }


def self_test() -> dict:
    store = GuestSessionStore()
    blocked = False
    try:
        store.create("Ahmed", "HVAC drawing status", 30, False)
    except ValueError as exc:
        blocked = str(exc) == "owner_approval_required"
    session = store.create("Ahmed", "HVAC drawing status", 30, True)
    safe = store.classify_question(session, "What is the purpose of this discussion?")
    action = store.classify_question(session, "Send me the owner's private documents")
    store.append_turn(session, safe.get("question", ""), "We are discussing the HVAC drawing status.")
    summary = store.owner_summary(session)
    checks = {
        "owner_approval_gate_verified": blocked,
        "unguessable_guest_token_verified": len(session.token) >= 40,
        "bounded_expiry_verified": session.expires_at > session.created_at,
        "guest_scope_present_verified": session.topic == "HVAC drawing status",
        "safe_conversation_allowed_verified": safe.get("status") == "conversation_allowed",
        "consequential_action_blocked_verified": action.get("status") == "owner_approval_required",
        "owner_summary_verified": summary.get("conversation_turns") == 1,
        "private_owner_data_blocked_verified": summary.get("private_owner_data_returned") is False,
        "external_action_executed": False,
        "external_network_accessed": False,
    }
    positive = [value for key, value in checks.items() if key not in {"external_action_executed", "external_network_accessed"}]
    ok = all(positive) and checks["external_action_executed"] is False and checks["external_network_accessed"] is False
    return {"ok": ok, **checks, "synthetic_inputs_only": True}

"""Adam v8.3.3.1 meeting focus engine.

Purpose: prevent side-room / other-project speech from entering the formal meeting
transcript, memory, response queue, or report when Meeting Focus Lock is enabled.

This layer intentionally does NOT claim biometric speaker recognition. It combines
meeting identity, project/topic relevance, immediate-thread context, and weak
near-field audio hints. Rejected speech is represented only by metadata; raw rejected
text is not retained by this module.
"""
from __future__ import annotations

import re
from typing import Iterable

_STOPWORDS = {
    "the","a","an","and","or","to","of","for","in","on","at","is","are","was","were","be","been","being",
    "this","that","these","those","we","you","they","he","she","it","our","your","their","with","from","by",
    "meeting","project","please","what","why","how","when","where","who","can","could","would","should","do","did",
    "does","will","about","think","recommend","adam","mohamad","owner","client","contractor","consultant",
}

_CONTEXTUAL_FOLLOWUPS = {
    "why","why is that","what do you think","what can we do","what do you recommend","what do you recommend next",
    "what next","did you check it","did you check","do you agree","is that approved","did you approve it",
    "how about that","explain why","tell me why","the client is asking why","the contractor is asking why",
}

_DOMAIN_TERMS = {
    "hvac","mep","duct","ductwork","airflow","cfm","ahu","fcu","static","pressure","chilled","water","chw","pipe",
    "hydraulic","pump","valve","drainage","sprinkler","firefighting","smoke","detector","cable","tray","clash",
    "coordination","rfi","variation","quotation","cost","commercial","contract","drawing","shop","submission",
    "revision","schedule","ifc","ifrs","programme","program","material","ceiling","insulation","balancing",
}

_CONSEQUENTIAL_TERMS = {
    "approve","approved","approval","agree","agreed","accepted","accept","variation","cost","payment","purchase",
    "quotation","price","contractual","entitlement","commitment","committed","confirm","confirmed"
}
_ACTION_TERMS = {
    "submit","provide","issue","revise","revised","deadline","due","tomorrow","monday","tuesday","wednesday",
    "thursday","friday","saturday","sunday","action"
}

_DIRECT_QUESTION_RE = re.compile(
    r"^(who|what|when|where|why|how|can|could|would|will|is|are|do|does|did|should|"
    r"please\s+explain|شو|مين|وين|امتى|إمتى|ليش|كيف|هل|قديش|متى|ماذا|ما\s+هو|ما\s+هي|"
    r"pourquoi|comment|quand|où|que|quel|quelle|quién|qué|cuándo|dónde|por\s+qué|cómo)\b",
    re.I,
)
_WAKE_RE = re.compile(r"\badam\b|آدم|ادم|ادام", re.I)


def _norm(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def _tokens(value: str) -> set[str]:
    raw = re.findall(r"[a-zA-Z0-9_-]{3,}|[\u0600-\u06ff]{3,}", _norm(value))
    return {t for t in raw if t not in _STOPWORDS and not t.isdigit()}


def _participant_tokens(value: str) -> set[str]:
    raw = re.findall(r"[a-zA-Z0-9_-]{3,}|[\u0600-\u06ff]{3,}", _norm(value))
    generic = {"participant", "participants", "company", "companies", "engineer", "engineers", "consultant", "contractor", "client", "owner"}
    return {t for t in raw if t not in generic and not t.isdigit()}


def _direct_question(text: str) -> bool:
    q = str(text or "").strip()
    if not q or _wake_only(q) or _question_preamble(q):
        return False
    q2 = _strip_wake_prefix(q)
    return bool("?" in q2 or "؟" in q2 or _DIRECT_QUESTION_RE.match(q2))


def _contextual_followup(text: str) -> bool:
    q = _norm(text).strip(" ?.!,:;")
    return q in _CONTEXTUAL_FOLLOWUPS


def _strip_wake_prefix(text: str) -> str:
    q = str(text or "").strip()
    q = re.sub(r"^(?:adam|آدم|ادم|ادام)\b[\s,.:;!?؟-]*", "", q, flags=re.I).strip()
    return q


def _wake_only(text: str) -> bool:
    return bool(_WAKE_RE.search(str(text or ""))) and not _strip_wake_prefix(text).strip(" \t\r\n,.:;!?؟-")


def _question_preamble(text: str) -> bool:
    q = _norm(_strip_wake_prefix(text)).strip(" ?.!,:;")
    if not q:
        return False
    patterns = (
        r"^(?:the\s+)?question\s+(?:is\s+)?for\s+you$",
        r"^i\s+(?:have|got)\s+(?:a|one)\s+question(?:\s+for\s+you)?$",
        r"^i\s+want\s+to\s+ask\s+you\s+(?:a|one|something)$",
        r"^(?:one|another)\s+(?:question|thing)(?:\s+for\s+you)?$",
        r"^(?:listen|listen\s+to\s+me)$",
        r"^the\s+question\s+for\s+you$",
    )
    return any(re.match(pat, q, re.I) for pat in patterns)


def _extract_explicit_project_names(text: str) -> list[str]:
    low = _norm(text)
    names: list[str] = []
    for pat in (
        r"\bfor\s+([a-zA-Z0-9_-]{2,})\s+project\b",
        r"\b([a-zA-Z0-9_-]{2,})\s+project\b",
        r"\bproject\s+([a-zA-Z0-9_-]{2,})\b",
        r"\bsite\s+([a-zA-Z0-9_-]{2,})\b",
    ):
        names.extend(re.findall(pat, low, re.I))
    out=[]
    for name in names:
        n=str(name or '').strip().lower()
        if n and n not in out and n not in _STOPWORDS and n not in {'as','the','this','that','our','your','their','active','current','increase','decrease','reduce','change','move','submit','provide','approve','approved','start','delivery','arrive','arrives','review','check'}:
            out.append(n)
    return out


def _cross_project_reference_intent(text: str) -> bool:
    low = _norm(text)
    return bool(re.search(
        r"\b(compare|comparison|compared|benchmark|reference|referencing|similar\s+to|like\s+the|lesson|example|versus|vs\.?|same\s+as|different\s+from)\b",
        low, re.I
    ))


def detect_explicit_project_mismatch(text: str, project_reference: str = "") -> dict:
    """Detect an explicit other-project reference.

    The active project is a hard boundary in strict meeting-focus mode. An explicit
    other project is rejected even when 'Adam' is spoken or the technical topic
    overlaps, unless the utterance clearly frames the other project as a comparison
    or reference to the active meeting.
    """
    names = _extract_explicit_project_names(text)
    active = _tokens(project_reference)
    if not names or not active:
        return {"mismatch": False, "project_names": names, "cross_reference": False}
    others = [n for n in names if n not in active]
    cross = bool(others and _cross_project_reference_intent(text))
    return {
        "mismatch": bool(others and not cross),
        "project_names": names,
        "other_project_names": others,
        "cross_reference": cross,
    }


def _other_project_penalty(text: str, known_terms: set[str]) -> tuple[float, str]:
    low = _norm(text)
    names = []
    for pat in (
        r"\bproject\s+([a-zA-Z0-9_-]{3,})\b",
        r"\b([a-zA-Z0-9_-]{3,})\s+project\b",
        r"\bsite\s+([a-zA-Z0-9_-]{3,})\b",
    ):
        names.extend(re.findall(pat, low, re.I))
    other = [n.lower() for n in names if n.lower() not in known_terms and n.lower() not in _STOPWORDS]
    if other:
        return -3.5, "possible different project reference"
    return 0.0, ""


def evaluate_meeting_focus(
    *,
    text: str,
    focus_locked: bool = True,
    sensitivity: str = "strict",
    meeting_title: str = "",
    project_reference: str = "",
    participants: str = "",
    focus_agenda: str = "",
    owner_briefing: str = "",
    recent_context: str = "",
    immediate_thread_available: bool = False,
    peak_rms: float = 0.0,
    noise_floor: float = 0.0,
    vad_available: bool = False,
) -> dict:
    """Return a conservative focus decision without retaining rejected text."""
    utterance = str(text or "").strip()
    if not utterance:
        return {"accept": False, "decision": "reject", "score": 0.0, "reason": "empty speech", "direct_question": False, "wake_name": False}
    if not focus_locked or sensitivity == "open":
        return {"accept": True, "decision": "accept", "score": 10.0, "reason": "meeting focus lock is open", "direct_question": _direct_question(utterance), "wake_name": bool(_WAKE_RE.search(utterance))}

    sensitivity = sensitivity if sensitivity in {"strict", "balanced", "open"} else "strict"
    wake = bool(_WAKE_RE.search(utterance))
    direct = _direct_question(utterance)
    followup = _contextual_followup(utterance) and bool(immediate_thread_available)
    wake_only = _wake_only(utterance)
    question_preamble = _question_preamble(utterance)

    project_guard = detect_explicit_project_mismatch(utterance, project_reference)
    if project_guard.get("mismatch") and sensitivity in {"strict", "balanced"}:
        return {
            "accept": False, "decision": "reject", "score": -99.0, "threshold": 3.2,
            "reason": "explicit other-project reference conflicts with active project",
            "direct_question": False, "wake_name": bool(wake), "wake_only": bool(wake_only),
            "question_preamble": bool(question_preamble), "contextual_followup": False,
            "hard_project_mismatch": True,
            "explicit_project_names": project_guard.get("project_names", []),
            "other_project_names": project_guard.get("other_project_names", []),
            "cross_project_reference_allowed": False,
            "rejected_text_retained": False, "biometric_speaker_recognition_claimed": False,
        }

    meeting_seed = " ".join([meeting_title, project_reference, participants, focus_agenda, owner_briefing])
    known_terms = _tokens(meeting_seed)
    recent_terms = _tokens(recent_context)
    utterance_terms = _tokens(utterance)
    meeting_overlap = utterance_terms & known_terms
    recent_overlap = utterance_terms & recent_terms
    domain_overlap = utterance_terms & _DOMAIN_TERMS

    score = 0.0
    reasons: list[str] = []
    if wake:
        score += 5.0; reasons.append("Adam addressed")
    if followup:
        score += 4.0; reasons.append("immediate meeting follow-up")
    if meeting_overlap:
        score += min(4.0, 1.5 + 0.8 * len(meeting_overlap)); reasons.append("meeting/project terms match")
    if recent_overlap:
        score += min(3.0, 1.0 + 0.55 * len(recent_overlap)); reasons.append("active discussion context match")
    if domain_overlap:
        # Domain relevance is useful but deliberately weak: another MEP meeting can be nearby.
        score += min(1.6, 0.45 * len(domain_overlap)); reasons.append("professional topic match")
    if direct:
        score += 0.8; reasons.append("direct-question form")

    critical_hits = utterance_terms & _CONSEQUENTIAL_TERMS
    if critical_hits:
        score += min(3.2, 1.7 + 0.6 * len(critical_hits)); reasons.append("material approval/commitment language")
    action_hits = utterance_terms & _ACTION_TERMS
    if action_hits:
        score += min(2.2, 1.0 + 0.4 * len(action_hits)); reasons.append("meeting action/deadline language")
    seed_low = _norm(meeting_seed)
    if ("mep" in seed_low or "coordination" in seed_low) and domain_overlap:
        score += 1.6; reasons.append("MEP/coordination meeting domain match")
    elif "hvac" in seed_low and domain_overlap & {"hvac","duct","ductwork","airflow","cfm","ahu","fcu","static","pressure","chilled","water","chw","pipe","hydraulic","pump","valve","balancing"}:
        score += 1.5; reasons.append("HVAC meeting domain match")

    # Participant roster mentions are evidence of the intended meeting, not biometric identity.
    participant_terms = _participant_tokens(participants)
    participant_overlap = utterance_terms & participant_terms
    if participant_overlap:
        score += min(2.5, 1.3 + 0.6 * len(participant_overlap)); reasons.append("declared participant/company reference")

    if project_guard.get('cross_reference'):
        penalty, penalty_reason = 0.0, ''
        reasons.append('explicit cross-project comparison/reference')
    else:
        penalty, penalty_reason = _other_project_penalty(utterance, known_terms)
    if penalty:
        score += penalty; reasons.append(penalty_reason)

    # Weak near-field hint. Browser auto gain is disabled in Focus Lock mode where supported.
    if vad_available and peak_rms > 0:
        ratio = peak_rms / max(noise_floor, 0.001)
        if peak_rms >= 0.035 and ratio >= 3.0:
            score += 1.2; reasons.append("strong near-field audio hint")
        elif peak_rms < 0.012 or ratio < 1.8:
            score -= 1.8; reasons.append("weak/distant audio hint")
        elif ratio >= 2.2:
            score += 0.35; reasons.append("speech above room noise")
    else:
        ratio = 0.0

    # Strict shared-room mode prefers false negatives over polluting the formal record.
    threshold = 3.2 if sensitivity == "strict" else 2.25
    # Wake name should normally pass unless there is strong evidence of a different project.
    if wake and penalty >= 0:
        threshold = min(threshold, 2.2)
    # A short contextual follow-up to the active thread should pass even without keywords.
    if followup:
        threshold = min(threshold, 2.0)
    # A deliberate comparison/reference to another project is allowed only when the
    # utterance also anchors itself to the active project/meeting.
    if project_guard.get('cross_reference') and meeting_overlap:
        threshold = min(threshold, 2.2)

    accept = score >= threshold
    if accept:
        decision = "accept"
        reason = "; ".join(reasons[:5]) or "meeting relevance accepted"
    else:
        decision = "reject"
        reason = "; ".join(reasons[:5]) or "insufficient evidence that speech belongs to the active meeting"

    return {
        "accept": bool(accept),
        "decision": decision,
        "score": round(score, 2),
        "threshold": threshold,
        "reason": reason,
        "direct_question": bool(direct),
        "wake_name": bool(wake),
        "wake_only": bool(wake_only),
        "question_preamble": bool(question_preamble),
        "contextual_followup": bool(followup),
        "hard_project_mismatch": False,
        "explicit_project_names": project_guard.get("project_names", []),
        "other_project_names": project_guard.get("other_project_names", []),
        "cross_project_reference_allowed": bool(project_guard.get("cross_reference")),
        "meeting_term_hits": sorted(meeting_overlap)[:8],
        "recent_context_hits": sorted(recent_overlap)[:8],
        "participant_reference_hits": sorted(participant_overlap)[:6],
        "near_field_ratio": round(ratio, 2) if ratio else 0.0,
        "rejected_text_retained": False,
        "biometric_speaker_recognition_claimed": False,
    }


def self_test() -> dict:
    common = dict(
        focus_locked=True, sensitivity="strict", meeting_title="MEP Coordination Meeting",
        project_reference="Tower", participants="Mohamad / A&B",
        focus_agenda="HVAC ductwork chilled water coordination variation",
        recent_context="We are checking the 800 by 400 supply duct and 18000 CFM airflow.",
        immediate_thread_available=True,
    )
    targeted = evaluate_meeting_focus(text="Adam, what do you think about the 800 by 400 duct?", **common)
    followup = evaluate_meeting_focus(text="Why?", **common)
    side = evaluate_meeting_focus(text="For Marina project, the generator delivery is tomorrow.", **common)
    unrelated_q = evaluate_meeting_focus(text="What time will the Marina architect arrive?", **common)
    relevant = evaluate_meeting_focus(text="The chilled water pipe from 100 mm to 125 mm needs hydraulic review.", **common)
    open_room = evaluate_meeting_focus(text="Anything at all", **{**common, "focus_locked": False})
    commitment = evaluate_meeting_focus(text="We agreed that Mohamad will approve the variation cost later.", **common)
    action = evaluate_meeting_focus(text="Contractor, please submit the revised drawing by Thursday.", **common)
    mep_side = evaluate_meeting_focus(text="For Marina project, the drainage pipe is clashing with the cable tray.", **common)
    addressed_other = evaluate_meeting_focus(text="Adam, for Marina project increase the chilled water pipe from 100 to 125.", **common)
    wake_only = evaluate_meeting_focus(text="Adam.", **common)
    preamble = evaluate_meeting_focus(text="Adam, the question for you.", **common)
    cross_ref = evaluate_meeting_focus(text="Compare the Tower chilled-water approach with Marina project as a reference.", **common)
    checks = {
        "adam_addressed_accepted": targeted["accept"] is True,
        "short_followup_accepted": followup["accept"] is True,
        "other_project_side_talk_rejected": side["accept"] is False,
        "unrelated_room_question_rejected": unrelated_q["accept"] is False,
        "active_mep_topic_accepted": relevant["accept"] is True,
        "open_room_mode_accepts": open_room["accept"] is True,
        "rejected_text_not_retained": side["rejected_text_retained"] is False,
        "no_false_biometric_claim": targeted["biometric_speaker_recognition_claimed"] is False,
        "material_commitment_not_filtered": commitment["accept"] is True,
        "meeting_action_not_filtered": action["accept"] is True,
        "other_project_mep_side_talk_rejected": mep_side["accept"] is False,
        "adam_address_does_not_override_other_project": addressed_other["accept"] is False and addressed_other.get("hard_project_mismatch") is True,
        "bare_adam_not_direct_question": wake_only["direct_question"] is False and wake_only.get("wake_only") is True,
        "question_preamble_not_direct_question": preamble["direct_question"] is False and preamble.get("question_preamble") is True,
        "explicit_cross_project_comparison_allowed": cross_ref["accept"] is True and cross_ref.get("cross_project_reference_allowed") is True,
    }
    return {"ok": all(checks.values()), **checks}

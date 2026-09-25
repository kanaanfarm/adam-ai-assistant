"""Adam v8.4.0.1 — correction isolation / context precision guard.

The guard prevents a natural owner correction from being silently merged with nearby
technical details that the owner did not actually restate or reconnect.

It is deliberately conservative: it does not execute actions, change authority, or
persist additional data. It only supplies a bounded instruction to the AI prompt.
"""
from __future__ import annotations

import re
from typing import Iterable

_MAX_TEXT = 1200

_CORRECTION_PATTERNS = (
    r"\bi\s+(?:didn['’]?t|did\s+not|never)\s+say\b",
    r"\bthat(?:'s| is)\s+not\s+what\s+i\s+said\b",
    r"\byou\s+(?:misheard|misunderstood)\b",
    r"\bcorrection\b",
    r"\bcorrect\s+(?:that|this|it)\b",
    r"\bno\s*[,—-]?\s*(?:i\s+said|i\s+mean|i\s+meant|not\s+that)\b",
    r"\bwhat\s+i\s+said\s+was\b",
    r"\bi\s+(?:mean|meant)\b",
    r"(?:ما\s+قلت|أنا\s+قلت|انا\s+قلت|قصدي|كنت\s+قصدي|مش\s+هيك|مو\s+هيك|تصحيح|صحح)",
)


def _clean(value: object, limit: int = _MAX_TEXT) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())[:limit]


def is_explicit_correction(text: str) -> bool:
    q = _clean(text)
    if not q:
        return False
    return any(re.search(pattern, q, re.I | re.S) for pattern in _CORRECTION_PATTERNS)


def latest_owner_correction(history: Iterable[dict] | None) -> str:
    """Return only the newest explicit owner correction from supplied chat history."""
    rows = list(history or [])
    for item in reversed(rows[-24:]):
        if not isinstance(item, dict) or item.get("role") != "user":
            continue
        text = _clean(item.get("content"))
        if text and is_explicit_correction(text):
            return text
    return ""


def build_correction_isolation_instruction(latest_text: str, history: Iterable[dict] | None = None) -> str:
    """Create a bounded prompt instruction enforcing correction precision.

    A correction changes only what the owner explicitly corrected. Adjacency in the
    chat is not evidence that sizes, dates, people, projects, causes, approvals or
    actions from an older turn belong to the corrected point.
    """
    latest = _clean(latest_text)
    current_is_correction = is_explicit_correction(latest)
    correction = latest if current_is_correction else latest_owner_correction(history)
    if not correction:
        return ""

    phase = "LATEST OWNER MESSAGE IS AN EXPLICIT CORRECTION." if current_is_correction else "A RECENT OWNER CORRECTION REMAINS ACTIVE FOR CONTEXT PRECISION."
    return (
        "CORRECTION ISOLATION POLICY — " + phase + "\n"
        "Authoritative correction wording: \"" + correction.replace('"', "'") + "\"\n"
        "Rules:\n"
        "1. Treat the owner's corrected wording as authoritative and supersede conflicting earlier assistant wording.\n"
        "2. Change ONLY the point the owner explicitly corrected. Do not automatically attach nearby historical facts to it.\n"
        "3. Do not infer that an earlier number, size, date, person, project, cause, approval, scope, action, or technical detail belongs to the corrected point unless the owner explicitly reconnects it.\n"
        "4. Conversation adjacency is not confirmation. If a linkage is not stated, keep it separate or say the linkage is not confirmed.\n"
        "5. When acknowledging a fresh correction, restate the corrected point minimally and do not embellish it with prior details.\n"
        "6. When later summarizing, preserve the corrected wording and do not reintroduce the superseded or unconfirmed association.\n"
    )


def self_test() -> dict:
    correction = "I didn't say third-water part. I said Empower request channel for chilled water."
    guard = build_correction_isolation_instruction(
        correction,
        [
            {"role": "user", "content": "Increase chilled water pipe from 100 mm to 125 mm."},
            {"role": "assistant", "content": "The request is 100 to 125 mm."},
        ],
    )
    followup_guard = build_correction_isolation_instruction(
        "What are the three open issues?",
        [
            {"role": "user", "content": "Increase chilled water pipe from 100 mm to 125 mm."},
            {"role": "assistant", "content": "The request is 100 to 125 mm."},
            {"role": "user", "content": correction},
        ],
    )
    unrelated = build_correction_isolation_instruction(
        "What is the capital of Australia?",
        [{"role": "user", "content": "What is a heat pump?"}],
    )
    return {
        "ok": bool(
            is_explicit_correction(correction)
            and "Empower request channel for chilled water" in guard
            and "100 mm" not in guard
            and "125 mm" not in guard
            and "Conversation adjacency is not confirmation" in guard
            and "Empower request channel for chilled water" in followup_guard
            and unrelated == ""
        ),
        "fresh_correction_detected": is_explicit_correction(correction),
        "fresh_guard_excludes_prior_sizes": "100 mm" not in guard and "125 mm" not in guard,
        "followup_guard_retains_correction_boundary": "Empower request channel for chilled water" in followup_guard,
        "unrelated_no_guard": unrelated == "",
    }

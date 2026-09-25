"""Adam v8.2 advanced intelligence routing.

This is deliberately conservative: it decides when live public research can
materially improve a normal knowledge answer. It never grants access to owner
private data and never authorizes consequential actions.
"""
import re

_EXPLICIT_SEARCH = re.compile(
    r"\b(search|google|look up|lookup|find online|on the web|internet|latest|current|today|news|price|weather)\b"
    r"|(?:فتش|فتّش|سيرش|ابحث|بحث|دور|دوّر|عالنت|على النت|المواقع|اخر|آخر|اليوم|حاليا|حالياً)",
    re.I,
)
_LOCAL_NICHE = re.compile(
    r"\b(village|town|neighborhood|neighbourhood|district|municipality|families|family names|who lives|residents)\b"
    r"|(?:قرية|بلدة|ضيعة|منطقة|بلدية|عائلات|العائلات|سكان|مين ساكن|من يسكن|اسماء العائلات|أسماء العائلات)",
    re.I,
)
_CURRENT = re.compile(
    r"\b(latest|current|today|now|recent|202[5-9]|price|stock|market|news|schedule|open now)\b"
    r"|(?:اليوم|هلأ|هلق|حاليا|حالياً|اخر|آخر|جديد|سعر|بورصة|سوق|اخبار|أخبار)",
    re.I,
)


def route_question(question, topic=""):
    text = f"{question or ''} {topic or ''}".strip()
    explicit = bool(_EXPLICIT_SEARCH.search(text))
    local_niche = bool(_LOCAL_NICHE.search(text))
    current = bool(_CURRENT.search(text))
    needs_web = explicit or local_niche or current
    reason = "explicit_search" if explicit else ("local_or_niche_fact" if local_niche else ("time_sensitive" if current else "model_reasoning"))
    return {
        "mode": "research" if needs_web else "reasoning",
        "needs_web_search": needs_web,
        "reason": reason,
        "owner_private_data_allowed": False,
        "consequential_action_allowed": False,
    }

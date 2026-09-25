"""v8.3.1 multilingual professional meeting language policy.

Adam listens with automatic multilingual transcription. Meeting replies are English
by default. A participant can explicitly request another reply language; the chosen
language remains active for the meeting session until another explicit request.
"""
from __future__ import annotations

import re
from typing import Optional

DEFAULT_REPLY_LANGUAGE = "English"

# Common meeting languages. The model can still understand languages outside this
# list; this map is only for deterministic spoken requests to switch Adam's reply.
_LANGUAGE_ALIASES = {
    "English": ("english", "الانجليزية", "الإنجليزية", "انجليزي", "إنجليزي", "بالانجليزي", "بالإنجليزي"),
    "Lebanese Arabic": ("arabic", "العربية", "عربي", "بالعربي", "باللغة العربية", "lebanese arabic", "لبناني", "باللبناني"),
    "French": ("french", "français", "francais", "فرنسي", "بالفرنسي"),
    "Spanish": ("spanish", "español", "espanol", "اسباني", "إسباني", "بالاسباني", "بالإسباني"),
    "German": ("german", "deutsch", "الماني", "ألماني", "بالالماني", "بالألماني"),
    "Italian": ("italian", "italiano", "ايطالي", "إيطالي", "بالايطالي", "بالإيطالي"),
    "Portuguese": ("portuguese", "português", "portugues", "برتغالي", "بالبرتغالي"),
    "Turkish": ("turkish", "türkçe", "turkce", "تركي", "بالتركي"),
    "Russian": ("russian", "русский", "روسي", "بالروسي"),
    "Chinese": ("chinese", "mandarin", "中文", "الصينية", "صيني", "بالصيني"),
    "Japanese": ("japanese", "日本語", "ياباني", "بالياباني"),
    "Korean": ("korean", "한국어", "كوري", "بالكوري"),
    "Hindi": ("hindi", "हिन्दी", "हिंदी", "هندي", "بالهندي"),
    "Urdu": ("urdu", "اردو", "أردو"),
    "Persian": ("persian", "farsi", "فارسي", "فارسيه", "فارسية"),
}

_COMMAND_CUES = (
    "speak", "answer", "reply", "respond", "continue", "explain", "talk", "use",
    "احكي", "تكلم", "تكلّم", "جاوب", "رد", "رُد", "كمل", "كمّل", "اشرح", "استعمل",
)


def detect_requested_reply_language(text: str) -> Optional[str]:
    """Return an explicit participant-requested reply language, else None.

    Ordinary mentions of a language do not switch Adam; the utterance must also
    contain a speech/answer command cue.
    """
    raw = str(text or "").strip()
    if not raw:
        return None
    low = raw.casefold()
    if not any(cue.casefold() in low for cue in _COMMAND_CUES):
        return None
    for canonical, aliases in _LANGUAGE_ALIASES.items():
        if any(alias.casefold() in low for alias in aliases):
            return canonical
    return None


def tts_locale_for_reply(language: str) -> str:
    lang = str(language or DEFAULT_REPLY_LANGUAGE).strip().casefold()
    mapping = {
        "english": "en-US",
        "lebanese arabic": "ar-LB",
        "arabic": "ar-LB",
        "french": "fr-FR",
        "spanish": "es-ES",
        "german": "de-DE",
        "italian": "it-IT",
        "portuguese": "pt-PT",
        "turkish": "tr-TR",
        "russian": "ru-RU",
        "chinese": "zh-CN",
        "japanese": "ja-JP",
        "korean": "ko-KR",
        "hindi": "hi-IN",
        "urdu": "ur-PK",
        "persian": "fa-IR",
    }
    return mapping.get(lang, "auto")


def professional_scope_prompt(scope: str = "auto") -> str:
    """Stable meeting-representative behavior across professional disciplines."""
    selected = str(scope or "auto").strip()
    return (
        "Operate as a cross-disciplinary professional meeting representative. "
        "Infer the discipline from the meeting question and context and use the correct professional terminology. "
        "You may reason across engineering and construction disciplines, MEP, architecture, project management, "
        "commercial/contracts, procurement, cost, finance, operations, IT/software, sales/business, HR and other "
        "ordinary professional domains. Do not pretend to hold a professional license, certification, legal authority, "
        "or project-specific knowledge you do not have. Separate reliable general knowledge from project facts. "
        "For regulated/high-stakes matters or unsupported project facts, state the limitation and ask for the necessary "
        "document, fact, specialist confirmation, or owner decision. Professional scope selection: " + selected + "."
    )

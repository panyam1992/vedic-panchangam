"""
Indic Transliteration Service powered by Aksharamukha Engine.
Supports script conversion across all major Indian languages:
- Telugu (తెలుగు) - Default Source
- Devanagari (हिन्दी / संस्कृत / मराठी)
- Tamil (தமிழ்)
- Kannada (ಕನ್ನಡ)
- Malayalam (മലയാളം)
- Bengali (বাংলা)
- Gujarati (ગુજરાતી)
- Oriya (ଓଡ଼ିଆ)
- Gurmukhi (ਪੰਜਾਬੀ)
- Assamese (অসমীয়া)
- IAST (English Romanization with Diacritics)
"""

from typing import Dict, Any, List, Union
from functools import lru_cache
from aksharamukha import transliterate

SUPPORTED_SCRIPTS = [
    {
        "id": "Telugu",
        "code": "te",
        "name_native": "తెలుగు",
        "name_en": "Telugu",
        "font_family": "'Noto Sans Telugu', 'Noto Serif Telugu', sans-serif"
    },
    {
        "id": "Devanagari",
        "code": "hi",
        "name_native": "हिन्दी / संस्कृत",
        "name_en": "Hindi / Sanskrit",
        "font_family": "'Noto Sans Devanagari', 'Noto Serif Devanagari', sans-serif"
    },
    {
        "id": "Tamil",
        "code": "ta",
        "name_native": "தமிழ்",
        "name_en": "Tamil",
        "font_family": "'Noto Sans Tamil', sans-serif"
    },
    {
        "id": "Kannada",
        "code": "kn",
        "name_native": "ಕನ್ನಡ",
        "name_en": "Kannada",
        "font_family": "'Noto Sans Kannada', sans-serif"
    },
    {
        "id": "Malayalam",
        "code": "ml",
        "name_native": "മലയാളം",
        "name_en": "Malayalam",
        "font_family": "'Noto Sans Malayalam', sans-serif"
    },
    {
        "id": "Bengali",
        "code": "bn",
        "name_native": "বাংলা",
        "name_en": "Bengali",
        "font_family": "'Noto Sans Bengali', sans-serif"
    },
    {
        "id": "Gujarati",
        "code": "gu",
        "name_native": "ગુજરાતી",
        "name_en": "Gujarati",
        "font_family": "'Noto Sans Gujarati', sans-serif"
    },
    {
        "id": "Oriya",
        "code": "or",
        "name_native": "ଓଡ଼ିଆ",
        "name_en": "Odia",
        "font_family": "'Noto Sans Oriya', sans-serif"
    },
    {
        "id": "Gurmukhi",
        "code": "pa",
        "name_native": "ਪੰਜਾਬੀ",
        "name_en": "Punjabi",
        "font_family": "'Noto Sans Gurmukhi', sans-serif"
    },
    {
        "id": "IAST",
        "code": "en",
        "name_native": "English (IAST)",
        "name_en": "Romanized Sanskrit",
        "font_family": "'Cinzel', 'Segoe UI', serif"
    }
]

SCRIPT_MAP = {s["id"].lower(): s["id"] for s in SUPPORTED_SCRIPTS}
SCRIPT_MAP.update({s["code"].lower(): s["id"] for s in SUPPORTED_SCRIPTS})
SCRIPT_MAP["hindi"] = "Devanagari"
SCRIPT_MAP["sanskrit"] = "Devanagari"
SCRIPT_MAP["marathi"] = "Devanagari"
SCRIPT_MAP["odia"] = "Oriya"
SCRIPT_MAP["punjabi"] = "Gurmukhi"


def normalize_script_name(script: str) -> str:
    """Normalizes input script code or name to Aksharamukha identifier."""
    if not script:
        return "Telugu"
    norm = script.strip().lower()
    return SCRIPT_MAP.get(norm, "Telugu")


@lru_cache(maxsize=16384)
def transliterate_text(text: str, target_script: str, source_script: str = "Telugu") -> str:
    """
    Transliterate a string from source_script to target_script using Aksharamukha.
    Results are cached via LRU for sub-millisecond execution.
    """
    if not text or not isinstance(text, str):
        return text

    tgt = normalize_script_name(target_script)
    src = normalize_script_name(source_script)

    if tgt == src:
        return text

    try:
        # nativize=True ensures natural script conventions
        res = transliterate.process(src, tgt, text, nativize=True)
        return res if res is not None else text
    except Exception as e:
        # Fallback to original text in case of conversion failure
        return text


def transliterate_data(data: Any, target_script: str, source_script: str = "Telugu") -> Any:
    """
    Recursively transliterate nested structures (dictionaries, lists, strings)
    into the target Indian script.
    """
    tgt = normalize_script_name(target_script)
    src = normalize_script_name(source_script)
    if tgt == src:
        return data

    if isinstance(data, str):
        return transliterate_text(data, tgt, src)
    elif isinstance(data, dict):
        new_dict = {}
        for k, v in data.items():
            # If key ends with '_te' or is text content, convert value
            new_dict[k] = transliterate_data(v, tgt, src)
        return new_dict
    elif isinstance(data, list):
        return [transliterate_data(item, tgt, src) for item in data]
    elif isinstance(data, tuple):
        return tuple(transliterate_data(item, tgt, src) for item in data)
    else:
        return data


def get_supported_languages() -> List[Dict[str, Any]]:
    """Return list of supported Indian languages with metadata."""
    return SUPPORTED_SCRIPTS

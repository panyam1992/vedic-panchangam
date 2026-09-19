"""
Localization service providing high-accuracy script transliteration and 
multilingual dictionary support for all major Indian languages.
"""

import re
from indic_transliteration import sanscript

SCRIPT_MAP = {
    "telugu": sanscript.TELUGU,
    "devanagari": sanscript.DEVANAGARI,
    "hindi": sanscript.DEVANAGARI,
    "sanskrit": sanscript.DEVANAGARI,
    "marathi": sanscript.DEVANAGARI,
    "tamil": sanscript.TAMIL,
    "kannada": sanscript.KANNADA,
    "malayalam": sanscript.MALAYALAM,
    "gujarati": sanscript.GUJARATI,
    "bengali": sanscript.BENGALI,
    "bangla": sanscript.BENGALI,
    "assamese": sanscript.BENGALI,
    "oriya": sanscript.ORIYA,
    "odia": sanscript.ORIYA,
    "gurmukhi": sanscript.GURMUKHI,
    "punjabi": sanscript.GURMUKHI,
    "english": sanscript.IAST,
    "iast": sanscript.IAST
}

DEVANAGARI_REGEX = re.compile(r'[\u0900-\u097F\u200B-\u200D]+')

# Classical Vedic Vasaram names across languages
WEEKDAYS = {
    0: {
        "telugu": "భాను వాసరం (రవి వాసరం)",
        "devanagari": "भानु वासर ( रवि वासर )",
        "tamil": "பானு வாசரம் (ரவி வாசரம்)",
        "kannada": "ಭಾನು ವಾಸರ (ರವಿ ವಾಸರ)",
        "malayalam": "ഭാനു വാസരം (രവി വാസരം)",
        "gujarati": "ભાનુ વાસર (રવિ વાસર)",
        "bengali": "ভানু বাসর (রবি বাসর)",
        "oriya": "ଭାନୁ ବାସର (ରବି ବାସର)",
        "gurmukhi": "ਭਾਨੁ ਵਾਸਰ (ਰਵੀ ਵਾਸਰ)",
        "english": "Bhanu vasaram ( Ravi vasaram )",
        "iast": "Bhānu Vāsaram ( Ravi Vāsaram )"
    },
    1: {
        "telugu": "ఇందు వాసరం (సోమ వాసరం)",
        "devanagari": "इन्दु वासर ( सोम वासर )",
        "tamil": "இந்து வாசரம் (சோம வாசரம்)",
        "kannada": "ಇಂದು ವಾಸರ (ಸೋಮ ವಾಸರ)",
        "malayalam": "ഇന്ദു വാസരം (സോമ വാസരം)",
        "gujarati": "ઇન્દુ વાસર (સોમ વાસર)",
        "bengali": "ইন্দু বাসর (সোম বাসর)",
        "oriya": "ଇନ୍ଦୁ ବାସର (ସୋମ ବାସର)",
        "gurmukhi": "ਇੰਦੁ ਵਾਸਰ (ਸੋਮ ਵਾਸਰ)",
        "english": "Indu vasaram ( Soma vasaram )",
        "iast": "Indu Vāsaram ( Soma Vāsaram )"
    },
    2: {
        "telugu": "భౌమ వాసరం (మంగళ వాసరం)",
        "devanagari": "भौम वासर ( मङ्गल वासर )",
        "tamil": "பௌம வாசரம் (மங்கள வாசரம்)",
        "kannada": "ಭೌಮ ವಾಸರ (ಮಂಗಳ ವಾಸರ)",
        "malayalam": "ഭൗമ വാസരം (മംഗള വാസരം)",
        "gujarati": "ભૌમ વાસર (મંગળ વાસર)",
        "bengali": "ভৌমু বাসর (মঙ্গল বাসর)",
        "oriya": "ଭୌମ ବାସର (ମଙ୍ଗଳ ବାସର)",
        "gurmukhi": "ਭੌਮ ਵਾਸਰ (ਮੰਗਲ ਵਾਸਰ)",
        "english": "Bhouma vasaram ( Mangala vasaram )",
        "iast": "Bhauma Vāsaram ( Maṅgala Vāsaram )"
    },
    3: {
        "telugu": "సౌమ్య వాసరం (బుధ వాసరం)",
        "devanagari": "सौम्य वासर ( बुध वासर )",
        "tamil": "சௌமிய வாசரம் (புத வாசரம்)",
        "kannada": "ಸೌಮ್ಯ ವಾಸರ (ಬುಧ ವಾಸರ)",
        "malayalam": "സൗമ്യ വാസരം (ബുധ വാസരം)",
        "gujarati": "સૌમ્ય વાસર (બુધ વાસર)",
        "bengali": "সৌম্য বাসর (বুধ বাসর)",
        "oriya": "ସୌମ୍ୟ ବାସର (ବୁଧ ବାସର)",
        "gurmukhi": "ਸੌਮ੍ਯ ਵਾਸਰ (ਬੁੱਧ ਵਾਸਰ)",
        "english": "Soumya vasaram ( Budha vasaram )",
        "iast": "Saumya Vāsaram ( Budha Vāsaram )"
    },
    4: {
        "telugu": "బృహస్పతి వాసరం (గురు వాసరం)",
        "devanagari": "बृहस्पति वासर ( गुरु वासर )",
        "tamil": "பிருஹஸ்பதி வாசரம் (குரு வாசரம்)",
        "kannada": "ಬೃಹಸ್ಪತಿ ವಾಸರ (ಗುರು ವಾಸರ)",
        "malayalam": "ബൃഹസ്പതി വാസരം (ഗുരു വാസരം)",
        "gujarati": "બૃહસ્પતિ વાસર (ગુરુ વાસર)",
        "bengali": "বৃহস্পতি বাসর (গুরু বাসর)",
        "oriya": "ବୃହସ୍ପତି ବାସର (ଗୁରୁ ବାସର)",
        "gurmukhi": "ਬ੍ਰਿਹਸਪਤੀ ਵਾਸਰ (ਗੁਰੂ ਵਾਸਰ)",
        "english": "Bruhaspati vasaram ( Guru vasaram )",
        "iast": "Bṛhaspati Vāsaram ( Guru Vāsaram )"
    },
    5: {
        "telugu": "భృగు వాసరం (శుక్ర వాసరం)",
        "devanagari": "भृगु वासर ( शुक्र वासर )",
        "tamil": "பிருகு வாசரம் (சுக்ர வாசரம்)",
        "kannada": "ಭೃಗು ವಾಸರ (ಶುಕ್ರ ವಾಸರ)",
        "malayalam": "ഭൃഗു വാസരം (ശുക്ര വാസരം)",
        "gujarati": "ભૃગુ વાસર (શુક્ર વાસર)",
        "bengali": "ভৃগু বাসর (শুক্র বাসর)",
        "oriya": "ଭୃଗୁ ବାସର (ଶୁକ୍ର ବାସର)",
        "gurmukhi": "ਭ੍ਰਿਗੂ ਵਾਸਰ (ਸ਼ੁੱਕਰ ਵਾਸਰ)",
        "english": "Bhrugu vasaram ( Sukra vasaram )",
        "iast": "Bhṛgu Vāsaram ( Śukra Vāsaram )"
    },
    6: {
        "telugu": "స్థిర వాసరం (శని వాసరం)",
        "devanagari": "स्थिर वासर ( शनि वासर )",
        "tamil": "ஸ்திர வாசரம் (சனி வாசரம்)",
        "kannada": "ಸ್ಥಿರ ವಾಸರ (ಶನಿ ವಾಸರ)",
        "malayalam": "സ്ഥിര വാസരം (ശനി വാസരം)",
        "gujarati": "સ્થિર વાસર (શનિ વાસર)",
        "bengali": "স্থির বাসর (শনি বাসর)",
        "oriya": "ସ୍ଥିର ବାସର (ଶନି ବାସର)",
        "gurmukhi": "ਸਥਿਰ ਵਾਸਰ (ਸ਼ਨਿੱਚਰ ਵਾਸਰ)",
        "english": "Sthira vasaram ( Shani vasaram )",
        "iast": "Sthira Vāsaram ( Śani Vāsaram )"
    }
}

VEDIC_VARA_SANKALPA_STEMS = {
    0: "भानु",
    1: "इन्दु",
    2: "भौम",
    3: "सौम्य",
    4: "बृहस्पति",
    5: "भृगु",
    6: "स्थिर"
}


def get_sankalpa_weekday_stem(weekday_idx: int) -> str:
    """Return authentic classical Sanskrit deity stem for Sankalpa (e.g. भानु, इन्दु, भौम, सौम्य, बृहस्पति, भृगु, स्थिर)."""
    return VEDIC_VARA_SANKALPA_STEMS.get(weekday_idx % 7, "भानु")


PAKSHA_NAMES = {
    "shukla": {
        "telugu": "శుక్ల పక్షము",
        "devanagari": "शुक्ल पक्ष",
        "tamil": "சுக்ல பக்ஷம்",
        "kannada": "ಶುಕ್ಲ ಪಕ್ಷ",
        "malayalam": "ശുക്ല പക്ഷം",
        "gujarati": "શુક્લ પક્ષ",
        "bengali": "শুক্ল পক্ষ",
        "oriya": "ଶୁକ୍ଲ ପକ୍ଷ",
        "gurmukhi": "ਸ਼ੁਕਲ ਪੱਖ",
        "english": "Shukla Paksha (Waxing Moon)",
        "iast": "Śukla Pakṣa"
    },
    "krishna": {
        "telugu": "కృష్ణ పక్షము",
        "devanagari": "कृष्ण पक्ष",
        "tamil": "கிருஷ்ண பக்ஷம்",
        "kannada": "ಕೃಷ್ಣ ಪಕ್ಷ",
        "malayalam": "കൃഷ്ണ പക്ഷം",
        "gujarati": "કૃષ્ણ પક્ષ",
        "bengali": "কৃষ্ণ পক্ষ",
        "oriya": "କୃଷ୍ଣ ପକ୍ଷ",
        "gurmukhi": "ਕ੍ਰਿਸ਼ਨ ਪੱਖ",
        "english": "Krishna Paksha (Waning Moon)",
        "iast": "Kṛṣṇa Pakṣa"
    }
}

AYANA_NAMES = {
    1: {  # Uttarayanam
        "telugu": "ఉత్తరాయణము",
        "devanagari": "उत्तरायण",
        "tamil": "உத்தராயணம்",
        "kannada": "ಉತ್ತರಾಯಣ",
        "malayalam": "ഉത്തരായനം",
        "gujarati": "ઉત્તરાયણ",
        "bengali": "উত্তরায়ণ",
        "oriya": "ଉତ୍ତରାୟଣ",
        "gurmukhi": "ਉੱਤਰਾਯਣ",
        "english": "Uttarayana (Northward Sun)",
        "iast": "Uttarāyaṇa"
    },
    2: {  # Dakshinayanam
        "telugu": "దక్షిణాయనము",
        "devanagari": "दक्षिणायन",
        "tamil": "தக்ஷிணாயனம்",
        "kannada": "ದಕ್ಷಿಣಾಯನ",
        "malayalam": "ദക്ഷിണായനം",
        "gujarati": "દક્ષિણાયન",
        "bengali": "দক্ষিণায়ন",
        "oriya": "ଦକ୍ଷିଣାୟଣ",
        "gurmukhi": "ਦੱਖਣਾਯਣ",
        "english": "Dakshinayana (Southward Sun)",
        "iast": "Dakṣiṇāyana"
    }
}

RITU_NAMES = {
    1: {  # Vasanta
        "telugu": "వసంత ఋతువు",
        "devanagari": "वसन्त ऋतु",
        "tamil": "வசந்த ருது",
        "kannada": "ವಸಂತ ಋತು",
        "malayalam": "വസന്ത ഋതു",
        "gujarati": "વસંત ઋતુ",
        "bengali": "বসন্ত ঋতু",
        "oriya": "ବସନ୍ତ ଋତୁ",
        "gurmukhi": "ਬਸੰਤ ਰੁੱਤ",
        "english": "Vasanta Ritu (Spring)",
        "iast": "Vasanta Ṛtu"
    },
    2: {  # Grishma
        "telugu": "గ్రీష్మ ఋతువు",
        "devanagari": "ग्रीष्म ऋतु",
        "tamil": "கிரீஷ்ம ருது",
        "kannada": "ಗ್ರೀಷ್ಮ ಋತು",
        "malayalam": "ഗ്രീഷ്മ ഋതു",
        "gujarati": "ગ્રીષ્મ ઋતુ",
        "bengali": "গ্রীষ্ম ঋতু",
        "oriya": "ଗ୍ରୀଷ୍ମ ଋତୁ",
        "gurmukhi": "ਗਰੀਸ਼ਮ ਰੁੱਤ",
        "english": "Grishma Ritu (Summer)",
        "iast": "Grīṣma Ṛtu"
    },
    3: {  # Varsha
        "telugu": "వర్ష ఋతువు",
        "devanagari": "वर्षा ऋतु",
        "tamil": "வர்ஷ ருது",
        "kannada": "ವರ್ಷ ಋತು",
        "malayalam": "വർഷ ഋതു",
        "gujarati": "વર્ષા ઋતુ",
        "bengali": "বর্ষা ঋতু",
        "oriya": "ବର୍ଷା ଋତୁ",
        "gurmukhi": "ਵਰਖਾ ਰੁੱਤ",
        "english": "Varsha Ritu (Monsoon)",
        "iast": "Varṣā Ṛtu"
    },
    4: {  # Sharad
        "telugu": "శరదృతువు",
        "devanagari": "शरद् ऋतु",
        "tamil": "சரத் ருது",
        "kannada": "ಶರದ್ ಋತು",
        "malayalam": "ശരദ് ഋതു",
        "gujarati": "શરદ ઋતુ",
        "bengali": "শরৎ ঋতু",
        "oriya": "ଶରତ ଋତୁ",
        "gurmukhi": "ਸ਼ਰਦ ਰੁੱਤ",
        "english": "Sharad Ritu (Autumn)",
        "iast": "Śarad Ṛtu"
    },
    5: {  # Hemanta
        "telugu": "హేమంత ఋతువు",
        "devanagari": "हेमन्त ऋतु",
        "tamil": "ஹேமந்த ருது",
        "kannada": "ಹೇಮಂತ ಋತು",
        "malayalam": "ഹേമന്ത ഋതു",
        "gujarati": "હેમંત ઋતુ",
        "bengali": "হেমন্ত ঋতু",
        "oriya": "ହେମନ୍ତ ଋତୁ",
        "gurmukhi": "ਹੇਮੰਤ ਰੁੱਤ",
        "english": "Hemanta Ritu (Pre-Winter)",
        "iast": "Hemanta Ṛtu"
    },
    6: {  # Shishira
        "telugu": "శిశిర ఋతువు",
        "devanagari": "शिशिर ऋतु",
        "tamil": "சிசிர ருது",
        "kannada": "ಶಿಶಿರ ಋತು",
        "malayalam": "ശിശിര ഋതു",
        "gujarati": "શિશિર ઋતુ",
        "bengali": "শিশির ঋতু",
        "oriya": "ଶିଶିର ଋତୁ",
        "gurmukhi": "ਸ਼ਿਸ਼ਿਰ ਰੁੱਤ",
        "english": "Shishira Ritu (Winter)",
        "iast": "Śiśira Ṛtu"
    }
}

MOON_PHASE_NAMES = {
    "new_moon": {
        "telugu": "అమావాస్య (New Moon)",
        "devanagari": "अमावास्या (New Moon)",
        "tamil": "அமாவாசை (New Moon)",
        "kannada": "ಅಮಾವಾಸ್ಯೆ (New Moon)",
        "english": "New Moon (Amavasya)"
    },
    "waxing_crescent": {
        "telugu": "శుక్ల పక్ష బాల చంద్రుడు (Waxing Crescent)",
        "devanagari": "शुक्ल पक्ष बाल चन्द्र (Waxing Crescent)",
        "tamil": "வளர்பிறை பிறை (Waxing Crescent)",
        "kannada": "ಶುಕ್ಲ ಪಕ್ಷ ಬಾಲ ಚಂದ್ರ (Waxing Crescent)",
        "english": "Waxing Crescent"
    },
    "first_quarter": {
        "telugu": "శుక్ల పక్ష అర్ధ చంద్రుడు (First Quarter)",
        "devanagari": "शुक्ल पक्ष अर्ध चन्द्र (First Quarter)",
        "tamil": "வளர்பிறை அரை நிலவு (First Quarter)",
        "kannada": "ಶುಕ್ಲ ಪಕ್ಷ ಅರ್ಧ ಚಂದ್ರ (First Quarter)",
        "english": "First Quarter"
    },
    "waxing_gibbous": {
        "telugu": "శుక్ల పక్ష కుంభ చంద్రుడు (Waxing Gibbous)",
        "devanagari": "शुक्ल पक्ष कुम्भ चन्द्र (Waxing Gibbous)",
        "tamil": "வளர்பிறை முக்கால் நிலவு (Waxing Gibbous)",
        "kannada": "ಶುಕ್ಲ ಪಕ್ಷ ಕುಂಭ ಚಂದ್ರ (Waxing Gibbous)",
        "english": "Waxing Gibbous"
    },
    "full_moon": {
        "telugu": "పూర్ణిమ (Full Moon)",
        "devanagari": "पूर्णिमा (Full Moon)",
        "tamil": "பௌர்ணமி (Full Moon)",
        "kannada": "ಹುಣ್ಣಿಮೆ (Full Moon)",
        "english": "Full Moon (Purnima)"
    },
    "waning_gibbous": {
        "telugu": "కృష్ణ పక్ష కుంభ చంద్రుడు (Waning Gibbous)",
        "devanagari": "कृष्ण पक्ष कुम्भ चन्द्र (Waning Gibbous)",
        "tamil": "தேய்பிறை முக்கால் நிலவு (Waning Gibbous)",
        "kannada": "ಕೃಷ್ಣ ಪಕ್ಷ ಕುಂಭ ಚಂದ್ರ (Waning Gibbous)",
        "english": "Waning Gibbous"
    },
    "third_quarter": {
        "telugu": "కృష్ణ పక్ష అర్ధ చంద్రుడు (Third Quarter)",
        "devanagari": "कृष्ण पक्ष अर्ध चन्द्र (Third Quarter)",
        "tamil": "தேய்பிறை அரை நிலவு (Third Quarter)",
        "kannada": "ಕೃಷ್ಣ ಪಕ್ಷ ಅರ್ಧ ಚಂದ್ರ (Third Quarter)",
        "english": "Third Quarter"
    },
    "waning_crescent": {
        "telugu": "కృష్ణ పక్ష బాల చంద్రుడు (Waning Crescent)",
        "devanagari": "कृष्ण पक्ष बाल चन्द्र (Waning Crescent)",
        "tamil": "தேய்பிறை பிறை (Waning Crescent)",
        "kannada": "ಕೃಷ್ಣ ಪಕ್ಷ ಬಾಲ ಚಂದ್ರ (Waning Crescent)",
        "english": "Waning Crescent"
    }
}


def get_moon_phase_name(phase_key: str, lang: str) -> str:
    """Return localized moon phase name."""
    target = (lang or "telugu").lower().strip()
    p_dict = MOON_PHASE_NAMES.get(phase_key, MOON_PHASE_NAMES["new_moon"])
    return p_dict.get(target, p_dict.get("english", "New Moon"))



def get_target_script(lang: str) -> str:
    """Normalize user requested language to a sanscript target script code."""
    cleaned = (lang or "telugu").lower().strip()
    return SCRIPT_MAP.get(cleaned, sanscript.TELUGU)


def transliterate_text(text: str, target_lang: str, source_script=sanscript.DEVANAGARI) -> str:
    """Transliterate text to the desired Indian language script."""
    if not text:
        return ""
    target_script = get_target_script(target_lang)
    if target_script == source_script:
        return text
    try:
        return sanscript.transliterate(text, source_script, target_script)
    except Exception:
        return text


def get_weekday_name(weekday_idx: int, lang: str) -> str:
    """Return localized weekday name (0=Sunday to 6=Saturday)."""
    target = (lang or "telugu").lower().strip()
    day_dict = WEEKDAYS.get(weekday_idx % 7, WEEKDAYS[0])
    return day_dict.get(target, day_dict.get("telugu", "ఆదివారం"))


def get_paksha_name(tithi_num: int, lang: str) -> str:
    """Determine Shukla/Krishna paksha from tithi (1-15: Shukla, 16-30: Krishna)."""
    target = (lang or "telugu").lower().strip()
    key = "shukla" if tithi_num <= 15 else "krishna"
    p_dict = PAKSHA_NAMES[key]
    return p_dict.get(target, p_dict.get("telugu", "శుక్ల పక్షము"))


def get_ayana_name(month_solar: int, lang: str) -> str:
    """Determine Uttarayana / Dakshinayana from solar month (10-3 = Makara-Mithuna: Uttarayana, else Dakshinayana)."""
    target = (lang or "telugu").lower().strip()
    # Solar month 10 (Makara) through 3 (Mithuna) is Uttarayana
    # 4 (Karkataka) through 9 (Dhanu) is Dakshinayana
    is_uttarayana = month_solar in [10, 11, 12, 1, 2, 3]
    a_dict = AYANA_NAMES[1 if is_uttarayana else 2]
    return a_dict.get(target, a_dict.get("telugu", "ఉత్తరాయణము"))


def get_ritu_name(month_num: int, lang: str) -> str:
    """Determine Ritu based on 2-month cycle."""
    target = (lang or "telugu").lower().strip()
    # Chaitra-Vaishakha: 1 (Vasanta), Jyeshtha-Ashadha: 2 (Grishma), etc.
    ritu_idx = int((((month_num - 1) % 12) // 2) + 1)
    r_dict = RITU_NAMES.get(ritu_idx, RITU_NAMES[1])
    return r_dict.get(target, r_dict.get("telugu", "వసంత ఋతువు"))


def format_samvatsara_display(sam_name: str, lang: str) -> str:
    """Format full ceremonial Samvatsara title (e.g. 'శ్రీ పరాభవ నామ సంవత్సరం')."""
    target = (lang or "telugu").lower().strip()
    clean = sam_name.replace("ః", "").replace(":", "").strip()
    if target == "telugu":
        if "సంవత్సర" in clean:
            return clean
        if not clean.startswith("శ్రీ"):
            clean = f"శ్రీ {clean}"
        return f"{clean} నామ సంవత్సరం"
    elif target == "devanagari":
        if "संवत्सर" in clean:
            return clean
        if not clean.startswith("श्री"):
            clean = f"श्री {clean}"
        return f"{clean} नाम संवत्सर"
    elif target == "kannada":
        if "ಸಂವತ್ಸರ" in clean:
            return clean
        if not clean.startswith("ಶ್ರೀ"):
            clean = f"ಶ್ರೀ {clean}"
        return f"{clean} ನಾಮ ಸಂವತ್ಸರ"
    elif target == "tamil":
        if "வருடம்" in clean:
            return clean
        if not clean.startswith("ஸ்ரீ"):
            clean = f"ஸ்ரீ {clean}"
        return f"{clean} நாம வருடம்"
    elif target == "english":
        if "samvatsara" in clean.lower():
            return clean
        if not clean.lower().startswith("sri"):
            clean = f"Sri {clean}"
        return f"{clean} Nama Samvatsara"
    else:
        return f"{clean} Samvatsara"


def format_masa_display(masa_name: str, lang: str) -> str:
    """Format traditional Masa title (e.g. 'చైత్ర మాసము')."""
    target = (lang or "telugu").lower().strip()
    clean = masa_name.replace("ః", "").replace(":", "").strip()
    if target == "telugu":
        if "మాస" in clean:
            return clean
        return f"{clean} మాసము"
    elif target == "devanagari":
        if "मास" in clean:
            return clean
        return f"{clean} मास"
    elif target == "kannada":
        if "ಮಾಸ" in clean:
            return clean
        return f"{clean} ಮಾಸ"
    elif target == "tamil":
        if "மாதம்" in clean:
            return clean
        return f"{clean} மாதம்"
    elif target == "english":
        if "masa" in clean.lower() or "month" in clean.lower():
            return clean
        return f"{clean} Masa"
    else:
        return f"{clean} Masa"



# Standardized 12 Rashi / Lagna names across languages
RASHI_NAMES = {
    1: {"telugu": "మేష లగ్నం", "devanagari": "मेष लग्न", "english": "Mesha (Aries)"},
    2: {"telugu": "వృషభ లగ్నం", "devanagari": "वृषभ लग्न", "english": "Vrishabha (Taurus)"},
    3: {"telugu": "మిథున లగ్నం", "devanagari": "मिथुन लग्न", "english": "Mithuna (Gemini)"},
    4: {"telugu": "కర్కాటక లగ్నం", "devanagari": "कर्क लग्न", "english": "Karka (Cancer)"},
    5: {"telugu": "సింహ లగ్నం", "devanagari": "सिंह लग्न", "english": "Simha (Leo)"},
    6: {"telugu": "కన్యా లగ్నం", "devanagari": "कन्या लग्न", "english": "Kanya (Virgo)"},
    7: {"telugu": "తులా లగ్నం", "devanagari": "तुला लग्न", "english": "Tula (Libra)"},
    8: {"telugu": "వృశ్చిక లగ్నం", "devanagari": "वृश्चिक लग्न", "english": "Vrischika (Scorpio)"},
    9: {"telugu": "ధనుస్సు లగ్నం", "devanagari": "धनु लग्न", "english": "Dhanu (Sagittarius)"},
    10: {"telugu": "మకర లగ్నం", "devanagari": "मकर लग्न", "english": "Makara (Capricorn)"},
    11: {"telugu": "కుంభ లగ్నం", "devanagari": "कुम्भ लग्न", "english": "Kumbha (Aquarius)"},
    12: {"telugu": "మీన లగ్నం", "devanagari": "मीन लग्न", "english": "Meena (Pisces)"},
}


def get_lagna_display_name(lagna_id: int, lang: str) -> str:
    """Return culturally accurate, localized Lagna display name."""
    target = (lang or "telugu").lower().strip()
    r_dict = RASHI_NAMES.get(lagna_id, RASHI_NAMES[1])
    if target in r_dict:
        return r_dict[target]
    # For other languages (tamil, kannada, etc.), transliterate from Devanagari
    dev_name = r_dict["devanagari"]
    return transliterate_text(dev_name, target, source_script=sanscript.DEVANAGARI)


# Curated cultural and linguistic localizations for Tamil solar/weekday and regional festivals
REGIONAL_FESTIVAL_NAMES = {
    "puraTTAci~can2ikkizhamai": {
        "telugu": "పురట్టాసి శనివారం (శ్రీ వేంకటేశ్వర స్వామి విశేష పూజ)",
        "devanagari": "पुरट्टासी शनिवार (श्री वेंकटेश्वर स्वामी विशेष पूजा)",
        "tamil": "புரட்டாசி சனிக்கிழமை",
        "kannada": "ಪುರಟ್ಟಾಸಿ ಶನಿವಾರ (ಶ್ರೀ ವೆಂಕಟೇಶ್ವರ ಸ್ವಾಮಿ ವಿಶೇಷ ಪೂಜೆ)",
        "malayalam": "പുരട്ടാസി ശനിയാഴ്ച (ശ്രീ വെങ്കടേശ്വര സ്വാമി പൂജ)",
        "gujarati": "પુરટ્ટાસી શનિવાર (શ્રી વેંકટેશ્વર સ્વામી વિશેષ પૂજા)",
        "bengali": "পুরট্টাসী শনিবার (শ্রী ভেঙ্কটেশ্বর স্বামী বিশেষ পূজা)",
        "oriya": "ପୁରଟ୍ଟାସୀ ଶନିବାର (ଶ୍ରୀ ବେଙ୍କଟେଶ୍ୱର ସ୍ୱାମୀ ପୂଜା)",
        "gurmukhi": "ਪੁਰੱਟਾਸੀ ਸ਼ਨਿੱਚਰਵਾਰ",
        "english": "Purattasi Saturday (Sri Venkateswara Swamy Puja)",
        "iast": "Puraṭṭāsi Śanivāram"
    },
    "ADi~veLLikkizhamai": {
        "telugu": "ఆడి శుక్రవారం (అమ్మవారి విశేష పూజ)",
        "devanagari": "आडि शुक्रवार (अम्मन विशेष पूजा)",
        "tamil": "ஆடி வெள்ளிக்கிழமை",
        "kannada": "ಆಡಿ ಶುಕ್ರವಾರ (ಅಮ್ಮನವರ ವಿಶೇಷ ಪೂಜೆ)",
        "malayalam": "ആടി വെള്ളിയാഴ്ച",
        "english": "Aadi Friday (Amman Special Puja)"
    },
    "AvaNi~JAyir2r2ukkizhamai": {
        "telugu": "ఆవణి ఆదివారం (సూర్య పూజ)",
        "devanagari": "आवणि रविवार (सूर्य पूजा)",
        "tamil": "ஆவணி ஞாயிற்றுக்கிழமை",
        "kannada": "ಆವಣಿ ಭಾನುವಾರ (ಸೂರ್ಯ ಪೂಜೆ)",
        "malayalam": "ആവണി ഞായറാഴ്ച",
        "english": "Avani Sunday (Surya Puja)"
    },
    "kArttigai~JAyir2r2ukkizhamai": {
        "telugu": "కార్తిక ఆదివారం (సూర్య పూజ)",
        "devanagari": "कार्त्तिकै रविवार (सूर्य पूजा)",
        "tamil": "கார்த்திகை ஞாயிற்றுக்கிழமை",
        "kannada": "ಕಾರ್ತಿಕ ಭಾನುವಾರ (ಸೂರ್ಯ ಪೂಜೆ)",
        "malayalam": "കാർത്തിക ഞായറാഴ്ച",
        "english": "Karthigai Sunday (Surya Puja)"
    },
    "tai~veLLikkizhamai": {
        "telugu": "తై శుక్రవారం (అమ్మవారి విశేష పూజ)",
        "devanagari": "तै शुक्रवार (अम्मन विशेष पूजा)",
        "tamil": "தை வெள்ளிக்கிழமை",
        "kannada": "ತೈ ಶುಕ್ರವಾರ",
        "malayalam": "തൈ വെള്ളിയാഴ്ച",
        "english": "Tai Friday (Amman Special Puja)"
    },
    "mAci~cevvAy": {
        "telugu": "మాసి మంగళవారం (అమ్మవారి విశేష పూజ)",
        "devanagari": "मासि मंगलवार (अम्मन विशेष पूजा)",
        "tamil": "மாசி செவ்வாய்",
        "kannada": "ಮಾಸಿ ಮಂಗಳವಾರ",
        "malayalam": "മാസി ചൊവ്വാഴ്ച",
        "english": "Masi Tuesday (Amman Special Puja)"
    },
    "kAraDaiyAn2_nOn2bu": {
        "telugu": "కారడైయాన్ నోంబు (సావిత్రీ వ్రతం)",
        "devanagari": "कारडैयान नोन्बु (सावित्री व्रत)",
        "tamil": "காரடையான் நோன்பு",
        "kannada": "ಕಾರಡೈಯಾನ್ ನೋಂಬು (ಸಾವಿತ್ರಿ ವ್ರತ)",
        "malayalam": "കാരടയാൻ നോമ്പ്",
        "english": "Karadaiyan Nombu (Savitri Vratam)"
    },
    "muDavan2_muzhukku": {
        "telugu": "ముడవన్ ముళుక్కు (తులా కావేరీ స్నానం)",
        "devanagari": "मुडवन मुऴुक्कु (कावेरी स्नान)",
        "tamil": "முடவன் முழுக்கு",
        "kannada": "ಮುಡವನ್ ಮುಳುಕ್ಕು",
        "malayalam": "മുടവൻ മുഴുകു",
        "english": "Mudavan Muzhukku (Kaveri Bath)"
    },
    "viSukkan2i": {
        "telugu": "విషుక్కణి (విషు పర్వదినం)",
        "devanagari": "विषुक्कणि (विषु पर्व)",
        "tamil": "விஷுக்கனி",
        "kannada": "ವಿಷುಕ್ಕಣಿ",
        "malayalam": "വിഷുക്കണി",
        "english": "Vishu Kani (Vishu Festival)"
    },
    "garbhOTTam-Arambham": {
        "telugu": "గర్భోట్టం ఆరంభం",
        "devanagari": "गर्भोट्टम आरम्भ",
        "tamil": "கர்போட்டம் ஆரம்பம்",
        "kannada": "ಗರ್ಭೋಟ್ಟಂ ಆರಂಭ",
        "english": "Garbhottam Arambham"
    },
    "garbhOTTam-muDivu": {
        "telugu": "గర్భోట్టం ముగింపు",
        "devanagari": "गर्भोट्टम समाप्ति",
        "tamil": "கர்போட்டம் முடிவு",
        "kannada": "ಗರ್ಭೋಟ್ಟಂ ಮುಕ್ತಾಯ",
        "english": "Garbhottam Completion"
    }
}


def transliterate_festival_name(fest_id: str, lang: str) -> str:
    """
    Accurately transliterates Jyotisha festival IDs into natural, elegant Telugu script
    or other selected languages, replacing technical transliteration artifacts (like N2, ఴ, zha)
    with authentic, culturally correct festival names.
    """
    if not fest_id:
        return ""
        
    target_lang = (lang or "telugu").lower().strip()
    
    # 1. Check curated regional festivals mapping
    fest_key = fest_id.strip()
    if fest_key in REGIONAL_FESTIVAL_NAMES:
        item = REGIONAL_FESTIVAL_NAMES[fest_key]
        if target_lang in item:
            return item[target_lang]
        if "telugu" in item:
            return item["telugu"]

    clean = fest_id.replace("~", " ").replace("_", " ")
    
    # Pre-clean phonetic anomalies from Tamil/Dravidian transliteration
    clean = re.sub(r'\bcan2i\b', 'shani', clean, flags=re.IGNORECASE)
    clean = re.sub(r'n2', 'n', clean)
    clean = re.sub(r'r2', 'r', clean)
    
    res = ""
    # 2. Try using Jyotisha's custom_transliteration if available
    try:
        import jyotisha.custom_transliteration as ct
        target_scr = get_target_script(target_lang)
        if target_lang in ["english", "iast"]:
            target_scr = sanscript.ISO
        res = ct.tr(clean, target_scr)
    except Exception:
        pass
        
    # 3. Fallback to sanscript.OPTITRANS
    if not res:
        try:
            target_script = get_target_script(target_lang)
            if target_lang in ["english", "iast"]:
                target_script = sanscript.IAST
            if re.search(r'[a-zA-Z]', clean):
                res = sanscript.transliterate(clean, sanscript.OPTITRANS, target_script)
                if target_lang in ["english", "iast"]:
                    res = res.title()
        except Exception:
            pass
            
    if not res:
        res = clean
        
    # Post-clean: eliminate any residual Dravidian encoding artifacts in Telugu / Devanagari
    if target_lang == "telugu":
        res = res.replace("N2", "న").replace("n2", "న")
        # Replace archaic Unicode Telugu letter LLLA / ZHA (ఴ U+0C34) with modern standard La/Laa (ళ U+0C33)
        res = res.replace("ఴ", "ళ")
        # Clean up stray Latin characters or formatting
        res = re.sub(r'[a-zA-Z]2?', '', res).strip()
    elif target_lang == "devanagari":
        res = res.replace("ऩ", "न").replace("ऴ", "ळ")
        
    return res
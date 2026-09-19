"""
Calculations for the three primary Vedic calendar systems:
1. Chandramana (Lunar Calendar - Amanta & Purnimanta)
2. Sauramana (Solar Sidereal Calendar - Tamil, Malayalam Kollam, Bengali, Odia)
3. Barhaspatyamana (Jovian Calendar - 60-year, 12-year Maha-Masa, Pushkara River)
"""

import math
import swisseph as swe
from jyotisha.panchaanga.temporal import names
from indic_transliteration import sanscript
from services.localization_service import transliterate_text, get_target_script
from services.intercalary_service import get_intercalary_status_for_date

# 12-Year Jovian Maha-Masa names (Mesha = Maha Chaitra, etc.)
MAHA_MASA_NAMES = {
    1: "महा-चैत्र",
    2: "महा-वैशाख",
    3: "महा-ज्येष्ठ",
    4: "महा-आषाढ",
    5: "महा-श्रावण",
    6: "महा-भाद्रपद",
    7: "महा-आश्वयुज",
    8: "महा-कार्तिक",
    9: "महा-मार्गशीर्ष",
    10: "महा-पौष",
    11: "महा-माघ",
    12: "महा-फाल्गुन"
}

# Sacred River Pushkaram governed by Jupiter's Rashi ingress
PUSHKARA_RIVERS = {
    1: {"name_sa": "गङ्गा", "name_te": "గంగా నది పుష్కరాలు", "desc": "Ganga River Pushkaram (Aries / Mesha)"},
    2: {"name_sa": "नर्मदा", "name_te": "నర్మదా నది పుష్కరాలు", "desc": "Narmada River Pushkaram (Taurus / Vrishabha)"},
    3: {"name_sa": "सरस्वती", "name_te": "సరస్వతీ నది పుష్కరాలు", "desc": "Saraswati River Pushkaram (Gemini / Mithuna)"},
    4: {"name_sa": "यमुना", "name_te": "యమునా నది పుష్కరాలు", "desc": "Yamuna River Pushkaram (Cancer / Karkataka)"},
    5: {"name_sa": "गोदावरी", "name_te": "గోదావరి నది పుష్కరాలు", "desc": "Godavari River Pushkaram (Leo / Simha)"},
    6: {"name_sa": "कृष्णा", "name_te": "కృష్ణా నది పుష్కరాలు", "desc": "Krishna River Pushkaram (Virgo / Kanya)"},
    7: {"name_sa": "कावेरी", "name_te": "కావేరీ నది పుష్కరాలు", "desc": "Kaveri River Pushkaram (Libra / Tula)"},
    8: {"name_sa": "भीमा / ताम्रपर्णी", "name_te": "భీమా / తామ్రపర్ణి నది పుష్కరాలు", "desc": "Bhima / Tamraparni River Pushkaram (Scorpio / Vrischika)"},
    9: {"name_sa": "ब्रह्मपुत्रा / पुष्कर", "name_te": "బ్రహ్మపుత్ర / పుష్కర సరస్సు", "desc": "Brahmaputra / Pushkar Lake Pushkaram (Sagittarius / Dhanus)"},
    10: {"name_sa": "तुङ्गभद्रा", "name_te": "తుంగభద్రా నది పుష్కరాలు", "desc": "Tungabhadra River Pushkaram (Capricorn / Makara)"},
    11: {"name_sa": "सिन्धु", "name_te": "సింధు నది పుష్కరాలు", "desc": "Sindhu / Indus River Pushkaram (Aquarius / Kumbha)"},
    12: {"name_sa": "प्राणहिता", "name_te": "ప్రాణహిత నది పుష్కరాలు", "desc": "Pranahita River Pushkaram (Pisces / Meena)"}
}

# Regional Sauramana Month Names
TAMIL_MONTHS = [
    "சித்திரை", "வைகாசி", "ஆனி", "ஆடி", "ஆவணி", "புரட்டாசி",
    "ஐப்பசி", "கார்த்திகை", "மார்கழி", "தை", "மாசி", "பங்குனி"
]

MALAYALAM_MONTHS = [
    "മേടം", "ഇടവം", "മിഥുനം", "കർക്കടകം", "ചിങ്ങം", "കന്നി",
    "തുലാം", "വൃശ്ചികം", "ധനു", "മകരം", "കുംഭം", "മീനം"
]

BENGALI_MONTHS = [
    "বৈশাখ", "জ্যৈষ্ঠ", "আষাঢ়", "শ্রাবণ", "ভাদ্র", "আশ্বিন",
    "কার্তিক", "অগ্রহায়ণ", "পৌষ", "মাঘ", "ফাল্গুন", "চৈত্র"
]

ODIA_MONTHS = [
    "ମେଷ", "ବୃଷ", "ମିଥୁନ", "କର୍କଟ", "ସିଂହ", "କନ୍ୟା",
    "ତୁଳା", "ବିଛା", "ଧନୁ", "ମକର", "କୁମ୍ଭ", "ମୀନ"
]

RASHI_NAMES_DEV = [
    "मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या",
    "तुला", "वृश्चिक", "धनु", "मकर", "कुम्भ", "मीन"
]

NAKSHATRA_NAMES_DEV = [
    "अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशीर्ष", "आर्द्रा",
    "पुनर्वसु", "पुष्य", "आश्लेषा", "मघा", "पूर्वाफाल्गुनी", "उत्तराफाल्गुनी",
    "हस्त", "चित్రా", "स्वाती", "विशाखा", "अनुराधा", "ज्येष्ठा",
    "मूल", "पूर्वाषाढा", "उत्तराषाढा", "श्रवण", "धनिष्ठा", "शतभिषक्",
    "पूर्वप्रोष्ठपदा", "उत्तरप्रोष्ठपदा", "रेवती"
]


def compute_chandramana(daily_panchaanga, target_lang: str) -> dict:
    """
    Computes complete Chandramana (Lunar) details including:
    - Amanta Month
    - Purnimanta Month
    - Samvatsara name (60-year Jovian/Lunar name)
    - Paksha (Shukla/Krishna)
    - Adhika/Nija/Kshaya status
    """
    lunar_date = daily_panchaanga.lunar_date
    m_idx = lunar_date.month.index
    is_adhika = getattr(lunar_date.month, 'is_adhika', False) or (m_idx % 1 != 0)
    month_int = int(math.ceil(m_idx))

    # Amanta month name
    amanta_masa_dev = names.get_chandra_masa(m_idx, sanscript.DEVANAGARI)
    amanta_masa_user = transliterate_text(amanta_masa_dev, target_lang)

    # Purnimanta month name:
    # In Purnimanta, the Krishna paksha (tithi > 15) belongs to the subsequent month
    tithi_num = daily_panchaanga.sunrise_day_angas.tithi_at_sunrise.index
    if tithi_num > 15 and not is_adhika:
        purnimanta_m_int = (month_int % 12) + 1
    else:
        purnimanta_m_int = month_int
    purnimanta_masa_dev = names.get_chandra_masa(purnimanta_m_int, sanscript.DEVANAGARI)
    purnimanta_masa_user = transliterate_text(purnimanta_masa_dev, target_lang)

    # Samvatsara: In Chandramana, Samvatsara starts at Chaitra Shukla Pratipada (lunar month 1).
    # In the early Gregorian months (Jan–May), if the lunar month is still Pushya/Magha/Phalguna (>=9),
    # it belongs to the previous civil year's Samvatsara.
    year = daily_panchaanga.date.year
    if daily_panchaanga.date.month <= 5 and month_int >= 9:
        effective_year = year - 1
    else:
        effective_year = year

    # Offset 1567: 2024 -> 38 (Krodhi), 2025 -> 39 (Vishvavasu), 2026 -> 40 (Parabhava), 2028 -> 42 (Kilaka)
    effective_samvatsara_id = (effective_year - 1567) % 60 + 1

    sam_dev = names.NAMES['SAMVATSARA_NAMES']['sa'][sanscript.DEVANAGARI][effective_samvatsara_id]
    sam_user = transliterate_text(sam_dev, target_lang)

    # Intercalary determination (Kshaya, Samsarpa, Adhika, Nija)
    inter_status = get_intercalary_status_for_date(daily_panchaanga.jd_sunrise, "surya_siddhanta", target_lang)
    classification = inter_status.get("classification", "NIJA")
    is_kshaya = inter_status.get("is_kshaya", False)
    is_samsarpa = inter_status.get("is_samsarpa", False)
    is_adhika = inter_status.get("is_adhika", False) or is_adhika
    sankranti_count = inter_status.get("sankranti_count", 1)
    badge_label = inter_status.get("badge_label", "సాధారణ మాసం")

    if is_kshaya:
        if target_lang == "telugu":
            amanta_masa_user = "యుగళీభూత అంహస్పతి (మార్గశిర–పుష్య క్షయ మాసం)"
        else:
            amanta_masa_user = transliterate_text("युगलीभूत अंहस्पति (मार्गशीर्ष–पौष क्षय मास)", target_lang)
        purnimanta_masa_user = amanta_masa_user
    elif is_samsarpa:
        if target_lang == "telugu":
            amanta_masa_user = "సంసర్ప కార్తిక మాసం"
        else:
            amanta_masa_user = transliterate_text("संसर्प कार्तिक मास", target_lang)
        purnimanta_masa_user = amanta_masa_user

    if target_lang == "telugu":
        paksha_str = "శుక్ల పక్షము" if tithi_num <= 15 else "కృష్ణ పక్షము"
    elif target_lang == "devanagari":
        paksha_str = "शुक्ल पक्ष" if tithi_num <= 15 else "कृष्ण पक्ष"
    else:
        paksha_str = "Shukla" if tithi_num <= 15 else "Krishna"

    return {
        "samvatsara": {
            "id": effective_samvatsara_id,
            "name": sam_user,
            "name_sanskrit": sam_dev
        },
        "amanta_masa": {
            "index": month_int,
            "name": amanta_masa_user,
            "name_sanskrit": amanta_masa_dev,
            "is_adhika": is_adhika,
            "is_kshaya": is_kshaya,
            "is_samsarpa": is_samsarpa,
            "masa_classification": classification,
            "sankranti_count": sankranti_count,
            "badge_label": badge_label
        },
        "purnimanta_masa": {
            "index": purnimanta_m_int,
            "name": purnimanta_masa_user,
            "name_sanskrit": purnimanta_masa_dev,
            "is_adhika": is_adhika,
            "is_kshaya": is_kshaya,
            "is_samsarpa": is_samsarpa,
            "masa_classification": classification,
            "sankranti_count": sankranti_count,
            "badge_label": badge_label
        },
        "paksha": paksha_str,
        "paksha_name": paksha_str,
        "tithi_at_sunrise": tithi_num,
        "description": f"{sam_user} సం|| {amanta_masa_user} {paksha_str}"
    }


def compute_sauramana(daily_panchaanga, target_lang: str) -> dict:
    """
    Computes Sauramana (Sidereal Solar) details:
    - Solar Sidereal Month (1=Mesha to 12=Meena)
    - Solar Day of the month
    - Tamil, Malayalam (Kollam), Bengali, and Odia month names
    - Next Sankranti transition time
    """
    ssd = daily_panchaanga.solar_sidereal_date_sunset
    solar_month = ssd.month  # 1 to 12 (Mesha to Meena)
    solar_day = ssd.day

    rashi_dev = RASHI_NAMES_DEV[solar_month - 1]
    rashi_user = transliterate_text(rashi_dev, target_lang)

    tamil_month = TAMIL_MONTHS[solar_month - 1]
    malayalam_month = MALAYALAM_MONTHS[solar_month - 1]
    bengali_month = BENGALI_MONTHS[solar_month - 1]
    odia_month = ODIA_MONTHS[solar_month - 1]

    # Kollam Year: Civil year - 825 (e.g. 2026 is Kollam 1201-1202)
    # Kollam new year starts in Chingam (Solar month 5 / Simha)
    kollam_year = daily_panchaanga.date.year - 825
    if solar_month >= 5:
        kollam_year += 1

    # Bangabda (Bengali Era): Civil year - 593 (starts Boishakh / Mesha)
    bengali_year = daily_panchaanga.date.year - 593

    transition_info = None
    if ssd.month_transition is not None:
        transition_info = {
            "transition_jd": ssd.month_transition,
            "target_solar_month": (solar_month % 12) + 1,
            "target_rashi": transliterate_text(RASHI_NAMES_DEV[solar_month % 12], target_lang)
        }

    solar_month_name = f"{rashi_user} ({solar_day}వ రోజు)" if target_lang == "telugu" else (f"{rashi_user} (Day {solar_day})" if target_lang == "english" else f"{rashi_user} ({solar_day})")

    return {
        "solar_month": {
            "index": solar_month,
            "name": solar_month_name,
            "rashi_name": rashi_user,
            "rashi_name_sanskrit": rashi_dev,
            "day": solar_day
        },
        "regional_solar_calendars": {
            "tamil": {
                "month_name": tamil_month,
                "day": solar_day
            },
            "malayalam_kollam": {
                "month_name": malayalam_month,
                "day": solar_day,
                "kollam_year": kollam_year
            },
            "bengali_san": {
                "month_name": bengali_month,
                "day": solar_day,
                "bangabda_year": bengali_year
            },
            "odia": {
                "month_name": odia_month,
                "day": solar_day
            }
        },
        "sankranti_transition": transition_info
    }


def compute_barhaspatyamana(jd: float, target_lang: str) -> dict:
    """
    Computes Barhaspatyamana (Jovian Calendar) using Swiss Ephemeris:
    - Jupiter's Sidereal Longitude, Rashi, Deg/Min
    - Jupiter's Nakshatra & Pada
    - Retrograde (Vakra) status
    - 60-Year Barhaspatya Samvatsara
    - 12-Year Jovian Maha-Masa Cycle
    - Sacred River Pushkaram
    """
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    ayan = swe.get_ayanamsa_ut(jd)
    res_j, _ = swe.calc_ut(jd, swe.JUPITER, swe.FLG_SWIEPH | swe.FLG_SPEED)

    # Sidereal Longitude
    sid_lon = (res_j[0] - ayan) % 360.0
    speed = res_j[3]
    is_retrograde = speed < 0

    # Rashi (1 = Mesha to 12 = Meena)
    rashi_idx = int(sid_lon // 30) + 1
    deg_in_rashi = sid_lon % 30
    deg_int = int(deg_in_rashi)
    min_int = int((deg_in_rashi - deg_int) * 60)

    # Nakshatra (1 to 27) & Pada (1 to 4)
    nakshatra_span = 360.0 / 27.0
    pada_span = 360.0 / 108.0
    naksh_idx = int(sid_lon // nakshatra_span) + 1
    pada = int((sid_lon % nakshatra_span) // pada_span) + 1

    rashi_dev = RASHI_NAMES_DEV[rashi_idx - 1]
    rashi_user = transliterate_text(rashi_dev, target_lang)

    naksh_dev = NAKSHATRA_NAMES_DEV[naksh_idx - 1]
    naksh_user = transliterate_text(naksh_dev, target_lang)

    # 12-Year Maha-Masa
    maha_masa_dev = MAHA_MASA_NAMES.get(rashi_idx, "महा-वैशाख")
    maha_masa_user = transliterate_text(maha_masa_dev, target_lang)

    # Pushkaram
    pushkara = PUSHKARA_RIVERS.get(rashi_idx, PUSHKARA_RIVERS[1])
    if target_lang.lower() == "telugu":
        pushkara_name = pushkara["name_te"]
    elif target_lang.lower() == "english":
        pushkara_name = f"{pushkara['name_sa']} River Pushkaram"
    elif target_lang.lower() == "devanagari":
        pushkara_name = f"{pushkara['name_sa']} नदी पुष्कर"
    elif target_lang.lower() == "tamil":
        pushkara_name = f"{pushkara['name_sa']} நதி புஷ்கரம்"
    elif target_lang.lower() == "kannada":
        pushkara_name = f"{pushkara['name_sa']} ನದಿ ಪುಷ್ಕರ"
    else:
        pushkara_name = transliterate_text(f"{pushkara['name_sa']} नदी पुष्कर", target_lang)

    motion_map = {
        "telugu": ("వక్ర (Retrograde)", "ఋజు (Direct)"),
        "english": ("Retrograde (Vakra)", "Direct (Riju)"),
        "devanagari": ("वक्री (Retrograde)", "मार्गी (Direct)"),
        "tamil": ("வக்ரம் (Retrograde)", "நேர்கதி (Direct)"),
        "kannada": ("ವಕ್ರ (Retrograde)", "ಋಜು (Direct)")
    }
    m_pair = motion_map.get(target_lang.lower(), motion_map["english"])
    motion_str = m_pair[0] if is_retrograde else m_pair[1]

    cycle_name_map = {
        "telugu": "ద్వాదశ వార్షిక బార్హస్పత్య యుగం",
        "english": "12-Year Jovian Cycle (Barhaspatya Yuga)",
        "devanagari": "द्वादश वार्षिक बार्हस्पत्य युग",
        "tamil": "துவாதச வார்ஷிக பார்ஹஸ்பத்ய யுகம்",
        "kannada": "ದ್ವಾದಶ ವಾರ್ಷಿಕ ಬಾರ್ಹಸ್ಪತ್ಯ ಯುಗ"
    }
    cycle_name = cycle_name_map.get(target_lang.lower(), cycle_name_map["english"])

    return {
        "jupiter_position": {
            "sidereal_longitude": round(sid_lon, 4),
            "rashi_index": rashi_idx,
            "rashi_name": rashi_user,
            "rashi_degrees": f"{deg_int}° {min_int}'",
            "nakshatra_index": naksh_idx,
            "nakshatra_name": naksh_user,
            "pada": pada,
            "is_retrograde": is_retrograde,
            "motion_status": motion_str
        },
        "jovian_cycle_12_year": {
            "cycle_name": cycle_name,
            "maha_masa": maha_masa_user,
            "maha_masa_sanskrit": maha_masa_dev
        },
        "sacred_river_pushkaram": {
            "active_river": pushkara_name,
            "rashi_ingress": rashi_user,
            "description": pushkara["desc"]
        }
    }
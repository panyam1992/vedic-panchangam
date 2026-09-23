"""
Rashi Phalalu (Horoscope & Transit Forecast) Service.
Calculates Daily (Dina), Monthly (Masa), and Yearly (Varsha) Rashi Phalalu
using Swiss Ephemeris astronomical positions, Gochara Shastra,
Chandra Bala, Tara Bala, Chandrashtama detection, Sade Sati status,
and traditional Panchanga Kandadayam (Adaya-Vyaya) principles.
"""

import math
from datetime import datetime, date
from typing import Dict, Any, List, Optional, Tuple
import swisseph as swe

from schemas.rashi_models import (
    RashiMeta,
    CategoryPredictions,
    DailyRashiItem,
    DailyRashiResponse,
    MonthlyRashiItem,
    MonthlyRashiResponse,
    KandadayamData,
    YearlyRashiItem,
    YearlyRashiResponse,
    TrimesterKandaya,
    NakshatraKandayaItem,
    RashiKandadayamItem,
    ComprehensiveKandadayamResponse
)
from indic_transliteration import sanscript
from services.localization_service import transliterate_text

# 12 Rashi Base Definitions
RASHI_DEFINITIONS = [
    {"code": "mesha", "symbol": "♈", "lord_code": "mars", "element_code": "fire", "start_nak": 0, "lucky_num": 9, "lucky_color_te": "ఎరుపు / సింధూరం", "lucky_color_en": "Red / Crimson", "direction_te": "తూర్పు", "direction_en": "East"},
    {"code": "vrishabha", "symbol": "♉", "lord_code": "venus", "element_code": "earth", "start_nak": 2, "lucky_num": 6, "lucky_color_te": "తెలుపు / క్రీమ్", "lucky_color_en": "White / Cream", "direction_te": "దక్షిణం", "direction_en": "South"},
    {"code": "mithuna", "symbol": "♊", "lord_code": "mercury", "element_code": "air", "start_nak": 4, "lucky_num": 5, "lucky_color_te": "ఆకుపచ్చ / పిస్తా", "lucky_color_en": "Green / Emerald", "direction_te": "పడమర", "direction_en": "West"},
    {"code": "karkataka", "symbol": "♋", "lord_code": "moon", "element_code": "water", "start_nak": 6, "lucky_num": 2, "lucky_color_te": "ముత్యపు తెలుపు / వెండి", "lucky_color_en": "Pearl White / Silver", "direction_te": "ఉత్తరం", "direction_en": "North"},
    {"code": "simha", "symbol": "♌", "lord_code": "sun", "element_code": "fire", "start_nak": 9, "lucky_num": 1, "lucky_color_te": "బంగారు పసుపు / నారింజ", "lucky_color_en": "Golden Yellow / Orange", "direction_te": "తూర్పు", "direction_en": "East"},
    {"code": "kanya", "symbol": "♍", "lord_code": "mercury", "element_code": "earth", "start_nak": 11, "lucky_num": 5, "lucky_color_te": "ఆకుపచ్చ / లేత పసుపు", "lucky_color_en": "Emerald Green", "direction_te": "దక్షిణం", "direction_en": "South"},
    {"code": "tula", "symbol": "♎", "lord_code": "venus", "element_code": "air", "start_nak": 13, "lucky_num": 6, "lucky_color_te": "తెలుపు / గులాబీ", "lucky_color_en": "White / Light Pink", "direction_te": "పడమర", "direction_en": "West"},
    {"code": "vrishchika", "symbol": "♏", "lord_code": "mars", "element_code": "water", "start_nak": 15, "lucky_num": 9, "lucky_color_te": "ఎరుపు / మెరూన్", "lucky_color_en": "Deep Red / Maroon", "direction_te": "ఉత్తరం", "direction_en": "North"},
    {"code": "dhanus", "symbol": "♐", "lord_code": "jupiter", "element_code": "fire", "start_nak": 18, "lucky_num": 3, "lucky_color_te": "పసుపు / బ్రౌన్", "lucky_color_en": "Yellow / Golden", "direction_te": "తూర్పు", "direction_en": "East"},
    {"code": "makara", "symbol": "♑", "lord_code": "saturn", "element_code": "earth", "start_nak": 20, "lucky_num": 8, "lucky_color_te": "నీలం / నలుపు", "lucky_color_en": "Navy Blue / Black", "direction_te": "దక్షిణం", "direction_en": "South"},
    {"code": "kumbha", "symbol": "♒", "lord_code": "saturn", "element_code": "air", "start_nak": 22, "lucky_num": 8, "lucky_color_te": "ఆకాశ నీలం / వంగపువ్వు", "lucky_color_en": "Sky Blue / Purple", "direction_te": "పడమర", "direction_en": "West"},
    {"code": "meena", "symbol": "♓", "lord_code": "jupiter", "element_code": "water", "start_nak": 24, "lucky_num": 3, "lucky_color_te": "బంగారు పసుపు / కేసరి", "lucky_color_en": "Yellow / Saffron", "direction_te": "ఉత్తరం", "direction_en": "North"},
]

# Multilingual Names for 12 Rashis
RASHI_NAMES = {
    "telugu": ["మేషం", "వృషభం", "మిథునం", "కర్కాటకం", "సింహం", "కన్య", "తుల", "వృశ్చికం", "ధనుస్సు", "మకరం", "కుంభం", "మీనం"],
    "english": ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"],
    "devanagari": ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुम्भ", "मीन"],
    "tamil": ["மேஷம்", "ரிஷபம்", "மிதுனம்", "கடகம்", "சிம்மம்", "கன்னி", "துலாம்", "விருச்சிகம்", "தனுசு", "மகரம்", "கும்பம்", "மீனம்"],
    "kannada": ["ಮೇಷ", "ವೃಷಭ", "ಮಿಥುನ", "ಕರ್ಕಾಟಕ", "ಸಿಂಹ", "ಕನ್ಯಾ", "ತುಲಾ", "ವೃಶ್ಚಿಕ", "ಧನು", "ಮಕರ", "ಕುಂಭ", "ಮೀನ"],
    "malayalam": ["മേടം", "ഇടവം", "മിഥുനം", "കർക്കിടകം", "ചിങ്ങം", "കന്നി", "തുലാം", "വൃശ്ചികം", "ധനു", "മകരം", "കുംഭം", "മീനം"],
    "gujarati": ["મેષ", "વૃષભ", "મિથુન", "કર્ક", "સિંહ", "કન્યા", "તુલા", "વૃશ્ચિક", "ધન", "મકર", "કુંભ", "મીન"],
    "bengali": ["মেষ", "বৃষ", "মিথুন", "কর্কট", "সিংহ", "কন্যা", "তুলা", "বৃশ্চিক", "ধনু", "মকর", "কুম্ভ", "মীন"],
}

# Lords Multilingual
LORD_NAMES = {
    "telugu": {"mars": "కుజుడు", "venus": "శుక్రుడు", "mercury": "బుధుడు", "moon": "చంద్రుడు", "sun": "సూర్యుడు", "jupiter": "గురుడు", "saturn": "శని"},
    "english": {"mars": "Mars", "venus": "Venus", "mercury": "Mercury", "moon": "Moon", "sun": "Sun", "jupiter": "Jupiter", "saturn": "Saturn"},
    "devanagari": {"mars": "मङ्गल", "venus": "शुक्र", "mercury": "बुध", "moon": "चन्द्र", "sun": "सूर्य", "jupiter": "गुरु", "saturn": "शनि"},
    "tamil": {"mars": "செவ்வாய்", "venus": "சுக்கிரன்", "mercury": "புதன்", "moon": "சந்திரன்", "sun": "சூரியன்", "jupiter": "குரு", "saturn": "சனி"},
    "kannada": {"mars": "ಕುಜ", "venus": "ಶುಕ್ರ", "mercury": "ಬುಧ", "moon": "ಚಂದ್ರ", "sun": "ಸೂರ್ಯ", "jupiter": "ಗುರು", "saturn": "ಶನಿ"},
    "malayalam": {"mars": "ചൊവ്വ", "venus": "ശുക്രൻ", "mercury": "ബുധൻ", "moon": "ചന്ദ്രൻ", "sun": "സൂര്യൻ", "jupiter": "വ്യാഴം", "saturn": "ശനി"},
    "gujarati": {"mars": "મંગળ", "venus": "શુક્ર", "mercury": "બુધ", "moon": "ચંદ્ર", "sun": "સૂર્ય", "jupiter": "ગુરુ", "saturn": "શનિ"},
    "bengali": {"mars": "মঙ্গল", "venus": "শুক্র", "mercury": "বুধ", "moon": "চন্দ্র", "sun": "সূর্য", "jupiter": "বৃহস্পতি", "saturn": "শনি"},
}

ELEMENT_NAMES = {
    "telugu": {"fire": "అగ్ని (Fire)", "earth": "భూమి (Earth)", "air": "వాయువు (Air)", "water": "జలం (Water)"},
    "english": {"fire": "Fire", "earth": "Earth", "air": "Air", "water": "Water"},
    "devanagari": {"fire": "अग्नि (Fire)", "earth": "पृथ्वी (Earth)", "air": "वायु (Air)", "water": "जल (Water)"},
    "tamil": {"fire": "நெருப்பு (Fire)", "earth": "நிலம் (Earth)", "air": "காற்று (Air)", "water": "நீர் (Water)"},
    "kannada": {"fire": "ಅಗ್ನಿ (Fire)", "earth": "ಭೂಮಿ (Earth)", "air": "ವಾಯು (Air)", "water": "ಜಲ (Water)"},
    "malayalam": {"fire": "തീ (Fire)", "earth": "ഭൂമി (Earth)", "air": "വായു (Air)", "water": "ജലം (Water)"},
    "gujarati": {"fire": "અગ્નિ (Fire)", "earth": "પૃથ્વી (Earth)", "air": "વાયુ (Air)", "water": "જળ (Water)"},
    "bengali": {"fire": "অগ্নি (Fire)", "earth": "ভূমি (Earth)", "air": "বায়ু (Air)", "water": "জল (Water)"},
}

# Traditional Parabhava Samvatsara (2026-2027) Kandadayam: (Adayam, Vyayam, Rajapujyam, Avamanam)
# Based on planetary lordship pairs and Ugadi Chaitra Shukla Pratipada horizon Ganitam:
PARABHAVA_KANDADAYAM = [
    (11, 5, 2, 4),   # Mesha (Aries - Mars)
    (5, 14, 5, 4),   # Vrishabha (Taurus - Venus)
    (8, 11, 1, 7),   # Mithuna (Gemini - Mercury)
    (2, 11, 4, 7),   # Karkataka (Cancer - Moon)
    (5, 5, 7, 7),    # Simha (Leo - Sun)
    (8, 11, 3, 3),   # Kanya (Virgo - Mercury)
    (5, 14, 6, 3),   # Tula (Libra - Venus)
    (11, 5, 2, 6),   # Vrishchika (Scorpio - Mars)
    (14, 11, 5, 6),  # Dhanus (Sagittarius - Jupiter)
    (2, 8, 1, 2),    # Makara (Capricorn - Saturn)
    (2, 8, 4, 2),    # Kumbha (Aquarius - Saturn)
    (14, 11, 7, 5),  # Meena (Pisces - Jupiter)
]

# 9 Tara Bala Names in Telugu & English
TARA_NAMES = {
    "telugu": ["జన్మ తార (శరీర శ్రమ/అప్రమత్తత)", "సంపత్ తార (ధనలాభం/శుభం)", "విపత్ తార (ప్రతిబంధకాలు)", "క్షేమ తార (క్షేమము/సంతోషం)", "ప్రత్యక్ తార (విరోధాలు)", "సాధక తార (కార్యసిద్ధి/విజయం)", "నైధన తార (తీవ్ర క్లేశం)", "మిత్ర తార (స్నేహం/సుఖం)", "పరమ మిత్ర తార (అత్యుత్తమ లాభం)"],
    "english": ["Janma Tara (Caution)", "Sampat Tara (Wealth)", "Vipat Tara (Obstacles)", "Kshema Tara (Well-being)", "Pratyak Tara (Disputes)", "Sadhaka Tara (Success)", "Naidhana Tara (Adversity)", "Mitra Tara (Friendly)", "Parama Mitra Tara (Supreme)"],
    "devanagari": ["जन्म तारा (सावधानी)", "सम्पत् तारा (धन लाभ)", "विपत् तारा (विघ्न)", "क्षेम तारा (क्षेम)", "प्रत्यक् तारा (विरोध)", "साधक तारा (कार्यसिद्धि)", "नैधन तारा (क्लेश)", "मित्र तारा (सुख)", "परम मित्र तारा (उत्कृष्ट)"]
}


def _get_julian_day(y: int, m: int, d: int, hour: float = 6.0) -> float:
    return swe.julday(y, m, d, hour)


def _get_sidereal_planets(jd: float) -> Dict[str, Tuple[float, int]]:
    """Returns sidereal Nirayana longitudes and rashi index (0-11) for all planets."""
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    planets_map = {
        "sun": swe.SUN,
        "moon": swe.MOON,
        "mars": swe.MARS,
        "mercury": swe.MERCURY,
        "jupiter": swe.JUPITER,
        "venus": swe.VENUS,
        "saturn": swe.SATURN,
        "rahu": swe.MEAN_NODE,
    }
    results = {}
    for name, p_id in planets_map.items():
        res, _ = swe.calc_ut(jd, p_id, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
        lon = res[0] % 360.0
        r_idx = int(lon // 30)
        results[name] = (lon, r_idx)

    # Ketu is exactly 180 degrees opposite to Rahu
    rahu_lon, _ = results["rahu"]
    ketu_lon = (rahu_lon + 180.0) % 360.0
    results["ketu"] = (ketu_lon, int(ketu_lon // 30))
    return results


def _build_rashi_meta(idx: int, lang: str) -> RashiMeta:
    base = RASHI_DEFINITIONS[idx]
    names_list = RASHI_NAMES.get(lang, RASHI_NAMES["telugu"])
    name_str = names_list[idx] if idx < len(names_list) else RASHI_NAMES["english"][idx]
    sanskrit_name = RASHI_NAMES["devanagari"][idx]
    lord_dict = LORD_NAMES.get(lang, LORD_NAMES["telugu"])
    lord_str = lord_dict.get(base["lord_code"], base["lord_code"].capitalize())
    elem_dict = ELEMENT_NAMES.get(lang, ELEMENT_NAMES["telugu"])
    elem_str = elem_dict.get(base["element_code"], base["element_code"].capitalize())

    return RashiMeta(
        id=idx + 1,
        code=base["code"],
        name=name_str,
        name_sanskrit=sanskrit_name,
        name_english=RASHI_NAMES["english"][idx],
        symbol=base["symbol"],
        lord=lord_str,
        element=elem_str
    )


# ==================== 1. DAILY RASHI PHALALU ====================

def compute_daily_rashi_phalalu(date_str: str, lang: str = "telugu") -> DailyRashiResponse:
    """Computes daily horoscope predictions for all 12 rashis for the specified date."""
    target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    jd = _get_julian_day(target_date.year, target_date.month, target_date.day, 6.0)
    planets = _get_sidereal_planets(jd)

    moon_lon, moon_r_idx = planets["moon"]
    moon_nak_idx = int(moon_lon // (360.0 / 27.0))

    lang_code = lang if lang in RASHI_NAMES else "telugu"
    moon_rashi_name = RASHI_NAMES[lang_code][moon_r_idx]
    weekday_str = target_date.strftime("%A")

    items: List[DailyRashiItem] = []

    for idx in range(12):
        meta = _build_rashi_meta(idx, lang_code)
        base = RASHI_DEFINITIONS[idx]

        # House of Moon from Janma Rashi (1 to 12)
        moon_house = ((moon_r_idx - idx) % 12) + 1
        is_chandrashtama = (moon_house == 8)

        # Chandra Bala Assessment
        if is_chandrashtama:
            chandra_status = "చంద్రాష్టమం (తీవ్ర అప్రమత్తత అవసరం)" if lang_code == "telugu" else ("Chandrashtama (High Caution)" if lang_code == "english" else "चन्द्राष्टम (सावधानी)")
        elif moon_house in [1, 3, 6, 7, 10, 11]:
            chandra_status = "అనుకూలం (చంద్రబలం కలదు)" if lang_code == "telugu" else ("Favorable (Chandra Balam Active)" if lang_code == "english" else "अनुकूल (चन्द्रबल)")
        else:
            chandra_status = "సాధారణం / మధ్యమం" if lang_code == "telugu" else ("Moderate" if lang_code == "english" else "मध्यम")

        # Tara Bala calculation
        start_nak = base["start_nak"]
        tara_idx = ((moon_nak_idx - start_nak) % 9)
        tara_name_list = TARA_NAMES.get(lang_code, TARA_NAMES["telugu"])
        tara_name = tara_name_list[tara_idx]
        is_tara_good = tara_idx in [1, 3, 5, 7, 8]  # 2, 4, 6, 8, 9

        # Score calculation (0-100%)
        score = 60
        if moon_house in [3, 6, 11]:
            score += 20
        elif moon_house in [1, 7, 10]:
            score += 10
        elif moon_house == 8:
            score -= 30
        else:
            score -= 10

        if is_tara_good:
            score += 15
        elif tara_idx in [2, 4, 6]:  # Vipat, Pratyak, Naidhana
            score -= 15

        # Benefic alignment (Jupiter, Venus)
        jup_house = ((planets["jupiter"][1] - idx) % 12) + 1
        if jup_house in [2, 5, 7, 9, 11]:
            score += 5

        score = max(35, min(95, score))

        if score >= 80:
            rating = "అత్యుత్తమం (Excellent)" if lang_code == "telugu" else ("Excellent" if lang_code == "english" else "उत्कृष्ट")
        elif score >= 65:
            rating = "అనుకూలం (Good)" if lang_code == "telugu" else ("Favorable" if lang_code == "english" else "अनुकूल")
        elif score >= 50:
            rating = "సాధారణం (Average)" if lang_code == "telugu" else ("Average" if lang_code == "english" else "सामान्य")
        else:
            rating = "అప్రమత్తత అవసరం (Caution)" if lang_code == "telugu" else ("Caution Needed" if lang_code == "english" else "सावधानी अपेक्षित")

        # Dynamic Category Predictions based on houses & transits
        preds = _generate_daily_predictions(idx, moon_house, is_chandrashtama, score, lang_code)
        remedy = _generate_daily_remedy(idx, is_chandrashtama, lang_code)

        lucky_color = base["lucky_color_te"] if lang_code == "telugu" else base["lucky_color_en"]
        lucky_direction = base["direction_te"] if lang_code == "telugu" else base["direction_en"]

        items.append(DailyRashiItem(
            rashi=meta,
            moon_house=moon_house,
            is_chandrashtama=is_chandrashtama,
            chandra_bala_status=chandra_status,
            tara_bala_name=tara_name,
            is_tara_bala_good=is_tara_good,
            score_percent=score,
            score_rating=rating,
            lucky_number=base["lucky_num"],
            lucky_color=lucky_color,
            lucky_direction=lucky_direction,
            predictions=preds,
            remedy=remedy
        ))

    return DailyRashiResponse(
        date=date_str,
        weekday=weekday_str,
        language=lang_code,
        moon_rashi=moon_rashi_name,
        moon_nakshatra=f"Nakshatra #{moon_nak_idx + 1}",
        rashis=items
    )


def _generate_daily_predictions(r_idx: int, moon_house: int, is_chandra: bool, score: int, lang: str) -> CategoryPredictions:
    if is_chandra:
        if lang == "telugu":
            return CategoryPredictions(
                general="చంద్రాష్టమ ప్రభావం వల్ల మనస్సు చంచలంగా ఉంటుంది. ముఖ్యమైన నిర్ణయాలు, నూతన ఒప్పందాలు రేపటికి వాయిదా వేయడం శ్రేయస్కరం.",
                career="కార్యాలయంలో అధికారులతో లేదా సహోద్యోగులతో అనవసర వాదనలకు దిగవద్దు. నిర్దేశిత పనులను ఓపికతో పూర్తి చేయండి.",
                finance="ఆర్థిక పరమైన లావాదేవీలలో అప్రమత్తంగా ఉండాలి. అనవసర వ్యయాలు, ఆకస్మిక ఖర్చులు పెరిగే అవకాశం ఉంది.",
                health="మానసిక ఒత్తిడి మరియు అలసట రాకుండా తగినంత విశ్రాంతి తీసుకోండి. ప్రయాణాలలో జాగ్రత్త వహించండి.",
                family="కుటుంబ సభ్యులతో సంభాషణలలో సంయమనం పాటించండి. చిన్న విషయాలకు కోపం తెచ్చుకోకపోవడం ఉత్తమం."
            )
        else:
            return CategoryPredictions(
                general="Chandrashtama is active today. Keep patience, avoid vital decisions, and postpone major investments.",
                career="Maintain composure at the workplace. Avoid confrontations with colleagues or senior managers.",
                finance="Monitor expenses closely. Avoid taking loans or lending money today.",
                health="Take adequate rest and stay calm. Avoid stressful travels and reckless driving.",
                family="Maintain peaceful communication with family members and spouse. Avoid arguments."
            )

    if moon_house in [3, 6, 11]:
        if lang == "telugu":
            return CategoryPredictions(
                general="ఈ రోజు మీకు సర్వతోముఖ అనుకూలత లభిస్తుంది. ధైర్య సాహసాలతో ప్రారంభించిన పనులు దిగ్విజయంగా పూర్తవుతాయి.",
                career="ఉద్యోగంలో మీ ప్రతిభకు గుర్తింపు లభిస్తుంది. అధికారుల ప్రశంసలు మరియు నూతన అవకాశాలు చేకూరతాయి.",
                finance="ఆర్థిక పరిస్థితి సంతృప్తికరంగా ఉంటుంది. రావలసిన బాకీలు వసూలవుతాయి, నూతన ఆదాయ వనరులు ఏర్పడతాయి.",
                health="ఉత్సాహంగా, చురుగ్గా ఉంటారు. పాత అనారోగ్య సమస్యల నుండి ఉపశమనం లభిస్తుంది.",
                family="కుటుంబంలో శుభ పరిణామాలు, ఆనందకర వాతావరణం నెలకొంటుంది. బంధుమిత్రుల కలయిక సంతోషాన్నిస్తుంది."
            )
        else:
            return CategoryPredictions(
                general="Favorable celestial transits bring courage, success, and prosperity across key undertakings.",
                career="Excellent progress in professional spheres. Your efforts will receive appreciation from leadership.",
                finance="Inflow of funds is strong. Profitable opportunities and pending receivables will materialize.",
                health="Energetic and cheerful disposition throughout the day. Health remains sound.",
                family="Warmth and harmony prevail in family life. Joyful interactions with relatives and friends."
            )

    if moon_house in [1, 7, 10]:
        if lang == "telugu":
            return CategoryPredictions(
                general="రోజువారీ పనులలో పురోగతి కనిపిస్తుంది. నూతన మిత్రుల సహకారం లభించి ఆత్మవిశ్వాసం పెరుగుతుంది.",
                career="వ్యాపార భాగస్వామ్యాలు లాభిస్తాయి. వృత్తిలో కీలక బాధ్యతలను సమర్థవంతంగా నిర్వర్తిస్తారు.",
                finance="ఆదాయ వ్యయాలు సమానంగా ఉంటాయి. గృహావసరాలు, శుభకార్యాల నిమిత్తం ఖర్చులు చేస్తారు.",
                health="ఆరోగ్యం నిలకడగా ఉంటుంది. సమయానికి భోజనం చేయడం మరియు నీరు తగినంత తాగడం ముఖ్యం.",
                family="దాంపత్య జీవితంలో అనురాగం పెంపొందుతుంది. పిల్లల చదువులు లేదా ప్రవర్తన సంతృప్తినిస్తుంది."
            )
        else:
            return CategoryPredictions(
                general="Steady progress in daily initiatives. Interactions with associates boost confidence.",
                career="Partnerships and collaborative tasks yield positive results. Professional responsibilities handled well.",
                finance="Balanced financial situation. Expenses incurred on auspicious home necessities.",
                health="Health remains stable. Maintain a balanced diet and regular hydration.",
                family="Affection and mutual support in marital life. Pleasant time spent with children and elders."
            )

    # Moderate / Challenging houses (2, 4, 5, 9, 12)
    if lang == "telugu":
        return CategoryPredictions(
            general="మధ్యస్థ ఫలితాలు గోచరిస్తున్నాయి. పనులలో చిన్నపాటి జాప్యం జరిగినా చివరికి సత్ఫలితాలు దక్కుతాయి.",
            career="పనుల ఒత్తిడి ఎక్కువగా ఉండవచ్చు. ప్రణాళికాబద్ధంగా వ్యవహరిస్తే అనుకున్న లక్ష్యాలను సాధించవచ్చు.",
            finance="ఖర్చులను నియంత్రించుకోవడం అవసరం. దుబారా ఖర్చులు చేయకుండా పొదుపుకు ప్రాధాన్యత ఇవ్వండి.",
            health="చిన్నపాటి తలనొప్పి లేదా కంటి సమస్యలు రావచ్చు. కంటినిండా నిద్రపోవడం అవసరం.",
            family="కుటుంబ సభ్యుల సలహాలు మేలు చేస్తాయి. ఆధ్యాత్మిక కార్యక్రమాలలో పాల్గొనడం ప్రశాంతతను ఇస్తుంది."
        )
    else:
        return CategoryPredictions(
            general="Mixed outcomes for the day. Minor delays in plans will be overcome with persistent effort.",
            career="Workload may demand extra concentration. Stay organized to meet expectations seamlessly.",
            finance="Practice financial discipline. Avoid impulsive purchases and focus on savings.",
            health="Minor eye strain or fatigue possible. Ensure restorative rest.",
            family="Elderly family guidance proves beneficial. Spiritual contemplation brings inner peace."
        )


def _generate_daily_remedy(r_idx: int, is_chandra: bool, lang: str) -> str:
    if is_chandra:
        return "ఓం నమశ్శివాయ జపం చేయండి లేదా శివునికి పాలాభిషేకం/దీపారాధన చేయడం ద్వారా చంద్రాష్టమ దోషం నివృత్తి అవుతుంది." if lang == "telugu" else "Chant 'Om Namah Shivaya' or offer white flowers/water to Lord Shiva for peace."

    lord_code = RASHI_DEFINITIONS[r_idx]["lord_code"]
    remedies_te = {
        "mars": "సుబ్రహ్మణ్య స్వామి స్తోత్రం లేదా హనుమాన్ చాలీసా పఠించండి.",
        "venus": "శ్రీ మహాలక్ష్మీ అష్టకం చదువుకోండి, ఆవుకు అరటిపండు సమర్పించండి.",
        "mercury": "విష్ణు సహస్రనామ స్తోత్రం లేదా బుధ గాయత్రి జపించండి.",
        "moon": "శివాష్టకం లేదా లలితా సహస్రనామ పఠనం శుభాన్నిస్తుంది.",
        "sun": "సూర్య నమస్కారాలు చేయండి లేదా ఆదిత్య హృదయ స్తోత్రం పఠించండి.",
        "jupiter": "దక్షిణామూర్తి స్తోత్రం లేదా గురు శ్లోకం చదివి శనగలు సమర్పించండి.",
        "saturn": "శని గాయత్రి జపించండి లేదా రావి చెట్టు వద్ద నూనె దీపం వెలిగించండి."
    }
    remedies_en = {
        "mars": "Chant Sri Subramanya Stotram or Hanuman Chalisa.",
        "venus": "Chant Mahalakshmi Ashtakam or offer fruit to a cow.",
        "mercury": "Chant Vishnu Sahasranamam or Budha Gayatri.",
        "moon": "Chant Lalita Sahasranama or offer milk/water to Shiva.",
        "sun": "Perform Surya Namaskar or recite Aditya Hridaya Stotram.",
        "jupiter": "Chant Dakshinamurthy Stotram or Guru Mantra.",
        "saturn": "Chant Shani Gayatri or light a sesame oil lamp."
    }
    return remedies_te.get(lord_code, remedies_te["mars"]) if lang == "telugu" else remedies_en.get(lord_code, remedies_en["mars"])


# ==================== 2. MONTHLY RASHI PHALALU ====================

def compute_monthly_rashi_phalalu(year: int, month: int, lang: str = "telugu") -> MonthlyRashiResponse:
    """Computes monthly horoscope predictions for all 12 rashis for the specified year/month."""
    jd = _get_julian_day(year, month, 15, 6.0)
    planets = _get_sidereal_planets(jd)
    sun_lon, sun_r_idx = planets["sun"]

    lang_code = lang if lang in RASHI_NAMES else "telugu"
    solar_month_name = RASHI_NAMES[lang_code][sun_r_idx]

    items: List[MonthlyRashiItem] = []

    for idx in range(12):
        meta = _build_rashi_meta(idx, lang_code)
        sun_house = ((sun_r_idx - idx) % 12) + 1
        is_sun_good = sun_house in [3, 6, 10, 11]

        jup_house = ((planets["jupiter"][1] - idx) % 12) + 1
        sat_house = ((planets["saturn"][1] - idx) % 12) + 1

        score = 65
        if is_sun_good:
            score += 15
        else:
            score -= 10

        if jup_house in [2, 5, 7, 9, 11]:
            score += 15
        else:
            score -= 5

        if sat_house in [3, 6, 11]:
            score += 10
        elif sat_house in [12, 1, 2, 8]:
            score -= 10

        score = max(40, min(95, score))
        rating = "అత్యుత్తమం (Excellent)" if score >= 80 else ("అనుకూలం (Good)" if score >= 65 else "సాధారణం (Average)")

        if lang_code == "telugu":
            preds = CategoryPredictions(
                general=f"ఈ మాసంలో రవి మీ రాశికి {sun_house}వ స్థానంలో సంచరిస్తున్నారు. {'సకల కార్యాలు దిగ్విజయంగా పూర్తి కాగలవు.' if is_sun_good else 'ఓపిక, సహనంతో కూడిన ప్రయత్నాలు సఫలమవుతాయి.'}",
                career="వృత్తి ఉద్యోగాలలో నూతన బాధ్యతలు చేపడతారు. తోటి ఉద్యోగుల సహకారం లభించి అధికారుల మన్ననలు పొందుతారు.",
                finance="ఆర్థిక పరిస్థితి గతం కంటే మెరుగ్గా ఉంటుంది. పెట్టుబడుల విషయంలో అనుభవజ్ఞుల సలహాలు తీసుకోవడం మేలు.",
                health="ఆరోగ్యం సాధారణంగా ఉంటుంది. కాలానికి తగిన ఆహార నియమాలు పాటించడం శ్రేయస్కరం.",
                family="కుటుంబ సభ్యులతో కలిసి ఆధ్యాత్మిక లేదా విహార యాత్రలు చేసే అవకాశాలున్నాయి. బంధాలు బలపడతాయి."
            )
            highlights = [
                f"సూర్య సంచార స్థానం: {sun_house}వ ఇల్లు ({'శుభప్రదం' if is_sun_good else 'మధ్యమం'})",
                f"గురు గ్రహ అనుకూలత: {'ఉంది' if jup_house in [2,5,7,9,11] else 'సాధారణం'}",
                "ప్రధాన ప్రాధాన్యత: క్రమశిక్షణతో కూడిన ఆర్థిక నిర్వహణ"
            ]
            remedy = "ప్రతి ఆదివారం ఆదిత్య హృదయ స్తోత్రం చదవండి మరియు శివాలయ దర్శనం శుభప్రదం."
        else:
            preds = CategoryPredictions(
                general=f"Sun transits the {sun_house}th house from your sign this month. {'Favorable outcomes in most ventures.' if is_sun_good else 'Steady progress with patience and focus.'}",
                career="Professional recognition and advancement in duties. Good cooperation from team members.",
                finance="Financial situation remains stable. Seek expert advice before initiating major speculative investments.",
                health="Vitality remains satisfactory. Follow wholesome dietary routines.",
                family="Harmonious family atmosphere with opportunities for pilgrimage or pleasant get-togethers."
            )
            highlights = [
                f"Sun transit: House #{sun_house} ({'Benefic' if is_sun_good else 'Moderate'})",
                f"Jupiter Grace: {'Strong' if jup_house in [2,5,7,9,11] else 'Moderate'}",
                "Key Focus: Prudent financial planning and relationship harmony"
            ]
            remedy = "Recite Aditya Hridaya Stotram on Sundays and visit Lord Shiva temple."

        items.append(MonthlyRashiItem(
            rashi=meta,
            sun_house=sun_house,
            is_sun_favorable=is_sun_good,
            score_percent=score,
            score_rating=rating,
            predictions=preds,
            highlights=highlights,
            remedy=remedy
        ))

    return MonthlyRashiResponse(
        year=year,
        month=month,
        solar_month=solar_month_name,
        language=lang_code,
        rashis=items
    )


# ==================== 3. YEARLY RASHI PHALALU (KANDADAYAM) ====================

def compute_yearly_rashi_phalalu(year: int = 2026, lang: str = "telugu") -> YearlyRashiResponse:
    """Computes full yearly Samvatsara predictions, Guru Balam, Sade Sati status,
    and traditional Kandadayam (Income/Expenditure/Honor/Disgrace) for all 12 rashis."""
    # Approximate mid-year for 2026 (Parabhava Nama Samvatsara)
    jd = _get_julian_day(year, 6, 15, 6.0)
    planets = _get_sidereal_planets(jd)

    lang_code = lang if lang in RASHI_NAMES else "telugu"
    samvatsara_name = "శ్రీ పరాభవ నామ సంవత్సరం" if lang_code == "telugu" else "Sri Parabhava Samvatsara"

    items: List[YearlyRashiItem] = []

    for idx in range(12):
        meta = _build_rashi_meta(idx, lang_code)
        kd_tuple = PARABHAVA_KANDADAYAM[idx]
        aadhayam, vyayam, rajapujyam, avamanam = kd_tuple

        # Comparative statuses
        if aadhayam > vyayam:
            fin_status = "విశేష ధనలాభం & ఆర్థిక అభివృద్ధి" if lang_code == "telugu" else "Substantial Wealth & Surplus"
        elif aadhayam == vyayam:
            fin_status = "ఆదాయ వ్యయాలు సమతుల్యం" if lang_code == "telugu" else "Balanced Income & Expenses"
        else:
            fin_status = "ఖర్చులు ఎక్కువ (ఆర్థిక జాగ్రత్త అవసరం)" if lang_code == "telugu" else "Expenditure Higher (Prudence Needed)"

        if rajapujyam > avamanam:
            soc_status = "సమాజంలో విశేష గౌరవం & కీర్తి" if lang_code == "telugu" else "High Honor & Social Prestige"
        elif rajapujyam == avamanam:
            soc_status = "సాధారణ గౌరవ మర్యాదలు" if lang_code == "telugu" else "Steady Social Standing"
        else:
            soc_status = "వివాదాలు రాకుండా సంయమనం పాటించాలి" if lang_code == "telugu" else "Maintain Caution against Disputes"

        kandadayam = KandadayamData(
            aadhayam=aadhayam,
            vyayam=vyayam,
            rajapujyam=rajapujyam,
            avamanam=avamanam,
            finance_status=fin_status,
            social_status=soc_status
        )

        # Jupiter transit assessment
        jup_r_idx = planets["jupiter"][1]
        jup_house = ((jup_r_idx - idx) % 12) + 1
        has_guru_balam = jup_house in [2, 5, 7, 9, 11]

        if has_guru_balam:
            guru_text = f"గురు బలం కలదు ({jup_house}వ స్థానం - విశేష శుభయోగం)" if lang_code == "telugu" else f"Jupiter Blessing Active (House #{jup_house} - Benefic)"
        else:
            guru_text = f"గురు ప్రతికూలత ({jup_house}వ స్థానం - గురు శాంతి అవసరం)" if lang_code == "telugu" else f"Jupiter Demands Remedial Prayers (House #{jup_house})"

        # Saturn transit assessment (Sade Sati, Ashtama Shani, Ardhastama Shani)
        sat_r_idx = planets["saturn"][1]
        sat_house = ((sat_r_idx - idx) % 12) + 1

        if sat_house == 12:
            sade_sati = "ఏలినాటి శని (ప్రథమ దశ - వ్యయ శని)" if lang_code == "telugu" else "Sade Sati (First Phase - Rising)"
        elif sat_house == 1:
            sade_sati = "ఏలినాటి శని (ద్వితీయ దశ - జన్మ శని - తీవ్ర ప్రభావం)" if lang_code == "telugu" else "Sade Sati (Second Phase - Peak Janma Shani)"
        elif sat_house == 2:
            sade_sati = "ఏలినాటి శని (తృతీయ దశ - ధన శని - ముగింపు)" if lang_code == "telugu" else "Sade Sati (Third Phase - Setting)"
        elif sat_house == 4:
            sade_sati = "అర్థాష్టమ శని (సుఖ స్థాన శని)" if lang_code == "telugu" else "Ardhastama Shani (4th House)"
        elif sat_house == 8:
            sade_sati = "అష్టమ శని (తీవ్ర పరీక్షల కాలం)" if lang_code == "telugu" else "Ashtama Shani (8th House - High Vigilance)"
        elif sat_house in [3, 6, 11]:
            sade_sati = "శని అనుకూలత (శని యోగం)" if lang_code == "telugu" else "Saturn Favorable (Upachaya Yoga)"
        else:
            sade_sati = "ఏలినాటి శని ప్రభావం లేదు (శుభం)" if lang_code == "telugu" else "No Sade Sati Influence"

        # Rahu-Ketu status
        rahu_house = ((planets["rahu"][1] - idx) % 12) + 1
        ketu_house = ((planets["ketu"][1] - idx) % 12) + 1
        rahu_ketu_str = f"రాహువు: {rahu_house}వ ఇల్లు, కేతువు: {ketu_house}వ ఇల్లు" if lang_code == "telugu" else f"Rahu in House #{rahu_house}, Ketu in House #{ketu_house}"

        # Yearly score computation
        year_score = 65
        if has_guru_balam:
            year_score += 15
        else:
            year_score -= 10

        if sat_house in [3, 6, 11]:
            year_score += 15
        elif sat_house in [12, 1, 2, 8]:
            year_score -= 15

        if aadhayam > vyayam:
            year_score += 10
        else:
            year_score -= 10

        year_score = max(40, min(95, year_score))
        year_rating = "అత్యుత్తమం (Excellent)" if year_score >= 80 else ("అనుకూలం (Good)" if year_score >= 65 else "సాధారణం (Average)")

        # Detailed yearly predictions
        if lang_code == "telugu":
            preds = CategoryPredictions(
                general=f"ఈ సంవత్సరంలో మీ రాశికి ఆదాయం {aadhayam}, వ్యయం {vyayam}, రాజపూజ్యం {rajapujyam}, అవమానం {avamanam}. {'ఆర్థికంగా అత్యంత అనుకూలమైన సంవత్సరం.' if aadhayam > vyayam else 'ఆదాయానికి మించి ఖర్చులు ఉండే అవకాశం ఉన్నందున పొదుపు అవసరం.'} గురుడు {jup_house}వ స్థానంలో, శని {sat_house}వ స్థానంలో సంచరిస్తున్నారు.",
                career="వృత్తి ఉద్యోగాలలో నూతన అవకాశాలు లభిస్తాయి. ఉన్నతాధికారుల మద్దతుతో పదోన్నతులు, ఇంక్రిమెంట్లు పొందే యోగం ఉంది. వ్యాపారులకు విస్తరణ అనుకూలం.",
                finance=f"ఆర్థిక లావాదేవీలు ఆశాజనకంగా ఉంటాయి. {fin_status}. నూతన ఆస్తులు, స్థిరాస్తులు కొనుగోలు చేసే ఆలోచనలు ఫలిస్తాయి.",
                health="శారీరక శ్రమ పెరిగినా ఆరోగ్యం సాధారణంగా అనుకూలిస్తుంది. దీర్ఘకాలిక సమస్యలు ఉన్నవారు క్రమం తప్పకుండా వైద్య పరీక్షలు చేయించుకోవాలి.",
                family="కుటుంబంలో శుభకార్యాలు, వివాహ ప్రయత్నాలు ఫలిస్తాయి. సంతాన ప్రాప్తి యోగం కలదు. బంధుమిత్రుల సహాయ సహకారాలు సంపూర్ణంగా లభిస్తాయి."
            )
            highlights = [
                f"కందాయం: ఆదాయం {aadhayam} / వ్యయం {vyayam}",
                f"కీర్తి ప్రతిష్టలు: రాజపూజ్యం {rajapujyam} / అవమానం {avamanam}",
                guru_text,
                sade_sati
            ]
            remedy = "సంవత్సరం పొడవునా నవగ్రహ ప్రార్థన చేయండి. గురువారం శనగల దానం మరియు శనివారం ఆంజనేయ స్వామి ఆరాధన విశేష ఫలితాలనిస్తాయి."
        else:
            preds = CategoryPredictions(
                general=f"For this Samvatsara, your Kandadayam stands at Income: {aadhayam}, Expenditure: {vyayam}, Honor: {rajapujyam}, Disgrace: {avamanam}. {fin_status}. Jupiter in {jup_house}th and Saturn in {sat_house}th houses govern major events.",
                career="Progressive opportunities in professional life. Recognition from superiors and promotion prospects. Favorable expansion for entrepreneurs.",
                finance=f"Sound financial standing through calculated investments. {fin_status}. Opportunities to acquire property or vehicles.",
                health="General vitality remains robust. Those with chronic ailments should maintain routine health check-ups and fitness regimens.",
                family="Auspicious celebrations, weddings, and joyful milestones at home. Cooperative and fulfilling family bonds throughout the year."
            )
            highlights = [
                f"Kandadayam: Income {aadhayam} / Expense {vyayam}",
                f"Social Standing: Honor {rajapujyam} / Disgrace {avamanam}",
                guru_text,
                sade_sati
            ]
            remedy = "Perform Navagraha prayers. Offer yellow grams on Thursdays and worship Lord Hanuman on Saturdays for sustained auspiciousness."

        items.append(YearlyRashiItem(
            rashi=meta,
            jupiter_house=jup_house,
            has_guru_balam=has_guru_balam,
            guru_balam_text=guru_text,
            saturn_house=sat_house,
            sade_sati_status=sade_sati,
            rahu_ketu_status=rahu_ketu_str,
            kandadayam=kandadayam,
            score_percent=year_score,
            score_rating=year_rating,
            predictions=preds,
            highlights=highlights,
            remedy=remedy
        ))

    return YearlyRashiResponse(
        year=year,
        samvatsara=samvatsara_name,
        language=lang_code,
        rashis=items
    )


# 27 Nakshatras Canonical Metadata & Pada-to-Rashi mapping
NAKSHATRAS_METADATA = [
    {"id": 1, "te": "అశ్వినీ", "en": "Ashwini", "dev": "अश्विनी", "rashis_te": ["మేషం"], "rashis_en": ["Aries"]},
    {"id": 2, "te": "భరణీ", "en": "Bharani", "dev": "भरणी", "rashis_te": ["మేషం"], "rashis_en": ["Aries"]},
    {"id": 3, "te": "కృత్తిక", "en": "Krittika", "dev": "कृत्तिका", "rashis_te": ["మేషం (1వ పాదం)", "వృషభం (2, 3, 4వ పాదాలు)"], "rashis_en": ["Aries (1st Pada)", "Taurus (2, 3, 4 Padas)"]},
    {"id": 4, "te": "రోహిణీ", "en": "Rohini", "dev": "रोहिणी", "rashis_te": ["వృషభం"], "rashis_en": ["Taurus"]},
    {"id": 5, "te": "మృగశిర", "en": "Mrigashira", "dev": "मृगशीर्ष", "rashis_te": ["వృషభం (1, 2వ పాదాలు)", "మిథునం (3, 4వ పాదాలు)"], "rashis_en": ["Taurus (1, 2 Padas)", "Gemini (3, 4 Padas)"]},
    {"id": 6, "te": "ఆర్ద్ర", "en": "Arudra", "dev": "आर्द्रा", "rashis_te": ["మిథునం"], "rashis_en": ["Gemini"]},
    {"id": 7, "te": "పునర్వసు", "en": "Punarvasu", "dev": "पुनर्वसु", "rashis_te": ["మిథునం (1, 2, 3వ పాదాలు)", "కర్కాటకం (4వ పాదం)"], "rashis_en": ["Gemini (1, 2, 3 Padas)", "Cancer (4th Pada)"]},
    {"id": 8, "te": "పుష్యమి", "en": "Pushyami", "dev": "पुष्य", "rashis_te": ["కర్కాటకం"], "rashis_en": ["Cancer"]},
    {"id": 9, "te": "ఆశ్లేష", "en": "Ashlesha", "dev": "आश्लेषा", "rashis_te": ["కర్కాటకం"], "rashis_en": ["Cancer"]},
    {"id": 10, "te": "మఖ", "en": "Makha", "dev": "मघा", "rashis_te": ["సింహం"], "rashis_en": ["Leo"]},
    {"id": 11, "te": "పూర్వఫల్గుణి (పుబ్బ)", "en": "Poorvaphalguni (Pubba)", "dev": "पूर्वाफाल्गुनी", "rashis_te": ["సింహం"], "rashis_en": ["Leo"]},
    {"id": 12, "te": "ఉత్తరఫల్గుణి (ఉత్తర)", "en": "Uttaraphalguni (Uttara)", "dev": "उत्तराफाल्गुनी", "rashis_te": ["సింహం (1వ పాదం)", "కన్య (2, 3, 4వ పాదాలు)"], "rashis_en": ["Leo (1st Pada)", "Virgo (2, 3, 4 Padas)"]},
    {"id": 13, "te": "హస్త", "en": "Hastha", "dev": "हस्त", "rashis_te": ["కన్య"], "rashis_en": ["Virgo"]},
    {"id": 14, "te": "చిత్త", "en": "Chitra", "dev": "चित्रा", "rashis_te": ["కన్య (1, 2వ పాదాలు)", "తుల (3, 4వ పాదాలు)"], "rashis_en": ["Virgo (1, 2 Padas)", "Libra (3, 4 Padas)"]},
    {"id": 15, "te": "స్వాతి", "en": "Swati", "dev": "स्वाती", "rashis_te": ["తుల"], "rashis_en": ["Libra"]},
    {"id": 16, "te": "విశాఖ", "en": "Vishakha", "dev": "विशाखा", "rashis_te": ["తుల (1, 2, 3వ పాదాలు)", "వృశ్చికం (4వ పాదం)"], "rashis_en": ["Libra (1, 2, 3 Padas)", "Scorpio (4th Pada)"]},
    {"id": 17, "te": "అనూరాధ", "en": "Anuradha", "dev": "अनुराधा", "rashis_te": ["వృశ్చికం"], "rashis_en": ["Scorpio"]},
    {"id": 18, "te": "జ్యేష్ఠ", "en": "Jyeshtha", "dev": "ज्येष्ठा", "rashis_te": ["వృశ్చికం"], "rashis_en": ["Scorpio"]},
    {"id": 19, "te": "మూల", "en": "Moola", "dev": "मूल", "rashis_te": ["ధనుస్సు"], "rashis_en": ["Sagittarius"]},
    {"id": 20, "te": "పూర్వాషాఢ", "en": "Poorvashadha", "dev": "पूर्वाषाढा", "rashis_te": ["ధనుస్సు"], "rashis_en": ["Sagittarius"]},
    {"id": 21, "te": "ఉత్తరాషాఢ", "en": "Uttarashadha", "dev": "उत्तराषाढा", "rashis_te": ["ధనుస్సు (1వ పాదం)", "మకరం (2, 3, 4వ పాదాలు)"], "rashis_en": ["Sagittarius (1st Pada)", "Capricorn (2, 3, 4 Padas)"]},
    {"id": 22, "te": "శ్రవణం", "en": "Shravanam", "dev": "श्रवण", "rashis_te": ["మకరం"], "rashis_en": ["Capricorn"]},
    {"id": 23, "te": "ధనిష్ఠ", "en": "Dhanishta", "dev": "धनिष्ठा", "rashis_te": ["మకరం (1, 2వ పాదాలు)", "కుంభం (3, 4వ పాదాలు)"], "rashis_en": ["Capricorn (1, 2 Padas)", "Aquarius (3, 4 Padas)"]},
    {"id": 24, "te": "శతభిషం", "en": "Shatabhisha", "dev": "शतभिषक्", "rashis_te": ["కుంభం"], "rashis_en": ["Aquarius"]},
    {"id": 25, "te": "పూర్వాభాద్ర", "en": "Poorvabhadra", "dev": "पूर्वभाद्रपदा", "rashis_te": ["కుంభం (1, 2, 3వ పాదాలు)", "మీనం (4వ పాదం)"], "rashis_en": ["Aquarius (1, 2, 3 Padas)", "Pisces (4th Pada)"]},
    {"id": 26, "te": "ఉత్తరాభాద్ర", "en": "Uttarabhadra", "dev": "उत्तरभाद्रपदा", "rashis_te": ["మీనం"], "rashis_en": ["Pisces"]},
    {"id": 27, "te": "రేవతి", "en": "Revati", "dev": "रेवती", "rashis_te": ["మీనం"], "rashis_en": ["Pisces"]},
]


def compute_comprehensive_kandadayam(year: int = 2026, lang: str = "telugu") -> ComprehensiveKandadayamResponse:
    """Computes complete traditional Kandadayam for all 12 Rashis (Adayam, Vyayam,
    Rajapujyam, Avamanam) and 27 Nakshatras across the 3 canonical trimesters:
    1. Prathama Kandayam (Chaitra, Vaishakha, Jyeshtha, Ashadha) - Months 1-4
    2. Dvitiya Kandayam (Shravana, Bhadrapada, Ashwayuja, Kartika) - Months 5-8
    3. Tritiya Kandayam (Margashirsha, Pushya, Magha, Phalguna) - Months 9-12
    """
    lang_code = lang if lang in RASHI_NAMES else "telugu"
    samvatsara_names = {
        "telugu": "శ్రీ పరాభవ నామ సంవత్సరం (2026-2027)",
        "tamil": "ஸ்ரீ பராபவ நாம வருடம் (2026-2027)",
        "kannada": "ಶ್ರೀ ಪರಾಭವ ನಾಮ ಸಂವತ್ಸರ (2026-2027)",
        "devanagari": "श्री पराभव नाम संवत्सर (2026-2027)",
        "hindi": "श्री पराभव नाम संवत्सर (2026-2027)",
        "sanskrit": "श्रीपराभवनामसंवत्सरः (2026-2027)",
        "english": "Sri Parabhava Samvatsara (2026-2027)"
    }
    samvatsara_name = samvatsara_names.get(lang_code, "Sri Parabhava Samvatsara (2026-2027)")

    # 1. 12 Rashi Kandadayam Items
    rashi_items: List[RashiKandadayamItem] = []
    for idx in range(12):
        meta = _build_rashi_meta(idx, lang_code)
        aadhayam, vyayam, rajapujyam, avamanam = PARABHAVA_KANDADAYAM[idx]

        if aadhayam > vyayam:
            fin_status_dict = {
                "telugu": "విశేష ధనలాభం & ఆర్థిక అభివృద్ధి",
                "tamil": "விசேஷ தனலாபம் & பொருளாதார வளர்ச்சி",
                "kannada": "ವಿಶೇಷ ಧನಲಾಭ & ಆರ್ಥಿಕ ಅಭಿವೃದ್ಧಿ",
                "devanagari": "विशेष धनलाभ एवं आर्थिक समृद्धि",
                "english": "Substantial Wealth & Surplus"
            }
        elif aadhayam == vyayam:
            fin_status_dict = {
                "telugu": "ఆదాయ వ్యయాలు సమతుల్యం",
                "tamil": "வரவு செலவு சமநிலை",
                "kannada": "ಆದಾಯ ವ್ಯಯಗಳು ಸಮತೋಲನ",
                "devanagari": "आय-व्यय सन्तुलन",
                "english": "Balanced Income & Expenses"
            }
        else:
            fin_status_dict = {
                "telugu": "ఖర్చులు ఎక్కువ (ఆర్థిక జాగ్రత్త అవసరం)",
                "tamil": "செலவுகள் அதிகம் (பட்ஜெட் கவனம் தேவை)",
                "kannada": "ವೆಚ್ಚಗಳು ಹೆಚ್ಚು (ಆರ್ಥಿಕ ಜಾಗರೂಕತೆ ಅಗತ್ಯ)",
                "devanagari": "व्ययाधिक्य (आर्थिक सतर्कता आवश्यक)",
                "english": "Expenditures Higher (Budget Prudence)"
            }
        fin_status = fin_status_dict.get(lang_code, fin_status_dict["english"])

        if rajapujyam > avamanam:
            soc_status_dict = {
                "telugu": "సమాజంలో విశేష గౌరవం & కీర్తి",
                "tamil": "சமூகத்தில் பெரும் மரியாதை & புகழ்",
                "kannada": "ಸಮಾಜದಲ್ಲಿ ವಿಶೇಷ ಗೌರವ & ಕೀರ್ತಿ",
                "devanagari": "समाज में विशेष मान-सम्मान एवं कीर्ति",
                "english": "High Honor & Social Respect"
            }
        elif rajapujyam == avamanam:
            soc_status_dict = {
                "telugu": "సాధారణ గౌరవ మర్యాదలు",
                "tamil": "நிலையான சமூக அந்தஸ்து",
                "kannada": "ಸಾಧಾರಣ ಗೌರವ ಮರ್ಯಾದೆಗಳು",
                "devanagari": "स्थिर सामाजिक प्रतिष्ठा",
                "english": "Steady Social Standing"
            }
        else:
            soc_status_dict = {
                "telugu": "వివాదాలు రాకుండా సంయమనం పాటించాలి",
                "tamil": "சர்ச்சைகள் வராமல் அமைதி காக்க வேண்டும்",
                "kannada": "ವಿವಾದಗಳು ಬಾರದಂತೆ ಸಂಯಮ ಕಾಪಾಡಿಕೊಳ್ಳಿ",
                "devanagari": "विवादों से बचें, संयम आवश्यक",
                "english": "Exercise Caution against Disputes"
            }
        soc_status = soc_status_dict.get(lang_code, soc_status_dict["english"])

        # Overall verdict text
        if aadhayam > vyayam and rajapujyam >= avamanam:
            verdict_dict = {
                "telugu": "అత్యంత శుభదాయకం - ఆర్థిక ప్రగతి, సమాజంలో గౌరవం",
                "tamil": "மிகவும் சுபகரமானது - பொருளாதார முன்னேற்றம், உயர் கௌரவம்",
                "kannada": "ಅತ್ಯಂತ ಶುಭದಾಯಕ - ಆರ್ಥಿಕ ಪ್ರಗತಿ, ಸಮಾಜದಲ್ಲಿ ಗೌರವ",
                "devanagari": "अत्यन्त शुभप्रद - आर्थिक प्रगति एवं सामाजिक सम्मान",
                "english": "Highly Auspicious - Financial Gain & High Honor"
            }
        elif aadhayam >= vyayam:
            verdict_dict = {
                "telugu": "శుభప్రదం - ఆర్థిక నిలకడ, శుభకార్యాలు",
                "tamil": "சுபகரமானது - நிதி நிலைத்தன்மை, நற்காரியங்கள்",
                "kannada": "ಶುಭಪ್ರದ - ಆರ್ಥಿಕ ಸ್ಥಿರತೆ, ಶುಭಕಾರ್ಯಗಳು",
                "devanagari": "शुभप्रद - आर्थिक स्थिरता एवं मांगलिक कार्य",
                "english": "Favorable - Financial Stability"
            }
        elif rajapujyam > avamanam:
            verdict_dict = {
                "telugu": "మధ్యమం - ఖర్చులు పెరిగినా గౌరవ మర్యాదలకు లోటుండదు",
                "tamil": "மத்திமம் - செலவுகள் இருப்பினும் கௌரவத்திற்கு குறைவில்லை",
                "kannada": "ಮಧ್ಯಮ - ಖರ್ಚು ಹೆಚ್ಚಿದರೂ ಗೌರವಕ್ಕೆ ಕೊರತೆಯಿಲ್ಲ",
                "devanagari": "मध्यम - व्यय के बावजूद मान-सम्मान यथावत्",
                "english": "Moderate - High Honor despite Expenses"
            }
        else:
            verdict_dict = {
                "telugu": "అప్రమత్తత అవసరం - వ్యయ నియంత్రణ, దైవ ప్రార్థన శ్రేయస్కరం",
                "tamil": "கவனம் தேவை - செலவுக் கட்டுப்பாடு, தெய்வ வழிபாடு நலம்",
                "kannada": "ಎಚ್ಚರಿಕೆ ಅಗತ್ಯ - ವೆಚ್ಚ ನಿಯಂತ್ರಣ, ದೈವ ಪ್ರಾರ್ಥನೆ ಕ್ಷೇಮ",
                "devanagari": "सावधानी आवश्यक - व्यय नियंत्रण एवं ईश्वर आराधना श्रेयस्कर",
                "english": "Caution Required - Prudent Budgeting & Prayers"
            }
        verdict = verdict_dict.get(lang_code, verdict_dict["english"])

        rashi_items.append(RashiKandadayamItem(
            rashi=meta,
            aadhayam=aadhayam,
            vyayam=vyayam,
            rajapujyam=rajapujyam,
            avamanam=avamanam,
            finance_status=fin_status,
            social_status=soc_status,
            verdict=verdict
        ))

    # 2. 27 Nakshatras 3-Trimester Kandaya
    nakshatra_items: List[NakshatraKandayaItem] = []
    is_te = (lang_code == "telugu")

    t1_title_dict = {
        "telugu": "ప్రథమ కందాయం (మొదటి 4 నెలలు)",
        "tamil": "முதல் கந்தாயம் (மாதங்கள் 1-4)",
        "kannada": "ಪ್ರಥಮ ಕಂದಾಯ (ತಿಂಗಳು 1-4)",
        "devanagari": "प्रथम कन्ददाय (मास 1-4)",
        "english": "1st Trimester (Months 1-4)"
    }
    t1_months_dict = {
        "telugu": "చైత్రం, వైశాఖం, జ్యేష్ఠం, ఆషాఢం",
        "tamil": "சைத்ரம், வைசாகம், ஜ்யேஷ்டம், ஆஷாடகம்",
        "kannada": "ಚೈತ್ರ, ವೈಶಾಖ, ಜ್ಯೇಷ್ಠ, ಆಷಾಢ",
        "devanagari": "चैत्र, वैशाख, ज्येष्ठ, आषाढ",
        "english": "Chaitra, Vaishakha, Jyeshtha, Ashadha"
    }
    t2_title_dict = {
        "telugu": "ద్వితీయ కందాయం (రెండవ 4 నెలలు)",
        "tamil": "இரண்டாம் கந்தாயம் (மாதங்கள் 5-8)",
        "kannada": "ದ್ವಿತೀಯ ಕಂದಾಯ (ತಿಂಗಳು 5-8)",
        "devanagari": "द्वितीय कन्ददाय (मास 5-8)",
        "english": "2nd Trimester (Months 5-8)"
    }
    t2_months_dict = {
        "telugu": "శ్రావణం, భాద్రపదం, ఆశ్వయుజం, కార్తీకం",
        "tamil": "ஸ்ராவணம், பாத்ரபதம், ஆஸ்வயுஜம், கார்த்திகம்",
        "kannada": "ಶ್ರಾವಣ, ಭಾದ್ರಪದ, ಆಶ್ವಯುಜ, ಕಾರ್ತಿಕ",
        "devanagari": "श्रावण, भाद्रपद, आश्वयुज, कार्तिक",
        "english": "Shravana, Bhadrapada, Ashwayuja, Kartika"
    }
    t3_title_dict = {
        "telugu": "తృతీయ కందాయం (మూడవ 4 నెలలు)",
        "tamil": "மூன்றாம் கந்தாயம் (மாதங்கள் 9-12)",
        "kannada": "ತೃತೀಯ ಕಂದಾಯ (ತಿಂಗಳು 9-12)",
        "devanagari": "तृतीय कन्ददाय (मास 9-12)",
        "english": "3rd Trimester (Months 9-12)"
    }
    t3_months_dict = {
        "telugu": "మార్గశిరం, పుష్యం, మాఘం, ఫాల్గుణం",
        "tamil": "மார்கசீர்ஷம், புஷ்யம், மாகம், பால்குனம்",
        "kannada": "ಮಾರ್ಗಶಿರ, ಪುಷ್ಯ, ಮಾಘ, ಫಾಲ್ಗುಣ",
        "devanagari": "मार्गशीर्ष, पौष, माघ, फाल्गुन",
        "english": "Margashirsha, Pushya, Magha, Phalguna"
    }
    t1_title = t1_title_dict.get(lang_code, t1_title_dict["english"])
    t1_months = t1_months_dict.get(lang_code, t1_months_dict["english"])
    t2_title = t2_title_dict.get(lang_code, t2_title_dict["english"])
    t2_months = t2_months_dict.get(lang_code, t2_months_dict["english"])
    t3_title = t3_title_dict.get(lang_code, t3_title_dict["english"])
    t3_months = t3_months_dict.get(lang_code, t3_months_dict["english"])

    status_labels = {
        "excellent": {"telugu": "ఉత్తమం", "tamil": "உத்தமம்", "kannada": "ಉತ್ತಮ", "devanagari": "उत्तम", "english": "Excellent"},
        "good": {"telugu": "అనుకూలం", "tamil": "அனுகூலம்", "kannada": "ಅನುಕೂಲ", "devanagari": "अनुकूल", "english": "Good"},
        "moderate": {"telugu": "మధ్యమం", "tamil": "மத்திமம்", "kannada": "ಮಧ್ಯಮ", "devanagari": "मध्यम", "english": "Moderate"},
        "caution": {"telugu": "అప్రమత్తత", "tamil": "கவனம் தேவை", "kannada": "ಎಚ್ಚರಿಕೆ", "devanagari": "सावधानी", "english": "Caution"}
    }

    for idx, nmeta in enumerate(NAKSHATRAS_METADATA):
        k1 = (4 + 3 * idx) % 8
        k2 = (2 + 1 * idx) % 3
        k3 = (1 + 2 * idx) % 5

        # T1 Assessment (0-7)
        if k1 >= 6:
            t1_status = status_labels["excellent"].get(lang_code, "Excellent")
            t1_pred = "విశేష ధనలాభం, నూతన కార్యసిద్ధి, ఉద్యోగ వ్యాపారాలలో అనుకూలత." if is_te else "Outstanding financial gains, success in ventures, and career growth."
        elif k1 >= 4:
            t1_status = status_labels["good"].get(lang_code, "Good")
            t1_pred = "ఆర్థిక నిలకడ, గౌరవ ప్రతిష్టలు, పనులలో పురోగతి మరియు సత్ఫలితాలు." if is_te else "Steady income, recognition, and consistent progress."
        elif k1 >= 2:
            t1_status = status_labels["moderate"].get(lang_code, "Moderate")
            t1_pred = "శ్రమతో కూడిన ఫలితాలు, హెచ్చుతగ్గులతో కూడిన ఆర్థిక స్థితి, సంయమనం అవసరం." if is_te else "Mixed results with effort, fluctuating finances; patience required."
        else:
            t1_status = status_labels["caution"].get(lang_code, "Caution")
            t1_pred = "అధిక ఖర్చులు, పనులలో జాప్యం, ఆరోగ్య విషయంలో జాగ్రత్త మరియు దైవారాధన అవసరం." if is_te else "High expenses, delays; health vigilance and prayers recommended."

        # T2 Assessment (0-2)
        if k2 == 2:
            t2_status = status_labels["excellent"].get(lang_code, "Excellent")
            t2_pred = "అభీష్టసిద్ధి, స్థిరాస్తి వ్యవహారాలలో లాభం, బంధుమిత్రుల ఆదరణ మరియు సంతోషం." if is_te else "Desires fulfilled, real estate gains, heartwarming family moments."
        elif k2 == 1:
            t2_status = status_labels["moderate"].get(lang_code, "Moderate")
            t2_pred = "సాధారణ జీవనం, అనుకూల ప్రతికూలతల సమతూకం, బడ్జెట్ ప్రకారం ఖర్చులు చేయాలి." if is_te else "Steady lifestyle; manage expenses prudently."
        else:
            t2_status = status_labels["caution"].get(lang_code, "Caution")
            t2_pred = "ప్రయాణాలలో జాగ్రత్త, శారీరక అలసట, వివాదాలకు దూరంగా ఉండటం శ్రేయస్కరం." if is_te else "Travel vigilance, physical fatigue; avoid controversies."

        # T3 Assessment (0-4)
        if k3 >= 3:
            t3_status = status_labels["excellent"].get(lang_code, "Excellent")
            t3_pred = "సర్వతోముఖాభివృద్ధి, నూతన వస్తు/వాహన లాభం, మానసిక ప్రశాంతత మరియు విజయాలు." if is_te else "All-round prosperity, acquisition of assets/vehicles, profound peace."
        elif k3 == 2:
            t3_status = status_labels["moderate"].get(lang_code, "Moderate")
            t3_pred = "శ్రమకు తగిన ప్రతిఫలం, నిలకడైన పరిస్థితులు, ఆలోచించి నిర్ణయాలు తీసుకోవాలి." if is_te else "Commensurate reward for hard work, maintain thoughtful planning."
        else:
            t3_status = status_labels["caution"].get(lang_code, "Caution")
            t3_pred = "ఆకస్మిక ఖర్చులు, మానసిక ఒత్తిడి, కులదైవ ఆరాధన మరియు నవగ్రహ ప్రార్థన మేలు చేస్తుంది." if is_te else "Sudden expenses, stress; worship of Ishta Devata brings relief."

        # Normalized Overall Composite Score
        norm = (k1 / 7.0 * 0.4) + (k2 / 2.0 * 0.3) + (k3 / 4.0 * 0.3)
        if norm >= 0.65:
            overall_rating = "ఉత్తమం (Highly Favorable)" if is_te else ("உத்தமம் (Highly Favorable)" if lang_code == "tamil" else "Highly Favorable")
            overall_status = "ఈ సంవత్సరంలోని అత్యధిక కాలం శుభప్రదంగా గడుస్తుంది. నూతన కార్యారంభాలు, ఆర్థిక అభివృద్ధి, కుటుంబ సౌఖ్యం సిద్ధిస్తుంది." if is_te else "Most of the year yields favorable results with strong financial progress and domestic happiness."
        elif norm >= 0.45:
            overall_rating = "అనుకూలం (Favorable)" if is_te else ("அனுகூலம் (Favorable)" if lang_code == "tamil" else "Favorable")
            overall_status = "మొత్తం మీద సంవత్సర ఫలితాలు ఆశాజనకంగా ఉంటాయి. మధ్యమ కందాయాలలో జాగ్రత్తలు పాటిస్తే కార్యసిద్ధి లభిస్తుంది." if is_te else "Overall year remains progressive. Prudence during moderate trimesters ensures success."
        elif norm >= 0.30:
            overall_rating = "మధ్యమం (Moderate)" if is_te else ("மத்திமம் (Moderate)" if lang_code == "tamil" else "Moderate")
            overall_status = "సంవత్సరంలో హెచ్చుతగ్గులు ఉంటాయి. ప్రణాళికాబద్ధంగా ముందుకు సాగడం, బడ్జెట్ నియంత్రణ మరియు దైవబలం రక్షిస్తుంది." if is_te else "Fluctuations exist across the seasons. Disciplined budgeting and prayers provide stability."
        else:
            overall_rating = "అప్రమత్తత (Caution)" if is_te else ("கவனம் தேவை (Caution)" if lang_code == "tamil" else "Caution")
            overall_status = "శ్రమ అధికంగా ఉండే కాలం. ముఖ్య నిర్ణయాలలో అనుభవజ్ఞుల సలహాలు తీసుకోవడం, నవగ్రహ శాంతి శ్రేయస్కరం." if is_te else "High diligence needed. Consult elders/experts for key decisions and observe remedial prayers."

        if is_te:
            n_name = nmeta["te"]
            r_names = nmeta["rashis_te"]
        elif lang_code == "english":
            n_name = nmeta["en"]
            r_names = nmeta["rashis_en"]
        else:
            n_name = transliterate_text(nmeta["dev"], lang_code)
            r_names = [transliterate_text(r, lang_code, sanscript.TELUGU) for r in nmeta["rashis_te"]]

        nakshatra_items.append(NakshatraKandayaItem(
            id=nmeta["id"],
            name=n_name,
            rashi_names=r_names,
            trimester_1=TrimesterKandaya(
                name=t1_title,
                months=t1_months,
                score=k1,
                max_score=8,
                status=t1_status,
                prediction=t1_pred
            ),
            trimester_2=TrimesterKandaya(
                name=t2_title,
                months=t2_months,
                score=k2,
                max_score=3,
                status=t2_status,
                prediction=t2_pred
            ),
            trimester_3=TrimesterKandaya(
                name=t3_title,
                months=t3_months,
                score=k3,
                max_score=5,
                status=t3_status,
                prediction=t3_pred
            ),
            overall_status=overall_status,
            overall_rating=overall_rating
        ))

    # Detailed Shastric Explanations
    explanation = {
        "title": "కందదాయ ఫలాల శాస్త్రీయ విజ్ఞానము & గణన పద్ధతి" if is_te else "Shastric Science & Calculation Method of Kandadayam",
        "trimester_system": (
            "సంవత్సరంలోని 12 మాసాలను 4 నెలల చొప్పున 3 కందాయాలుగా విభజిస్తారు:\n"
            "• ప్రథమ కందాయం (మొదటి 4 నెలలు): చైత్రం, వైశాఖం, జ్యేష్ఠం, ఆషాఢం (మొత్తం 8 భాగాలు/శేషం).\n"
            "• ద్వితీయ కందాయం (రెండవ 4 నెలలు): శ్రావణం, భాద్రపదం, ఆశ్వయుజం, కార్తీకం (మొత్తం 3 భాగాలు/శేషం).\n"
            "• తృతీయ కందాయం (మూడవ 4 నెలలు): మార్గశిరం, పుష్యం, మాఘం, ఫాల్గుణం (మొత్తం 5 భాగాలు/శేషం)."
        ) if is_te else (
            "The 12 months of the Vedic lunar year are grouped into 3 canonical trimesters of 4 months each:\n"
            "• 1st Trimester: Chaitra, Vaishakha, Jyeshtha, Ashadha (Modulo 8).\n"
            "• 2nd Trimester: Shravana, Bhadrapada, Ashwayuja, Kartika (Modulo 3).\n"
            "• 3rd Trimester: Margashirsha, Pushya, Magha, Phalguna (Modulo 5)."
        ),
        "rashi_kandadayam_rule": (
            "రాశి కందదాయంలో ఆదాయ-వ్యయాలు (0-14 పాయింట్లు), రాజపూజ్య-అవమానాలు (0-8 పాయింట్లు) ఉంటాయి.\n"
            "• ఆదాయం > వ్యయం అయితే ధనలాభం, మిగులు నిధులు.\n"
            "• వ్యయం > ఆదాయం అయితే ఖర్చులు ఎక్కువ, రుణభారం రాకుండా పొదుపు పాటించాలి.\n"
            "• రాజపూజ్యం > అవమానం అయితే సమాజంలో ఉన్నత గౌరవం, కీర్తి.\n"
            "• అవమానం > రాజపూజ్యం అయితే వివాదాలు, అపవాదులు రాకుండా మితభాషణం, సంయమనం ముఖ్యం."
        ) if is_te else (
            "In Rashi Kandadayam, Income-Expense (0-14) and Honor-Disgrace (0-8) are evaluated:\n"
            "• Income > Expense signifies substantial wealth accumulation and financial surplus.\n"
            "• Expense > Income advises financial caution and avoiding unnecessary debt.\n"
            "• Honor > Disgrace indicates widespread public prestige and accolades.\n"
            "• Disgrace > Honor calls for diplomatic speech and emotional restraint."
        )
    }

    return ComprehensiveKandadayamResponse(
        samvatsara=samvatsara_name,
        year=year,
        language=lang_code,
        explanation=explanation,
        rashis=rashi_items,
        nakshatras=nakshatra_items
    )


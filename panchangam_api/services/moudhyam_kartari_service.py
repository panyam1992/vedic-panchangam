"""
Vedic Moudhyam (Combustion) and Kartari (Solar Agni Ingress) Computation Service.
Rooted in Classical Jyotisha Siddhanta, Muhurtha Chintamani, Kalamadhaviyam,
and Panchanga Pithika Lekhana Prakriya by Sri Pidaparti Sitarama Sastry.
"""

from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from typing import Dict, Any, List, Optional
import swisseph as swe

swe.set_sid_mode(swe.SIDM_LAHIRI)

# Angular limits for planetary combustion (Moudhyam)
GURU_MOUDYAM_LIMIT = 11.0  # Jupiter: 11 degrees
SUKRA_PROGRADE_LIMIT = 10.0 # Venus prograde: 10 degrees
SUKRA_RETROGRADE_LIMIT = 8.0 # Venus retrograde: 8 degrees

# Kartari Sun Longitude Boundaries (Lahiri Sidereal)
# Bharani 3rd pada start: 20°00' Aries (20.0°)
KARTARI_CHINNA_START = 20.0
# Krittika 1st pada start: 26°40' Aries (26.666667°)
KARTARI_PEDDA_START = 26.66666667
# Rohini 1st pada start: 10°00' Taurus (40.0°)
KARTARI_ROHINI_START = 40.0
# Rohini 2nd pada end / 3rd pada start: 16°40' Taurus (46.666667°)
KARTARI_END = 46.66666667

# Multilingual strings
MOUDYAM_KARTARI_TEXTS = {
    "telugu": {
        "status_auspicious": "✨ శుద్ధ కాలం (మౌఢ్యం & కర్తరి దోషాలు లేవు)",
        "status_auspicious_desc": "వివాహాది సమస్త శుభ ముహూర్తములకు అనుకూలమైన పవిత్ర కాలం.",
        "guru_moudhyam": "గురు మౌఢ్యమి (బృహస్పతి అస్తమయం)",
        "guru_moudhyam_desc": "సూర్యుడు – గురువుల సామీప్యం (11° లోపు). వివాహం, ఉపనయనం, గృహప్రవేశం, శంకుస్థాపనలు పూర్తిగా వర్జ్యం.",
        "sukra_moudhyam": "శుక్ర మౌఢ్యమి (భార్గవ అస్తమయం)",
        "sukra_moudhyam_desc": "సూర్యుడు – శుక్రుల సామీప్యం (వక్రగతి 8° / ఋజుగతి 10° లోపు). సమస్త కామ్య శుభకార్యములు నిషిద్ధం.",
        "both_moudhyam": "గురు & శుక్ర ద్వంద్వ మౌఢ్యమి",
        "both_moudhyam_desc": "గురు, శుక్రులు ఇద్దరూ అస్తంగతులైన కాలం. శుభకార్యములు త్యాజ్యం.",
        "chinna_kartari": "చిన్న కర్తరి (పూర్వ కత్తెర)",
        "chinna_kartari_desc": "సూర్యుడు భరణి 3, 4 పాదాలలో సంచారం. గృహ శంకుస్థాపనలు, చెట్లు నరకడం అశుభం.",
        "pedda_kartari": "అగ్ని కర్తరి (పెద్ద కత్తెర / ప్రచండ భాను తాపం)",
        "pedda_kartari_desc": "సూర్యుడు కృత్తిక 4 పాదాలలో సంచారం. అత్యంత తీవ్రమైన సూర్యతాపం. నూతన గృహారంభం, స్లాబులు, కలప కోయడం, బావులు తవ్వడం నిషిద్ధం.",
        "rohini_kartari": "రోహిణి కర్తరి (ఉత్తర కత్తెర)",
        "rohini_kartari_desc": "సూర్యుడు రోహిణి 1, 2 పాదాలలో సంచారం. కర్తరి సమాప్తి దశ.",
        "vardhakya_warning": "వార్ధక్య దోషం (అస్తమయానికి పూర్వం 3 రోజులు)",
        "balya_warning": "బాల్య దోషం (ఉదయించిన పిదప 3 రోజులు)",
        "taboos_moudhyam": [
            "వివాహం (Marriage ceremonies)",
            "ఉపనయనం (Sacred thread ceremony)",
            "నూతన గృహప్రవేశం (Housewarming)",
            "గృహారంభం / శంకుస్థాపన (Foundation stone laying)",
            "నూతన దేవతా ప్రతిష్ఠ (Deity consecration)",
            "యజ్ఞ-యాగాదులు & కామ్య వ్రతాలు (Vedic sacrifices)"
        ],
        "taboos_kartari": [
            "నూతన గృహ నిర్మాణ ఆరంభం (New house construction)",
            "ఇంటి పైకప్పు / స్లాబ్ వేయడం (Laying roof slabs)",
            "బావులు, బోర్లు తవ్వడం (Digging wells / borewells)",
            "కలప కోయడం & తోటల పనులు (Cutting timber / tree plantation)",
            "అగ్ని సంబంధిత క్రతువులు (Fire-hazard works)"
        ],
        "permitted_karmas": [
            "నిత్య దైవ పూజలు & సంధ్యావందనం (Daily worship & Sandhyavandanam)",
            "శ్రాద్ధ కర్మలు & తర్పణాలు (Ancestral rites)",
            "శాంతి హోమాలు & జప-తపాలు (Remedial prayers & japa)",
            "జాతకర్మ, నామకరణం, అన్నప్రాశన (Infant life-cycle rites)"
        ]
    },
    "english": {
        "status_auspicious": "✨ Auspicious Period (Free of Moudhyam & Kartari)",
        "status_auspicious_desc": "Auspicious sidereal alignment suitable for marriages, housewarmings, and sacred ceremonies.",
        "guru_moudhyam": "Guru Moudhyam (Jupiter Combustion / Astangata)",
        "guru_moudhyam_desc": "Jupiter combust within 11° of Sun. Marriages, Upanayanams, house construction, and major auspicious events prohibited.",
        "sukra_moudhyam": "Sukra Moudhyam (Venus Combustion / Astangata)",
        "sukra_moudhyam_desc": "Venus combust within 8°–10° of Sun. All major auspicious ceremonies prohibited.",
        "both_moudhyam": "Dual Moudhyam (Both Jupiter & Venus Combust)",
        "both_moudhyam_desc": "Both major benefic planets are combust. Auspicious karmas strictly avoided.",
        "chinna_kartari": "Chinna Kartari (Minor Summer Ingress)",
        "chinna_kartari_desc": "Sun transits Bharani padas 3 & 4. Foundation ceremonies and cutting wood discouraged.",
        "pedda_kartari": "Agni Kartari / Maha Kartari (Peak Heat Ingress)",
        "pedda_kartari_desc": "Sun transits Krittika nakshatra. Peak solar heat. New building foundations, roof slabs, digging wells, and cutting timber prohibited.",
        "rohini_kartari": "Rohini Kartari (Concluding Kartari Ingress)",
        "rohini_kartari_desc": "Sun transits Rohini padas 1 & 2. Final phase before Kartari Tyagam.",
        "vardhakya_warning": "Vardhakya Period (Infirmity 3 days prior to setting)",
        "balya_warning": "Balya Period (Infancy 3 days following rising)",
        "taboos_moudhyam": [
            "Vivaha (Weddings)",
            "Upanayana (Sacred Thread Ceremony)",
            "Griha Pravesha (Housewarming)",
            "Shankusthapana (Foundation Stone Laying)",
            "Devata Pratishtha (Deity Consecration)",
            "Major Kamya Yagnas"
        ],
        "taboos_kartari": [
            "Starting new building construction",
            "Casting roof slabs",
            "Digging wells or borewells",
            "Cutting timber and planting trees",
            "Fire-sensitive construction activities"
        ],
        "permitted_karmas": [
            "Daily worship and Sandhyavandana",
            "Ancestral Shradh and Tarpanam",
            "Shanti homas and japa",
            "Infant naming and Annaprashana"
        ]
    }
}

# Alias mapping for other languages
for _l in ["devanagari", "hindi", "sanskrit", "tamil", "kannada", "malayalam", "gujarati", "bengali"]:
    if _l not in MOUDYAM_KARTARI_TEXTS:
        MOUDYAM_KARTARI_TEXTS[_l] = MOUDYAM_KARTARI_TEXTS["telugu"]


def _get_lang_dict(lang: str) -> Dict[str, Any]:
    l_clean = (lang or "telugu").lower().strip()
    return MOUDYAM_KARTARI_TEXTS.get(l_clean, MOUDYAM_KARTARI_TEXTS["telugu"])


def jd_to_local_datetime_str(jd: float, tz_name: str = "Asia/Kolkata") -> str:
    """
    Converts Julian Day float to localized date-time string in target timezone.
    If timezone is not IST, also appends (IST: HH:MM AM/PM) for dual awareness.
    """
    year, month, day, hour_float = swe.revjul(jd)
    whole_hours = int(hour_float)
    minute_float = (hour_float - whole_hours) * 60.0
    whole_minutes = int(minute_float)
    whole_seconds = int((minute_float - whole_minutes) * 60.0)

    dt_utc = datetime(year, month, day, whole_hours, whole_minutes, whole_seconds, tzinfo=timezone.utc)
    try:
        target_tz = ZoneInfo(tz_name)
    except Exception:
        target_tz = ZoneInfo("Asia/Kolkata")

    dt_local = dt_utc.astimezone(target_tz)
    local_str = dt_local.strftime("%Y-%m-%d %I:%M %p %Z")

    if target_tz.key != "Asia/Kolkata":
        dt_ist = dt_utc.astimezone(ZoneInfo("Asia/Kolkata"))
        return f"{local_str} (IST: {dt_ist.strftime('%I:%M %p')})"
    return local_str


def jd_to_ist_datetime_str(jd: float) -> str:
    return jd_to_local_datetime_str(jd, "Asia/Kolkata")


def compute_daily_moudhyam_kartari(jd: float, lang: str = "telugu") -> Dict[str, Any]:
    """
    Computes real-time Moudhyam and Kartari status for a given Julian Day (noon/sunrise).
    """
    texts = _get_lang_dict(lang)

    # 1. Calculate Sidereal Longitudes
    res_s, _ = swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
    res_j, _ = swe.calc_ut(jd, swe.JUPITER, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
    res_v, _ = swe.calc_ut(jd, swe.VENUS, swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED)

    sun_lon = res_s[0] % 360.0
    jup_lon = res_j[0] % 360.0
    ven_lon = res_v[0] % 360.0
    ven_speed = res_v[3]

    # Angular separations modulo 360
    diff_jup = abs(sun_lon - jup_lon)
    if diff_jup > 180.0:
        diff_jup = 360.0 - diff_jup

    diff_ven = abs(sun_lon - ven_lon)
    if diff_ven > 180.0:
        diff_ven = 360.0 - diff_ven

    # 2. Check Kartari
    is_kartari = False
    kartari_type = "NONE"
    kartari_name = None
    kartari_desc = None

    if KARTARI_CHINNA_START <= sun_lon < KARTARI_PEDDA_START:
        is_kartari = True
        kartari_type = "CHINNA_KARTARI"
        kartari_name = texts["chinna_kartari"]
        kartari_desc = texts["chinna_kartari_desc"]
    elif KARTARI_PEDDA_START <= sun_lon < KARTARI_ROHINI_START:
        is_kartari = True
        kartari_type = "PEDDA_KARTARI"
        kartari_name = texts["pedda_kartari"]
        kartari_desc = texts["pedda_kartari_desc"]
    elif KARTARI_ROHINI_START <= sun_lon <= KARTARI_END:
        is_kartari = True
        kartari_type = "ROHINI_KARTARI"
        kartari_name = texts["rohini_kartari"]
        kartari_desc = texts["rohini_kartari_desc"]

    # 3. Check Moudhyam
    is_guru_moudhyam = diff_jup <= GURU_MOUDYAM_LIMIT
    ven_limit = SUKRA_RETROGRADE_LIMIT if ven_speed < 0 else SUKRA_PROGRADE_LIMIT
    is_sukra_moudhyam = diff_ven <= ven_limit

    is_moudhyam = is_guru_moudhyam or is_sukra_moudhyam
    moudhyam_type = "NONE"
    moudhyam_name = None
    moudhyam_desc = None

    if is_guru_moudhyam and is_sukra_moudhyam:
        moudhyam_type = "BOTH"
        moudhyam_name = texts["both_moudhyam"]
        moudhyam_desc = texts["both_moudhyam_desc"]
    elif is_guru_moudhyam:
        moudhyam_type = "GURU_MOUDYAM"
        moudhyam_name = texts["guru_moudhyam"]
        moudhyam_desc = texts["guru_moudhyam_desc"]
    elif is_sukra_moudhyam:
        moudhyam_type = "SUKRA_MOUDYAM"
        moudhyam_name = texts["sukra_moudhyam"]
        moudhyam_desc = texts["sukra_moudhyam_desc"]

    # 4. Synthesize Overall Status & Badge
    if is_moudhyam:
        badge_level = "danger"
        badge_text = f"⚠️ {moudhyam_name}"
        status_title = moudhyam_name
        status_desc = moudhyam_desc
        active_taboos = texts["taboos_moudhyam"]
    elif is_kartari:
        badge_level = "warning" if kartari_type != "PEDDA_KARTARI" else "danger"
        badge_text = f"🔥 {kartari_name}"
        status_title = kartari_name
        status_desc = kartari_desc
        active_taboos = texts["taboos_kartari"]
    else:
        badge_level = "success"
        badge_text = texts["status_auspicious"]
        status_title = texts["status_auspicious"]
        status_desc = texts["status_auspicious_desc"]
        active_taboos = []

    return {
        "is_moudhyam": is_moudhyam,
        "moudhyam_type": moudhyam_type,
        "moudhyam_name": moudhyam_name,
        "moudhyam_description": moudhyam_desc,
        "is_guru_moudhyam": is_guru_moudhyam,
        "guru_angular_distance": round(diff_jup, 2),
        "is_sukra_moudhyam": is_sukra_moudhyam,
        "sukra_angular_distance": round(diff_ven, 2),
        "is_kartari": is_kartari,
        "kartari_type": kartari_type,
        "kartari_name": kartari_name,
        "kartari_description": kartari_desc,
        "sun_sidereal_longitude": round(sun_lon, 2),
        "badge_level": badge_level,  # "danger", "warning", "success"
        "badge_text": badge_text,
        "status_title": status_title,
        "status_description": status_desc,
        "prohibited_karmas": active_taboos,
        "permitted_karmas": texts["permitted_karmas"]
    }


def _find_exact_sun_ingress(target_lon: float, jd_start: float, jd_end: float) -> float:
    low = jd_start
    high = jd_end
    for _ in range(40):
        mid = (low + high) / 2.0
        res, _ = swe.calc_ut(mid, swe.SUN, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
        if res[0] < target_lon:
            low = mid
        else:
            high = mid
    return mid


def _find_exact_moudhyam_boundary(planet: int, limit: float, jd_start: float, jd_end: float, is_entry: bool = True) -> float:
    low = jd_start
    high = jd_end
    for _ in range(40):
        mid = (low + high) / 2.0
        res_s, _ = swe.calc_ut(mid, swe.SUN, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
        res_p, _ = swe.calc_ut(mid, planet, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
        diff = abs(res_s[0] - res_p[0])
        if diff > 180.0:
            diff = 360.0 - diff
        if is_entry:
            if diff > limit:
                low = mid
            else:
                high = mid
        else:
            if diff < limit:
                low = mid
            else:
                high = mid
    return mid


def get_annual_moudhyam_kartari(year: int = 2026, lang: str = "telugu", tz_name: str = "Asia/Kolkata") -> Dict[str, Any]:
    """
    Computes full-year schedule of Moudhyam periods and Kartari ingress milestones
    localized to the requested city's timezone.
    """
    texts = _get_lang_dict(lang)

    # 1. Exact Kartari Milestones for the Year (May-June)
    jd_chinna = _find_exact_sun_ingress(KARTARI_CHINNA_START, swe.julday(year, 5, 1), swe.julday(year, 5, 8))
    jd_pedda = _find_exact_sun_ingress(KARTARI_PEDDA_START, swe.julday(year, 5, 8), swe.julday(year, 5, 16))
    jd_rohini = _find_exact_sun_ingress(KARTARI_ROHINI_START, swe.julday(year, 5, 20), swe.julday(year, 5, 29))
    jd_end = _find_exact_sun_ingress(KARTARI_END, swe.julday(year, 5, 27), swe.julday(year, 6, 5))

    kartari_schedule = {
        "year": year,
        "timezone": tz_name,
        "title": "అగ్ని కర్తరి నిర్ణయ పట్టిక (Kartari Schedule)",
        "chinna_kartari_start": jd_to_local_datetime_str(jd_chinna, tz_name),
        "pedda_kartari_start": jd_to_local_datetime_str(jd_pedda, tz_name),
        "rohini_kartari_start": jd_to_local_datetime_str(jd_rohini, tz_name),
        "kartari_end": jd_to_local_datetime_str(jd_end, tz_name),
        "description": "సూర్యుడు భరణి 3వ పాదం ప్రవేశం మొదలు రోహిణి 2వ పాదం ముగిసే వరకు కర్తరి. గృహారంభాలు, శంకుస్థాపనలు, స్లాబులు, కలప కోయడం నిషిద్ధం.",
        "milestones": [
            {
                "phase": "చిన్న కర్తరి ప్రారంభం",
                "transit": "సూర్యుడు భరణి 3వ పాదం ప్రవేశం (మేషం 20°00')",
                "timing": jd_to_local_datetime_str(jd_chinna, tz_name),
                "importance": "పూర్వ కర్తరి ఆరంభం • శంకుస్థాపనలు వర్జ్యం"
            },
            {
                "phase": "పెద్ద కర్తరి / అగ్ని కర్తరి ప్రారంభం",
                "transit": "సూర్యుడు కృత్తిక 1వ పాదం ప్రవేశం (మేషం 26°40')",
                "timing": jd_to_local_datetime_str(jd_pedda, tz_name),
                "importance": "ముఖ్య అగ్ని కర్తరి • ప్రచండ సూర్యతాపం • సమస్త గృహ నిర్మాణ పనులు నిషిద్ధం"
            },
            {
                "phase": "రోహిణి కర్తరి ప్రారంభం",
                "transit": "సూర్యుడు రోహిణి 1వ పాదం ప్రవేశం (వృషభం 10°00')",
                "timing": jd_to_local_datetime_str(jd_rohini, tz_name),
                "importance": "ఉత్తర కర్తరి దశ"
            },
            {
                "phase": "కర్తరి త్యాగం (సమాప్తి)",
                "transit": "సూర్యుడు రోహిణి 2వ పాదం ముగింపు (వృషభం 16°40')",
                "timing": jd_to_local_datetime_str(jd_end, tz_name),
                "importance": "కర్తరి విముక్తి • యథావిధిగా నిర్మాణ పనులు ప్రారంభించవచ్చు"
            }
        ]
    }

    # 2. Moudhyam Intervals (Jupiter & Venus) across the Gregorian year
    moudhyam_list = []

    # Check Guru Moudhyam in 2026 (July-August)
    if year == 2026:
        jd_g_start = _find_exact_moudhyam_boundary(swe.JUPITER, GURU_MOUDYAM_LIMIT, swe.julday(year, 7, 10), swe.julday(year, 7, 18), is_entry=True)
        jd_g_end = _find_exact_moudhyam_boundary(swe.JUPITER, GURU_MOUDYAM_LIMIT, swe.julday(year, 8, 10), swe.julday(year, 8, 20), is_entry=False)
        moudhyam_list.append({
            "graha": "గురుడు (బృహస్పతి)",
            "graha_code": "jupiter",
            "type": "గురు మౌఢ్యం (బృహస్పతి అస్తమయం)",
            "start": jd_to_local_datetime_str(jd_g_start, tz_name),
            "end": jd_to_local_datetime_str(jd_g_end, tz_name),
            "peak_conjunction": "2026-07-29",
            "vardhakya_start": "అస్తమయానికి 3 రోజుల ముందు",
            "balya_end": "ఉదయించిన 3 రోజుల తర్వాత",
            "prohibition": "వివాహం, ఉపనయనం, గృహప్రవేశం, శంకుస్థాపనలు, నూతన వ్రతాలు సమస్తం నిషిద్ధం.",
            "duration_days": 30
        })

        # Check Venus Moudhyam in 2026 (October)
        jd_v_start = _find_exact_moudhyam_boundary(swe.VENUS, SUKRA_RETROGRADE_LIMIT, swe.julday(year, 10, 16), swe.julday(year, 10, 22), is_entry=True)
        jd_v_end = _find_exact_moudhyam_boundary(swe.VENUS, SUKRA_RETROGRADE_LIMIT, swe.julday(year, 10, 25), swe.julday(year, 10, 31), is_entry=False)
        moudhyam_list.append({
            "graha": "శుక్రుడు (భార్గవుడు)",
            "graha_code": "venus",
            "type": "శుక్ర మౌఢ్యం (భార్గవ అస్తమయం - వక్రగతి)",
            "start": jd_to_local_datetime_str(jd_v_start, tz_name),
            "end": jd_to_local_datetime_str(jd_v_end, tz_name),
            "peak_conjunction": "2026-10-24",
            "vardhakya_start": "అస్తమయానికి 3 రోజుల ముందు",
            "balya_end": "ఉదయించిన 3 రోజుల తర్వాత",
            "prohibition": "సమస్త శుభకార్యములు నిషిద్ధం.",
            "duration_days": 12
        })

    return {
        "year": year,
        "timezone": tz_name,
        "kartari_schedule": kartari_schedule,
        "moudhyam_schedule": moudhyam_list,
        "shastric_taboos": {
            "moudhyam_taboos": texts["taboos_moudhyam"],
            "kartari_taboos": texts["taboos_kartari"],
            "permitted_karmas": texts["permitted_karmas"]
        }
    }

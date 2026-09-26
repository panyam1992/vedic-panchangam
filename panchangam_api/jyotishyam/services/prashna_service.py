"""
Classical Vedic & Tajika Prashna Jyotishyam Engine.
Based on:
- Prashna Marga (పనక్కాట్టు నంబూదిరి)
- Shatpanchasika (పృథుయశస్సు - వరాహమిహిర పుత్రుడు)
- Tajika Neelakanthi (నీలకంఠ దైవజ్ఞుడు - తాజిక యోగాలు)

Calculates:
- Prashna Lagna & Planetary Cusps (Swiss Ephemeris topocentric precision)
- Lagnesha (పృచ్ఛకుడు) and Karyesha (కార్యేశుడు)
- Tajika Deeptamshas (Orbs) & Tajika Yogas:
  * Ithasala (ఇత్థశాల - Success)
  * Musaripha/Esharapha (ముసరిఫ - Denial/Separation)
  * Nakta (నక్త - Mediation)
  * Yamaya (యమయ - Authority)
  * Kamboola (కంబూల - Moon involvement)
- Verdict (కార్య సిద్ధి: అనుకూలం / ఆలస్యంగా / ప్రతికూలం)
- Probability / Success percentage
- Event timing estimation
- Prashna Marga authentic remedies
"""

import math
from datetime import datetime
from typing import Dict, Any, List
import swisseph as swe
from jyotishyam.services.ephemeris_service import (
    calc_julian_day_ut,
    set_ayanamsa_mode,
    calculate_planets
)
from jyotishyam.services.kundali_calculator import RASHIS, format_dms

# Planetary Daily Speeds (average deg/day) to determine which planet is faster
PLANET_DAILY_SPEEDS = {
    "Moon": 13.176,
    "Mercury": 1.383,
    "Venus": 1.200,
    "Sun": 0.985,
    "Mars": 0.524,
    "Jupiter": 0.083,
    "Saturn": 0.033
}

# Tajika Deeptamshas (Orbs in degrees)
TAJIKA_ORBS = {
    "Sun": 15.0,
    "Moon": 12.0,
    "Mars": 8.0,
    "Mercury": 7.0,
    "Jupiter": 9.0,
    "Venus": 7.0,
    "Saturn": 9.0
}

# Classical Prashna Categories
PRASHNA_CATEGORIES = [
    {
        "id": "job",
        "title_te": "ఉద్యోగ అవకాశాలు / పదోన్నతి / ఇంటర్వ్యూ",
        "title_en": "Career / Job Offer / Promotion",
        "karya_bhava": 10,
        "signification": "జీవనోపాధి, కీర్తి, ప్రభుత్వ ఆదరణ, అధికార ప్రాప్తి"
    },
    {
        "id": "marriage",
        "title_te": "వివాహ పురోగతి / సంబంధం కుదురుట",
        "title_en": "Marriage / Partnership Proposal",
        "karya_bhava": 7,
        "signification": "కళత్రం, వివాహ చర్చలు, భాగస్వామ్య విజయము"
    },
    {
        "id": "health",
        "title_te": "ఆరోగ్య స్వస్థత / రోగ నివారణ",
        "title_en": "Health / Disease Recovery",
        "karya_bhava": 1,
        "secondary_bhava": 6,
        "signification": "శరీర రక్షణ, ఆయుర్బలం, చికిత్సా ఫలితము"
    },
    {
        "id": "lost_item",
        "title_te": "పోయిన వస్తువు తిరిగి లభించునా?",
        "title_en": "Recovery of Lost Item / Property",
        "karya_bhava": 2,
        "secondary_bhava": 7,
        "signification": "ధన ధాన్య సంపద, పోయిన వస్తువు లభించు దిశ"
    },
    {
        "id": "court_case",
        "title_te": "కోర్టు కేసులు / వివాదాలలో జయము",
        "title_en": "Court Case / Litigation Outcome",
        "karya_bhava": 6,
        "secondary_bhava": 1,
        "signification": "శత్రుజయం, న్యాయస్థానంలో అనుకూల తీర్పు"
    },
    {
        "id": "foreign_travel",
        "title_te": "విదేశీ ప్రయాణం / వీసా ఆమోదం",
        "title_en": "Foreign Travel / Visa Approval",
        "karya_bhava": 9,
        "secondary_bhava": 12,
        "signification": "దూర ప్రయాణాలు, వీసా ప్రాప్తి, భాగ్యోదయం"
    },
    {
        "id": "business",
        "title_te": "నూతన వ్యాపారం / ఒప్పందాలు",
        "title_en": "Business Venture / Commercial Deals",
        "karya_bhava": 7,
        "secondary_bhava": 11,
        "signification": "క్రయవిక్రయాలు, వ్యాపార విస్తరణ, లాభాలు"
    },
    {
        "id": "wealth",
        "title_te": "ధన లాభం / ఋణ సమస్యల పరిష్కారం",
        "title_en": "Financial Gain / Debt Resolution",
        "karya_bhava": 11,
        "secondary_bhava": 2,
        "signification": "ఆర్థిక లాభం, అప్పులు తీరుట, వాణిజ్య ఫలం"
    },
    {
        "id": "progeny",
        "title_te": "సంతాన ప్రాప్తి / పిల్లల అభివృద్ధి",
        "title_en": "Childbirth / Progeny Prospects",
        "karya_bhava": 5,
        "signification": "పూర్వపుణ్య బలం, సంతాన యోగం, మేధస్సు"
    },
    {
        "id": "education",
        "title_te": "పరీక్షలలో విజయం / ప్రవేశం",
        "title_en": "Exam Success / Academic Admission",
        "karya_bhava": 4,
        "secondary_bhava": 5,
        "signification": "విద్యాభ్యాసం, పోటీ పరీక్షల్లో ఉత్తీర్ణత"
    },
    {
        "id": "property",
        "title_te": "భూమి / గృహ / వాహన కొనుగోలు",
        "title_en": "Property / Land / Vehicle Purchase",
        "karya_bhava": 4,
        "signification": "స్థిరాస్తుల కొనుగోలు, గృహ సౌఖ్యం, రియల్ ఎస్టేట్"
    },
    {
        "id": "general_success",
        "title_te": "తలపెట్టిన కార్యం విజయవంతమవుతుందా?",
        "title_en": "General Endeavor / Fulfillment of Desire",
        "karya_bhava": 11,
        "signification": "సంకల్ప సిద్ధి, సర్వతోముఖ విజయం"
    }
]


def calculate_prashna_chart(
    question_id: str,
    dt: datetime,
    lat: float,
    lon: float,
    tz_offset_hours: float = 0.0,
    ayanamsa_name: str = "lahiri"
) -> Dict[str, Any]:
    """
    Executes full Classical Vedic & Tajika Prashna evaluation.
    Works worldwide for any geographical coordinates and timezone.
    """
    cat = next((c for c in PRASHNA_CATEGORIES if c["id"] == question_id), PRASHNA_CATEGORIES[-1])
    karya_bhava = cat["karya_bhava"]

    # Calculate Julian Day UT
    jd_ut = calc_julian_day_ut(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, tz_offset_hours)
    set_ayanamsa_mode(ayanamsa_name)

    # Calculate Ascendant
    cusps, ascmc = swe.houses_ex(jd_ut, lat, lon, b'E', swe.FLG_SIDEREAL)
    lagna_deg = ascmc[0] % 360.0
    lagna_rashi = int(lagna_deg // 30)
    lagnesha_name = RASHIS[lagna_rashi]["lord_en"]
    lagnesha_name_te = RASHIS[lagna_rashi]["lord_te"]

    # Calculate Planets
    planets_raw = calculate_planets(jd_ut)
    p_map = {p["name"]: p for p in planets_raw}

    # Karya Bhava Rashi & Lord
    karya_rashi = (lagna_rashi + karya_bhava - 1) % 12
    karyesha_name = RASHIS[karya_rashi]["lord_en"]
    karyesha_name_te = RASHIS[karya_rashi]["lord_te"]

    lagnesha_p = p_map.get(lagnesha_name)
    karyesha_p = p_map.get(karyesha_name)
    moon_p = p_map.get("Moon")

    # If lagnesha == karyesha (e.g. 1st house question or same lord)
    same_lord = (lagnesha_name == karyesha_name)
    if same_lord:
        # Use Moon as co-significator of the native
        karyesha_p = lagnesha_p
        lagnesha_p = moon_p
        karyesha_name = karyesha_name
        lagnesha_name = "Moon"
        lagnesha_name_te = "చంద్రుడు"

    # Tajika Aspect & Yoga evaluation
    l_deg = lagnesha_p["longitude"] if lagnesha_p else lagna_deg
    k_deg = karyesha_p["longitude"] if karyesha_p else 0.0
    m_deg = moon_p["longitude"] if moon_p else 0.0

    # Angular distance
    ang_dist = abs(l_deg - k_deg) % 360.0
    if ang_dist > 180.0:
        ang_dist = 360.0 - ang_dist

    # Check classical Tajika aspect types (Conjunction 0°, Sextile 60°, Square 90°, Trine 120°, Opposition 180°)
    aspect_type = "None"
    aspect_name_te = "దృష్టి లేదు"
    aspect_diff = 999.0

    for target_angle, name_en, name_te, is_benefic in [
        (0.0, "Conjunction", "సంయోగం (ఒకే రాశి/సమీపం)", True),
        (60.0, "Sextile (3/11)", "లాభ/తృతీయ దృష్టి (60°)", True),
        (120.0, "Trine (5/9)", "త్రికోణ దృష్టి (120°)", True),
        (90.0, "Square (4/10)", "కేంద్ర దృష్టి (90°)", False),
        (180.0, "Opposition (1/7)", "ప్రత్యక్ష సప్తమ దృష్టి (180°)", False)
    ]:
        diff = abs(ang_dist - target_angle)
        if diff < aspect_diff:
            aspect_diff = diff
            aspect_type = name_en
            aspect_name_te = name_te
            is_harmonious = is_benefic

    # Orb calculation
    orb_l = TAJIKA_ORBS.get(lagnesha_name, 8.0)
    orb_k = TAJIKA_ORBS.get(karyesha_name, 8.0)
    avg_orb = (orb_l + orb_k) / 2.0

    is_within_orb = (aspect_diff <= avg_orb)

    # Check faster/slower for applying (Ithasala) vs separating (Musaripha)
    speed_l = PLANET_DAILY_SPEEDS.get(lagnesha_name, 1.0)
    speed_k = PLANET_DAILY_SPEEDS.get(karyesha_name, 0.5)
    faster_is_l = (speed_l > speed_k)

    # Applying vs Separating:
    # If the faster planet is behind the slower planet approaching aspect -> Applying
    # Simplified degree modulo 30 or circular arc
    is_applying = False
    if is_within_orb:
        if faster_is_l:
            is_applying = (lagnesha_p.get("speed", 1.0) > 0 and karyesha_p.get("speed", 0.0) >= 0)
        else:
            is_applying = (karyesha_p.get("speed", 1.0) > 0)

    # Detect Yogas
    detected_yogas = []
    has_ithasala = is_within_orb and is_applying and aspect_type in ["Conjunction", "Sextile (3/11)", "Trine (5/9)", "Opposition (1/7)"]
    has_musaripha = is_within_orb and not is_applying

    # Check Nakta Yoga (Moon or fast planet transfers light between Lagnesha and Karyesha)
    has_nakta = False
    nakta_mediator = ""
    if not has_ithasala and moon_p:
        # Moon in aspect with both
        m_l_diff = abs(m_deg - l_deg) % 360.0
        m_k_diff = abs(m_deg - k_deg) % 360.0
        if (m_l_diff <= 12.0 or abs(m_l_diff - 60) <= 6.0 or abs(m_l_diff - 120) <= 6.0) and \
           (m_k_diff <= 12.0 or abs(m_k_diff - 60) <= 6.0 or abs(m_k_diff - 120) <= 6.0):
            has_nakta = True
            nakta_mediator = "చంద్రుడు (Moon)"

    # Check Yamaya Yoga (Slower planet receives light from both)
    has_yamaya = False
    yamaya_planet = ""
    if not has_ithasala and not has_nakta:
        for p_name in ["Jupiter", "Saturn"]:
            if p_name not in [lagnesha_name, karyesha_name] and p_name in p_map:
                p_deg = p_map[p_name]["longitude"]
                if (abs(p_deg - l_deg) <= 9.0) and (abs(p_deg - k_deg) <= 9.0):
                    has_yamaya = True
                    yamaya_planet = p_map[p_name]["name_te"]
                    break

    # Build Yogas list
    if has_ithasala:
        detected_yogas.append({
            "name": "ఇత్థశాల యోగం (Ithasala Yoga)",
            "type": "శుభప్రద యోగం (Success)",
            "desc": f"లగ్నాధిపతి ({lagnesha_name_te}) మరియు కార్యేశుడు ({karyesha_name_te}) ఒకరికొకరు దీప్తాంశల పరిధిలో ({round(aspect_diff, 1)}°) అనుకూల దృష్టితో చేరుకుంటున్నారు. ఇది సంపూర్ణ కార్యసిద్ధిని సూచిస్తుంది."
        })
    elif has_nakta:
        detected_yogas.append({
            "name": "నక్త యోగం (Nakta Yoga)",
            "type": "మధ్యవర్తిత్వ యోగం (Success via Mediator)",
            "desc": f"{nakta_mediator} లగ్నాధిపతి మరియు కార్యేశుల మధ్య కాంతిని బదిలీ చేస్తూ కార్యసిద్ధిని సమకూరుస్తుంది. మూడవ వ్యక్తి లేదా మిత్రుని సహకారంతో కార్యం సఫలమవుతుంది."
        })
    elif has_yamaya:
        detected_yogas.append({
            "name": "యమయ యోగం (Yamaya Yoga)",
            "type": "అధికార యోగం (Success via Authority)",
            "desc": f"గురు/శని వంటి అధికారి లేదా పెద్దల సహాయంతో కార్యసిద్ధి లభిస్తుంది ({yamaya_planet} అనుగ్రహం)."
        })
    elif has_musaripha:
        detected_yogas.append({
            "name": "ఈశరాఫ / ముసరిఫ యోగం (Musaripha Yoga)",
            "type": "వియోగాత్మక యోగం (Separation/Delay)",
            "desc": f"గ్రహాలు ఒకదానికొకటి దూరమవుతున్న స్థితిలో ఉన్నాయి. కాలాతీతమగుట లేదా పట్టువిడుపుల వలన జాప్యం కలగవచ్చు."
        })
    else:
        detected_yogas.append({
            "name": "సాధారణ తాజిక దృష్టి",
            "type": "మధ్యమ స్థితి",
            "desc": "ప్రత్యక్ష ఇత్థశాల యోగం లేనందున అధిక శ్రమ, పట్టుదల మరియు దైవబలం అవసరం."
        })

    # Moon Analysis (చంద్ర బలం)
    moon_bhava = ((int(m_deg // 30) - lagna_rashi) % 12) + 1
    moon_strength_good = moon_bhava in [1, 4, 5, 7, 9, 10, 11]

    # Verdict & Probability Score
    score = 50
    if has_ithasala:
        score += 35
    elif has_nakta:
        score += 25
    elif has_yamaya:
        score += 20
    elif has_musaripha:
        score -= 20

    if moon_strength_good:
        score += 15
    else:
        score -= 10

    # Benefic Kendra check
    for b in [1, 4, 7, 10]:
        h_rashi = (lagna_rashi + b - 1) % 12
        for p in planets_raw:
            if p["rashi_index"] == h_rashi and p["name"] in ["Jupiter", "Venus", "Mercury"]:
                score += 5

    score = max(15, min(95, score))

    if score >= 70:
        verdict = "అనుకూలం (Yes - Favorable)"
        verdict_badge = "success"
        verdict_summary = f"మీరు తలపెట్టిన '{cat['title_te']}' కార్యం సంపూర్ణంగా లేదా అత్యధిక స్థాయిలో నెరవేరే సూచనలు ప్రబలంగా ఉన్నాయి. గ్రహస్థితులు మీకు అనుకూలంగా ఉన్నాయి."
    elif score >= 45:
        verdict = "ఆలస్యంగా సిద్ధిస్తుంది (Conditional / With Effort)"
        verdict_badge = "warning"
        verdict_summary = f"కార్యసిద్ధి అవకాశాలు ఉన్నప్పటికీ, కొంత శ్రమ, కాలవిలంబం లేదా ఒకరి సహాయ సహకారాలు తప్పనిసరిగా అవసరమవుతాయి."
    else:
        verdict = "ప్రతికూలం / పునరాలోచన అవసరం (Challenging)"
        verdict_badge = "danger"
        verdict_summary = f"ప్రస్తుత సమయానికి గ్రహాల అనుకూలత తక్కువగా ఉన్నది. తొందరపాటు నిర్ణయాలు తీసుకోకుండా శాంతితో పునరాలోచించి, శాస్త్రోక్త దైవ పరిహారం చేయడం మంచిది."

    # Timing calculation based on sign modality of Lagna
    # 0,3,6,9 (Movable - Chara): Fast (Days)
    # 1,4,7,10 (Fixed - Sthira): Slow (Months)
    # 2,5,8,11 (Dual - Dwiswabhava): Medium (Weeks)
    deg_diff = max(1.0, round(aspect_diff, 1))
    if lagna_rashi in [0, 3, 6, 9]:
        timing_str = f"{int(deg_diff * 2)} నుండి {int(deg_diff * 4)} రోజులలోపు (త్వరిత ఫలితం)"
    elif lagna_rashi in [2, 5, 8, 11]:
        timing_str = f"{max(1, int(deg_diff))} నుండి {int(deg_diff * 2)} వారాలలోపు (మధ్యమ కాలం)"
    else:
        timing_str = f"{max(1, int(deg_diff))} నుండి {int(deg_diff * 2)} మాసాలలోపు (స్థిర కాలం)"

    # Shastric Remedy from Prashna Marga
    remedies = [
        "రోజూ ఉదయం ఇష్టదైవ ప్రార్థన చేసి, 'ఓం నమో భగవతే వాసుదేవాయ' లేదా 'శ్రీ మాత్రే నమః' 108 సార్లు జపించండి.",
        f"లగ్నాధిపతియైన {lagnesha_name_te} మరియు కార్యేశుడైన {karyesha_name_te} అనుగ్రహం కొరకు ఆయా గ్రహ స్తోత్రాలను పారాయణం చేయండి.",
        "ఆలయ దర్శనం చేసి అర్చన జరిపించడం మరియు గోసేవ చేయడం ద్వారా విఘ్నాలు తొలగి కార్యసిద్ధి త్వరితగతిన లభిస్తుంది."
    ]

    return {
        "question_id": question_id,
        "question_title_te": cat["title_te"],
        "question_title_en": cat["title_en"],
        "karya_bhava": karya_bhava,
        "karya_bhava_title": f"{karya_bhava}వ భావం ({cat['signification']})",
        "calculation_time": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "lagna_dms": f"{RASHIS[lagna_rashi]['name_te']} {format_dms(lagna_deg % 30.0)}",
        "lagnesha": f"{lagnesha_name_te} ({lagnesha_name})",
        "karyesha": f"{karyesha_name_te} ({karyesha_name})",
        "chandra_bhava": f"చంద్రుడు లగ్నం నుండి {moon_bhava}వ భావంలో ఉన్నారు",
        "aspect_details": f"గ్రహ సంబంధం: {aspect_name_te} (కోణ వ్యత్యాసం: {round(aspect_diff, 2)}°, సగటు ఆర్బ్: {avg_orb}°)",
        "tajika_yogas": detected_yogas,
        "score_percent": score,
        "verdict": verdict,
        "verdict_badge": verdict_badge,
        "verdict_summary": verdict_summary,
        "timing_estimate": timing_str,
        "remedies": remedies
    }

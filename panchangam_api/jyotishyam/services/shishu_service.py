"""
Newborn / Shishu Jatakam (నవశిశు జాతకం) & Comprehensive Infant Doshas Engine.
Covers:
1. Nakshatra Pada Naming Syllables (నామకరణ నామాక్షరాలు - 108 Padas)
2. Balarishta Dosha (బాలారిష్ట దోషం) & Balarishta Bhanga (దోష నివృత్తి)
3. Gandanta Doshas (గండాంత దోషాలు): Nakshatra, Tithi, and Lagna Gandanta
4. Moola & Jyeshtha Nakshatra Doshas (మూల, జ్యేష్ఠ నక్షత్ర దోషాలు)
5. Visha Ghatika Dosha (విష ఘటికా దోషం)
6. Eclipse Birth Dosha (గ్రహణ జనన దోషం)
7. Sankranti Birth Dosha (సంక్రాంతి జనన దోషం)
8. Shastric Shanti Remedies (ఆయుష్య సూక్తం, మృత్యుంజయ జపం, నక్షత్ర శాంతి)
"""

from typing import Dict, Any, List
from datetime import datetime
import swisseph as swe
from jyotishyam.services.ephemeris_service import (
    calc_julian_day_ut,
    set_ayanamsa_mode,
    calculate_planets
)
from jyotishyam.services.kundali_calculator import (
    RASHIS,
    NAKSHATRAS,
    format_dms,
    enrich_lagna_details,
    enrich_planets,
    build_charts
)
from jyotishyam.services.panchangam_calc import calculate_birth_panchangam

# 108 Nakshatra Pada Naming Syllables (నామాక్షరాలు)
NAMING_SYLLABLES = [
    # 0: Ashwini
    ["చూ", "చే", "చో", "లా"],
    # 1: Bharani
    ["లీ", "లూ", "లే", "లో"],
    # 2: Krittika
    ["ఆ", "ఈ", "ఊ", "ఏ"],
    # 3: Rohini
    ["ఓ", "వా", "వీ", "వూ"],
    # 4: Mrigashira
    ["వే", "వో", "కా", "కీ"],
    # 5: Ardra
    ["కూ", "ఘ", "ఙ", "ఛ"],
    # 6: Punarvasu
    ["కే", "కో", "హా", "హీ"],
    # 7: Pushya
    ["హూ", "హే", "హో", "డా"],
    # 8: Aslesha
    ["డీ", "డూ", "డే", "డో"],
    # 9: Magha
    ["మా", "మీ", "మూ", "మే"],
    # 10: Purva Phalguni
    ["మో", "టా", "టీ", "టూ"],
    # 11: Uttara Phalguni
    ["టే", "టో", "పా", "పీ"],
    # 12: Hasta
    ["పూ", "ష", "ణా", "ఠా"],
    # 13: Chitra
    ["పే", "పో", "రా", "రీ"],
    # 14: Swati
    ["రూ", "రే", "రో", "తా"],
    # 15: Vishakha
    ["తీ", "తూ", "తే", "తో"],
    # 16: Anuradha
    ["నా", "నీ", "నూ", "నే"],
    # 17: Jyeshtha
    ["నో", "యా", "యీ", "యూ"],
    # 18: Moola
    ["యే", "యో", "భా", "భీ"],
    # 19: Purvashadha
    ["భూ", "ధా", "ఫా", "ఢా"],
    # 20: Uttarashadha
    ["భే", "భో", "జా", "జీ"],
    # 21: Shravana
    ["ఖీ", "ఖూ", "ఖే", "ఖో"],
    # 22: Dhanishta
    ["గా", "గీ", "గూ", "గే"],
    # 23: Shatabhisha
    ["గో", "సా", "సీ", "సూ"],
    # 24: Purvabhadra
    ["సే", "సో", "దా", "దీ"],
    # 25: Uttarabhadra
    ["దూ", "శ్యా", "ఝా", "దా"],
    # 26: Revati
    ["దే", "దో", "చా", "చీ"]
]

# Visha Ghatikas (starting ghatika out of 60 ghatikas for each nakshatra)
VISHA_GHATIKAS = [
    50, 24, 30, 40, 14, 21, 30, 20, 32, 30, 20, 18, 21, 20, 14, 14, 10, 14, 56, 24, 20, 10, 10, 18, 16, 24, 30
]


def calculate_shishu_jatakam(
    name: str,
    gender: str,
    dt: datetime,
    lat: float,
    lon: float,
    tz_offset_hours: float = 0.0,
    ayanamsa_name: str = "lahiri"
) -> Dict[str, Any]:
    """
    Computes complete Newborn Horoscope with Naming Syllables and
    Comprehensive Shastric Dosha checks.
    """
    # 1. Astronomical Longitudes
    jd_ut = calc_julian_day_ut(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, tz_offset_hours)
    set_ayanamsa_mode(ayanamsa_name)

    cusps, ascmc = swe.houses_ex(jd_ut, lat, lon, b'E', swe.FLG_SIDEREAL)
    lagna_deg = ascmc[0] % 360.0
    lagna_rashi = int(lagna_deg // 30)

    planets_raw = calculate_planets(jd_ut)
    p_map = {p["name"]: p for p in planets_raw}

    moon = p_map.get("Moon", {})
    sun = p_map.get("Sun", {})
    jupiter = p_map.get("Jupiter", {})
    mars = p_map.get("Mars", {})
    saturn = p_map.get("Saturn", {})
    rahu = p_map.get("Rahu", {})
    ketu = p_map.get("Ketu", {})

    moon_lon = moon.get("longitude", 0.0)
    sun_lon = sun.get("longitude", 0.0)

    # Nakshatra and Pada
    nak_span = 360.0 / 27.0
    nak_idx = int(moon_lon / nak_span) % 27
    deg_in_nak = moon_lon % nak_span
    pada_idx = int(deg_in_nak / (nak_span / 4.0)) + 1  # 1 to 4
    moon_rashi = int(moon_lon // 30)

    # 2. Naming Syllables
    nak_syllables = NAMING_SYLLABLES[nak_idx]
    recommended_syllable = nak_syllables[pada_idx - 1]

    # 3. Tithi calculation
    tithi_diff = (moon_lon - sun_lon) % 360.0
    tithi_num = int(tithi_diff / 12.0) + 1  # 1 to 30

    # 4. DOSHA CHECKS

    doshas_found = []
    has_any_dosha = False

    # A. BALARISHTA DOSHA (బాలారిష్ట దోషం)
    # Moon in 6, 8, or 12 from Lagna
    moon_bhava = ((moon_rashi - lagna_rashi) % 12) + 1
    balarishta_reasons = []

    if moon_bhava in [6, 8, 12]:
        balarishta_reasons.append(f"చంద్రుడు లగ్నం నుండి దుఃస్థానమైన {moon_bhava}వ భావంలో ఉన్నారు.")

    # Malefics in Kendras (1, 4, 7, 10)
    kendra_rashis = [(lagna_rashi + k - 1) % 12 for k in [1, 4, 7, 10]]
    malefics_in_kendra = []
    for m_name in ["Mars", "Saturn", "Rahu", "Ketu"]:
        if m_name in p_map and p_map[m_name]["rashi_index"] in kendra_rashis:
            malefics_in_kendra.append(p_map[m_name]["name_te"])

    if len(malefics_in_kendra) >= 2:
        balarishta_reasons.append(f"కేంద్ర స్థానాల్లో పాపగ్రహాలు ({', '.join(malefics_in_kendra)}) స్థితి కలిగి ఉన్నారు.")

    # Balarishta Bhanga (Cancellations)
    bhanga_reasons = []
    # Jupiter in Kendra
    if jupiter and jupiter["rashi_index"] in kendra_rashis:
        bhanga_reasons.append("కేంద్రంలో దేవగురువైన బృహస్పతి (గురుడు) ఉన్నందున సర్వ బాలారిష్టాలు భంగమైనవి (శాస్త్రోక్త మినహాయింపు).")

    # Exalted Lagna Lord
    lagna_lord_name = RASHIS[lagna_rashi]["lord_en"]
    if lagna_lord_name in p_map:
        ll_p = p_map[lagna_lord_name]
        if ll_p.get("dignity_en") == "Exalted":
            bhanga_reasons.append(f"లగ్నాధిపతియైన {ll_p['name_te']} ఉచ్ఛ స్థితిలో ఉన్నందున సంపూర్ణ ఆయుర్దాయ రక్షణ లభించింది.")

    # Bright Moon (Shukla Paksha away from Sun)
    if 90.0 <= tithi_diff <= 270.0:
        bhanga_reasons.append("పూర్ణ చంద్ర బలం (శుక్లపక్ష చంద్రుడు) ఉన్నందున శిశువుకు శారీరక ఆరోగ్యం సిద్ధిస్తుంది.")

    if balarishta_reasons and not bhanga_reasons:
        has_any_dosha = True
        doshas_found.append({
            "name": "బాలారిష్ట దోషం (Balarishta Dosha)",
            "status": "దోషం కలదు (Dosha Present)",
            "badge": "danger",
            "desc": " ".join(balarishta_reasons),
            "remedy": "శిశువు క్షేమం కొరకు ఆయుష్య హోమం, మహా మృత్యుంజయ జపం లేదా రుద్రాభిషేకం జరిపించడం మరియు బాల రక్షా స్తోత్ర పారాయణ శ్రేయస్కరం."
        })
    elif balarishta_reasons and bhanga_reasons:
        doshas_found.append({
            "name": "బాలారిష్ట భంగం / నివృత్తి (Balarishta Cancelled)",
            "status": "దోష భంగం (Exempted)",
            "badge": "success",
            "desc": f"బాలారిష్ట సూచనలు ఉన్నప్పటికీ, {' '.join(bhanga_reasons)} వలన దోషం పూర్తిగా పరిహారమై ఆయుర్దాయం వృద్ధి చెందింది.",
            "remedy": "ఇష్టదైవ దర్శనం మరియు శివార్చన శుభప్రదం."
        })
    else:
        doshas_found.append({
            "name": "బాలారిష్ట రహితం (No Balarishta)",
            "status": "దోష రహితం (Safe)",
            "badge": "success",
            "desc": "చంద్రుడు మరియు కేంద్ర స్థానాలు శుభప్రదంగా ఉన్నందున శిశువుకు ఎటువంటి బాలారిష్ట దోషం లేదు. చక్కని ఆయురారోగ్యాలు కలవు.",
            "remedy": "సాధారణ దైవ ప్రార్థన చాలును."
        })

    # B. GANDANTA DOSHAS (గండాంత దోషాలు)
    # 1. Nakshatra Gandanta: Junction of Water & Fire nakshatras
    # Revati-Ashwini, Aslesha-Magha, Jyeshtha-Moola
    GANDANTA_NAKSHATRAS = {
        0: {"pada": 1, "name": "అశ్విని 1వ పాదం", "impact": "తండ్రికి అరిష్టం లేదా ప్రారంభంలో రుగ్మతలు. జననానంతరం శాంతి జరిగే వరకు తండ్రి ముఖం చూడకూడదని శాస్త్రం."},
        8: {"pada": 4, "name": "ఆశ్లేష 4వ పాదం", "impact": "తల్లికి లేదా అత్తమామలకు కష్టాలు. 27వ రోజు నక్షత్ర శాంతి చేయించడం అత్యవసరం."},
        9: {"pada": 1, "name": "మఖ 1వ పాదం", "impact": "తల్లి లేదా మేనమామలకు ప్రతికూలత. నవగ్రహ శాంతి మరియు గోదానం శ్రేయస్కరం."},
        17: {"pada": 4, "name": "జ్యేష్ఠ 4వ పాదం", "impact": "శిశువు స్వయంగా ఆరోగ్య సమస్యలు లేదా పెద్దన్నకు చికాకులు. జ్యేష్ఠా శాంతి పూజ అవసరం."},
        18: {"pada": 1, "name": "మూల 1వ పాదం (అభుక్త మూల)", "impact": "వంశానికి లేదా తండ్రికి దోషం. అభుక్త మూల శాంతి మరియు సువర్ణ దానం తప్పనిసరి."},
        26: {"pada": 4, "name": "రేవతి 4వ పాదం", "impact": "ధన క్షయం లేదా శిశువు ఆరోగ్యంలో ఒడిదుడుకులు. రేవతీ నక్షత్ర శాంతి చేయించాలి."}
    }

    if nak_idx in GANDANTA_NAKSHATRAS and pada_idx == GANDANTA_NAKSHATRAS[nak_idx]["pada"]:
        has_any_dosha = True
        g_info = GANDANTA_NAKSHATRAS[nak_idx]
        doshas_found.append({
            "name": f"నక్షత్ర గండాంత దోషం ({g_info['name']})",
            "status": "గండాంత దోషం కలదు",
            "badge": "danger",
            "desc": f"జల-అగ్ని రాశుల సంధి నక్షత్రమైన {g_info['name']} లో జన్మించడం వల్ల గండాంతం ఏర్పడింది. {g_info['impact']}",
            "remedy": "27వ రోజు లేదా అదే నక్షత్రం వచ్చిన రోజున వేద పండితులచే నక్షత్ర శాంతి, కలశ స్థాపన, మరియు రుద్రాభిషేకం జరిపించండి."
        })

    # 2. Tithi Gandanta (Junction of Purna & Nanda tithis: 5-6, 10-11, 15-1, 30-1)
    tithi_rem = tithi_diff % 12.0
    if tithi_rem < 0.8 or tithi_rem > 11.2:
        if tithi_num in [1, 5, 6, 10, 11, 15, 16, 30]:
            has_any_dosha = True
            doshas_found.append({
                "name": "తిథి గండాంత దోషం (Tithi Gandanta)",
                "status": "తిథి సంధి దోషం కలదు",
                "badge": "warning",
                "desc": f"{tithi_num}వ తిథి సంధికాలంలో (మొదటి లేదా చివరి ఘడియలలో) జననం సంభవించినది.",
                "remedy": "తిథి దేవతారాధన మరియు నవగ్రహ జపం చేయించడం మంచిది."
            })

    # 3. Lagna Gandanta (Last 2 deg of water signs: 3, 7, 11 or first 2 deg of fire signs: 0, 4, 8)
    lagna_in_rashi = lagna_deg % 30.0
    if (lagna_rashi in [3, 7, 11] and lagna_in_rashi >= 28.0) or (lagna_rashi in [0, 4, 8] and lagna_in_rashi <= 2.0):
        has_any_dosha = True
        doshas_found.append({
            "name": "లగ్న గండాంత దోషం (Lagna Gandanta)",
            "status": "లగ్న సంధి దోషం కలదు",
            "badge": "warning",
            "desc": "లగ్నం రాశి సంధిలో (జల-అగ్ని రాశుల మధ్య 2 డిగ్రీలలోపు) ఉన్నది.",
            "remedy": "బ్రాహ్మణ సమారాధన, పంచామృతాభిషేకం మరియు గాయత్రీ హవనం శ్రేయస్కరం."
        })

    # C. MOOLA / JYESHTHA FULL PADA EVALUATION
    if nak_idx == 18:  # Moola
        moola_desc = {
            1: "1వ పాదం: తండ్రికి అరిష్టం (మూల శాంతి తప్పనిసరి)",
            2: "2వ పాదం: తల్లికి దోషం / చికాకులు",
            3: "3వ పాదం: ధన నష్టం లేదా కుటుంబ వ్యయాలు",
            4: "4వ పాదం: వంశాభివృద్ధి, శుభ ఫలితాలు (దోష రహితం)"
        }
        doshas_found.append({
            "name": f"మూల నక్షత్ర పరిశీలన ({pada_idx}వ పాదం)",
            "status": "శాంతి అవసరం" if pada_idx in [1, 2, 3] else "శుభప్రదం",
            "badge": "danger" if pada_idx == 1 else ("warning" if pada_idx in [2, 3] else "success"),
            "desc": moola_desc.get(pada_idx, ""),
            "remedy": "మూల నక్షత్ర జనన శాంతి హోమం మరియు గోదానం నిర్వహించండి."
        })
    elif nak_idx == 17:  # Jyeshtha
        jyeshtha_desc = {
            1: "1వ పాదం: జ్యేష్ఠ సోదరులకు లేదా మేనమామకు ప్రతికూలత",
            2: "2వ పాదం: కనిష్ఠ సోదరులకు ఒడిదుడుకులు",
            3: "3వ పాదం: తల్లికి ఆరోగ్య సమస్యలు",
            4: "4వ పాదం: శిశువు స్వయంగా ఆయురారోగ్య జాగ్రత్తలు అవసరం"
        }
        doshas_found.append({
            "name": f"జ్యేష్ఠ నక్షత్ర పరిశీలన ({pada_idx}వ పాదం)",
            "status": "శాంతి అవసరం",
            "badge": "warning",
            "desc": jyeshtha_desc.get(pada_idx, ""),
            "remedy": "జ్యేష్ఠా శాంతి హోమం మరియు శ్రీ విష్ణు సహస్రనామ పారాయణ ఉత్తమం."
        })

    # D. ECLIPSE BIRTH DOSHA (గ్రహణ జనన దోషం)
    # Sun and Moon close to Rahu or Ketu (within 12 degrees)
    rahu_lon = rahu.get("longitude", 0.0)
    ketu_lon = ketu.get("longitude", 0.0)
    sun_rahu_dist = min(abs(sun_lon - rahu_lon) % 360.0, abs(sun_lon - ketu_lon) % 360.0)
    moon_sun_dist = abs(moon_lon - sun_lon) % 360.0

    if sun_rahu_dist <= 12.0 and (moon_sun_dist <= 12.0 or abs(moon_sun_dist - 180.0) <= 12.0):
        has_any_dosha = True
        doshas_found.append({
            "name": "గ్రహణ జనన దోషం (Eclipse Birth Dosha)",
            "status": "గ్రహణ జననం",
            "badge": "danger",
            "desc": "సూర్య లేదా చంద్ర గ్రహణ సమయంలో లేదా దానికి అత్యంత సమీపంలో జననం జరిగినది.",
            "remedy": "సూర్య/చంద్ర గ్రహణ శాంతి హోమం మరియు బంగారు/వెండి నాగ ప్రతిమ దానం చేయించడం శాస్త్రోక్తం."
        })

    # E. SANKRANTI BIRTH DOSHA (సంక్రాంతి జనన దోషం)
    # Sun at the very beginning of a sign (< 1 degree)
    sun_in_rashi = sun_lon % 30.0
    if sun_in_rashi <= 0.8:
        has_any_dosha = True
        doshas_found.append({
            "name": "సంక్రాంతి జనన దోషం (Sankranti Birth Dosha)",
            "status": "సంక్రమణ కాల జననం",
            "badge": "warning",
            "desc": "సూర్యుడు ఒక రాశి నుండి మరొక రాశిలోకి ప్రవేశించే సంక్రమణ పుణ్యకాలంలో జననం జరిగినది.",
            "remedy": "ఆదిత్య హృదయ స్తోత్ర పారాయణ మరియు సూర్య నమస్కారాలు, గోధుమల దానం శ్రేయస్కరం."
        })

    # Overall Summary
    if has_any_dosha:
        overall_status_te = "శాంతి పరిహారాలు సూచించబడ్డాయి (Shanti Recommended)"
        overall_badge = "warning"
        summary_te = "శిశువు జాతకంలో కొన్ని విశిష్ట నక్షత్ర/తిథి/కాల సంధి దోషాలు ఉన్నందున, శాస్త్రోక్త శాంతి పూజలను సకాలంలో జరిపించడం ద్వారా సంపూర్ణ ఆయురారోగ్యాలు, విద్యాభివృద్ధి చేకూరుతాయి."
    else:
        overall_status_te = "సర్వ శుభకరం • దోష రహితం (Auspicious & Safe)"
        overall_badge = "success"
        summary_te = "శిశువు జాతకంలో ఎటువంటి తీవ్రమైన గండాంత లేదా బాలారిష్ట దోషాలు లేవు. గ్రహ స్థితులు శిశువు దీర్ఘాయుష్షుకు, క్షేమానికి అనుకూలంగా ఉన్నాయి."

    # Panchangam, Tatkala Graha Sampatti, and D1 / D9 Chakras
    lagna_info = enrich_lagna_details(lagna_deg)
    enriched_planets = enrich_planets(planets_raw, lagna_deg)
    d1_chart, d9_chart, chalit_chart = build_charts(lagna_info, enriched_planets)
    birth_panchangam = calculate_birth_panchangam(sun_lon, moon_lon, dt.strftime("%Y-%m-%d"), lagna_info)

    return {
        "name": name,
        "gender": gender,
        "dob_formatted": dt.strftime("%d-%B-%Y, %I:%M %p"),
        "lagna_dms": f"{RASHIS[lagna_rashi]['name_te']} {format_dms(lagna_deg % 30.0)}",
        "lagna_info": lagna_info,
        "nakshatra_name_te": NAKSHATRAS[nak_idx]["name_te"],
        "nakshatra_pada": pada_idx,
        "rashi_name_te": RASHIS[moon_rashi]["name_te"],
        "recommended_naming_syllables": nak_syllables,
        "primary_syllable": recommended_syllable,
        "overall_status_te": overall_status_te,
        "overall_badge": overall_badge,
        "summary_te": summary_te,
        "doshas": doshas_found,
        "protective_remedies": [
            "శిశువు రక్షణ కొరకు రోజూ 'ఓం నమో భగవతే వాసుదేవాయ' లేదా 'శ్రీ మాత్రే నమః' నామస్మరణ చేయండి.",
            "శిశువు ఊయల దగ్గర లేదా గదిలో నెమలి ఈకను లేదా శ్రీకృష్ణుని చిరుచిత్రాన్ని ఉంచడం శుభకరం.",
            "జన్మ నక్షత్రం వచ్చిన ప్రతి నెలా శిశువు పేరిట గోసేవ లేదా పాలు/ఆహార దానం చేయడం దీర్ఘాయుష్షుకు కారణమవుతుంది."
        ],
        "panchangam": birth_panchangam,
        "tatkala_graha_sampatti": enriched_planets,
        "charts": {
            "d1": d1_chart,
            "d9": d9_chart,
            "lagna_rashi_index": lagna_rashi
        }
    }

"""
Kundali calculations: Rashis, Nakshatras, Navamsha (D9), Dignity, Bhavas, and Stree/Purusha highlights.
"""

import math
from typing import Dict, Any, List, Tuple

# 12 Rashis definitions
RASHIS = [
    {"index": 0, "name_en": "Aries", "name_te": "మేషం", "lord_en": "Mars", "lord_te": "కుజుడు", "element": "Fire"},
    {"index": 1, "name_en": "Taurus", "name_te": "వృషభం", "lord_en": "Venus", "lord_te": "శుక్రుడు", "element": "Earth"},
    {"index": 2, "name_en": "Gemini", "name_te": "మిథునం", "lord_en": "Mercury", "lord_te": "బుధుడు", "element": "Air"},
    {"index": 3, "name_en": "Cancer", "name_te": "కర్కాటకం", "lord_en": "Moon", "lord_te": "చంద్రుడు", "element": "Water"},
    {"index": 4, "name_en": "Leo", "name_te": "సింహం", "lord_en": "Sun", "lord_te": "సూర్యుడు", "element": "Fire"},
    {"index": 5, "name_en": "Virgo", "name_te": "కన్య", "lord_en": "Mercury", "lord_te": "బుధుడు", "element": "Earth"},
    {"index": 6, "name_en": "Libra", "name_te": "తుల", "lord_en": "Venus", "lord_te": "శుక్రుడు", "element": "Air"},
    {"index": 7, "name_en": "Scorpio", "name_te": "వృశ్చికం", "lord_en": "Mars", "lord_te": "కుజుడు", "element": "Water"},
    {"index": 8, "name_en": "Sagittarius", "name_te": "ధనుస్సు", "lord_en": "Jupiter", "lord_te": "గురుడు", "element": "Fire"},
    {"index": 9, "name_en": "Capricorn", "name_te": "మకరం", "lord_en": "Saturn", "lord_te": "శని", "element": "Earth"},
    {"index": 10, "name_en": "Aquarius", "name_te": "కుంభం", "lord_en": "Saturn", "lord_te": "శని", "element": "Air"},
    {"index": 11, "name_en": "Pisces", "name_te": "మీనం", "lord_en": "Jupiter", "lord_te": "గురుడు", "element": "Water"},
]

# 27 Nakshatras definitions
NAKSHATRAS = [
    {"index": 0, "name_en": "Ashwini", "name_te": "అశ్విని", "lord": "Ketu", "lord_te": "కేతువు", "gana": "Deva", "nadi": "Aadi"},
    {"index": 1, "name_en": "Bharani", "name_te": "భరణి", "lord": "Venus", "lord_te": "శుక్రుడు", "gana": "Manushya", "nadi": "Madhya"},
    {"index": 2, "name_en": "Krittika", "name_te": "కృత్తిక", "lord": "Sun", "lord_te": "సూర్యుడు", "gana": "Rakshasa", "nadi": "Antya"},
    {"index": 3, "name_en": "Rohini", "name_te": "రోహిణి", "lord": "Moon", "lord_te": "చంద్రుడు", "gana": "Manushya", "nadi": "Antya"},
    {"index": 4, "name_en": "Mrigashira", "name_te": "మృగశిర", "lord": "Mars", "lord_te": "కుజుడు", "gana": "Deva", "nadi": "Madhya"},
    {"index": 5, "name_en": "Ardra", "name_te": "ఆరుద్ర", "lord": "Rahu", "lord_te": "రాహువు", "gana": "Manushya", "nadi": "Aadi"},
    {"index": 6, "name_en": "Punarvasu", "name_te": "పునర్వసు", "lord": "Jupiter", "lord_te": "గురుడు", "gana": "Deva", "nadi": "Aadi"},
    {"index": 7, "name_en": "Pushya", "name_te": "పుష్యమి", "lord": "Saturn", "lord_te": "శని", "gana": "Deva", "nadi": "Madhya"},
    {"index": 8, "name_en": "Ashlesha", "name_te": "ఆశ్లేష", "lord": "Mercury", "lord_te": "బుధుడు", "gana": "Rakshasa", "nadi": "Antya"},
    {"index": 9, "name_en": "Magha", "name_te": "మఖ", "lord": "Ketu", "lord_te": "కేతువు", "gana": "Rakshasa", "nadi": "Antya"},
    {"index": 10, "name_en": "Purva Phalguni", "name_te": "పూర్వఫల్గుణి (పుబ్బ)", "lord": "Venus", "lord_te": "శుక్రుడు", "gana": "Manushya", "nadi": "Madhya"},
    {"index": 11, "name_en": "Uttara Phalguni", "name_te": "ఉత్తరఫల్గుణి (ఉత్తర)", "lord": "Sun", "lord_te": "సూర్యుడు", "gana": "Manushya", "nadi": "Aadi"},
    {"index": 12, "name_en": "Hasta", "name_te": "హస్త", "lord": "Moon", "lord_te": "చంద్రుడు", "gana": "Deva", "nadi": "Aadi"},
    {"index": 13, "name_en": "Chitra", "name_te": "చిత్త", "lord": "Mars", "lord_te": "కుజుడు", "gana": "Rakshasa", "nadi": "Madhya"},
    {"index": 14, "name_en": "Swati", "name_te": "స్వాతి", "lord": "Rahu", "lord_te": "రాహువు", "gana": "Deva", "nadi": "Antya"},
    {"index": 15, "name_en": "Vishakha", "name_te": "విశాఖ", "lord": "Jupiter", "lord_te": "గురుడు", "gana": "Rakshasa", "nadi": "Antya"},
    {"index": 16, "name_en": "Anuradha", "name_te": "అనూరాధ", "lord": "Saturn", "lord_te": "శని", "gana": "Deva", "nadi": "Madhya"},
    {"index": 17, "name_en": "Jyeshtha", "name_te": "జ్యేష్ఠ", "lord": "Mercury", "lord_te": "బుధుడు", "gana": "Rakshasa", "nadi": "Aadi"},
    {"index": 18, "name_en": "Mula", "name_te": "మూల", "lord": "Ketu", "lord_te": "కేతువు", "gana": "Rakshasa", "nadi": "Aadi"},
    {"index": 19, "name_en": "Purva Ashadha", "name_te": "పూర్వాషాఢ", "lord": "Venus", "lord_te": "శుక్రుడు", "gana": "Manushya", "nadi": "Madhya"},
    {"index": 20, "name_en": "Uttara Ashadha", "name_te": "ఉత్తరాషాఢ", "lord": "Sun", "lord_te": "సూర్యుడు", "gana": "Manushya", "nadi": "Antya"},
    {"index": 21, "name_en": "Shravana", "name_te": "శ్రవణం", "lord": "Moon", "lord_te": "చంద్రుడు", "gana": "Deva", "nadi": "Antya"},
    {"index": 22, "name_en": "Dhanishta", "name_te": "ధనిష్ట", "lord": "Mars", "lord_te": "కుజుడు", "gana": "Rakshasa", "nadi": "Madhya"},
    {"index": 23, "name_en": "Shatabhisha", "name_te": "శతభిషం", "lord": "Rahu", "lord_te": "రాహువు", "gana": "Rakshasa", "nadi": "Aadi"},
    {"index": 24, "name_en": "Purva Bhadrapada", "name_te": "పూర్వాభాద్ర", "lord": "Jupiter", "lord_te": "గురుడు", "gana": "Manushya", "nadi": "Aadi"},
    {"index": 25, "name_en": "Uttara Bhadrapada", "name_te": "ఉత్తరాభాద్ర", "lord": "Saturn", "lord_te": "శని", "gana": "Manushya", "nadi": "Madhya"},
    {"index": 26, "name_en": "Revati", "name_te": "రేవతి", "lord": "Mercury", "lord_te": "బుధుడు", "gana": "Deva", "nadi": "Antya"},
]

# Exaltation & Debilitation (degrees)
PLANET_DIGNITY_SPECS = {
    "Sun": {"exalt_sign": 0, "exalt_deg": 10.0, "deb_sign": 6, "own": [4], "moola": 4},
    "Moon": {"exalt_sign": 1, "exalt_deg": 3.0, "deb_sign": 7, "own": [3], "moola": 1},
    "Mars": {"exalt_sign": 9, "exalt_deg": 28.0, "deb_sign": 3, "own": [0, 7], "moola": 0},
    "Mercury": {"exalt_sign": 5, "exalt_deg": 15.0, "deb_sign": 11, "own": [2, 5], "moola": 5},
    "Jupiter": {"exalt_sign": 3, "exalt_deg": 5.0, "deb_sign": 9, "own": [8, 11], "moola": 8},
    "Venus": {"exalt_sign": 11, "exalt_deg": 27.0, "deb_sign": 5, "own": [1, 6], "moola": 6},
    "Saturn": {"exalt_sign": 6, "exalt_deg": 20.0, "deb_sign": 0, "own": [9, 10], "moola": 10},
    "Rahu": {"exalt_sign": 1, "exalt_deg": 20.0, "deb_sign": 7, "own": [10], "moola": 1},  # Parashara: Taurus/Virgo
    "Ketu": {"exalt_sign": 7, "exalt_deg": 20.0, "deb_sign": 1, "own": [7], "moola": 7},
}

# Natural Relationships (Mitra, Shatru, Sama)
PERMANENT_RELATIONSHIPS = {
    "Sun": {"friends": ["Moon", "Mars", "Jupiter"], "enemies": ["Venus", "Saturn"], "neutral": ["Mercury"]},
    "Moon": {"friends": ["Sun", "Mercury"], "enemies": [], "neutral": ["Mars", "Jupiter", "Venus", "Saturn"]},
    "Mars": {"friends": ["Sun", "Moon", "Jupiter"], "enemies": ["Mercury"], "neutral": ["Venus", "Saturn"]},
    "Mercury": {"friends": ["Sun", "Venus"], "enemies": ["Moon"], "neutral": ["Mars", "Jupiter", "Saturn"]},
    "Jupiter": {"friends": ["Sun", "Moon", "Mars"], "enemies": ["Mercury", "Venus"], "neutral": ["Saturn"]},
    "Venus": {"friends": ["Mercury", "Saturn"], "enemies": ["Sun", "Moon"], "neutral": ["Mars", "Jupiter"]},
    "Saturn": {"friends": ["Mercury", "Venus"], "enemies": ["Sun", "Moon", "Mars"], "neutral": ["Jupiter"]},
    "Rahu": {"friends": ["Venus", "Saturn", "Mercury"], "enemies": ["Sun", "Moon", "Mars"], "neutral": ["Jupiter"]},
    "Ketu": {"friends": ["Mars", "Venus", "Saturn"], "enemies": ["Sun", "Moon"], "neutral": ["Mercury", "Jupiter"]},
}


def format_dms(deg: float) -> str:
    """Format degrees to DD° MM' SS" string."""
    d = int(deg)
    rem = (deg - d) * 60.0
    m = int(rem)
    s = int(round((rem - m) * 60.0))
    if s == 60:
        s = 0
        m += 1
    if m == 60:
        m = 0
        d += 1
    return f"{d:02d}° {m:02d}' {s:02d}\""


def get_nakshatra_and_pada(lon: float) -> Tuple[Dict[str, Any], int]:
    """
    Calculate Nakshatra (0-26) and Pada (1-4) from 0-360 degree sidereal longitude.
    Each Nakshatra = 13° 20' = 13.333333°
    Each Pada = 3° 20' = 3.333333°
    """
    nak_span = 360.0 / 27.0  # 13.333333333333334
    pada_span = nak_span / 4.0  # 3.3333333333333335

    nak_idx = int(lon / nak_span) % 27
    pada = int((lon % nak_span) / pada_span) + 1
    if pada > 4:
        pada = 4

    return NAKSHATRAS[nak_idx], pada


def calculate_navamsha(lon: float) -> int:
    """
    Calculate Navamsha (D9) sign index (0-11) from longitude.
    Formula: Total padas passed from 0 deg Aries.
    Total padas = int(lon / (3.3333333333333335))
    Navamsha sign = total_padas % 12
    """
    pada_span = 360.0 / 108.0  # 3° 20'
    pada_num = int(lon / pada_span)
    return pada_num % 12


def determine_dignity(planet_name: str, rashi_idx: int, degree_in_rashi: float) -> Tuple[str, str]:
    """
    Determine dignity of planet in sign:
    Exalted (ఉచ్ఛ), Debilitated (నీచ), Own (స్వక్షేత్ర), Friend (మిత్ర), Enemy (శత్రు), Neutral (సమ)
    """
    specs = PLANET_DIGNITY_SPECS.get(planet_name)
    if not specs:
        return "Neutral", "సమక్షేత్రం"

    # Exalted
    if rashi_idx == specs["exalt_sign"]:
        return "Exalted", "ఉచ్ఛ స్థితి"
    # Debilitated
    if rashi_idx == specs["deb_sign"]:
        return "Debilitated", "నీచ స్థితి"
    # Own sign
    if rashi_idx in specs["own"]:
        if rashi_idx == specs.get("moola"):
            return "Moolatrikona", "మూలత్రికోణం"
        return "Own Sign", "స్వక్షేత్రం"

    # Friendly / Enemy / Neutral based on sign lord
    sign_lord = RASHIS[rashi_idx]["lord_en"]
    rel = PERMANENT_RELATIONSHIPS.get(planet_name, {})
    if sign_lord in rel.get("friends", []):
        return "Friend", "మిత్ర క్షేత్రం"
    elif sign_lord in rel.get("enemies", []):
        return "Enemy", "శత్రు క్షేత్రం"
    else:
        return "Neutral", "సమ క్షేత్రం"


def enrich_lagna_details(lagna_deg: float) -> Dict[str, Any]:
    """Enrich Lagna with rashi, nakshatra, pada, and navamsha."""
    rashi_idx = int(lagna_deg // 30)
    deg_in_rashi = lagna_deg % 30.0
    nak, pada = get_nakshatra_and_pada(lagna_deg)
    nav_idx = calculate_navamsha(lagna_deg)

    return {
        "longitude": lagna_deg,
        "rashi_index": rashi_idx,
        "rashi_name_en": RASHIS[rashi_idx]["name_en"],
        "rashi_name_te": RASHIS[rashi_idx]["name_te"],
        "lord_en": RASHIS[rashi_idx]["lord_en"],
        "lord_te": RASHIS[rashi_idx]["lord_te"],
        "degree_in_rashi": deg_in_rashi,
        "formatted_degree": format_dms(deg_in_rashi),
        "nakshatra_index": nak["index"],
        "nakshatra_name_en": nak["name_en"],
        "nakshatra_name_te": nak["name_te"],
        "nakshatra_lord_te": nak["lord_te"],
        "pada": pada,
        "navamsha_rashi_index": nav_idx,
        "navamsha_rashi_te": RASHIS[nav_idx]["name_te"],
    }


def enrich_planets(planets_raw: List[Dict[str, Any]], lagna_deg: float) -> List[Dict[str, Any]]:
    """Enrich raw planets with rashi, pada, navamsha, dignity, and bhava."""
    enriched = []
    lagna_rashi = int(lagna_deg // 30)

    for p in planets_raw:
        lon = p["longitude"]
        rashi_idx = int(lon // 30)
        deg_in_rashi = lon % 30.0
        nak, pada = get_nakshatra_and_pada(lon)
        nav_idx = calculate_navamsha(lon)
        dig_en, dig_te = determine_dignity(p["name_en"], rashi_idx, deg_in_rashi)

        # Whole sign bhava relative to Lagna (1 to 12)
        bhava_num = ((rashi_idx - lagna_rashi) % 12) + 1

        enriched.append({
            "id": p["id"],
            "name_en": p["name_en"],
            "name_te": p["name_te"],
            "short_name": p["short_name"],
            "symbol": p["symbol"],
            "longitude": lon,
            "rashi_index": rashi_idx,
            "rashi_name_en": RASHIS[rashi_idx]["name_en"],
            "rashi_name_te": RASHIS[rashi_idx]["name_te"],
            "degree_in_rashi": deg_in_rashi,
            "formatted_degree": format_dms(deg_in_rashi),
            "speed": p["speed"],
            "is_retrograde": p["is_retrograde"],
            "is_combust": p["is_combust"],
            "nakshatra_index": nak["index"],
            "nakshatra_name_en": nak["name_en"],
            "nakshatra_name_te": nak["name_te"],
            "pada": pada,
            "navamsha_rashi_index": nav_idx,
            "navamsha_rashi_te": RASHIS[nav_idx]["name_te"],
            "bhava": bhava_num,
            "dignity_en": dig_en,
            "dignity_te": dig_te,
        })

    return enriched


def calculate_bhava_sphuta(lagna_deg: float, planets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Computes 12 Bhava Sphuta (House Cusps) with Arambha (Start), Madhya (Mid Cusp),
    and Anthya (End Cusp), along with occupying planets.
    """
    bhavas = []
    for i in range(12):
        mid = (lagna_deg + (i * 30.0)) % 360.0
        start = (mid - 15.0) % 360.0
        end = (mid + 15.0) % 360.0

        rashi_idx = int(mid // 30)
        start_rashi = int(start // 30)
        end_rashi = int(end // 30)

        # Check which planets fall in this bhava span
        planets_in_bhava = []
        for p in planets:
            p_lon = p["longitude"]
            diff = (p_lon - start) % 360.0
            span = (end - start) % 360.0
            if diff < span:
                planets_in_bhava.append(p["name_te"])

        bhavas.append({
            "bhava_num": i + 1,
            "rashi_index": rashi_idx,
            "rashi_name_te": RASHIS[rashi_idx]["name_te"],
            "rashi_name_en": RASHIS[rashi_idx]["name_en"],
            "lord_te": RASHIS[rashi_idx]["lord_te"],
            "lord_en": RASHIS[rashi_idx]["lord_en"],
            "arambha_deg": start,
            "arambha_formatted": f"{RASHIS[start_rashi]['name_te']} {format_dms(start % 30.0)}",
            "arambha_dms": f"{RASHIS[start_rashi]['name_te']} {format_dms(start % 30.0)}",
            "madhya_deg": mid,
            "madhya_formatted": f"{RASHIS[rashi_idx]['name_te']} {format_dms(mid % 30.0)}",
            "madhya_dms": f"{RASHIS[rashi_idx]['name_te']} {format_dms(mid % 30.0)}",
            "anthya_deg": end,
            "anthya_formatted": f"{RASHIS[end_rashi]['name_te']} {format_dms(end % 30.0)}",
            "anthya_dms": f"{RASHIS[end_rashi]['name_te']} {format_dms(end % 30.0)}",
            "planets": planets_in_bhava,
            "occupants": planets_in_bhava
        })
    return bhavas


def build_charts(
    lagna_info: Dict[str, Any],
    planets: List[Dict[str, Any]],
    bhava_sphuta: List[Dict[str, Any]] = None
) -> Tuple[Dict[int, List[Dict[str, Any]]], Dict[int, List[Dict[str, Any]]], Dict[int, List[Dict[str, Any]]]]:
    """
    Build D1 (Rashi), D9 (Navamsha), and Bhava Chalit grids (0 to 11 -> list of occupants).
    """
    d1 = {i: [] for i in range(12)}
    d9 = {i: [] for i in range(12)}
    chalit = {i: [] for i in range(12)}

    # Add Lagna indicator
    d1[lagna_info["rashi_index"]].append({
        "name_en": "Lagna",
        "name_te": "లగ్నం",
        "short_name": "LAG",
        "is_lagna": True,
        "formatted_degree": lagna_info["formatted_degree"],
    })

    d9[lagna_info["navamsha_rashi_index"]].append({
        "name_en": "Lagna",
        "name_te": "లగ్నం",
        "short_name": "LAG",
        "is_lagna": True,
    })

    chalit[lagna_info["rashi_index"]].append({
        "name_en": "Lagna",
        "name_te": "లగ్నం",
        "short_name": "LAG",
        "is_lagna": True,
        "formatted_degree": lagna_info["formatted_degree"],
    })

    # Add Planets to D1 & D9
    for p in planets:
        d1[p["rashi_index"]].append({
            "name_en": p["name_en"],
            "name_te": p["name_te"],
            "short_name": p["short_name"],
            "symbol": p["symbol"],
            "degree_in_rashi": p["degree_in_rashi"],
            "formatted_degree": p["formatted_degree"],
            "is_retrograde": p["is_retrograde"],
            "is_combust": p["is_combust"],
            "dignity_te": p["dignity_te"],
            "is_lagna": False,
        })

        d9[p["navamsha_rashi_index"]].append({
            "name_en": p["name_en"],
            "name_te": p["name_te"],
            "short_name": p["short_name"],
            "symbol": p["symbol"],
            "is_lagna": False,
        })

    # Add Planets to Bhava Chalit Chart
    if bhava_sphuta:
        for b in bhava_sphuta:
            house_sign = b["rashi_index"]
            for p in planets:
                p_lon = p["longitude"]
                start = b["arambha_deg"]
                end = b["anthya_deg"]
                diff = (p_lon - start) % 360.0
                span = (end - start) % 360.0
                if diff < span:
                    chalit[house_sign].append({
                        "name_en": p["name_en"],
                        "name_te": p["name_te"],
                        "short_name": p["short_name"],
                        "symbol": p["symbol"],
                        "degree_in_rashi": p["degree_in_rashi"],
                        "formatted_degree": p["formatted_degree"],
                        "is_retrograde": p["is_retrograde"],
                        "is_combust": p["is_combust"],
                        "dignity_te": p["dignity_te"],
                        "is_lagna": False,
                    })

    return d1, d9, chalit



def get_gender_specific_highlights(gender: str, lagna_info: Dict[str, Any], planets: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Extract classical Stree Jataka (Female) or Purusha Jataka (Male) highlights.
    Based on Brihat Parasara Hora Sastra & Phaladeepika Stree Jataka chapters.
    """
    planet_map = {p["name_en"]: p for p in planets}
    moon = planet_map.get("Moon")
    guru = planet_map.get("Jupiter")
    shukra = planet_map.get("Venus")
    kuja = planet_map.get("Mars")
    lagna_rashi = lagna_info["rashi_index"]

    # 7th and 8th house lords from Lagna
    seventh_rashi = (lagna_rashi + 6) % 12
    seventh_lord = RASHIS[seventh_rashi]["lord_te"]
    eighth_rashi = (lagna_rashi + 7) % 12
    eighth_lord = RASHIS[eighth_rashi]["lord_te"]

    if gender.lower() == "female":
        # Stree Jataka focuses:
        # 1. Guru (Bhartrukaraka)
        # 2. 8th House (Mangalya Sthana / Saubhagya)
        # 3. 7th House (Pati Sthana / Harmony)
        # 4. Lagna & Moon (Body & Mind, Character)
        return {
            "gender_category": "స్త్రీ జాతకం (Stree Jataka)",
            "primary_significator": "గురుడు (భర్తృ కారకుడు / Husband Significator)",
            "primary_karaka_details": f"గురుడు {guru['rashi_name_te']}లో {guru['bhava']}వ స్థానంలో ఉన్నారు ({guru['dignity_te']}).",
            "mangalya_sthana": f"8వ భావం ({RASHIS[eighth_rashi]['name_te']}), అధిపతి: {eighth_lord}. సౌభాగ్య, దీర్ఘ సుమంగళీ యోగానికి మూలస్తంభం.",
            "kalatra_sthana": f"7వ భావం ({RASHIS[seventh_rashi]['name_te']}), అధిపతి: {seventh_lord}. వైవాహిక జీవితం మరియు భర్త యోగ క్షేమాలు.",
            "chandra_bala": f"చంద్రుడు {moon['rashi_name_te']}లో {moon['bhava']}వ స్థానంలో ఉన్నారు. మనోకారకుడు & దేహసౌఖ్యం.",
            "shastra_focus": "స్త్రీ జాతకంలో గురు బలం, 8వ భావ బలం మరియు నవాంశ (D9) పరిశీలన అత్యంత ప్రాధాన్యమైనవి."
        }
    else:
        # Purusha Jataka focuses:
        # 1. Shukra (Kalatrakaraka)
        # 2. 7th House (Kalatra / Vivaha Sthana)
        # 3. 10th House (Karma Sthana / Career & Prestige)
        # 4. 9th House (Bhagya / Father / Fortune)
        tenth_rashi = (lagna_rashi + 9) % 12
        tenth_lord = RASHIS[tenth_rashi]["lord_te"]
        return {
            "gender_category": "పురుష జాతకం (Purusha Jataka)",
            "primary_significator": "శుక్రుడు (కళత్ర కారకుడు / Wife Significator)",
            "primary_karaka_details": f"శుక్రుడు {shukra['rashi_name_te']}లో {shukra['bhava']}వ స్థానంలో ఉన్నారు ({shukra['dignity_te']}).",
            "kalatra_sthana": f"7వ భావం ({RASHIS[seventh_rashi]['name_te']}), అధిపతి: {seventh_lord}. భార్య, వైవాహిక జీవితం మరియు భాగస్వామ్యం.",
            "karma_sthana": f"10వ భావం ({RASHIS[tenth_rashi]['name_te']}), అధిపతి: {tenth_lord}. ఉద్యోగం, వ్యాపారం, కీర్తి ప్రతిష్టలు.",
            "chandra_bala": f"చంద్రుడు {moon['rashi_name_te']}లో {moon['bhava']}వ స్థానంలో ఉన్నారు.",
            "shastra_focus": "పురుష జాతకంలో 10వ భావం (కర్మ), 9వ భావం (భాగ్యం) మరియు శుక్ర బలం ప్రధానంగా చూడబడతాయి."
        }

"""
Gocharam (Real-time planetary transits) analysis engine.
Compares today's planetary positions against native's Janma Rashi.
Analyzes Sade Sati, Ashtama Shani, Kantaka Shani, and Guru Bala.
"""

from typing import Dict, Any, List
from jyotishyam.services.ephemeris_service import get_current_julian_day_ut, calculate_planet_positions
from jyotishyam.services.kundali_calculator import RASHIS


def analyze_gocharam(janma_rashi_idx: int) -> Dict[str, Any]:
    """Calculate current Gocharam transits relative to Janma Rashi."""
    now_jd = get_current_julian_day_ut()
    current_planets = calculate_planet_positions(now_jd, ayanamsa_name="lahiri")
    curr_map = {p["name_en"]: p for p in current_planets}

    # Transiting Rashi for each planet
    transits = []
    for p in current_planets:
        t_rashi = int(p["longitude"] // 30)
        # House from Moon: 1 to 12
        h_from_moon = ((t_rashi - janma_rashi_idx) % 12) + 1

        transits.append({
            "planet_en": p["name_en"],
            "planet_te": p["name_te"],
            "transit_rashi_idx": t_rashi,
            "transit_rashi_te": RASHIS[t_rashi]["name_te"],
            "house_from_moon": h_from_moon,
            "is_retrograde": p["is_retrograde"],
            "degree": round(p["longitude"] % 30.0, 2),
        })

    # Shani Gochara Analysis
    saturn = curr_map["Saturn"]
    sat_rashi = int(saturn["longitude"] // 30)
    sat_house = ((sat_rashi - janma_rashi_idx) % 12) + 1

    sade_sati_status = "ఏలినాటి శని లేదు (No Sade Sati currently)"
    sade_sati_active = False

    if sat_house == 12:
        sade_sati_status = "ఏలినాటి శని ప్రథమ చరణం (Rising Phase of Sade Sati - 12th house)"
        sade_sati_active = True
    elif sat_house == 1:
        sade_sati_status = "జన్మ శని - ఏలినాటి శని ద్వితీయ చరణం (Peak Phase of Sade Sati - 1st house)"
        sade_sati_active = True
    elif sat_house == 2:
        sade_sati_status = "ఏలినాటి శని తృతీయ చరణం (Setting Phase of Sade Sati - 2nd house)"
        sade_sati_active = True
    elif sat_house == 8:
        sade_sati_status = "అష్టమ శని నడుస్తోంది (Ashtama Shani - 8th house transit)"
        sade_sati_active = True
    elif sat_house == 4:
        sade_sati_status = "అర్థాష్టమ శని నడుస్తోంది (Ardhastama Shani - 4th house transit)"
        sade_sati_active = True
    elif sat_house in [3, 6, 11]:
        sade_sati_status = f"శని గోచారం అత్యంత శుభప్రదం ({sat_house}వ స్థానంలో సంచారం - విజయం & కార్యసిద్ధి)"

    # Guru Gochara Analysis
    jupiter = curr_map["Jupiter"]
    jup_rashi = int(jupiter["longitude"] // 30)
    jup_house = ((jup_rashi - janma_rashi_idx) % 12) + 1

    guru_auspicious = jup_house in [2, 5, 7, 9, 11]
    if guru_auspicious:
        guru_status = f"గురు బలం సంపూర్ణంగా కలదు ({jup_house}వ స్థానంలో సంచారం - శుభకార్యాలు, ధన లాభం, యశస్సు)"
    else:
        guru_status = f"గురు సంచారం సాధారణం ({jup_house}వ స్థానంలో సంచారం - గురు గ్రహ శాంతి/స్తోత్ర పారాయణ శ్రేయస్కరం)"

    # Rahu & Ketu Transits
    rahu = curr_map["Rahu"]
    ketu = curr_map["Ketu"]
    rahu_rashi = int(rahu["longitude"] // 30)
    ketu_rashi = int(ketu["longitude"] // 30)
    rahu_house = ((rahu_rashi - janma_rashi_idx) % 12) + 1
    ketu_house = ((ketu_rashi - janma_rashi_idx) % 12) + 1

    return {
        "janma_rashi_name": RASHIS[janma_rashi_idx]["name_te"],
        "transits": transits,
        "shani_gochara": {
            "house": sat_house,
            "status": sade_sati_status,
            "is_severe": sat_house in [1, 8, 12],
            "transit_rashi": RASHIS[sat_rashi]["name_te"],
        },
        "guru_gochara": {
            "house": jup_house,
            "has_guru_bala": guru_auspicious,
            "status": guru_status,
            "transit_rashi": RASHIS[jup_rashi]["name_te"],
        },
        "rahu_ketu_gochara": {
            "rahu_house": rahu_house,
            "rahu_rashi": RASHIS[rahu_rashi]["name_te"],
            "ketu_house": ketu_house,
            "ketu_rashi": RASHIS[ketu_rashi]["name_te"],
        }
    }

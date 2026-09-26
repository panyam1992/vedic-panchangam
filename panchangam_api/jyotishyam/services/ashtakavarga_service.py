"""
Parashari Ashtakavarga & Sarvashtakavarga (SAV) Calculation Engine.
Calculates BAV (Bhinna Ashtakavarga) for 7 planets (Sun to Saturn)
and aggregates into the standard 337-point Sarvashtakavarga (SAV) chart.
"""

from typing import Dict, Any, List

# Classical Parashari Benefic Houses (1-indexed from each planet)
# Format: [from_Sun, from_Moon, from_Mars, from_Merc, from_Jup, from_Ven, from_Sat, from_Lagna]

SUN_RULES = {
    "Sun": [1, 2, 4, 7, 8, 9, 10, 11],
    "Moon": [3, 6, 10, 11],
    "Mars": [1, 2, 4, 7, 8, 9, 10, 11],
    "Mercury": [3, 5, 6, 9, 10, 11, 12],
    "Jupiter": [5, 6, 9, 11],
    "Venus": [6, 7, 12],
    "Saturn": [1, 2, 4, 7, 8, 9, 10, 11],
    "Lagna": [3, 4, 6, 10, 11, 12]
}

MOON_RULES = {
    "Sun": [3, 6, 7, 8, 10, 11],
    "Moon": [1, 3, 6, 7, 10, 11],
    "Mars": [2, 3, 5, 6, 9, 10, 11],
    "Mercury": [1, 3, 4, 5, 7, 8, 10, 11],
    "Jupiter": [1, 4, 7, 8, 10, 11, 12],
    "Venus": [3, 4, 5, 7, 9, 10, 11],
    "Saturn": [3, 5, 6, 11],
    "Lagna": [3, 6, 10, 11]
}

MARS_RULES = {
    "Sun": [3, 5, 6, 10, 11],
    "Moon": [3, 6, 11],
    "Mars": [1, 2, 4, 7, 8, 10, 11],
    "Mercury": [3, 5, 6, 11],
    "Jupiter": [6, 10, 11, 12],
    "Venus": [6, 8, 11, 12],
    "Saturn": [1, 4, 7, 8, 9, 10, 11],
    "Lagna": [1, 3, 6, 10, 11]
}

MERCURY_RULES = {
    "Sun": [5, 6, 9, 11, 12],
    "Moon": [2, 4, 6, 8, 10, 11],
    "Mars": [1, 2, 4, 7, 8, 9, 10, 11],
    "Mercury": [1, 3, 5, 6, 9, 10, 11, 12],
    "Jupiter": [6, 8, 11, 12],
    "Venus": [1, 2, 3, 4, 5, 8, 9, 11],
    "Saturn": [1, 2, 4, 7, 8, 9, 10, 11],
    "Lagna": [1, 2, 4, 6, 8, 10, 11]
}

JUPITER_RULES = {
    "Sun": [1, 2, 3, 4, 7, 8, 9, 10, 11],
    "Moon": [2, 5, 7, 9, 11],
    "Mars": [1, 2, 4, 7, 8, 10, 11],
    "Mercury": [1, 2, 4, 5, 6, 9, 10, 11],
    "Jupiter": [1, 2, 3, 4, 7, 8, 10, 11],
    "Venus": [2, 5, 6, 9, 10, 11],
    "Saturn": [3, 5, 6, 12],
    "Lagna": [1, 2, 4, 5, 6, 7, 9, 10, 11]
}

VENUS_RULES = {
    "Sun": [8, 11, 12],
    "Moon": [1, 2, 3, 4, 5, 8, 9, 11, 12],
    "Mars": [3, 5, 6, 9, 11, 12],
    "Mercury": [3, 5, 6, 9, 11],
    "Jupiter": [5, 8, 9, 10, 11],
    "Venus": [1, 2, 3, 4, 5, 8, 9, 10, 11],
    "Saturn": [3, 4, 5, 8, 9, 10, 11],
    "Lagna": [1, 2, 3, 4, 5, 8, 9, 11]
}

SATURN_RULES = {
    "Sun": [1, 2, 4, 7, 8, 10, 11],
    "Moon": [3, 6, 11],
    "Mars": [3, 5, 6, 10, 11, 12],
    "Mercury": [6, 8, 9, 10, 11, 12],
    "Jupiter": [5, 6, 11, 12],
    "Venus": [6, 11, 12],
    "Saturn": [3, 5, 6, 11],
    "Lagna": [1, 3, 4, 6, 10, 11]
}

PLANET_RULES = {
    "Sun": SUN_RULES,
    "Moon": MOON_RULES,
    "Mars": MARS_RULES,
    "Mercury": MERCURY_RULES,
    "Jupiter": JUPITER_RULES,
    "Venus": VENUS_RULES,
    "Saturn": SATURN_RULES
}

RASHI_NAMES = [
    {"en": "Aries", "te": "మేషం"},
    {"en": "Taurus", "te": "వృషభం"},
    {"en": "Gemini", "te": "మిథునం"},
    {"en": "Cancer", "te": "కర్కాటకం"},
    {"en": "Leo", "te": "సింహం"},
    {"en": "Virgo", "te": "కన్య"},
    {"en": "Libra", "te": "తుల"},
    {"en": "Scorpio", "te": "వృశ్చికం"},
    {"en": "Sagittarius", "te": "ధనుస్సు"},
    {"en": "Capricorn", "te": "మకరం"},
    {"en": "Aquarius", "te": "కుంభం"},
    {"en": "Pisces", "te": "మీనం"}
]


def calculate_ashtakavarga(planets_data: List[Dict[str, Any]], lagna_idx: int) -> Dict[str, Any]:
    """
    Computes 7 Bhinna Ashtakavargas and the 337-point Sarvashtakavarga.
    """
    # Map planetary sign indices (0-11)
    p_signs = {}
    for p in planets_data:
        en_name = p.get("name_en")
        if en_name in PLANET_RULES:
            p_signs[en_name] = p.get("rashi_index", 0)

    p_signs["Lagna"] = lagna_idx

    # Individual Bhinna Ashtakavarga tables (7 planets x 12 signs)
    bav_tables = {}
    # Sarvashtakavarga 12 signs array
    sav_rashi = [0] * 12

    for target_planet, rule_set in PLANET_RULES.items():
        bav = [0] * 12
        for ref_entity, auspicious_houses in rule_set.items():
            if ref_entity not in p_signs:
                continue
            ref_sign = p_signs[ref_entity]
            for h in auspicious_houses:
                target_sign = (ref_sign + (h - 1)) % 12
                bav[target_sign] += 1
        bav_tables[target_planet] = bav
        for i in range(12):
            sav_rashi[i] += bav[i]

    # Format output for each Rashi
    rashi_summary = []
    for i in range(12):
        pts = sav_rashi[i]
        status_te = "అత్యంత బలమైనది" if pts >= 32 else ("బలమైనది" if pts >= 28 else "సామాన్యమైనది")
        rashi_summary.append({
            "rashi_index": i,
            "rashi_name_te": RASHI_NAMES[i]["te"],
            "rashi_name_en": RASHI_NAMES[i]["en"],
            "points": pts,
            "status_te": status_te,
            "is_strong": pts >= 28
        })

    # Map to 12 Bhavas relative to Lagna
    bhava_summary = []
    for h in range(1, 13):
        sign_idx = (lagna_idx + h - 1) % 12
        pts = sav_rashi[sign_idx]
        bhava_summary.append({
            "bhava_num": h,
            "rashi_index": sign_idx,
            "rashi_name_te": RASHI_NAMES[sign_idx]["te"],
            "points": pts,
            "status_te": "శుభం (Strong)" if pts >= 28 else "మధ్యమం (Average)"
        })

    # Key Astrological Insights
    eleventh_pts = bhava_summary[10]["points"]  # 11th Bhava (Gains)
    twelfth_pts = bhava_summary[11]["points"]   # 12th Bhava (Expenses)
    tenth_pts = bhava_summary[9]["points"]      # 10th Bhava (Career)
    first_pts = bhava_summary[0]["points"]      # 1st Bhava (Self/Health)

    wealth_insight = (
        "11వ లాభ స్థాన బిందువులు 12వ వ్యయ స్థానం కంటే ఎక్కువగా ఉన్నాయి. సంపద ఆదా అవుతుంది, ఆర్థిక స్థిరత్వం ఉంటుంది."
        if eleventh_pts >= twelfth_pts else
        "12వ వ్యయ స్థాన బిందువులు ఎక్కువగా ఉన్నాయి. ఖర్చులపై నియంత్రణ అవసరం, బడ్జెట్ పాటించాలి."
    )

    total_points = sum(sav_rashi)

    return {
        "total_points": total_points,
        "average_points": 28,
        "sarvashtakavarga_rashi": rashi_summary,
        "sarvashtakavarga_bhava": bhava_summary,
        "bav_planets": bav_tables,
        "insights": {
            "wealth_status": wealth_insight,
            "eleventh_points": eleventh_pts,
            "twelfth_points": twelfth_pts,
            "career_points": tenth_pts,
            "lagna_points": first_pts
        }
    }

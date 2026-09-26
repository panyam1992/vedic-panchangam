"""
Vimshottari Dasha calculation engine.
Calculates birth dasha balance, full 120-year cycle, Antardashas (Bhuktis),
and pinpoints current running Mahadasha and Bhukti.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List

# Vimshottari Lord Cycle & Years (Total 120 years)
DASHA_ORDER = [
    {"lord": "Ketu", "lord_te": "కేతువు", "years": 7},
    {"lord": "Venus", "lord_te": "శుక్రుడు", "years": 20},
    {"lord": "Sun", "lord_te": "సూర్యుడు", "years": 6},
    {"lord": "Moon", "lord_te": "చంద్రుడు", "years": 10},
    {"lord": "Mars", "lord_te": "కుజుడు", "years": 7},
    {"lord": "Rahu", "lord_te": "రాహువు", "years": 18},
    {"lord": "Jupiter", "lord_te": "గురుడు", "years": 16},
    {"lord": "Saturn", "lord_te": "శని", "years": 19},
    {"lord": "Mercury", "lord_te": "బుధుడు", "years": 17},
]

DAYS_PER_YEAR = 365.2425


def calculate_vimshottari_dasha(moon_lon: float, dob_str: str) -> Dict[str, Any]:
    """Calculate Vimshottari Dasha timeline and identify active dasha."""
    nak_span = 360.0 / 27.0  # 13.333333333333334 degrees
    nak_index = int(moon_lon / nak_span) % 27

    # Nakshatra lord cycle index (0 to 8)
    first_lord_idx = nak_index % 9
    first_dasha = DASHA_ORDER[first_lord_idx]

    # Arc elapsed in current nakshatra
    arc_in_nak = moon_lon % nak_span
    fraction_elapsed = arc_in_nak / nak_span
    fraction_remaining = 1.0 - fraction_elapsed

    balance_years = first_dasha["years"] * fraction_remaining
    balance_days = int(balance_years * DAYS_PER_YEAR)

    balance_y = int(balance_years)
    balance_m = int((balance_years - balance_y) * 12)
    balance_d = int((balance_years - balance_y - balance_m / 12) * 365.25)

    birth_date = datetime.strptime(dob_str, "%Y-%m-%d")
    now_date = datetime.now()

    # Generate full dasha cycles
    mahadashas = []
    current_start = birth_date

    # 1. First (partial) Mahadasha
    first_end = current_start + timedelta(days=balance_days)
    mahadashas.append({
        "lord": first_dasha["lord"],
        "lord_te": first_dasha["lord_te"],
        "total_years": first_dasha["years"],
        "start_date": current_start.strftime("%Y-%m-%d"),
        "end_date": first_end.strftime("%Y-%m-%d"),
        "is_partial": True,
    })
    current_start = first_end

    # 2. Subsequent Mahadashas up to 120 years
    for step in range(1, 10):
        lord_info = DASHA_ORDER[(first_lord_idx + step) % 9]
        dur_days = int(lord_info["years"] * DAYS_PER_YEAR)
        d_end = current_start + timedelta(days=dur_days)
        mahadashas.append({
            "lord": lord_info["lord"],
            "lord_te": lord_info["lord_te"],
            "total_years": lord_info["years"],
            "start_date": current_start.strftime("%Y-%m-%d"),
            "end_date": d_end.strftime("%Y-%m-%d"),
            "is_partial": False,
        })
        current_start = d_end

    # Determine current running Mahadasha
    current_maha = None
    for md in mahadashas:
        s_dt = datetime.strptime(md["start_date"], "%Y-%m-%d")
        e_dt = datetime.strptime(md["end_date"], "%Y-%m-%d")
        if s_dt <= now_date < e_dt:
            current_maha = md
            break

    if not current_maha and mahadashas:
        current_maha = mahadashas[0]

    # Calculate Antardashas (Bhuktis) for current running Mahadasha
    current_maha_idx = next(i for i, d in enumerate(DASHA_ORDER) if d["lord"] == current_maha["lord"])
    maha_total_years = current_maha["total_years"]
    m_start_dt = datetime.strptime(current_maha["start_date"], "%Y-%m-%d")

    bhuktis = []
    b_curr_start = m_start_dt
    for b_step in range(9):
        b_lord = DASHA_ORDER[(current_maha_idx + b_step) % 9]
        b_years = (maha_total_years * b_lord["years"]) / 120.0
        b_days = int(b_years * DAYS_PER_YEAR)
        b_end = b_curr_start + timedelta(days=b_days)

        is_active = (b_curr_start <= now_date < b_end)
        bhuktis.append({
            "lord": b_lord["lord"],
            "lord_te": b_lord["lord_te"],
            "start_date": b_curr_start.strftime("%Y-%m-%d"),
            "end_date": b_end.strftime("%Y-%m-%d"),
            "is_active": is_active,
        })
        b_curr_start = b_end

    # Current active Bhukti
    current_bhukti = next((b for b in bhuktis if b["is_active"]), bhuktis[0] if bhuktis else None)

    return {
        "birth_balance_text": f"{first_dasha['lord_te']} దశ శేషం: {balance_y} సంవత్సరాల {balance_m} నెలల {balance_d} రోజులు",
        "balance_years": round(balance_years, 2),
        "first_dasha_lord": first_dasha["lord_te"],
        "current_mahadasha": current_maha,
        "current_bhukti": current_bhukti,
        "all_mahadashas": mahadashas,
        "current_bhuktis": bhuktis,
    }

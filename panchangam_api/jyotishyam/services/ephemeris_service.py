"""
Swiss Ephemeris calculation wrapper using pyswisseph.
"""

import os
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Tuple
import swisseph as swe

from jyotishyam.config import EPHEMERIS_DIR, DEFAULT_AYANAMSA

# Initialize Swiss Ephemeris file path if available
if EPHEMERIS_DIR.exists():
    swe.set_ephe_path(str(EPHEMERIS_DIR))

# Swiss Ephemeris Planet Constants
PLANET_IDS = [
    (swe.SUN, "Sun", "సూర్యుడు", "SU", "☉"),
    (swe.MOON, "Moon", "చంద్రుడు", "MO", "☽"),
    (swe.MARS, "Mars", "కుజుడు", "MA", "♂"),
    (swe.MERCURY, "Mercury", "బుధుడు", "ME", "☿"),
    (swe.JUPITER, "Jupiter", "గురుడు", "JU", "♃"),
    (swe.VENUS, "Venus", "శుక్రుడు", "VE", "♀"),
    (swe.SATURN, "Saturn", "శని", "SA", "♄"),
    (swe.TRUE_NODE, "Rahu", "రాహువు", "RA", "☊"),
]

AYANAMSA_MODES = {
    "lahiri": swe.SIDM_LAHIRI,
    "kp": swe.SIDM_KRISHNAMURTI,
    "raman": swe.SIDM_RAMAN,
    "fagan_bradley": swe.SIDM_FAGAN_BRADLEY,
}


def get_julian_day_ut(dob_str: str, tob_str: str, tz_offset_hours: float) -> float:
    """
    Calculate Julian Day UT from date, time, and timezone offset.
    dob_str: 'YYYY-MM-DD'
    tob_str: 'HH:MM' or 'HH:MM:SS'
    tz_offset_hours: e.g. 5.5 for IST
    """
    dt_str = f"{dob_str} {tob_str}"
    formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]
    dt = None
    for fmt in formats:
        try:
            dt = datetime.strptime(dt_str, fmt)
            break
        except ValueError:
            pass
    if dt is None:
        raise ValueError(f"Invalid date/time format: {dob_str} {tob_str}")

    # Convert to decimal hour
    hour_decimal = dt.hour + dt.minute / 60.0 + dt.second / 3600.0
    # Adjust for Timezone to get UT (Universal Time)
    hour_ut = hour_decimal - tz_offset_hours

    # swe.julday calculates julian day
    jd_ut = swe.julday(dt.year, dt.month, dt.day, hour_ut)
    return jd_ut


def calc_julian_day_ut(year: int, month: int, day: int, hour: int = 12, minute: int = 0, second: int = 0, tz_offset_hours: float = 0.0) -> float:
    """Calculate Julian Day UT directly from numeric components."""
    hour_decimal = hour + minute / 60.0 + second / 3600.0 - tz_offset_hours
    return swe.julday(year, month, day, hour_decimal)


def get_current_julian_day_ut() -> float:
    """Get current Julian Day UT for Gocharam (transits)."""
    now_utc = datetime.now(timezone.utc)
    hour_dec = now_utc.hour + now_utc.minute / 60.0 + now_utc.second / 3600.0
    return swe.julday(now_utc.year, now_utc.month, now_utc.day, hour_dec)


def set_ayanamsa_mode(ayanamsa_name: str = "lahiri"):
    """Set the sidereal ayanamsa mode."""
    mode = AYANAMSA_MODES.get(ayanamsa_name.lower(), swe.SIDM_LAHIRI)
    swe.set_sid_mode(mode)


def get_ayanamsa_value(jd_ut: float) -> float:
    """Returns current ayanamsa value in degrees."""
    return swe.get_ayanamsa_ut(jd_ut)


def calculate_planet_positions(jd_ut: float, ayanamsa_name: str = "lahiri") -> List[Dict[str, Any]]:
    """
    Calculate sidereal longitudes and speeds for 9 Vedic planets (Sun through Ketu).
    """
    set_ayanamsa_mode(ayanamsa_name)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

    planets_data = []
    sun_lon = 0.0

    # Calculate 7 main planets + Rahu
    for pid, name_en, name_te, short_name, symbol in PLANET_IDS:
        res = swe.calc_ut(jd_ut, pid, flags)
        lon = res[0][0] % 360.0
        speed = res[0][3]
        is_retrograde = speed < 0.0

        if pid == swe.SUN:
            sun_lon = lon

        planets_data.append({
            "id": pid,
            "name": name_en,
            "name_en": name_en,
            "name_te": name_te,
            "short_name": short_name,
            "symbol": symbol,
            "longitude": lon,
            "rashi_index": int(lon // 30),
            "speed": speed,
            "is_retrograde": is_retrograde,
            "is_combust": False,  # Will evaluate below
        })

    # Add Ketu (always opposite Rahu by 180 degrees)
    rahu_item = next(p for p in planets_data if p["name_en"] == "Rahu")
    ketu_lon = (rahu_item["longitude"] + 180.0) % 360.0
    planets_data.append({
        "id": 100,  # Synthetic ID for Ketu
        "name": "Ketu",
        "name_en": "Ketu",
        "name_te": "కేతువు",
        "short_name": "KE",
        "symbol": "☋",
        "longitude": ketu_lon,
        "rashi_index": int(ketu_lon // 30),
        "speed": rahu_item["speed"],
        "is_retrograde": True,  # Nodes are typically retrograde
        "is_combust": False,
    })

    # Check combustion (Asta) with Sun
    # Classical combustion limits (degrees from Sun):
    # Moon: 12°, Mars: 17°, Mercury: 14° (12° when retrograde), Jupiter: 11°, Venus: 10° (8° when retrograde), Saturn: 15°
    combust_limits = {
        "Moon": 12.0,
        "Mars": 17.0,
        "Mercury": 14.0,
        "Jupiter": 11.0,
        "Venus": 10.0,
        "Saturn": 15.0,
    }

    for p in planets_data:
        p_name = p["name_en"]
        if p_name in combust_limits:
            diff = abs(p["longitude"] - sun_lon)
            diff = min(diff, 360.0 - diff)
            limit = combust_limits[p_name]
            if p["is_retrograde"] and p_name == "Mercury":
                limit = 12.0
            elif p["is_retrograde"] and p_name == "Venus":
                limit = 8.0
            if diff <= limit:
                p["is_combust"] = True

    return planets_data


# Alias for calculate_planet_positions
calculate_planets = calculate_planet_positions


def calculate_lagna_and_houses(
    jd_ut: float,
    lat: float,
    lon: float,
    ayanamsa_name: str = "lahiri",
    house_system: str = "E"
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Calculate Lagna (Ascendant) and 12 Bhavas (Houses).
    house_system: 'E' for Equal house, 'P' for Placidus, 'W' for Whole sign.
    Vedic standard Equal house system starts from exact Lagna degree.
    """
    set_ayanamsa_mode(ayanamsa_name)
    hsys_byte = house_system[0].upper().encode('ascii')

    # swe.houses_ex with FLG_SIDEREAL calculates sidereal cusps & ascmc
    cusps, ascmc = swe.houses_ex(jd_ut, lat, lon, hsys_byte, swe.FLG_SIDEREAL)
    lagna_deg = ascmc[0] % 360.0

    lagna_info = {
        "longitude": lagna_deg,
        "degree_in_rashi": lagna_deg % 30.0,
        "rashi_index": int(lagna_deg // 30),
    }

    # Build 12 Bhavas (Equal house: each bhava spans 30 degrees centered or beginning at Lagna)
    bhavas = []
    for i in range(12):
        # Equal house system: Bhava 1 begins at Lagna - 15 deg (or exactly at Lagna).
        # In Indian tradition (Sripati/Bhava madhya), Lagna is Bhava Madhya of 1st Bhava.
        mid = (lagna_deg + (i * 30.0)) % 360.0
        start = (mid - 15.0) % 360.0
        end = (mid + 15.0) % 360.0

        bhavas.append({
            "bhava_num": i + 1,
            "start_degree": start,
            "mid_degree": mid,
            "end_degree": end,
            "rashi_index": int(mid // 30),
            "planets": []
        })

    return lagna_info, bhavas

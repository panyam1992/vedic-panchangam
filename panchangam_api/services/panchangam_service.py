"""
Core Panchangam service integrating Jyotisha, Swiss Ephemeris,
Mana systems (Chandramana, Sauramana, Barhaspatyamana),
multilingual transliteration, and Vedic Deśa-Kāla Sankalpa generation.
"""

import os
import sys
import math
import calendar
from datetime import datetime, date
from typing import Dict, Any, List, Optional
import swisseph as swe

# Ensure Jyotisha and API root are in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
JYOTISHA_DIR = os.path.join(PROJECT_ROOT, "Jyotisha")
if JYOTISHA_DIR not in sys.path:
    sys.path.insert(0, JYOTISHA_DIR)

from jyotisha.panchaanga.spatio_temporal import City, annual
from jyotisha.panchaanga.temporal import ComputationSystem, names, Graha, time as jtime
from jyotisha.panchaanga.temporal.time import Date, Timezone
from jyotisha.panchaanga.writer.tex.day_details import (
    get_raahu_yama_gulika_strings,
    get_abhijit_muhurta_string,
    get_varjyam_strings,
    get_amrita_kalam_strings,
)
from indic_transliteration import sanscript

from services.localization_service import (
    transliterate_text,
    get_target_script,
    get_weekday_name,
    get_sankalpa_weekday_stem,
    get_paksha_name,
    get_ayana_name,
    get_ritu_name,
    get_moon_phase_name,
    format_samvatsara_display,
    format_masa_display,
    get_lagna_display_name,
    transliterate_festival_name
)
from services.mana_systems import (
    compute_chandramana,
    compute_sauramana,
    compute_barhaspatyamana,
    RASHI_NAMES_DEV
)
from services.sankalpa_service import generate_sankalpam
from services.moudhyam_kartari_service import compute_daily_moudhyam_kartari, get_annual_moudhyam_kartari

# Load default computation system
COMP_SYSTEM_PATH = os.path.join(JYOTISHA_DIR, 'computation_systems', 'vishvAsa_bhAskara.toml')
DEFAULT_COMP_SYSTEM = ComputationSystem.read_from_file(COMP_SYSTEM_PATH)

# In-memory cache for annual panchangas: (city_key, year) -> Panchaanga
_ANNUAL_CACHE: Dict[str, Any] = {}


def _get_cache_key(city_name: str, lat: float, lon: float, tz: str, year: int) -> str:
    return f"{city_name}_{lat:.4f}_{lon:.4f}_{tz}_{year}"


def get_annual_panchaanga(city: City, year: int) -> Any:
    """Retrieve or compute annual panchaanga for the given city and civil year."""
    key = _get_cache_key(city.name, float(city.latitude), float(city.longitude), city.timezone, year)
    if key in _ANNUAL_CACHE:
        return _ANNUAL_CACHE[key]

    # Precomputed storage directory: check bundled project data first, then user Documents
    bundled_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "precomputed")
    if os.path.isdir(bundled_dir):
        precomputed_dir = bundled_dir
    else:
        precomputed_dir = os.path.expanduser("~/Documents/jyotisha")

    panchaanga = annual.get_panchaanga_for_civil_year(
        city=city,
        year=year,
        computation_system=DEFAULT_COMP_SYSTEM,
        allow_precomputed=True,
        precomputed_json_dir=precomputed_dir
    )
    _ANNUAL_CACHE[key] = panchaanga
    return panchaanga


def _format_jd_local_detail(jd: Optional[float], tz: Timezone, base_date: Optional[Any] = None) -> tuple:
    """
    Convert Julian Day to 12-hour local time string, date string, full datetime string, and next-day boolean.
    Returns: (time_str, date_str, datetime_str, is_next_day)
    Example: ("04:57 AM", "2026-03-27", "2026-03-27 04:57 AM", True)
    """
    if jd is None:
        return None, None, None, False
    lt = tz.julian_day_to_local_time(jd)
    hour_12 = lt.hour % 12 or 12
    am_pm = "AM" if lt.hour < 12 else "PM"
    time_str = f"{hour_12:02d}:{lt.minute:02d} {am_pm}"
    date_str = f"{lt.year:04d}-{lt.month:02d}-{lt.day:02d}"
    datetime_str = f"{date_str} {time_str}"
    
    is_next_day = False
    if base_date is not None:
        if isinstance(base_date, str):
            parts = [int(p) for p in base_date.split("-")]
            b_y, b_m, b_d = parts[0], parts[1], parts[2]
        else:
            b_y, b_m, b_d = base_date.year, base_date.month, base_date.day
        if (lt.year, lt.month, lt.day) > (b_y, b_m, b_d):
            is_next_day = True
            
    return time_str, date_str, datetime_str, is_next_day


# Classical Pushkara Navamsha midpoint degree within sign:
# Fire signs (1, 5, 9): 7th Navamsha midpoint = 21°40' (21.666667°)
# Earth signs (2, 6, 10): 5th Navamsha midpoint = 15°00' (15.0°)
# Air signs (3, 7, 11): 8th Navamsha midpoint = 25°00' (25.0°)
# Water signs (4, 8, 12): 3rd Navamsha midpoint = 8°20' (8.333333°)
PUSHKARA_NAV_MID_DEG = {
    1: 21.666667,
    2: 15.0,
    3: 25.0,
    4: 8.333333,
    5: 21.666667,
    6: 15.0,
    7: 25.0,
    8: 8.333333,
    9: 21.666667,
    10: 15.0,
    11: 25.0,
    12: 8.333333
}


def find_pushkara_amsha_jd(lagna_id: int, start_jd: float, end_jd: float, lat: float, lon: float) -> Optional[float]:
    """
    Finds the exact Julian Day when the Lagna (Ascendant) crosses the Pushkara Navamsha midpoint.
    """
    if start_jd >= end_jd:
        return None
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    deg_in_sign = PUSHKARA_NAV_MID_DEG.get(lagna_id, 15.0)
    target_nirayana_deg = ((lagna_id - 1) * 30.0 + deg_in_sign) % 360.0

    low_jd = start_jd
    high_jd = end_jd
    for _ in range(25):
        mid_jd = (low_jd + high_jd) / 2.0
        ayan = swe.get_ayanamsa_ut(mid_jd)
        cusps, ascmc = swe.houses(mid_jd, lat, lon, b'P')
        asc_sayana = ascmc[0]
        asc_nirayana = (asc_sayana - ayan) % 360.0
        diff = (asc_nirayana - target_nirayana_deg + 180.0) % 360.0 - 180.0
        if diff < 0:
            low_jd = mid_jd
        else:
            high_jd = mid_jd
    return (low_jd + high_jd) / 2.0


def _format_jd_local(jd: Optional[float], tz: Timezone) -> Optional[str]:
    """Convert Julian Day to 12-hour local time string (e.g. '07:36 AM')."""
    time_str, _, _, _ = _format_jd_local_detail(jd, tz)
    return time_str


def _format_time_span_str(span_str: str) -> str:
    """Convert internal time format 'HH:MM--HH:MM' to friendly 'hh:mm AM – hh:mm PM'."""
    if not span_str or "--" not in span_str:
        return span_str
    return span_str.replace("--", " – ")


def _get_moon_illumination_and_phase(jd: float, lang: str = "telugu") -> tuple:
    """Calculate moon illumination fraction (0.0 to 1.0) and phase name."""
    res, _ = swe.calc_ut(jd, swe.MOON, swe.FLG_SWIEPH)
    res_s, _ = swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH)
    diff = (res[0] - res_s[0]) % 360.0
    illum = (1 - math.cos(math.radians(diff))) / 2.0

    if diff < 15 or diff > 345:
        key = "new_moon"
    elif 15 <= diff < 75:
        key = "waxing_crescent"
    elif 75 <= diff < 105:
        key = "first_quarter"
    elif 105 <= diff < 165:
        key = "waxing_gibbous"
    elif 165 <= diff <= 195:
        key = "full_moon"
    elif 195 < diff <= 255:
        key = "waning_gibbous"
    elif 255 < diff <= 285:
        key = "third_quarter"
    else:
        key = "waning_crescent"

    return round(illum, 3), get_moon_phase_name(key, lang)



def get_daily_panchangam(
    lat: float,
    lon: float,
    tz_str: str,
    target_date: Optional[str] = None,
    lang: str = "telugu",
    city_name: str = "Custom Location",
    country_name: str = "India"
) -> Dict[str, Any]:
    """
    Computes complete, comprehensive daily Panchangam for any location worldwide.
    Includes all 3 Manams, 5 Angas, Sun/Moon, Muhurthams, Lagnas, Festivals, and Sankalpam.
    """
    tz = Timezone(tz_str)

    # Parse target date or use today in city timezone
    if target_date:
        parts = [int(p) for p in target_date.split("-")]
        d_obj = Date(parts[0], parts[1], parts[2])
    else:
        now_dt = tz.julian_day_to_local_time(swe.julday(
            datetime.utcnow().year, datetime.utcnow().month, datetime.utcnow().day, datetime.utcnow().hour
        ))
        d_obj = Date(now_dt.year, now_dt.month, now_dt.day)

    date_str = d_obj.get_date_str()
    year = d_obj.year

    city = City(city_name, str(lat), str(lon), tz_str)
    panchaanga = get_annual_panchaanga(city, year)

    if date_str not in panchaanga.date_str_to_panchaanga:
        raise ValueError(f"Date {date_str} not found in computed Panchaanga for {city_name}.")

    dp = panchaanga.date_str_to_panchaanga[date_str]
    target_script = get_target_script(lang)

    # --- 1. Five Angas ---
    # Tithi
    tithis = []
    for t in dp.sunrise_day_angas.tithis_with_ends:
        t_id = t.anga.index
        t_name_dev = names.NAMES['TITHI_NAMES']['sa'][sanscript.DEVANAGARI][t_id]
        t_name_user = transliterate_text(t_name_dev, lang)
        t_time, t_date, t_dt, t_next = _format_jd_local_detail(t.jd_end, tz, dp.date)
        tithis.append({
            "id": t_id,
            "name": t_name_user,
            "name_sanskrit": t_name_dev,
            "end_time": t_time,
            "end_date": t_date,
            "end_datetime": t_dt,
            "is_next_day": t_next,
            "end_jd": t.jd_end
        })

    # Nakshatra
    nakshatras = []
    for n in dp.sunrise_day_angas.nakshatras_with_ends:
        n_id = n.anga.index
        n_name_dev = names.NAMES['NAKSHATRA_NAMES']['sa'][sanscript.DEVANAGARI][n_id]
        n_name_user = transliterate_text(n_name_dev, lang)
        n_time, n_date, n_dt, n_next = _format_jd_local_detail(n.jd_end, tz, dp.date)
        nakshatras.append({
            "id": n_id,
            "name": n_name_user,
            "name_sanskrit": n_name_dev,
            "end_time": n_time,
            "end_date": n_date,
            "end_datetime": n_dt,
            "is_next_day": n_next,
            "end_jd": n.jd_end
        })

    # Yoga
    yogas = []
    for y in dp.sunrise_day_angas.yogas_with_ends:
        y_id = y.anga.index
        y_name_dev = names.NAMES['YOGA_NAMES']['sa'][sanscript.DEVANAGARI][y_id]
        y_name_user = transliterate_text(y_name_dev, lang)
        y_time, y_date, y_dt, y_next = _format_jd_local_detail(y.jd_end, tz, dp.date)
        yogas.append({
            "id": y_id,
            "name": y_name_user,
            "name_sanskrit": y_name_dev,
            "end_time": y_time,
            "end_date": y_date,
            "end_datetime": y_dt,
            "is_next_day": y_next,
            "end_jd": y.jd_end
        })

    # Karana
    karanas = []
    for k in dp.sunrise_day_angas.karanas_with_ends:
        k_id = k.anga.index
        k_name_dev = names.NAMES['KARANA_NAMES']['sa'][sanscript.DEVANAGARI][k_id]
        k_name_user = transliterate_text(k_name_dev, lang)
        k_time, k_date, k_dt, k_next = _format_jd_local_detail(k.jd_end, tz, dp.date)
        karanas.append({
            "id": k_id,
            "name": k_name_user,
            "name_sanskrit": k_name_dev,
            "end_time": k_time,
            "end_date": k_date,
            "end_datetime": k_dt,
            "is_next_day": k_next,
            "end_jd": k.jd_end
        })

    weekday_idx = dp.date.get_weekday()
    weekday_name = get_weekday_name(weekday_idx, lang)
    weekday_en = get_weekday_name(weekday_idx, "english")

    # --- 1. Five Angas & Temporal Coordinates ---
    # Will assemble angas_data after mana systems computation below

    # --- 2. Sun and Moon Timings ---
    illum, phase_name = _get_moon_illumination_and_phase(dp.jd_sunrise, lang)

    # Day length divisions for Sandhya & Brahma Muhurtham
    fifteen = dp.day_length_based_periods.fifteen_fold_division
    brahma_start = _format_jd_local(fifteen.braahma.jd_start, tz)
    brahma_end = _format_jd_local(fifteen.braahma.jd_end, tz)
    pratah_start = _format_jd_local(fifteen.praatas_sandhyaa.jd_start, tz)
    pratah_end = _format_jd_local(fifteen.praatas_sandhyaa.jd_end, tz)
    sayan_start = _format_jd_local(dp.jd_sunset, tz)
    # Sayan sandhya extends ~48 mins after sunset
    sayan_end = _format_jd_local(dp.jd_sunset + (48.0 / 1440.0), tz)

    moonrise_str = _format_jd_local(dp.graha_rise_jd.get(Graha.MOON), tz) or "---"
    moonset_str = _format_jd_local(dp.graha_set_jd.get(Graha.MOON), tz) or "---"

    sun_moon_data = {
        "sunrise": _format_jd_local(dp.jd_sunrise, tz),
        "sunset": _format_jd_local(dp.jd_sunset, tz),
        "midday": _format_jd_local((dp.jd_sunrise + dp.jd_sunset) / 2.0, tz),
        "moonrise": moonrise_str,
        "moonset": moonset_str,
        "brahma_muhurtham": f"{brahma_start} – {brahma_end}",
        "pratahsandhya": f"{pratah_start} – {pratah_end}",
        "sayansandhya": f"{sayan_start} – {sayan_end}",
        "moon_illumination": illum,
        "moon_phase_name": phase_name
    }

    # --- 3. Muhurthams & Inauspicious Periods ---
    gulika_str, rahu_str, yama_str, _, _, dur1_str, dur2_str = get_raahu_yama_gulika_strings(dp, "hh:mm:a")

    durmuhurtams = []
    if dur1_str:
        durmuhurtams.append(_format_time_span_str(dur1_str))
    if dur2_str:
        durmuhurtams.append(_format_time_span_str(dur2_str))

    abhijit_str = get_abhijit_muhurta_string(dp, "hh:mm:a")
    abhijit_formatted = _format_time_span_str(abhijit_str) if abhijit_str else None

    # Day index in panchaanga for Varjyam & Amritakalam
    day_idx = None
    sorted_days = panchaanga.daily_panchaangas_sorted()
    for idx, d_item in enumerate(sorted_days):
        if d_item.date.get_date_str() == date_str:
            day_idx = idx
            break

    varjyam_list = []
    amrita_list = []
    if day_idx is not None:
        v_raw = get_varjyam_strings(panchaanga, day_idx, "hh:mm:a")
        if v_raw and v_raw != '---':
            for v_part in v_raw.split(','):
                varjyam_list.append(_format_time_span_str(v_part.strip()))

        a_raw = get_amrita_kalam_strings(panchaanga, day_idx, "hh:mm:a")
        if a_raw and a_raw != '---':
            for a_part in a_raw.split(','):
                amrita_list.append(_format_time_span_str(a_part.strip()))

    muhurthams_data = {
        "rahu_kalam": _format_time_span_str(rahu_str),
        "yama_gandam": _format_time_span_str(yama_str),
        "gulika_kalam": _format_time_span_str(gulika_str),
        "abhijit_muhurtham": abhijit_formatted,
        "durmuhurtham": durmuhurtams,
        "varjyam": varjyam_list,
        "amrita_kalam": amrita_list
    }

    # --- 4. The 3 Mana Systems ---
    chandramana = compute_chandramana(dp, lang)
    sauramana = compute_sauramana(dp, lang)
    barhaspatyamana = compute_barhaspatyamana(dp.jd_sunrise, lang)

    # Compute cultural displays for Samvatsaram, Ayanam, Rutu, Masam, Paksham
    tithi_num = dp.sunrise_day_angas.tithi_at_sunrise.index
    solar_month = dp.solar_sidereal_date_sunset.month
    lunar_month = int(math.ceil(dp.lunar_date.month.index))

    ayana_display = get_ayana_name(solar_month, lang)
    ritu_display = get_ritu_name(lunar_month, lang)
    paksha_display = get_paksha_name(tithi_num, lang)
    samvatsara_display = format_samvatsara_display(chandramana["samvatsara"]["name"], lang)
    masam_display = format_masa_display(chandramana["amanta_masa"]["name"], lang)

    chandramana["samvatsara_name"] = samvatsara_display
    chandramana["ayana_name"] = ayana_display
    chandramana["ritu_name"] = ritu_display
    chandramana["masam_name"] = masam_display
    chandramana["paksha_name"] = paksha_display
    chandramana["paksha"] = paksha_display
    chandramana["description"] = f"{samvatsara_display} • {ayana_display} • {ritu_display} • {masam_display} • {paksha_display}"

    sauramana["solar_month"]["ayana"] = ayana_display

    angas_data = {
        "vara": weekday_name,
        "vara_english": weekday_en,
        "tithis": tithis,
        "nakshatras": nakshatras,
        "yogas": yogas,
        "karanas": karanas,
        "samvatsara": samvatsara_display,
        "ayanam": ayana_display,
        "rutu": ritu_display,
        "masam": masam_display,
        "paksham": paksha_display
    }

    # --- 5. Festivals & Vratams ---
    festivals = []
    for f_id, f_inst in dp.festival_id_to_instance.items():
        name_user = transliterate_festival_name(f_id, lang)
        festivals.append({
            "id": f_id,
            "name": name_user
        })

    # --- 6. 24-Hour Lagna Schedule with Pushkara Navamsha ---
    lagnas = []
    lagna_raw = dp.get_lagna_data()
    if lagna_raw:
        cur_start_jd = dp.jd_sunrise
        for lagna_id, lagna_end_jd in lagna_raw:
            r_user = get_lagna_display_name(lagna_id, lang)
            st_time, st_date, st_dt, _ = _format_jd_local_detail(cur_start_jd, tz, date_str)
            et_time, et_date, et_dt, is_next = _format_jd_local_detail(lagna_end_jd, tz, date_str)

            duration_min = round((lagna_end_jd - cur_start_jd) * 24 * 60)
            dur_h, dur_m = divmod(duration_min, 60)
            if lang == "telugu":
                dur_str = f"{dur_h} గం. {dur_m} ని."
            elif lang in ["devanagari", "hindi", "sanskrit"]:
                dur_str = f"{dur_h} घण्टे {dur_m} मिनट"
            elif lang == "kannada":
                dur_str = f"{dur_h} ಗಂ. {dur_m} ನಿ."
            elif lang == "tamil":
                dur_str = f"{dur_h} மணி {dur_m} நிமி."
            elif lang == "malayalam":
                dur_str = f"{dur_h} മണി. {dur_m} മിനി."
            elif lang == "gujarati":
                dur_str = f"{dur_h} ક. {dur_m} മി."
            elif lang == "bengali":
                dur_str = f"{dur_h} ঘণ্টা {dur_m} মিনিট"
            else:
                dur_str = f"{dur_h}h {dur_m}m"

            # Pushkara Navamsha calculation
            pushkara_time = None
            pushkara_is_next = False
            p_jd = find_pushkara_amsha_jd(lagna_id, cur_start_jd, lagna_end_jd, lat, lon)
            if p_jd:
                p_t, _, _, pushkara_is_next = _format_jd_local_detail(p_jd, tz, date_str)
                pushkara_time = p_t

            lagnas.append({
                "lagna_id": lagna_id,
                "rashi_name": r_user,
                "start_time": st_time or "---",
                "start_date": st_date,
                "start_datetime": st_dt,
                "end_time": et_time or "---",
                "end_date": et_date,
                "end_datetime": et_dt,
                "is_next_day": is_next,
                "duration": dur_str,
                "pushkara_amsha": pushkara_time,
                "pushkara_is_next_day": pushkara_is_next
            })
            cur_start_jd = lagna_end_jd

    # --- 7. Vedic Deśa-Kāla Sankalpam ---
    sankalpa_res = generate_sankalpam(
        city_name=city_name,
        country=country_name,
        samvatsara_sa=chandramana["samvatsara"]["name_sanskrit"],
        ayana_sa=get_ayana_name(sauramana["solar_month"]["index"], "devanagari"),
        ritu_sa=get_ritu_name(chandramana["amanta_masa"]["index"], "devanagari"),
        masa_sa=chandramana["amanta_masa"]["name_sanskrit"],
        paksha_sa="शुक्ल" if tithis[0]["id"] <= 15 else "कृष्ण",
        tithi_sa=tithis[0]["name_sanskrit"],
        nakshatra_sa=nakshatras[0]["name_sanskrit"],
        weekday_sa=get_sankalpa_weekday_stem(weekday_idx),
        target_lang=lang
    )

    # 8. Moudhyam & Kartari Assessment
    moudhyam_kartari = compute_daily_moudhyam_kartari(dp.jd_sunrise, lang)

    return {
        "city": city_name,
        "country": country_name,
        "latitude": lat,
        "longitude": lon,
        "timezone": tz_str,
        "date": date_str,
        "weekday": weekday_name,
        "weekday_english": weekday_en,
        "language": lang,
        "chandramana": chandramana,
        "sauramana": sauramana,
        "barhaspatyamana": barhaspatyamana,
        "angas": angas_data,
        "sun_moon": sun_moon_data,
        "muhurthams": muhurthams_data,
        "festivals": festivals,
        "lagnas": lagnas,
        "sankalpam": sankalpa_res,
        "moudhyam_kartari": moudhyam_kartari
    }


def get_monthly_panchangam(
    lat: float,
    lon: float,
    tz_str: str,
    year: int,
    month: int,
    lang: str = "telugu",
    city_name: str = "Custom Location",
    country_name: str = "India"
) -> Dict[str, Any]:
    """
    Retrieves full monthly calendar grid data for the given year and month.
    Extracts daily summaries for all days in the month in the requested script.
    """
    tz = Timezone(tz_str)
    city = City(city_name, str(lat), str(lon), tz_str)
    panchaanga = get_annual_panchaanga(city, year)
    target_script = get_target_script(lang)

    _, num_days = calendar.monthrange(year, month)
    day_summaries = []

    for d in range(1, num_days + 1):
        d_str = f"{year:04d}-{month:02d}-{d:02d}"
        if d_str not in panchaanga.date_str_to_panchaanga:
            continue
        dp = panchaanga.date_str_to_panchaanga[d_str]

        # Tithi at sunrise
        first_tithi = dp.sunrise_day_angas.tithis_with_ends[0]
        t_name_dev = names.NAMES['TITHI_NAMES']['sa'][sanscript.DEVANAGARI][first_tithi.anga.index]
        t_name = transliterate_text(t_name_dev, lang)
        t_time, t_date, _, t_next = _format_jd_local_detail(first_tithi.jd_end, tz, dp.date)

        # Nakshatra at sunrise
        first_nak = dp.sunrise_day_angas.nakshatras_with_ends[0]
        n_name_dev = names.NAMES['NAKSHATRA_NAMES']['sa'][sanscript.DEVANAGARI][first_nak.anga.index]
        n_name = transliterate_text(n_name_dev, lang)
        n_time, n_date, _, n_next = _format_jd_local_detail(first_nak.jd_end, tz, dp.date)

        # Masa & Paksha
        m_idx = dp.lunar_date.month.index
        masa_dev = names.get_chandra_masa(m_idx, sanscript.DEVANAGARI)
        masa_name = transliterate_text(masa_dev, lang)
        paksha_name = get_paksha_name(first_tithi.anga.index, lang)

        # Weekday
        weekday_idx = dp.date.get_weekday()
        w_name = get_weekday_name(weekday_idx, lang)

        # Timings
        sr_str = _format_jd_local(dp.jd_sunrise, tz) or ""
        ss_str = _format_jd_local(dp.jd_sunset, tz) or ""
        gulika_str, rahu_str, yama_str, _, _, _, _ = get_raahu_yama_gulika_strings(dp, "hh:mm:a")

        # Festivals
        fest_names = [transliterate_festival_name(f_id, lang) for f_id in dp.festival_id_to_instance.keys()]

        day_summaries.append({
            "date": d_str,
            "day": d,
            "weekday": w_name,
            "tithi_name": t_name,
            "tithi_end_time": t_time,
            "tithi_end_date": t_date,
            "tithi_is_next_day": t_next,
            "nakshatra_name": n_name,
            "nakshatra_end_time": n_time,
            "nakshatra_end_date": n_date,
            "nakshatra_is_next_day": n_next,
            "amanta_masa": masa_name,
            "paksha": paksha_name,
            "sunrise": sr_str,
            "sunset": ss_str,
            "rahu_kalam": _format_time_span_str(rahu_str),
            "yamagandam": _format_time_span_str(yama_str),
            "gulika_kalam": _format_time_span_str(gulika_str),
            "festivals": fest_names
        })

    return {
        "city": city_name,
        "country": country_name,
        "year": year,
        "month": month,
        "language": lang,
        "days": day_summaries
    }
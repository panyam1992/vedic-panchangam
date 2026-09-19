"""
Panchangam API Router.
Provides daily and monthly Panchangam calculations across all Indian languages
and 3 traditional calendar systems (Chandramana, Sauramana, Barhaspatyamana).
"""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Query, HTTPException

from schemas.panchangam_models import (
    DailyPanchangamResponse,
    MonthlyPanchangamResponse,
    IntercalaryListResponse,
    IntercalaryTheoryResponse
)
from services.panchangam_service import get_daily_panchangam, get_monthly_panchangam
from services.city_service import get_city_by_name, search_cities
from services.intercalary_service import (
    get_intercalary_months_range,
    get_intercalary_theory_and_formulas
)

router = APIRouter(prefix="/api/v1/panchangam", tags=["Panchangam"])


def _resolve_location(city: Optional[str], lat: Optional[float], lon: Optional[float], tz: Optional[str]):
    city_name = "Hyderabad"
    country = "India"
    c_lat, c_lon, c_tz = 17.3850, 78.4867, "Asia/Kolkata"

    if city:
        found = get_city_by_name(city)
        if not found:
            res = search_cities(city, limit=1)
            if res:
                found = res[0]
        if found:
            city_name = found["name"]
            country = found.get("country", "India")
            c_lat = found["lat"]
            c_lon = found["lon"]
            c_tz = found["tz"]
        else:
            city_name = city
            if lat is not None and lon is not None and tz is not None:
                c_lat, c_lon, c_tz = lat, lon, tz
            else:
                raise HTTPException(status_code=404, detail=f"City '{city}' not found in database. Please supply lat, lon, and tz.")
    elif lat is not None and lon is not None and tz is not None:
        city_name = "Custom Location"
        country = "Global"
        c_lat, c_lon, c_tz = lat, lon, tz

    return city_name, country, c_lat, c_lon, c_tz


@router.get("/daily", response_model=DailyPanchangamResponse)
def get_daily(
    city: Optional[str] = Query(None, description="City name (e.g. Frisco, Hyderabad, Dallas, London)"),
    lat: Optional[float] = Query(None, description="Latitude coordinate"),
    lon: Optional[float] = Query(None, description="Longitude coordinate"),
    tz: Optional[str] = Query(None, description="Timezone ID (e.g. America/Chicago, Asia/Kolkata)"),
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format (defaults to current date)"),
    language: str = Query("telugu", description="Target language: telugu, devanagari, tamil, kannada, malayalam, gujarati, bengali, oriya, gurmukhi, english")
):
    """
    Compute complete, authoritative daily Panchangam for any location worldwide.
    Includes:
    - 5 Angas (Tithi, Nakshatra, Yoga, Karana, Vara) with exact end times
    - All 3 Mana Systems (Chandramana, Sauramana, Barhaspatyamana)
    - Auspicious/Inauspicious Muhurthams (Rahu Kalam, Yamagandam, Gulika, Durmuhurtham, Abhijit, Varjyam, Amritakalam)
    - Sun/Moon timings (Sunrise, Sunset, Brahma Muhurtham, Sandhya, Moonrise, Moonset, Illumination)
    - 24-Hour Lagna Schedule
    - Hindu Festivals & Vratas
    - Full Vedic Deśa-Kāla Sankalpam mantra and segments
    """
    city_name, country, c_lat, c_lon, c_tz = _resolve_location(city, lat, lon, tz)
    try:
        data = get_daily_panchangam(
            lat=c_lat,
            lon=c_lon,
            tz_str=c_tz,
            target_date=date,
            lang=language.lower(),
            city_name=city_name,
            country_name=country
        )
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/monthly", response_model=MonthlyPanchangamResponse)
def get_monthly(
    city: Optional[str] = Query(None, description="City name (e.g. Frisco, Hyderabad, Dallas)"),
    lat: Optional[float] = Query(None, description="Latitude coordinate"),
    lon: Optional[float] = Query(None, description="Longitude coordinate"),
    tz: Optional[str] = Query(None, description="Timezone ID (e.g. America/Chicago, Asia/Kolkata)"),
    year: int = Query(2026, ge=1900, le=2100, description="Gregorian Year (e.g. 2026)"),
    month: int = Query(3, ge=1, le=12, description="Gregorian Month (1 to 12)"),
    language: str = Query("telugu", description="Target language: telugu, devanagari, tamil, kannada, malayalam, gujarati, bengali, oriya, gurmukhi, english")
):
    """
    Retrieve full monthly calendar grid data for calendar UI views.
    Returns daily Tithi, Nakshatra, Masa, Paksha, Timings, and Festivals for all days in the month.
    """
    city_name, country, c_lat, c_lon, c_tz = _resolve_location(city, lat, lon, tz)
    try:
        data = get_monthly_panchangam(
            lat=c_lat,
            lon=c_lon,
            tz_str=c_tz,
            year=year,
            month=month,
            lang=language.lower(),
            city_name=city_name,
            country_name=country
        )
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/intercalary-months", response_model=IntercalaryListResponse)
def get_intercalary_months(
    start_year: int = Query(2026, ge=1900, le=2100, description="Start Gregorian Year"),
    end_year: int = Query(2036, ge=1900, le=2100, description="End Gregorian Year"),
    system: str = Query("surya_siddhanta", description="Calculation system: 'surya_siddhanta' (Canonical/Vidwathsabha) or 'drik' (Swiss Ephemeris)"),
    language: str = Query("telugu", description="Target language: telugu, devanagari, english, etc.")
):
    """
    Computes all Adhika Masas (Asankranta), Kshaya Masas (Dvi-Sankranta), and Samsarpa Masas
    in the requested year range under Vedic Surya Siddhanta / Dharmashastra (Kalamadhava) or Drik Ganitha.
    """
    try:
        months = get_intercalary_months_range(start_year, end_year, system.lower(), language.lower())
        return {
            "start_year": start_year,
            "end_year": end_year,
            "calculation_system": system,
            "language": language,
            "count": len(months),
            "months": months
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/intercalary-theory", response_model=IntercalaryTheoryResponse)
def get_intercalary_theory(
    language: str = Query("telugu", description="Target language: telugu, devanagari, english, etc.")
):
    """
    Returns canonical treatise, mathematical formulas, solar-lunar drift (11 days/year),
    Vedanga Jyotisha 5-year Yuga cycle (60 solar = 62 lunar months),
    Kaliyuga 432,000-year net balance (168,152 - 8,718 = 159,034),
    and Metonic recurrence intervals (19, 38, 46, 65, 76, 141 years).
    """
    try:
        return get_intercalary_theory_and_formulas(language.lower())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

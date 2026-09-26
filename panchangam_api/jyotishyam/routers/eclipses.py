"""
Worldwide Solar & Lunar Eclipses API router.
"""

from fastapi import APIRouter
from jyotishyam.schemas.input_models import CityEclipseRequest
from jyotishyam.services.city_service import get_city_details
from jyotishyam.services.eclipse_service import get_worldwide_eclipses, calculate_city_eclipses

router = APIRouter(prefix="/api/v1/eclipses", tags=["Eclipses"])


@router.post("/calculate-city")
def get_city_eclipses(req: CityEclipseRequest):
    """
    Computes city-specific eclipse data:
    - Checks local visibility (పాక్షిక / ఛాయ / సంపూర్ణ / కంకణాకార)
    - Converts Sparsha, Madhya, Moksha to local city timezone
    - Computes Sutaka timings (12h/9h before)
    - Total duration in hours and minutes
    - Affected Zodiac Sign & Nakshatra, 12-Rashi predictions & Shanti remedies.
    """
    country = req.country or "US"
    lat = req.latitude
    lon = req.longitude
    tz_name = req.timezone_name
    tz_offset = req.timezone_offset or -5.0

    if req.city:
        resolved = get_city_details(req.city)
        if resolved:
            is_default = (abs(lat - 33.1976) < 0.001 and abs(lon - (-96.6178)) < 0.001)
            city_matched = (
                resolved["name"].lower() in req.city.lower() or
                req.city.lower().strip() in resolved["name"].lower() or
                (resolved.get("name_te") and resolved["name_te"] in req.city)
            )
            if is_default or city_matched:
                lat = resolved["lat"]
                lon = resolved["lon"]
                tz_offset = resolved.get("tz", tz_offset)
                if resolved.get("country", "").lower() in ["india", "in"]:
                    country = "IN"
                    if tz_name in ["America/Chicago", ""]:
                        tz_name = "Asia/Kolkata"

    return calculate_city_eclipses(
        year=req.year,
        city=req.city,
        country=country,
        lat=lat,
        lon=lon,
        tz_name=tz_name,
        tz_offset=tz_offset,
        eclipse_type=req.eclipse_type or "all",
        visible_only=req.visible_only if req.visible_only is not None else True,
        language=req.language or "te"
    )


@router.get("/{year}")
def get_eclipses_by_year(year: int):
    """
    Returns Worldwide Solar & Lunar Eclipses for the specified year:
    - Global visibility across continents
    - UTC and IST timings (Sparsha, Madhya, Moksha)
    - Astrological coordinates (Rashi & Nakshatra)
    - 12 Rashi impacts and universal guidelines.
    """
    return get_worldwide_eclipses(year)

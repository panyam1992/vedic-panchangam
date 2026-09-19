"""
Vedic Deśa-Kāla Sankalpam API Router.
Generates fully personalized, astronomically anchored Vedic Sankalpa mantras
for worship and rituals worldwide.
"""

from typing import Optional, Dict, Any
from fastapi import APIRouter, Query, HTTPException

from services.city_service import get_city_by_name, search_cities
from services.panchangam_service import get_daily_panchangam
from services.sankalpa_service import generate_sankalpam
from services.localization_service import get_ayana_name, get_ritu_name, get_sankalpa_weekday_stem

router = APIRouter(prefix="/api/v1/sankalpam", tags=["Sankalpam"])


@router.get("/generate")
def generate_custom_sankalpam(
    city: Optional[str] = Query("Hyderabad", description="City name (e.g. Frisco, Hyderabad, Dallas, London)"),
    lat: Optional[float] = Query(None, description="Latitude"),
    lon: Optional[float] = Query(None, description="Longitude"),
    tz: Optional[str] = Query(None, description="Timezone"),
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format (defaults to today)"),
    language: str = Query("telugu", description="Target language: telugu, devanagari, tamil, kannada, etc."),
    gotra: Optional[str] = Query(None, description="User Gotra (e.g. 'Kashyapa', 'Bharadwaja', 'Kaundinya')"),
    sharma_name: Optional[str] = Query(None, description="User Name / Sharma (e.g. 'Rama Sharma')"),
    kula_devata: Optional[str] = Query(None, description="Family Deity / Kula Devata (e.g. 'Sri Venkateswara Swamy')")
) -> Dict[str, Any]:
    """
    Generate customized Vedic Deśa-Kāla Sankalpam for daily Puja, Vratam, or Havan.
    Automatically resolves geographical location:
    - In India: Jambu Dveepe, Bharatha Varshe, Bharatha Khande, Meroh Dakshine Parsve, Dandakaranya...
    - In USA/Americas: Krauncha Dveepe, Ramanaka Varshe, Aindra Khande, Meroh Paschima Digbhage, Missouri/Mississippi Nadi Pranthey...
    - In Europe: Plaksha Dveepe...
    """
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
    elif lat is not None and lon is not None and tz is not None:
        c_lat, c_lon, c_tz = lat, lon, tz
        city_name = "Custom Location"
        country = "Global"

    try:
        p_data = get_daily_panchangam(
            lat=c_lat,
            lon=c_lon,
            tz_str=c_tz,
            target_date=date,
            lang=language.lower(),
            city_name=city_name,
            country_name=country
        )

        chandramana = p_data["chandramana"]
        sauramana = p_data["sauramana"]
        angas = p_data["angas"]

        sankalpa = generate_sankalpam(
            city_name=city_name,
            country=country,
            samvatsara_sa=chandramana["samvatsara"]["name_sanskrit"],
            ayana_sa=get_ayana_name(sauramana["solar_month"]["index"], "devanagari"),
            ritu_sa=get_ritu_name(chandramana["amanta_masa"]["index"], "devanagari"),
            masa_sa=chandramana["amanta_masa"]["name_sanskrit"],
            paksha_sa="शुक्ल" if angas["tithis"][0]["id"] <= 15 else "कृष्ण",
            tithi_sa=angas["tithis"][0]["name_sanskrit"],
            nakshatra_sa=angas["nakshatras"][0]["name_sanskrit"],
            weekday_sa=get_sankalpa_weekday_stem(angas["tithis"][0]["id"] % 7),
            target_lang=language.lower(),
            kula_devata=kula_devata,
            gotra=gotra,
            sharma_name=sharma_name
        )

        return {
            "city": city_name,
            "country": country,
            "date": p_data["date"],
            "language": language,
            "sankalpam": sankalpa
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

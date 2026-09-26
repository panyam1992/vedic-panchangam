"""
Newborn / Shishu Jatakam API router.
Provides naming syllables and comprehensive Balarishta & Gandanta doshas analysis.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from jyotishyam.schemas.input_models import ShishuRequest
from jyotishyam.services.city_service import get_city_details
from jyotishyam.services.shishu_service import calculate_shishu_jatakam

router = APIRouter(prefix="/api/v1/shishu", tags=["Shishu"])


@router.post("/generate")
def generate_shishu_jatakam(req: ShishuRequest):
    """
    Computes complete Newborn Horoscope:
    - Nakshatra, Pada, and Auspicious Naming Syllables (నామాక్షరాలు)
    - Comprehensive Balarishta Dosha & Balarishta Bhanga (cancellations)
    - Nakshatra, Tithi, and Lagna Gandanta Dosha analysis
    - Moola & Jyeshtha Nakshatra Pada evaluations
    - Eclipse and Sankranti birth checks
    - Authentic Shastric protective remedies and Shanti guidelines.
    """
    # Auto-resolve city coordinates if place_name provided
    if req.place_name:
        resolved = get_city_details(req.place_name)
        if resolved:
            is_default = (abs(req.latitude - 17.3850) < 0.001 and abs(req.longitude - 78.4867) < 0.001)
            city_matched = (
                resolved["name"].lower() in req.place_name.lower() or
                req.place_name.lower().strip() in resolved["name"].lower() or
                (resolved.get("name_te") and resolved["name_te"] in req.place_name)
            )
            if is_default or city_matched:
                req.latitude = resolved["lat"]
                req.longitude = resolved["lon"]
                req.timezone_offset = resolved.get("tz", req.timezone_offset)
                if "," not in req.place_name and resolved.get("state"):
                    req.place_name = f"{resolved['name']}, {resolved['state']}"
                elif "," not in req.place_name:
                    req.place_name = f"{resolved['name']}, {resolved.get('country', '')}"

    try:
        dt_str = f"{req.dob} {req.tob}"
        fmt = "%Y-%m-%d %H:%M:%S" if len(req.tob.split(":")) == 3 else "%Y-%m-%d %H:%M"
        dt = datetime.strptime(dt_str, fmt)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid date/time format: {str(e)}")

    try:
        result = calculate_shishu_jatakam(
            name=req.name,
            gender=req.gender,
            dt=dt,
            lat=req.latitude,
            lon=req.longitude,
            tz_offset_hours=req.timezone_offset,
            ayanamsa_name=req.ayanamsa
        )
        result["place_name"] = req.place_name
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Shishu Jatakam error: {str(e)}")

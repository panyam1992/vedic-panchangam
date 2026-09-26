"""
Prashna Jyotishyam API router.
Classical Vedic & Tajika Horary system for worldwide users.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from jyotishyam.schemas.input_models import PrashnaRequest
from jyotishyam.services.city_service import get_city_details
from jyotishyam.services.prashna_service import (
    calculate_prashna_chart,
    PRASHNA_CATEGORIES
)

router = APIRouter(prefix="/api/v1/prashna", tags=["Prashna"])


@router.get("/categories")
def get_prashna_categories():
    """Returns available Prashna question categories."""
    return {"categories": PRASHNA_CATEGORIES}


@router.post("/calculate")
def evaluate_prashna(req: PrashnaRequest):
    """
    Evaluates a specific Prashna using Classical Vedic and Tajika principles:
    - Prashna Lagna and Planetary positions (Swiss Ephemeris precision)
    - Lagnesha vs Karyesha alignment
    - 16 Tajika Yogas (Ithasala, Musaripha, Nakta, Yamaya, Kamboola)
    - Verdict, Success Probability %, Timing of fruition & Prashna Marga remedies.
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
        if req.date and req.time:
            dt_str = f"{req.date} {req.time}"
            # Support both HH:MM and HH:MM:SS
            fmt = "%Y-%m-%d %H:%M:%S" if len(req.time.split(":")) == 3 else "%Y-%m-%d %H:%M"
            dt = datetime.strptime(dt_str, fmt)
        else:
            # Default to current UTC time adjusted to requested timezone
            dt = datetime.utcnow()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid date/time format: {str(e)}")

    try:
        qid = req.question_id or req.category or "job"
        result = calculate_prashna_chart(
            question_id=qid,
            dt=dt,
            lat=req.latitude,
            lon=req.longitude,
            tz_offset_hours=req.timezone_offset,
            ayanamsa_name=req.ayanamsa
        )
        result["location"] = req.place_name
        result["coordinates"] = f"{req.latitude:.4f}, {req.longitude:.4f}"
        result["timezone_offset"] = req.timezone_offset
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prashna calculation error: {str(e)}")

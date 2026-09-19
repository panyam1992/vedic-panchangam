"""
Rashi Phalalu (Horoscope & Transit Forecast) API Router.
Endpoints for Daily (Dina), Monthly (Masa), and Yearly (Varsha) Rashi Phalalu
with Chandra Bala, Tara Bala, Chandrashtama detection, Sade Sati,
and traditional Panchanga Kandadayam computations.
"""

from datetime import datetime, date
from typing import Optional
from fastapi import APIRouter, Query, HTTPException

from schemas.rashi_models import (
    DailyRashiResponse,
    MonthlyRashiResponse,
    YearlyRashiResponse
)
from services.rashi_service import (
    compute_daily_rashi_phalalu,
    compute_monthly_rashi_phalalu,
    compute_yearly_rashi_phalalu
)

router = APIRouter(prefix="/api/v1/rashi", tags=["Rashi Phalalu"])


@router.get("/daily", response_model=DailyRashiResponse)
def get_daily_rashi(
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format (defaults to current date)"),
    language: str = Query("telugu", description="Target language: telugu, english, devanagari, tamil, kannada, malayalam, gujarati, bengali")
):
    """
    Compute daily Rashi Phalalu (Horoscope) for all 12 zodiac signs.
    Includes:
    - Chandra Bala (Moon house relative to Rashi)
    - Chandrashtama (8th house Moon) detection and warning
    - Tara Bala assessment (Navatara group)
    - Favorable compatibility score (0-100%)
    - Lucky numbers, lucky colors, and directions
    - Categorized predictions (General, Career, Finance, Health, Family)
    - Specific Vedic shanti and remedies
    """
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    try:
        # Validate format
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Expected YYYY-MM-DD.")

    return compute_daily_rashi_phalalu(date_str=date, lang=language)


@router.get("/monthly", response_model=MonthlyRashiResponse)
def get_monthly_rashi(
    year: Optional[int] = Query(None, description="Year (e.g. 2026, defaults to current year)"),
    month: Optional[int] = Query(None, description="Month 1-12 (defaults to current month)"),
    language: str = Query("telugu", description="Target language: telugu, english, devanagari, tamil, kannada, malayalam, gujarati, bengali")
):
    """
    Compute monthly Rashi Phalalu based on Sun transit (Sauramana month)
    and major planetary alignments.
    """
    now = datetime.now()
    if not year:
        year = now.year
    if not month:
        month = now.month

    if not (1 <= month <= 12):
        raise HTTPException(status_code=400, detail="Month must be between 1 and 12.")

    return compute_monthly_rashi_phalalu(year=year, month=month, lang=language)


@router.get("/yearly", response_model=YearlyRashiResponse)
def get_yearly_rashi(
    year: Optional[int] = Query(None, description="Year (defaults to current year)"),
    language: str = Query("telugu", description="Target language: telugu, english, devanagari, tamil, kannada, malayalam, gujarati, bengali")
):
    """
    Compute yearly Samvatsara Rashi Phalalu for all 12 zodiac signs.
    Includes:
    - Traditional Panchanga Kandadayam (ఆదాయం, వ్యయం, రాజపూజ్యం, అవమానం)
    - Jupiter Transit (Guru Balam) analysis
    - Saturn Transit: Sade Sati (ఏలినాటి శని), Ashtama Shani, Ardhastama Shani
    - Rahu & Ketu influence
    - Comprehensive yearly forecast and remedies
    """
    if not year:
        year = datetime.now().year

    return compute_yearly_rashi_phalalu(year=year, lang=language)

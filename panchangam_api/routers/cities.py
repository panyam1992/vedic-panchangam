"""
Cities API Router.
Provides instant worldwide city search, coordinate resolution, and popular city lists.
"""

from typing import List
from fastapi import APIRouter, Query

from schemas.city_models import CityItem, CitySearchResponse
from services.city_service import search_cities, get_city_by_name, find_nearest_city, GLOBAL_CITIES

router = APIRouter(prefix="/api/v1/cities", tags=["Cities"])

POPULAR_CITY_NAMES = [
    "Hyderabad", "Amaravati", "Vijayawada", "Visakhapatnam", "Tirupati", "Bengaluru",
    "Chennai", "Mumbai", "New Delhi", "Varanasi (Kashi)", "Ayodhya",
    "Frisco", "Dallas", "Plano", "Austin", "San Jose", "San Francisco",
    "New York", "Chicago", "London", "Toronto", "Dubai", "Singapore", "Sydney"
]


@router.get("/search", response_model=CitySearchResponse)
def search(
    q: str = Query("", description="City name or prefix to search (e.g. 'Fri', 'Hyd', 'Dallas')"),
    limit: int = Query(15, ge=1, le=100, description="Maximum number of cities to return")
):
    """Instant fuzzy/prefix search across 500+ worldwide cities."""
    results = search_cities(q, limit=limit)
    return {
        "query": q,
        "total": len(results),
        "cities": results
    }


@router.get("/popular", response_model=List[CityItem])
def get_popular():
    """Retrieve curated list of popular cities for quick selection in UI dropdowns."""
    matched = []
    seen = set()
    for c in GLOBAL_CITIES:
        if c["name"] in POPULAR_CITY_NAMES and c["name"] not in seen:
            matched.append(c)
            seen.add(c["name"])
    return matched


@router.get("/nearest", response_model=CityItem)
def get_nearest(
    lat: float = Query(..., description="GPS Latitude"),
    lon: float = Query(..., description="GPS Longitude")
):
    """Resolve nearest catalog city for GPS coordinates."""
    return find_nearest_city(lat, lon)


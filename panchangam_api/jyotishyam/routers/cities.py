"""
City search API router.
"""

from fastapi import APIRouter, Query
from typing import List, Dict
from jyotishyam.services.city_service import search_cities

router = APIRouter(prefix="/api/v1/cities", tags=["Cities"])


@router.get("/search")
def search_city(q: str = Query(default="", description="City query")):
    """Search cities for birth place autocomplete."""
    return search_cities(q, limit=15)

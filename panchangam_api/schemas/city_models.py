from pydantic import BaseModel, Field
from typing import List, Optional

class CityItem(BaseModel):
    name: str = Field(..., examples=["Hyderabad"])
    state: Optional[str] = Field(None, examples=["Telangana"])
    country: str = Field(..., examples=["India"])
    lat: float = Field(..., examples=[17.3850])
    lon: float = Field(..., examples=[78.4867])
    tz: str = Field(..., examples=["Asia/Kolkata"])

class CitySearchResponse(BaseModel):
    query: str
    total: int
    cities: List[CityItem]
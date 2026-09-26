"""
Input schemas for Jyotishyam API.
Supports worldwide locations, timezones, and coordinates.
"""

from pydantic import BaseModel, Field
from typing import Optional


class BirthDetailsRequest(BaseModel):
    name: str = Field(default="జాతుకుడు", description="Person's name")
    gender: str = Field(default="male", description="'male' or 'female'")
    dob: str = Field(..., description="Date of birth: YYYY-MM-DD")
    tob: str = Field(..., description="Time of birth: HH:MM or HH:MM:SS (24-hr)")
    place_name: str = Field(default="Hyderabad", description="Place name")
    latitude: float = Field(default=17.3850, description="Latitude in decimal degrees (-90 to 90)")
    longitude: float = Field(default=78.4867, description="Longitude in decimal degrees (-180 to 180)")
    timezone_offset: float = Field(default=5.5, description="Timezone offset in hours (e.g. 5.5 for IST, -5 for EST, 0 for UTC)")
    ayanamsa: str = Field(default="lahiri", description="Ayanamsa system: 'lahiri', 'kp', 'raman'")


class PrashnaRequest(BaseModel):
    question_id: str = Field(default="job", description="Prashna query category ID")
    category: Optional[str] = Field(default=None, description="Alias for question_id")
    question_text: Optional[str] = Field(default=None, description="Optional custom question text")
    date: Optional[str] = Field(default=None, description="Question date (YYYY-MM-DD), defaults to now")
    time: Optional[str] = Field(default=None, description="Question time (HH:MM:SS), defaults to now")
    place_name: str = Field(default="Hyderabad", description="Location name")
    latitude: float = Field(default=17.3850, description="Latitude in decimal degrees")
    longitude: float = Field(default=78.4867, description="Longitude in decimal degrees")
    timezone_offset: float = Field(default=5.5, description="Timezone offset from UTC in hours")
    ayanamsa: str = Field(default="lahiri", description="Ayanamsa: 'lahiri' or 'kp'")


class ShishuRequest(BaseModel):
    name: str = Field(default="నవ శిశువు", description="Baby's temporary or desired name")
    gender: str = Field(default="male", description="'male' or 'female'")
    dob: str = Field(..., description="Date of birth: YYYY-MM-DD")
    tob: str = Field(..., description="Time of birth: HH:MM (24-hr)")
    place_name: str = Field(default="Hyderabad", description="Place of birth")
    latitude: float = Field(default=17.3850, description="Latitude")
    longitude: float = Field(default=78.4867, description="Longitude")
    timezone_offset: float = Field(default=5.5, description="Timezone offset from UTC")
    ayanamsa: str = Field(default="lahiri", description="Ayanamsa")


class CityEclipseRequest(BaseModel):
    year: int = Field(default=2028, description="Calendar year (2024 to 2030)")
    country: Optional[str] = Field(default="US", description="Country code or name")
    city: str = Field(default="McKinney", description="City name")
    latitude: float = Field(default=33.1976, description="Latitude")
    longitude: float = Field(default=-96.6178, description="Longitude")
    timezone_name: str = Field(default="America/Chicago", description="IANA timezone name or string")
    timezone_offset: Optional[float] = Field(default=-5.0, description="Fallback numeric offset")
    eclipse_type: Optional[str] = Field(default="all", description="'all', 'solar', 'lunar'")
    visible_only: Optional[bool] = Field(default=True, description="If True, return only eclipses visible in this city")
    language: str = Field(default="te", description="'te' for Telugu or 'en' for English")


class CoupleAnalysisRequest(BaseModel):
    husband: BirthDetailsRequest
    wife: BirthDetailsRequest
    focus_area: Optional[str] = Field(default="general", description="'general', 'santana', 'marriage'")


class FamilyMemberInput(BaseModel):
    id: Optional[str] = Field(default="", description="Optional member ID")
    name: str = Field(default="కుటుంబ సభ్యుడు", description="Member's name")
    relation: str = Field(default="కుటుంబ సభ్యుడు", description="Relation (e.g. భర్త/తండ్రి, భార్య/తల్లి, కుమారుడు, కుమార్తె)")
    gender: str = Field(default="male", description="'male' or 'female'")
    dob: str = Field(..., description="Date of birth: YYYY-MM-DD")
    tob: str = Field(..., description="Time of birth: HH:MM (24-hr)")
    place_name: str = Field(default="Hyderabad", description="Place name")
    latitude: float = Field(default=17.3850, description="Latitude")
    longitude: float = Field(default=78.4867, description="Longitude")
    timezone_offset: float = Field(default=5.5, description="Timezone offset")
    ayanamsa: str = Field(default="lahiri", description="Ayanamsa system")


class FamilyAuditRequest(BaseModel):
    family_name: Optional[str] = Field(default="మా కుటుంబం", description="Family display name")
    purpose: Optional[str] = Field(default="all", description="'all', 'santana', 'grihapravesha', 'sarpa_pitru'")
    members: list[FamilyMemberInput] = Field(..., description="List of family members")


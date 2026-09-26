"""
Chart and Kundali response schemas.
"""

from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from jyotishyam.schemas.input_models import BirthDetailsRequest


class GrahaSpashtaItem(BaseModel):
    id: int
    name_en: str
    name_te: str
    short_name: str
    symbol: str
    longitude: float
    rashi_index: int
    rashi_name_en: str
    rashi_name_te: str
    degree_in_rashi: float
    formatted_degree: str
    speed: float
    is_retrograde: bool
    is_combust: bool
    nakshatra_index: int
    nakshatra_name_en: str
    nakshatra_name_te: str
    pada: int
    navamsha_rashi_index: int
    navamsha_rashi_te: str
    bhava: int
    dignity_en: str
    dignity_te: str


class BhavaItem(BaseModel):
    bhava_num: int
    start_degree: float
    mid_degree: float
    end_degree: float
    rashi_index: int
    rashi_name_te: str
    lord_en: str
    lord_te: str
    planets: List[str]


class KundaliResponse(BaseModel):
    input: BirthDetailsRequest
    ayanamsa_value: float
    lagna: Dict[str, Any]
    planets: List[GrahaSpashtaItem]
    bhavas: List[BhavaItem]
    d1_chart: Dict[int, List[Dict[str, Any]]]
    d9_chart: Dict[int, List[Dict[str, Any]]]
    chalit_chart: Optional[Dict[int, List[Dict[str, Any]]]] = None
    bhava_sphuta: Optional[List[Dict[str, Any]]] = None
    panchangam: Dict[str, Any]
    dasha: Dict[str, Any]
    gocharam: Dict[str, Any]
    yogas: List[Dict[str, Any]]
    gender_highlights: Dict[str, Any]
    ashtakavarga: Optional[Dict[str, Any]] = None
    kuja_dosha: Optional[Dict[str, Any]] = None
    kalasarpa_dosha: Optional[Dict[str, Any]] = None
    predictions: Optional[Dict[str, Any]] = None
    dasha_analysis: Optional[Dict[str, Any]] = None
    classical_tables: Optional[Dict[str, Any]] = None
    remedy_verification: Optional[Dict[str, Any]] = None
    santana_analysis: Optional[Dict[str, Any]] = None

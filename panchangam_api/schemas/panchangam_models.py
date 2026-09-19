from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class AngaDetail(BaseModel):
    id: int
    name: str
    name_sanskrit: Optional[str] = None
    end_time: Optional[str] = None
    end_date: Optional[str] = None
    end_datetime: Optional[str] = None
    is_next_day: Optional[bool] = None
    end_jd: Optional[float] = None

class PanchangaAngas(BaseModel):
    vara: str = Field(..., examples=["బృహస్పతి వాసరం (గురు వాసరం)"])
    vara_english: Optional[str] = Field(None, examples=["Bruhaspati vasaram ( Guru vasaram )"])
    tithis: List[AngaDetail]
    nakshatras: List[AngaDetail]
    yogas: List[AngaDetail]
    karanas: List[AngaDetail]
    samvatsara: Optional[str] = Field(None, examples=["శ్రీ పరాభవ నామ సంవత్సరం"])
    ayanam: Optional[str] = Field(None, examples=["ఉత్తరాయణము"])
    rutu: Optional[str] = Field(None, examples=["వసంత ఋతువు"])
    masam: Optional[str] = Field(None, examples=["చైత్ర మాసము"])
    paksham: Optional[str] = Field(None, examples=["శుక్ల పక్షము"])

class SunMoonTimings(BaseModel):
    sunrise: str = Field(..., examples=["07:36 AM"])
    sunset: str = Field(..., examples=["07:38 PM"])
    midday: str = Field(..., examples=["01:37 PM"])
    moonrise: str = Field(..., examples=["07:15 AM"])
    moonset: str = Field(..., examples=["08:20 PM"])
    brahma_muhurtham: Optional[str] = Field(None, examples=["05:54 AM – 06:42 AM"])
    pratahsandhya: Optional[str] = Field(None, examples=["06:18 AM – 07:36 AM"])
    sayansandhya: Optional[str] = Field(None, examples=["07:38 PM – 08:56 PM"])
    moon_illumination: Optional[float] = Field(None, examples=[0.02])
    moon_phase_name: Optional[str] = Field(None, examples=["New Moon (Amavasya)"])

class MuhurthaWindows(BaseModel):
    rahu_kalam: str = Field(..., examples=["01:30 PM – 03:00 PM"])
    yama_gandam: str = Field(..., examples=["06:00 AM – 07:30 AM"])
    gulika_kalam: str = Field(..., examples=["09:00 AM – 10:30 AM"])
    abhijit_muhurtham: Optional[str] = Field(None, examples=["11:55 AM – 12:43 PM"])
    durmuhurtham: List[str] = Field(default_factory=list, examples=[["10:15 AM – 11:02 AM"]])
    varjyam: List[str] = Field(default_factory=list, examples=[["08:20 PM – 09:50 PM"]])
    amrita_kalam: List[str] = Field(default_factory=list, examples=[["05:10 AM – 06:40 AM"]])

class ChandramanaData(BaseModel):
    samvatsara: Dict[str, Any]
    amanta_masa: Dict[str, Any]
    purnimanta_masa: Dict[str, Any]
    paksha: str
    paksha_name: Optional[str] = None
    samvatsara_name: Optional[str] = None
    ayana_name: Optional[str] = None
    ritu_name: Optional[str] = None
    masam_name: Optional[str] = None
    tithi_at_sunrise: int
    description: str

    model_config = {"extra": "allow"}

class SauramanaData(BaseModel):
    solar_month: Dict[str, Any]
    regional_solar_calendars: Dict[str, Any]
    sankranti_transition: Optional[Dict[str, Any]] = None

    model_config = {"extra": "allow"}

class BarhaspatyamanaData(BaseModel):
    jupiter_position: Dict[str, Any]
    jovian_cycle_12_year: Dict[str, Any]
    sacred_river_pushkaram: Dict[str, Any]

    model_config = {"extra": "allow"}

class LagnaItem(BaseModel):
    lagna_id: int
    rashi_name: str
    start_time: Optional[str] = None
    start_date: Optional[str] = None
    start_datetime: Optional[str] = None
    end_time: str
    end_date: Optional[str] = None
    end_datetime: Optional[str] = None
    is_next_day: bool = False
    duration: Optional[str] = None
    pushkara_amsha: Optional[str] = None
    pushkara_is_next_day: bool = False

class FestivalItem(BaseModel):
    id: str
    name: str

class DailyPanchangamResponse(BaseModel):
    city: str
    country: Optional[str] = "India"
    latitude: float
    longitude: float
    timezone: str
    date: str
    weekday: str
    language: str
    chandramana: ChandramanaData
    sauramana: SauramanaData
    barhaspatyamana: BarhaspatyamanaData
    angas: PanchangaAngas
    sun_moon: SunMoonTimings
    muhurthams: MuhurthaWindows
    festivals: List[FestivalItem]
    lagnas: List[LagnaItem]
    sankalpam: Dict[str, Any]
    moudhyam_kartari: Optional[Dict[str, Any]] = None

    model_config = {"extra": "allow"}


class MonthlyDaySummary(BaseModel):
    date: str
    day: int
    weekday: str
    tithi_name: str
    tithi_end_time: Optional[str] = None
    tithi_end_date: Optional[str] = None
    tithi_is_next_day: Optional[bool] = None
    nakshatra_name: str
    nakshatra_end_time: Optional[str] = None
    nakshatra_end_date: Optional[str] = None
    nakshatra_is_next_day: Optional[bool] = None
    amanta_masa: str
    paksha: str
    sunrise: str
    sunset: str
    rahu_kalam: str
    yamagandam: str
    gulika_kalam: str
    festivals: List[str] = Field(default_factory=list)


class MonthlyPanchangamResponse(BaseModel):
    city: str
    country: Optional[str] = "India"
    year: int
    month: int
    language: str
    days: List[MonthlyDaySummary]


class IntercalaryMonthItem(BaseModel):
    year: int
    samvatsara_name: str
    samvatsara_name_telugu: Optional[str] = None
    masa_name: str
    masa_name_telugu: Optional[str] = None
    full_display_name: str
    classification: str
    classification_name: str
    sankranti_count: int
    conjoined_months: Optional[List[str]] = None
    start_date: str
    end_date: str
    description: str
    shastra_verse: Optional[str] = None


class IntercalaryListResponse(BaseModel):
    start_year: int
    end_year: int
    calculation_system: str
    language: str
    count: int
    months: List[IntercalaryMonthItem]


class IntercalaryTheoryResponse(BaseModel):
    title: str
    principles: List[Dict[str, Any]]
    kalamadhava_canonical_rule: Dict[str, Any]
    solar_lunar_drift: Dict[str, Any]
    kaliyuga_epoch_balance: Dict[str, Any]
    kshaya_recurrence_intervals: Dict[str, Any]
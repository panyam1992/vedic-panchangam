from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class RashiMeta(BaseModel):
    id: int = Field(..., description="Rashi index 1 to 12 (1=Mesha, 12=Meena)")
    code: str = Field(..., description="Unique slug code (e.g. mesha, vrishabha)")
    name: str = Field(..., description="Localized name (e.g. మేషం, मेष, Mesha)")
    name_sanskrit: Optional[str] = Field(None, description="Sanskrit script name")
    name_english: str = Field(..., description="English zodiac name (e.g. Aries)")
    symbol: str = Field(..., description="Zodiac astrological glyph (e.g. ♈)")
    lord: str = Field(..., description="Ruling planet name (e.g. కుజుడు / Mars)")
    element: str = Field(..., description="Vedic element: అగ్ని (Fire), భూమి (Earth), వాయువు (Air), జలం (Water)")

class CategoryPredictions(BaseModel):
    general: str = Field(..., description="సాధారణ ఫలితం / General overview")
    career: str = Field(..., description="ఉద్యోగం & వ్యాపారం / Career & Business")
    finance: str = Field(..., description="ఆర్థిక స్థితి / Wealth & Finances")
    health: str = Field(..., description="ఆరోగ్యం / Health & Vitality")
    family: str = Field(..., description="కుటుంబం & దాంపత్యం / Family & Relationships")

class DailyRashiItem(BaseModel):
    rashi: RashiMeta
    moon_house: int = Field(..., description="Moon transit house relative to Janma Rashi (1-12)")
    is_chandrashtama: bool = Field(..., description="True if Moon is in 8th house from Janma Rashi")
    chandra_bala_status: str = Field(..., description="Chandra Bala assessment (e.g. అనుకూలం, మధ్యమం, చంద్రాష్టమం)")
    tara_bala_name: str = Field(..., description="Tara Bala name (e.g. సాధక తార, సంపత్ తార)")
    is_tara_bala_good: bool = Field(..., description="True if Tara is auspicious")
    score_percent: int = Field(..., description="Favorable percentage index 0-100%")
    score_rating: str = Field(..., description="Rating description (e.g. ఉత్తమం, అనుకూలం, సాధారణం, అప్రమత్తత)")
    lucky_number: int = Field(..., description="Lucky number for the day (1-9)")
    lucky_color: str = Field(..., description="Auspicious color for the day")
    lucky_direction: str = Field(..., description="Auspicious direction")
    predictions: CategoryPredictions
    remedy: str = Field(..., description="Recommended simple remedy or mantra for the day")

class DailyRashiResponse(BaseModel):
    date: str
    weekday: str
    language: str
    moon_rashi: str
    moon_nakshatra: str
    rashis: List[DailyRashiItem]

class MonthlyRashiItem(BaseModel):
    rashi: RashiMeta
    sun_house: int = Field(..., description="Sun transit house relative to Janma Rashi (1-12)")
    is_sun_favorable: bool = Field(..., description="True if Sun is in 3, 6, 10, 11")
    score_percent: int = Field(..., description="Favorable monthly percentage index 0-100%")
    score_rating: str
    predictions: CategoryPredictions
    highlights: List[str] = Field(default_factory=list, description="Key bullet points for the month")
    remedy: str

class MonthlyRashiResponse(BaseModel):
    year: int
    month: int
    solar_month: str
    language: str
    rashis: List[MonthlyRashiItem]

class KandadayamData(BaseModel):
    aadhayam: int = Field(..., description="ఆదాయం (Income points 0-14)")
    vyayam: int = Field(..., description="వ్యయం (Expenditure points 0-14)")
    rajapujyam: int = Field(..., description="రాజపూజ్యం (Honor/Fame points 0-8)")
    avamanam: int = Field(..., description="అవమానం (Disgrace/Obstacles points 0-8)")
    finance_status: str = Field(..., description="ఆదాయ-వ్యయ తులనాత్మక ఫలితం (e.g. విశేష ధనలాభం, సాధారణం, అధిక ఖర్చులు)")
    social_status: str = Field(..., description="రాజపూజ్య-అవమాన తులనాత్మక ఫలితం (e.g. కీర్తి ప్రతిష్టలు, అప్రమత్తత)")

class YearlyRashiItem(BaseModel):
    rashi: RashiMeta
    jupiter_house: int = Field(..., description="Jupiter transit house relative to Janma Rashi (1-12)")
    has_guru_balam: bool = Field(..., description="True if Jupiter is in 2, 5, 7, 9, 11")
    guru_balam_text: str = Field(..., description="Jupiter transit assessment description")
    saturn_house: int = Field(..., description="Saturn transit house relative to Janma Rashi (1-12)")
    sade_sati_status: str = Field(..., description="Sade Sati / Shani status (e.g. ఏలినాటి శని లేదు, ఏలినాటి శని, అష్టమ శని, అనుకూలం)")
    rahu_ketu_status: str = Field(..., description="Rahu and Ketu transit status")
    kandadayam: KandadayamData
    score_percent: int = Field(..., description="Overall yearly favorable score 0-100%")
    score_rating: str
    predictions: CategoryPredictions
    highlights: List[str] = Field(default_factory=list)
    remedy: str

class YearlyRashiResponse(BaseModel):
    year: int
    samvatsara: str
    language: str
    rashis: List[YearlyRashiItem]

class TrimesterKandaya(BaseModel):
    name: str = Field(..., description="కందాయం పేరు (e.g. ప్రథమ కందాయం)")
    months: str = Field(..., description="నెలలు (e.g. చైత్రం, వైశాఖం, జ్యేష్ఠం, ఆషాఢం)")
    score: int = Field(..., description="కందాయ సంఖ్య")
    max_score: int = Field(..., description="గరిష్ట సంఖ్య (8, 3, or 5)")
    status: str = Field(..., description="ఫలిత వర్గీకరణ (ఉత్తమం, మధ్యమం, అప్రమత్తత)")
    prediction: str = Field(..., description="వివరణాత్మక ఫలితం")

class NakshatraKandayaItem(BaseModel):
    id: int = Field(..., description="నక్షత్ర సంఖ్య 1 to 27")
    name: str = Field(..., description="నక్షత్రం పేరు")
    rashi_names: List[str] = Field(default_factory=list, description="నక్షత్ర పాదాలు వ్యాపించిన రాశులు")
    trimester_1: TrimesterKandaya
    trimester_2: TrimesterKandaya
    trimester_3: TrimesterKandaya
    overall_status: str = Field(..., description="సంవత్సర సమగ్ర ఫలితం")
    overall_rating: str = Field(..., description="ఉత్తమం / అనుకూలం / మధ్యమం / అప్రమత్తత")

class RashiKandadayamItem(BaseModel):
    rashi: RashiMeta
    aadhayam: int
    vyayam: int
    rajapujyam: int
    avamanam: int
    finance_status: str
    social_status: str
    verdict: str

class ComprehensiveKandadayamResponse(BaseModel):
    samvatsara: str
    year: int
    language: str
    explanation: Dict[str, str]
    rashis: List[RashiKandadayamItem]
    nakshatras: List[NakshatraKandayaItem]


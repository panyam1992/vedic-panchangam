# -*- coding: utf-8 -*-
"""
Router for Muhurtam (ముహూర్త నిర్ణయం) and Santana Dosha / Pregnancy Loss Analysis.
Provides high-precision astronomical Muhurtam calculations grounded in:
- ముహూర్త రత్నావళి (Muhurtha Ratnavali)
- కాలామృతమ్ (Kalamritam)
- ముహూర్త దర్పణం (Muhurtha Darpana)
- బృహత్ పరాశర హోరాశాస్త్రం (Santana Adhyayam)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from jyotishyam.services.muhurtam_service import find_best_muhurtams, EVENT_SPECS
from jyotishyam.schemas.input_models import BirthDetailsRequest
from jyotishyam.routers.kundali import generate_kundali


router = APIRouter(prefix="/api/v1/muhurtam", tags=["Muhurtam & Santana Pariharam"])


class MuhurtamCalculateRequest(BaseModel):
    event_type: str = Field(default="naga_pratishtha", description="Key from EVENT_SPECS")
    start_date: Optional[str] = Field(default=None, description="Start date in YYYY-MM-DD format (defaults to today)")
    days_range: int = Field(default=30, ge=1, le=180, description="Number of days to search")
    latitude: float = Field(default=17.3850, description="City latitude (default: Hyderabad)")
    longitude: float = Field(default=78.4867, description="City longitude (default: Hyderabad)")
    timezone_offset: float = Field(default=5.5, description="Timezone offset in hours")
    native_nakshatra_index: Optional[int] = Field(default=None, ge=0, le=26, description="Native Nakshatra (0-26) for personalized Tara Bala")
    native_rashi_index: Optional[int] = Field(default=None, ge=0, le=11, description="Native Moon Rashi (0-11) for personalized Chandra Bala")
    participant_mode: str = Field(default="individual", description="'individual', 'couple' (husband & wife), 'family' (whole family)")
    family_members: Optional[List[Dict[str, Any]]] = Field(default=None, description="List of family members/couple participants with name, role, nakshatra_index, rashi_index")
    limit: int = Field(default=7, ge=1, le=20, description="Number of top auspicious slots to return")


@router.get("/event-types")
def get_event_types():
    """
    Returns all supported Muhurtam event types (Parihara Homas & Auspicious Samskaras)
    with their Shastra references and descriptions.
    """
    pariharams = []
    samskaras = []
    for code, spec in EVENT_SPECS.items():
        item = {
            "code": code,
            "title_te": spec["title_te"],
            "category": spec["category"],
            "description": spec["description"],
            "shastra_source": spec["shastra_source"],
            "rule_note": spec["rule_note"]
        }
        if spec["category"] == "pariharam":
            pariharams.append(item)
        else:
            samskaras.append(item)

    return {
        "status": "success",
        "pariharams": pariharams,
        "samskaras": samskaras,
        "total_events": len(EVENT_SPECS)
    }


@router.post("/calculate")
def calculate_muhurtam(req: MuhurtamCalculateRequest):
    """
    Computes precise, astronomically verified auspicious Muhurtams for the requested event,
    filtering out Rahu Kalam, Yamagandam, Gulika, Varjyam (Visha Ghatikas), and Durmuhurtham,
    while evaluating joint Tara Bala & Chandra Bala for single native, couple, or entire family members!
    """
    try:
        results = find_best_muhurtams(
            event_type=req.event_type,
            start_date_str=req.start_date,
            days_range=req.days_range,
            lat=req.latitude,
            lon=req.longitude,
            tz_offset=req.timezone_offset,
            native_nak_idx=req.native_nakshatra_index,
            native_rashi_idx=req.native_rashi_index,
            family_members=req.family_members,
            limit=req.limit
        )
        return {
            "status": "success",
            "data": results
        }
    except KeyError as ke:
        raise HTTPException(status_code=400, detail=f"చెల్లని ముహూర్త కార్యం: {str(ke)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ముహూర్త నిర్ణయంలో లోపం: {str(e)}")


@router.post("/santana-analysis")
def santana_and_pregnancy_analysis(req: BirthDetailsRequest):
    """
    Comprehensive Santana & Pregnancy Loss (గర్భస్రావ / సంతాన దోష విశ్లేషణ) Engine.
    Evaluates:
    - 5th House, 5th Lord, and Jupiter (Putrakaraka)
    - Beeja Sphuta (Male virility) & Kshetra Sphuta (Female womb fertility)
    - Sarpa Shaapa / Naga Dosha
    - Kuja-Ketu Garbhasrava (Miscarriage) Dosha
    - Pithru / Matru Shaapa
    - Automatically finds upcoming Auspicious Muhurtams for the native's recommended remedy!
    """
    try:
        kundali = generate_kundali(req)
        p_info = kundali.panchangam or {}
        native_nak_idx = p_info.get("nakshatra_index")
        native_rashi_idx = p_info.get("rashi_index")
        santana_data = kundali.santana_analysis or {}

        # Pre-calculate upcoming Muhurtams for the primary recommended remedy
        rec_event = santana_data.get("recommended_event_type", "santana_gopala")
        muhurtam_candidates = find_best_muhurtams(
            event_type=rec_event,
            days_range=30,
            lat=req.latitude,
            lon=req.longitude,
            tz_offset=req.timezone_offset,
            native_nak_idx=native_nak_idx,
            native_rashi_idx=native_rashi_idx,
            limit=5
        )

        return {
            "status": "success",
            "native_name": req.name,
            "gender": req.gender,
            "lagna": kundali.lagna.get("rashi_name_te", ""),
            "rashi": p_info.get("rashi", ""),
            "nakshatra": p_info.get("nakshatra", ""),
            "santana_analysis": santana_data,
            "recommended_muhurtams": muhurtam_candidates
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"సంతాన విశ్లేషణలో లోపం: {str(e)}")


class CoupleSantanaRequest(BaseModel):
    husband: BirthDetailsRequest
    wife: BirthDetailsRequest
    days_range: int = Field(default=30, ge=1, le=90)


@router.post("/couple-santana-analysis")
def couple_santana_and_muhurtam_analysis(req: CoupleSantanaRequest):
    """
    Combined Dampati (Husband & Wife) Progeny & Pregnancy Loss Analysis.
    Evaluates:
    - Husband's Beeja Sphuta (పురుష వీర్య బలం) and 5th house
    - Wife's Kshetra Sphuta (స్త్రీ గర్భాశయ శక్తి) and Garbhasrava (Miscarriage) risk
    - Both charts for Sarpa Shaapa / Naga Dosha
    - Joint Vedic Remedy recommendation
    - Calculates joint Muhurtams where NEITHER husband NOR wife has Ashtama Chandra or Naidhana Tara!
    """
    try:
        # 1. Generate both charts
        h_kundali = generate_kundali(req.husband)
        w_kundali = generate_kundali(req.wife)

        h_santana = h_kundali.santana_analysis or {}
        w_santana = w_kundali.santana_analysis or {}

        h_nak_idx = h_kundali.panchangam.get("nakshatra_index")
        h_rashi_idx = h_kundali.panchangam.get("rashi_index")

        w_nak_idx = w_kundali.panchangam.get("nakshatra_index")
        w_rashi_idx = w_kundali.panchangam.get("rashi_index")

        # 2. Extract Beeja & Kshetra Sphutas
        beeja = h_santana.get("sphutas", {}).get("beeja_sphuta", {})
        kshetra = w_santana.get("sphutas", {}).get("kshetra_sphuta", {})

        # 3. Combine doshas
        joint_doshas = []
        for d in h_santana.get("doshas_detected", []):
            item = dict(d)
            item["afflicted_person"] = f"భర్త ({req.husband.name})"
            joint_doshas.append(item)

        for d in w_santana.get("doshas_detected", []):
            item = dict(d)
            item["afflicted_person"] = f"భార్య ({req.wife.name})"
            joint_doshas.append(item)

        # 4. Joint Diagnosis & Recommended Parihara
        has_naga = any("naga" in d.get("code", "") for d in joint_doshas)
        has_garbhasrava = any("garbhasrava" in d.get("code", "") for d in joint_doshas)
        is_beeja_weak = beeja.get("badge") == "danger"
        is_kshetra_weak = kshetra.get("badge") == "danger"

        if has_naga:
            rec_event = "naga_pratishtha"
            joint_remedy_title = "దంపతుల ఉమ్మడి నాగ ప్రతిష్ఠ లేదా ఆశ్లేషా బలి పూజ"
            joint_verdict = "జాతకంలో సర్ప శాప / నాగ దోష ప్రభావం ఉన్నందున దంపతులు ఇరువురూ కలిసి అశ్వత్థ వృక్ష సన్నిధిలో నాగ ప్రతిష్ఠ లేదా కుక్కే/శ్రీకాళహస్తి క్షేత్రంలో పూజ చేయించడం ఉత్తమం."
        elif has_garbhasrava or is_kshetra_weak:
            rec_event = "kuja_shanti_subrahmanya"
            joint_remedy_title = "సుబ్రహ్మణ్య షష్ఠి వ్రతం & గర్భరక్షాంబికా అమ్మవారి ఆరాధన"
            joint_verdict = "స్త్రీ క్షేత్ర బలం లేదా కుజ-కేతు ప్రభావం వలన గర్భం నిలవడంలో సమస్యలు (గర్భస్రావ సూచన) ఉన్నందున సుబ్రహ్మణ్యేశ్వర స్వామి మరియు శ్రీ గర్భరక్షాంబికా అమ్మవారి ఆరాధన అత్యంత ఫలప్రదం."
        elif is_beeja_weak:
            rec_event = "santana_gopala"
            joint_remedy_title = "సంతాన గోపాల హోమం & కృష్ణార్చన"
            joint_verdict = "పురుష బీజ స్పష్టంలో బలం తక్కువగా ఉన్నందున శ్రీకృష్ణునికి సంతాన గోపాల హోమం మరియు హరివంశ పురాణ శ్రవణం చేయించాలి."
        else:
            rec_event = "santana_gopala"
            joint_remedy_title = "సంతాన గోపాల హోమం / కృష్ణార్చన"
            joint_verdict = "దంపతుల ఇరువురి జాతకాలలో సంతాన యోగం అనుకూలంగా ఉంది. ఇష్టదైవ ప్రార్థనతో పాటు సంతాన గోపాల మంత్ర జపంతో సత్సంతాన భాగ్యం సిద్ధిస్తుంది."

        # 5. Build couple family members list for joint Muhurtam evaluation
        couple_members = [
            {
                "name": f"{req.husband.name} (భర్త)",
                "role": "husband",
                "nakshatra_index": h_nak_idx,
                "rashi_index": h_rashi_idx
            },
            {
                "name": f"{req.wife.name} (భార్య)",
                "role": "wife",
                "nakshatra_index": w_nak_idx,
                "rashi_index": w_rashi_idx
            }
        ]

        # Calculate joint Muhurtams
        joint_muhurtams = find_best_muhurtams(
            event_type=rec_event,
            days_range=req.days_range,
            lat=req.husband.latitude,
            lon=req.husband.longitude,
            tz_offset=req.husband.timezone_offset,
            family_members=couple_members,
            limit=5
        )

        return {
            "status": "success",
            "husband_info": {
                "name": req.husband.name,
                "lagna": h_kundali.lagna.get("rashi_name_te", ""),
                "rashi": h_kundali.panchangam.get("rashi", ""),
                "nakshatra": h_kundali.panchangam.get("nakshatra", ""),
                "beeja_sphuta": beeja,
                "fifth_house": h_santana.get("fifth_house_info", {})
            },
            "wife_info": {
                "name": req.wife.name,
                "lagna": w_kundali.lagna.get("rashi_name_te", ""),
                "rashi": w_kundali.panchangam.get("rashi", ""),
                "nakshatra": w_kundali.panchangam.get("nakshatra", ""),
                "kshetra_sphuta": kshetra,
                "fifth_house": w_santana.get("fifth_house_info", {})
            },
            "joint_diagnosis": {
                "recommended_event_type": rec_event,
                "joint_remedy_title": joint_remedy_title,
                "joint_verdict": joint_verdict,
                "total_doshas_detected": len(joint_doshas),
                "joint_doshas": joint_doshas,
                "shastric_rule": "దంపతులు ఇరువురి జాతకాలను సమన్వయపరిచి, ఇద్దరికీ అష్టమ చంద్రుడు మరియు నైధన తార లేని పవిత్ర కాలంలో మాత్రమే పరిహారాలు జరిపించాలి (*కాలామృతమ్*)."
            },
            "joint_muhurtams": joint_muhurtams
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"దంపతుల ఉమ్మడి సంతాన విశ్లేషణలో లోపం: {str(e)}")

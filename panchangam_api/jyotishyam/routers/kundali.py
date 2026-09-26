"""
Kundali generation API router.
"""

from fastapi import APIRouter, HTTPException
from jyotishyam.schemas.input_models import (
    BirthDetailsRequest,
    CoupleAnalysisRequest,
    FamilyAuditRequest,
    FamilyMemberInput,
)
from jyotishyam.schemas.chart_models import KundaliResponse
from jyotishyam.services.joint_dosha_service import analyze_couple_joint, audit_family_doshas

from jyotishyam.services.ephemeris_service import (
    get_julian_day_ut,
    get_ayanamsa_value,
    calculate_planet_positions,
    calculate_lagna_and_houses,
)
from jyotishyam.services.kundali_calculator import (
    enrich_lagna_details,
    enrich_planets,
    build_charts,
    calculate_bhava_sphuta,
    get_nakshatra_and_pada,
    get_gender_specific_highlights,
    RASHIS,
)
from jyotishyam.services.city_service import get_city_details
from jyotishyam.services.panchangam_calc import calculate_birth_panchangam
from jyotishyam.services.dasha_service import calculate_vimshottari_dasha
from jyotishyam.services.gochara_service import analyze_gocharam
from jyotishyam.services.yoga_service import detect_yogas, analyze_kuja_dosha, analyze_kalasarpa_dosha
from jyotishyam.services.ashtakavarga_service import calculate_ashtakavarga
from jyotishyam.services.predictions_service import generate_predictions
from jyotishyam.services.dasha_predictions_service import generate_dasha_antardasha_analysis
from jyotishyam.services.classical_tables_service import (
    calculate_ghata_chakra,
    calculate_lucky_factors,
    calculate_jaimini_karakas,
    calculate_maitri_chakra,
    calculate_planetary_aspects,
    calculate_gemstones_and_rudraksha,
    calculate_vastu_house_facing,
)
from jyotishyam.services.remedy_verification_service import (
    audit_all_common_pujas,
    audit_kuja_dosha_puja,
    audit_kalasarpa_puja,
    audit_shani_puja,
    audit_gemstone_safety,
)
from jyotishyam.services.santana_dosha_service import analyze_santana_and_pregnancy_doshas

router = APIRouter(prefix="/api/v1/kundali", tags=["Kundali"])


@router.post("/generate", response_model=KundaliResponse)
def generate_kundali(req: BirthDetailsRequest):
    """
    Generate comprehensive Janma Kundali:
    - Lagna and 12 Bhavas
    - 9 Sidereal Planetary Positions & Dignities
    - D1 (Rashi), D9 (Navamsha), and Bhava Chalit Charts
    - Dvadasa Bhava Sphuta (House Cusps & Spans)
    - Birth Panchangam (Tithi, Vara, Nakshatra, Yoga, Karana, Gana, Nadi, Avakahada)
    - Vimshottari Dasha timeline & current running dasha
    - Current Gocharam & Sade Sati analysis
    - Astrological Yogas, Kuja Dosha & Kala Sarpa Dosha
    - 337-point Sarvashtakavarga (SAV) & BAV
    - In-depth Classical Telugu Predictions
    - Gender-specific (Stree / Purusha Jataka) highlights
    """
    # Auto-resolve city coordinates if place_name provided and matches a known city
    if req.place_name:
        resolved = get_city_details(req.place_name)
        if resolved:
            is_default = (
                (abs(req.latitude - 16.3067) < 0.001 and abs(req.longitude - 80.4365) < 0.001) or
                (abs(req.latitude - 17.3850) < 0.001 and abs(req.longitude - 78.4867) < 0.001)
            )
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
        jd_ut = get_julian_day_ut(req.dob, req.tob, req.timezone_offset)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid date/time/timezone: {str(e)}")

    ayanamsa_val = get_ayanamsa_value(jd_ut)

    # 1. Calculate Lagna & Houses
    lagna_raw, bhavas_raw = calculate_lagna_and_houses(
        jd_ut, req.latitude, req.longitude, ayanamsa_name=req.ayanamsa
    )
    lagna_info = enrich_lagna_details(lagna_raw["longitude"])

    # 2. Calculate Planets
    planets_raw = calculate_planet_positions(jd_ut, ayanamsa_name=req.ayanamsa)
    planets_enriched = enrich_planets(planets_raw, lagna_info["longitude"])

    # Map planets into Bhavas
    bhavas_enriched = []
    p_map_by_bhava = {i: [] for i in range(1, 13)}
    for p in planets_enriched:
        p_map_by_bhava[p["bhava"]].append(f"{p['name_te']} ({p['formatted_degree']})")

    for b in bhavas_raw:
        r_idx = b["rashi_index"]
        bhavas_enriched.append({
            "bhava_num": b["bhava_num"],
            "start_degree": b["start_degree"],
            "mid_degree": b["mid_degree"],
            "end_degree": b["end_degree"],
            "rashi_index": r_idx,
            "rashi_name_te": RASHIS[r_idx]["name_te"],
            "lord_en": RASHIS[r_idx]["lord_en"],
            "lord_te": RASHIS[r_idx]["lord_te"],
            "planets": p_map_by_bhava[b["bhava_num"]]
        })

    # 3. Calculate Bhava Sphuta & Build Charts (D1, D9, Bhava Chalit)
    bhava_sphuta = calculate_bhava_sphuta(lagna_info["longitude"], planets_enriched)
    d1_chart, d9_chart, chalit_chart = build_charts(lagna_info, planets_enriched, bhava_sphuta)

    # 4. Birth Panchangam & Avakahada Chakra
    sun_lon = next(p["longitude"] for p in planets_enriched if p["name_en"] == "Sun")
    moon_lon = next(p["longitude"] for p in planets_enriched if p["name_en"] == "Moon")
    panchangam = calculate_birth_panchangam(sun_lon, moon_lon, req.dob, lagna_info)

    # 5. Vimshottari Dasha
    dasha = calculate_vimshottari_dasha(moon_lon, req.dob)

    # 6. Current Gocharam
    moon_rashi_idx = int(moon_lon // 30)
    gocharam = analyze_gocharam(moon_rashi_idx)

    # 7. Astrological Yogas & Classical Dosha Analysis
    yogas = detect_yogas(lagna_info, planets_enriched)
    kuja_dosha = analyze_kuja_dosha(lagna_info, planets_enriched)
    kalasarpa_dosha = analyze_kalasarpa_dosha(lagna_info, planets_enriched)

    # 8. 337-Point Parashari Sarvashtakavarga (SAV)
    ashtakavarga = calculate_ashtakavarga(planets_enriched, lagna_info["rashi_index"])

    # 9. Classical Telugu Predictions (Lagna, Nakshatra, Rashi, Dasha)
    curr_d = dasha.get("current_dasha") or {}
    current_maha = curr_d.get("mahadasha_te", "దశ")
    current_bhukti = curr_d.get("antardasha_te", "భుక్తి")
    moon_nak, _ = get_nakshatra_and_pada(moon_lon)
    predictions = generate_predictions(
        lagna_idx=lagna_info["rashi_index"],
        nak_idx=moon_nak["index"],
        rashi_idx=moon_rashi_idx,
        current_maha=current_maha,
        current_bhukti=current_bhukti,
        gender=req.gender
    )

    # 10. Gender Specific Highlights
    gender_highlights = get_gender_specific_highlights(req.gender, lagna_info, planets_enriched)

    # 11. Vimshottari Dasha-Antardasha Classical Predictions
    dasha_analysis = generate_dasha_antardasha_analysis(dasha)

    # 12. Classical Astrological Tables (Full Parity with OnlineJyotish)
    classical_tables = {
        "ghata_chakra": calculate_ghata_chakra(moon_rashi_idx),
        "lucky_factors": calculate_lucky_factors(lagna_info, moon_rashi_idx),
        "jaimini_karakas": calculate_jaimini_karakas(planets_enriched),
        "maitri_chakra": calculate_maitri_chakra(planets_enriched),
        "planetary_aspects": calculate_planetary_aspects(planets_enriched, lagna_info),
        "gemstones_rudraksha": calculate_gemstones_and_rudraksha(lagna_info, moon_rashi_idx, moon_nak["index"]),
        "vastu_facing": calculate_vastu_house_facing(moon_rashi_idx)
    }

    # 13. Authentic Vedic Remedy Verification & Puja Recheck Engine
    remedy_verification = audit_all_common_pujas(
        lagna_info=lagna_info,
        planets=planets_enriched,
        dasha_data=dasha,
        panchangam=panchangam,
        gocharam=gocharam,
        kuja_data=kuja_dosha,
        kalasarpa_data=kalasarpa_dosha
    )

    # 14. Santana & Pregnancy Loss (గర్భస్రావ / సంతాన దోష విశ్లేషణ) Engine
    santana_analysis = analyze_santana_and_pregnancy_doshas(
        lagna_info=lagna_info,
        planets=planets_enriched,
        gender=req.gender
    )

    return KundaliResponse(
        input=req,
        ayanamsa_value=round(ayanamsa_val, 4),
        lagna=lagna_info,
        planets=planets_enriched,
        bhavas=bhavas_enriched,
        d1_chart=d1_chart,
        d9_chart=d9_chart,
        chalit_chart=chalit_chart,
        bhava_sphuta=bhava_sphuta,
        panchangam=panchangam,
        dasha=dasha,
        dasha_analysis=dasha_analysis,
        gocharam=gocharam,
        yogas=yogas,
        kuja_dosha=kuja_dosha,
        kalasarpa_dosha=kalasarpa_dosha,
        ashtakavarga=ashtakavarga,
        predictions=predictions,
        gender_highlights=gender_highlights,
        classical_tables=classical_tables,
        remedy_verification=remedy_verification,
        santana_analysis=santana_analysis,
    )


@router.post("/verify-remedy")
def verify_specific_remedy(req: BirthDetailsRequest):
    """
    Dedicated endpoint to verify any prescribed puja or remedy against
    classical Vedic Shastras for the native's chart.
    """
    # Reuse generation logic to get current chart state
    kundali = generate_kundali(req)
    return {
        "status": "success",
        "native_name": req.name,
        "lagna": kundali.lagna["rashi_name_te"],
        "rashi": kundali.panchangam.get("rashi", ""),
        "nakshatra": kundali.panchangam.get("nakshatra", ""),
        "remedy_verification": kundali.remedy_verification
    }


@router.post("/couple-analyze")
def analyze_couple(req: CoupleAnalysisRequest):
    """
    Joint Analysis of Husband & Wife Horoscopes:
    - Complete Kundali generation for Husband and Wife
    - Beeja Sphuta & Kshetra Sphuta joint fertility & Santana audit
    - Kuja Dosha Samyam (Mutual Mars affliction cancellation check)
    - Comparative Sarpa, Kala Sarpa, Pitru, and Shani doshas
    - Dharmashastric Karta (కర్త) designation and unified couple Parihara plan
    - Direct 1-click Muhurtam linkages
    """
    h_kundali = generate_kundali(req.husband)
    w_kundali = generate_kundali(req.wife)

    h_dict = h_kundali.model_dump() if hasattr(h_kundali, "model_dump") else h_kundali.dict()
    w_dict = w_kundali.model_dump() if hasattr(w_kundali, "model_dump") else w_kundali.dict()

    joint_result = analyze_couple_joint(h_dict, w_dict)

    return {
        "status": "success",
        "husband_kundali": h_dict,
        "wife_kundali": w_dict,
        "joint_analysis": joint_result
    }


@router.post("/family-audit")
def audit_family(req: FamilyAuditRequest):
    """
    Whole Family Horoscope Dosha Audit:
    - Computes Vedic birth chart for each family member
    - Member-by-member audit of Sarpa, Kuja, Kalasarpa, Pitru, Shani, Gandanta
    - Pinpoints who in the family carries which affliction
    - Designates Family Karta (కుటుంబ సంకల్ప కర్త)
    - Recommends Family Pariharas with direct 1-click Muhurtam linkages
    """
    members_data = []
    for m in req.members:
        b_req = BirthDetailsRequest(
            name=m.name,
            gender=m.gender,
            dob=m.dob,
            tob=m.tob,
            place_name=m.place_name,
            latitude=m.latitude,
            longitude=m.longitude,
            timezone_offset=m.timezone_offset,
            ayanamsa=m.ayanamsa
        )
        kundali = generate_kundali(b_req)
        k_dict = kundali.model_dump() if hasattr(kundali, "model_dump") else kundali.dict()
        m_info = m.model_dump() if hasattr(m, "model_dump") else m.dict()
        members_data.append({
            "member_info": m_info,
            "kundali": k_dict
        })

    family_audit = audit_family_doshas(members_data, family_name=req.family_name or "మా కుటుంబం")

    return {
        "status": "success",
        "family_audit": family_audit,
        "members_data": members_data
    }



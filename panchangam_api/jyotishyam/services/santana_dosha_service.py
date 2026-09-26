# -*- coding: utf-8 -*-
"""
Santana Dosha, Progeny & Pregnancy Loss (గర్భస్రావ / సంతాన దోష విశ్లేషణ) Engine.
Evaluates 5th House (Putra Sthana), Putrakaraka Jupiter, Beeja Sphuta, Kshetra Sphuta,
and prescribes authentic Shastric remedies (Naga Pratishtha, Ashlesha Bali, Rudra Pashupatam, Chandi, Santana Gopala)
with direct links to precise Muhurtam calculations.

Cites:
- బృహత్ పరాశర హోరాశాస్త్రం (Brihat Parashara Hora Shastra - సంతాన ప్రతిబంధక అధ్యాయం)
- ఫలదీపిక (Phaladeepika - అధ్యాయం 12)
- జాతకాభరణం (Jatakabharanam - గర్భధారణ & పుత్రఫల ప్రకరణం)
- జాతక పారిజాతం (Jataka Parijata)
"""

from typing import Dict, Any, List, Optional
from jyotishyam.services.kundali_calculator import RASHIS


def calculate_beeja_and_kshetra_sphuta(planets: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computes Beeja Sphuta (పురుష వీర్య బలం) and Kshetra Sphuta (స్త్రీ గర్భాశయ/క్షేత్ర బలం).
    Classical Formula (Phaladeepika Ch. 12 / BPHS):
    - Male Beeja Sphuta = (Sun + Venus + Jupiter) % 360
      Auspicious if in Odd sign and Odd navamsha (1, 3, 5, 7, 9, 11).
    - Female Kshetra Sphuta = (Moon + Mars + Jupiter) % 360
      Auspicious if in Even sign and Even navamsha (2, 4, 6, 8, 10, 12).
    """
    p_map = {p["name_en"]: p for p in planets}
    sun = p_map.get("Sun", {}).get("longitude", 0.0)
    venus = p_map.get("Venus", {}).get("longitude", 0.0)
    jupiter = p_map.get("Jupiter", {}).get("longitude", 0.0)
    moon = p_map.get("Moon", {}).get("longitude", 0.0)
    mars = p_map.get("Mars", {}).get("longitude", 0.0)

    # 1. Beeja Sphuta (Male)
    beeja_deg = (sun + venus + jupiter) % 360.0
    beeja_rashi_idx = int(beeja_deg // 30)
    # Navamsha index
    beeja_navamsha_idx = int((beeja_deg % 30.0) / (30.0 / 9.0))
    # Starting navamsha based on element
    # Fire/Earth/Air/Water signs start from Aries, Capricorn, Libra, Cancer
    elem_start = [0, 9, 6, 3][beeja_rashi_idx % 4]
    beeja_nav_rashi = (elem_start + beeja_navamsha_idx) % 12

    beeja_rashi_odd = (beeja_rashi_idx % 2 == 0) # 0-indexed: 0=Aries (Odd), 1=Taurus (Even)
    beeja_nav_odd = (beeja_nav_rashi % 2 == 0)

    if beeja_rashi_odd and beeja_nav_odd:
        beeja_status = "సంపూర్ణ బీజ బలం కలదు (Strong Male Virility)"
        beeja_badge = "success"
        beeja_desc = "బీజ స్పష్టం పురుష రాశి మరియు పురుష నవాంశలో ఉన్నందున సంతానోత్పత్తి శక్తి పరిపూర్ణంగా ఉన్నది."
    elif beeja_rashi_odd or beeja_nav_odd:
        beeja_status = "మధ్యమ బీజ బలం (Moderate - Minor Delay)"
        beeja_badge = "warning"
        beeja_desc = "బీజ స్పష్టంలో మిశ్రమ ప్రభావం ఉన్నది; కొద్దిపాటి జాప్యం లేదా వైద్య/దైవ సహాయంతో సంతాన ప్రాప్తి కలుగుతుంది."
    else:
        beeja_status = "బీజ దోషం / బలహీనత (Weak Virility / Dosha)"
        beeja_badge = "danger"
        beeja_desc = "బీజ స్పష్టం స్త్రీ రాశి మరియు స్త్రీ నవాంశలో పడినందున సంతాన ప్రతిబంధకాలు ఏర్పడును; వైదిక శాంతి ఆవశ్యకం."

    # 2. Kshetra Sphuta (Female)
    kshetra_deg = (moon + mars + jupiter) % 360.0
    kshetra_rashi_idx = int(kshetra_deg // 30)
    kshetra_navamsha_idx = int((kshetra_deg % 30.0) / (30.0 / 9.0))
    elem_start_k = [0, 9, 6, 3][kshetra_rashi_idx % 4]
    kshetra_nav_rashi = (elem_start_k + kshetra_navamsha_idx) % 12

    kshetra_rashi_even = (kshetra_rashi_idx % 2 == 1) # 1=Taurus, 3=Cancer (Even)
    kshetra_nav_even = (kshetra_nav_rashi % 2 == 1)

    if kshetra_rashi_even and kshetra_nav_even:
        kshetra_status = "సంపూర్ణ క్షేత్ర బలం కలదు (Fertile Womb / Strong Uterus)"
        kshetra_badge = "success"
        kshetra_desc = "క్షేత్ర స్పష్టం స్త్రీ రాశి మరియు స్త్రీ నవాంశలో ఉన్నందున గర్భధారణ సామర్థ్యం ఉత్తమంగా ఉన్నది."
    elif kshetra_rashi_even or kshetra_nav_even:
        kshetra_status = "మధ్యమ క్షేత్ర బలం (Moderate Fertility)"
        kshetra_badge = "warning"
        kshetra_desc = "గర్భధారణకు అనుకూలమైనప్పటికీ హార్మోన్ల సమతుల్యత మరియు గర్భరక్షణ స్తోత్ర పారాయణ అవసరం."
    else:
        kshetra_status = "క్షేత్ర దోషం / గర్భస్రావ సూచన (Weak Uterine Energy)"
        kshetra_badge = "danger"
        kshetra_desc = "క్షేత్ర స్పష్టం పురుష రాశి/నవాంశలలో పడినందున గర్భం నిలవకపోవడం (Miscarriage) లేదా జాప్యం జరగవచ్చు."

    return {
        "beeja_sphuta": {
            "degree": round(beeja_deg, 2),
            "rashi_name_te": RASHIS[beeja_rashi_idx]["name_te"],
            "status": beeja_status,
            "badge": beeja_badge,
            "description": beeja_desc
        },
        "kshetra_sphuta": {
            "degree": round(kshetra_deg, 2),
            "rashi_name_te": RASHIS[kshetra_rashi_idx]["name_te"],
            "status": kshetra_status,
            "badge": kshetra_badge,
            "description": kshetra_desc
        }
    }


def analyze_santana_and_pregnancy_doshas(
    lagna_info: Dict[str, Any],
    planets: List[Dict[str, Any]],
    gender: str = "female"
) -> Dict[str, Any]:
    """
    In-depth analysis of 5th House, Putrakaraka Jupiter, Garbhasrava (Miscarriage),
    and prescribes specific Vedic Remedies (Naga Pratishtha, Ashlesha Bali, Rudra Pashupatam, Chandi, Santana Gopala)
    along with direct Muhurtam Calculator linkages.
    """
    p_map = {p["name_en"]: p for p in planets}
    lagna_rashi = lagna_info["rashi_index"]

    # 5th House from Lagna
    fifth_rashi = (lagna_rashi + 4) % 12
    fifth_lord_en = RASHIS[fifth_rashi]["lord_en"]
    fifth_lord_te = RASHIS[fifth_rashi]["lord_te"]

    # Planets in 5th house
    occupants_5th = [p for p in planets if p.get("bhava") == 5]
    occ_names_te = [p.get("name_te", p.get("name_en", "")) for p in occupants_5th]

    fifth_lord_planet = p_map.get(fifth_lord_en, {})
    jupiter = p_map.get("Jupiter", {})
    rahu = p_map.get("Rahu", {})
    ketu = p_map.get("Ketu", {})
    mars = p_map.get("Mars", {})
    saturn = p_map.get("Saturn", {})
    sun = p_map.get("Sun", {})

    # Detect specific Santana Doshas
    doshas_detected = []

    # 1. SARPA SHAAPA / NAGA DOSHA (సర్ప శాపం / నాగ దోషం)
    # Rahu in 5th or aspecting 5th, or Rahu conjunct 5th lord, or Mars/Saturn in 5th with Rahu
    rahu_in_5th = rahu.get("bhava") == 5
    rahu_with_5th_lord = rahu.get("rashi_index") == fifth_lord_planet.get("rashi_index")
    if rahu_in_5th or rahu_with_5th_lord or (ketu.get("bhava") == 5):
        doshas_detected.append({
            "code": "naga_dosha",
            "name_te": "సర్ప శాప / నాగ దోషం (Sarpa Shaapa / Naga Dosha)",
            "impact_te": "సంతాన లేమి, గర్భధారణలో తీవ్ర జాప్యం, మరియు సంతాన ప్రతిబంధక స్వప్నాలు.",
            "astrological_reason": f"పంచమ స్థానంలో లేదా పంచమాధిపతితో రాహు/కేతువుల సంబంధం ఏర్పడినది (రాహువు: {rahu.get('bhava')}వ భావం, కేతువు: {ketu.get('bhava')}వ భావం).",
            "shastra_authority": "బృహత్ పరాశర హోరాశాస్త్రం (సంతాన ప్రతిబంధక అధ్యాయం) & జాతకాభరణం",
            "primary_remedy": {
                "name": "నాగ ప్రతిష్ఠ (Naga Pratishtha)",
                "event_type": "naga_pratishtha",
                "procedure": "కుక్కే సుబ్రహ్మణ్య, శ్రీకాళహస్తి లేదా పుణ్యక్షేత్రాలలో అశ్వత్థ వృక్ష సన్నిధిలో నాగ శిలా ప్రతిష్ఠ జరిపించి పాలాభిషేకం చేయాలి.",
                "mantra": "ఓం నమో భగవతే వాసుదేవాయ & నాగ స్తోత్రం",
                "japa_count": "రాహు జపం 18,000 లేదా నాగ గాయత్రి 10,000"
            },
            "secondary_remedy": {
                "name": "ఆశ్లేషా బలి పూజ (Ashlesha Bali)",
                "event_type": "ashlesha_bali",
                "procedure": "ఆశ్లేషా నక్షత్రం ఉన్న పవిత్ర దినాన సర్ప క్షేత్రంలో ఆశ్లేషా బలి పూజ చేయించడం వల్ల సర్ప దోషం నివృత్తి అగును."
            }
        })

    # 2. KUJA-KETU GARBHASRAVA DOSHA (గర్భస్రావ దోషం / Miscarriage & Heat Affliction)
    # Mars in 5th or aspecting 5th with Ketu / Rahu / Sun
    mars_in_5th = mars.get("bhava") == 5
    mars_aspects_5th = mars.get("bhava") in [2, 10, 11] # 4th, 7th, 8th aspects on 5th
    ketu_in_5th = ketu.get("bhava") == 5
    if (mars_in_5th or (mars_aspects_5th and (rahu_in_5th or ketu_in_5th))) or (mars_in_5th and ketu.get("rashi_index") == mars.get("rashi_index")):
        doshas_detected.append({
            "code": "garbhasrava_dosha",
            "name_te": "కుజ-కేతు గర్భస్రావ దోషం (Garbhasrava / Miscarriage Risk)",
            "impact_te": "గర్భం ధరించినప్పటికీ 1 నుండి 3వ నెలలోపు నిలవకపోవడం (గర్భస్రావం), రక్త/ఉష్ణ సంబంధిత సమస్యలు.",
            "astrological_reason": f"పంచమ స్థానంలో లేదా పంచమంపై కుజ-కేతువుల ఉష్ణ ప్రభావం ఉన్నది (కుజుడు: {mars.get('bhava')}వ భావం). శాస్త్ర ప్రకారం కుజుడు రక్తకారకుడు, కేతువు ఛేదనకారకుడు.",
            "shastra_authority": "జాతకాభరణం (గర్భధారణ ప్రకరణం) & ఫలదీపిక",
            "primary_remedy": {
                "name": "సుబ్రహ్మణ్య షష్ఠి వ్రతం & కుజ శాంతి (Subrahmanya Shashti)",
                "event_type": "kuja_shanti_subrahmanya",
                "procedure": "శుక్లపక్ష షష్ఠి తిథి నాడు సుబ్రహ్మణ్యేశ్వర స్వామి సన్నిధిలో పంచామృతాభిషేకం మరియు కుజ శాంతి హోమం నిర్వహించాలి.",
                "mantra": "శ్రీ గర్భరక్షాంబికా స్తోత్రం & సుబ్రహ్మణ్యాష్టకం",
                "japa_count": "కుజ జపం 10,000 సార్లు"
            },
            "secondary_remedy": {
                "name": "గర్భరక్షాంబికా అమ్మవారి ఆరాధన",
                "event_type": "kuja_shanti_subrahmanya",
                "procedure": "రోజూ నెయ్యి దీపారాధన చేసి గర్భరక్షాంబికా స్తోత్రం పఠించడం వల్ల గర్భం సంరక్షించబడుతుంది."
            }
        })

    # 3. GURU-CHANDAL / PUTRAKARAKA AFFLICTION (గురు-చాండాల / సంతాన కారక పీడ)
    # Jupiter in 6, 8, 12 or debilitated (Capricorn) or combust or conjunct Rahu
    jup_bhava = jupiter.get("bhava", 1)
    jup_debilitated = jupiter.get("dignity_en") == "Debilitated"
    jup_combust = jupiter.get("is_combust", False)
    jup_rahu = jupiter.get("rashi_index") == rahu.get("rashi_index")

    if (jup_bhava in [6, 8, 12] or jup_debilitated or jup_combust or jup_rahu) and len(doshas_detected) < 2:
        doshas_detected.append({
            "code": "guru_santana_dosha",
            "name_te": "సంతానకారక గురు పీడ (Putrakaraka Jupiter Affliction)",
            "impact_te": "సంతాన ప్రాప్తిలో తీవ్ర నిరీక్షణ, దైవానుగ్రహం లోపించడం, వైద్య ఫలితాలు ఆశించినంతగా లేకపోవడం.",
            "astrological_reason": f"సంతాన కారకుడైన బృహస్పతి {jup_bhava}వ భావంలో {'నీచ స్థితి' if jup_debilitated else ('అస్తంగత' if jup_combust else 'రాహు సంయోగం')}లో ఉన్నారు.",
            "shastra_authority": "బృహత్ పరాశర హోరాశాస్త్రం (పుత్రభావ ఫలం)",
            "primary_remedy": {
                "name": "సంతాన గోపాల హోమం / కృష్ణార్చన (Santana Gopala Homa)",
                "event_type": "santana_gopala",
                "procedure": "గురువారం నాడు వేద పండితులచే శ్రీకృష్ణునికి సంతాన గోపాల హోమం మరియు పాయస నైవేద్యం సమర్పించాలి.",
                "mantra": "ఓం శ్రీం హ్రీం క్లీం గ్లౌం దేవకీసుత గోవింద వాసుదేవ జగత్పతే దేహి మే తనయం కృష్ణ త్వామహం శరణం గతః",
                "japa_count": "సంతాన గోపాల మంత్ర జపం: 10,000 సార్లు"
            },
            "secondary_remedy": {
                "name": "గురు పాదుకా పూజ & విద్యాదానం",
                "event_type": "santana_gopala",
                "procedure": "ప్రతి గురువారం దక్షిణామూర్తి లేదా రాఘవేంద్ర స్వామి దర్శనం, పేద విద్యార్థులకు పుస్తకాలు/శనగలు దానం."
            }
        })

    # 4. SHANI / RUDRA SHAAPA (శని ప్రతిబంధకం / రుద్ర పాశుపతం)
    saturn_in_5th = saturn.get("bhava") == 5
    if saturn_in_5th and len(doshas_detected) < 3:
        doshas_detected.append({
            "code": "rudra_shaapa",
            "name_te": "శని ప్రతిబంధక దోషం / రుద్ర కోపం (Saturn 5th House Obstacle)",
            "impact_te": "కారణం లేని జాప్యం, వైద్య పరీక్షలన్నీ బాగున్నా గర్భధారణ కాకపోవడం, నిరాశానిస్పృహలు.",
            "astrological_reason": f"శని భగవానుడు 5వ భావంలో ({RASHIS[fifth_rashi]['name_te']} రాశి) స్థాన బంధనం కలిగించి ఉన్నారు.",
            "shastra_authority": "జాతకాభరణం & ఫలదీపిక",
            "primary_remedy": {
                "name": "రుద్ర పాశుపత హోమం / మహా రుద్రాభిషేకం (Rudra Pashupata Homa)",
                "event_type": "rudra_pashupatam",
                "procedure": "త్రయోదశి ప్రదోష వేళ లేదా మాస శివరాత్రి నాడు ఏకాదశ రుద్రాభిషేకం లేదా పాశుపత హోమం జరిపించాలి.",
                "mantra": "శ్రీ రుద్ర నమక-చమక పారాయణం & మహా మృత్యుంజయ మంత్రం",
                "japa_count": "మృత్యుంజయ జపం: 11,000"
            },
            "secondary_remedy": {
                "name": "శివాలయంలో బిల్వార్చన",
                "event_type": "rudra_pashupatam",
                "procedure": "సోమవారం నాడు ఆవు పాలతో శివలింగానికి అభిషేకం చేసి మారేడు దళాలతో పూజించాలి."
            }
        })

    # 5. CHANDI HOMA / MATRU SHAAPA
    moon_in_5th = p_map.get("Moon", {}).get("bhava") == 5
    if (moon_in_5th and (mars_in_5th or saturn_in_5th)) and len(doshas_detected) < 3:
        doshas_detected.append({
            "code": "matru_shaapa",
            "name_te": "మాతృ శాపం / నవగ్రహ పీడ (Chandi Remedy)",
            "impact_te": "మానసిక ఆందోళన, హార్మోన్ల హెచ్చుతగ్గులు, మరియు నరదృష్టి ప్రభావం.",
            "astrological_reason": "చంద్రుడు 5వ భావంలో పాప గ్రహ సంయోగం పొంది ఉన్నారు.",
            "shastra_authority": "బృహత్ పరాశర హోరాశాస్త్రం",
            "primary_remedy": {
                "name": "చండీ హోమం / దుర్గా సప్తశతి (Chandi Homa)",
                "event_type": "chandi_homam",
                "procedure": "అష్టమి లేదా నవమి తిథి నాడు చండీ హోమం నిర్వహించి సువాసినులకు తాంబూలం సమర్పించాలి.",
                "mantra": "దుర్గా కవచం & సప్తశతి శ్లోకాలు",
                "japa_count": "నవార్ణ మంత్ర జపం: 10,000"
            },
            "secondary_remedy": {
                "name": "లలితా సహస్రనామ పారాయణ",
                "event_type": "chandi_homam",
                "procedure": "శుక్రవారం అమ్మవారికి కుంకుమార్చన చేయడం."
            }
        })

    # Default Auspicious Outlook if no severe dosha detected
    if len(doshas_detected) == 0:
        overall_status_te = "సంతాన యోగం అనుకూలం (Favorable Progeny Indicators)"
        overall_badge = "success"
        overall_desc = f"5వ భావం ({RASHIS[fifth_rashi]['name_te']} రాశి, అధిపతి: {fifth_lord_te}) మరియు గురు బలం శుభప్రదంగా ఉన్నాయి. తీవ్రమైన సర్ప లేదా గర్భస్రావ దోషాలు లేవు. సాధారణ ఇష్టదైవ ప్రార్థనతో సత్సంతాన ప్రాప్తి కలుగును."
        primary_recommended_parihara = "సంతాన గోపాల కృష్ణార్చన"
        recommended_event_type = "santana_gopala"
    else:
        overall_status_te = "శాస్త్రోక్త శాంతి పరిహారాలు ఆవశ్యకం (Parihara Recommended)"
        overall_badge = "warning"
        overall_desc = "జాతకంలో కొన్ని విశిష్ట సర్ప/కుజ/గురు ప్రతిబంధకాలు ఉన్నందున శాస్త్రోక్తమైన నాగ ప్రతిష్ఠ, ఆశ్లేషా బలి, లేదా సంతాన గోపాల హోమాన్ని శుభ ముహూర్తంలో ఆచరించడం ద్వారా గర్భ రక్షణ మరియు సంతాన సౌఖ్యం సిద్ధిస్తాయి."
        primary_recommended_parihara = doshas_detected[0]["primary_remedy"]["name"]
        recommended_event_type = doshas_detected[0]["primary_remedy"]["event_type"]

    # Calculate Beeja / Kshetra Sphutas
    sphutas = calculate_beeja_and_kshetra_sphuta(planets)

    return {
        "fifth_house_info": {
            "rashi_name_te": RASHIS[fifth_rashi]["name_te"],
            "lord_te": fifth_lord_te,
            "lord_en": fifth_lord_en,
            "occupants": occ_names_te if occ_names_te else ["ఎవరూ లేరు (శుభప్రదం)"],
            "jupiter_status": f"{jupiter.get('rashi_name_te', '')}లో ({jupiter.get('dignity_te', 'సాధారణం')})"
        },
        "overall_status_te": overall_status_te,
        "overall_badge": overall_badge,
        "overall_description": overall_desc,
        "primary_recommended_parihara": primary_recommended_parihara,
        "recommended_event_type": recommended_event_type,
        "sphutas": sphutas,
        "doshas_detected": doshas_detected,
        "shastric_note": "ప్రాచీన హోరా శాస్త్రాల ప్రకారం శారీరక వైద్యంతో పాటు శాస్త్రోక్త దైవిక పరిహారాలను శుభ ముహూర్తంలో ఆచరించినప్పుడు సంపూర్ణ సంతాన భాగ్యం కలుగుతుంది."
    }

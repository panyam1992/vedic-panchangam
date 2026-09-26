# -*- coding: utf-8 -*-
"""
Vedic Joint & Whole Family Dosha Audit Service (దంపతుల & సకుటుంబ సమగ్ర దోష పరిశీలన & పరిహార నిర్ణయం).

Provides authoritative classical Shastric analysis for:
1. Couple Joint Jathakam (భర్త & భార్య సంయుక్త జాతకం):
   - Beeja Sphuta (Husband) vs Kshetra Sphuta (Wife) - Santana obstacles & miscarriage evaluation.
   - Kuja Dosha Samyam (కుజ దోష సామ్యం - mutual cancellation of Mars affliction).
   - Comparative Sarpa, Kala Sarpa, Pitru, and Shani doshas.
   - Karta (కర్త) determination and unified couple Parihara action plan.
2. Whole Family Jathakam (సకుటుంబ సమగ్ర దోష పరిశీలన):
   - Member-by-member dosha audit (Lagna, Rashi, Nakshatra, Sarpa, Kuja, Kalasarpa, Pitru, Shani, Gandanta).
   - Identifies exactly WHO carries which affliction in the family.
   - Designates the Family Karta (కుటుంబ సంకల్ప కర్త) according to Dharmashastra.
   - Prescribes the precise Shastric Parihara with direct 1-click Muhurtam linkages.

Cites:
- బృహత్ పరాశర హోరాశాస్త్రం (BPHS Ch. 83-84: Santana & Kuja Dosha Samyam, Pitru Shapa)
- ముహూర్త రత్నావళి (Muhurtha Ratnavali: Kuja Dosha Samyam - దంపత్యోః కుజదోషశ్చేత్ సమబలేన శమ్యతి)
- ఫలదీపిక (Phaladeepika Ch. 12-13: Stri Jataka & Beeja-Kshetra)
- జాతకాభరణం (Jatakabharanam: Garbhadharana & Dosha Parihara)
- ధర్మసింధు & నిర్ణయసింధు (Dharmasindhu: Family Sankalpa & Karta Vidhi)
"""

from typing import Dict, Any, List, Optional
from jyotishyam.services.kundali_calculator import RASHIS


def detect_pitru_dosha(lagna_info: Dict[str, Any], planets: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Detects Pitru Dosha (పితృ దోషం / పితృ శాపం) based on:
    - Sun (Pitrukaraka) afflicted by Rahu, Ketu, or Saturn
    - 9th house (Pitru Sthana) afflicted by Rahu or Ketu
    - 9th lord afflicted or in 6, 8, 12
    Cites: Brihat Parashara Hora Shastra (పితృ శాప అధ్యాయం)
    """
    p_map = {p.get("name_en"): p for p in planets}
    sun = p_map.get("Sun", {})
    rahu = p_map.get("Rahu", {})
    ketu = p_map.get("Ketu", {})
    saturn = p_map.get("Saturn", {})
    jupiter = p_map.get("Jupiter", {})

    lagna_rashi = lagna_info.get("rashi_index", 0)
    ninth_rashi = (lagna_rashi + 8) % 12
    ninth_lord_en = RASHIS[ninth_rashi]["lord_en"]
    ninth_lord_te = RASHIS[ninth_rashi]["lord_te"]
    ninth_lord_planet = p_map.get(ninth_lord_en, {})

    sun_rashi = sun.get("rashi_index", -1)
    sun_bhava = sun.get("bhava", -1)
    rahu_rashi = rahu.get("rashi_index", -2)
    rahu_bhava = rahu.get("bhava", -2)
    ketu_rashi = ketu.get("rashi_index", -3)
    saturn_rashi = saturn.get("rashi_index", -4)

    reasons = []
    severity = "none"

    # 1. Sun conjunct Rahu or Ketu (Surya Grahan / Pitru Shapa)
    if sun_rashi == rahu_rashi:
        reasons.append("రవి-రాహు సంయోగం (సూర్య గ్రహణ దోషం / పితృ శాపం). పితృకారకుడైన సూర్యునిపై రాహు ప్రభావం ఉన్నది.")
        severity = "severe" if sun_bhava in [1, 5, 9, 10] else "moderate"
    elif sun_rashi == ketu_rashi:
        reasons.append("రవి-కేతు సంయోగం వలన పితృ స్థానంలో ఛేదన ప్రభావం ఏర్పడినది.")
        severity = "moderate"

    # 2. Sun conjunct Saturn (Surya-Shani enmity)
    if sun_rashi == saturn_rashi:
        reasons.append("రవి-శని సంయోగం (పితృ-పుత్ర గ్రహ వైరం). తండ్రీకొడుకుల మధ్య అభిప్రాయ భేదాలు లేదా పిత్రార్జితంలో ఆటంకాలు.")
        if severity == "none":
            severity = "moderate"

    # 3. Rahu or Ketu in 9th house (Bhagya / Pitru Sthana)
    if rahu_bhava == 9:
        reasons.append("9వ భావం (పితృ స్థానం)లో రాహువు స్థితి. పితృ దేవతల ఆశీర్వాదంలో లోపం లేదా పూర్వీకుల శాంతి లోపాలు.")
        severity = "severe" if severity != "none" else "moderate"
    elif ketu.get("bhava") == 9:
        reasons.append("9వ భావంలో కేతువు స్థితి. ఆధ్యాత్మిక పురోగతి ఉన్నప్పటికీ పితృ కర్మలలో విస్మరణ సూచన.")
        if severity == "none":
            severity = "mild"

    # 4. 9th lord in 6, 8, 12 or with Rahu
    ninth_lord_bhava = ninth_lord_planet.get("bhava", -1)
    if ninth_lord_bhava in [6, 8, 12] and severity != "none":
        reasons.append(f"9వ అధిపతి ({ninth_lord_te}) {ninth_lord_bhava}వ త్రిక స్థానంలో బలహీనపడి ఉన్నారు.")

    # Mitigation by Jupiter
    if jupiter and severity != "none":
        jup_dist = ((jupiter.get("rashi_index", 0) - sun_rashi) % 12) + 1
        if jup_dist in [1, 5, 7, 9]:
            reasons.append("రవిపై దేవగురు బృహస్పతి శుభ దృష్టి ఉన్నందున పితృ దోష తీవ్రత గణనీయంగా తగ్గినది (దోష శమనం).")
            if severity == "severe":
                severity = "moderate"
            elif severity == "moderate":
                severity = "mild"

    has_dosha = severity in ["moderate", "severe", "mild"]

    if not has_dosha:
        status_te = "పితృ దోషం లేదు (No Pitru Dosha)"
        badge = "success"
        summary_te = "జాతకంలో రవి మరియు 9వ భావాలు శుభ స్థితిలో ఉన్నందున ఎటువంటి పితృ దోషం లేదు."
        primary_remedy = "నిత్య పితృ ప్రార్థన, అమావాస్య తర్పణం."
        event_type = "satyanarayana_vrata"
    elif severity == "mild":
        status_te = "స్వల్ప పితృ దోషం (Mild Pitru Dosha)"
        badge = "info"
        summary_te = "స్వల్ప పితృ ప్రభావం ఉన్నది; సాధారణ అమావాస్య తర్పణం, అన్నదానంతో దోష నివృత్తి అగును."
        primary_remedy = "దర్శ అమావాస్య నాడు తిల తర్పణం & గోసేవ."
        event_type = "satyanarayana_vrata"
    elif severity == "moderate":
        status_te = "మధ్యమ పితృ దోషం (Moderate Pitru Dosha)"
        badge = "warning"
        summary_te = "పితృకారక రవి లేదా 9వ భావంపై ఛాయాగ్రహ ప్రభావం ఉన్నందున పితృ శాంతి ఆవశ్యకం."
        primary_remedy = "తిల హోమం లేదా మహాలయ పక్ష శ్రాద్ధం & బ్రాహ్మణ సమారాధన."
        event_type = "tila_homam_pitru"
    else:
        status_te = "తీవ్ర పితృ దోషం / పితృ శాపం (Severe Pitru Shapa)"
        badge = "danger"
        summary_te = "రవి-రాహు సంయోగం లేదా 9వ భావంలో రాహు స్థితి వలన తీవ్ర పితృ శాపం సూచించబడుచున్నది; శాస్త్రోక్త తిల హోమం లేదా నారాయణ బలి చేయాలి."
        primary_remedy = "నారాయణ బలి / గయా శ్రాద్ధం లేదా శ్రీకాళహస్తి/గోకర్ణ క్షేత్రంలో తిల హోమం."
        event_type = "tila_homam_pitru"

    return {
        "has_dosha": has_dosha,
        "severity": severity,
        "status_te": status_te,
        "badge": badge,
        "summary_te": summary_te,
        "reasons": reasons,
        "primary_remedy": primary_remedy,
        "event_type": event_type,
        "shastra_authority": "బృహత్ పరాశర హోరాశాస్త్రం (పితృ శాప అధ్యాయం) & ధర్మసింధు"
    }


def detect_sarpa_naga_dosha(lagna_info: Dict[str, Any], planets: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Detects Sarpa / Naga Dosha (సర్ప దోషం / నాగ దోషం) based on:
    - Rahu in 1, 5, 7, 8
    - Rahu conjunct Moon, Jupiter, or 5th lord
    - Ketu in 5th or 7th
    Cites: Brihat Parashara Hora Shastra & Jatakabharanam
    """
    p_map = {p.get("name_en"): p for p in planets}
    rahu = p_map.get("Rahu", {})
    ketu = p_map.get("Ketu", {})
    moon = p_map.get("Moon", {})
    jupiter = p_map.get("Jupiter", {})

    lagna_rashi = lagna_info.get("rashi_index", 0)
    fifth_rashi = (lagna_rashi + 4) % 12
    fifth_lord_en = RASHIS[fifth_rashi]["lord_en"]
    fifth_lord = p_map.get(fifth_lord_en, {})

    rahu_bhava = rahu.get("bhava", -1)
    ketu_bhava = ketu.get("bhava", -1)
    rahu_rashi = rahu.get("rashi_index", -1)

    reasons = []
    severity = "none"

    # 1. Rahu in 5th house (Santana Pratibandhaka / Sarpa Shapa)
    if rahu_bhava == 5 or (fifth_lord and fifth_lord.get("rashi_index") == rahu_rashi):
        reasons.append("పంచమ స్థానంలో లేదా పంచమాధిపతితో రాహువు స్థితి (సర్ప శాపం - సంతాన ప్రతిబంధకం).")
        severity = "severe"
    elif ketu_bhava == 5:
        reasons.append("పంచమ స్థానంలో కేతువు స్థితి (గర్భధారణలో జాప్యం లేదా ఆందోళన).")
        severity = "moderate"

    # 2. Rahu in 7th or 8th house (Daampatya / Kalathra Sarpa Dosha)
    if rahu_bhava in [7, 8]:
        reasons.append(f"లగ్నం నుండి {rahu_bhava}వ స్థానంలో రాహువు స్థితి (దాంపత్య కలహాలు, ఆరోగ్య చికాకులు).")
        if severity != "severe":
            severity = "moderate"
    elif ketu_bhava in [7, 8]:
        reasons.append(f"లగ్నం నుండి {ketu_bhava}వ స్థానంలో కేతువు స్థితి.")
        if severity == "none":
            severity = "mild"

    # 3. Rahu in 1st house (Janma Rahu)
    if rahu_bhava == 1 and severity == "none":
        reasons.append("లగ్నంలో రాహువు స్థితి (మానసిక చంచలత్వం, తల తిరగడం, అభద్రతా భావం).")
        severity = "mild"

    # 4. Rahu conjunct Moon or Jupiter (Guru Chandal / Chandra Grahan)
    if moon and moon.get("rashi_index") == rahu_rashi and severity == "none":
        reasons.append("చంద్ర-రాహు సంయోగం (మానసిక ఆందోళన, నరదృష్టి, భయాలు).")
        severity = "mild"
    if jupiter and jupiter.get("rashi_index") == rahu_rashi and severity == "none":
        reasons.append("గురు-రాహు సంయోగం (గురు చాండాల యోగం - దైవానుగ్రహ ప్రతిబంధకం).")
        severity = "moderate"

    has_dosha = severity in ["mild", "moderate", "severe"]

    if not has_dosha:
        status_te = "సర్ప దోషం లేదు (No Sarpa Dosha)"
        badge = "success"
        summary_te = "జాతకంలో రాహు-కేతువుల శుభ స్థితి వలన ఎటువంటి నాగ/సర్ప దోషం లేదు."
        primary_remedy = "నిత్య శివారాధన లేదా సుబ్రహ్మణ్య ప్రార్థన."
        event_type = "satyanarayana_vrata"
    elif severity == "mild":
        status_te = "స్వల్ప నాగ దోషం (Mild Naga Dosha)"
        badge = "info"
        summary_te = "స్వల్ప ఛాయాగ్రహ ప్రభావం కలదు; ఇంట్లోనే సుబ్రహ్మణ్యాష్టకం లేదా నాగ స్తోత్ర పారాయణ సరిపోతుంది."
        primary_remedy = "మంగళవారం లేదా శుక్ల పంచమి నాడు సుబ్రహ్మణ్య దర్శనం, పాలాభిషేకం."
        event_type = "ashlesha_bali"
    elif severity == "moderate":
        status_te = "మధ్యమ సర్ప దోషం (Moderate Sarpa Dosha)"
        badge = "warning"
        summary_te = "వివాహ లేదా దాంపత్యంలో చిన్నపాటి చికాకులు; శాస్త్రోక్త ఆశ్లేషా బలి లేదా సుబ్రహ్మణ్య పూజ శ్రేయస్కరం."
        primary_remedy = "ఆశ్లేషా నక్షత్రం ఉన్న దినాన ఆశ్లేషా బలి లేదా సర్ప సూక్త శాంతి."
        event_type = "ashlesha_bali"
    else:
        status_te = "తీవ్ర సర్ప శాపం / నాగ దోషం (Severe Sarpa Shapa)"
        badge = "danger"
        summary_te = "పంచమ స్థానంలో రాహువు ఉండటం వలన తీవ్ర సర్ప శాపం ఏర్పడినది; సంతాన సౌఖ్యం కొరకు నాగ ప్రతిష్ఠ ఆవశ్యకం."
        primary_remedy = "కుక్కే సుబ్రహ్మణ్య, శ్రీకాళహస్తి లేదా పుణ్యక్షేత్రాలలో శాస్త్రోక్త నాగ ప్రతిష్ఠ & పాలాభిషేకం."
        event_type = "naga_pratishtha"

    return {
        "has_dosha": has_dosha,
        "severity": severity,
        "status_te": status_te,
        "badge": badge,
        "summary_te": summary_te,
        "reasons": reasons,
        "primary_remedy": primary_remedy,
        "event_type": event_type,
        "shastra_authority": "బృహత్ పరాశర హోరాశాస్త్రం (సంతాన ప్రతిబంధక అధ్యాయం)"
    }


def analyze_couple_joint(husband_kundali: Dict[str, Any], wife_kundali: Dict[str, Any]) -> Dict[str, Any]:
    """
    Synthesizes Husband & Wife charts jointly into a unified verdict:
    1. Santana & Beeja/Kshetra Sphuta Joint Audit (Brihat Parashara 83, Phaladeepika 12)
    2. Kuja Dosha Samyam (కుజ దోష సామ్య విశ్లేషణ - Muhurtha Ratnavali)
    3. Joint Sarpa, Pitru, and Kala Sarpa Dosha Matrix
    4. Designation of Primary Karta (కర్త) and Unified Parihara Plan
    5. Direct 1-click Muhurtam linkages
    """
    h_name = husband_kundali.get("input", {}).get("name", "భర్త")
    w_name = wife_kundali.get("input", {}).get("name", "భార్య")

    # 1. Santana & Beeja / Kshetra Sphutas
    h_santana = husband_kundali.get("santana_analysis", {})
    w_santana = wife_kundali.get("santana_analysis", {})

    h_beeja = h_santana.get("sphutas", {}).get("beeja_sphuta", {})
    w_kshetra = w_santana.get("sphutas", {}).get("kshetra_sphuta", {})

    h_beeja_status = h_beeja.get("status", "మధ్యమ బీజ బలం")
    h_beeja_badge = h_beeja.get("badge", "warning")
    w_kshetra_status = w_kshetra.get("status", "మధ్యమ క్షేత్ర బలం")
    w_kshetra_badge = w_kshetra.get("badge", "warning")

    h_has_santana_dosha = len(h_santana.get("doshas_detected", [])) > 0 or h_beeja_badge == "danger"
    w_has_santana_dosha = len(w_santana.get("doshas_detected", [])) > 0 or w_kshetra_badge == "danger"

    # Identify who carries the santana obstacle
    if not h_has_santana_dosha and not w_has_santana_dosha:
        santana_joint_verdict = "ఇద్దరి జాతకాలలో సంతాన యోగం అనుకూలంగా ఉన్నది (Both Charts Favorable)"
        santana_joint_badge = "success"
        santana_joint_who = "దోష రహితం — ఇద్దరికీ శుభప్రదం"
        santana_joint_desc = f"భర్త ({h_name}) బీజ స్పష్టం మరియు భార్య ({w_name}) క్షేత్ర స్పష్టం రెండూ శాస్త్రోక్తంగా బలవత్తరంగా ఉన్నాయి. తీవ్రమైన సర్ప లేదా గర్భస్రావ దోషాలు లేవు. సాధారణ ఇష్టదైవ ఆరాధనతో సత్సంతాన ప్రాప్తి కలుగుతుంది."
        santana_remedy = "సంతాన గోపాల కృష్ణార్చన"
        santana_event_type = "santana_gopala"
        santana_karta = "ఉభయులు సంయుక్తంగా (Jointly)"
    elif h_has_santana_dosha and not w_has_santana_dosha:
        santana_joint_verdict = f"ప్రతిబంధకం ప్రధానంగా భర్త ({h_name}) జాతకంలో కలదు"
        santana_joint_badge = "warning"
        santana_joint_who = f"భర్త ({h_name}) జాతకంలో బీజ లోపం / సర్ప శాపం"
        h_dosha_names = [d.get("name_te", "") for d in h_santana.get("doshas_detected", [])]
        dosha_str = ", ".join(h_dosha_names) if h_dosha_names else "బీజ స్పష్ట బలహీనత"
        santana_joint_desc = f"భార్య ({w_name}) క్షేత్ర స్పష్టం పరిపూర్ణంగా ఉన్నప్పటికీ, భర్త ({h_name}) జాతకంలో {dosha_str} కలదు. దీని వలన సంతాన ప్రాప్తిలో జాప్యం ఏర్పడుచున్నది. భర్త ప్రధాన సంకల్ప కర్తగా ఉండి శాస్త్రోక్త పరిహారం జరిపించాలి."
        primary_dosha = h_santana.get("doshas_detected", [{}])[0]
        santana_remedy = primary_dosha.get("primary_remedy", {}).get("name", "నాగ ప్రతిష్ఠ / సంతాన గోపాల హోమం")
        santana_event_type = primary_dosha.get("primary_remedy", {}).get("event_type", "naga_pratishtha")
        santana_karta = f"భర్త ({h_name}) ప్రధాన కర్తగా (భార్య సమేతంగా)"
    elif not h_has_santana_dosha and w_has_santana_dosha:
        santana_joint_verdict = f"ప్రతిబంధకం ప్రధానంగా భార్య ({w_name}) జాతకంలో కలదు"
        santana_joint_badge = "warning"
        santana_joint_who = f"భార్య ({w_name}) జాతకంలో క్షేత్ర లోపం / గర్భస్రావ సూచన"
        w_dosha_names = [d.get("name_te", "") for d in w_santana.get("doshas_detected", [])]
        dosha_str = ", ".join(w_dosha_names) if w_dosha_names else "క్షేత్ర స్పష్ట బలహీనత"
        santana_joint_desc = f"భర్త ({h_name}) బీజ బలం బాగున్నప్పటికీ, భార్య ({w_name}) జాతకంలో {dosha_str} సూచించబడుచున్నది (గర్భం నిలవకపోవడం లేదా ఉష్ణ/రక్త ప్రభావం). భార్య రక్షణ కొరకు గర్భరక్షాంబికా ఆరాధన లేదా సుబ్రహ్మణ్య షష్ఠి శాంతి నిర్వహించాలి."
        primary_dosha = w_santana.get("doshas_detected", [{}])[0]
        santana_remedy = primary_dosha.get("primary_remedy", {}).get("name", "సుబ్రహ్మణ్య షష్ఠి వ్రతం & గర్భరక్షాంబికా పూజ")
        santana_event_type = primary_dosha.get("primary_remedy", {}).get("event_type", "kuja_shanti_subrahmanya")
        santana_karta = f"భార్య ({w_name}) ప్రధాన సంకల్పంతో (భర్త సమేతంగా)"
    else:
        santana_joint_verdict = "ఉభయుల (భర్త & భార్య) జాతకాలలో సంయుక్త ప్రతిబంధకాలు కలవు"
        santana_joint_badge = "danger"
        santana_joint_who = "దంపతులిద్దరి జాతకాలలో దోషాలు (Joint Affliction)"
        santana_joint_desc = f"భర్త ({h_name}) జాతకంలో బీజ స్పష్టం/సర్ప ప్రభావం, మరియు భార్య ({w_name}) జాతకంలో క్షేత్ర స్పష్టం/కుజ ప్రభావం రెండూ ఉన్నాయి. దీని వల్ల తీవ్ర నిరీక్షణ ఏర్పడుతుంది. ప్రాచీన బృహత్ పరాశర హోరాశాస్త్ర ప్రకారం దంపతులు సంయుక్తంగా నాగ ప్రతిష్ఠ మరియు సంతాన గోపాల హోమాన్ని నిర్వహించాలి."
        santana_remedy = "సకుటుంబ నాగ ప్రతిష్ఠ & సంతాన గోపాల హోమం"
        santana_event_type = "naga_pratishtha"
        santana_karta = "దంపతులిద్దరూ సమాన సంకల్ప కర్తలుగా (Joint Performers)"

    # 2. Kuja Dosha Samyam (కుజ దోష సామ్య విశ్లేషణ - Muhurtha Ratnavali & BPHS)
    h_kuja = husband_kundali.get("kuja_dosha", {})
    w_kuja = wife_kundali.get("kuja_dosha", {})

    h_kuja_active = h_kuja.get("has_dosha", False) and h_kuja.get("severity") == "present"
    w_kuja_active = w_kuja.get("has_dosha", False) and w_kuja.get("severity") == "present"

    if h_kuja_active and w_kuja_active:
        kuja_samya_status = "samya_neutralized"
        kuja_samya_badge = "success"
        kuja_samya_title = "కుజ దోష సామ్యం — దోషం పరస్పరం రద్దయినది (Mutual Neutralization)!"
        kuja_samya_desc = (
            f"భర్త ({h_name}) జాతకంలో మరియు భార్య ({w_name}) జాతకంలో ఇద్దరికీ సమానంగా కుజదోషం ఉన్నది. "
            "ముహూర్త రత్నావళి మరియు బృహత్ పరాశర హోరాశాస్త్ర ప్రమాణం ప్రకారం: 'దంపత్యోః కుజదోషశ్చేత్ సమబలేన శమ్యతి' — "
            "ఉభయుల కుజ ప్రభావాలు పరస్పరం సమతుల్యమై దోషం రద్దవుతుంది (Neutralize). కాబట్టి ఎటువంటి ఖరీదైన కుజదోష పూజలు చేయనక్కర్లేదు."
        )
        kuja_puja_needed = False
    elif h_kuja_active and not w_kuja_active:
        kuja_samya_status = "husband_only"
        kuja_samya_badge = "warning"
        kuja_samya_title = f"భర్త ({h_name}) జాతకంలో మాత్రమే కుజదోషం కలదు"
        kuja_samya_desc = (
            f"భర్త జాతకంలో {h_kuja.get('kuja_from_lagna')}వ స్థానంలో కుజుడు ఉండడం వల్ల కుజదోషం ఉన్నది; "
            f"భార్య ({w_name}) జాతకంలో కుజదోషం లేదు. కాబట్టి దాంపత్య సౌఖ్యం కోసం భర్త పేరిట సుబ్రహ్మణ్యారాధన శ్రేయస్కరం."
        )
        kuja_puja_needed = True
    elif not h_kuja_active and w_kuja_active:
        kuja_samya_status = "wife_only"
        kuja_samya_badge = "warning"
        kuja_samya_title = f"భార్య ({w_name}) జాతకంలో మాత్రమే కుజదోషం కలదు"
        kuja_samya_desc = (
            f"భార్య జాతకంలో {w_kuja.get('kuja_from_lagna')}వ స్థానంలో కుజుడు ఉండడం వల్ల కుజదోషం ఉన్నది; "
            f"భర్త ({h_name}) జాతకంలో కుజదోషం లేదు. కాబట్టి దాంపత్య సామరస్యం కోసం భార్య పేరిట స్కంద షష్ఠి వ్రతం శ్రేయస్కరం."
        )
        kuja_puja_needed = True
    else:
        kuja_samya_status = "none"
        kuja_samya_badge = "success"
        kuja_samya_title = "దంపతులిద్దరికీ కుజదోషం లేదు (No Kuja Dosha)"
        kuja_samya_desc = "భర్త మరియు భార్య ఇద్దరి జాతకాలలోనూ కుజదోషం వర్తించదు లేదా శాస్త్రోక్త మినహాయింపుల ద్వారా దోషభంగం సిద్ధించినది."
        kuja_puja_needed = False

    # 3. Pitru Dosha & Sarpa Dosha Checks
    h_lagna = husband_kundali.get("lagna", {})
    w_lagna = wife_kundali.get("lagna", {})
    h_planets = husband_kundali.get("planets", [])
    w_planets = wife_kundali.get("planets", [])

    h_pitru = detect_pitru_dosha(h_lagna, h_planets)
    w_pitru = detect_pitru_dosha(w_lagna, w_planets)
    h_sarpa = detect_sarpa_naga_dosha(h_lagna, h_planets)
    w_sarpa = detect_sarpa_naga_dosha(w_lagna, w_planets)

    # 4. Synthesize Unified Couple Parihara Plan
    joint_pariharas = []

    # Priority 1: Santana / Naga Pratishtha
    if santana_joint_badge in ["warning", "danger"]:
        joint_pariharas.append({
            "priority": "1 (అత్యంత ముఖ్యం)",
            "title": santana_remedy,
            "event_type": santana_event_type,
            "for_whom": santana_joint_who,
            "karta": santana_karta,
            "timeframe_te": "రాబోయే 3 నుండి 6 నెలల లోపు (గర్భధారణ ప్రయత్నాలకు పూర్వమే ఆచరించుట పరమ శ్రేష్ఠం)",
            "ideal_days_range": 90,
            "urgency": "అత్యవసరం (High Priority)",
            "procedure": "శుభ ముహూర్తంలో పుణ్యక్షేత్రంలో అశ్వత్థ వృక్ష సన్నిధిలో నాగ ప్రతిష్ఠ లేదా ఇంట్లో సంతాన గోపాల హోమం నిర్వహించాలి.",
            "mantra": "ఓం శ్రీం హ్రీం క్లీం గ్లౌం దేవకీసుత గోవింద వాసుదేవ జగత్పతే దేహి మే తనయం కృష్ణ త్వామహం శరణం గతః",
            "shastra_quote": "ఫలదీపిక & బృహత్ పరాశర హోరాశాస్త్రం (సంతాన ప్రతిబంధక పరిహార ప్రకరణం)"
        })

    # Priority 2: Pitru Shanti
    if h_pitru.get("has_dosha") or w_pitru.get("has_dosha"):
        pitru_who = f"భర్త ({h_name})" if h_pitru.get("has_dosha") else f"భార్య ({w_name})"
        joint_pariharas.append({
            "priority": "2 (పితృ తర్పణం)",
            "title": "తిల హోమం / పితృ తర్పణ శాంతి (Tila Homa)",
            "event_type": "tila_homam_pitru",
            "for_whom": f"{pitru_who} జాతకంలో పితృ దోష సూచన",
            "karta": f"భర్త ({h_name}) ప్రధాన పితృ కర్తగా",
            "timeframe_te": "రాబోయే 3 నుండి 6 నెలల లోపు (అమావాస్య లేదా మహాలయ పక్షం)",
            "ideal_days_range": 120,
            "urgency": "పితృ శాంతి (Important)",
            "procedure": "మహాలయ పక్షం లేదా అమావాస్య నాడు తిల హోమం జరిపించి పేదలకు అన్నదానం మరియు వస్త్రదానం చేయాలి.",
            "mantra": "పితృ గాయత్రీ మంత్రం & తిల తర్పణ మంత్రాలు",
            "shastra_quote": "ధర్మసింధు & పరాశర స్మృతి: 'పితౄణాం తర్పణం కుర్యాత్ సర్వపాప ప్రణాశనం'"
        })

    # Priority 3: Kuja Shanti (if not cancelled by samyam)
    if kuja_puja_needed:
        kuja_target = f"భర్త ({h_name})" if kuja_samya_status == "husband_only" else f"భార్య ({w_name})"
        joint_pariharas.append({
            "priority": "3 (గ్రహ శాంతి)",
            "title": "సుబ్రహ్మణ్య షష్ఠి పూజ & కుజ శాంతి",
            "event_type": "kuja_shanti_subrahmanya",
            "for_whom": f"{kuja_target} జాతకంలో కుజ దోషం",
            "karta": f"{kuja_target} ప్రధాన సంకల్పంతో",
            "timeframe_te": "శీఘ్రముగా — రాబోయే 30 నుండి 60 రోజుల లోపు",
            "ideal_days_range": 60,
            "urgency": "శీఘ్ర పరిహారం (Within 60 Days)",
            "procedure": "శుక్లపక్ష షష్ఠి లేదా మంగళవారం నాడు సుబ్రహ్మణ్యేశ్వర స్వామి సన్నిధిలో పంచామృతాభిషేకం మరియు కందుల దానం.",
            "mantra": "ఓం శరవణభవాయ నమః & స్కంద షష్ఠి కవచం",
            "shastra_quote": "ముహూర్త రత్నావళి"
        })

    # Default Auspicious Parihara if all clean
    if len(joint_pariharas) == 0:
        joint_pariharas.append({
            "priority": "శుభ సంకల్పం",
            "title": "శ్రీ సత్యనారాయణ స్వామి వ్రతం / ఆయుష్య హోమం",
            "event_type": "satyanarayana_vrata",
            "for_whom": "దంపతుల దాంపత్య ఐకమత్యం & సర్వాభీష్ట సిద్ధి",
            "karta": "దంపతులు సంయుక్తంగా",
            "timeframe_te": "రాబోయే 30 రోజుల లోపు (పౌర్ణమి లేదా ఏకాదశి)",
            "ideal_days_range": 30,
            "urgency": "శుభ సంకల్పం",
            "procedure": "పౌర్ణమి లేదా శుభ తిథి నాడు సకుటుంబంగా సత్యనారాయణ స్వామి వ్రతం ఆచరించి ప్రసాద వితరణ చేయండి.",
            "mantra": "శ్రీ సత్యనారాయణ స్వామి అష్టోత్తర శతనామావళి",
            "shastra_quote": "స్కంద పురాణం (రేవాఖండం)"
        })

    return {
        "couple_names": {
            "husband": h_name,
            "wife": w_name
        },
        "santana_joint": {
            "verdict": santana_joint_verdict,
            "badge": santana_joint_badge,
            "who_carries_dosha": santana_joint_who,
            "description": santana_joint_desc,
            "husband_beeja": h_beeja,
            "wife_kshetra": w_kshetra,
            "recommended_remedy": santana_remedy,
            "event_type": santana_event_type,
            "karta": santana_karta
        },
        "kuja_samya": {
            "status": kuja_samya_status,
            "badge": kuja_samya_badge,
            "title": kuja_samya_title,
            "description": kuja_samya_desc,
            "is_puja_needed": kuja_puja_needed,
            "husband_kuja": h_kuja,
            "wife_kuja": w_kuja
        },
        "comparative_matrix": [
            {
                "dosha_name": "సంతాన / బీజ-క్షేత్ర దోషం",
                "husband_status": h_beeja_status,
                "wife_status": w_kshetra_status,
                "joint_result": santana_joint_who,
                "badge": santana_joint_badge
            },
            {
                "dosha_name": "కుజ దోషం (Mars Affliction)",
                "husband_status": h_kuja.get("status_te", "లేదు"),
                "wife_status": w_kuja.get("status_te", "లేదు"),
                "joint_result": kuja_samya_title,
                "badge": kuja_samya_badge
            },
            {
                "dosha_name": "సర్ప / నాగ దోషం",
                "husband_status": h_sarpa.get("status_te", "లేదు"),
                "wife_status": w_sarpa.get("status_te", "లేదు"),
                "joint_result": "భర్తకు కలదు" if h_sarpa.get("has_dosha") and not w_sarpa.get("has_dosha") else ("భార్యకు కలదు" if w_sarpa.get("has_dosha") and not h_sarpa.get("has_dosha") else ("ఇద్దరికీ కలదు" if h_sarpa.get("has_dosha") else "లేదు")),
                "badge": "warning" if (h_sarpa.get("has_dosha") or w_sarpa.get("has_dosha")) else "success"
            },
            {
                "dosha_name": "పితృ దోషం (Pitru Dosha)",
                "husband_status": h_pitru.get("status_te", "లేదు"),
                "wife_status": w_pitru.get("status_te", "లేదు"),
                "joint_result": "భర్తకు కలదు" if h_pitru.get("has_dosha") and not w_pitru.get("has_dosha") else ("భార్యకు కలదు" if w_pitru.get("has_dosha") and not h_pitru.get("has_dosha") else ("ఇద్దరికీ కలదు" if h_pitru.get("has_dosha") else "లేదు")),
                "badge": "warning" if (h_pitru.get("has_dosha") or w_pitru.get("has_dosha")) else "success"
            },
            {
                "dosha_name": "కాలసర్ప దోషం",
                "husband_status": husband_kundali.get("kalasarpa_dosha", {}).get("type_te", "లేదు"),
                "wife_status": wife_kundali.get("kalasarpa_dosha", {}).get("type_te", "లేదు"),
                "joint_result": "పరిశీలించబడింది",
                "badge": "info"
            }
        ],
        "joint_pariharas": joint_pariharas,
        "primary_action_karta": santana_karta if santana_joint_badge in ["warning", "danger"] else "దంపతులు సంయుక్తంగా",
        "primary_recommended_event_type": joint_pariharas[0]["event_type"] if joint_pariharas else "santana_gopala"
    }


def audit_family_doshas(
    members_data: List[Dict[str, Any]],
    family_name: str = "మా కుటుంబం"
) -> Dict[str, Any]:
    """
    Comprehensive Family Dosha Audit Engine (సకుటుంబ దోష సమగ్ర పరిశీలన యంత్రం):
    - Audits every family member individually for:
      * Nakshatra & Pada
      * Sarpa / Naga Dosha
      * Kuja Dosha
      * Kala Sarpa Dosha
      * Pitru Dosha
      * Shani / Sade Sati (Transit)
      * Gandanta / Moola
    - Aggregates family-level statistics:
      * Afflicted members vs Safe members
      * Who carries which affliction
      * Determines Family Karta (కుటుంబ సంకల్ప కర్త)
      * Prescribes unified Family Pariharas with direct Muhurtam linkages
    """
    total_members = len(members_data)
    audit_table = []
    afflicted_members = []
    safe_members = []

    family_has_sarpa = False
    family_has_pitru = False
    family_has_kuja = False
    family_has_shani = False

    for idx, item in enumerate(members_data):
        m_info = item.get("member_info", {})
        m_name = m_info.get("name", "సభ్యుడు")
        m_relation = m_info.get("relation", "కుటుంబ సభ్యుడు")
        m_gender = m_info.get("gender", "male")

        k_data = item.get("kundali", {})
        lagna = k_data.get("lagna", {})
        planets = k_data.get("planets", [])
        panchangam = k_data.get("panchangam", {})
        gocharam = k_data.get("gocharam", {})

        # Run Audits
        pitru = detect_pitru_dosha(lagna, planets)
        sarpa = detect_sarpa_naga_dosha(lagna, planets)
        kuja = k_data.get("kuja_dosha", {})
        kalasarpa = k_data.get("kalasarpa_dosha", {})
        sade_sati = gocharam.get("sade_sati", {})

        nak_name = panchangam.get("nakshatra", "")
        pada = panchangam.get("pada", 1)
        rashi_name = panchangam.get("janma_rashi") or panchangam.get("rashi_name_te") or ""

        # Moola / Gandanta check
        is_gandanta = "మూల" in nak_name or "జ్యేష్ఠ" in nak_name or "ఆశ్లేష" in nak_name
        gandanta_str = f"⚠️ {nak_name} గండాంతం" if is_gandanta else "🌿 శుభం"

        # Kuja check
        has_kuja_active = kuja.get("has_dosha", False) and kuja.get("severity") == "present"
        kuja_str = f"🚩 కుజ దోషం ({kuja.get('kuja_from_lagna')}వ ఇల్లు)" if has_kuja_active else ("🌿 భంగం / రద్దు" if kuja.get("severity") == "cancelled" else "🌿 లేదు")

        # Sarpa check
        has_sarpa = sarpa.get("has_dosha", False)
        sarpa_str = f"🚩 {sarpa.get('status_te')}" if has_sarpa else "🌿 లేదు"

        # Pitru check
        has_pitru = pitru.get("has_dosha", False)
        pitru_str = f"🚩 {pitru.get('status_te')}" if has_pitru else "🌿 లేదు"

        # Kalasarpa check
        has_kalasarpa = kalasarpa.get("has_kalasarpa", False)
        kalasarpa_str = f"🚩 {kalasarpa.get('type_te', 'కలదు')}" if has_kalasarpa else "🌿 లేదు"

        # Sade Sati check
        is_sade_sati = sade_sati.get("is_active", False)
        shani_phase = sade_sati.get("phase_te", "సాధారణం")
        shani_str = f"🪐 {shani_phase}" if is_sade_sati else "🌿 అనుకూలం"

        # Individual verdict
        has_any_affliction = has_sarpa or has_pitru or has_kuja_active or has_kalasarpa or (is_gandanta and pada == 1)

        if has_any_affliction:
            affliction_badge = "danger" if (sarpa.get("severity") == "severe" or pitru.get("severity") == "severe") else "warning"
            affliction_verdict = "🚩 దోష ప్రభావం కలదు"
            afflicted_members.append(f"{m_name} ({m_relation})")
        else:
            affliction_badge = "success"
            affliction_verdict = "🌿 సంపూర్ణ దోష రహితం"
            safe_members.append(f"{m_name} ({m_relation})")

        if has_sarpa:
            family_has_sarpa = True
        if has_pitru:
            family_has_pitru = True
        if has_kuja_active:
            family_has_kuja = True
        if is_sade_sati:
            family_has_shani = True

        audit_table.append({
            "member_index": idx,
            "id": m_info.get("id", m_name),
            "name": m_name,
            "relation": m_relation,
            "gender": m_gender,
            "lagna": lagna.get("rashi_name_te", ""),
            "rashi": rashi_name,
            "nakshatra": f"{nak_name}-{pada}",
            "sarpa_dosha": sarpa_str,
            "sarpa_badge": "danger" if has_sarpa else "success",
            "kuja_dosha": kuja_str,
            "kuja_badge": "warning" if has_kuja_active else "success",
            "kalasarpa_dosha": kalasarpa_str,
            "kalasarpa_badge": "warning" if has_kalasarpa else "success",
            "pitru_dosha": pitru_str,
            "pitru_badge": "warning" if has_pitru else "success",
            "shani_dosha": shani_str,
            "shani_badge": "info" if is_sade_sati else "success",
            "gandanta": gandanta_str,
            "verdict": affliction_verdict,
            "verdict_badge": affliction_badge,
            "primary_remedy": sarpa.get("primary_remedy") if has_sarpa else (pitru.get("primary_remedy") if has_pitru else "నిత్య ఇష్టదైవ ఆరాధన")
        })

    # Determine Family Karta (Dharmashastra principle)
    # The male head of the household (Father / Eldest) is the primary Karta for general family well-being.
    karta_candidate = None
    for item in members_data:
        rel = item.get("member_info", {}).get("relation", "").lower()
        if "తండ్రి" in rel or "భర్త" in rel or "గృహపతి" in rel or "యజమాని" in rel:
            karta_candidate = item.get("member_info", {}).get("name")
            break
    if not karta_candidate and len(members_data) > 0:
        karta_candidate = members_data[0].get("member_info", {}).get("name")

    # Family Pariharas
    family_remedies = []
    if family_has_sarpa:
        family_remedies.append({
            "title": "సకుటుంబ నాగ ప్రతిష్ఠ / ఆశ్లేషా బలి (Family Naga Pratishtha)",
            "event_type": "naga_pratishtha",
            "target": "కుటుంబంలో సర్ప దోషం కలిగిన సభ్యుల పేరిట",
            "karta": f"{karta_candidate} (గృహయజమాని) సకుటుంబంగా",
            "timeframe_te": "3 నుండి 6 నెలల లోపు (గరిష్ఠంగా 90 రోజులలోపు శ్రేయస్కరం)",
            "ideal_days_range": 90,
            "urgency": "అత్యవసరం (High Priority)",
            "procedure": "పుణ్యక్షేత్రాలలో అశ్వత్థ వృక్ష సన్నిధిలో నాగ శిలా ప్రతిష్ఠ జరిపించి పాలాభిషేకం చేయించాలి.",
            "shastra_quote": "బృహత్ పరాశర హోరాశాస్త్రం (వంశాభివృద్ధి ప్రకరణం)"
        })

    if family_has_pitru:
        family_remedies.append({
            "title": "సకుటుంబ తిల హోమం & పితృ తర్పణం (Family Tila Homa)",
            "event_type": "tila_homam_pitru",
            "target": "పూర్వీకుల ఆశీర్వాదం & వంశాభివృద్ధి కొరకు",
            "karta": f"{karta_candidate} ప్రధాన పితృ కర్తగా",
            "timeframe_te": "3 నుండి 6 నెలల లోపు లేదా రాబోయే మహాలయ పక్షం / దర్శ అమావాస్య",
            "ideal_days_range": 120,
            "urgency": "మధ్యమం (Medium Priority)",
            "procedure": "మహాలయ పక్షం లేదా అమావాస్య నాడు తిల హోమం జరిపించి అన్నదానం సమర్పించాలి.",
            "shastra_quote": "ధర్మసింధు & పరాశర స్మృతి"
        })

    # Default Auspicious Family Parihara
    family_remedies.append({
        "title": "సకుటుంబ శ్రీ సత్యనారాయణ స్వామి వ్రతం (Family Satyanarayana Vrata)",
        "event_type": "satyanarayana_vrata",
        "target": "సకుటుంబ సర్వాభీష్ట సిద్ధి & గృహ శాంతి",
        "karta": f"{karta_candidate} సకుటుంబంగా",
        "timeframe_te": "30 నుండి 45 రోజుల లోపు (రాబోయే శుక్ల పక్ష పౌర్ణమి నాటికి)",
        "ideal_days_range": 45,
        "urgency": "శుభప్రదం (Auspicious Priority)",
        "procedure": "పౌర్ణమి లేదా శుభ తిథి యందు సకుటుంబ సమేతంగా సత్యనారాయణ వ్రతమాచరించుట పరమ శుభప్రదం.",
        "shastra_quote": "స్కంద పురాణం"
    })

    return {
        "family_name": family_name,
        "total_members": total_members,
        "afflicted_count": len(afflicted_members),
        "safe_count": len(safe_members),
        "afflicted_members": afflicted_members,
        "safe_members": safe_members,
        "audit_table": audit_table,
        "designated_karta": f"{karta_candidate} (కుటుంబ యజమాని / సంకల్ప కర్త)",
        "family_summary_te": (
            f"మొత్తం {total_members} కుటుంబ సభ్యుల జాతకాలు పరిశీలించబడ్డాయి. "
            f"{len(afflicted_members)} మంది సభ్యుల జాతకాలలో విశేష దోష ప్రభావాలు గుర్తించబడ్డాయి; "
            f"{len(safe_members)} మంది సభ్యులు దోష రహితంగా ఉన్నారు. "
            f"శాస్త్ర ప్రకారం కుటుంబ యజమాని ({karta_candidate}) ప్రధాన కర్తగా ఉండి సకుటుంబ శాంతి నిర్వహించాలి."
        ),
        "family_remedies": family_remedies,
        "primary_recommended_event_type": family_remedies[0]["event_type"]
    }

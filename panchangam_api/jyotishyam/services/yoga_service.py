"""
Vedic Yogas and Doshas detection engine.
Identifies Raja Yogas, Dhana Yogas, Gajakesari, Budhaditya,
Pancha Mahapurusha, Kuja Dosha, and Viparita Raja Yogas.
"""

from typing import Dict, Any, List
from jyotishyam.services.kundali_calculator import RASHIS


def detect_yogas(lagna_info: Dict[str, Any], planets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Detect prominent astrological yogas and doshas in the chart."""
    yogas = []
    p_map = {p["name_en"]: p for p in planets}
    lagna_rashi = lagna_info["rashi_index"]

    moon = p_map.get("Moon")
    sun = p_map.get("Sun")
    mars = p_map.get("Mars")
    mercury = p_map.get("Mercury")
    jupiter = p_map.get("Jupiter")
    venus = p_map.get("Venus")
    saturn = p_map.get("Saturn")

    # 1. Gajakesari Yoga (Jupiter in 1, 4, 7, 10 from Moon)
    if moon and jupiter:
        jup_from_moon = ((jupiter["rashi_index"] - moon["rashi_index"]) % 12) + 1
        if jup_from_moon in [1, 4, 7, 10]:
            yogas.append({
                "name": "గజకేసరి యోగం (Gajakesari Yoga)",
                "type": "శుభ యోగం (Auspicious)",
                "description": "చంద్రునికి కేంద్రంలో (1, 4, 7, 10) గురుడు ఉన్నప్పుడు ఏర్పడుతుంది. అపారమైన కీర్తి, గౌరవం, దీర్ఘాయుష్షు, విద్యాబుద్ధులు లభిస్తాయి.",
                "strength": "బలమైన శుభ యోగం",
                "source": "బృహత్ పరాశర హోరా శాస్త్రం & జాతక చంద్రిక"
            })

    # 2. Budhaditya Yoga (Sun + Mercury in same Rashi)
    if sun and mercury and sun["rashi_index"] == mercury["rashi_index"]:
        yogas.append({
            "name": "బుధాదిత్య యోగం (Budhaditya Yoga)",
            "type": "రాజ యోగం (Raja Yoga)",
            "description": "రవి మరియు బుధుడు ఒకే రాశిలో ఉండడం వల్ల ఏర్పడుతుంది. నిశితమైన బుద్ధికుశలత, గణిత/శాస్త్ర నైపుణ్యం, సమాజంలో విశేషమైన గుర్తింపు చేకూరుస్తుంది.",
            "strength": "ఉత్తమం",
            "source": "జాతకాభరణం"
        })

    # 3. Pancha Mahapurusha Yogas (Exalted or Own in Kendra from Lagna)
    kendra_bhavas = [1, 4, 7, 10]
    # Ruchaka (Mars)
    if mars and mars["bhava"] in kendra_bhavas and mars["dignity_en"] in ["Exalted", "Own Sign", "Moolatrikona"]:
        yogas.append({
            "name": "రుచక యోగం (Ruchaka Yoga - పంచమహాపురుష)",
            "type": "మహాపురుష యోగం",
            "description": "కుజుడు కేంద్రంలో స్వక్షేత్రంలో లేదా ఉచ్ఛలో ఉండటం వల్ల ధైర్యం, భూ సంపద, ఉన్నత అధికార పదవులు ప్రాప్తిస్తాయి.",
            "strength": "అత్యుత్తమం",
            "source": "బృహత్ పరాశర హోరా శాస్త్రం"
        })

    # Bhadra (Mercury)
    if mercury and mercury["bhava"] in kendra_bhavas and mercury["dignity_en"] in ["Exalted", "Own Sign", "Moolatrikona"]:
        yogas.append({
            "name": "భద్ర యోగం (Bhadra Yoga - పంచమహాపురుష)",
            "type": "మహాపురుష యోగం",
            "description": "బుధుడు కేంద్రంలో స్వక్షేత్రంలో లేదా ఉచ్ఛలో ఉండటం వల్ల పాండిత్యం, వాక్చాతుర్యం, వ్యాపార రంగంలో విశేష విజయం సిద్ధిస్తాయి.",
            "strength": "అత్యుత్తమం",
            "source": "బృహత్ పరాశర హోరా శాస్త్రం"
        })

    # Hamsa (Jupiter)
    if jupiter and jupiter["bhava"] in kendra_bhavas and jupiter["dignity_en"] in ["Exalted", "Own Sign", "Moolatrikona"]:
        yogas.append({
            "name": "హంస యోగం (Hamsa Yoga - పంచమహాపురుష)",
            "type": "మహాపురుష యోగం",
            "description": "గురుడు కేంద్రంలో స్వక్షేత్రంలో లేదా ఉచ్ఛలో ఉంటే ఆధ్యాత్మిక ఔన్నత్యం, దైవానుగ్రహం, సకల సద్గుణాలు చేకూరుతాయి.",
            "strength": "అత్యుత్తమం",
            "source": "బృహత్ పరాశర హోరా శాస్త్రం"
        })

    # Malavya (Venus)
    if venus and venus["bhava"] in kendra_bhavas and venus["dignity_en"] in ["Exalted", "Own Sign", "Moolatrikona"]:
        yogas.append({
            "name": "మాళవ్య యోగం (Malavya Yoga - పంచమహాపురుష)",
            "type": "మహాపురుష యోగం",
            "description": "శుక్రుడు కేంద్రంలో స్వక్షేత్రం లేదా ఉచ్ఛలో ఉంటే సౌందర్యం, కళాభిరుచి, వాహన-గృహ ప్రాప్తి, ఆనందమయ దాంపత్య జీవితం కలుగుతాయి.",
            "strength": "అత్యుత్తమం",
            "source": "బృహత్ పరాశర హోరా శాస్త్రం"
        })

    # Sasa (Saturn)
    if saturn and saturn["bhava"] in kendra_bhavas and saturn["dignity_en"] in ["Exalted", "Own Sign", "Moolatrikona"]:
        yogas.append({
            "name": "శశ యోగం (Sasa Yoga - పంచమహాపురుష)",
            "type": "మహాపురుష యోగం",
            "description": "శని కేంద్రంలో స్వక్షేత్రం లేదా ఉచ్ఛలో ఉంటే ప్రజా నాయకత్వం, స్థిరమైన సంపద, లోతైన ధ్యానబుద్ధి ప్రాప్తిస్తాయి.",
            "strength": "అత్యుత్తమం",
            "source": "బృహత్ పరాశర హోరా శాస్త్రం"
        })

    # 4. Chandra-Mangala Yoga (Moon + Mars together)
    if moon and mars and moon["rashi_index"] == mars["rashi_index"]:
        yogas.append({
            "name": "చంద్ర-మంగళ యోగం (Chandra-Mangala Yoga)",
            "type": "ధన యోగం (Wealth)",
            "description": "చంద్ర-కుజుల కలయిక వల్ల అపారమైన ధనలాభం, రియల్ ఎస్టేట్ మరియు స్థిరాస్తి అభివృద్ధి సిద్ధిస్తుంది.",
            "strength": "మంచి ధన యోగం",
            "source": "జాతక చంద్రిక"
        })

    # 5. Kuja Dosha (Manglik) Check
    # Mars in 1, 2, 4, 7, 8, 12 from Lagna or Moon
    if mars:
        kuja_from_lagna = mars["bhava"]
        kuja_from_moon = ((mars["rashi_index"] - moon["rashi_index"]) % 12) + 1 if moon else 0

        is_kuja_dosha = (kuja_from_lagna in [1, 2, 4, 7, 8, 12]) or (kuja_from_moon in [1, 2, 4, 7, 8, 12])
        if is_kuja_dosha:
            # Check classical cancellations (Exalted in Cap, Own in Aries/Scorpio, aspected by Jupiter)
            has_cancellation = mars["dignity_en"] in ["Exalted", "Own Sign"] or (jupiter and ((jupiter["rashi_index"] - mars["rashi_index"]) % 12) in [4, 6, 8])
            canc_note = " (అయితే కుజుని బలం/గురు దృష్టి వల్ల దోష తీవ్రత పరిహారమైనది - దోషభంగం)" if has_cancellation else " (వివాహ విషయాలలో కుజ దోష సామ్యం చూడడం శ్రేయస్కరం)"

            yogas.append({
                "name": "కుజ దోషం (Kuja / Manglik Presence)",
                "type": "పరిశీలించదగిన యోగం (Dosha)",
                "description": f"కుజుడు లగ్నం నుండి {kuja_from_lagna}వ స్థానంలో ఉన్నారు.{canc_note}",
                "strength": "సాధారణం" if has_cancellation else "పరిహారార్హం",
                "source": "జాతక నారాయణీయమ్ & ముహూర్త రత్నావళి"
            })

    # 6. Viparita Raja Yogas (Uttara Kalamritam)
    # Check 6th, 8th, 12th house lords placed in 6, 8, 12
    sixth_rashi = (lagna_rashi + 5) % 12
    eighth_rashi = (lagna_rashi + 7) % 12
    twelfth_rashi = (lagna_rashi + 11) % 12

    sixth_lord_en = RASHIS[sixth_rashi]["lord_en"]
    eighth_lord_en = RASHIS[eighth_rashi]["lord_en"]
    twelfth_lord_en = RASHIS[twelfth_rashi]["lord_en"]

    trik_bhavas = [6, 8, 12]
    sixth_lord_bhava = p_map[sixth_lord_en]["bhava"] if sixth_lord_en in p_map else 0
    eighth_lord_bhava = p_map[eighth_lord_en]["bhava"] if eighth_lord_en in p_map else 0
    twelfth_lord_bhava = p_map[twelfth_lord_en]["bhava"] if twelfth_lord_en in p_map else 0

    if sixth_lord_bhava in trik_bhavas:
        yogas.append({
            "name": "హర్ష విపరీత రాజయోగం (Harsha Viparita Raja Yoga)",
            "type": "విపరీత రాజయోగం",
            "description": "6వ అధిపతి దుఃస్థానాలలో (6, 8, 12) ఉండటం వల్ల శత్రు జయం, రోగ విముక్తి, అనుకోని విజయాలు వరిస్తాయి.",
            "strength": "ఉత్తమ విపరీత రాజయోగం",
            "source": "ఉత్తర కాలామృతం (కాళిదాస)"
        })

    if eighth_lord_bhava in trik_bhavas:
        yogas.append({
            "name": "సరళ విపరీత రాజయోగం (Sarala Viparita Raja Yoga)",
            "type": "విపరీత రాజయోగం",
            "description": "8వ అధిపతి దుఃస్థానాలలో ఉండటం వల్ల దీర్ఘాయుష్షు, విద్యాప్రాప్తి, ఆకస్మిక ధనలాభం ప్రాప్తిస్తాయి.",
            "strength": "ఉత్తమ విపరీత రాజయోగం",
            "source": "ఉత్తర కాలామృతం (కాళిదాస)"
        })

    if twelfth_lord_bhava in trik_bhavas:
        yogas.append({
            "name": "విమల విపరీత రాజయోగం (Vimala Viparita Raja Yoga)",
            "type": "విపరీత రాజయోగం",
            "description": "12వ అధిపతి దుఃస్థానాలలో ఉండటం వల్ల స్వతంత్ర వ్యక్తిత్వం, ధన సంచయం, గౌరవప్రదమైన జీవనం ఏర్పడతాయి.",
            "strength": "ఉత్తమ విపరీత రాజయోగం",
            "source": "ఉత్తర కాలామృతం (కాళిదాస)"
        })

    return yogas


def analyze_kuja_dosha(lagna_info: Dict[str, Any], planets: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Comprehensive Kuja Dosha (Manglik) Analyzer.
    Evaluates 1, 2, 4, 7, 8, 12 from Lagna, Moon, and Venus,
    along with classical Shastric cancellation rules (మినహాయింపులు).
    """
    p_map = {p["name_en"]: p for p in planets}
    mars = p_map.get("Mars")
    moon = p_map.get("Moon")
    venus = p_map.get("Venus")
    jupiter = p_map.get("Jupiter")

    if not mars:
        return {"has_dosha": False, "status_te": "దోష రహితం", "description": "కుజ గ్రహ సమాచారం లభించలేదు."}

    lagna_rashi = lagna_info["rashi_index"]
    mars_rashi = mars["rashi_index"]
    mars_bhava = mars["bhava"]

    # Houses from Lagna, Moon, Venus
    h_lagna = mars_bhava
    h_moon = ((mars_rashi - moon["rashi_index"]) % 12) + 1 if moon else 0
    h_venus = ((mars_rashi - venus["rashi_index"]) % 12) + 1 if venus else 0

    dosha_houses = [1, 2, 4, 7, 8, 12]
    dosha_from_lagna = h_lagna in dosha_houses
    dosha_from_moon = h_moon in dosha_houses
    dosha_from_venus = h_venus in dosha_houses

    has_dosha = dosha_from_lagna or dosha_from_moon or dosha_from_venus

    cancellations = []
    # 1. Own sign or exaltation
    if mars_rashi in [0, 7]:  # Mesha, Vrischika
        cancellations.append("కుజుడు స్వక్షేత్రమైన మేషం లేదా వృశ్చికంలో ఉండడం వల్ల దోషభంగం/దోష నివృత్తి ఏర్పడింది.")
    elif mars_rashi == 9:  # Makara
        cancellations.append("కుజుడు పరమోచ్ఛ రాశియైన మకరంలో ఉండడం వల్ల కుజ దోషం నివృత్తి అయినది.")

    # 2. Conjoined or aspected by Jupiter or Moon
    if jupiter:
        jup_dist = ((jupiter["rashi_index"] - mars_rashi) % 12) + 1
        if jup_dist in [1, 5, 7, 9]:
            cancellations.append("కుజునిపై దేవగురువైన బృహస్పతి (గురుడు) దృష్టి లేదా సంయోగం ఉన్నందున దోష తీవ్రత పరిహారమైనది.")
    if moon and moon["rashi_index"] == mars_rashi:
        cancellations.append("చంద్ర-మంగళ సంయోగం వలన కుజ దోషం పరిహారమై రాజయోగంగా మారినది.")

    # 3. Specific house-rashi exceptions
    if h_lagna == 2 and mars_rashi in [2, 5]:  # Gemini/Virgo
        cancellations.append("2వ స్థానంలో మిథున లేదా కన్యారాశిలో కుజుడు ఉండడం వల్ల దోషరహితం.")
    elif h_lagna == 4 and mars_rashi in [0, 7]:  # Aries/Scorpio
        cancellations.append("4వ స్థానంలో మేష లేదా వృశ్చిక రాశిలో కుజుడు ఉండడం వల్ల దోషరహితం.")
    elif h_lagna == 7 and mars_rashi in [3, 9]:  # Cancer/Capricorn
        cancellations.append("7వ స్థానంలో కర్కాటక లేదా మకర రాశిలో కుజుడు ఉండడం వల్ల శాస్త్రోక్త మినహాయింపు లభించినది.")
    elif h_lagna == 8 and mars_rashi in [8, 11]:  # Sag/Pisces
        cancellations.append("8వ స్థానంలో ధనుస్సు లేదా మీనరాశిలో కుజుడు ఉండడం వల్ల దోషం రద్దయినది.")
    elif h_lagna == 12 and mars_rashi in [1, 6]:  # Taurus/Libra
        cancellations.append("12వ స్థానంలో వృషభ లేదా తులా రాశిలో కుజుడు ఉండడం వల్ల దోషరహితం.")

    # Status Determination & Authentic Shastric Verification
    if not has_dosha:
        status_te = "కుజ దోషం లేదు (No Kuja Dosha)"
        summary_te = f"కుజుడు లగ్నం నుండి {h_lagna}వ స్థానంలో ఉన్నారు. వివాహ విచారణలో కుజదోషం వర్తించదు."
        severity = "none"
        recheck_verdict = {
            "is_puja_needed": False,
            "badge": "success",
            "verdict_title": "పూజ అవసరం లేదు (No Kuja Dosha)",
            "shastra_authority": "ముహూర్త రత్నావళి & బృహత్ పరాశర హోరాశాస్త్రం (అధ్యాయం 84)",
            "authentic_reason": f"కుజుడు లగ్నం నుండి {h_lagna}వ భావంలో ఉన్నారు (దోష భావాలైన 1, 2, 4, 7, 8, 12 లో లేరు). వివాహ పొంతనలో కుజదోష విచారణ వర్తించదు.",
            "zero_cost_remedy": "నిత్య సుబ్రహ్మణ్య ప్రార్థన సాధారణ శుభప్రదం."
        }
    elif len(cancellations) > 0:
        status_te = "కుజ దోష నివృత్తి / దోష భంగం (Cancelled/Exempted)"
        summary_te = f"కుజుడు {h_lagna}వ భావంలో ఉన్నప్పటికీ, శాస్త్రోక్త మినహాయింపుల వల్ల కుజ దోష తీవ్రత తొలగిపోయినది (దోష భంగం)."
        severity = "cancelled"
        recheck_verdict = {
            "is_puja_needed": False,
            "badge": "info",
            "verdict_title": "దోష భంగం — ఖరీదైన శాంతి పూజలు అవసరం లేదు",
            "shastra_authority": "ముహూర్త రత్నావళి (వివాహ ప్రకరణం) & జాతక నారాయణీయమ్: 'కుజే కుంభే చ మీనే వా... శుభదృష్టే న దోషః'",
            "authentic_reason": "కుజుడు దోష స్థానంలో ఉన్నప్పటికీ ప్రామాణిక గ్రంథాల ప్రకారం బలమైన దోషభంగ కారణాలు సిద్ధించినందున దోష తీవ్రత తొలగిపోయింది. ఖరీదైన శాంతి హోమాలు చేయనక్కర్లేదు.",
            "cancellation_details": cancellations,
            "zero_cost_remedy": "ఇంట్లోనే మంగళవారం సుబ్రహ్మణ్యాష్టకం లేదా స్కంద షష్ఠి కవచం పఠించండి. సుబ్రహ్మణ్య దర్శనం ఉత్తమం."
        }
    else:
        status_te = "కుజ దోషం కలదు (Kuja Dosha Present)"
        summary_te = f"కుజుడు లగ్నం నుండి {h_lagna}వ భావంలో, చంద్రుని నుండి {h_moon}వ భావంలో ఉన్నారు. వివాహ పొంతనలో కుజదోష సామ్యం కలిగిన జాతకాన్ని ఎంచుకోవడం శ్రేయస్కరం."
        severity = "present"
        recheck_verdict = {
            "is_puja_needed": True,
            "badge": "warning",
            "verdict_title": "పరిహారార్హం — వైదిక సాధన & కుజదోష సామ్యం ముఖ్యం",
            "shastra_authority": "బృహత్ పరాశర హోరాశాస్త్రం & జాతకాభరణం",
            "authentic_reason": f"కుజుడు లగ్నం నుండి {h_lagna}వ స్థానంలో, చంద్రుని నుండి {h_moon}వ స్థానంలో ఉన్నారు. ప్రత్యక్ష శుభగ్రహ దృష్టి లేదు.",
            "zero_cost_remedy": "సుబ్రహ్మణ్యారాధన, మంగళవారం 'ఓం భౌమాయ నమః' జపం (జప సంఖ్య: 10,000), కందుల దానం."
        }

    remedies = [
        "శ్రీ సుబ్రహ్మణ్యేశ్వర స్వామి ఆరాధన, సుబ్రహ్మణ్యాష్టకం లేదా స్కంద షష్ఠి కవచం పారాయణం చేయండి.",
        "ప్రతి మంగళవారం కందులు లేదా ఎర్రటి వస్త్రాలను దానం చేయడం వల్ల కుజ అనుగ్రహం లభిస్తుంది.",
        "మంగళవారం అంగారక స్తోత్రం లేదా 'ఓం భౌమాయ నమః' 108 సార్లు జపించండి (మొత్తం జప సంఖ్య: 10,000)."
    ]

    return {
        "has_dosha": has_dosha,
        "severity": severity,
        "status_te": status_te,
        "summary_te": summary_te,
        "kuja_from_lagna": h_lagna,
        "kuja_from_moon": h_moon,
        "kuja_from_venus": h_venus,
        "cancellations": cancellations,
        "remedies": remedies,
        "shastra_authority": "ముహూర్త రత్నావళి & బృహత్ పరాశర హోరాశాస్త్రం",
        "recheck_verdict": recheck_verdict
    }


def analyze_kalasarpa_dosha(lagna_info: Dict[str, Any], planets: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Comprehensive Kala Sarpa Yoga / Dosha Analyzer.
    Evaluates whether all 7 physical planets are hemmed between Rahu and Ketu.
    Identifies 12 specific classical types (Ananta to Sheshanaga).
    """
    p_map = {p["name_en"]: p for p in planets}
    rahu = p_map.get("Rahu")
    ketu = p_map.get("Ketu")

    if not rahu or not ketu:
        return {"has_dosha": False, "status_te": "పరిశీలన అసంపూర్ణం", "name": ""}

    rahu_lon = rahu["longitude"]
    ketu_lon = ketu["longitude"]

    # 7 physical planets
    seven_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    lons = [p_map[name]["longitude"] for name in seven_planets if name in p_map]

    if len(lons) < 7:
        return {"has_dosha": False, "status_te": "దోష రహితం", "name": ""}

    # Check side 1: Rahu -> Ketu (forward direction)
    # Circular distance
    def in_arc(lon, start, end):
        return ((lon - start) % 360.0) <= ((end - start) % 360.0)

    side1_count = sum(1 for lon in lons if in_arc(lon, rahu_lon, ketu_lon))
    side2_count = 7 - side1_count

    KALASARPA_TYPES = [
        {"num": 1, "name": "అనంత కాలసర్ప యోగం", "desc": "1వ స్థానంలో రాహువు, 7వ స్థానంలో కేతువు. ఆత్మవిశ్వాసం, వైవాహిక జీవితంలో ఓర్పు అవసరం."},
        {"num": 2, "name": "కుళిక కాలసర్ప యోగం", "desc": "2వ స్థానంలో రాహువు, 8వ స్థానంలో కేతువు. ఆర్థిక వ్యవహారాలు, కుటుంబ వాక్కుపై నియంత్రణ అవసరం."},
        {"num": 3, "name": "వాసుకి కాలసర్ప యోగం", "desc": "3వ స్థానంలో రాహువు, 9వ స్థానంలో కేతువు. సోదరులతో సత్సంబంధాలు, విదేశీ ప్రయాణాలలో విజయం."},
        {"num": 4, "name": "శంఖపాల కాలసర్ప యోగం", "desc": "4వ స్థానంలో రాహువు, 10వ స్థానంలో కేతువు. గృహ, వాహన సౌఖ్యాలు, వృత్తిలో కృషి."},
        {"num": 5, "name": "పద్మ కాలసర్ప యోగం", "desc": "5వ స్థానంలో రాహువు, 11వ స్థానంలో కేతువు. ఉన్నత విద్య, సంతాన యోగం, బుద్ధికుశలత."},
        {"num": 6, "name": "మహా పద్మ కాలసర్ప యోగం", "desc": "6వ స్థానంలో రాహువు, 12వ స్థానంలో కేతువు. శత్రుజయం, ఋణ విముక్తి, పోటీ పరీక్షల్లో విజయం."},
        {"num": 7, "name": "తక్షక కాలసర్ప యోగం", "desc": "7వ స్థానంలో రాహువు, 1వ స్థానంలో కేతువు. భాగస్వామ్య వ్యాపారాలు, దాంపత్య సామరస్యం."},
        {"num": 8, "name": "కార్కోటక కాలసర్ప యోగం", "desc": "8వ స్థానంలో రాహువు, 2వ స్థానంలో కేతువు. ఆయుర్దాయం, ఆకస్మిక ధనలాభాలు."},
        {"num": 9, "name": "శంఖచూడ కాలసర్ప యోగం", "desc": "9వ స్థానంలో రాహువు, 3వ స్థానంలో కేతువు. భాగ్యోదయం, పితృభక్తి, తీర్థయాత్రలు."},
        {"num": 10, "name": "ఘాతక కాలసర్ప యోగం", "desc": "10వ స్థానంలో రాహువు, 4వ స్థానంలో కేతువు. ఉద్యోగంలో పదోన్నతి, రాజకీయ లేదా పరిపాలనా గుర్తింపు."},
        {"num": 11, "name": "విషధర కాలసర్ప యోగం", "desc": "11వ స్థానంలో రాహువు, 5వ స్థానంలో కేతువు. వ్యాపార లాభాలు, మిత్రుల సహకారం."},
        {"num": 12, "name": "శేషనాగ కాలసర్ప యోగం", "desc": "12వ స్థానంలో రాహువు, 6వ స్థానంలో కేతువు. విదేశీయానం, ఆధ్యాత్మిక మోక్ష సాధన."}
    ]

    rahu_bhava = rahu["bhava"]
    type_info = KALASARPA_TYPES[rahu_bhava - 1] if 1 <= rahu_bhava <= 12 else KALASARPA_TYPES[0]

    remedies = [
        "శ్రీకాళహస్తి లేదా త్రయంబకేశ్వర్ క్షేత్రంలో రాహు-కేతు సర్పదోష నివారణ పూజ చేయించుకోవడం అత్యంత శ్రేయస్కరం.",
        "ప్రతిరోజూ మహా మృత్యుంజయ మంత్రం లేదా శివ పంచాక్షరీ స్తోత్రం 108 సార్లు పారాయణం చేయండి.",
        "నాగ దేవతకు పాలాభిషేకం మరియు శుక్లపక్ష షష్ఠి తిథి నాడు సుబ్రహ్మణ్యేశ్వర స్వామి దర్శనం చేసుకోండి."
    ]

    if side1_count == 7 or side2_count == 7:
        # Full Kala Sarpa
        is_yoga = (side1_count == 7)
        title = f"పూర్ణ {type_info['name']}"
        status_te = f"పూర్ణ కాలసర్ప యోగం / దోషం కలదు ({type_info['name']})"
        summary_te = f"సమస్త సప్త గ్రహాలు రాహు-కేతువుల మధ్య బంధించబడి ఉన్నందున {type_info['name']} ఏర్పడినది. {type_info['desc']}"
        recheck_verdict = {
            "is_puja_needed": True,
            "badge": "warning",
            "verdict_title": "పూర్ణ కాలసర్పం — నిత్య వైదిక సాధన & శివారాధన శ్రేయస్కరం",
            "shastra_authority": "జాతకాభరణం & జాతక పారిజాతం",
            "authentic_reason": "సప్త భౌతిక గ్రహాలూ రాహు-కేతువుల ఒకే అర్ధభాగంలో బంధించబడి ఉన్నాయి. అయితే లగ్నాధిపతి లేదా గురు బలం ఉన్నచో క్రమంగా రాజయోగంగా మారును.",
            "zero_cost_remedy": "మహా మృత్యుంజయ మంత్ర జపం 108 సార్లు (జప సంఖ్య: 11,000), ప్రదోష వేళ శివారాధన, జీవహింస చేయకుండుట."
        }
        return {
            "has_dosha": True,
            "is_partial": False,
            "type_name": title,
            "status_te": status_te,
            "summary_te": summary_te,
            "rahu_bhava": rahu_bhava,
            "ketu_bhava": ketu["bhava"],
            "remedies": remedies,
            "shastra_authority": "జాతకాభరణం & జాతక పారిజాతం",
            "recheck_verdict": recheck_verdict
        }
    elif side1_count == 6 or side2_count == 6:
        # Partial / Ardha Kala Sarpa
        title = f"అంశిక / అర్ధ కాలసర్ప ప్రభావం ({type_info['name']})"
        status_te = "అంశిక కాలసర్ప ప్రభావం (ఒక గ్రహం వెలుపల ఉన్నది)"
        summary_te = f"ఆరు గ్రహాలు రాహు-కేతువుల మధ్య ఉండి, ఒక గ్రహం వెలుపల ఉండటం వలన కాలసర్ప దోష తీవ్రత గణనీయంగా తగ్గింది (దోష భంగం)."
        recheck_verdict = {
            "is_puja_needed": False,
            "badge": "info",
            "verdict_title": "అంశిక కాలసర్పం — భారీ ఖర్చుల పూజలు చేయనవసరం లేదు",
            "shastra_authority": "జాతక పారిజాతం & పూర్వ కాలామృతం",
            "authentic_reason": "ఒక గ్రహం రాహు-కేతువుల వలయం నుండి బయట ఉన్నందున కాలసర్ప బంధం భంగమైనది. తీవ్ర దోషం వర్తించదు.",
            "zero_cost_remedy": "రోజూ శివ పంచాక్షరి 'ఓం నమః శివాయ' జపం మరియు సుబ్రహ్మణ్య దర్శనం చాలును."
        }
        return {
            "has_dosha": True,
            "is_partial": True,
            "type_name": title,
            "status_te": status_te,
            "summary_te": summary_te,
            "rahu_bhava": rahu_bhava,
            "ketu_bhava": ketu["bhava"],
            "remedies": remedies[:2],
            "shastra_authority": "జాతక పారిజాతం & పూర్వ కాలామృతం",
            "recheck_verdict": recheck_verdict
        }
    else:
        recheck_verdict = {
            "is_puja_needed": False,
            "badge": "success",
            "verdict_title": "దోష రహితం — కాలసర్ప పూజ అవసరం లేదు (Safe)",
            "shastra_authority": "జాతకాభరణం",
            "authentic_reason": "గ్రహాలు రాహు-కేతువుల ఇరువైపులా స్వేచ్ఛగా ఉన్నాయి. కాలసర్ప బంధనం ఏమాత్రం లేదు.",
            "zero_cost_remedy": "సాధారణ ఇష్టదైవ ప్రార్థన చాలును."
        }
        return {
            "has_dosha": False,
            "is_partial": False,
            "type_name": "కాలసర్ప దోషం లేదు (No Kala Sarpa Dosha)",
            "status_te": "దోష రహితం",
            "summary_te": "సప్త గ్రహాలు రాహు-కేతువుల పరిధి వెలుపల స్వేచ్ఛగా ఉన్నందున జాతకంలో ఎటువంటి కాలసర్ప దోషం లేదు.",
            "rahu_bhava": rahu_bhava,
            "ketu_bhava": ketu["bhava"],
            "remedies": [],
            "shastra_authority": "జాతకాభరణం",
            "recheck_verdict": recheck_verdict
        }


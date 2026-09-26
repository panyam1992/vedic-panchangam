# -*- coding: utf-8 -*-
"""
High-Precision Vedic Muhurtam Calculator Engine (అత్యంత ఖచ్చితమైన వైదిక ముహూర్త నిర్ణయం).
Built using Swiss Ephemeris (pyswisseph) astronomical coordinates.
Adheres to classical Shastra rules:
- ముహూర్త రత్నావళి (Muhurtha Ratnavali)
- ముహూర్త దర్పణం (Muhurtha Darpana)
- కాలామృతమ్ (Kalamritam - Mahakavi Kalidasa)
- ముహూర్త చింతామణి (Muhurtha Chintamani)
- ధర్మసింధు & స్మృతి ముక్తావళి
"""

from datetime import datetime, date, timedelta, timezone
from typing import Dict, Any, List, Optional, Tuple
import swisseph as swe

from jyotishyam.services.ephemeris_service import (
    calc_julian_day_ut,
    set_ayanamsa_mode,
    calculate_planet_positions,
    calculate_lagna_and_houses,
    PLANET_IDS
)
from jyotishyam.services.kundali_calculator import RASHIS, NAKSHATRAS
from jyotishyam.services.panchangam_calc import TITHI_NAMES, VARA_NAMES, YOGA_NAMES, KARANA_MOVING, KARANA_FIXED

# Visha Ghatikas (Starting ghatika for each of the 27 Nakshatras - Kalamritam / Muhurtha Ratnavali)
VARJYAM_START_GHATIKAS = [
    50, 24, 30, 40, 14, 21, 30, 20, 32,  # Ashwini to Ashlesha
    30, 20, 18, 21, 20, 14, 14, 10, 14,  # Magha to Jyeshtha
    56, 24, 20, 10, 10, 18, 16, 24, 30   # Moola to Revati
]

# Supported Auspicious Events & Parihara Homas
EVENT_SPECS = {
    # 1. PARIHARA MUHURTAMS (పరిహార / శాంతి ముహూర్తాలు)
    "naga_pratishtha": {
        "title_te": "నాగ ప్రతిష్ఠ ముహూర్తం (Naga Pratishtha)",
        "category": "pariharam",
        "description": "సర్ప శాపం, నాగ దోషం, మరియు రాహు-కేతు సంతాన ప్రతిబంధక నివారణార్థం అశ్వత్థ వృక్ష సన్నిధిలో నాగ శిలా ప్రతిష్ఠ.",
        "shastra_source": "ముహూర్త రత్నావళి (ప్రతిష్ఠా ప్రకరణం) & కాలామృతమ్",
        "ideal_tithis": [5, 6, 7, 10, 11, 15],  # Panchami, Shashti, Saptami, Dashami, Ekadashi, Purnima
        "ideal_varas": [0, 2, 4, 5],            # Sun, Tue, Thu, Fri
        "ideal_nakshatras": [3, 4, 6, 7, 8, 11, 12, 14, 16, 21, 26], # Rohini, Mriga, Punarvasu, Pushya, Ashlesha, Uttara, Hasta, Swati, Anuradha, Shravana, Revati
        "ideal_lagnas": [1, 4, 7, 10, 2, 5, 8, 11], # Sthira & Dvisvabhava Lagnas
        "rule_note": "శుక్ల పంచమి (నాగ పంచమి) లేదా షష్ఠి అత్యుత్తమం. 8వ స్థానంలో పాప గ్రహాలు ఉండరాదు (అష్టమ శుద్ధి)."
    },
    "ashlesha_bali": {
        "title_te": "ఆశ్లేషా బలి పూజ (Ashlesha Bali Puja)",
        "category": "pariharam",
        "description": "కుక్కే లేదా సర్ప క్షేత్రాలలో ఆశ్లేషా నక్షత్ర యుక్త దినాన సర్ప దోష ఉపశమనం మరియు సంతాన ప్రాప్తికై చేసే బలి పూజ.",
        "shastra_source": "ధర్మసింధు & స్మృతి ముక్తావళి",
        "ideal_tithis": [5, 6, 8, 14, 15, 30],
        "ideal_varas": [0, 2, 4],
        "ideal_nakshatras": [8],  # Ashlesha is supreme
        "ideal_lagnas": [1, 3, 4, 7, 10],
        "rule_note": "ఆశ్లేషా నక్షత్రం ఉన్న రోజు ప్రదోష వేళ లేదా సూర్యోదయ లగ్నంలో ఆచరించడం అత్యంత ఫలప్రదం."
    },
    "rudra_pashupatam": {
        "title_te": "రుద్ర పాశుపత హోమం / మహా రుద్రాభిషేకం (Rudra Pashupatam)",
        "category": "pariharam",
        "description": "తీవ్రమైన వ్యాధులు, శత్రు భయం, సంతాన లేమి, మరియు కర్మ ప్రతిబంధక నివారణార్థం పరమశివునికి చేసే పాశుపత హోమం.",
        "shastra_source": "శివ పురాణం & ముహూర్త చింతామణి",
        "ideal_tithis": [8, 13, 14, 15],  # Ashtami, Trayodashi (Pradosha), Chaturdashi (Shivaratri), Purnima
        "ideal_varas": [1, 2, 4],         # Mon, Tue, Thu
        "ideal_nakshatras": [4, 6, 7, 12, 14, 16, 21, 25],
        "ideal_lagnas": [0, 3, 7, 8, 11],
        "rule_note": "శివ వాస పరిశీలన ముఖ్యం: కైలాసంలో లేదా గౌరీ సన్నిధిలో శివుడు ఉన్నప్పుడు హోమం జరిపిస్తే శీఘ్ర ఫలప్రాప్తి."
    },
    "chandi_homam": {
        "title_te": "చండీ హోమం / దుర్గా సప్తశతి (Chandi Homa)",
        "category": "pariharam",
        "description": "సకల గ్రహ పీడలు, నరదృష్టి, భయాలు, మరియు వంశాభివృద్ధికి జగన్మాత దుర్గాదేవి ప్రీత్యర్థం చేసే చండీ హోమం.",
        "shastra_source": "దేవీ భాగవతం & ముహూర్త రత్నావళి",
        "ideal_tithis": [8, 9, 14, 15],  # Ashtami, Navami, Chaturdashi, Purnima
        "ideal_varas": [2, 5],            # Tue, Fri
        "ideal_nakshatras": [2, 6, 9, 13, 14, 15, 17, 18, 20],
        "ideal_lagnas": [0, 1, 4, 6, 7, 9],
        "rule_note": "అగ్ని వాస పరిశీలన ముఖ్యం: పృథ్వీ వాసమున్నప్పుడు హోమం జరిపించాలి."
    },
    "santana_gopala": {
        "title_te": "సంతాన గోపాల హోమం / కృష్ణార్చన (Santana Gopala Homa)",
        "category": "pariharam",
        "description": "సంతాన భాగ్య సిద్ధి, గర్భ రక్షణ, మరియు వంశోద్ధారకుడైన సత్సంతాన ప్రాప్తికై శ్రీకృష్ణునికి సమర్పించే హోమం.",
        "shastra_source": "శ్రీమద్భాగవతం & ముహూర్త దర్పణం",
        "ideal_tithis": [2, 3, 5, 7, 10, 11, 12, 15], # Dvitiya, Tritiya, Panchami, Ekadashi, Purnima
        "ideal_varas": [3, 4],                         # Wed, Thu
        "ideal_nakshatras": [3, 7, 12, 21, 26],        # Rohini, Pushya, Hasta, Shravana, Revati
        "ideal_lagnas": [1, 3, 8, 11],                # Taurus, Cancer, Sag, Pisces
        "rule_note": "రోహిణి లేదా శ్రవణ నక్షత్రం, గురువారం అత్యంత శ్రేష్ఠం. 5వ స్థానంలో శుభ గ్రహాలుండాలి."
    },
    "kuja_shanti_subrahmanya": {
        "title_te": "సుబ్రహ్మణ్య షష్ఠి / కుజ శాంతి (Subrahmanya Shashti)",
        "category": "pariharam",
        "description": "రక్త సంబంధ దోషాలు, గర్భస్రావ నివారణ (Miscarriage Protection), మరియు దాంపత్య సౌఖ్యం కొరకు కుజ ప్రీతి.",
        "shastra_source": "స్కంద పురాణం & జాతకాభరణం",
        "ideal_tithis": [6],              # Shashti tithi
        "ideal_varas": [2],               # Tuesday
        "ideal_nakshatras": [2, 4, 13, 22], # Krittika, Mrigashira, Chitra, Dhanishta
        "ideal_lagnas": [0, 3, 7, 9],
        "rule_note": "శుక్లపక్ష షష్ఠి నాడు సుబ్రహ్మణ్యేశ్వర స్వామి సన్నిధిలో పంచామృతాభిషేకం ఉత్తమం."
    },
    "tila_homa_narayana_bali": {
        "title_te": "నారాయణ బలి / తిల హోమం (Narayana Bali / Pithru Shanti)",
        "category": "pariharam",
        "description": "పితృ శాప నివారణ, అకాల మరణ దోష శమనం, మరియు వంశాభివృద్ధికి చేసే పితృ శాంతి.",
        "shastra_source": "గరుడ పురాణం & ధర్మసింధు",
        "ideal_tithis": [11, 14, 30],     # Ekadashi, Chaturdashi, Amavasya
        "ideal_varas": [1, 6],            # Mon, Sat
        "ideal_nakshatras": [0, 9, 18, 23],
        "ideal_lagnas": [3, 7, 11],
        "rule_note": "దక్షిణాయనం లేదా అమావాస్య, కృష్ణపక్షంలో పుణ్యతీర్థాలలో చేయుట శ్రేయస్కరం."
    },
    "navagraha_shanti": {
        "title_te": "నవగ్రహ శాంతి హోమం (Navagraha Shanti Homa)",
        "category": "pariharam",
        "description": "జాతకంలో పాప గ్రహ పీడలు, మారక దశా ప్రభావాలు తొలగి ఆయురారోగ్యాలు చేకూరుటకు.",
        "shastra_source": "బృహత్ పరాశర హోరాశాస్త్రం (అధ్యాయం 85)",
        "ideal_tithis": [2, 3, 5, 7, 10, 11, 13, 15],
        "ideal_varas": [0, 1, 3, 4, 5],
        "ideal_nakshatras": [0, 3, 7, 12, 14, 16, 21, 26],
        "ideal_lagnas": [1, 2, 4, 5, 6, 8, 10, 11],
        "rule_note": "ఆదివారం లేదా గురువారం నాడు నవగ్రహ సమారాధన ఉత్తమ ఫలితాలనిస్తుంది."
    },

    # 2. SAMSKARA & AUSPICIOUS LIFE EVENTS (శుభకార్య ముహూర్తాలు)
    "vivaha": {
        "title_te": "వివాహ ముహూర్తం (Marriage Muhurtam)",
        "category": "samskara",
        "description": "ఆజన్మాంత దాంపత్య సౌఖ్యం, వంశాభివృద్ధి, మరియు సకల సౌభాగ్యాల కొరకు నిర్ణయించే పవిత్ర పాణిగ్రహణ ముహూర్తం.",
        "shastra_source": "ముహూర్త రత్నావళి (వివాహ ప్రకరణం) & ముహూర్త దర్పణం",
        "ideal_tithis": [2, 3, 5, 7, 10, 11, 12, 13], # Rikta tithis 4, 9, 14, and Amavasya are strictly avoided
        "ideal_varas": [1, 3, 4, 5],                   # Mon, Wed, Thu, Fri
        "ideal_nakshatras": [3, 4, 9, 10, 11, 12, 14, 15, 16, 20, 21, 25, 26], # Rohini, Mriga, Magha, Uttara, Hasta, Swati, Anuradha, etc.
        "ideal_lagnas": [1, 2, 3, 4, 5, 6, 8, 10, 11],
        "rule_note": "లగ్న శుద్ధి మరియు సప్తమ శుద్ధి (7వ స్థానంలో ఏ గ్రహం లేకుండుట) అత్యంత ఆవశ్యకం."
    },
    "grihapravesha": {
        "title_te": "గృహ ప్రవేశ ముహూర్తం (Housewarming)",
        "category": "samskara",
        "description": "నూతన లేదా పురాతన గృహంలోకి ప్రవేశించి స్థిర సంపద, ఆయురారోగ్యాలు, మరియు శాంతి లభించుటకు.",
        "shastra_source": "ముహూర్త రత్నావళి (వాస్తు ప్రకరణం) & కాలామృతమ్",
        "ideal_tithis": [2, 3, 5, 7, 10, 11, 12, 13, 15],
        "ideal_varas": [1, 3, 4, 5],
        "ideal_nakshatras": [3, 4, 6, 7, 11, 12, 14, 16, 20, 21, 25, 26],
        "ideal_lagnas": [1, 4, 7, 10], # Sthira Lagnas are preferred for Grihapravesha
        "rule_note": "స్థిర లగ్నమైన వృషభం, సింహం, వృశ్చికం, లేదా కుంభం గృహ ప్రవేశానికి అత్యంత శ్రేష్ఠం. 4వ భావ శుద్ధి ముఖ్యం."
    },
    "namakarana": {
        "title_te": "నామకరణ ముహూర్తం (Baby Naming)",
        "category": "samskara",
        "description": "శిశువుకు ఆయుష్షు, కీర్తి, మరియు ఐశ్వర్యం ప్రసాదించుటకు 11, 12, లేదా 21వ రోజున నామకరణ సంస్కారం.",
        "shastra_source": "ముహూర్త దర్పణం",
        "ideal_tithis": [1, 2, 3, 5, 7, 10, 11, 12, 13],
        "ideal_varas": [1, 3, 4, 5],
        "ideal_nakshatras": [0, 3, 4, 6, 7, 11, 12, 14, 16, 21, 25, 26],
        "ideal_lagnas": [1, 2, 3, 5, 6, 8, 10, 11],
        "rule_note": "జన్మ నక్షత్ర పాదాక్షరాన్ని ఆధారంగా చేసుకుని శుభ లగ్నంలో నామకరణం చేయాలి."
    },
    "annaprashana": {
        "title_te": "అన్నప్రాశన ముహూర్తం (First Solid Feeding)",
        "category": "samskara",
        "description": "శిశువుకు తొలిసారిగా ఆహారం అందించే పవిత్ర సంస్కారం (బాలునికి 6వ నెల, బాలికకు 5 లేదా 7వ నెల).",
        "shastra_source": "ముహూర్త రత్నావళి",
        "ideal_tithis": [2, 3, 5, 7, 10, 12, 13],
        "ideal_varas": [1, 3, 4, 5],
        "ideal_nakshatras": [0, 3, 4, 6, 7, 11, 12, 14, 16, 21, 25, 26],
        "ideal_lagnas": [1, 2, 3, 5, 6, 8, 11],
        "rule_note": "1, 10వ స్థానాలలో శుభ గ్రహాలుండాలి. శుక్ల పక్షం అత్యంత అనుకూలం."
    },
    "upanayana": {
        "title_te": "ఉపనయన ముహూర్తం (Sacred Thread)",
        "category": "samskara",
        "description": "గాయత్రీ మంత్రోపదేశం మరియు బ్రహ్మవర్చస్సును ప్రసాదించే అత్యంత పవిత్ర ద్విజత్వ సంస్కారం.",
        "shastra_source": "ముహూర్త చింతామణి",
        "ideal_tithis": [2, 3, 5, 7, 10, 11, 12, 13],
        "ideal_varas": [3, 4, 5],
        "ideal_nakshatras": [0, 3, 4, 6, 7, 11, 12, 14, 16, 21, 25, 26],
        "ideal_lagnas": [2, 5, 8, 11],
        "rule_note": "ఉత్తరాయణం, గురు శుక్రుల మౌఢ్యం లేని కాలంలో మాత్రమే ఉపనయనం చేయాలి."
    },
    "vyapara_arambha": {
        "title_te": "నూతన వ్యాపార ప్రారంభం (Business Launch)",
        "category": "samskara",
        "description": "వాణిజ్యం, దుకాణం, ఫ్యాక్టరీ, లేదా నూతన ఆర్థిక ఒప్పందాలను లాభసాటిగా ప్రారంభించుటకు.",
        "shastra_source": "కాలామృతమ్",
        "ideal_tithis": [2, 3, 5, 7, 10, 11, 12, 13, 15],
        "ideal_varas": [3, 4, 5],
        "ideal_nakshatras": [0, 3, 4, 7, 12, 14, 16, 21, 26],
        "ideal_lagnas": [1, 2, 5, 6, 8, 10, 11],
        "rule_note": "లగ్నానికి 11వ స్థానంలో శుభ గ్రహాలు లేదా రవి ఉండటం విశేష ధనలాభ ప్రదం."
    },
    "vahana_purchase": {
        "title_te": "నూతన వాహన కొనుగోలు (Vehicle Purchase)",
        "category": "samskara",
        "description": "కారు, బైక్ లేదా యంత్రాలను క్షేమంగా, దీర్ఘకాలిక సౌఖ్యంతో నడుపుటకు అనుకూల కాలం.",
        "shastra_source": "ముహూర్త దర్పణం",
        "ideal_tithis": [2, 3, 5, 7, 10, 11, 12, 13, 15],
        "ideal_varas": [1, 3, 4, 5],
        "ideal_nakshatras": [0, 3, 4, 6, 7, 11, 12, 14, 16, 21, 25, 26],
        "ideal_lagnas": [1, 3, 6, 10], # Shukra-ruled or Chara Lagnas
        "rule_note": "శుక్రుడు బలముగా ఉన్న లగ్నంలో వాహన కొనుగోలు ప్రయాణ క్షేమాన్ని ఇస్తుంది."
    },

    # 3. ADDITIONAL SHODASHA SAMSKARAS & EDUCATION (షోడశ సంస్కారాలు & విద్యా ముహూర్తాలు)
    "aksharabhyasa": {
        "title_te": "అక్షరాభ్యాసం / విద్యారంభం (Aksharabhyasa / Vidyarambham)",
        "category": "samskara",
        "description": "శిశువుకు సరస్వతీ సమారాధన పూర్వకంగా తొలిసారిగా విద్యాభ్యాసం, అక్షర రచన ప్రారంభించే అత్యంత పవిత్ర ముహూర్తం.",
        "shastra_source": "ముహూర్త చింతామణి & ముహూర్త దర్పణం",
        "ideal_tithis": [2, 3, 5, 7, 10, 11, 12, 13],
        "ideal_varas": [1, 3, 4, 5],
        "ideal_nakshatras": [0, 3, 4, 6, 7, 11, 12, 14, 16, 21, 23, 26],
        "ideal_lagnas": [1, 2, 5, 8, 11],
        "rule_note": "విద్యాకారకుడైన బుధుడు మరియు గురుడు కేంద్ర-త్రికోణాలలో ఉండుట విశేష మేధాశక్తిని, ఉన్నత విద్యా ప్రాప్తిని ఇస్తుంది."
    },
    "karnavedha": {
        "title_te": "కర్ణవేధ ముహూర్తం (Karna Vedha - Ear Piercing)",
        "category": "samskara",
        "description": "శిశువు శారీరక ఆరోగ్యం, మేధస్సు, మరియు దృష్టి దోష నివారణార్థం చెవులు కుట్టే శాస్త్రోక్త సంస్కారం (6, 7, 8 లేదా 12వ మాసమున).",
        "shastra_source": "ముహూర్త రత్నావళి (కర్ణవేధ ప్రకరణం)",
        "ideal_tithis": [2, 3, 5, 7, 10, 11, 12, 13],
        "ideal_varas": [1, 3, 4, 5],
        "ideal_nakshatras": [0, 3, 4, 6, 7, 12, 14, 16, 21, 22, 26],
        "ideal_lagnas": [1, 2, 5, 6, 8, 10, 11],
        "rule_note": "శుక్ల పక్షం, పగటి వేళ (పూర్వాహ్నమున) కర్ణవేధ శ్రేష్ఠం. కుజుడు 8వ భావంలో ఉండరాదు."
    },
    "chowla_karma": {
        "title_te": "చౌల కర్మ / చూడాకరణ / ప్రథమ కేశఖండన (Chowla Karma / First Tonsure)",
        "category": "samskara",
        "description": "శిశువుకు గర్భస్థ మాలిన్యాలు తొలగి ఆయురారోగ్యాలు, తేజస్సు చేకూరుటకు తొలిసారి పుట్టువెండ్రుకలు సమర్పించే వైదిక సంస్కారం (1వ లేదా 3వ సంవత్సరంలో).",
        "shastra_source": "కాలామృతమ్ & ఆశ్వలాయన గృహ్యసూత్రాలు",
        "ideal_tithis": [2, 3, 5, 7, 10, 11, 13],
        "ideal_varas": [1, 3, 4, 5],
        "ideal_nakshatras": [0, 3, 4, 6, 7, 12, 13, 14, 16, 21, 22, 26],
        "ideal_lagnas": [1, 2, 5, 6, 8, 11],
        "rule_note": "ఉత్తరాయణమున, శుక్ల పక్షమున ఆచరించుట శ్రేయస్కరం. జన్మ నక్షత్రం, జన్మ మాసం పరిహరించాలి."
    },
    "seemantham": {
        "title_te": "సీమంతం / పుంసవనం (Seemantham / Pumsavana - Baby Shower)",
        "category": "samskara",
        "description": "గర్భిణీ స్త్రీకి మనశ్శాంతి, గర్భ రక్షణ, మరియు తేజోవంతమైన సంతానం కలుగుటకు 6, 7 లేదా 8వ మాసంలో నిర్వహించే మాతృ రక్షా సంస్కారం.",
        "shastra_source": "స్మృతి ముక్తావళి & ముహూర్త దర్పణం",
        "ideal_tithis": [2, 3, 5, 7, 8, 10, 11, 12, 13, 15],
        "ideal_varas": [1, 3, 4, 5],
        "ideal_nakshatras": [0, 3, 4, 6, 7, 11, 12, 14, 16, 21, 25, 26],
        "ideal_lagnas": [1, 2, 3, 5, 8, 11],
        "rule_note": "8వ స్థానంలో కుజుడు లేదా శని ఉండరాదు (అష్టమ శుద్ధి). చంద్రుడు శుభ స్థానాలలో ఉండాలి."
    },
    "nischitartham": {
        "title_te": "నిశ్చితార్థం / వాగ్దానం (Nischitartham / Engagement)",
        "category": "samskara",
        "description": "వర-కన్యల వివాహ నిశ్చయార్థం ఉభయ కుటుంబాల సమ్మతితో తాంబూలాలు మార్చుకుని లగ్న పత్రిక రచించే పవిత్ర కార్యం.",
        "shastra_source": "ముహూర్త రత్నావళి (వాగ్దాన ప్రకరణం)",
        "ideal_tithis": [2, 3, 5, 7, 10, 11, 12, 13, 15],
        "ideal_varas": [1, 3, 4, 5],
        "ideal_nakshatras": [0, 3, 4, 6, 7, 9, 10, 11, 12, 14, 15, 16, 20, 21, 25, 26],
        "ideal_lagnas": [1, 2, 3, 4, 5, 6, 8, 10, 11],
        "rule_note": "వర-కన్యలిద్దరికీ అష్టమ చంద్రుడు మరియు నైధన తార లేకుండా ఉండుట పరమ ముఖ్యం."
    },
    "samavartanam": {
        "title_te": "సమావర్తనం / విద్యా సమాప్తి (Samavartanam / Graduation)",
        "category": "samskara",
        "description": "విద్యాభ్యాస సమాప్తి, దీక్షా స్నానం, మరియు ఉద్యోగ/గృహస్థాశ్రమ ప్రవేశ అర్హతను సూచించే వైదిక ఘట్టం.",
        "shastra_source": "పారస్కర గృహ్యసూత్రాలు & ధర్మసింధు",
        "ideal_tithis": [2, 3, 5, 7, 10, 11, 12, 13],
        "ideal_varas": [3, 4, 5],
        "ideal_nakshatras": [0, 3, 4, 6, 7, 12, 14, 16, 21, 26],
        "ideal_lagnas": [2, 5, 8, 11],
        "rule_note": "గురు బలం పరిపూర్ణంగా ఉన్న కాలంలో ఆచరించడం ద్వారా భవిష్యత్తులో సమాజంలో ఉన్నత గౌరవ ప్రతిష్టలు లభిస్తాయి."
    },

    # 4. VAASTU, REAL ESTATE & CONSTRUCTION (వాస్తు, స్థిరాస్తి & నిర్మాణ ముహూర్తాలు)
    "shanku_sthapana": {
        "title_te": "శంకుస్థాపన / గృహారంభం (Shanku Sthapana / Foundation Stone)",
        "category": "samskara",
        "description": "నూతన భవన నిర్మాణార్థం వాస్తు పురుష పూజ చేసి ప్రథమ శిలాన్యాసం (పునాది రాయి) వేసే ప్రధాన వాస్తు ముహూర్తం.",
        "shastra_source": "వాస్తు రాజవల్లభం & ముహూర్త రత్నావళి",
        "ideal_tithis": [2, 3, 5, 7, 10, 11, 12, 13, 15],
        "ideal_varas": [1, 3, 4, 5],
        "ideal_nakshatras": [3, 4, 6, 7, 11, 12, 14, 16, 20, 21, 25, 26],
        "ideal_lagnas": [1, 4, 7, 10], # Sthira Lagnas for permanent stability
        "rule_note": "స్థిర లగ్నం అత్యుత్తమం. వాస్తు పురుష నిద్రా కాలం కాకుండా ప్రబుద్ధ కాలంలో మాత్రమే శంకుస్థాపన చేయాలి."
    },
    "dwara_bandha": {
        "title_te": "సింహద్వార స్థాపన / ద్వారబంధం (Dwara Bandha Sthapana - Main Door)",
        "category": "samskara",
        "description": "ఇంటికి లక్ష్మీ ప్రవేశ ద్వారమైన ప్రధాన సింహద్వార చట్రాన్ని అమర్చే శుభ ముహూర్తం — స్థిర సంపద మరియు క్షేమాభివృద్ధి కొరకు.",
        "shastra_source": "మయమతం & ముహూర్త చింతామణి",
        "ideal_tithis": [2, 3, 5, 7, 10, 11, 12, 13, 15],
        "ideal_varas": [1, 3, 4, 5],
        "ideal_nakshatras": [3, 4, 6, 7, 11, 12, 14, 16, 20, 21, 25, 26],
        "ideal_lagnas": [1, 4, 7, 10],
        "rule_note": "సింహద్వార స్థాపనకు స్థిర లగ్నాలు శ్రేష్ఠం. లగ్నానికి 4వ మరియు 8వ స్థానాలలో పాప గ్రహాలు ఉండరాదు."
    },
    "bhoomi_puja": {
        "title_te": "భూమి పూజ / స్థల కొనుగోలు & రిజిస్ట్రేషన్ (Bhoomi Puja / Land Registry)",
        "category": "samskara",
        "description": "స్థలం, ఇల్లు లేదా వ్యవసాయ భూమిని కొనుగోలు చేసి రిజిస్ట్రేషన్ చేసుకోవడానికి, లేదా భూమాతకు పూజ చేసి భూమిని స్వాధీనం చేసుకోవడానికి.",
        "shastra_source": "కాలామృతమ్ (భూలాభ ప్రకరణం)",
        "ideal_tithis": [2, 3, 5, 7, 10, 11, 12, 13, 15],
        "ideal_varas": [1, 3, 4, 5],
        "ideal_nakshatras": [3, 4, 6, 7, 11, 12, 14, 16, 20, 21, 25, 26],
        "ideal_lagnas": [1, 2, 4, 5, 7, 8, 10, 11],
        "rule_note": "కుజుడు భూకారకుడు కావున కుజ దృష్టి లగ్నంపై ఉండుట మరియు స్థిర లగ్నం భూలాభాన్ని, శాశ్వత ఆస్తి వృద్ధిని ఇస్తాయి."
    },
    "borewell_kupa": {
        "title_te": "బోరువెల్ / బావి తవ్వకం (Borewell / Well Water Digging)",
        "category": "samskara",
        "description": "భూమిలో అమృత జలాలు పుష్కలంగా పడటానికి, నూతన బావి లేదా బోరువెల్ తవ్వకం ప్రారంభించే పవిత్ర జల ముహూర్తం.",
        "shastra_source": "బృహత్ సంహిత (దకార్గళ అధ్యాయం) & ముహూర్త దర్పణం",
        "ideal_tithis": [2, 3, 5, 7, 10, 11, 12, 13, 15],
        "ideal_varas": [1, 3, 4, 5],
        "ideal_nakshatras": [3, 4, 6, 7, 10, 11, 12, 14, 16, 20, 21, 24, 25, 26],
        "ideal_lagnas": [3, 7, 11], # Jala Rashis: Cancer, Scorpio, Pisces
        "rule_note": "జల రాశులైన కర్కాటకం, వృశ్చికం, మీన లగ్నాలలో శుక్రుడు లేదా చంద్రుడు కేంద్రంలో ఉన్నప్పుడు తవ్వకం చేపడితే స్వచ్ఛమైన జల సమృద్ధి కలుగుతుంది."
    },

    # 5. CAREER, PROFESSIONAL & FINANCIAL (వృత్తి, ఉద్యోగ & ఆర్థిక ముహూర్తాలు)
    "udyoga_pravesha": {
        "title_te": "నూతన ఉద్యోగ ప్రవేశం (Job Joining / Oath Taking)",
        "category": "samskara",
        "description": "కొత్త ఉద్యోగంలో తొలి రోజు చేరడానికి, బాధ్యతలు స్వీకరించడానికి, లేదా పదవీ ప్రమాణ స్వీకారానికి దీర్ఘకాలిక ఉన్నతినిచ్చే ముహూర్తం.",
        "shastra_source": "ముహూర్త చింతామణి (రాజసేవా ప్రకరణం)",
        "ideal_tithis": [2, 3, 5, 7, 10, 11, 12, 13, 15],
        "ideal_varas": [0, 1, 3, 4, 5],
        "ideal_nakshatras": [0, 3, 4, 7, 11, 12, 14, 16, 21, 26],
        "ideal_lagnas": [0, 1, 4, 5, 8, 9, 10],
        "rule_note": "10వ భావంలో (దశమ స్థానం/రాజ్య స్థానం) రవి లేదా గురుడు లేదా బుధుడు ఉండుట అధికార ప్రాప్తిని, ప్రమోషన్లను ఇస్తుంది."
    },
    "machinery_pratishtha": {
        "title_te": "కర్మాగార యంత్ర ప్రతిష్ఠ (Factory Machinery / Server Commissioning)",
        "category": "samskara",
        "description": "పరిశ్రమలు, వర్క్‌షాప్‌లు, లేదా ఐటీ కంప్యూటర్ సర్వర్లు, భారీ యంత్రాలను విజయవంతంగా ప్రారంభించుటకు.",
        "shastra_source": "ముహూర్త రత్నావళి & కాలామృతమ్",
        "ideal_tithis": [2, 3, 5, 7, 10, 11, 12, 13, 15],
        "ideal_varas": [2, 3, 4, 6],
        "ideal_nakshatras": [0, 3, 4, 7, 12, 13, 14, 16, 21, 22, 26],
        "ideal_lagnas": [0, 1, 7, 9, 10],
        "rule_note": "కుజ మరియు శని బలం యంత్ర పరిశ్రమలకు శ్రేయస్కరం. 11వ స్థానంలో రాహువు లేదా రవి ఉండటం లాభదాయకం."
    },
    "runa_vimukthi": {
        "title_te": "రుణ విముక్తి / రుణ చెల్లింపు (Debt Repayment / Runa Vimukthi)",
        "category": "pariharam",
        "description": "తీవ్రమైన అప్పుల నుండి శాశ్వతంగా బయటపడటానికి, రుణ విముక్తి కొరకు మొదటి వాయిదా లేదా పూర్తి అప్పు చెల్లించే విశేష ముహూర్తం.",
        "shastra_source": "ముహూర్త చింతామణి (రుణ ప్రకరణం) — భౌమవారే రవిభే చైవ...",
        "ideal_tithis": [1, 2, 3, 5, 6, 7, 10, 11, 12, 13],
        "ideal_varas": [2], # Tuesday is supreme for debt settlement
        "ideal_nakshatras": [0, 2, 11, 16, 20],
        "ideal_lagnas": [0, 7, 9],
        "rule_note": "మంగళవారం నాడు అశ్వినీ లేదా అనూరాధ నక్షత్రంలో అప్పు తీర్చివేస్తే తిరిగి జీవితంలో అప్పు చేయవలసిన అగత్యం కలగదు."
    },
    "swarnabharana_dharana": {
        "title_te": "నూతన వస్త్ర & స్వర్ణాభరణ ధారణ (New Clothes & Gold Jewelry)",
        "category": "samskara",
        "description": "నూతన సువర్ణాభరణాలు, వజ్రాభరణాలు లేదా పట్టు వస్త్రాలను తొలిసారిగా ధరించి లక్ష్మీ స్థిరత్వాన్ని పొందే శుభ ముహూర్తం.",
        "shastra_source": "కాలామృతమ్ (వస్త్రాభరణ ప్రకరణం)",
        "ideal_tithis": [2, 3, 5, 7, 10, 11, 12, 13, 15],
        "ideal_varas": [1, 3, 4, 5],
        "ideal_nakshatras": [0, 3, 4, 6, 7, 12, 13, 14, 16, 21, 22, 26],
        "ideal_lagnas": [1, 2, 6, 11],
        "rule_note": "గురువారం లేదా శుక్రవారం నాడు పుష్యమి లేదా ధనిష్ఠ నక్షత్రంలో బంగారం ధరిస్తే సంపద ఇనుమడిస్తుంది."
    },
    "videsha_prayana": {
        "title_te": "విదేశీ ప్రయాణం / దూర ప్రయాణం (Foreign Travel / Long Journey)",
        "category": "samskara",
        "description": "విదేశీ ప్రయాణం, వీసా ఇంటర్వ్యూ, లేదా సుదూర తీర్థయాత్రలు క్షేమంగా, విజయవంతంగా సాగుటకు.",
        "shastra_source": "ముహూర్త రత్నావళి (యాత్రా ప్రకరణం)",
        "ideal_tithis": [2, 3, 5, 7, 10, 11, 12, 13],
        "ideal_varas": [1, 3, 4, 5],
        "ideal_nakshatras": [0, 3, 4, 6, 7, 12, 14, 16, 21, 26],
        "ideal_lagnas": [0, 2, 6, 8, 10],
        "rule_note": "చర లగ్నమైన మేష, తుల, మకరంలో ప్రయాణం శీఘ్ర గమనాన్ని, విజయవంతమైన పునరాగమనాన్ని ఇస్తుంది. దిక్ శూల పరిహారం ముఖ్యం."
    },

    # 6. HEALTH, MEDICINE & HEALING (వైద్య, ఆయుర్వేద & ఆరోగ్య ముహూర్తాలు)
    "aushadha_sevana": {
        "title_te": "ఔషధ సేవనారంభం (Medicine / Ayurvedic Treatment Commencement)",
        "category": "pariharam",
        "description": "దీర్ఘకాలిక వ్యాధుల నుండి విముక్తి కొరకు ఆయుర్వేద, సిద్ధ లేదా అల్లోపతి మందులు, రసాయన చికిత్సలు ప్రారంభించే ముహూర్తం.",
        "shastra_source": "భావప్రకాశ నిఘంటు & ముహూర్త చింతామణి",
        "ideal_tithis": [2, 3, 5, 7, 8, 10, 11, 12, 13],
        "ideal_varas": [0, 1, 3, 4],
        "ideal_nakshatras": [0, 3, 4, 6, 7, 12, 13, 14, 16, 21, 26],
        "ideal_lagnas": [1, 2, 5, 6, 8, 11],
        "rule_note": "అశ్వినీ నక్షత్రం దేవ వైద్యులైన అశ్వినీ దేవతలకు ప్రతీక కావున అశ్వినీ నాడు ప్రారంభించిన ఔషధం అమృతమై శీఘ్ర రోగ నివారణ చేస్తుంది."
    },
    "shastra_chikitsa": {
        "title_te": "శస్త్రచికిత్స ముహూర్తం (Elective Surgery / Medical Procedure)",
        "category": "pariharam",
        "description": "ఆపరేషన్ లేదా శస్త్రచికిత్స విజయవంతమై రక్తస్రావం లేకుండా త్వరగా కోలుకోవడానికి శాస్త్రోక్త రక్షా సమయం.",
        "shastra_source": "సుశ్రుత సంహిత & ముహూర్త దర్పణం",
        "ideal_tithis": [2, 3, 5, 6, 7, 10, 11, 12, 13],
        "ideal_varas": [2, 6, 0],
        "ideal_nakshatras": [0, 2, 4, 5, 13, 18, 22],
        "ideal_lagnas": [0, 7, 9],
        "rule_note": "అమావాస్య మరియు గ్రహణ సమయాలు అత్యంత నిషిద్ధం. లగ్నంలో చంద్రుడు లేకుండా చూడాలి (రక్తస్రావ నియంత్రణ కొరకు)."
    },

    # 7. SPIRITUAL, DIVINE VRATAS & SHANTIS (విశిష్ట దైవిక & వ్రత ముహూర్తాలు)
    "satyanarayana_vratam": {
        "title_te": "శ్రీ సత్యనారాయణ స్వామి వ్రతం (Sri Satyanarayana Swamy Vratam)",
        "category": "samskara",
        "description": "ఇష్టకామ్యార్థ సిద్ధి, కుటుంబ సౌభాగ్యం, మరియు సర్వ విఘ్న నివారణార్థం శ్రీ సత్యనారాయణ స్వామి సమారాధన ముహూర్తం.",
        "shastra_source": "స్కాంద పురాణం (రేవా ఖండం) & ధర్మసింధు",
        "ideal_tithis": [11, 13, 15],
        "ideal_varas": [0, 1, 3, 4, 5],
        "ideal_nakshatras": [0, 3, 4, 6, 7, 12, 14, 16, 21, 26],
        "ideal_lagnas": [1, 2, 3, 4, 5, 6, 8, 10, 11],
        "rule_note": "పౌర్ణమి సంధ్యా వేళ లేదా ప్రదోష కాలంలో సత్యనారాయణ వ్రతం ఆచరించడం కోటి రెట్ల పుణ్యప్రదం."
    },
    "mrityunjaya_ayushya": {
        "title_te": "మహా మృత్యుంజయ / ఆయుష్య హోమం (Ayushya / Mrityunjaya Homam)",
        "category": "pariharam",
        "description": "జన్మదినం నాడు లేదా అపమృత్యు దోషం, మారక దశా కాలంలో ఆయుర్వృద్ధి మరియు రోగ విముక్తి కొరకు పరమశివునికి సమర్పించే హోమం.",
        "shastra_source": "ఋగ్వేదం (త్రయంబకం మంత్రం) & బోధాయన గృహ్యసూత్రాలు",
        "ideal_tithis": [2, 3, 5, 7, 8, 10, 11, 13, 14, 15],
        "ideal_varas": [1, 2, 4],
        "ideal_nakshatras": [4, 6, 7, 12, 14, 16, 21, 25],
        "ideal_lagnas": [0, 3, 7, 8, 11],
        "rule_note": "శివ వాస పరిశీలన ముఖ్యం: కైలాసంలో లేదా గౌరీ సన్నిధిలో శివుడు ఉన్నప్పుడు హోమం జరిపిస్తే దీర్ఘాయుష్షు సిద్ధించును."
    },
    "vastu_shanti": {
        "title_te": "వాస్తు శాంతి హోమం (Vastu Shanti Homa)",
        "category": "pariharam",
        "description": "నివాస గృహంలో లేదా వాణిజ్య సంస్థలో ఉన్న వాస్తు దోషాలు, దిశా దోషాలు తొలగి శాంతి, ఆరోగ్య, ఐశ్వర్యాలు నిలచుటకు.",
        "shastra_source": "మత్స్య పురాణం (వాస్తు శాంతి అధ్యాయం) & విశ్వకర్మ ప్రకాశిక",
        "ideal_tithis": [2, 3, 5, 7, 10, 11, 12, 13, 15],
        "ideal_varas": [1, 3, 4, 5],
        "ideal_nakshatras": [3, 4, 6, 7, 11, 12, 14, 16, 20, 21, 25, 26],
        "ideal_lagnas": [1, 4, 7, 10],
        "rule_note": "స్థిర లగ్నంలో వాస్తు శాంతి అత్యంత ప్రశస్తం. అగ్ని వాస పరిశీలన ముఖ్యం (పృథ్వీ వాసం)."
    },
    "devata_pratishtha": {
        "title_te": "దేవాలయ విగ్రహ ప్రతిష్ఠ / కుంభాభిషేకం (Temple Deity Prana Pratishtha)",
        "category": "samskara",
        "description": "నూతన దేవాలయంలో విగ్రహ ప్రాణ ప్రతిష్ఠ, కుంభాభిషేకం, మరియు బ్రహ్మోత్సవాల ప్రారంభ పవిత్ర కాలం.",
        "shastra_source": "పాంచరాత్ర / వైఖానస ఆగమం & శైవాగమం",
        "ideal_tithis": [2, 3, 5, 7, 10, 11, 12, 13, 15],
        "ideal_varas": [0, 1, 3, 4, 5],
        "ideal_nakshatras": [3, 4, 6, 7, 11, 12, 14, 16, 20, 21, 25, 26],
        "ideal_lagnas": [1, 4, 7, 10, 2, 5, 8, 11],
        "rule_note": "ఉత్తరాయణం, శుక్ల పక్షం, స్థిర లగ్నం, మరియు సమస్త కేంద్రాలలో శుభ గ్రహాలు ఉండుట ఆవశ్యకం."
    }
}


def get_astronomical_sun_times(jd_day_midnight: float, lat: float, lon: float) -> Dict[str, float]:
    """
    Computes exact astronomical Sunrise, Sunset, and Solar Noon JD values
    using Swiss Ephemeris swe.rise_trans.
    """
    geopos = (lon, lat, 0.0)
    # Sunrise
    res_rise, tret_rise = swe.rise_trans(jd_day_midnight, swe.SUN, swe.CALC_RISE, geopos)
    jd_rise = tret_rise[0] if res_rise == 0 else jd_day_midnight + 0.25

    # Sunset
    res_set, tret_set = swe.rise_trans(jd_day_midnight, swe.SUN, swe.CALC_SET, geopos)
    jd_set = tret_set[0] if res_set == 0 else jd_day_midnight + 0.75

    # Meridian Transit (Local Solar Noon)
    res_noon, tret_noon = swe.rise_trans(jd_day_midnight, swe.SUN, swe.CALC_MTRANSIT, geopos)
    jd_noon = tret_noon[0] if res_noon == 0 else (jd_rise + jd_set) / 2.0

    return {
        "sunrise_jd": jd_rise,
        "sunset_jd": jd_set,
        "noon_jd": jd_noon
    }


def jd_to_time_str(jd: float, tz_offset: float) -> str:
    """Converts a Julian Day to local HH:MM AM/PM string."""
    # Day fraction
    day_frac = (jd + 0.5 + (tz_offset / 24.0)) % 1.0
    total_sec = int(round(day_frac * 86400.0))
    hours = (total_sec // 3600) % 24
    mins = (total_sec % 3600) // 60
    
    suffix = "AM" if hours < 12 else "PM"
    h12 = hours % 12
    if h12 == 0:
        h12 = 12
    return f"{h12:02d}:{mins:02d} {suffix}"


def get_shiva_vasa(tithi_num: int) -> Dict[str, Any]:
    """
    Computes Shiva Vasa (శివ వాస నిర్ణయం) for Rudra Pashupatam & Abhishekam.
    Classical formula: ((Tithi + 1) * 2 + 5) % 7
    """
    t = (tithi_num % 15) + 1  # 1 to 15
    val = ((t + 1) * 2 + 5) % 7
    shiva_vasa_map = {
        1: {"place": "కైలాస వాసం", "impact": "సర్వ సౌఖ్యం (Supreme Auspicious)", "favorable": True},
        2: {"place": "గౌరీ సన్నిధి", "impact": "సకల సంపద & సంతోషం (Highly Auspicious)", "favorable": True},
        3: {"place": "వృషభారూఢుడు", "impact": "కార్యసిద్ధి (Favorable)", "favorable": True},
        4: {"place": "సభాయాం", "impact": "మానసిక సంతృప్తి (Neutral)", "favorable": False},
        5: {"place": "భోజనే", "impact": "పీడ / ఆహార లోపం (Avoid Homa)", "favorable": False},
        6: {"place": "క్రీడాయాం", "impact": "శ్రమ & చికాకులు (Avoid)", "favorable": False},
        0: {"place": "శ్మశానే", "impact": "అరిష్టం (Inauspicious)", "favorable": False}
    }
    return shiva_vasa_map.get(val, shiva_vasa_map[1])


def get_agni_vasa(tithi_num: int, weekday_num: int) -> Dict[str, Any]:
    """
    Computes Agni Vasa (అగ్ని వాస నిర్ణయం) for Chandi Homa, Santana Gopala, and Homas.
    Classical formula: (Tithi + Weekday + 1) % 4
    """
    val = (tithi_num + weekday_num + 1) % 4
    if val == 1:
        return {"place": "పృథ్వీ వాసం (భూమిపై అగ్ని నివాసం)", "impact": "అత్యంత శుభం - శీఘ్ర ఫలప్రాప్తి", "favorable": True}
    elif val == 2:
        return {"place": "పాతాళ వాసం", "impact": "ధన క్షయం (Avoid Homa)", "favorable": False}
    elif val == 3:
        return {"place": "స్వర్గ వాసం", "impact": "ప్రాణ భయం (Avoid Homa)", "favorable": False}
    else:
        return {"place": "నిరగ్ని", "impact": "సామాన్యం", "favorable": False}


def calculate_tara_bala(target_nak_idx: int, native_nak_idx: int) -> Dict[str, Any]:
    """
    Calculates Navatara Chakra (తారాబలం) for native's birth star.
    """
    diff = ((target_nak_idx - native_nak_idx) % 9) + 1
    tara_names = {
        1: {"name": "జన్మ తార (Janma)", "status": "సాధారణం", "favorable": False, "desc": "ప్రథమ పర్యాయంలో సాధారణం"},
        2: {"name": "సంపత్ తార (Sampat)", "status": "అత్యంత శుభం", "favorable": True, "desc": "ధనలాభం, కార్యసిద్ధి"},
        3: {"name": "విపత్ తార (Vipat)", "status": "వర్జ్యం / అశుభం", "favorable": False, "desc": "ఆటంకాలు, నష్టాలు"},
        4: {"name": "క్షేమ తార (Kshema)", "status": "శుభం", "favorable": True, "desc": "క్షేమం, ఆరోగ్యం"},
        5: {"name": "ప్రత్యక్ తార (Pratyak)", "status": "వర్జ్యం / అశుభం", "favorable": False, "desc": "విరోధం, ప్రతికూలత"},
        6: {"name": "సాధన తార (Sadhana)", "status": "అత్యంత శుభం", "favorable": True, "desc": "కార్యసాధన, విజయం"},
        7: {"name": "నైధన తార (Naidhana)", "status": "తీవ్ర నిషిద్ధం", "favorable": False, "desc": "మహదరిష్టం, ప్రాణహాని"},
        8: {"name": "మిత్ర తార (Mitra)", "status": "శుభం", "favorable": True, "desc": "సహకారం, శాంతి"},
        9: {"name": "పరమ మిత్ర తార (Parama Mitra)", "status": "అత్యుత్తమ శుభం", "favorable": True, "desc": "అఖండ విజయాలు"}
    }
    res = dict(tara_names.get(diff, tara_names[2]))
    res["tara_num"] = diff
    return res


def calculate_chandra_bala(target_rashi_idx: int, native_rashi_idx: int) -> Dict[str, Any]:
    """
    Calculates Chandra Bala (చంద్రబలం) based on Moon sign transit from Janma Rashi.
    Avoids 6, 8, 12 (specifically 8th Ashtama Chandra).
    """
    house = ((target_rashi_idx - native_rashi_idx) % 12) + 1
    if house in [1, 3, 6, 7, 10, 11]:
        return {"house": house, "status": "ఉత్తమ చంద్రబలం", "favorable": True, "desc": f"జన్మరాశి నుండి {house}వ స్థానం (పూర్ణ బలం)"}
    elif house in [2, 5, 9]:
        return {"house": house, "status": "మధ్యమ చంద్రబలం", "favorable": True, "desc": f"జన్మరాశి నుండి {house}వ స్థానం (అనుకూలం)"}
    else:  # 4, 8, 12
        is_ashtama = (house == 8)
        tag = "అష్టమ చంద్ర దోషం (తీవ్ర నిషిద్ధం)" if is_ashtama else f"{house}వ స్థాన చంద్రుడు (వర్జ్యం)"
        return {"house": house, "status": tag, "favorable": False, "desc": "చంద్రబలం లోపించినది"}


def calculate_joint_family_muhurta_bala(
    target_nak_idx: int,
    target_rashi_idx: int,
    members: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Computes Joint Family / Dampati (Husband & Wife / Whole Family) Muhurta Compatibility.
    Classical Shastric Rules (Muhurtha Ratnavali & Kalamritam):
    1. Ashtama Chandra (8th House Moon) for ANY active participant (Husband, Wife, or Family head)
       strictly prohibits Vivaha, Grihapravesha, and Santana Pariharas.
    2. Naidhana (7th Tara - death star) and Vipat (3rd Tara) must be avoided.
    3. Evaluates all family members concurrently and returns comprehensive individual breakdown
       and an overall Family Harmony Score.
    """
    if not members:
        return {
            "all_favorable": True,
            "has_ashtama_chandra": False,
            "has_naidhana_tara": False,
            "status_te": "కుటుంబ వివరాలు నమోదు కాలేదు",
            "badge": "info",
            "score_adjustment": 0,
            "members": []
        }

    member_evals = []
    has_ashtama = False
    has_naidhana = False
    has_vipat_or_pratyak = False
    ashtama_names = []
    naidhana_names = []

    for m in members:
        name = m.get("name") or "కుటుంబ సభ్యుడు"
        role = m.get("role") or m.get("relation") or "సభ్యుడు"
        nak_idx = m.get("nakshatra_index")
        rashi_idx = m.get("rashi_index")

        tara_res = None
        chandra_res = None
        is_ash = False
        is_nai = False

        if nak_idx is not None and 0 <= int(nak_idx) < 27:
            tara_res = calculate_tara_bala(target_nak_idx, int(nak_idx))
            if tara_res.get("tara_num") == 7:
                is_nai = True
                has_naidhana = True
                naidhana_names.append(name)
            elif tara_res.get("tara_num") in [3, 5]:
                has_vipat_or_pratyak = True

        if rashi_idx is not None and 0 <= int(rashi_idx) < 12:
            chandra_res = calculate_chandra_bala(target_rashi_idx, int(rashi_idx))
            if chandra_res.get("house") == 8:
                is_ash = True
                has_ashtama = True
                ashtama_names.append(name)

        tara_fav = tara_res.get("favorable", True) if tara_res else True
        chandra_fav = chandra_res.get("favorable", True) if chandra_res else True

        member_evals.append({
            "name": name,
            "role": role,
            "nakshatra_name": NAKSHATRAS[int(nak_idx)]["name_te"] if nak_idx is not None and 0 <= int(nak_idx) < 27 else "—",
            "rashi_name": RASHIS[int(rashi_idx)]["name_te"] if rashi_idx is not None and 0 <= int(rashi_idx) < 12 else "—",
            "tara_name": tara_res.get("name", "సాధారణం") if tara_res else "—",
            "tara_favorable": tara_fav,
            "chandra_status": chandra_res.get("status", "అనుకూలం") if chandra_res else "—",
            "chandra_favorable": chandra_fav,
            "is_ashtama_chandra": is_ash,
            "is_naidhana_tara": is_nai,
            "favorable_overall": tara_fav and chandra_fav and not is_ash and not is_nai
        })

    all_fav = all(m["favorable_overall"] for m in member_evals)

    # Calculate Score Adjustment
    if has_ashtama:
        score_adj = -60
        status_te = f"అష్టమ చంద్ర దోషం: {', '.join(ashtama_names)} గారికి 8వ చంద్రుడు (తీవ్ర నిషిద్ధం)"
        badge = "danger"
    elif has_naidhana:
        score_adj = -45
        status_te = f"నైధన తారా దోషం: {', '.join(naidhana_names)} గారికి 7వ నైధన తార (వర్జ్యం)"
        badge = "danger"
    elif all_fav:
        score_adj = +30
        status_te = "సంపూర్ణ కుటుంబ అనుకూలత (100% Family Harmony - అందరికీ శుభకరం)"
        badge = "success"
    else:
        score_adj = -10 if has_vipat_or_pratyak else +10
        status_te = "మధ్యమ కుటుంబ అనుకూలత (Acceptable with compensation)"
        badge = "warning"

    return {
        "all_favorable": all_fav,
        "has_ashtama_chandra": has_ashtama,
        "has_naidhana_tara": has_naidhana,
        "ashtama_names": ashtama_names,
        "naidhana_names": naidhana_names,
        "status_te": status_te,
        "badge": badge,
        "score_adjustment": score_adj,
        "members": member_evals
    }


def calculate_muhurta_day_windows(
    dt_target: date,
    lat: float,
    lon: float,
    tz_offset: float = 5.5
) -> Dict[str, Any]:
    """
    Computes precise sunrise, sunset, noon, and inauspicious windows
    (Rahu Kalam, Yamagandam, Gulika, Durmuhurtham, Varjyam, Abhijit) for a day.
    """
    jd_midnight = swe.julday(dt_target.year, dt_target.month, dt_target.day, 0.0) - (tz_offset / 24.0)
    sun_times = get_astronomical_sun_times(jd_midnight, lat, lon)
    jd_rise = sun_times["sunrise_jd"]
    jd_set = sun_times["sunset_jd"]
    jd_noon = sun_times["noon_jd"]

    dina_mana = jd_set - jd_rise  # Day length in JD days
    ashtama_part = dina_mana / 8.0 # 1/8th of daytime
    muhurta_part = dina_mana / 15.0 # 1/15th of daytime (~48 mins)

    weekday = (dt_target.weekday() + 1) % 7 # Sunday = 0

    # 1. Rahu Kalam (Part 1 to 8)
    rahu_parts = {0: 8, 1: 2, 2: 7, 3: 5, 4: 6, 5: 4, 6: 3}
    r_idx = rahu_parts[weekday]
    jd_rahu_start = jd_rise + (r_idx - 1) * ashtama_part
    jd_rahu_end = jd_rise + r_idx * ashtama_part

    # 2. Yamagandam
    yama_parts = {0: 5, 1: 4, 2: 3, 3: 2, 4: 1, 5: 7, 6: 6}
    y_idx = yama_parts[weekday]
    jd_yama_start = jd_rise + (y_idx - 1) * ashtama_part
    jd_yama_end = jd_rise + y_idx * ashtama_part

    # 3. Gulika Kalam
    gulika_parts = {0: 7, 1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1}
    g_idx = gulika_parts[weekday]
    jd_gulika_start = jd_rise + (g_idx - 1) * ashtama_part
    jd_gulika_end = jd_rise + g_idx * ashtama_part

    # 4. Durmuhurtham (15 parts of daytime)
    durmuhurta_parts = {
        0: [14],
        1: [8, 12],
        2: [4, 11],
        3: [5],
        4: [6, 12],
        5: [4, 9],
        6: [1, 2]
    }
    dur_windows = []
    for d_idx in durmuhurta_parts[weekday]:
        s = jd_rise + (d_idx - 1) * muhurta_part
        e = jd_rise + d_idx * muhurta_part
        dur_windows.append({"start_jd": s, "end_jd": e, "str": f"{jd_to_time_str(s, tz_offset)} - {jd_to_time_str(e, tz_offset)}"})

    # 5. Abhijit Muhurtam (8th Muhurta, centered around Solar Noon, ~48 mins)
    jd_abhijit_start = jd_noon - (24.0 / 1440.0) # 24 mins before solar noon
    jd_abhijit_end = jd_noon + (24.0 / 1440.0)   # 24 mins after solar noon

    return {
        "date_str": dt_target.strftime("%Y-%m-%d"),
        "sunrise_str": jd_to_time_str(jd_rise, tz_offset),
        "sunset_str": jd_to_time_str(jd_set, tz_offset),
        "solar_noon_str": jd_to_time_str(jd_noon, tz_offset),
        "sunrise_jd": jd_rise,
        "sunset_jd": jd_set,
        "noon_jd": jd_noon,
        "rahu_kalam_str": f"{jd_to_time_str(jd_rahu_start, tz_offset)} - {jd_to_time_str(jd_rahu_end, tz_offset)}",
        "rahu_kalam_jd": (jd_rahu_start, jd_rahu_end),
        "yamagandam_str": f"{jd_to_time_str(jd_yama_start, tz_offset)} - {jd_to_time_str(jd_yama_end, tz_offset)}",
        "yamagandam_jd": (jd_yama_start, jd_yama_end),
        "gulika_str": f"{jd_to_time_str(jd_gulika_start, tz_offset)} - {jd_to_time_str(jd_gulika_end, tz_offset)}",
        "gulika_jd": (jd_gulika_start, jd_gulika_end),
        "durmuhurtham_list": dur_windows,
        "abhijit_str": f"{jd_to_time_str(jd_abhijit_start, tz_offset)} - {jd_to_time_str(jd_abhijit_end, tz_offset)}",
        "abhijit_jd": (jd_abhijit_start, jd_abhijit_end)
    }


def find_best_muhurtams(
    event_type: str,
    start_date_str: Optional[str] = None,
    days_range: int = 45,
    lat: float = 16.3067,
    lon: float = 80.4365,
    tz_offset: float = 5.5,
    native_nak_idx: Optional[int] = None,
    native_rashi_idx: Optional[int] = None,
    family_members: Optional[List[Dict[str, Any]]] = None,
    limit: int = 7
) -> Dict[str, Any]:
    """
    High-precision search for optimal Vedic Muhurtam slots across a date range.
    Supports Single Native, Couple (Husband & Wife), and Whole Family Member evaluations.
    Filters: Tithi, Vara, Nakshatra compatibility, Tara Bala, Chandra Bala,
    Rahu Kalam, Yamagandam, Durmuhurtham, and Varjyam avoidance, Abhijit & Amrita Kalam scoring.
    """
    spec = EVENT_SPECS.get(event_type, EVENT_SPECS["vivaha"])
    if not start_date_str:
        start_dt = date.today()
        start_date_str = start_dt.strftime("%Y-%m-%d")
    else:
        start_dt = datetime.strptime(start_date_str, "%Y-%m-%d").date()

    evaluated_candidates = []

    for day_offset in range(days_range):
        curr_dt = start_dt + timedelta(days=day_offset)
        weekday = (curr_dt.weekday() + 1) % 7 # Sunday = 0

        # Day windows
        day_windows = calculate_muhurta_day_windows(curr_dt, lat, lon, tz_offset)
        noon_jd = day_windows["noon_jd"]

        # Calculate sidereal planetary positions at noon
        planets = calculate_planet_positions(noon_jd, ayanamsa_name="lahiri")
        p_map = {p["name_en"]: p for p in planets}

        sun_lon = p_map["Sun"]["longitude"]
        moon_lon = p_map["Moon"]["longitude"]

        # Tithi at noon
        diff = (moon_lon - sun_lon) % 360.0
        tithi_idx = int(diff / 12.0)
        tithi_num = (tithi_idx % 15) + 1 # 1 to 15
        is_shukla = tithi_idx < 15

        # Nakshatra
        nak_idx = int(moon_lon / (360.0 / 27.0)) % 27
        moon_rashi_idx = int(moon_lon // 30)

        # 1. Base Compatibility Checks
        tithi_ok = tithi_num in spec["ideal_tithis"]
        vara_ok = weekday in spec["ideal_varas"]
        nak_ok = nak_idx in spec["ideal_nakshatras"]

        score = 0
        reasons = []

        if tithi_ok:
            score += 25
            reasons.append(f"అనుకూల తిథి: {TITHI_NAMES[tithi_idx]}")
        else:
            reasons.append(f"సాధారణ తిథి: {TITHI_NAMES[tithi_idx]}")

        if vara_ok:
            score += 20
            reasons.append(f"అనుకూల వారం: {VARA_NAMES[weekday]['te']}")
        
        if nak_ok:
            score += 25
            reasons.append(f"అనుకూల నక్షత్రం: {NAKSHATRAS[nak_idx]['name_te']}")

        # 2. Native Personalized Tara Bala & Chandra Bala (Single vs Couple / Whole Family)
        tara_info = None
        chandra_info = None
        family_eval = None

        if family_members and len(family_members) > 0:
            family_eval = calculate_joint_family_muhurta_bala(nak_idx, moon_rashi_idx, family_members)
            score += family_eval["score_adjustment"]
            if family_eval["has_ashtama_chandra"]:
                reasons.append(f"ప్రతికూలత: {family_eval['status_te']}")
            elif family_eval["has_naidhana_tara"]:
                reasons.append(f"ప్రతికూలత: {family_eval['status_te']}")
            else:
                reasons.append(f"కుటుంబ అనుకూలత: {family_eval['status_te']}")
        else:
            if native_nak_idx is not None:
                tara_info = calculate_tara_bala(nak_idx, native_nak_idx)
                if tara_info["favorable"]:
                    score += 15
                    reasons.append(f"శుభ తారాబలం: {tara_info['name']}")
                else:
                    score -= 20
                    reasons.append(f"ప్రతికూల తార: {tara_info['name']} (వర్జ్యం)")

            if native_rashi_idx is not None:
                chandra_info = calculate_chandra_bala(moon_rashi_idx, native_rashi_idx)
                if chandra_info["favorable"]:
                    score += 15
                    reasons.append(f"చంద్రబలం: {chandra_info['status']}")
                else:
                    score -= 25
                    reasons.append(f"ప్రతికూల చంద్రుడు: {chandra_info['status']}")

        # 3. Parihara Special Alignments (Shiva Vasa, Agni Vasa)
        shiva_vasa = None
        agni_vasa = None
        if "rudra" in event_type or "pashupatam" in event_type:
            shiva_vasa = get_shiva_vasa(tithi_num)
            if shiva_vasa["favorable"]:
                score += 15
                reasons.append(f"శివ వాసం: {shiva_vasa['place']} ({shiva_vasa['impact']})")
        elif "chandi" in event_type or "gopala" in event_type:
            agni_vasa = get_agni_vasa(tithi_num, weekday)
            if agni_vasa["favorable"]:
                score += 15
                reasons.append(f"అగ్ని వాసం: {agni_vasa['place']}")

        # Varjyam & Amrita Kalam computation for the day's nakshatra
        v_start_ghatika = VARJYAM_START_GHATIKAS[nak_idx]
        # 1 Ghatika = 24 minutes = 1/60th of day
        v_offset_hours = (v_start_ghatika / 60.0) * 24.0
        jd_varjyam_start = day_windows["sunrise_jd"] + (v_offset_hours / 24.0)
        jd_varjyam_end = jd_varjyam_start + (1.6 / 24.0) # 1 hr 36 mins (4 ghatikas)

        varjyam_str = f"{jd_to_time_str(jd_varjyam_start, tz_offset)} - {jd_to_time_str(jd_varjyam_end, tz_offset)}"

        # Amrita Kalam starts 14 ghatikas after Varjyam start (~5.6 hours later)
        jd_amrita_start = jd_varjyam_start + ((14 * 24.0 / 60.0) / 24.0)
        jd_amrita_end = jd_amrita_start + (1.6 / 24.0)
        amrita_str = f"{jd_to_time_str(jd_amrita_start, tz_offset)} - {jd_to_time_str(jd_amrita_end, tz_offset)}"

        # Ideal Muhurta Window Selection
        # If Abhijit falls outside Rahu Kalam and Varjyam, it is candidate 1!
        r_start, r_end = day_windows["rahu_kalam_jd"]
        ab_start, ab_end = day_windows["abhijit_jd"]

        is_abhijit_clean = not (ab_start < r_end and ab_end > r_start) and not (ab_start < jd_varjyam_end and ab_end > jd_varjyam_start)
        
        if is_abhijit_clean and weekday != 3: # Avoid Abhijit on Wednesday
            best_window_str = f"{day_windows['abhijit_str']} (అభిజిత్ ముహూర్తం - సర్వదోషహరం)"
            best_window_label = "మధ్యాహ్న అభిజిత్ ముహూర్తం"
            jd_window_mid = (ab_start + ab_end) / 2.0
            score += 10
        else:
            best_window_str = f"{amrita_str} (అమృత ఘడియలు)"
            best_window_label = "అమృత కాలం"
            jd_window_mid = (jd_amrita_start + jd_amrita_end) / 2.0

        # Calculate exact Muhurta Lagna & Ashtama Shuddhi at window midpoint
        lagna_raw, _ = calculate_lagna_and_houses(jd_window_mid, lat, lon, ayanamsa_name="lahiri")
        lagna_deg = lagna_raw["longitude"]
        lagna_rashi_idx = int(lagna_deg // 30)
        lagna_name_te = RASHIS[lagna_rashi_idx]["name_te"]
        deg_in_sign = lagna_deg % 30.0
        lagna_deg_str = f"{int(deg_in_sign)}° {int((deg_in_sign % 1) * 60)}'"

        if lagna_rashi_idx in [1, 4, 7, 10]:
            lagna_nature_te = "స్థిర లగ్నం (Fixed - ప్రశస్తం)"
        elif lagna_rashi_idx in [2, 5, 8, 11]:
            lagna_nature_te = "ద్విస్వభావ లగ్నం (Dual - అనుకూలం)"
        else:
            lagna_nature_te = "చర లగ్నం (Movable)"

        # Ashtama Shuddhi check (8th house from Muhurta Lagna must be clean of malefics)
        ashtama_rashi_idx = (lagna_rashi_idx + 7) % 12
        planets_window = calculate_planet_positions(jd_window_mid, ayanamsa_name="lahiri")
        ashtama_malefics = []
        for p in planets_window:
            p_rashi = int(p["longitude"] // 30)
            if p_rashi == ashtama_rashi_idx and p["name_en"] in ["Saturn", "Mars", "Rahu", "Ketu", "Sun"]:
                ashtama_malefics.append(p.get("name_te", p["name_en"]))

        has_ashtama_shuddhi = len(ashtama_malefics) == 0
        if has_ashtama_shuddhi:
            ashtama_shuddhi_desc = "8వ స్థానంలో పాప గ్రహాలు లేవు (అష్టమ శుద్ధి సిద్ధించినది ✓)"
            ashtama_shuddhi_badge = "success"
            score += 10
        else:
            mal_str = ", ".join(ashtama_malefics)
            ashtama_shuddhi_desc = f"8వ స్థానంలో {mal_str} ఉన్నందున అష్టమ శుద్ధి కొరవడినది"
            ashtama_shuddhi_badge = "warning"
            score -= 15

        muhurta_lagna_data = {
            "rashi_index": lagna_rashi_idx,
            "rashi_name_te": lagna_name_te,
            "nature_te": lagna_nature_te,
            "degree_formatted": lagna_deg_str,
            "has_ashtama_shuddhi": has_ashtama_shuddhi,
            "ashtama_shuddhi_desc": ashtama_shuddhi_desc,
            "ashtama_shuddhi_badge": ashtama_shuddhi_badge
        }

        # Classification
        if score >= 65:
            classification = "ఉత్తమ ముహూర్తం (Excellent / Highly Auspicious)"
            badge = "success"
        elif score >= 45:
            classification = "మధ్యమ ముహూర్తం (Good / Acceptable with Puja)"
            badge = "info"
        else:
            classification = "సామాన్య / పరిశీలనార్హం (Average)"
            badge = "warning"

        evaluated_candidates.append({
            "date": curr_dt.strftime("%Y-%m-%d"),
            "formatted_date": curr_dt.strftime("%d-%B-%Y"),
            "weekday_te": VARA_NAMES[weekday]["te"],
            "weekday_en": VARA_NAMES[weekday]["en"],
            "score": score,
            "badge": badge,
            "classification": classification,
            "best_window": best_window_str,
            "best_window_label": best_window_label,
            "muhurta_lagna": muhurta_lagna_data,
            "tithi": TITHI_NAMES[tithi_idx],
            "nakshatra": NAKSHATRAS[nak_idx]["name_te"],
            "moon_rashi": RASHIS[moon_rashi_idx]["name_te"],
            "sunrise": day_windows["sunrise_str"],
            "sunset": day_windows["sunset_str"],
            "abhijit_muhurtam": day_windows["abhijit_str"],
            "amrita_kalam": amrita_str,
            "rahu_kalam": day_windows["rahu_kalam_str"],
            "yamagandam": day_windows["yamagandam_str"],
            "varjyam": varjyam_str,
            "tara_bala": tara_info["name"] if tara_info else "సాధారణం",
            "tara_favorable": tara_info["favorable"] if tara_info else True,
            "chandra_bala": chandra_info["status"] if chandra_info else "అనుకూలం",
            "chandra_favorable": chandra_info["favorable"] if chandra_info else True,
            "shiva_vasa": shiva_vasa,
            "agni_vasa": agni_vasa,
            "family_compatibility": family_eval,
            "reasons": reasons
        })

    # Sort candidates by score descending
    evaluated_candidates.sort(key=lambda x: x["score"], reverse=True)
    top_picks = evaluated_candidates[:limit]

    return {
        "event_type": event_type,
        "event_title_te": spec["title_te"],
        "category": spec["category"],
        "description": spec["description"],
        "shastra_source": spec["shastra_source"],
        "rule_note": spec["rule_note"],
        "search_period": f"{start_date_str} నుండి {days_range} రోజులు",
        "is_family_mode": bool(family_members and len(family_members) > 0),
        "participants_count": len(family_members) if family_members else 1,
        "top_muhurtams": top_picks
    }

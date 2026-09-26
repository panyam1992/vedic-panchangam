# -*- coding: utf-8 -*-
"""
Authentic Vedic Remedy Verification & Puja Recheck Engine (శాస్త్రోక్త పరిహార పునఃపరిశీలన & నిర్ధారణ యంత్రం).
Provides authoritative Shastric validation for astrological remedies, pujas, and gemstones.
Evaluates whether a prescribed puja is genuinely necessary, cancelled by classical exceptions (దోష భంగం),
or prohibited (నిషిద్ధం), citing authentic classical authorities:
- బృహత్ పరాశర హోరాశాస్త్రం (Brihat Parashara Hora Shastra)
- జాతక చంద్రిక (Jataka Chandrika / Laghu Parashari)
- జాతకాభరణం (Jatakabharanam - Dhundhiraja)
- ఉత్తర కాలామృతం (Uttara Kalamritam - Mahakavi Kalidasa)
- ముహూర్త రత్నావళి (Muhurtha Ratnavali)
- జాతక పారిజాతం (Jataka Parijata)
- జాతక నారాయణీయమ్ (Jataka Narayaneeyam)
- ఫలదీపిక (Phaladeepika - Mantreswara)
"""

from typing import Dict, Any, List, Optional
from jyotishyam.services.kundali_calculator import RASHIS

# 12 Lagnas Functional Lordship & Gemstone Safety Rules (Jataka Chandrika)
# Trikona (1, 5, 9) lords' gems are NECTAR (అమృతం).
# Trika (6, 8, 12) lords' gems are POISON (విషం / నిషిద్ధం).
GEMSTONE_RULES_BY_LAGNA = {
    0: {  # Aries / మేషం
        "name_te": "మేష లగ్నం",
        "benefic_gems": [
            {"gem": "పగడం (Red Coral)", "planet": "కుజుడు", "bhava": "1వ లగ్నాధిపతి", "role": "జీవన రత్నం", "reason": "లగ్నాధిపతి కుజుని రత్నం. ఆయురారోగ్యాలు, ఆత్మవిశ్వాసం, నాయకత్వ శక్తిని ఇస్తుంది."},
            {"gem": "మాణిక్యం (Ruby)", "planet": "సూర్యుడు", "bhava": "5వ పంచమాధిపతి", "role": "అదృష్ట రత్నం", "reason": "పంచమ త్రికోణాధిపతి సూర్యుని రత్నం. మేధస్సు, ఉన్నత విద్యావిజయం, గౌరవాన్ని ప్రసాదిస్తుంది."},
            {"gem": "పుష్యరాగం (Yellow Sapphire)", "planet": "గురుడు", "bhava": "9వ భాగ్యాధిపతి", "role": "భాగ్య రత్నం", "reason": "భాగ్యాధిపతి దేవగురు బృహస్పతి రత్నం. దైవానుగ్రహం, ధనలాభం, కీర్తిని పెంచుతుంది."}
        ],
        "prohibited_gems": [
            {"gem": "పచ్చ (Emerald)", "planet": "బుధుడు", "houses": "3 మరియు 6వ అధిపతి", "reason": "బుధుడు 3, 6వ అధిపతిగా పాపి. పచ్చ ధరిస్తే రోగాలు, శత్రుపీడ, రక్త సంబంధ సమస్యలు రావచ్చు."},
            {"gem": "వజ్రం (Diamond) / తెల్ల జార్ఖాన్", "planet": "శుక్రుడు", "houses": "2 మరియు 7వ మారకాధిపతి", "reason": "శుక్రుడు ప్రబల మారకుడు (2, 7 అధిపతి). వజ్ర ధారణ వల్ల దాంపత్య చికాకులు, ఆరోగ్య క్షీణత రావచ్చు."},
            {"gem": "నీలం (Blue Sapphire)", "planet": "శని", "houses": "10 మరియు 11వ అధిపతి", "reason": "శని 11వ బాహ్య పాపిగా ఉంటాడు. పరిశీలన లేకుండా నీలం ధరించడం హానికరం."}
        ]
    },
    1: {  # Taurus / వృషభం
        "name_te": "వృషభ లగ్నం",
        "benefic_gems": [
            {"gem": "వజ్రం (Diamond)", "planet": "శుక్రుడు", "bhava": "1వ లగ్నాధిపతి", "role": "జీవన రత్నం", "reason": "లగ్నాధిపతి శుక్రుని రత్నం. ఆయురారోగ్యాలు, ఆకర్షణ, సౌఖ్యాన్ని పెంచుతుంది."},
            {"gem": "పచ్చ (Emerald)", "planet": "బుధుడు", "bhava": "2, 5వ అధిపతి", "role": "అదృష్ట రత్నం", "reason": "ధన-పంచమాధిపతి బుధుని రత్నం. విద్యాబుద్ధులు, వాక్చాతుర్యం, ధనసంచయాన్ని ఇస్తుంది."},
            {"gem": "నీలం (Blue Sapphire)", "planet": "శని", "bhava": "9, 10వ పరమ యోగకారకుడు", "role": "రాజయోగ రత్నం", "reason": "ధర్మ-కర్మాధిపతి శని వృషభ లగ్నానికి ఏకైక పరమ రాజయోగకారకుడు. అఖండ భాగ్యాన్ని ఇస్తుంది."}
        ],
        "prohibited_gems": [
            {"gem": "పుష్యరాగం (Yellow Sapphire)", "planet": "గురుడు", "houses": "8 మరియు 11వ అధిపతి", "reason": "గురుడు అష్టమాధిపతిగా తీవ్ర అశుభ ఫలితాలనిస్తాడు. పుష్యరాగం ధరిస్తే వ్యాపార నష్టాలు, అనారోగ్యం కలుగుతాయి."},
            {"gem": "పగడం (Red Coral)", "planet": "కుజుడు", "houses": "7 మరియు 12వ మారకాధిపతి", "reason": "కుజుడు 7, 12 స్థానాల మారకుడు. పగడం ధరిస్తే ప్రమాదాలు, దాంపత్య కలహాలు రావచ్చు."},
            {"gem": "ముత్యం (Pearl)", "planet": "చంద్రుడు", "houses": "3వ అధిపతి", "reason": "చంద్రుడు 3వ స్థానాధిపతిగా అశుభుడు. ముత్యం వల్ల మానసిక ఆందోళన పెరుగుతుంది."}
        ]
    },
    2: {  # Gemini / మిథునం
        "name_te": "మిథున లగ్నం",
        "benefic_gems": [
            {"gem": "పచ్చ (Emerald)", "planet": "బుధుడు", "bhava": "1, 4వ అధిపతి", "role": "జీవన రత్నం", "reason": "లగ్నాధిపతి బుధుని రత్నం. మేధోశక్తి, ఆరోగ్యం, వ్యాపార పురోగతికి శ్రేష్ఠం."},
            {"gem": "వజ్రం (Diamond)", "planet": "శుక్రుడు", "bhava": "5వ త్రికోణాధిపతి", "role": "అదృష్ట రత్నం", "reason": "పంచమాధిపతి శుక్రుని రత్నం. కళలు, సంతాన సౌఖ్యం, అదృష్టాన్ని ఇస్తుంది."},
            {"gem": "నీలం (Blue Sapphire)", "planet": "శని", "bhava": "9వ భాగ్యాధిపతి", "role": "భాగ్య రత్నం", "reason": "భాగ్యాధిపతి శని రత్నం. ధర్మ వర్తన, ఉన్నత పదవులు, స్థిరమైన భాగ్యోదయాన్ని ఇస్తుంది."}
        ],
        "prohibited_gems": [
            {"gem": "పగడం (Red Coral)", "planet": "కుజుడు", "houses": "6 మరియు 11వ అధిపతి - తీవ్ర పాపి", "reason": "కుజుడు మిథున లగ్నానికి పరమ శత్రువు మరియు రోగ-శత్రు స్థానాధిపతి. పగడం ధరిస్తే రక్తపోటు, శస్త్రచికిత్సలు, కోర్టు కేసులు సంభవిస్తాయి."},
            {"gem": "పుష్యరాగం (Yellow Sapphire)", "planet": "గురుడు", "houses": "7 మరియు 10వ కేంద్రాధిపత్య దోష & మారక గ్రహం", "reason": "గురుడు కేంద్రాధిపత్య దోషం కలిగిన మారకుడు. పుష్యరాగం ధరించడం అత్యంత ప్రమాదకరం."},
            {"gem": "మాణిక్యం (Ruby)", "planet": "సూర్యుడు", "houses": "3వ భ్రాతృ & పరాక్రమ స్థానాధిపతి", "reason": "సూర్యుడు త్రికోణాధిపతి కాదు, సాధారణంగా మాణిక్యం మిథున లగ్నానికి అనుకూలించదు."}
        ]
    },
    3: {  # Cancer / కర్కాటకం
        "name_te": "కర్కాటక లగ్నం",
        "benefic_gems": [
            {"gem": "ముత్యం (Natural Pearl)", "planet": "చంద్రుడు", "bhava": "1వ లగ్నాధిపతి", "role": "జీవన రత్నం", "reason": "లగ్నాధిపతి చంద్రుని రత్నం. మానసిక ప్రశాంతత, ఆరోగ్యం, దీర్ఘాయుష్షును ఇస్తుంది."},
            {"gem": "పగడం (Red Coral)", "planet": "కుజుడు", "bhava": "5, 10వ పరమ యోగకారకుడు", "role": "రాజయోగ రత్నం", "reason": "కుజుడు కర్కాటకానికి ఏకైక ధర్మ-కర్మ రాజయోగకారకుడు. అధికార ప్రాప్తి, ధైర్యం, భూ సంపద లభిస్తుంది."},
            {"gem": "పుష్యరాగం (Yellow Sapphire)", "planet": "గురుడు", "bhava": "9వ భాగ్యాధిపతి", "role": "భాగ్య రత్నం", "reason": "భాగ్యాధిపతి గురుని రత్నం. సంపద, దైవభక్తి, విద్యాభివృద్ధి చేకూరుస్తుంది."}
        ],
        "prohibited_gems": [
            {"gem": "వజ్రం (Diamond)", "planet": "శుక్రుడు", "houses": "4 మరియు 11వ అధిపతి - శత్రువు", "reason": "శుక్రుడు కర్కాటక లగ్నానికి పాపి. వజ్రం ధరిస్తే గృహ చికాకులు, అనారోగ్యం కలుగుతాయి."},
            {"gem": "పచ్చ (Emerald)", "planet": "బుధుడు", "houses": "3 మరియు 12వ వ్యయాధిపతి", "reason": "బుధుడు 12వ వ్యయాధిపతి. పచ్చ ధరిస్తే ఆర్థిక నష్టాలు, వ్యయాలు పెరుగుతాయి."},
            {"gem": "నీలం (Blue Sapphire)", "planet": "శని", "houses": "7 మరియు 8వ ఆయుః/మారకాధిపతి", "reason": "శని 8వ రంధ్రాధిపతి మరియు మారకుడు. నీలం ధరించడం నిషిద్ధం."}
        ]
    },
    4: {  # Leo / సింహం
        "name_te": "సింహ లగ్నం",
        "benefic_gems": [
            {"gem": "మాణిక్యం (Ruby)", "planet": "సూర్యుడు", "bhava": "1వ లగ్నాధిపతి", "role": "జీవన రత్నం", "reason": "లగ్నాధిపతి సూర్యుని రత్నం. తేజస్సు, నాయకత్వం, ప్రభుత్వ గుర్తింపు, ఆయుష్షు నిస్తుంది."},
            {"gem": "పగడం (Red Coral)", "planet": "కుజుడు", "bhava": "4, 9వ పరమ యోగకారకుడు", "role": "భాగ్య రత్నం", "reason": "కుజుడు సింహ లగ్నానికి పూర్ణ యోగకారకుడు. అదృష్టం, భూములు, ఉన్నత పదవులు లభిస్తాయి."},
            {"gem": "పుష్యరాగం (Yellow Sapphire)", "planet": "గురుడు", "bhava": "5వ పంచమాధిపతి", "role": "అదృష్ట రత్నం", "reason": "పంచమాధిపతి గురుని రత్నం. సంతాన ప్రాప్తి, వివేకం, ఆధ్యాత్మిక ఉన్నతి నిస్తుంది."}
        ],
        "prohibited_gems": [
            {"gem": "వజ్రం (Diamond)", "planet": "శుక్రుడు", "houses": "3 మరియు 10వ అధిపతి - సూర్య శత్రువు", "reason": "శుక్రుడు సూర్యునికి బద్ధ శత్రువు. వజ్రం ధరిస్తే వృత్తిలో అవమానాలు రావచ్చు."},
            {"gem": "నీలం (Blue Sapphire)", "planet": "శని", "houses": "6 మరియు 7వ శత్రు/మారకాధిపతి", "reason": "శని 6వ రోగ స్థానాధిపతి. నీలం ధరిస్తే దీర్ఘకాలిక రోగాలు, శత్రువులు పెరుగుతారు."},
            {"gem": "పచ్చ (Emerald)", "planet": "బుధుడు", "houses": "2 మరియు 11వ అధిపతి", "reason": "పరిశీలన లేకుండా పచ్చ ధరిస్తే కుటుంబంలో వివాదాలు రావచ్చు."}
        ]
    },
    5: {  # Virgo / కన్య
        "name_te": "కన్యా లగ్నం",
        "benefic_gems": [
            {"gem": "పచ్చ (Emerald)", "planet": "బుధుడు", "bhava": "1, 10వ అధిపతి", "role": "జీవన రత్నం", "reason": "లగ్న-కర్మాధిపతి బుధుని రత్నం. వ్యాపార విజయం, ఆరోగ్యం, మేధోవికాసాన్ని ఇస్తుంది."},
            {"gem": "వజ్రం (Diamond)", "planet": "శుక్రుడు", "bhava": "2, 9వ భాగ్యాధిపతి", "role": "భాగ్య రత్నం", "reason": "భాగ్యాధిపతి శుక్రుని రత్నం. సంపద, విలాసాలు, అదృష్టాన్ని తెస్తుంది."},
            {"gem": "నీలం (Blue Sapphire)", "planet": "శని", "bhava": "5వ పంచమాధిపతి", "role": "అదృష్ట రత్నం", "reason": "పంచమాధిపతి శని రత్నం. స్థిరమైన ఆలోచనలు, విద్యా విజయం, పట్టుదలనిస్తుంది."}
        ],
        "prohibited_gems": [
            {"gem": "పగడం (Red Coral)", "planet": "కుజుడు", "houses": "3 మరియు 8వ అష్టమాధిపతి - పరమ పాపి", "reason": "కుజుడు కన్యా లగ్నానికి తీవ్ర పాపి. పగడం ధరిస్తే ప్రమాదాలు, శస్త్రచికిత్సలు, నష్టాలు సంభవిస్తాయి."},
            {"gem": "పుష్యరాగం (Yellow Sapphire)", "planet": "గురుడు", "houses": "4 మరియు 7వ కేంద్రాధిపత్య మారక గ్రహం", "reason": "గురుడు కేంద్రాధిపత్య దోషం కలిగిన మారకుడు. పుష్యరాగం ధరించడం తగదు."},
            {"gem": "ముత్యం (Pearl)", "planet": "చంద్రుడు", "houses": "11వ లాభాధిపతి", "reason": "చంద్రుడు పాప స్థానాధిపతిగా ఉంటాడు, ముత్యం సాధారణంగా సిఫార్సు చేయబడదు."}
        ]
    },
    6: {  # Libra / తుల
        "name_te": "తులా లగ్నం",
        "benefic_gems": [
            {"gem": "వజ్రం (Diamond)", "planet": "శుక్రుడు", "bhava": "1, 8వ లగ్నాధిపతి", "role": "జీవన రత్నం", "reason": "లగ్నాధిపతి శుక్రుని రత్నం. రూపలావణ్యం, ఆయుష్షు, ఆకర్షణను పెంచుతుంది."},
            {"gem": "నీలం (Blue Sapphire)", "planet": "శని", "bhava": "4, 5వ పరమ యోగకారకుడు", "role": "రాజయోగ రత్నం", "reason": "శని తులా లగ్నానికి ఏకైక పరమ రాజయోగకారకుడు. ఉన్నత పదవులు, గృహ-వాహన ప్రాప్తిని ఇస్తుంది."},
            {"gem": "పచ్చ (Emerald)", "planet": "బుధుడు", "bhava": "9వ భాగ్యాధిపతి", "role": "భాగ్య రత్నం", "reason": "భాగ్యాధిపతి బుధుని రత్నం. అదృష్టం, వ్యాపార లాభాలు, దైవానుగ్రహాన్ని ఇస్తుంది."}
        ],
        "prohibited_gems": [
            {"gem": "పుష్యరాగం (Yellow Sapphire)", "planet": "గురుడు", "houses": "3 మరియు 6వ తీవ్ర రోగాధిపతి", "reason": "గురుడు తులా లగ్నానికి పరమ పాపి (3, 6 అధిపతి). పుష్యరాగం ధరిస్తే తీవ్రమైన అనారోగ్యం, అప్పులు, శత్రువులు పెరుగుతారు."},
            {"gem": "మాణిక్యం (Ruby)", "planet": "సూర్యుడు", "houses": "11వ బాధకాధిపతి", "reason": "సూర్యుడు బాధకాధిపతి. మాణిక్యం ధరిస్తే పనులలో తీవ్రమైన ఆటంకాలు ఏర్పడతాయి."},
            {"gem": "పగడం (Red Coral)", "planet": "కుజుడు", "houses": "2 మరియు 7వ మారకాధిపతి", "reason": "కుజుడు ప్రబల మారకుడు. పగడం ధరించడం దాంపత్యానికి, ఆయుష్షుకు హానికరం."}
        ]
    },
    7: {  # Scorpio / వృశ్చికం
        "name_te": "వృశ్చిక లగ్నం",
        "benefic_gems": [
            {"gem": "పగడం (Red Coral)", "planet": "కుజుడు", "bhava": "1, 6వ లగ్నాధిపతి", "role": "జీవన రత్నం", "reason": "లగ్నాధిపతి కుజుని రత్నం. ఆత్మబలం, రోగనిరోధక శక్తి, విజయాన్ని ఇస్తుంది."},
            {"gem": "పుష్యరాగం (Yellow Sapphire)", "planet": "గురుడు", "bhava": "2, 5వ అధిపతి", "role": "అదృష్ట రత్నం", "reason": "ధన-పంచమాధిపతి గురుని రత్నం. సంతాన సౌఖ్యం, అపార ధనలాభం, గౌరవాన్ని ఇస్తుంది."},
            {"gem": "ముత్యం (Pearl)", "planet": "చంద్రుడు", "bhava": "9వ భాగ్యాధిపతి", "role": "భాగ్య రత్నం", "reason": "భాగ్యాధిపతి చంద్రుని రత్నం. భాగ్యోదయం, మనశ్శాంతి, శుభకార్యాలు నెరవేరుస్తుంది."}
        ],
        "prohibited_gems": [
            {"gem": "పచ్చ (Emerald)", "planet": "బుధుడు", "houses": "8 మరియు 11వ అధిపతి - తీవ్ర పాపి", "reason": "బుధుడు వృశ్చికానికి అష్టమాధిపతి. పచ్చ ధరిస్తే ఆకస్మిక నష్టాలు, నరాల బలహీనత కలుగుతాయి."},
            {"gem": "వజ్రం (Diamond)", "planet": "శుక్రుడు", "houses": "7 మరియు 12వ మారక/వ్యయాధిపతి", "reason": "శుక్రుడు మారకుడు మరియు వ్యయాధిపతి. వజ్రం ధరిస్తే దాంపత్యంలో విడాకులు లేదా నష్టాలు రావచ్చు."},
            {"gem": "నీలం (Blue Sapphire)", "planet": "శని", "houses": "3 మరియు 4వ అధిపతి", "reason": "శని సాధారణంగా వృశ్చికానికి పాపిగా పరిగణించబడతాడు."}
        ]
    },
    8: {  # Sagittarius / ధనుస్సు
        "name_te": "ధనుర్ లగ్నం",
        "benefic_gems": [
            {"gem": "పుష్యరాగం (Yellow Sapphire)", "planet": "గురుడు", "bhava": "1, 4వ లగ్నాధిపతి", "role": "జీవన రత్నం", "reason": "లగ్నాధిపతి గురుని రత్నం. ఆయురారోగ్యాలు, పాండిత్యం, ఉన్నత గౌరవాన్ని ప్రసాదిస్తుంది."},
            {"gem": "పగడం (Red Coral)", "planet": "కుజుడు", "bhava": "5, 12వ పంచమాధిపతి", "role": "అదృష్ట రత్నం", "reason": "పంచమ త్రికోణాధిపతి కుజుని రత్నం. ధైర్యం, బుద్ధికుశలత, కార్యసిద్ధిని ఇస్తుంది."},
            {"gem": "మాణిక్యం (Ruby)", "planet": "సూర్యుడు", "bhava": "9వ భాగ్యాధిపతి", "role": "భాగ్య రత్నం", "reason": "భాగ్యాధిపతి సూర్యుని రత్నం. పితృసౌఖ్యం, ప్రభుత్వ లాభాలు, భాగ్యోదయాన్ని కలిగిస్తుంది."}
        ],
        "prohibited_gems": [
            {"gem": "వజ్రం (Diamond)", "planet": "శుక్రుడు", "houses": "6 మరియు 11వ శత్రు/రోగ స్థానాధిపతి", "reason": "శుక్రుడు ధనుస్సుకు పరమ పాపి. వజ్రం ధరిస్తే శత్రువులు, రోగాలు, అప్పులు పెరుగుతాయి."},
            {"gem": "పచ్చ (Emerald)", "planet": "బుధుడు", "houses": "7 మరియు 10వ కేంద్రాధిపత్య మారకుడు", "reason": "బుధుడు కేంద్రాధిపత్య దోషం కలిగిన మారకుడు. పచ్చ ధరించడం అంత శ్రేయస్కరం కాదు."},
            {"gem": "నీలం (Blue Sapphire)", "planet": "శని", "houses": "2 మరియు 3వ మారకాధిపతి", "reason": "శని 2వ మారకుడు. నీలం ధరించడం హానికరం."}
        ]
    },
    9: {  # Capricorn / మకరం
        "name_te": "మకర లగ్నం",
        "benefic_gems": [
            {"gem": "నీలం (Blue Sapphire)", "planet": "శని", "bhava": "1, 2వ లగ్నాధిపతి", "role": "జీవన రత్నం", "reason": "లగ్నాధిపతి శని రత్నం. ఆయురారోగ్యాలు, స్థిరత్వం, వ్యాపార పురోగతిని ఇస్తుంది."},
            {"gem": "వజ్రం (Diamond)", "planet": "శుక్రుడు", "bhava": "5, 10వ పరమ రాజయోగకారకుడు", "role": "రాజయోగ రత్నం", "reason": "శుక్రుడు మకర లగ్నానికి పూర్ణ రాజయోగకారకుడు. విలాసాలు, పదవులు, అదృష్టాన్ని ఇస్తుంది."},
            {"gem": "పచ్చ (Emerald)", "planet": "బుధుడు", "bhava": "9వ భాగ్యాధిపతి", "role": "భాగ్య రత్నం", "reason": "భాగ్యాధిపతి బుధుని రత్నం. ఉన్నత విద్య, దైవానుగ్రహం, భాగ్యవృద్ధిని తెస్తుంది."}
        ],
        "prohibited_gems": [
            {"gem": "పుష్యరాగం (Yellow Sapphire)", "planet": "గురుడు", "houses": "3 మరియు 12వ వ్యయాధిపతి - పరమ పాపి", "reason": "గురుడు మకరానికి తీవ్ర పాపి. పుష్యరాగం ధరిస్తే ధన నష్టం, అనారోగ్యం, వ్యయాలు పెరుగుతాయి."},
            {"gem": "పగడం (Red Coral)", "planet": "కుజుడు", "houses": "4 మరియు 11వ బాధకాధిపతి", "reason": "కుజుడు పాప ఫలితాలనిస్తాడు. పగడం ధరిస్తే కలహాలు, రక్తపోటు రావచ్చు."},
            {"gem": "ముత్యం (Pearl)", "planet": "చంద్రుడు", "houses": "7వ మారకాధిపతి", "reason": "చంద్రుడు ప్రబల మారకుడు. ముత్యం ధరించడం శ్రేయస్కరం కాదు."}
        ]
    },
    10: {  # Aquarius / కుంభం
        "name_te": "కుంభ లగ్నం",
        "benefic_gems": [
            {"gem": "నీలం (Blue Sapphire)", "planet": "శని", "bhava": "1, 12వ లగ్నాధిపతి", "role": "జీవన రత్నం", "reason": "లగ్నాధిపతి శని రత్నం. ఆయురారోగ్యాలు, నాయకత్వం, సంయమనాన్ని ఇస్తుంది."},
            {"gem": "వజ్రం (Diamond)", "planet": "శుక్రుడు", "bhava": "4, 9వ పరమ యోగకారకుడు", "role": "భాగ్య రత్నం", "reason": "శుక్రుడు కుంభానికి పూర్ణ యోగకారకుడు. గృహ-వాహన సౌఖ్యం, అదృష్టాన్ని ఇస్తుంది."},
            {"gem": "పచ్చ (Emerald)", "planet": "బుధుడు", "bhava": "5వ పంచమాధిపతి", "role": "అదృష్ట రత్నం", "reason": "పంచమాధిపతి బుధుని రత్నం. మేధోవికాసం, విద్యా విజయం, సంతాన క్షేమాన్ని ఇస్తుంది."}
        ],
        "prohibited_gems": [
            {"gem": "పుష్యరాగం (Yellow Sapphire)", "planet": "గురుడు", "houses": "2 మరియు 11వ ధన/పాప స్థానాధిపతి", "reason": "గురుడు 2వ మారకుడు మరియు 11వ పాపి. పుష్యరాగం ధరించడం ప్రమాదకరం."},
            {"gem": "పగడం (Red Coral)", "planet": "కుజుడు", "houses": "3 మరియు 10వ అధిపతి - శత్రువు", "reason": "కుజుడు లగ్నాధిపతి శనికి శత్రువు. పగడం ధరిస్తే ఆటంకాలు, వివాదాలు వస్తాయి."},
            {"gem": "ముత్యం (Pearl)", "planet": "చంద్రుడు", "houses": "6వ రోగ స్థానాధిపతి", "reason": "చంద్రుడు 6వ రోగాధిపతి. ముత్యం ధరిస్తే శత్రువులు, వ్యాధులు పెరుగుతాయి."}
        ]
    },
    11: {  # Pisces / మీనం
        "name_te": "మీన లగ్నం",
        "benefic_gems": [
            {"gem": "పుష్యరాగం (Yellow Sapphire)", "planet": "గురుడు", "bhava": "1, 10వ లగ్నాధిపతి", "role": "జీవన రత్నం", "reason": "లగ్నాధిపతి గురుని రత్నం. ఆయురారోగ్యాలు, దైవభక్తి, కీర్తి ప్రతిష్టలను ఇస్తుంది."},
            {"gem": "ముత్యం (Pearl)", "planet": "చంద్రుడు", "bhava": "5వ పంచమాధిపతి", "role": "అదృష్ట రత్నం", "reason": "పంచమ త్రికోణాధిపతి చంద్రుని రత్నం. సంతాన సౌఖ్యం, విద్యావిజయం, మానసిక ప్రశాంతతనిస్తుంది."},
            {"gem": "పగడం (Red Coral)", "planet": "కుజుడు", "bhava": "2, 9వ భాగ్యాధిపతి", "role": "భాగ్య రత్నం", "reason": "భాగ్యాధిపతి కుజుని రత్నం. ధనలాభం, ధైర్యం, అదృష్టాన్ని తెస్తుంది."}
        ],
        "prohibited_gems": [
            {"gem": "వజ్రం (Diamond)", "planet": "శుక్రుడు", "houses": "3 మరియు 8వ అష్టమాధిపతి - తీవ్ర పాపి", "reason": "శుక్రుడు మీన లగ్నానికి పరమ శత్రువు మరియు అష్టమాధిపతి. వజ్రం ధరిస్తే తీవ్రమైన ప్రమాదాలు, నష్టాలు, దాంపత్య విచ్ఛిన్నం రావచ్చు."},
            {"gem": "పచ్చ (Emerald)", "planet": "బుధుడు", "houses": "4 మరియు 7వ కేంద్రాధిపత్య మారకుడు", "reason": "బుధుడు కేంద్రాధిపత్య మారకుడు. పచ్చ ధరించడం హానికరం."},
            {"gem": "నీలం (Blue Sapphire)", "planet": "శని", "houses": "11 మరియు 12వ వ్యయాధిపతి", "reason": "శని 12వ వ్యయాధిపతి. నీలం ధరిస్తే ధనక్షయం, నిరాశ పెరుగుతాయి."}
        ]
    }
}


def audit_kuja_dosha_puja(lagna_info: Dict[str, Any], planets: List[Dict[str, Any]], kuja_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Audits whether Kuja Dosha Shanti Puja is genuinely necessary or cancelled.
    Cites: Muhurtha Ratnavali, Brihat Parashara Hora Shastra, Jataka Narayaneeyam.
    """
    p_map = {p["name_en"]: p for p in planets}
    mars = p_map.get("Mars")
    moon = p_map.get("Moon")
    venus = p_map.get("Venus")
    jupiter = p_map.get("Jupiter")

    if not mars:
        return {
            "puja_name": "కుజ దోష శాంతి పూజ (Kuja Dosha Shanti Puja)",
            "verdict_status": "no_dosha",
            "verdict_badge": "success",
            "verdict_title": "పూజ అవసరం లేదు (Not Required)",
            "verdict_summary": "జాతకంలో కుజ గ్రహ ప్రభావం సాధారణంగా ఉన్నందున ఎటువంటి కుజదోష పూజ చేయనవసరం లేదు.",
            "astrological_reason": "కుజుని సమాచారం లభించలేదు.",
            "shastra_authority": "ముహూర్త రత్నావళి",
            "cancellation_proof": "దోషం లేదు",
            "zero_cost_remedy": "నిత్య సుబ్రహ్మణ్య ప్రార్థన చాలును.",
            "commercial_warning": "ఖరీదైన శాంతి పూజలు చేయనవసరం లేదు."
        }

    mars_rashi = mars["rashi_index"]
    mars_bhava = mars["bhava"]
    h_moon = ((mars_rashi - moon["rashi_index"]) % 12) + 1 if moon else 0
    h_venus = ((mars_rashi - venus["rashi_index"]) % 12) + 1 if venus else 0

    dosha_houses = [1, 2, 4, 7, 8, 12]
    has_raw_dosha = (mars_bhava in dosha_houses) or (h_moon in dosha_houses) or (h_venus in dosha_houses)

    # Shastric Cancellations check
    cancellations = []
    if mars_rashi in [0, 7]:  # Mesha, Vrischika
        cancellations.append("కుజుడు స్వక్షేత్రమైన మేషం లేదా వృశ్చికంలో ఉన్నాడు (ముహూర్త రత్నావళి: స్వక్షేత్రస్థే కుజే దోషో న విద్యతే).")
    elif mars_rashi == 9:  # Makara
        cancellations.append("కుజుడు పరమోచ్ఛ రాశియైన మకరంలో ఉన్నాడు (జాతకాభరణం: ఉచ్ఛస్థే కుజే సర్వదోష నివృత్తిః).")

    if jupiter:
        jup_dist = ((jupiter["rashi_index"] - mars_rashi) % 12) + 1
        if jup_dist in [1, 5, 7, 9]:
            cancellations.append("కుజునిపై దేవగురువైన బృహస్పతి పవిత్ర దృష్టి లేదా సంయోగం ఉన్నది (పరాశర హోర: గురుదృష్టే కుజే దోషభంగః).")

    if moon and moon["rashi_index"] == mars_rashi:
        cancellations.append("చంద్ర-మంగళ సంయోగం వలన కుజదోషం పరిహారమై రాజయోగంగా మారినది (జాతక చంద్రిక).")

    if mars_bhava == 2 and mars_rashi in [2, 5]:  # Gemini / Virgo
        cancellations.append("2వ స్థానంలో మిథున లేదా కన్యారాశిలో కుజుడు ఉన్నందున శాస్త్రోక్త మినహాయింపు లభించినది.")
    elif mars_bhava == 4 and mars_rashi in [0, 7]:  # Aries / Scorpio
        cancellations.append("4వ స్థానంలో మేష లేదా వృశ్చిక రాశిలో కుజుడు ఉన్నందున దోష నివృత్తి అయినది.")
    elif mars_bhava == 7 and mars_rashi in [3, 9]:  # Cancer / Capricorn
        cancellations.append("7వ స్థానంలో కర్కాటకంలో నీచభంగం లేదా మకరంలో ఉచ్ఛ స్థితి వలన దోషం రద్దయినది.")
    elif mars_bhava == 8 and mars_rashi in [8, 11]:  # Sag / Pisces
        cancellations.append("8వ స్థానంలో గురు క్షేత్రాలైన ధనుస్సు లేదా మీనంలో కుజుడు ఉన్నందున శాస్త్రోక్త దోషరాహిత్యం.")
    elif mars_bhava == 12 and mars_rashi in [1, 6]:  # Taurus / Libra
        cancellations.append("12వ స్థానంలో వృషభ లేదా తులా రాశిలో కుజుడు ఉన్నందున దోషం వర్తించదు.")

    if not has_raw_dosha:
        return {
            "puja_name": "కుజ దోష శాంతి పూజ (Kuja Dosha Puja Verification)",
            "verdict_status": "no_dosha",
            "verdict_badge": "success",
            "verdict_title": "దోష రహితం — పూజ అవసరం లేదు (No Kuja Dosha)",
            "verdict_summary": f"కుజుడు లగ్నం నుండి {mars_bhava}వ భావంలో ఉన్నాడు. శాస్త్ర ప్రకారం ఇది కుజదోష స్థానం కాదు. కాబట్టి కుజదోష నివారణ పూజ చేయవలసిన అవసరం ఎంతమాత్రం లేదు.",
            "astrological_reason": f"కుజుడు లగ్నం నుండి {mars_bhava}వ భావంలో, చంద్రుని నుండి {h_moon}వ స్థానంలో ఉన్నారు (దోష స్థానాలైన 1, 2, 4, 7, 8, 12 లో లేరు).",
            "shastra_authority": "ముహూర్త రత్నావళి & బృహత్ పరాశర హోరాశాస్త్రం (అధ్యాయం 84)",
            "cancellation_proof": "కుజ దోష పరిధి వెలుపల గ్రహ స్థితి ఉన్నది.",
            "zero_cost_remedy": "రోజూ సాధారణ సుబ్రహ్మణ్యేశ్వర స్వామి స్మరణ చాలును.",
            "commercial_warning": "కొందరు జ్యోతిష్యులు సాధారణ గ్రహ స్థితులను చూపి కుజదోష పూజ చేయాలని సూచించవచ్చు; కానీ మీ జాతకంలో కుజదోషం లేనందున ఎటువంటి ఖరీదైన శాంతులు చేయనక్కర్లేదు."
        }
    elif len(cancellations) > 0:
        return {
            "puja_name": "కుజ దోష శాంతి పూజ (Kuja Dosha Puja Verification)",
            "verdict_status": "not_needed_cancelled",
            "verdict_badge": "info",
            "verdict_title": "దోష భంగం — ఖరీదైన పూజలు అవసరం లేదు (Cancelled / Exempted)",
            "verdict_summary": "కుజుడు దోష స్థానంలో ఉన్నప్పటికీ, ప్రామాణిక జ్యోతిష్య గ్రంథాల ప్రకారం బలమైన 'దోష భంగ మినహాయింపులు' లభించినందున దోష తీవ్రత పూర్తిగా తొలగిపోయింది. కావున వేలకు వేలు ఖర్చు చేసి ప్రత్యేక శాంతి పూజలు చేయనవసరం లేదు.",
            "astrological_reason": f"కుజుడు {mars_bhava}వ స్థానంలో ఉన్నప్పటికీ: " + " | ".join(cancellations),
            "shastra_authority": "ముహూర్త రత్నావళి (వివాహ ప్రకరణం) & జాతక నారాయణీయమ్: 'కుజే వ్యయే చ పాతాళే జామాత్రే చాష్టమే కుజే... శుభదృష్టే న దోషః'",
            "cancellation_proof": " • " + "\n • ".join(cancellations),
            "zero_cost_remedy": "మంగళవారం నాడు ఇంట్లోనే సుబ్రహ్మణ్యాష్టకం లేదా స్కంద షష్ఠి కవచం పఠించండి. శివాలయంలో దీపారాధన శ్రేయస్కరం.",
            "commercial_warning": "దోష భంగం జరిగిన జాతకాలకు కూడా కొందరు పూజలు తప్పనిసరి అని భయపెడతారు. శాస్త్రోక్తంగా దోష నివృత్తి జరిగినందున భయపడవలసిన పని లేదు."
        }
    else:
        return {
            "puja_name": "కుజ దోష శాంతి పూజ (Kuja Dosha Puja Verification)",
            "verdict_status": "recommended_mild",
            "verdict_badge": "warning",
            "verdict_title": "దోష పరిశీలనార్హం — శాస్త్రోక్త సాధన శ్రేయస్కరం (Valid Kuja Presence)",
            "verdict_summary": f"కుజుడు లగ్నం నుండి {mars_bhava}వ స్థానంలో ఉన్నారు. వివాహ విషయాలలో కుజ దోష సామ్యం కలిగిన జాతకాన్ని ఎంచుకోవడం ప్రాథమిక శాస్త్రోక్త విధి. ఖరీదైన తాంత్రిక పూజల కన్నా నిత్య వైదిక ఆరాధన ఉత్తమ ఫలితాలనిస్తుంది.",
            "astrological_reason": f"కుజుడు లగ్నం నుండి {mars_bhava}వ భావంలో ({RASHIS[mars_rashi]['name_te']} రాశి), చంద్రుని నుండి {h_moon}వ భావంలో ఉన్నాడు. ప్రత్యక్ష శుభగ్రహ దృష్టి లేదు.",
            "shastra_authority": "బృహత్ పరాశర హోరాశాస్త్రం & జాతకాభరణం",
            "cancellation_proof": "ప్రత్యక్ష దోషభంగ కారణాలు లేవు; వివాహ కుండలి మేళనంలో కుజదోష సామ్యం చూడాలి.",
            "zero_cost_remedy": "1. రోజూ సుబ్రహ్మణ్య భుజంగ స్తోత్రం లేదా సుబ్రహ్మణ్యాష్టకం పారాయణం. 2. మంగళవారం 'ఓం భౌమాయ నమః' 108 సార్లు జపం (మొత్తం జప సంఖ్య: 10,000). 3. మంగళవారం కందులు లేదా ఎరుపు వస్త్రం దానం.",
            "commercial_warning": "వివాహానికి కుజదోష సామ్యం సరిచూసుకోవడమే నిజమైన శాస్త్ర పరిష్కారం. కొందరు చేసే భారీ ఖర్చుల పూజల కన్నా భక్తితో చేసే సుబ్రహ్మణ్యారాధన అత్యంత ఫలవంతమైనది."
        }


def audit_kalasarpa_puja(planets: List[Dict[str, Any]], kalasarpa_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Audits Kala Sarpa Puja requirement and protects against unwarranted panic.
    Cites: Jatakabharanam, Jataka Parijata.
    """
    p_map = {p["name_en"]: p for p in planets}
    rahu = p_map.get("Rahu")
    ketu = p_map.get("Ketu")

    if not rahu or not ketu:
        return {
            "puja_name": "కాలసర్ప దోష శాంతి పూజ (Kala Sarpa Puja Verification)",
            "verdict_status": "no_dosha",
            "verdict_badge": "success",
            "verdict_title": "పూజ అవసరం లేదు (No Dosha)",
            "verdict_summary": "కాలసర్ప దోషం లేదు. ప్రత్యేక పూజలు అవసరం లేదు.",
            "astrological_reason": "సప్త గ్రహాలు స్వేచ్ఛగా ఉన్నాయి.",
            "shastra_authority": "జాతకాభరణం",
            "cancellation_proof": "దోష రహితం",
            "zero_cost_remedy": "నిత్య శివ నామస్మరణ.",
            "commercial_warning": "కాలసర్ప దోష భయాలు నిరాధారం."
        }

    rahu_lon = rahu["longitude"]
    ketu_lon = ketu["longitude"]
    seven_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    lons = [p_map[name]["longitude"] for name in seven_planets if name in p_map]

    if len(lons) < 7:
        side1_count = 0
    else:
        def in_arc(lon, start, end):
            return ((lon - start) % 360.0) <= ((end - start) % 360.0)
        side1_count = sum(1 for lon in lons if in_arc(lon, rahu_lon, ketu_lon))

    is_full = (side1_count == 7 or side1_count == 0)
    is_partial = (side1_count == 6 or side1_count == 1)

    if not is_full and not is_partial:
        return {
            "puja_name": "కాలసర్ప దోష శాంతి పూజ (Kala Sarpa Puja Verification)",
            "verdict_status": "no_dosha",
            "verdict_badge": "success",
            "verdict_title": "దోష రహితం — కాలసర్ప పూజ అవసరం లేదు (No Kala Sarpa)",
            "verdict_summary": "గ్రహాలు రాహు-కేతువుల ఇరువైపులా స్వేచ్ఛగా సంచరిస్తున్నాయి. మీ జాతకంలో కాలసర్ప దోషం ఎంతమాత్రం లేదు. కాబట్టి కాలసర్ప శాంతి లేదా నాగదోష పూజలు చేయనవసరం లేదు.",
            "astrological_reason": f"సప్త గ్రహాలలో {side1_count} గ్రహాలు ఒకవైపు, {7 - side1_count} గ్రహాలు రెండవవైపు ఉన్నాయి. రాహు-కేతువుల బంధనం లేదు.",
            "shastra_authority": "జాతకాభరణం & జాతక పారిజాతం",
            "cancellation_proof": "సప్త గ్రహాలు రాహు-కేతువుల అక్షం వెలుపల ఉన్నాయి.",
            "zero_cost_remedy": "ప్రదోష కాలంలో శివ దర్శనం సాధారణ శుభకరం.",
            "commercial_warning": "కొందరు స్వల్ప రాహు-కేతు స్థితులను చూసి కాలసర్ప దోషమని భయపెట్టి పూజలు చేయిస్తుంటారు. శాస్త్రోక్తంగా మీ జాతకంలో దోషం లేదు."
        }
    elif is_partial:
        return {
            "puja_name": "కాలసర్ప దోష శాంతి పూజ (Kala Sarpa Puja Verification)",
            "verdict_status": "not_needed_cancelled",
            "verdict_badge": "info",
            "verdict_title": "అంశిక కాలసర్పం — ఖరీదైన పూజలు అవసరం లేదు (Partial / Not Harmful)",
            "verdict_summary": "ఒక గ్రహం రాహు-కేతువుల పరిధి వెలుపల ఉన్నందున ఇది పూర్ణ కాలసర్పం కాదు (అంశిక ప్రభావం మాత్రమే). దీనికి భారీ ఖర్చులతో కూడిన శాంతి హోమాలు చేయనక్కర్లేదు. సాధారణ శివారాధనతో సర్వ శుభాలు కలుగుతాయి.",
            "astrological_reason": "ఆరు గ్రహాలు రాహు-కేతువుల మధ్య ఉండి, ఒక గ్రహం స్వతంత్రంగా బయట ఉన్నందున కాలసర్ప బంధనం భంగమైనది.",
            "shastra_authority": "జాతక పారిజాతం & పూర్వ కాలామృతం",
            "cancellation_proof": "ఒక గ్రహం రాహు-కేతువుల పరిధి దాటి ఉన్నందున పూర్ణ కాలసర్పం వర్తించదు.",
            "zero_cost_remedy": "ప్రతి సోమవారం శివ పంచాక్షరీ జపం (ఓం నమః శివాయ) 108 సార్లు చేయండి. శివాలయ దర్శనం శుభకరం.",
            "commercial_warning": "అంశిక కాలసర్పానికి శ్రీకాళహస్తి లేదా త్రయంబకేశ్వర్ వెళ్లి వేల రూపాయల పూజలు చేయవలసిన అత్యవసరం లేదు."
        }
    else:
        return {
            "puja_name": "కాలసర్ప దోష శాంతి పూజ (Kala Sarpa Puja Verification)",
            "verdict_status": "recommended_mild",
            "verdict_badge": "warning",
            "verdict_title": "పూర్ణ కాలసర్పం — భయపడకండి, వైదిక పరిహారం చాలు (Full Kala Sarpa)",
            "verdict_summary": "సప్త గ్రహాలు రాహు-కేతువుల మధ్య బంధించబడి ఉన్నాయి. అయితే శాస్త్రం ప్రకారం కాలసర్పం జీవిత ద్వితీయార్ధంలో అఖండ రాజయోగాన్ని కూడా ఇస్తుంది. భయపడవలసిన అవసరం లేదు; శాస్త్రోక్త దైవారాధన సరిపోతుంది.",
            "astrological_reason": "ఏడు భౌతిక గ్రహాలూ రాహు-కేతువుల ఒకే అర్ధగోళంలో ఉన్నాయి.",
            "shastra_authority": "జాతకాభరణం: 'రాహు కేతు అంతర్గతే సర్వే గ్రహాః...'",
            "cancellation_proof": "లగ్నాధిపతి లేదా గురు బలం ఉన్నచో క్రమంగా రాజయోగంగా మారుతుంది.",
            "zero_cost_remedy": "1. రోజూ మహా మృత్యుంజయ మంత్రం 108 సార్లు పఠించండి (మొత్తం జపం: 11,000). 2. శుక్లపక్ష షష్ఠి లేదా ప్రదోషం నాడు శివునికి పాలాభిషేకం చేయండి. 3. పక్షులకు లేదా చీమలకు ఆహారం వేయండి.",
            "commercial_warning": "కాలసర్ప దోషం పేరుతో చేసే భయాల దోపిడీకి గురికాకండి. నిత్య శివారాధన మరియు మృత్యుంజయ జపం ద్వారా సమస్త ప్రతికూలతలు తొలగి విజయం లభిస్తుంది."
        }


def audit_shani_puja(lagna_info: Dict[str, Any], planets: List[Dict[str, Any]], dasha_data: Dict[str, Any], gocharam_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Audits Saturn (Shani Shanti / Sade Sati / Ashtama Shani) Puja.
    Cites: Jataka Chandrika, Dasharatha Shani Stotram.
    """
    lagna_idx = lagna_info["rashi_index"]
    shani_gochara = gocharam_data.get("shani_gochara", {})
    is_sade_sati = shani_gochara.get("is_severe", False) or "ఏలినాటి" in shani_gochara.get("status", "") or "అష్టమ" in shani_gochara.get("status", "")

    # Check if Saturn is Yogakaraka
    is_yogakaraka = lagna_idx in [1, 6]  # Taurus, Libra
    curr_m = dasha_data.get("current_mahadasha", {})
    is_shani_dasha = curr_m.get("lord") == "Saturn"

    if is_yogakaraka:
        return {
            "puja_name": "శని శాంతి / ఏలినాటి శని పూజ (Saturn Shanti Verification)",
            "verdict_status": "not_needed_cancelled",
            "verdict_badge": "info",
            "verdict_title": "శని యోగకారకుడు — ప్రత్యేక శాంతి పూజ అవసరం లేదు (Yogakaraka Saturn)",
            "verdict_summary": f"{lagna_info['rashi_name_te']} లగ్నానికి శని భగవానుడు ఏకైక పరమ రాజయోగకారకుడు (ధర్మ-కర్మాధిపతి). కాబట్టి గోచారంలో ఏలినాటి శని లేదా అష్టమ శని నడుస్తున్నప్పటికీ శని హాని చేయడు; కృషికి తగిన శాశ్వత అభివృద్ధిని ఇస్తాడు.",
            "astrological_reason": f"లగ్నాధిపతి శుక్రునికి శని పరమ మిత్రుడు. జాతక చంద్రిక ప్రకారం శని పూర్ణ యోగకారుడు.",
            "shastra_authority": "జాతక చంద్రిక: 'వృషభస్య శనైశ్చర ఏక ఏవ రాజయోగకారకః' / 'తులాయాం మందో యోగప్రదః'",
            "cancellation_proof": "లగ్న పరమ రాజయోగకారక గ్రహం ఎన్నడూ తీవ్ర అరిష్టాన్ని కలిగించదు.",
            "zero_cost_remedy": "రోజూ హనుమాన్ చాలీసా లేదా దశరథ ప్రోక్త శని స్తోత్రం పఠించడం అత్యుత్తమం.",
            "commercial_warning": "వృషభ, తులా లగ్నాలకు శని శాంతి పేరుతో చేయించే ఖరీదైన పూజలు శాస్త్ర విరుద్ధం."
        }
    elif not is_sade_sati and not is_shani_dasha:
        return {
            "puja_name": "శని శాంతి / ఏలినాటి శని పూజ (Saturn Shanti Verification)",
            "verdict_status": "no_dosha",
            "verdict_badge": "success",
            "verdict_title": "శని దోషం లేదు — పూజ అవసరం లేదు (No Saturn Affliction)",
            "verdict_summary": "ప్రస్తుతం మీకు ఏలినాటి శని గానీ, అష్టమ శని గానీ, లేదా శని మహాదశ గానీ నడవడం లేదు. కావున శని శాంతి పూజ చేయవలసిన అవసరం ఎంతమాత్రం లేదు.",
            "astrological_reason": f"గోచార శని జన్మరాశి నుండి {shani_gochara.get('house', 'అనుకూల')}వ స్థానంలో ఉన్నాడు. ఏలినాటి శని వర్తించదు.",
            "shastra_authority": "ఫలదీపిక & జాతకాభరణం",
            "cancellation_proof": "గోచార మరియు దశా పరంగా శని అనుకూలంగా ఉన్నాడు.",
            "zero_cost_remedy": "సాధారణ ధర్మవర్తన, పేదలకు సహాయం చేయడం చాలును.",
            "commercial_warning": "అవసరం లేని సమయాలలో శని శాంతి పూజలు చేయించడం నిరర్థకం."
        }
    else:
        return {
            "puja_name": "శని శాంతి / ఏలినాటి శని పూజ (Saturn Shanti Verification)",
            "verdict_status": "recommended_mild",
            "verdict_badge": "warning",
            "verdict_title": "శని ప్రభావ కాలం — వైదిక దైవారాధన ఉత్తమం (Saturn Period Active)",
            "verdict_summary": "ప్రస్తుతం ఏలినాటి శని/అష్టమ శని లేదా శని దశ ప్రభావం ఉన్నది. శని న్యాయాధికారి; కష్టపడే తత్వాన్ని, క్రమశిక్షణను కోరుకుంటాడు. హోమాల కంటే దశరథ ప్రోక్త శని స్తోత్రం, హనుమత్సేవ మరియు సేవా కార్యక్రమాలు అత్యంత శక్తివంతమైన ఫలితాలనిస్తాయి.",
            "astrological_reason": f"గోచారం: {shani_gochara.get('status', 'శని ప్రభావం')}. దశా కాలంలో శ్రమ అధికమయ్యే అవకాశం.",
            "shastra_authority": "పద్మపురాణం (దశరథ ప్రోక్త శని స్తోత్రం) & బృహత్ పరాశర హోరాశాస్త్రం",
            "cancellation_proof": "శని జప సంఖ్య 23,000 లేదా నిత్య స్తోత్ర పారాయణం ద్వారా శాంతి కలుగును.",
            "zero_cost_remedy": "1. శనివారం దశరథ ప్రోక్త శని స్తోత్రం 11 సార్లు లేదా హనుమాన్ చాలీసా పఠించండి. 2. నువ్వుల నూనెతో శనివారం ప్రదోష వేళ దీపారాధన. 3. నిస్సహాయులకు, శ్రామికులకు నల్ల నువ్వులు, ఆహారం లేదా చెప్పులు దానం చేయండి.",
            "commercial_warning": "శని భగవానుడు భక్తికి, నీతికి మాత్రమే కరుగుతాడు; వేల రూపాయల వ్యాపార పూజల కంటే శ్రామికులకు చేసే అన్నదానమే నిజమైన శని శాంతి."
        }


def audit_gemstone_safety(lagna_info: Dict[str, Any], query_gem: Optional[str] = None) -> Dict[str, Any]:
    """
    Audits Gemstone wearing safety based on Lagna.
    Explicitly separates Recommended Trikona gems from Strictly Prohibited Trika (6, 8, 12) gems.
    Cites: Jataka Chandrika.
    """
    lagna_idx = lagna_info["rashi_index"]
    rules = GEMSTONE_RULES_BY_LAGNA.get(lagna_idx, GEMSTONE_RULES_BY_LAGNA[0])

    benefics = rules["benefic_gems"]
    prohibited = rules["prohibited_gems"]

    return {
        "lagna_name_te": rules["name_te"],
        "shastra_rule": "జాతక చంద్రిక ప్రమాణం: 'లగ్న-పంచమ-భాగ్యేషాః సర్వదా శుభదాయకాః... త్రికాధిపానాం రత్నాని న ధార్యాణి కదాచన' — లగ్న, పంచమ, భాగ్య త్రికోణాధిపతుల రత్నాలు మాత్రమే అమృత సమానమైనవి. 6, 8, 12 దుఃస్థానాధిపతుల రత్నాలు ధరిస్తే రోగాలు, శత్రువులు, ప్రమాదాలు పెరుగుతాయి.",
        "recommended_gems": benefics,
        "strictly_prohibited_gems": prohibited,
        "safety_summary": f"{rules['name_te']} జాతకులు కేవలం త్రికోణాధిపతుల రత్నాలైన {', '.join([b['gem'] for b in benefics])} మాత్రమే ధరించాలి. దుఃస్థానాధిపతుల రత్నాలైన {', '.join([p['gem'] for p in prohibited])} ధరిస్తే తీవ్రమైన నష్టాలు, ప్రమాదాలు వాటిల్లుతాయి."
    }


def audit_all_common_pujas(
    lagna_info: Dict[str, Any],
    planets: List[Dict[str, Any]],
    dasha_data: Dict[str, Any],
    panchangam: Dict[str, Any],
    gocharam: Dict[str, Any],
    kuja_data: Optional[Dict[str, Any]] = None,
    kalasarpa_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Runs a comprehensive Vedic Verification Audit across all common astrological pujas and remedies.
    """
    # 1. Kuja Dosha Puja Audit
    kuja_audit = audit_kuja_dosha_puja(lagna_info, planets, kuja_data)

    # 2. Kala Sarpa Puja Audit
    kalasarpa_audit = audit_kalasarpa_puja(planets, kalasarpa_data)

    # 3. Saturn / Sade Sati Puja Audit
    shani_audit = audit_shani_puja(lagna_info, planets, dasha_data, gocharam)

    # 4. Gemstone Safety Audit
    gems_audit = audit_gemstone_safety(lagna_info)

    # 5. Running Dasha-Bhukti Shanti Audit
    curr_m = dasha_data.get("current_mahadasha", {})
    curr_b = dasha_data.get("current_bhukti", {})
    m_lord_te = curr_m.get("lord_te", "దశానాథుడు")
    b_lord_te = curr_b.get("lord_te", "భుక్తినాథుడు")
    m_lord_en = curr_m.get("lord", "Sun")

    dasha_audit = {
        "puja_name": f"{m_lord_te} మహాదశ / {b_lord_te} అంతర్దశా శాంతి",
        "verdict_status": "recommended_mild",
        "verdict_badge": "info",
        "verdict_title": "నిత్య వైదిక ఆరాధన శ్రేయస్కరం (Vedic Dasha Sadhana)",
        "verdict_summary": f"ప్రస్తుతం జరుగుతున్న {m_lord_te} దశలో {b_lord_te} అంతర్దశకు అధిదేవతలను భక్తితో ఆరాధించడం వల్ల సమస్త కార్యవిఘ్నాలు తొలగి శుభాలు చేకూరుతాయి.",
        "astrological_reason": f"ప్రస్తుత మహాదశాధిపతి: {m_lord_te} ({curr_m.get('end_date', '')} వరకు), అంతర్దశాధిపతి: {b_lord_te} ({curr_b.get('end_date', '')} వరకు).",
        "shastra_authority": "బృహత్ పరాశర హోరాశాస్త్రం (దశాఫల అధ్యాయం)",
        "cancellation_proof": "గ్రహ మిత్రత్వం మరియు భావ స్థితిని బట్టి ఫలితాలు నిర్ణయించబడతాయి.",
        "zero_cost_remedy": f"దశాధిపతి {m_lord_te} అనుగ్రహం కొరకు సంబంధిత స్తోత్ర పారాయణం మరియు ధర్మ కార్యాలు ఆచరించండి.",
        "commercial_warning": "దశ మార్పు వచ్చినప్పుడల్లా ఖరీదైన హోమాలు చేయనవసరం లేదు; నిజమైన వైదిక నామ జపం శ్రేష్ఠమైనది."
    }

    # 6. Moola / Gandanta Audit
    nak_name = panchangam.get("nakshatra", "")
    pada_num = panchangam.get("pada", "1")
    is_moola = "మూల" in nak_name or "జ్యేష్ఠ" in nak_name or "ఆశ్లేష" in nak_name
    pada_int = int(str(pada_num)[0]) if str(pada_num)[0].isdigit() else 1

    if "మూల" in nak_name and pada_int == 4:
        moola_status = "not_needed_cancelled"
        moola_badge = "success"
        moola_title = "దోష రహితం — శాంతి పూజ అవసరం లేదు (Moola 4th Pada Auspicious)"
        moola_desc = "మూలా నక్షత్రం 4వ పాదంలో జన్మించిన వారికి ఎటువంటి దోషం ఉండదు. ఇది వంశాభివృద్ధిని ఇచ్చే ఉత్తమ పాదం. కాబట్టి మూలా శాంతి పూజ చేయనక్కర్లేదు."
    elif is_moola:
        moola_status = "recommended_mild"
        moola_badge = "warning"
        moola_title = "శాస్త్రోక్త నక్షత్ర శాంతి శ్రేయస్కరం (Nakshatra Shanti Recommended)"
        moola_desc = f"{nak_name} ({pada_num}) సంధికాల నక్షత్రం అయినందున జన్మదినం లేదా 27వ రోజున శాస్త్రోక్త నక్షత్ర శాంతి లేదా గోసేవ ఉత్తమం."
    else:
        moola_status = "no_dosha"
        moola_badge = "success"
        moola_title = "దోష రహితం — పూజ అవసరం లేదు (Safe Nakshatra)",
        moola_desc = f"{nak_name} నక్షత్రం ఎటువంటి గండాంత దోష పరిధిలో లేదు. నక్షత్ర శాంతి పూజ చేయవలసిన పని లేదు."

    moola_audit = {
        "puja_name": f"{nak_name} నక్షత్ర / గండాంత శాంతి పరిశీలన",
        "verdict_status": moola_status,
        "verdict_badge": moola_badge,
        "verdict_title": moola_title,
        "verdict_summary": moola_desc,
        "astrological_reason": f"జన్మ నక్షత్రం: {nak_name}, పాదం: {pada_num}.",
        "shastra_authority": "ముహూర్త రత్నావళి & కాలామృతమ్",
        "cancellation_proof": "నక్షత్ర పాద నిర్ణయం ప్రకారం ఫలితాలు నిర్ధారించబడ్డాయి.",
        "zero_cost_remedy": "రోజూ గాయత్రీ మంత్రం లేదా ఇష్టదైవ నామస్మరణ చేయండి.",
        "commercial_warning": "శుభ పాదాలలో పుట్టినప్పటికీ కొందరు నక్షత్ర శాంతి చేయాలని సూచిస్తారు; శాస్త్ర ప్రకారం మూల 4వ పాదం దోషరహితం."
    }

    all_audits = [
        kuja_audit,
        kalasarpa_audit,
        shani_audit,
        dasha_audit,
        moola_audit
    ]

    return {
        "summary": "శాస్త్రోక్త పరిహార పునఃసమీక్ష పూర్తయినది. జాతకంలో గ్రహ స్థితులు, బలహీనతలు, మరియు దోష భంగాలను ప్రామాణిక గ్రంథాల ఆధారంగా నిర్ధారించడమైనది.",
        "verified_pujas": all_audits,
        "gemstones_audit": gems_audit
    }

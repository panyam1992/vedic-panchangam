"""
Classical Astrological Tables Service.
Provides:
1. Ghata Chakra (ఘాత చక్రం - Parashara system)
2. Lucky Things (అదృష్ట విషయాలు - Days, Planets, Metals, Colors, Numbers, Deities)
3. Jaimini Chara Karakas (జైమిని చర కారకాలు: Atma to Dara) & Sthira Karakas
4. Maitri Chakra (మైత్రి చక్రం - Naisargika, Tatkalika, Panchadha)
5. Planetary & Bhava Aspects (గ్రహ & భావ వీక్షణలు)
6. Gemstones, Rudraksha & Ishta Devata (రత్న సూచన, రుద్రాక్ష, ఇష్ట దేవత)
7. Vastu House Facing (గృహ ముఖద్వారం & వాస్తు సూచనలు)
"""

from typing import Dict, Any, List, Optional
from jyotishyam.services.kundali_calculator import RASHIS

# 1. Ghata Chakra Specifications by Moon Sign (చంద్ర రాశి ఆధారంగా ఘాత చక్రం)
GHATA_SPECS = {
    0: {  # Mesha (Aries)
        "masa": "కార్తీక మాసం",
        "tithi": "పాడ్యమి, షష్ఠి, ఏకాదశి (నంద తిథులు)",
        "vara": "ఆదివారం",
        "nakshatra": "మఖ",
        "yoga": "విష్కంభ",
        "karana": "బవ",
        "prahar": "1వ ప్రహర (సూర్యోదయం నుండి 3 గంటలు)",
        "rashi": "వృశ్చిక రాశి"
    },
    1: {  # Vrishabha (Taurus)
        "masa": "మార్గశిర మాసం",
        "tithi": "పంచమి, దశమి, పూర్ణిమ (పూర్ణ తిథులు)",
        "vara": "శనివారం",
        "nakshatra": "హస్త",
        "yoga": "అతిగండ",
        "karana": "కౌలవ",
        "prahar": "2వ ప్రహర",
        "rashi": "కన్య రాశి"
    },
    2: {  # Mithuna (Gemini)
        "masa": "ఆషాఢ మాసం",
        "tithi": "తదియ, అష్టమి, త్రయోదశి (జయ తిథులు)",
        "vara": "సోమవారం",
        "nakshatra": "స్వాతి",
        "yoga": "ధృతి",
        "karana": "తైతిల",
        "prahar": "3వ ప్రహర",
        "rashi": "కుంభ రాశి"
    },
    3: {  # Karka (Cancer)
        "masa": "పుష్య మాసం",
        "tithi": "విదియ, సప్తమి, ద్వాదశి (భద్ర తిథులు)",
        "vara": "బుధవారం",
        "nakshatra": "అనూరాధ",
        "yoga": "శూల",
        "karana": "గరజ",
        "prahar": "4వ ప్రహర",
        "rashi": "మకర రాశి"
    },
    4: {  # Simha (Leo)
        "masa": "జ్యేష్ఠ మాసం",
        "tithi": "చవితి, నవమి, చతుర్దశి (రిక్త తిథులు)",
        "vara": "గురువారం",
        "nakshatra": "మూల",
        "yoga": "గండ",
        "karana": "వణిజ",
        "prahar": "1వ ప్రహర",
        "rashi": "మేష రాశి"
    },
    5: {  # Kanya (Virgo)
        "masa": "భాద్రపద మాసం",
        "tithi": "పంచమి, దశమి, పూర్ణిమ (పూర్ణ తిథులు)",
        "vara": "శనివారం",
        "nakshatra": "శ్రవణం",
        "yoga": "వ్యాఘాత",
        "karana": "విష్టి (భద్ర)",
        "prahar": "2వ ప్రహర",
        "rashi": "మిథున రాశి"
    },
    6: {  # Tula (Libra)
        "masa": "మాఘ మాసం",
        "tithi": "చవితి, నవమి, చతుర్దశి (రిక్త తిథులు)",
        "vara": "గురువారం",
        "nakshatra": "శతభిషం",
        "yoga": "శుక్ల",
        "karana": "తైతిల",
        "prahar": "4వ ప్రహర",
        "rashi": "ధనుస్సు రాశి"
    },
    7: {  # Vrischika (Scorpio)
        "masa": "వైశాఖ మాసం",
        "tithi": "విదియ, సప్తమి, ద్వాదశి (భద్ర తిథులు)",
        "vara": "శుక్రవారం",
        "nakshatra": "రేవతి",
        "yoga": "వజ్ర",
        "karana": "కౌలవ",
        "prahar": "3వ ప్రహర",
        "rashi": "వృషభ రాశి"
    },
    8: {  # Dhanu (Sagittarius)
        "masa": "ఫాల్గుణ మాసం",
        "tithi": "తదియ, అష్టమి, త్రయోదశి (జయ తిథులు)",
        "vara": "శుక్రవారం",
        "nakshatra": "భరణి",
        "yoga": "వ్యతీపాత",
        "karana": "బవ",
        "prahar": "2వ ప్రహర",
        "rashi": "సింహ రాశి"
    },
    9: {  # Makara (Capricorn)
        "masa": "చైత్ర మాసం",
        "tithi": "తదియ, అష్టమి, త్రయోదశి (జయ తిథులు)",
        "vara": "మంగళవారం",
        "nakshatra": "రోహిణి",
        "yoga": "పరిఘ",
        "karana": "గరజ",
        "prahar": "4వ ప్రహర",
        "rashi": "మీన రాశి"
    },
    10: {  # Kumbha (Aquarius)
        "masa": "శ్రావణ మాసం",
        "tithi": "చవితి, నవమి, చతుర్దశి (రిక్త తిథులు)",
        "vara": "గురువారం",
        "nakshatra": "ఆరుద్ర",
        "yoga": "శివ",
        "karana": "వణిజ",
        "prahar": "1వ ప్రహర",
        "rashi": "కర్కాటక రాశి"
    },
    11: {  # Meena (Pisces)
        "masa": "ఆశ్వయుజ మాసం",
        "tithi": "పాడ్యమి, షష్ఠి, ఏకాదశి (నంద తిథులు)",
        "vara": "శుక్రవారం",
        "nakshatra": "ఆశ్లేష",
        "yoga": "సిద్ధ",
        "karana": "బాలవ",
        "prahar": "2వ ప్రహర",
        "rashi": "తులా రాశి"
    }
}

# 2. Lucky Factors by Lagna (లగ్న ఆధారంగా అదృష్ట విషయాలు)
LUCKY_BY_LAGNA = {
    0: {  # Aries (Mesha)
        "days": "మంగళవారం, ఆదివారం, గురువారం",
        "planets": "కుజుడు, రవి, గురుడు",
        "friendly_rashis": "ధనుస్సు, సింహం, వృశ్చికం",
        "friendly_lagnas": "సింహం, ధనుస్సు, మీనం",
        "life_gem": "పగడం (Red Coral)",
        "lucky_gem": "మాణిక్యం (Ruby)",
        "bhagya_gem": "పుష్యరాగం (Yellow Sapphire)",
        "deity": "శ్రీ సుబ్రహ్మణ్యేశ్వర స్వామి, హనుమంతుడు",
        "metal": "రాగి (Copper), బంగారం",
        "color": "ఎరుపు, నారింజ, పసుపు",
        "direction": "తూర్పు (East)",
        "time": "సూర్యోదయ సమయం",
        "numbers": "1, 3, 9"
    },
    1: {  # Taurus (Vrishabha)
        "days": "శుక్రవారం, బుధవారం, శనివారం",
        "planets": "శుక్రుడు, శని, బుధుడు",
        "friendly_rashis": "కన్య, మకరం, తుల",
        "friendly_lagnas": "మకరం, కన్య, కుంభం",
        "life_gem": "వజ్రం (Diamond) / తెల్ల జార్ఖాన్",
        "lucky_gem": "పచ్చ (Emerald)",
        "bhagya_gem": "నీలం (Blue Sapphire)",
        "deity": "శ్రీ మహాలక్ష్మి, శ్రీ వేంకటేశ్వర స్వామి",
        "metal": "వెండి (Silver), ప్లాటినం",
        "color": "తెలుపు, లేత గులాబీ, ఆకుపచ్చ",
        "direction": "దక్షిణం (South)",
        "time": "సూర్యాస్తమయ సమయం",
        "numbers": "5, 6, 8"
    },
    2: {  # Gemini (Mithuna)
        "days": "బుధవారం, శుక్రవారం, శనివారం",
        "planets": "బుధుడు, శుక్రుడు, శని",
        "friendly_rashis": "తుల, కుంభం, కన్య",
        "friendly_lagnas": "తుల, కుంభం, మేషం",
        "life_gem": "పచ్చ (Emerald)",
        "lucky_gem": "వజ్రం (Diamond)",
        "bhagya_gem": "నీలం (Blue Sapphire)",
        "deity": "శ్రీ మహాలక్ష్మి, శ్రీ మహావిష్ణువు",
        "metal": "కంచు (Bronze), వెండి",
        "color": "ఆకుపచ్చ, లేత మీగడ రంగు",
        "direction": "పడమర (West)",
        "time": "సూర్యోదయం తర్వాత 2 గంటలకు",
        "numbers": "5, 7, 9"
    },
    3: {  # Cancer (Karka)
        "days": "సోమవారం, మంగళవారం, గురువారం",
        "planets": "చంద్రుడు, కుజుడు, గురుడు",
        "friendly_rashis": "వృశ్చికం, మీనం, మేషం",
        "friendly_lagnas": "వృశ్చికం, మీనం, ధనుస్సు",
        "life_gem": "ముత్యం (Natural Pearl)",
        "lucky_gem": "పగడం (Red Coral)",
        "bhagya_gem": "పుష్యరాగం (Yellow Sapphire)",
        "deity": "శ్రీ పార్వతీ దేవి, పరమశివుడు",
        "metal": "వెండి, బంగారం",
        "color": "తెలుపు, వెండి రంగు, లేత పసుపు",
        "direction": "ఉత్తరం (North)",
        "time": "రాత్రి వేళ / చంద్రోదయ సమయం",
        "numbers": "2, 3, 9"
    },
    4: {  # Leo (Simha)
        "days": "ఆదివారం, మంగళవారం, గురువారం",
        "planets": "సూర్యుడు, కుజుడు, గురుడు",
        "friendly_rashis": "మేషం, ధనుస్సు, సింహం",
        "friendly_lagnas": "మేషం, ధనుస్సు, కటకం",
        "life_gem": "మాణిక్యం (Ruby)",
        "lucky_gem": "పుష్యరాగం (Yellow Sapphire)",
        "bhagya_gem": "పగడం (Red Coral)",
        "deity": "శ్రీ సూర్య భగవానుడు, గాయత్రీ దేవి",
        "metal": "బంగారం (Gold), రాగి",
        "color": "ఎరుపు, బంగారు పసుపు, కాషాయం",
        "direction": "తూర్పు (East)",
        "time": "మధ్యాహ్న సమయం",
        "numbers": "1, 4, 9"
    },
    5: {  # Virgo (Kanya)
        "days": "బుధవారం, శుక్రవారం, శనివారం",
        "planets": "బుధుడు, శుక్రుడు, శని",
        "friendly_rashis": "మకరం, వృషభం, తుల",
        "friendly_lagnas": "వృషభం, మకరం, మిథునం",
        "life_gem": "పచ్చ (Emerald)",
        "lucky_gem": "వజ్రం (Diamond)",
        "bhagya_gem": "నీలం (Blue Sapphire)",
        "deity": "శ్రీ మహావిష్ణువు, దుర్గాదేవి",
        "metal": "కంచు, వెండి",
        "color": "ముదురు ఆకుపచ్చ, బూడిద రంగు",
        "direction": "దక్షిణం (South)",
        "time": "సాయంకాలం",
        "numbers": "5, 6, 7"
    },
    6: {  # Libra (Tula)
        "days": "శుక్రవారం, శనివారం, బుధవారం",
        "planets": "శుక్రుడు, శని, బుధుడు",
        "friendly_rashis": "కుంభం, మిథునం, వృషభం",
        "friendly_lagnas": "కుంభం, మిథునం, కన్య",
        "life_gem": "వజ్రం (Diamond)",
        "lucky_gem": "నీలం (Blue Sapphire)",
        "bhagya_gem": "పచ్చ (Emerald)",
        "deity": "శ్రీ లక్ష్మీదేవి, సంతోషిమాత",
        "metal": "వెండి, ప్లాటినం",
        "color": "తెలుపు, నీలిరంగు, గులాబీ",
        "direction": "పడమర (West)",
        "time": "ఉదయం 10 నుండి 12 వరకు",
        "numbers": "6, 8, 9"
    },
    7: {  # Scorpio (Vrischika)
        "days": "మంగళవారం, గురువారం, ఆదివారం",
        "planets": "కుజుడు, గురుడు, రవి",
        "friendly_rashis": "మీనం, కర్కాటకం, మేషం",
        "friendly_lagnas": "మీనం, కర్కాటకం, సింహం",
        "life_gem": "పగడం (Red Coral)",
        "lucky_gem": "పుష్యరాగం (Yellow Sapphire)",
        "bhagya_gem": "ముత్యం (Pearl)",
        "deity": "శ్రీ సుబ్రహ్మణ్యేశ్వర స్వామి, నరసింహ స్వామి",
        "metal": "రాగి, బంగారం",
        "color": "ముదురు ఎరుపు, పసుపు",
        "direction": "ఉత్తరం (North)",
        "time": "సూర్యోదయ సమయం",
        "numbers": "3, 7, 9"
    },
    8: {  # Sagittarius (Dhanu)
        "days": "గురువారం, ఆదివారం, మంగళవారం",
        "planets": "గురుడు, రవి, కుజుడు",
        "friendly_rashis": "మేషం, సింహం, మీనం",
        "friendly_lagnas": "మేషం, సింహం, కర్కాటకం",
        "life_gem": "పుష్యరాగం (Yellow Sapphire)",
        "lucky_gem": "పగడం (Red Coral)",
        "bhagya_gem": "మాణిక్యం (Ruby)",
        "deity": "శ్రీ దక్షిణామూర్తి, దత్తాత్రేయ స్వామి",
        "metal": "బంగారం, ఇత్తడి",
        "color": "పసుపు, బంగారు రంగు, కేసరి",
        "direction": "తూర్పు (East)",
        "time": "ఉదయం 8 నుండి 10 వరకు",
        "numbers": "3, 5, 9"
    },
    9: {  # Capricorn (Makara)
        "days": "శనివారం, బుధవారం, శుక్రవారం",
        "planets": "శని, శుక్రుడు, బుధుడు",
        "friendly_rashis": "వృషభం, కన్య, కుంభం",
        "friendly_lagnas": "వృషభం, కన్య, తుల",
        "life_gem": "నీలం (Blue Sapphire)",
        "lucky_gem": "వజ్రం (Diamond)",
        "bhagya_gem": "పచ్చ (Emerald)",
        "deity": "శ్రీ వేంకటేశ్వర స్వామి, శని దేవుడు",
        "metal": "ఇనుము (Iron), సీసం",
        "color": "నీలం, నలుపు, ముదురు బూడిద",
        "direction": "దక్షిణం (South)",
        "time": "సంధ్యా సమయం",
        "numbers": "6, 8, 9"
    },
    10: {  # Aquarius (Kumbha)
        "days": "శనివారం, శుక్రవారం, బుధవారం",
        "planets": "శని, శుక్రుడు, బుధుడు",
        "friendly_rashis": "మిథునం, తుల, మకరం",
        "friendly_lagnas": "మిథునం, తుల, వృషభం",
        "life_gem": "నీలం (Blue Sapphire)",
        "lucky_gem": "పచ్చ (Emerald)",
        "bhagya_gem": "వజ్రం (Diamond)",
        "deity": "శ్రీ రుద్రుడు, ఆంజనేయ స్వామి",
        "metal": "ఇనుము, పంచలోహం",
        "color": "ఆకాశ నీలం, నలుపు",
        "direction": "పడమర (West)",
        "time": "సాయంత్రం",
        "numbers": "3, 7, 8"
    },
    11: {  # Pisces (Meena)
        "days": "గురువారం, మంగళవారం, ఆదివారం",
        "planets": "గురుడు, కుజుడు, చంద్రుడు",
        "friendly_rashis": "కర్కాటకం, వృశ్చికం, ధనుస్సు",
        "friendly_lagnas": "కర్కాటకం, వృశ్చికం, మేషం",
        "life_gem": "పుష్యరాగం (Yellow Sapphire)",
        "lucky_gem": "ముత్యం (Pearl)",
        "bhagya_gem": "పగడం (Red Coral)",
        "deity": "శ్రీ మహావిష్ణువు, బృహస్పతి",
        "metal": "బంగారం",
        "color": "పసుపు, లేత ఎరుపు, గులాబీ",
        "direction": "ఉత్తరం (North)",
        "time": "ఉదయం పూట",
        "numbers": "3, 7, 9"
    }
}

# 3. Rudraksha & Ishta Devata by Nakshatra
NAKSHATRA_RUDRAKSHA = [
    {"mukhi": "9 ముఖి రుద్రాక్ష", "deity": "శ్రీ దుర్గాదేవి / వినాయకుడు", "stotram": "గణేశ పంచరత్నం & దుర్గా కవచం"},      # Ashwini
    {"mukhi": "6 ముఖి రుద్రాక్ష", "deity": "శ్రీ సుబ్రహ్మణ్యేశ్వర స్వామి", "stotram": "సుబ్రహ్మణ్య భుజంగం"},               # Bharani
    {"mukhi": "1 ముఖి లేదా 12 ముఖి రుద్రాక్ష", "deity": "శ్రీ సూర్య భగవానుడు", "stotram": "ఆదిత్య హృదయ స్తోత్రం"},     # Krittika
    {"mukhi": "2 ముఖి రుద్రాక్ష", "deity": "శ్రీ గౌరీ శంకరులు", "stotram": "శివ పంచాక్షరీ స్తోత్రం"},                      # Rohini
    {"mukhi": "3 ముఖి రుద్రాక్ష", "deity": "శ్రీ అగ్ని దేవుడు / కుమారస్వామి", "stotram": "అంగారక స్తోత్రం"},                # Mrigashira
    {"mukhi": "8 ముఖి రుద్రాక్ష", "deity": "శ్రీ భైరవ స్వామి / విఘ్నేశ్వరుడు", "stotram": "కాలభైరవాష్టకం"},               # Ardra
    {"mukhi": "4 ముఖి లేదా 5 ముఖి రుద్రాక్ష", "deity": "శ్రీ బ్రహ్మదేవుడు / బృహస్పతి", "stotram": "గురు స్తోత్రం"},       # Punarvasu
    {"mukhi": "7 ముఖి లేదా 14 ముఖి రుద్రాక్ష", "deity": "శ్రీ మహాలక్ష్మి / శనీశ్వరుడు", "stotram": "కనకధారా స్తోత్రం"},    # Pushya
    {"mukhi": "9 ముఖి రుద్రాక్ష", "deity": "శ్రీ నాగదేవత / దుర్గాదేవి", "stotram": "నాగ స్తోత్రం"},                        # Aslesha
    {"mukhi": "9 ముఖి రుద్రాక్ష", "deity": "శ్రీ గణపతి / సూర్యుడు", "stotram": "సంకటనాశన గణేశ స్తోత్రం"},                 # Magha
    {"mukhi": "6 ముఖి రుద్రాక్ష", "deity": "శ్రీ లక్ష్మీనారాయణ స్వామి", "stotram": "లక్ష్మీనారాయణ హృదయం"},                 # Purva Phalguni
    {"mukhi": "1 ముఖి లేదా 12 ముఖి రుద్రాక్ష", "deity": "శ్రీ సూర్య నారాయణుడు", "stotram": "సూర్యాష్టకం"},               # Uttara Phalguni
    {"mukhi": "2 ముఖి రుద్రాక్ష", "deity": "శ్రీ గౌరీ సమేత శివుడు", "stotram": "చంద్ర కవచం"},                            # Hasta
    {"mukhi": "3 ముఖి రుద్రాక్ష", "deity": "శ్రీ వీరభద్రుడు / కార్తికేయుడు", "stotram": "సుబ్రహ్మణ్యాష్టకం"},             # Chitra
    {"mukhi": "8 ముఖి రుద్రాక్ష", "deity": "శ్రీ దుర్గా భవానీ", "stotram": "మహిషాసుర మర్దినీ స్తోత్రం"},                   # Swati
    {"mukhi": "4 లేదా 5 ముఖి రుద్రాక్ష", "deity": "శ్రీ ఇంద్రాగ్ని / బృహస్పతి", "stotram": "గురు పాదుకా స్తోత్రం"},       # Vishakha
    {"mukhi": "7 ముఖి రుద్రాక్ష", "deity": "శ్రీ రాధాకృష్ణులు / శనీశ్వరుడు", "stotram": "శని వజ్రపంజర స్తోత్రం"},         # Anuradha
    {"mukhi": "9 ముఖి రుద్రాక్ష", "deity": "శ్రీ విష్ణుమూర్తి", "stotram": "విష్ణు సహస్రనామ స్తోత్రం"},                   # Jyeshtha
    {"mukhi": "9 ముఖి లేదా 11 ముఖి రుద్రాక్ష", "deity": "శ్రీ ఆంజనేయ స్వామి", "stotram": "హనుమాన్ చాలీసా"},               # Moola
    {"mukhi": "6 ముఖి రుద్రాక్ష", "deity": "శ్రీ రాజరాజేశ్వరీ దేవి", "stotram": "లలితా సహస్రనామ స్తోత్రం"},              # Purvashadha
    {"mukhi": "12 ముఖి రుద్రాక్ష", "deity": "శ్రీ సూర్య భగవానుడు", "stotram": "ఆదిత్య హృదయం"},                            # Uttarashadha
    {"mukhi": "2 ముఖి రుద్రాక్ష", "deity": "శ్రీ వేంకటేశ్వర స్వామి", "stotram": "శ్రీ వేంకటేశ్వర సుప్రభాతం"},             # Shravana
    {"mukhi": "3 ముఖి రుద్రాక్ష", "deity": "శ్రీ సుబ్రహ్మణ్య స్వామి", "stotram": "స్కంద షష్ఠి కవచం"},                     # Dhanishta
    {"mukhi": "8 ముఖి రుద్రాక్ష", "deity": "శ్రీ మృత్యుంజయ రుద్రుడు", "stotram": "మహా మృత్యుంజయ స్తోత్రం"},               # Shatabhisha
    {"mukhi": "4 లేదా 5 ముఖి రుద్రాక్ష", "deity": "శ్రీ హయగ్రీవ స్వామి", "stotram": "హయగ్రీవ స్తోత్రం"},                   # Purvabhadra
    {"mukhi": "7 ముఖి రుద్రాక్ష", "deity": "శ్రీ లక్ష్మీ నరసింహ స్వామి", "stotram": "నరసింహ కరావలంబ స్తోత్రం"},          # Uttarabhadra
    {"mukhi": "9 ముఖి లేదా 10 ముఖి రుద్రాక్ష", "deity": "శ్రీ కృష్ణ పరమాత్మ", "stotram": "మధురాష్టకం"}                   # Revati
]


def calculate_ghata_chakra(rashi_index: int) -> Dict[str, Any]:
    """Calculate Ghata Chakra details for the native's Moon sign."""
    idx = rashi_index % 12
    spec = GHATA_SPECS.get(idx, GHATA_SPECS[0])
    return {
        "rashi_name_te": RASHIS[idx]["name_te"],
        "masa": spec["masa"],
        "tithi": spec["tithi"],
        "vara": spec["vara"],
        "nakshatra": spec["nakshatra"],
        "yoga": spec["yoga"],
        "karana": spec["karana"],
        "prahar": spec["prahar"],
        "ghata_rashi": spec["rashi"],
        "rashi": spec["rashi"],
        "warning_te": "ఘాత దినం, ఘాత తిథి, మరియు ఘాత నక్షత్రం ఉన్న రోజులలో నూతన కార్యాలు, ప్రయాణాలు, గృహ ప్రవేశం వంటి శుభకార్యాలు నిషిద్ధం."
    }


def calculate_lucky_factors(lagna_info: Dict[str, Any], rashi_index: int) -> Dict[str, Any]:
    """Calculate Lucky factors, deities, gems, metals, and numbers."""
    lagna_idx = lagna_info["rashi_index"]
    spec = LUCKY_BY_LAGNA.get(lagna_idx, LUCKY_BY_LAGNA[0])
    return {
        "lagna_name_te": RASHIS[lagna_idx]["name_te"],
        "rashi_name_te": RASHIS[rashi_index % 12]["name_te"],
        "days": spec["days"],
        "planets": spec["planets"],
        "friendly_rashis": spec["friendly_rashis"],
        "friendly_lagnas": spec["friendly_lagnas"],
        "life_gem": spec["life_gem"],
        "lucky_gem": spec["lucky_gem"],
        "bhagya_gem": spec["bhagya_gem"],
        "deity": spec["deity"],
        "metal": spec["metal"],
        "color": spec["color"],
        "direction": spec["direction"],
        "time": spec["time"],
        "numbers": spec["numbers"],
        "gem_advice_te": "పైన ఇవ్వబడిన రత్నాలు లగ్న, పంచమ, భాగ్యాధిపతుల శాస్త్రోక్త సూచన మాత్రమే. రత్నధారణ విషయంలో అనుభవజ్ఞులైన జ్యోతిష్కుని సలహా తీసుకోవడం శ్రేయస్కరం."
    }


def calculate_jaimini_karakas(planets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Computes 7-Karaka Jaimini Chara Karakas:
    Atma, Amatya, Bhratri, Matri, Putra, Gnyati, Dara.
    Sorted in descending order of degrees modulo 30.
    """
    eligible = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    p_list = [p for p in planets if p["name_en"] in eligible]
    
    # Sort by degree_in_rashi descending
    p_list.sort(key=lambda x: x["degree_in_rashi"], reverse=True)
    
    KARAKA_NAMES = [
        {"code": "AK", "name_te": "ఆత్మ కారకుడు", "name_en": "Atmakaraka", "signifies": "జీవాత్మ, వ్యక్తిత్వం, ఆయుర్దాయం, ఉన్నత స్థితి"},
        {"code": "AmK", "name_te": "అమాత్య కారకుడు", "name_en": "Amatyakaraka", "signifies": "మనస్సు, ఉద్యోగం, వృత్తి, ఆర్థిక స్థితి"},
        {"code": "BK", "name_te": "భ్రాతృ కారకుడు", "name_en": "Bhratrikaraka", "signifies": "తోబుట్టువులు, గురువు, ధైర్య పరాక్రమాలు"},
        {"code": "MK", "name_te": "మాతృ కారకుడు", "name_en": "Matrikaraka", "signifies": "తల్లి, విద్యా సౌఖ్యం, స్థిరాస్తులు"},
        {"code": "PK", "name_te": "పుత్ర కారకుడు", "name_en": "Putrakaraka", "signifies": "సంతానం, మేధస్సు, పూర్వపుణ్యం, సృజనాత్మకత"},
        {"code": "GK", "name_te": "జ్ఞాతి కారకుడు", "name_en": "Gnyatikaraka", "signifies": "బంధువులు, శత్రువులు, రోగాలు, పోటీ తత్వం"},
        {"code": "DK", "name_te": "దార కారకుడు", "name_en": "Darakaraka", "signifies": "భార్య/భర్త, వైవాహిక సౌఖ్యం, వ్యాపార భాగస్వామ్యం"}
    ]
    
    results = []
    for i, p in enumerate(p_list[:7]):
        k_info = KARAKA_NAMES[i]
        results.append({
            "karaka_code": k_info["code"],
            "karaka_name_te": k_info["name_te"],
            "karaka_name_en": k_info["name_en"],
            "signifies": k_info["signifies"],
            "planet_name_te": p["name_te"],
            "planet_name_en": p["name_en"],
            "rashi_name_te": p["rashi_name_te"],
            "degree_formatted": p["formatted_degree"],
            "degree_val": round(p["degree_in_rashi"], 4)
        })
    return results


def calculate_maitri_chakra(planets: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computes Naisargika (Natural), Tatkalika (Temporal),
    and Panchadha (5-fold compound) Friendship Chakra.
    """
    # Classical Natural relationships
    NAISARGIKA = {
        "Sun": {"friends": ["Moon", "Mars", "Jupiter"], "enemies": ["Venus", "Saturn", "Rahu", "Ketu"], "neutrals": ["Mercury"]},
        "Moon": {"friends": ["Sun", "Mercury"], "enemies": ["Rahu", "Ketu"], "neutrals": ["Mars", "Jupiter", "Venus", "Saturn"]},
        "Mars": {"friends": ["Sun", "Moon", "Jupiter", "Ketu"], "enemies": ["Mercury", "Rahu"], "neutrals": ["Venus", "Saturn"]},
        "Mercury": {"friends": ["Sun", "Venus"], "enemies": ["Moon"], "neutrals": ["Mars", "Jupiter", "Saturn", "Rahu", "Ketu"]},
        "Jupiter": {"friends": ["Sun", "Moon", "Mars", "Rahu"], "enemies": ["Mercury", "Venus"], "neutrals": ["Saturn", "Ketu"]},
        "Venus": {"friends": ["Mercury", "Saturn", "Rahu", "Ketu"], "enemies": ["Sun", "Moon"], "neutrals": ["Mars", "Jupiter"]},
        "Saturn": {"friends": ["Mercury", "Venus", "Rahu"], "enemies": ["Sun", "Moon", "Mars", "Ketu"], "neutrals": ["Jupiter"]}
    }

    p_map = {p["name_en"]: p for p in planets if p["name_en"] in NAISARGIKA}
    order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    telugu_names = {
        "Sun": "సూర్యుడు", "Moon": "చంద్రుడు", "Mars": "కుజుడు",
        "Mercury": "బుధుడు", "Jupiter": "గురువు", "Venus": "శుక్రుడు", "Saturn": "శని"
    }

    panchadha_matrix = {}
    for p1 in order:
        panchadha_matrix[p1] = {}
        rashi1 = p_map[p1]["rashi_index"] if p1 in p_map else 0
        for p2 in order:
            if p1 == p2:
                panchadha_matrix[p1][p2] = {"rel": "స్వయం", "score": 0}
                continue
            rashi2 = p_map[p2]["rashi_index"] if p2 in p_map else 0
            # Temporal relationship: houses 2, 3, 4, 10, 11, 12 from each other are Friends (+1), else Enemies (-1)
            dist = ((rashi2 - rashi1) % 12) + 1
            is_tatkalika_friend = dist in [2, 3, 4, 10, 11, 12]

            # Natural relationship (+1, 0, -1)
            nat = NAISARGIKA.get(p1, {})
            if p2 in nat.get("friends", []):
                nat_score = 1
            elif p2 in nat.get("enemies", []):
                nat_score = -1
            else:
                nat_score = 0

            tat_score = 1 if is_tatkalika_friend else -1
            total_score = nat_score + tat_score

            if total_score == 2:
                status = "అధి మిత్రుడు (Great Friend)"
            elif total_score == 1:
                status = "మిత్రుడు (Friend)"
            elif total_score == 0:
                status = "సముడు (Neutral)"
            elif total_score == -1:
                status = "శత్రువు (Enemy)"
            else:
                status = "అధి శత్రువు (Bitter Enemy)"

            panchadha_matrix[p1][p2] = {
                "rel": status,
                "score": total_score,
                "tatkalika": "మిత్రుడు" if is_tatkalika_friend else "శత్రువు"
            }

    planets_te = [telugu_names[p] for p in order]
    panchadha_dict = {}
    for p1 in order:
        t1 = telugu_names[p1]
        panchadha_dict[t1] = {}
        for p2 in order:
            t2 = telugu_names[p2]
            panchadha_dict[t1][t2] = panchadha_matrix[p1][p2]["rel"].split(" ")[0]

    return {
        "order": order,
        "telugu_names": telugu_names,
        "matrix": panchadha_matrix,
        "planets": planets_te,
        "panchadha": panchadha_dict
    }


def calculate_planetary_aspects(planets: List[Dict[str, Any]], lagna_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Computes Drishti (Planetary & Bhava Aspects):
    - All planets aspect 7th house (Full Drishti).
    - Mars aspects 4th, 7th, 8th.
    - Jupiter & Rahu/Ketu aspect 5th, 7th, 9th.
    - Saturn aspects 3rd, 7th, 10th.
    """
    p_aspects = []
    house_aspects = {i + 1: [] for i in range(12)}
    lagna_rashi_idx = lagna_info.get("rashi_index", 0) if lagna_info else 0

    for p in planets:
        p_name = p["name_en"]
        p_bhava = p.get("bhava", ((p["rashi_index"]) % 12) + 1)
        
        aspects_offset = [7]
        if p_name == "Mars":
            aspects_offset = [4, 7, 8]
        elif p_name in ["Jupiter", "Rahu", "Ketu"]:
            aspects_offset = [5, 7, 9]
        elif p_name == "Saturn":
            aspects_offset = [3, 7, 10]

        target_bhavas = []
        for offset in aspects_offset:
            target = ((p_bhava + offset - 2) % 12) + 1
            target_bhavas.append(target)
            house_aspects[target].append(p["name_te"])

        p_aspects.append({
            "planet_name_te": p["name_te"],
            "planet_name_en": p["name_en"],
            "planet_te": p["name_te"],
            "planet_en": p["name_en"],
            "placed_bhava": p_bhava,
            "current_house": p_bhava,
            "current_rashi_te": p.get("rashi_name_te", ""),
            "aspecting_bhavas": target_bhavas,
            "aspected_houses": target_bhavas,
            "aspecting_bhavas_str": ", ".join(f"{b}వ భావం" for b in target_bhavas)
        })

    house_summary = [
        {
            "bhava": h,
            "house": h,
            "sign_te": RASHIS[(lagna_rashi_idx + h - 1) % 12]["name_te"],
            "aspecting_planets": house_aspects[h],
            "aspecting_planets_str": ", ".join(house_aspects[h]) if house_aspects[h] else "ఎవరూ లేరు (శూన్యం)"
        }
        for h in range(1, 13)
    ]

    return {
        "planet_aspects": p_aspects,
        "house_aspects": house_summary
    }


def calculate_vastu_house_facing(rashi_index: int) -> Dict[str, Any]:
    """
    Calculates classical Vastu house entrance recommendation
    based on the native's birth Rashi / Tattva.
    """
    idx = rashi_index % 12
    # 0: Mesha (Fire - East)
    # 1: Vrishabha (Earth - South)
    # 2: Mithuna (Air - West)
    # 3: Karka (Water - North)
    # 4: Simha (Fire - East)
    # 5: Kanya (Earth - South)
    # 6: Tula (Air - West)
    # 7: Vrischika (Water - North)
    # 8: Dhanu (Fire - East)
    # 9: Makara (Earth - South)
    # 10: Kumbha (Air - West)
    # 11: Meena (Water - North)
    
    tattva_map = {
        0: {"tattva": "అగ్ని తత్వం", "facing": "తూర్పు ముఖద్వారం (East Facing)", "secondary": "ఉత్తరం (North)", "avoid": "నైరుతి (South-West)"},
        1: {"tattva": "భూ తత్వం", "facing": "దక్షిణ ముఖద్వారం (South Facing)", "secondary": "పడమర (West)", "avoid": "ఈశాన్యం మూసివేయకూడదు"},
        2: {"tattva": "వాయు తత్వం", "facing": "పశ్చిమ ముఖద్వారం (West Facing)", "secondary": "ఉత్తరం (North)", "avoid": "ఆగ్నేయం"},
        3: {"tattva": "జల తత్వం", "facing": "ఉత్తర ముఖద్వారం (North Facing)", "secondary": "తూర్పు (East)", "avoid": "దక్షిణం"},
        4: {"tattva": "అగ్ని తత్వం", "facing": "తూర్పు ముఖద్వారం (East Facing)", "secondary": "ఉత్తరం (North)", "avoid": "నైరుతి"},
        5: {"tattva": "భూ తత్వం", "facing": "దక్షిణ ముఖద్వారం (South Facing)", "secondary": "పడమర (West)", "avoid": "ఈశాన్యం"},
        6: {"tattva": "వాయు తత్వం", "facing": "పశ్చిమ ముఖద్వారం (West Facing)", "secondary": "తూర్పు (East)", "avoid": "నైరుతి"},
        7: {"tattva": "జల తత్వం", "facing": "ఉత్తర ముఖద్వారం (North Facing)", "secondary": "తూర్పు (East)", "avoid": "దక్షిణం"},
        8: {"tattva": "అగ్ని తత్వం", "facing": "తూర్పు ముఖద్వారం (East Facing)", "secondary": "ఉత్తరం (North)", "avoid": "నైరుతి"},
        9: {"tattva": "భూ తత్వం", "facing": "దక్షిణ లేదా పశ్చిమ ముఖద్వారం", "secondary": "తూర్పు (East)", "avoid": "ఈశాన్యం"},
        10: {"tattva": "వాయు తత్వం", "facing": "పశ్చిమ ముఖద్వారం (West Facing)", "secondary": "ఉత్తరం (North)", "avoid": "దక్షిణం"},
        11: {"tattva": "జల తత్వం", "facing": "ఉత్తర ముఖద్వారం (North Facing)", "secondary": "తూర్పు (East)", "avoid": "నైరుతి"}
    }
    spec = tattva_map[idx]
    return {
        "rashi_name_te": RASHIS[idx]["name_te"],
        "tattva": spec["tattva"],
        "recommended_facing": spec["facing"],
        "secondary_facing": spec["secondary"],
        "avoid_direction": spec["avoid"],
        "vastu_rules_te": [
            "ప్రధాన సింహద్వారం ఎల్లప్పుడూ వెలుతురుతో, శుభ్రంగా మరియు శబ్దం లేకుండా సులువుగా తెరుచుకునేలా ఉండాలి.",
            "ఈశాన్య మూలలో పూజా గది లేదా జల స్థానం, ఆగ్నేయంలో వంటగది, నైరుతిలో యజమాని పడకగది ఉండటం సర్వదా శ్రేయస్కరం.",
            "సింహద్వారానికి ఎదురుగా ఎటువంటి స్తంభాలు, బావులు, లేదా చెట్లు నేరుగా అడ్డం లేకుండా ఉండటం శాస్త్రోక్తం."
        ]
    }


def calculate_gemstones_and_rudraksha(lagna_info: Dict[str, Any], rashi_index: int, nakshatra_index: int) -> Dict[str, Any]:
    """
    Computes Life Gem, Lucky Gem, Fortune Gem, Rudraksha, Ishta Devata,
    along with Shastric Safety Audit (Recommended vs Strictly Prohibited Gems).
    """
    from jyotishyam.services.remedy_verification_service import audit_gemstone_safety

    lucky = calculate_lucky_factors(lagna_info, rashi_index)
    rudra = NAKSHATRA_RUDRAKSHA[nakshatra_index % 27]
    safety_audit = audit_gemstone_safety(lagna_info)

    return {
        "life_gem": lucky["life_gem"],
        "lucky_gem": lucky["lucky_gem"],
        "bhagya_gem": lucky["bhagya_gem"],
        "rudraksha": rudra["mukhi"],
        "ishta_devata": rudra["deity"],
        "stotram": rudra["stotram"],
        "metal": lucky["metal"],
        "color": lucky["color"],
        "deity_mantra_te": f"రోజూ పారాయణకు అనుకూల స్తోత్రం: {rudra['stotram']}. ఇది జన్మ నక్షత్ర దోష నివృత్తికి మరియు సర్వతోముఖాభివృద్ధికి అత్యంత శక్తివంతమైనది.",
        "safety_audit": safety_audit,
        "strictly_prohibited_gems": safety_audit.get("strictly_prohibited_gems", []),
        "recommended_gems_detail": safety_audit.get("recommended_gems", []),
        "shastra_gem_rule": safety_audit.get("shastra_rule", "")
    }

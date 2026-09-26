"""
Global Cities service for birth place lookup with coordinate and timezone resolution.
Includes sacred Indian kshetras, all major and district/taluk level Andhra & Telangana towns,
prominent Indian cities, and global diaspora hubs.
"""

from typing import List, Dict, Optional
import urllib.request
import urllib.parse
import json

# Comprehensive database of cities across Andhra Pradesh, Telangana, India & Global hubs
CITIES_DB = [
    # --- Rayalaseema & Kadapa District (Including Proddatur) ---
    {"name": "Proddatur", "name_te": "ప్రొద్దుటూరు", "state": "Andhra Pradesh", "country": "India", "lat": 14.7504, "lon": 78.5528, "tz": 5.5, "aliases": ["proddaturu", "prodatur", "prodattur", "prodaturu", "proddutur", "ప్రొద్దుటూరు పట్టణం"]},
    {"name": "Kadapa", "name_te": "కడప", "state": "Andhra Pradesh", "country": "India", "lat": 14.4673, "lon": 78.8242, "tz": 5.5, "aliases": ["cuddapah"]},
    {"name": "Pulivendula", "name_te": "పులివెందుల", "state": "Andhra Pradesh", "country": "India", "lat": 14.4230, "lon": 78.2323, "tz": 5.5},
    {"name": "Jammalamadugu", "name_te": "జమ్మలమడుగు", "state": "Andhra Pradesh", "country": "India", "lat": 14.8500, "lon": 78.3833, "tz": 5.5},
    {"name": "Badvel", "name_te": "బద్వేల్", "state": "Andhra Pradesh", "country": "India", "lat": 14.7419, "lon": 79.0578, "tz": 5.5},
    {"name": "Mydukur", "name_te": "మైదుకూరు", "state": "Andhra Pradesh", "country": "India", "lat": 14.7119, "lon": 78.6819, "tz": 5.5},
    {"name": "Rajampet", "name_te": "రాజంపేట", "state": "Andhra Pradesh", "country": "India", "lat": 14.1925, "lon": 79.1578, "tz": 5.5},
    {"name": "Rayachoty", "name_te": "రాయచోటి", "state": "Andhra Pradesh", "country": "India", "lat": 14.0560, "lon": 78.7520, "tz": 5.5},
    {"name": "Kamalapuram", "name_te": "కమలాపురం", "state": "Andhra Pradesh", "country": "India", "lat": 14.5930, "lon": 78.6750, "tz": 5.5},
    {"name": "Vontimitta", "name_te": "ఒంటిమిట్ట", "state": "Andhra Pradesh", "country": "India", "lat": 14.3850, "lon": 79.0300, "tz": 5.5},

    # --- Kurnool & Nandyal District ---
    {"name": "Kurnool", "name_te": "కర్నూలు", "state": "Andhra Pradesh", "country": "India", "lat": 15.8281, "lon": 78.0373, "tz": 5.5},
    {"name": "Nandyal", "name_te": "నంద్యాల", "state": "Andhra Pradesh", "country": "India", "lat": 15.4889, "lon": 78.4836, "tz": 5.5},
    {"name": "Adoni", "name_te": "ఆదోని", "state": "Andhra Pradesh", "country": "India", "lat": 15.6322, "lon": 77.2728, "tz": 5.5},
    {"name": "Yemmiganur", "name_te": "ఎమ్మిగనూరు", "state": "Andhra Pradesh", "country": "India", "lat": 15.7337, "lon": 77.4842, "tz": 5.5},
    {"name": "Dhone", "name_te": "డోన్", "state": "Andhra Pradesh", "country": "India", "lat": 15.4167, "lon": 77.8667, "tz": 5.5},
    {"name": "Allagadda", "name_te": "ఆళ్లగడ్డ", "state": "Andhra Pradesh", "country": "India", "lat": 15.1333, "lon": 78.5167, "tz": 5.5},
    {"name": "Srisailam", "name_te": "శ్రీశైలం", "state": "Andhra Pradesh", "country": "India", "lat": 16.0735, "lon": 78.8682, "tz": 5.5},
    {"name": "Mantralayam", "name_te": "మంత్రాలయం", "state": "Andhra Pradesh", "country": "India", "lat": 15.9400, "lon": 77.4300, "tz": 5.5},
    {"name": "Ahobilam", "name_te": "అహోబిలం", "state": "Andhra Pradesh", "country": "India", "lat": 15.1340, "lon": 78.7180, "tz": 5.5},
    {"name": "Mahanandi", "name_te": "మహానంది", "state": "Andhra Pradesh", "country": "India", "lat": 15.4833, "lon": 78.6167, "tz": 5.5},

    # --- Anantapur & Sri Sathya Sai District ---
    {"name": "Anantapur", "name_te": "అనంతపురం", "state": "Andhra Pradesh", "country": "India", "lat": 14.6819, "lon": 77.6006, "tz": 5.5},
    {"name": "Dharmavaram", "name_te": "ధర్మవరం", "state": "Andhra Pradesh", "country": "India", "lat": 14.4137, "lon": 77.7126, "tz": 5.5},
    {"name": "Hindupur", "name_te": "హిందూపురం", "state": "Andhra Pradesh", "country": "India", "lat": 13.8282, "lon": 77.4925, "tz": 5.5},
    {"name": "Guntakal", "name_te": "గుంతకల్లు", "state": "Andhra Pradesh", "country": "India", "lat": 15.1674, "lon": 77.3756, "tz": 5.5},
    {"name": "Tadipatri", "name_te": "తాడిపత్రి", "state": "Andhra Pradesh", "country": "India", "lat": 14.9100, "lon": 78.0100, "tz": 5.5},
    {"name": "Kadiri", "name_te": "కదిరి", "state": "Andhra Pradesh", "country": "India", "lat": 14.1167, "lon": 78.1667, "tz": 5.5},
    {"name": "Puttaparthi", "name_te": "పుట్టపర్తి", "state": "Andhra Pradesh", "country": "India", "lat": 14.1678, "lon": 77.8114, "tz": 5.5},
    {"name": "Penukonda", "name_te": "పెనుకొండ", "state": "Andhra Pradesh", "country": "India", "lat": 14.0833, "lon": 77.6000, "tz": 5.5},
    {"name": "Lepakshi", "name_te": "లేపాక్షి", "state": "Andhra Pradesh", "country": "India", "lat": 13.8050, "lon": 77.6080, "tz": 5.5},

    # --- Chittoor & Tirupati District ---
    {"name": "Tirupati", "name_te": "తిరుపతి", "state": "Andhra Pradesh", "country": "India", "lat": 13.6288, "lon": 79.4192, "tz": 5.5},
    {"name": "Chittoor", "name_te": "చిత్తూరు", "state": "Andhra Pradesh", "country": "India", "lat": 13.2172, "lon": 79.1003, "tz": 5.5},
    {"name": "Madanapalle", "name_te": "మదనపల్లె", "state": "Andhra Pradesh", "country": "India", "lat": 13.5500, "lon": 78.5000, "tz": 5.5},
    {"name": "Srikalahasti", "name_te": "శ్రీకాళహస్తి", "state": "Andhra Pradesh", "country": "India", "lat": 13.7498, "lon": 79.6984, "tz": 5.5},
    {"name": "Punganur", "name_te": "పుంగనూరు", "state": "Andhra Pradesh", "country": "India", "lat": 13.3667, "lon": 78.5833, "tz": 5.5},
    {"name": "Nagari", "name_te": "నగరి", "state": "Andhra Pradesh", "country": "India", "lat": 13.3300, "lon": 79.5800, "tz": 5.5},
    {"name": "Palamaner", "name_te": "పలమనేరు", "state": "Andhra Pradesh", "country": "India", "lat": 13.2000, "lon": 78.7500, "tz": 5.5},
    {"name": "Kanipakam", "name_te": "కాణిపాకం", "state": "Andhra Pradesh", "country": "India", "lat": 13.2667, "lon": 79.0333, "tz": 5.5},

    # --- Nellore & Prakasam Districts ---
    {"name": "Nellore", "name_te": "నెల్లూరు", "state": "Andhra Pradesh", "country": "India", "lat": 14.4426, "lon": 79.9865, "tz": 5.5},
    {"name": "Gudur", "name_te": "గూడూరు", "state": "Andhra Pradesh", "country": "India", "lat": 14.1463, "lon": 79.8504, "tz": 5.5},
    {"name": "Kavali", "name_te": "కావలి", "state": "Andhra Pradesh", "country": "India", "lat": 14.9132, "lon": 79.9927, "tz": 5.5},
    {"name": "Venkatagiri", "name_te": "వెంకటగిరి", "state": "Andhra Pradesh", "country": "India", "lat": 13.9667, "lon": 79.5833, "tz": 5.5},
    {"name": "Sullurpeta", "name_te": "సూళ్లూరుపేట", "state": "Andhra Pradesh", "country": "India", "lat": 13.7008, "lon": 80.0207, "tz": 5.5},
    {"name": "Ongole", "name_te": "ఒంగోలు", "state": "Andhra Pradesh", "country": "India", "lat": 15.5057, "lon": 80.0499, "tz": 5.5},
    {"name": "Chirala", "name_te": "చీరాల", "state": "Andhra Pradesh", "country": "India", "lat": 15.8246, "lon": 80.3522, "tz": 5.5},
    {"name": "Markapur", "name_te": "మార్కాపురం", "state": "Andhra Pradesh", "country": "India", "lat": 15.7350, "lon": 79.2700, "tz": 5.5},
    {"name": "Kandukur", "name_te": "కందుకూరు", "state": "Andhra Pradesh", "country": "India", "lat": 15.2167, "lon": 79.9000, "tz": 5.5},
    {"name": "Giddalur", "name_te": "గిద్దలూరు", "state": "Andhra Pradesh", "country": "India", "lat": 15.3800, "lon": 78.9300, "tz": 5.5},

    # --- Guntur & Palnadu Districts ---
    {"name": "Guntur", "name_te": "గుంటూరు", "state": "Andhra Pradesh", "country": "India", "lat": 16.3067, "lon": 80.4365, "tz": 5.5},
    {"name": "Tenali", "name_te": "తెనాలి", "state": "Andhra Pradesh", "country": "India", "lat": 16.2437, "lon": 80.6406, "tz": 5.5},
    {"name": "Narasaraopet", "name_te": "నరసరావుపేట", "state": "Andhra Pradesh", "country": "India", "lat": 16.2360, "lon": 80.0520, "tz": 5.5},
    {"name": "Bapatla", "name_te": "బాపట్ల", "state": "Andhra Pradesh", "country": "India", "lat": 15.9042, "lon": 80.4674, "tz": 5.5},
    {"name": "Mangalagiri", "name_te": "మంగళగిరి", "state": "Andhra Pradesh", "country": "India", "lat": 16.4300, "lon": 80.5700, "tz": 5.5},
    {"name": "Amaravati", "name_te": "అమరావతి", "state": "Andhra Pradesh", "country": "India", "lat": 16.5131, "lon": 80.5165, "tz": 5.5},
    {"name": "Sattenapalle", "name_te": "సత్తెనపల్లి", "state": "Andhra Pradesh", "country": "India", "lat": 16.3961, "lon": 80.1472, "tz": 5.5},
    {"name": "Macherla", "name_te": "మాచర్ల", "state": "Andhra Pradesh", "country": "India", "lat": 16.4800, "lon": 79.3000, "tz": 5.5},
    {"name": "Vinukonda", "name_te": "వినుకొండ", "state": "Andhra Pradesh", "country": "India", "lat": 16.0500, "lon": 79.7500, "tz": 5.5},
    {"name": "Chilakaluripet", "name_te": "చిలకలూరిపేట", "state": "Andhra Pradesh", "country": "India", "lat": 16.0892, "lon": 80.1672, "tz": 5.5},
    {"name": "Repalle", "name_te": "రేపల్లె", "state": "Andhra Pradesh", "country": "India", "lat": 16.0200, "lon": 80.8500, "tz": 5.5},

    # --- Krishna & NTR Districts ---
    {"name": "Vijayawada", "name_te": "విజయవాడ", "state": "Andhra Pradesh", "country": "India", "lat": 16.5062, "lon": 80.6480, "tz": 5.5},
    {"name": "Machilipatnam", "name_te": "మచిలీపట్నం", "state": "Andhra Pradesh", "country": "India", "lat": 16.1875, "lon": 81.1389, "tz": 5.5},
    {"name": "Gudivada", "name_te": "గుడివాడ", "state": "Andhra Pradesh", "country": "India", "lat": 16.4410, "lon": 80.9926, "tz": 5.5},
    {"name": "Nuzvid", "name_te": "నూజివీడు", "state": "Andhra Pradesh", "country": "India", "lat": 16.7889, "lon": 80.8464, "tz": 5.5},
    {"name": "Jaggayyapeta", "name_te": "జగ్గయ్యపేట", "state": "Andhra Pradesh", "country": "India", "lat": 16.8928, "lon": 80.0975, "tz": 5.5},
    {"name": "Vuyyuru", "name_te": "వుయ్యూరు", "state": "Andhra Pradesh", "country": "India", "lat": 16.3667, "lon": 80.8500, "tz": 5.5},

    # --- West & East Godavari Districts ---
    {"name": "Rajahmundry", "name_te": "రాజమండ్రి", "state": "Andhra Pradesh", "country": "India", "lat": 17.0005, "lon": 81.8040, "tz": 5.5},
    {"name": "Kakinada", "name_te": "కాకినాడ", "state": "Andhra Pradesh", "country": "India", "lat": 16.9891, "lon": 82.2475, "tz": 5.5},
    {"name": "Eluru", "name_te": "ఏలూరు", "state": "Andhra Pradesh", "country": "India", "lat": 16.7107, "lon": 81.0952, "tz": 5.5},
    {"name": "Bhimavaram", "name_te": "భీమవరం", "state": "Andhra Pradesh", "country": "India", "lat": 16.5449, "lon": 81.5212, "tz": 5.5},
    {"name": "Tadepalligudem", "name_te": "తాడేపల్లిగూడెం", "state": "Andhra Pradesh", "country": "India", "lat": 16.8144, "lon": 81.5267, "tz": 5.5},
    {"name": "Tanuku", "name_te": "తణుకు", "state": "Andhra Pradesh", "country": "India", "lat": 16.7565, "lon": 81.6824, "tz": 5.5},
    {"name": "Palakollu", "name_te": "పాలకొల్లు", "state": "Andhra Pradesh", "country": "India", "lat": 16.5167, "lon": 81.7333, "tz": 5.5},
    {"name": "Narasapuram", "name_te": "నరసాపురం", "state": "Andhra Pradesh", "country": "India", "lat": 16.4333, "lon": 81.6833, "tz": 5.5},
    {"name": "Amalapuram", "name_te": "అమలాపురం", "state": "Andhra Pradesh", "country": "India", "lat": 16.5787, "lon": 82.0061, "tz": 5.5},
    {"name": "Samalkot", "name_te": "సామర్లకోట", "state": "Andhra Pradesh", "country": "India", "lat": 17.0531, "lon": 82.1695, "tz": 5.5},
    {"name": "Annavaram", "name_te": "అన్నవరం", "state": "Andhra Pradesh", "country": "India", "lat": 17.2800, "lon": 82.4000, "tz": 5.5},
    {"name": "Draksharamam", "name_te": "ద్రాక్షారామం", "state": "Andhra Pradesh", "country": "India", "lat": 16.7900, "lon": 82.0600, "tz": 5.5},
    {"name": "Pithapuram", "name_te": "పిఠాపురం", "state": "Andhra Pradesh", "country": "India", "lat": 17.1167, "lon": 82.2667, "tz": 5.5},

    # --- Visakhapatnam, Vizianagaram & Srikakulam ---
    {"name": "Visakhapatnam", "name_te": "విశాఖపట్నం", "state": "Andhra Pradesh", "country": "India", "lat": 17.6868, "lon": 83.2185, "tz": 5.5},
    {"name": "Anakapalle", "name_te": "అనకాపల్లి", "state": "Andhra Pradesh", "country": "India", "lat": 17.6913, "lon": 83.0039, "tz": 5.5},
    {"name": "Vizianagaram", "name_te": "విజయనగరం", "state": "Andhra Pradesh", "country": "India", "lat": 18.1133, "lon": 83.3977, "tz": 5.5},
    {"name": "Srikakulam", "name_te": "శ్రీకాకుళం", "state": "Andhra Pradesh", "country": "India", "lat": 18.2949, "lon": 83.8938, "tz": 5.5},
    {"name": "Bobbili", "name_te": "బొబ్బిలి", "state": "Andhra Pradesh", "country": "India", "lat": 18.5667, "lon": 83.3667, "tz": 5.5},
    {"name": "Parvathipuram", "name_te": "పార్వతీపురం", "state": "Andhra Pradesh", "country": "India", "lat": 18.7833, "lon": 83.4333, "tz": 5.5},
    {"name": "Simhachalam", "name_te": "సింహాచలం", "state": "Andhra Pradesh", "country": "India", "lat": 17.7667, "lon": 83.2500, "tz": 5.5},

    # --- Telangana State Comprehensive ---
    {"name": "Hyderabad", "name_te": "హైదరాబాద్", "state": "Telangana", "country": "India", "lat": 17.3850, "lon": 78.4867, "tz": 5.5},
    {"name": "Secunderabad", "name_te": "సికింద్రాబాద్", "state": "Telangana", "country": "India", "lat": 17.4399, "lon": 78.4983, "tz": 5.5},
    {"name": "Warangal", "name_te": "వరంగల్", "state": "Telangana", "country": "India", "lat": 17.9784, "lon": 79.5941, "tz": 5.5},
    {"name": "Hanamkonda", "name_te": "హన్మకొండ", "state": "Telangana", "country": "India", "lat": 18.0138, "lon": 79.5630, "tz": 5.5},
    {"name": "Karimnagar", "name_te": "కరీంనగర్", "state": "Telangana", "country": "India", "lat": 18.4386, "lon": 79.1288, "tz": 5.5},
    {"name": "Nizamabad", "name_te": "నిజామాబాద్", "state": "Telangana", "country": "India", "lat": 18.6725, "lon": 78.0941, "tz": 5.5},
    {"name": "Khammam", "name_te": "ఖమ్మం", "state": "Telangana", "country": "India", "lat": 17.2473, "lon": 80.1514, "tz": 5.5},
    {"name": "Ramagundam", "name_te": "రామగుండం", "state": "Telangana", "country": "India", "lat": 18.7562, "lon": 79.4746, "tz": 5.5},
    {"name": "Mahabubnagar", "name_te": "మహబూబ్‌నగర్", "state": "Telangana", "country": "India", "lat": 16.7433, "lon": 78.0033, "tz": 5.5},
    {"name": "Nalgonda", "name_te": "నల్గొండ", "state": "Telangana", "country": "India", "lat": 17.0577, "lon": 79.2684, "tz": 5.5},
    {"name": "Suryapet", "name_te": "సూర్యాపేట", "state": "Telangana", "country": "India", "lat": 17.1439, "lon": 79.6239, "tz": 5.5},
    {"name": "Miryalaguda", "name_te": "మిర్యాలగూడ", "state": "Telangana", "country": "India", "lat": 16.8719, "lon": 79.5639, "tz": 5.5},
    {"name": "Adilabad", "name_te": "ఆదిలాబాద్", "state": "Telangana", "country": "India", "lat": 19.6641, "lon": 78.5320, "tz": 5.5},
    {"name": "Mancherial", "name_te": "మంచిర్యాల", "state": "Telangana", "country": "India", "lat": 18.8679, "lon": 79.4639, "tz": 5.5},
    {"name": "Siddipet", "name_te": "సిద్ధిపేట", "state": "Telangana", "country": "India", "lat": 18.1018, "lon": 78.8520, "tz": 5.5},
    {"name": "Medak", "name_te": "మెదక్", "state": "Telangana", "country": "India", "lat": 18.0461, "lon": 78.2612, "tz": 5.5},
    {"name": "Sangareddy", "name_te": "సంగారెడ్డి", "state": "Telangana", "country": "India", "lat": 17.6190, "lon": 78.0815, "tz": 5.5},
    {"name": "Kamareddy", "name_te": "కామారెడ్డి", "state": "Telangana", "country": "India", "lat": 18.3225, "lon": 78.3392, "tz": 5.5},
    {"name": "Jagtial", "name_te": "జగిత్యాల", "state": "Telangana", "country": "India", "lat": 18.7942, "lon": 78.9125, "tz": 5.5},
    {"name": "Sircilla", "name_te": "సిరిసిల్ల", "state": "Telangana", "country": "India", "lat": 18.3844, "lon": 78.8078, "tz": 5.5},
    {"name": "Bhadrachalam", "name_te": "భద్రాచలం", "state": "Telangana", "country": "India", "lat": 17.6688, "lon": 80.8936, "tz": 5.5},
    {"name": "Yadagirigutta", "name_te": "యాదగిరిగుట్ట", "state": "Telangana", "country": "India", "lat": 17.5898, "lon": 78.9388, "tz": 5.5},
    {"name": "Kothagudem", "name_te": "కొత్తగూడెం", "state": "Telangana", "country": "India", "lat": 17.5524, "lon": 80.6175, "tz": 5.5},
    {"name": "Gadwal", "name_te": "గద్వాల", "state": "Telangana", "country": "India", "lat": 16.2300, "lon": 77.8000, "tz": 5.5},
    {"name": "Wanaparthy", "name_te": "వనపర్తి", "state": "Telangana", "country": "India", "lat": 16.3620, "lon": 78.0620, "tz": 5.5},
    {"name": "Vikarabad", "name_te": "వికారాబాద్", "state": "Telangana", "country": "India", "lat": 17.3364, "lon": 77.9048, "tz": 5.5},
    {"name": "Jangaon", "name_te": "జనగాం", "state": "Telangana", "country": "India", "lat": 17.7231, "lon": 79.1606, "tz": 5.5},

    # --- Other Major Indian Metros & Spiritual Hubs ---
    {"name": "Bengaluru", "name_te": "బెంగళూరు", "state": "Karnataka", "country": "India", "lat": 12.9716, "lon": 77.5946, "tz": 5.5},
    {"name": "Mysuru", "name_te": "మైసూరు", "state": "Karnataka", "country": "India", "lat": 12.2958, "lon": 76.6394, "tz": 5.5},
    {"name": "Mangaluru", "name_te": "మంగళూరు", "state": "Karnataka", "country": "India", "lat": 12.9141, "lon": 74.8560, "tz": 5.5},
    {"name": "Chennai", "name_te": "చెన్నై", "state": "Tamil Nadu", "country": "India", "lat": 13.0827, "lon": 80.2707, "tz": 5.5},
    {"name": "Coimbatore", "name_te": "కోయంబత్తూర్", "state": "Tamil Nadu", "country": "India", "lat": 11.0168, "lon": 76.9558, "tz": 5.5},
    {"name": "Madurai", "name_te": "మదురై", "state": "Tamil Nadu", "country": "India", "lat": 9.9252, "lon": 78.1198, "tz": 5.5},
    {"name": "Rameswaram", "name_te": "రామేశ్వరం", "state": "Tamil Nadu", "country": "India", "lat": 9.2876, "lon": 79.3129, "tz": 5.5},
    {"name": "Kanchipuram", "name_te": "కాంచీపురం", "state": "Tamil Nadu", "country": "India", "lat": 12.8342, "lon": 79.7036, "tz": 5.5},
    {"name": "Thiruvananthapuram", "name_te": "తిరువనంతపురం", "state": "Kerala", "country": "India", "lat": 8.5241, "lon": 76.9366, "tz": 5.5},
    {"name": "Kochi", "name_te": "కొచ్చి", "state": "Kerala", "country": "India", "lat": 9.9312, "lon": 76.2673, "tz": 5.5},
    {"name": "Guruvayur", "name_te": "గురువాయూర్", "state": "Kerala", "country": "India", "lat": 10.5946, "lon": 76.0418, "tz": 5.5},
    {"name": "Mumbai", "name_te": "ముంబై", "state": "Maharashtra", "country": "India", "lat": 19.0760, "lon": 72.8777, "tz": 5.5},
    {"name": "Pune", "name_te": "పుణె", "state": "Maharashtra", "country": "India", "lat": 18.5204, "lon": 73.8567, "tz": 5.5},
    {"name": "Nagpur", "name_te": "నాగ్‌పూర్", "state": "Maharashtra", "country": "India", "lat": 21.1458, "lon": 79.0882, "tz": 5.5},
    {"name": "Shirdi", "name_te": "షిర్డీ", "state": "Maharashtra", "country": "India", "lat": 19.7667, "lon": 74.4767, "tz": 5.5},
    {"name": "Delhi", "name_te": "ఢిల్లీ", "state": "Delhi", "country": "India", "lat": 28.6139, "lon": 77.2090, "tz": 5.5},
    {"name": "Kolkata", "name_te": "కోల్‌కతా", "state": "West Bengal", "country": "India", "lat": 22.5726, "lon": 88.3639, "tz": 5.5},
    {"name": "Varanasi (Kashi)", "name_te": "కాశీ / వారణాసి", "state": "Uttar Pradesh", "country": "India", "lat": 25.3176, "lon": 82.9739, "tz": 5.5},
    {"name": "Ayodhya", "name_te": "అయోధ్య", "state": "Uttar Pradesh", "country": "India", "lat": 26.7922, "lon": 82.1998, "tz": 5.5},
    {"name": "Prayagraj", "name_te": "ప్రయాగ్‌రాజ్", "state": "Uttar Pradesh", "country": "India", "lat": 25.4358, "lon": 81.8463, "tz": 5.5},
    {"name": "Mathura", "name_te": "మథుర", "state": "Uttar Pradesh", "country": "India", "lat": 27.4924, "lon": 77.6737, "tz": 5.5},
    {"name": "Haridwar", "name_te": "హరిద్వార్", "state": "Uttarakhand", "country": "India", "lat": 29.9457, "lon": 78.1642, "tz": 5.5},
    {"name": "Rishikesh", "name_te": "ఋషికేశ్", "state": "Uttarakhand", "country": "India", "lat": 30.0869, "lon": 78.2676, "tz": 5.5},
    {"name": "Ujjain", "name_te": "ఉజ్జయిని", "state": "Madhya Pradesh", "country": "India", "lat": 23.1765, "lon": 75.7885, "tz": 5.5},
    {"name": "Puri", "name_te": "పూరీ జగన్నాథ క్షేత్రం", "state": "Odisha", "country": "India", "lat": 19.8135, "lon": 85.8312, "tz": 5.5},
    {"name": "Ahmedabad", "name_te": "అహ్మదాబాద్", "state": "Gujarat", "country": "India", "lat": 23.0225, "lon": 72.5714, "tz": 5.5},
    {"name": "Dwarka", "name_te": "ద్వారక", "state": "Gujarat", "country": "India", "lat": 22.2394, "lon": 68.9678, "tz": 5.5},
    {"name": "Jaipur", "name_te": "జైపూర్", "state": "Rajasthan", "country": "India", "lat": 26.9124, "lon": 75.7873, "tz": 5.5},

    # --- International Diaspora & Global Metros ---
    {"name": "Dallas / Frisco", "state": "Texas", "country": "USA", "lat": 33.1507, "lon": -96.8236, "tz": -6.0},
    {"name": "McKinney", "state": "Texas", "country": "USA", "lat": 33.1976, "lon": -96.6178, "tz": -6.0},
    {"name": "Plano", "state": "Texas", "country": "USA", "lat": 33.0198, "lon": -96.6989, "tz": -6.0},
    {"name": "Irving", "state": "Texas", "country": "USA", "lat": 32.8140, "lon": -96.9489, "tz": -6.0},
    {"name": "New York", "state": "New York", "country": "USA", "lat": 40.7128, "lon": -74.0060, "tz": -5.0},
    {"name": "Jersey City / Edison", "state": "New Jersey", "country": "USA", "lat": 40.5187, "lon": -74.4121, "tz": -5.0},
    {"name": "San Jose (Silicon Valley)", "state": "California", "country": "USA", "lat": 37.3382, "lon": -121.8863, "tz": -8.0},
    {"name": "San Francisco", "state": "California", "country": "USA", "lat": 37.7749, "lon": -122.4194, "tz": -8.0},
    {"name": "Los Angeles", "state": "California", "country": "USA", "lat": 34.0522, "lon": -118.2437, "tz": -8.0},
    {"name": "Seattle", "state": "Washington", "country": "USA", "lat": 47.6062, "lon": -122.3321, "tz": -8.0},
    {"name": "Chicago", "state": "Illinois", "country": "USA", "lat": 41.8781, "lon": -87.6298, "tz": -6.0},
    {"name": "Houston", "state": "Texas", "country": "USA", "lat": 29.7604, "lon": -95.3698, "tz": -6.0},
    {"name": "Austin", "state": "Texas", "country": "USA", "lat": 30.2672, "lon": -97.7431, "tz": -6.0},
    {"name": "Atlanta", "state": "Georgia", "country": "USA", "lat": 33.7490, "lon": -84.3880, "tz": -5.0},
    {"name": "Boston", "state": "Massachusetts", "country": "USA", "lat": 42.3601, "lon": -71.0589, "tz": -5.0},
    {"name": "Washington DC", "state": "District of Columbia", "country": "USA", "lat": 38.9072, "lon": -77.0369, "tz": -5.0},
    {"name": "Toronto", "state": "Ontario", "country": "Canada", "lat": 43.6532, "lon": -79.3832, "tz": -5.0},
    {"name": "Vancouver", "state": "British Columbia", "country": "Canada", "lat": 49.2827, "lon": -123.1207, "tz": -8.0},
    {"name": "London", "state": "England", "country": "UK", "lat": 51.5074, "lon": -0.1278, "tz": 0.0},
    {"name": "Dublin", "state": "Leinster", "country": "Ireland", "lat": 53.3498, "lon": -6.2603, "tz": 0.0},
    {"name": "Berlin", "state": "Berlin", "country": "Germany", "lat": 52.5200, "lon": 13.4050, "tz": 1.0},
    {"name": "Frankfurt", "state": "Hesse", "country": "Germany", "lat": 50.1109, "lon": 8.6821, "tz": 1.0},
    {"name": "Paris", "state": "Ile-de-France", "country": "France", "lat": 48.8566, "lon": 2.3522, "tz": 1.0},
    {"name": "Amsterdam", "state": "North Holland", "country": "Netherlands", "lat": 52.3676, "lon": 4.9041, "tz": 1.0},
    {"name": "Zurich", "state": "Zurich", "country": "Switzerland", "lat": 47.3769, "lon": 8.5417, "tz": 1.0},
    {"name": "Dubai", "state": "Dubai", "country": "UAE", "lat": 25.2048, "lon": 55.2708, "tz": 4.0},
    {"name": "Abu Dhabi", "state": "Abu Dhabi", "country": "UAE", "lat": 24.4539, "lon": 54.3773, "tz": 4.0},
    {"name": "Doha", "state": "Ad Dawhah", "country": "Qatar", "lat": 25.2854, "lon": 51.5310, "tz": 3.0},
    {"name": "Riyadh", "state": "Riyadh", "country": "Saudi Arabia", "lat": 24.7136, "lon": 46.6753, "tz": 3.0},
    {"name": "Singapore", "state": "Singapore", "country": "Singapore", "lat": 1.3521, "lon": 103.8198, "tz": 8.0},
    {"name": "Kuala Lumpur", "state": "Federal Territory", "country": "Malaysia", "lat": 3.1390, "lon": 101.6869, "tz": 8.0},
    {"name": "Tokyo", "state": "Tokyo", "country": "Japan", "lat": 35.6762, "lon": 139.6503, "tz": 9.0},
    {"name": "Sydney", "state": "NSW", "country": "Australia", "lat": -33.8688, "lon": 151.2093, "tz": 10.0},
    {"name": "Melbourne", "state": "Victoria", "country": "Australia", "lat": -37.8136, "lon": 144.9631, "tz": 10.0},
    {"name": "Brisbane", "state": "Queensland", "country": "Australia", "lat": -27.4698, "lon": 153.0251, "tz": 10.0},
    {"name": "Auckland", "state": "Auckland", "country": "New Zealand", "lat": -36.8485, "lon": 174.7633, "tz": 12.0},
]


def geocode_online(query: str, limit: int = 5) -> List[Dict]:
    """
    Fallback geocoder querying OpenStreetMap Nominatim with strict timeout.
    Enables automatic coordinate resolution for any village or town in the world.
    """
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(query)}&format=json&limit={limit}&addressdetails=1"
        req = urllib.request.Request(url, headers={"User-Agent": "JyotishyamPanchangamApp/2.0"})
        with urllib.request.urlopen(req, timeout=2.5) as resp:
            data = json.loads(resp.read().decode())
            results = []
            for item in data:
                addr = item.get("address", {})
                city_name = addr.get("city") or addr.get("town") or addr.get("village") or addr.get("municipality") or item.get("name") or query.title()
                state = addr.get("state", "")
                country = addr.get("country", "")
                lat = round(float(item["lat"]), 4)
                lon = round(float(item["lon"]), 4)
                
                # Default timezone determination
                tz = 5.5
                if country.lower() != "india":
                    # Approximate longitude to standard timezone offset
                    tz = round((lon / 15.0) * 2) / 2.0

                results.append({
                    "name": city_name,
                    "state": state,
                    "country": country,
                    "lat": lat,
                    "lon": lon,
                    "tz": tz
                })
            return results
    except Exception:
        return []


def search_cities(query: str, limit: int = 15) -> List[Dict]:
    """
    Search cities matching query prefix, substring, or alias.
    Supports Telugu script queries, English queries, compound strings (e.g. 'Proddatur, Andhra Pradesh'),
    and auto online geocoding.
    """
    q = query.strip().lower()
    if not q:
        return CITIES_DB[:limit]

    # Primary token (handles "Proddatur, Andhra Pradesh" -> "proddatur")
    q_primary = q.split(",")[0].split("(")[0].strip()

    exact_matches = []
    prefix_matches = []
    sub_matches = []
    seen = set()

    for c in CITIES_DB:
        c_name = c["name"].lower()
        c_state = c.get("state", "").lower()
        c_country = c.get("country", "").lower()
        c_te = c.get("name_te", "").lower()
        aliases = [a.lower() for a in c.get("aliases", [])]
        compound = f"{c_name}, {c_state}, {c_country}"

        key = (c["name"], c.get("state", ""), c["lat"], c["lon"])
        if key in seen:
            continue

        # 1. Exact match (name, telugu, or alias)
        if c_name == q or c_name == q_primary or c_te == q or c_te == q_primary or q in aliases or q_primary in aliases:
            exact_matches.append(c)
            seen.add(key)
        # 2. Prefix match
        elif (c_name.startswith(q) or c_name.startswith(q_primary) or
              (c_te and (c_te.startswith(q) or c_te.startswith(q_primary))) or
              any(a.startswith(q) or a.startswith(q_primary) for a in aliases)):
            prefix_matches.append(c)
            seen.add(key)
        # 3. Substring match
        elif (q in c_name or q_primary in c_name or
              (c_te and (q in c_te or q_primary in c_te)) or
              q in compound or q_primary in compound or
              q in c_state or q in c_country or
              any(q in a for a in aliases)):
            sub_matches.append(c)
            seen.add(key)

    matches = (exact_matches + prefix_matches + sub_matches)[:limit]

    # If no local match was found and query is at least 3 characters, try online fallback
    if len(matches) == 0 and len(q) >= 3:
        online_results = geocode_online(query, limit=5)
        for r in online_results:
            key = (r["name"], r.get("state", ""), r["lat"], r["lon"])
            if key not in seen:
                matches.append(r)
                seen.add(key)
                # Cache dynamically into local database
                CITIES_DB.append(r)

    return matches[:limit]


def get_city_details(city_name: str) -> Optional[Dict]:
    """Get exact or best city match for a place name or compound location string."""
    if not city_name or not city_name.strip():
        return None
    c_lower = city_name.strip().lower()
    c_primary = c_lower.split(",")[0].split("(")[0].strip()

    # 1. Try exact or alias match first
    for c in CITIES_DB:
        c_name = c["name"].lower()
        c_te = c.get("name_te", "").strip().lower()
        aliases = [a.lower() for a in c.get("aliases", [])]
        if c_name == c_lower or c_name == c_primary or c_te == c_lower or c_te == c_primary:
            return c
        if c_lower in aliases or c_primary in aliases:
            return c

    # 2. Fallback to smart search
    res = search_cities(city_name, limit=1)
    return res[0] if res else None


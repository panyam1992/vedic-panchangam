"""
Birth Panchangam calculations: Tithi, Vara, Nakshatra, Yoga, Karana, Gana, Nadi, Yoni, Varna.
"""

from datetime import datetime
from typing import Dict, Any

TITHI_NAMES = [
    "పాడ్యమి (Prathama)", "విదియ (Dvitiya)", "తదియ (Tritiya)", "చవితి (Chaturthi)", "పంచమి (Panchami)",
    "షష్ఠి (Shashti)", "సప్తమి (Saptami)", "అష్టమి (Ashtami)", "నవమి (Navami)", "దశమి (Dashami)",
    "ఏకాదశి (Ekadashi)", "ద్వాదశి (Dvadashi)", "త్రయోదశి (Trayodashi)", "చతుర్దశి (Chaturdashi)", "పూర్ణిమ (Purnima)",
    "పాడ్యమి (Prathama)", "విదియ (Dvitiya)", "తదియ (Tritiya)", "చవితి (Chaturthi)", "పంచమి (Panchami)",
    "షష్ఠి (Shashti)", "సప్తమి (Saptami)", "అష్టమి (Ashtami)", "నవమి (Navami)", "దశమి (Dashami)",
    "ఏకాదశి (Ekadashi)", "ద్వాదశి (Dvadashi)", "త్రయోదశి (Trayodashi)", "చతుర్దశి (Chaturdashi)", "అమావాస్య (Amavasya)"
]

VARA_NAMES = [
    {"en": "Sunday", "te": "ఆదివారం", "lord": "సూర్యుడు"},
    {"en": "Monday", "te": "సోమవారం", "lord": "చంద్రుడు"},
    {"en": "Tuesday", "te": "మంగళవారం", "lord": "కుజుడు"},
    {"en": "Wednesday", "te": "బుధవారం", "lord": "బుధుడు"},
    {"en": "Thursday", "te": "గురువారం", "lord": "గురుడు"},
    {"en": "Friday", "te": "శుక్రవారం", "lord": "శుక్రుడు"},
    {"en": "Saturday", "te": "శనివారం", "lord": "శని"},
]

YOGA_NAMES = [
    "విష్కంభం (Vishkambha)", "ప్రీతి (Priti)", "ఆయుష్మాన్ (Ayushman)", "సౌభాగ్యం (Saubhagya)", "శోభనం (Shobhana)",
    "అతిగండం (Atiganda)", "సుకుర్మ (Sukarma)", "ధృతి (Dhriti)", "శూలం (Shula)", "గండం (Ganda)",
    "వృద్ధి (Vriddhi)", "ధ్రువం (Dhruva)", "వ్యాఘాతం (Vyaghata)", "హర్షణం (Harshana)", "వజ్రం (Vajra)",
    "సిద్ధి (Siddhi)", "వ్యతీపాతం (Vyatipata)", "వరియాన్ (Variyan)", "పరిఘం (Parigha)", "శివం (Shiva)",
    "సిద్ధం (Siddha)", "సాధ్యం (Sadhya)", "శుభం (Shubha)", "శుభ్రం (Shukla)", "బ్రహ్మం (Brahma)",
    "ఐంద్రం (Indra)", "వైధృతి (Vaidhriti)"
]

KARANA_MOVING = ["బవ (Bava)", "బాలవ (Balava)", "కౌలవ (Kaulava)", "తైతిల (Taitila)", "గరిజ (Garija)", "వణిజ (Vanija)", "విష్టి / భద్ర (Vishti/Bhadra)"]
KARANA_FIXED = ["శకుని (Shakuni)", "చతుష్పాద (Chatushpada)", "నాగవ (Naga)", "కింస్తుఘ్న (Kimstughna)"]

YONI_MAP = [
    "అశ్వం (Horse)", "గజం (Elephant)", "మేషం (Sheep)", "సర్పం (Serpent)", "సర్పం (Serpent)",
    "శ్వానం (Dog)", "మార్జాలం (Cat)", "మేషం (Sheep)", "మార్జాలం (Cat)", "మూషికం (Rat)",
    "మూషికం (Rat)", "గోవు (Cow)", "మహిషం (Buffalo)", "వ్యాఘ్రం (Tiger)", "మహిషం (Buffalo)",
    "వ్యాఘ్రం (Tiger)", "మృగం (Deer)", "మృగం (Deer)", "శ్వానం (Dog)", "వానరం (Monkey)",
    "నఖులం (Mongoose)", "వానరం (Monkey)", "సింహం (Lion)", "అశ్వం (Horse)", "సింహం (Lion)",
    "గోవు (Cow)", "గజం (Elephant)"
]


def calculate_birth_panchangam(
    sun_lon: float,
    moon_lon: float,
    dob_str: str,
    lagna_info: Dict[str, Any]
) -> Dict[str, Any]:
    """Calculate complete Vedic Panchangam at time of birth."""
    # 1. Tithi
    diff = (moon_lon - sun_lon) % 360.0
    tithi_index = int(diff / 12.0)
    paksha = "శుక్ల పక్షం (Shukla Paksha)" if tithi_index < 15 else "కృష్ణ పక్షం (Krishna Paksha)"
    tithi_name = TITHI_NAMES[tithi_index]

    # 2. Vara (Day of week from DOB)
    dt = datetime.strptime(dob_str, "%Y-%m-%d")
    # weekday(): Monday is 0, Sunday is 6
    # Vedic: Sunday=0, Monday=1, ..., Saturday=6
    weekday_vedic = (dt.weekday() + 1) % 7
    vara = VARA_NAMES[weekday_vedic]

    # 3. Nakshatra from Moon
    from jyotishyam.services.kundali_calculator import get_nakshatra_and_pada
    moon_nak, pada = get_nakshatra_and_pada(moon_lon)

    # 4. Yoga = (Sun + Moon) % 360 / (13° 20')
    yoga_sum = (sun_lon + moon_lon) % 360.0
    yoga_index = int(yoga_sum / (360.0 / 27.0)) % 27
    yoga_name = YOGA_NAMES[yoga_index]

    # 5. Karana = Tithi half (6 degrees)
    karana_num = int(diff / 6.0)
    if karana_num == 0:
        karana_name = KARANA_FIXED[3]  # Kimstughna
    elif karana_num >= 57:
        karana_name = KARANA_FIXED[karana_num - 57]
    else:
        karana_name = KARANA_MOVING[(karana_num - 1) % 7]

    # 6. Gana, Nadi, Yoni, Varna
    gana = moon_nak["gana"]
    gana_te = "దేవ గణం" if gana == "Deva" else ("మానుష గణం" if gana == "Manushya" else "రాక్షస గణం")

    nadi = moon_nak["nadi"]
    nadi_te = "ఆది నాడి" if nadi == "Aadi" else ("మధ్య నాడి" if nadi == "Madhya" else "అంత్య నాడి")

    yoni_te = YONI_MAP[moon_nak["index"]]

# 27 Nakshatras Name Syllables (నామ నక్షత్రాక్షరాలు: 4 padas each)
NAKSHATRA_SYLLABLES = [
    ["చూ", "చే", "చో", "లా"],        # 1. Ashwini
    ["లీ", "లూ", "లే", "లో"],        # 2. Bharani
    ["ఆ", "ఈ", "ఊ", "ఏ"],          # 3. Krittika
    ["ఓ", "వా", "వీ", "వూ"],        # 4. Rohini
    ["వే", "వో", "కా", "కీ"],        # 5. Mrigashira
    ["కూ", "ఘ", "ఙ", "ఛ"],          # 6. Arudra
    ["కే", "కో", "హా", "హీ"],        # 7. Punarvasu
    ["హూ", "హే", "హో", "డా"],        # 8. Pushyami
    ["డీ", "డూ", "డే", "డో"],        # 9. Ashlesha
    ["మా", "మీ", "మూ", "మే"],        # 10. Magha
    ["మో", "టా", "టీ", "టూ"],        # 11. Purva Phalguni
    ["టే", "టో", "పా", "పీ"],        # 12. Uttara Phalguni
    ["పూ", "ష", "ణ", "ఠ"],          # 13. Hasta
    ["పే", "పో", "రా", "రీ"],        # 14. Chitra
    ["రూ", "రే", "రో", "తా"],        # 15. Swati
    ["తీ", "తూ", "తే", "తో"],        # 16. Vishakha
    ["నా", "నీ", "నూ", "నే"],        # 17. Anuradha
    ["నో", "యా", "యీ", "యూ"],        # 18. Jyeshtha
    ["యే", "యో", "భా", "భీ"],        # 19. Moola
    ["భూ", "ధా", "భా", "ఢా"],        # 20. Purva Ashadha
    ["భే", "భో", "జా", "జీ"],        # 21. Uttara Ashadha
    ["ఖీ", "ఖూ", "ఖే", "ఖో"],        # 22. Shravana
    ["గా", "గీ", "గూ", "గే"],        # 23. Dhanishta
    ["గో", "సా", "సీ", "సూ"],        # 24. Shatabhisha
    ["సే", "సో", "దా", "దీ"],        # 25. Purva Bhadra
    ["దూ", "శ్యా", "ఝ", "థా"],       # 26. Uttara Bhadra
    ["దే", "దో", "చా", "చీ"]         # 27. Revati
]

# Nakshatra Vruksham (వృక్షం)
NAKSHATRA_VRUKSHA = [
    "జీవి చెట్టు (Poison Nut)", "ఉసిరి (Amla)", "మేడి (Cluster Fig)", "నేరేడు (Jamun)", "చండ్ర (Khadira)",
    "రేగు (Carissa)", "వెదురు (Bamboo)", "రావి (Peepal)", "నాగకేసరి (Ironwood)", "మర్రి (Banyan)",
    "మోదుగ (Flame of Forest)", "జువ్వి (Ficus)", "కుంకుడు (Soapnut)", "బిల్వ / మారేడు (Bael)", "మద్ది (Arjuna)",
    "వెలగ (Wood Apple)", "పొగడ (Bakul)", "విష్ణుక్రాంత (Pine)", "మద్ది (Sal)", "అశోక (Ashoka)",
    "పనస (Jackfruit)", "జెల్లెడు (Calotropis)", "జమ్మి (Shami)", "కదంబ (Kadamba)", "మామిడి (Mango)",
    "వేప (Neem)", "ఇప్ప (Mahua)"
]

# Nakshatra Birds (పక్షి)
NAKSHATRA_PAKSHI = [
    "పులుగు (Wild Hawk)", "కాకి (Crow)", "నెమలి (Peacock)", "కోయిల (Cuckoo)", "కోడి (Rooster)",
    "పింగళ (Owl)", "హంస (Swan)", "కాకి (Crow)", "నెమలి (Peacock)", "గద్ద (Eagle)",
    "గోరువంక (Myna)", "కాకి (Crow)", "రాబందు (Vulture)", "పిచ్చుక (Sparrow)", "హంస (Swan)",
    "నెమలి (Peacock)", "జిట్ట (Nightingale)", "చకోరం (Chakora)", "గ్రద్ద (Kite)", "గోరువంక (Myna)",
    "కొంగ (Stork)", "కౌజు (Partridge)", "నెమలి (Peacock)", "గుడ్లగూబ (Owl)", "హంస (Swan)",
    "కాకి (Crow)", "నెమలి (Peacock)"
]

# Vashya by Moon Rashi (వశ్యం)
VASHYA_MAP = {
    0: "చతుష్పాద వశ్యం (Quadruped)",     # Aries
    1: "చతుష్పాద వశ్యం (Quadruped)",     # Taurus
    2: "ద్విపాద / నర వశ్యం (Human)",      # Gemini
    3: "జలచర వశ్యం (Water Creature)",   # Cancer
    4: "వనచర / సింహ వశ్యం (Wild)",       # Leo
    5: "ద్విపాద / నర వశ్యం (Human)",      # Virgo
    6: "ద్విపాద / నర వశ్యం (Human)",      # Libra
    7: "కీటక వశ్యం (Insect)",            # Scorpio
    8: "ద్విపాద / చతుష్పాద వశ్యం",        # Sagittarius
    9: "జలచర / చతుష్పాద వశ్యం",          # Capricorn
    10: "ద్విపాద / నర వశ్యం (Human)",     # Aquarius
    11: "జలచర వశ్యం (Water Creature)"   # Pisces
}

# Tatwa by Moon Rashi (పంచభూత తత్త్వం)
TATWA_MAP = {
    0: "అగ్ని తత్త్వం (Fire)", 4: "అగ్ని తత్త్వం (Fire)", 8: "అగ్ని తత్త్వం (Fire)",
    1: "భూ తత్త్వం (Earth)", 5: "భూ తత్త్వం (Earth)", 9: "భూ తత్త్వం (Earth)",
    2: "వాయు తత్త్వం (Air)", 6: "వాయు తత్త్వం (Air)", 10: "వాయు తత్త్వం (Air)",
    3: "జల తత్త్వం (Water)", 7: "జల తత్త్వం (Water)", 11: "జల తత్త్వం (Water)"
}


def calculate_birth_panchangam(
    sun_lon: float,
    moon_lon: float,
    dob_str: str,
    lagna_info: Dict[str, Any]
) -> Dict[str, Any]:
    """Calculate complete Vedic Panchangam & Avakahada Chakra at time of birth."""
    # 1. Tithi
    diff = (moon_lon - sun_lon) % 360.0
    tithi_index = int(diff / 12.0)
    paksha = "శుక్ల పక్షం (Shukla Paksha)" if tithi_index < 15 else "కృష్ణ పక్షం (Krishna Paksha)"
    tithi_name = TITHI_NAMES[tithi_index]

    # 2. Vara (Day of week from DOB)
    dt = datetime.strptime(dob_str, "%Y-%m-%d")
    weekday_vedic = (dt.weekday() + 1) % 7
    vara = VARA_NAMES[weekday_vedic]

    # 3. Nakshatra from Moon
    from jyotishyam.services.kundali_calculator import get_nakshatra_and_pada, RASHIS
    moon_nak, pada = get_nakshatra_and_pada(moon_lon)
    nak_idx = moon_nak["index"]

    # 4. Yoga = (Sun + Moon) % 360 / (13° 20')
    yoga_sum = (sun_lon + moon_lon) % 360.0
    yoga_index = int(yoga_sum / (360.0 / 27.0)) % 27
    yoga_name = YOGA_NAMES[yoga_index]

    # 5. Karana = Tithi half (6 degrees)
    karana_num = int(diff / 6.0)
    if karana_num == 0:
        karana_name = KARANA_FIXED[3]  # Kimstughna
    elif karana_num >= 57:
        karana_name = KARANA_FIXED[karana_num - 57]
    else:
        karana_name = KARANA_MOVING[(karana_num - 1) % 7]

    # 6. Gana, Nadi, Yoni, Varna
    gana = moon_nak["gana"]
    gana_te = "దేవ గణం" if gana == "Deva" else ("మానుష గణం" if gana == "Manushya" else "రాక్షస గణం")

    nadi = moon_nak["nadi"]
    nadi_te = "ఆది నాడి" if nadi == "Aadi" else ("మధ్య నాడి" if nadi == "Madhya" else "అంత్య నాడి")

    yoni_te = YONI_MAP[nak_idx]

    moon_rashi_idx = int(moon_lon // 30)
    varna_map = {
        0: "క్షత్రియ వర్ణం", 4: "క్షత్రియ వర్ణం", 8: "క్షత్రియ వర్ణం",
        1: "వైశ్య వర్ణం", 5: "వైశ్య వర్ణం", 9: "వైశ్య వర్ణం",
        2: "శూద్ర వర్ణం", 6: "శూద్ర వర్ణం", 10: "శూద్ర వర్ణం",
        3: "బ్రాహ్మణ వర్ణం", 7: "బ్రాహ్మణ వర్ణం", 11: "బ్రాహ్మణ వర్ణం",
    }
    varna_te = varna_map.get(moon_rashi_idx, "వైశ్య వర్ణం")

    # 7. Vashya & Tatwa
    vashya_te = VASHYA_MAP.get(moon_rashi_idx, "చతుష్పాద వశ్యం")
    tatwa_te = TATWA_MAP.get(moon_rashi_idx, "భూ తత్త్వం")

    # 8. Paya (పాద చక్రం: based on Moon's house from Lagna)
    lagna_idx = lagna_info.get("rashi_index", 0)
    moon_house = ((moon_rashi_idx - lagna_idx) % 12) + 1

    if moon_house in [2, 5, 9]:
        paya_name = "రజత పాయ (Silver Foot)"
        paya_desc = "అత్యంత శుభప్రదం - సంపద, యశస్సు, సౌభాగ్య వృద్ధి"
    elif moon_house in [3, 7, 10]:
        paya_name = "తామ్ర పాయ (Copper Foot)"
        paya_desc = "శుభప్రదం - స్థిరమైన అభివృద్ధి, కార్యసిద్ధి"
    elif moon_house in [1, 6, 11]:
        paya_name = "స్వర్ణ పాయ (Gold Foot)"
        paya_desc = "మిశ్రమ ఫలితాలు - ప్రారంభంలో శ్రమ, తదుపరి అధిక లాభాలు"
    else:  # 4, 8, 12
        paya_name = "లోహ / ఇనుము పాయ (Iron Foot)"
        paya_desc = "సామాన్యం - తీవ్ర శ్రమ, ఓర్పుతో లక్ష్యాల సాధన"

    # 9. Naming Syllables (నామ నక్షత్రాక్షరాలు)
    pada_int = int(pada)
    pada_idx = max(0, min(3, pada_int - 1))
    pada_syllable = NAKSHATRA_SYLLABLES[nak_idx][pada_idx]
    all_syllables = ", ".join(NAKSHATRA_SYLLABLES[nak_idx])

    # 10. Vruksha & Pakshi
    vruksha_te = NAKSHATRA_VRUKSHA[nak_idx]
    pakshi_te = NAKSHATRA_PAKSHI[nak_idx]

    return {
        "tithi": tithi_name,
        "paksha": paksha,
        "vara": f"{vara['te']} ({vara['en']})",
        "vara_lord": vara["lord"],
        "nakshatra": f"{moon_nak['name_te']} ({moon_nak['name_en']})",
        "nakshatra_index": nak_idx,
        "moon_nakshatra_index": nak_idx,
        "nakshatra_name_te": moon_nak["name_te"],
        "nakshatra_name_en": moon_nak["name_en"],
        "pada": f"{pada}వ పాదం",
        "nakshatra_lord": moon_nak["lord_te"],
        "yoga": yoga_name,
        "karana": karana_name,
        # Complete Avakahada Chakra
        "gana": gana_te,
        "nadi": nadi_te,
        "yoni": yoni_te,
        "varna": varna_te,
        "vashya": vashya_te,
        "tatwa": tatwa_te,
        "paya": paya_name,
        "paya_desc": paya_desc,
        "nama_aksharam": pada_syllable,
        "all_nama_aksharas": all_syllables,
        "vruksha": vruksha_te,
        "pakshi": pakshi_te,
        "janma_rashi": RASHIS[moon_rashi_idx]["name_te"],
        "janma_rashi_index": moon_rashi_idx,
        "janma_rashi_en": RASHIS[moon_rashi_idx]["name_en"],
        "rashi_name_te": RASHIS[moon_rashi_idx]["name_te"],
        "janma_lagna": RASHIS[lagna_info["rashi_index"]]["name_te"],
        "janma_lagna_index": lagna_info["rashi_index"],
    }


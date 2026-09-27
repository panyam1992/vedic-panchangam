# -*- coding: utf-8 -*-
"""
Ashtakoota & Dashakoota Guna Milan Engine (అష్టకూట గుణ మేలనం & దశకూట పొంతన - 36 Points Match).

Classical 36-Point Vedic Marriage Compatibility System:
1. వర్ణ కూటం (Varna - 1 Point) - Spiritual & ego compatibility
2. వశ్య కూటం (Vashya - 2 Points) - Mutual attraction & dominance
3. తారా కూటం (Tara / Dina - 3 Points) - Destiny, health & longevity
4. యోని కూటం (Yoni - 4 Points) - Biological, intimate & physical harmony
5. గ్రహ మైత్రి కూటం (Graha Maitri - 5 Points) - Mental, psychological & friendship harmony
6. గణ కూటం (Gana - 6 Points) - Temperament & behavioral compatibility (Deva, Manushya, Rakshasa)
7. భకూట కూటం (Bhakoota - 7 Points) - Family happiness, financial growth & emotional bond
8. నాడీ కూటం (Nadi - 8 Points) - Genetic, physiological health & progeny vitality

Plus South Indian Dashakoota (దశకూటములు - 10 Poruthams):
Dina, Gana, Mahendra, Stree Deergha, Yoni, Rashi, Rasyadhipati, Vashya, Rajju, Vedha.

Cites:
- బృహత్ పరాశర హోరాశాస్త్రం (BPHS Ch. 83 - వివాహ మేలనం)
- ముహూర్త చింతామణి (Muhurtha Chintamani - వివాహ ప్రకరణం)
- ఫలదీపిక (Phaladeepika Ch. 12)
- కాలామృతమ్ (Kalamritam - వివాహ కూట విచారణ)
"""

from typing import Dict, Any, List, Tuple


# 27 Nakshatra Names in Telugu & English
NAKSHATRAS = [
    {"name_te": "అశ్విని", "name_en": "Ashwini", "lord": "కేతువు"},
    {"name_te": "భరణి", "name_en": "Bharani", "lord": "శుక్రుడు"},
    {"name_te": "కృత్తిక", "name_en": "Krittika", "lord": "సూర్యుడు"},
    {"name_te": "రోహిణి", "name_en": "Rohini", "lord": "చంద్రుడు"},
    {"name_te": "మృగశిర", "name_en": "Mrigashira", "lord": "కుజుడు"},
    {"name_te": "ఆరుద్ర", "name_en": "Ardra", "lord": "రాహువు"},
    {"name_te": "పునర్వసు", "name_en": "Punarvasu", "lord": "గురుడు"},
    {"name_te": "పుష్యమి", "name_en": "Pushya", "lord": "శని"},
    {"name_te": "ఆశ్లేష", "name_en": "Ashlesha", "lord": "బుధుడు"},
    {"name_te": "మఖ", "name_en": "Magha", "lord": "కేతువు"},
    {"name_te": "పూర్వఫల్గుణి", "name_en": "Purva Phalguni", "lord": "శుక్రుడు"},
    {"name_te": "ఉత్తరఫల్గుణి", "name_en": "Uttara Phalguni", "lord": "సూర్యుడు"},
    {"name_te": "హస్త", "name_en": "Hasta", "lord": "చంద్రుడు"},
    {"name_te": "చిత్త", "name_en": "Chitra", "lord": "కుజుడు"},
    {"name_te": "స్వాతి", "name_en": "Swati", "lord": "రాహువు"},
    {"name_te": "విశాఖ", "name_en": "Vishakha", "lord": "గురుడు"},
    {"name_te": "అనూరాధ", "name_en": "Anuradha", "lord": "శని"},
    {"name_te": "జ్యేష్ఠ", "name_en": "Jyeshtha", "lord": "బుధుడు"},
    {"name_te": "మూల", "name_en": "Moola", "lord": "కేతువు"},
    {"name_te": "పూర్వాషాఢ", "name_en": "Purvashadha", "lord": "శుక్రుడు"},
    {"name_te": "ఉత్తరాషాఢ", "name_en": "Uttarashadha", "lord": "సూర్యుడు"},
    {"name_te": "శ్రవణం", "name_en": "Shravana", "lord": "చంద్రుడు"},
    {"name_te": "ధనిష్ఠ", "name_en": "Dhanishta", "lord": "కుజుడు"},
    {"name_te": "శతభిషం", "name_en": "Shatabhisha", "lord": "రాహువు"},
    {"name_te": "పూర్వాభాద్ర", "name_en": "Purvabhadra", "lord": "గురుడు"},
    {"name_te": "ఉత్తరాభాద్ర", "name_en": "Uttarabhadra", "lord": "శని"},
    {"name_te": "రేవతి", "name_en": "Revati", "lord": "బుధుడు"}
]

# 12 Rashi Lords & Telugu Names
RASHI_LORDS = ["కుజుడు", "శుక్రుడు", "బుధుడు", "చంద్రుడు", "సూర్యుడు", "బుధుడు", "శుక్రుడు", "కుజుడు", "గురుడు", "శని", "శని", "గురుడు"]
RASHI_NAMES_TE = ["మేషం", "వృషభం", "మిథునం", "కర్కాటకం", "సింహం", "కన్య", "తుల", "వృశ్చికం", "ధనుస్సు", "మకరం", "కుంభం", "మీనం"]

# 1. VARNA CLASSIFICATION (Brahmin, Kshatriya, Vaishya, Shudra)
# Water = Brahmin (Cancer, Scorpio, Pisces -> 3, 7, 11)
# Fire = Kshatriya (Aries, Leo, Sagittarius -> 0, 4, 8)
# Earth = Vaishya (Taurus, Virgo, Capricorn -> 1, 5, 9)
# Air = Shudra (Gemini, Libra, Aquarius -> 2, 6, 10)
RASHI_VARNA = {
    3: ("బ్రాహ్మణ", 4), 7: ("బ్రాహ్మణ", 4), 11: ("బ్రాహ్మణ", 4),
    0: ("క్షత్రియ", 3), 4: ("క్షత్రియ", 3), 8: ("క్షత్రియ", 3),
    1: ("వైశ్య", 2), 5: ("వైశ్య", 2), 9: ("వైశ్య", 2),
    2: ("శూద్ర", 1), 6: ("శూద్ర", 1), 10: ("శూద్ర", 1)
}

# 2. VASHYA CLASSIFICATION
# 0=Chatushpada (Quadruped), 1=Manava (Human), 2=Jalachara (Water), 3=Vanachara (Wild/Lion), 4=Keeta (Insect)
RASHI_VASHYA = {
    0: "చతుష్పాద", 1: "చతుష్పాద",
    2: "మానవ/ద్విపాద", 3: "జలచర",
    4: "వనచర (సింహం)", 5: "మానవ/ద్విపాద",
    6: "మానవ/ద్విపాద", 7: "కీటకం",
    8: "మానవ/ద్విపాద", 9: "జలచర/చతుష్పాద",
    10: "మానవ/ద్విపాద", 11: "జలచర"
}

# 3. YONI (14 Animals)
NAKSHATRA_YONI = {
    0: ("అశ్వం (గుర్రం)", "Horse", 0),
    1: ("గజం (ఏనుగు)", "Elephant", 1),
    2: ("మేషం (గొర్రె)", "Sheep", 2),
    3: ("సర్పం (పాము)", "Serpent", 3),
    4: ("సర్పం (పాము)", "Serpent", 3),
    5: ("శునకం (కుక్క)", "Dog", 4),
    6: ("మార్జాలం (పిల్లి)", "Cat", 5),
    7: ("మేషం (గొర్రె)", "Sheep", 2),
    8: ("మార్జాలం (పిల్లి)", "Cat", 5),
    9: ("మూషికం (ఎలుక)", "Rat", 6),
    10: ("మూషికం (ఎలుక)", "Rat", 6),
    11: ("గోవు (ఆవు)", "Cow", 7),
    12: ("మహిషం (దున్నపోతు)", "Buffalo", 8),
    13: ("వ్యాఘ్రం (పులి)", "Tiger", 9),
    14: ("మహిషం (దున్నపోతు)", "Buffalo", 8),
    15: ("వ్యాఘ్రం (పులి)", "Tiger", 9),
    16: ("మృగం (జింక)", "Deer", 10),
    17: ("మృగం (జింక)", "Deer", 10),
    18: ("శునకం (కుక్క)", "Dog", 4),
    19: ("వానరం (కోతి)", "Monkey", 11),
    20: ("నకులం (ముంగిస)", "Mongoose", 12),
    21: ("వానరం (కోతి)", "Monkey", 11),
    22: ("సింహం", "Lion", 13),
    23: ("అశ్వం (గుర్రం)", "Horse", 0),
    24: ("సింహం", "Lion", 13),
    25: ("గోవు (ఆవు)", "Cow", 7),
    26: ("గజం (ఏనుగు)", "Elephant", 1)
}

# Sworn enemy animal pairs (0 points)
YONI_ENEMIES = {
    frozenset({0, 8}),   # Horse vs Buffalo
    frozenset({1, 13}),  # Elephant vs Lion
    frozenset({2, 11}),  # Sheep vs Monkey
    frozenset({3, 12}),  # Serpent vs Mongoose
    frozenset({4, 10}),  # Dog vs Deer
    frozenset({5, 6}),   # Cat vs Rat
    frozenset({7, 9}),   # Cow vs Tiger
}

# 4. GANA (Deva, Manushya, Rakshasa)
# 0=Deva, 1=Manushya, 2=Rakshasa
NAKSHATRA_GANA = {
    0: ("దేవ గణం", 0), 1: ("మనుష్య గణం", 1), 2: ("రాక్షస గణం", 2),
    3: ("మనుష్య గణం", 1), 4: ("దేవ గణం", 0), 5: ("మనుష్య గణం", 1),
    6: ("దేవ గణం", 0), 7: ("దేవ గణం", 0), 8: ("రాక్షస గణం", 2),
    9: ("రాక్షస గణం", 2), 10: ("మనుష్య గణం", 1), 11: ("మనుష్య గణం", 1),
    12: ("దేవ గణం", 0), 13: ("రాక్షస గణం", 2), 14: ("దేవ గణం", 0),
    15: ("రాక్షస గణం", 2), 16: ("దేవ గణం", 0), 17: ("రాక్షస గణం", 2),
    18: ("రాక్షస గణం", 2), 19: ("మనుష్య గణం", 1), 20: ("మనుష్య గణం", 1),
    21: ("దేవ గణం", 0), 22: ("రాక్షస గణం", 2), 23: ("రాక్షస గణం", 2),
    24: ("మనుష్య గణం", 1), 25: ("మనుష్య గణం", 1), 26: ("దేవ గణం", 0)
}

# 5. NADI (Aadi, Madhya, Antya)
# 0=Aadi, 1=Madhya, 2=Antya
NAKSHATRA_NADI = {
    0: ("ఆది నాడి", 0), 1: ("మధ్య నాడి", 1), 2: ("అంత్య నాడి", 2),
    3: ("అంత్య నాడి", 2), 4: ("మధ్య నాడి", 1), 5: ("ఆది నాడి", 0),
    6: ("ఆది నాడి", 0), 7: ("మధ్య నాడి", 1), 8: ("అంత్య నాడి", 2),
    9: ("అంత్య నాడి", 2), 10: ("మధ్య నాడి", 1), 11: ("ఆది నాడి", 0),
    12: ("ఆది నాడి", 0), 13: ("మధ్య నాడి", 1), 14: ("అంత్య నాడి", 2),
    15: ("అంత్య నాడి", 2), 16: ("మధ్య నాడి", 1), 17: ("ఆది నాడి", 0),
    18: ("ఆది నాడి", 0), 19: ("మధ్య నాడి", 1), 20: ("అంత్య నాడి", 2),
    21: ("అంత్య నాడి", 2), 22: ("మధ్య నాడి", 1), 23: ("ఆది నాడి", 0),
    24: ("ఆది నాడి", 0), 25: ("మధ్య నాడి", 1), 26: ("అంత్య నాడి", 2)
}

# 6. RAJJU (South Indian Porutham: Siro, Kantha, Nabha, Kati, Pada)
NAKSHATRA_RAJJU = {
    0: "పాద రజ్జు", 1: "కటి రజ్జు", 2: "నాభి రజ్జు", 3: "కంఠ రజ్జు", 4: "శిరో రజ్జు",
    5: "కంఠ రజ్జు", 6: "నాభి రజ్జు", 7: "కటి రజ్జు", 8: "పాద రజ్జు",
    9: "పాద రజ్జు", 10: "కటి రజ్జు", 11: "నాభి రజ్జు", 12: "కంఠ రజ్జు", 13: "శిరో రజ్జు",
    14: "కంఠ రజ్జు", 15: "నాభి రజ్జు", 16: "కటి రజ్జు", 17: "పాద రజ్జు",
    18: "పాద రజ్జు", 19: "కటి రజ్జు", 20: "నాభి రజ్జు", 21: "కంఠ రజ్జు", 22: "శిరో రజ్జు",
    23: "కంఠ రజ్జు", 24: "నాభి రజ్జు", 25: "కటి రజ్జు", 26: "పాద రజ్జు"
}


def calculate_ashtakoota_milan(
    groom_nak_idx: int,
    groom_rashi_idx: int,
    bride_nak_idx: int,
    bride_rashi_idx: int,
    groom_pada: int = 1,
    bride_pada: int = 1
) -> Dict[str, Any]:
    """
    Computes complete 36-Point Ashtakoota Guna Milan and 10 Dashakoota Poruthams
    between Groom and Bride according to Brihat Parashara Hora Shastra & Muhurtha Chintamani.
    """
    g_nak = groom_nak_idx % 27
    b_nak = bride_nak_idx % 27
    g_rashi = groom_rashi_idx % 12
    b_rashi = bride_rashi_idx % 12

    kootas = []
    total_obtained = 0.0
    total_max = 36.0

    # -------------------------------------------------------------
    # 1. VARNA KOOTA (వర్ణ కూటం - Max 1.0 Point)
    # -------------------------------------------------------------
    g_varna_name, g_varna_val = RASHI_VARNA.get(g_rashi, ("శూద్ర", 1))
    b_varna_name, b_varna_val = RASHI_VARNA.get(b_rashi, ("శూద్ర", 1))

    if g_varna_val >= b_varna_val:
        varna_pts = 1.0
        varna_desc = f"వరుని వర్ణం ({g_varna_name}) వధువు వర్ణానికి ({b_varna_name}) సమానం లేదా ఉన్నతమైనది. ఆహంకార సమన్వయం ఉత్తమం."
        varna_badge = "success"
    else:
        varna_pts = 0.0
        varna_desc = f"వధువు వర్ణం ({b_varna_name}) వరుని కంటే ఉన్నతం. పరస్పర సహనం ఆవశ్యకం."
        varna_badge = "danger"

    kootas.append({
        "name_te": "వర్ణ కూటం (Varna)",
        "name_en": "Varna Koota",
        "obtained": varna_pts,
        "max": 1.0,
        "groom_attr": g_varna_name,
        "bride_attr": b_varna_name,
        "description": varna_desc,
        "badge": varna_badge
    })
    total_obtained += varna_pts

    # -------------------------------------------------------------
    # 2. VASHYA KOOTA (వశ్య కూటం - Max 2.0 Points)
    # -------------------------------------------------------------
    g_vashya = RASHI_VASHYA.get(g_rashi, "మానవ/ద్విపాద")
    b_vashya = RASHI_VASHYA.get(b_rashi, "మానవ/ద్విపాద")

    if g_rashi == b_rashi or g_vashya == b_vashya:
        vashya_pts = 2.0
        vashya_desc = f"ఇరువురి వశ్య స్వభావం ({g_vashya}) సమానం; పరస్పర ఆకర్షణ, ఏకీభావం పరిపూర్ణం."
        vashya_badge = "success"
    elif (g_rashi, b_rashi) in [(2, 5), (5, 2), (2, 6), (6, 2), (0, 4), (4, 0), (8, 0)]:
        vashya_pts = 1.0
        vashya_desc = "మధ్యమ వశ్య ప్రభావం; దాంపత్యంలో ఒకరికొకరు సర్దుకుపోయే తత్వం కలదు."
        vashya_badge = "warning"
    else:
        vashya_pts = 0.0
        vashya_desc = "భిన్న వశ్య రాశులు; దాంపత్యంలో సమాన గౌరవం మరియు సంభాషణ అవసరం."
        vashya_badge = "info"

    kootas.append({
        "name_te": "వశ్య కూటం (Vashya)",
        "name_en": "Vashya Koota",
        "obtained": vashya_pts,
        "max": 2.0,
        "groom_attr": g_vashya,
        "bride_attr": b_vashya,
        "description": vashya_desc,
        "badge": vashya_badge
    })
    total_obtained += vashya_pts

    # -------------------------------------------------------------
    # 3. TARA KOOTA (తారా కూటం / దిన పొంతన - Max 3.0 Points)
    # Count from Bride to Groom, and Groom to Bride (mod 9)
    # Favorable: 2 (Sampat), 4 (Kshema), 6 (Sadhana), 8 (Mitra), 0/9 (Parama Mitra), and 1 if same nakshatra
    # -------------------------------------------------------------
    b_to_g = ((g_nak - b_nak) % 27) % 9
    g_to_b = ((b_nak - g_nak) % 27) % 9

    favorable_taras = [1, 2, 4, 6, 8, 0]
    g_favorable = b_to_g in favorable_taras
    b_favorable = g_to_b in favorable_taras

    if g_favorable and b_favorable:
        tara_pts = 3.0
        tara_desc = "వధూవరులిద్దరికీ ఉభయ తారాబలం పరిపూర్ణంగా ఉన్నది. ఆయురారోగ్యాలు, అదృష్టం సిద్ధించును."
        tara_badge = "success"
    elif g_favorable or b_favorable:
        tara_pts = 1.5
        tara_desc = "ఏకపక్ష తారాబలం కలదు; మధ్యమ ఫలితం. సాధారణ ఇష్టదైవ ఆరాధన శ్రేయస్కరం."
        tara_badge = "warning"
    else:
        tara_pts = 0.0
        tara_desc = "ఇరువురికీ నైధన లేదా విపత్ తార సూచన. గురు/చంద్ర బల పరిశీలన ఆవశ్యకం."
        tara_badge = "danger"

    kootas.append({
        "name_te": "తారా కూటం (Tara)",
        "name_en": "Tara Koota",
        "obtained": tara_pts,
        "max": 3.0,
        "groom_attr": f"తార: {b_to_g if b_to_g != 0 else 9}",
        "bride_attr": f"తార: {g_to_b if g_to_b != 0 else 9}",
        "description": tara_desc,
        "badge": tara_badge
    })
    total_obtained += tara_pts

    # -------------------------------------------------------------
    # 4. YONI KOOTA (యోని కూటం - Max 4.0 Points)
    # Biological, Physical & Intimate compatibility
    # -------------------------------------------------------------
    g_yoni_te, g_yoni_en, g_yoni_id = NAKSHATRA_YONI.get(g_nak, ("అశ్వం", "Horse", 0))
    b_yoni_te, b_yoni_en, b_yoni_id = NAKSHATRA_YONI.get(b_nak, ("అశ్వం", "Horse", 0))

    is_sworn_enemy = frozenset({g_yoni_id, b_yoni_id}) in YONI_ENEMIES

    if g_yoni_id == b_yoni_id:
        yoni_pts = 4.0
        yoni_desc = f"ఇరువురిదీ ఒకే యోని ({g_yoni_te}); శారీరక, మానసిక దాంపత్య సౌఖ్యం అత్యుత్తమం."
        yoni_badge = "success"
    elif is_sworn_enemy:
        yoni_pts = 0.0
        yoni_desc = f"పరస్పర వైరి యోనులు ({g_yoni_te} vs {b_yoni_te}); ప్రకృతి సిద్ధ విరోధం కలదు."
        yoni_badge = "danger"
    else:
        # Friendly vs Neutral animals
        diff = abs(g_yoni_id - b_yoni_id)
        if diff in [1, 2, 4]:
            yoni_pts = 3.0
            yoni_desc = f"మిత్ర యోనులు ({g_yoni_te} & {b_yoni_te}); ఉత్తమ దాంపత్య సామరస్యం."
            yoni_badge = "success"
        else:
            yoni_pts = 2.0
            yoni_desc = f"సాధారణ యోని పొంతన ({g_yoni_te} & {b_yoni_te}); అనుకూల దాంపత్యం."
            yoni_badge = "warning"

    kootas.append({
        "name_te": "యోని కూటం (Yoni)",
        "name_en": "Yoni Koota",
        "obtained": yoni_pts,
        "max": 4.0,
        "groom_attr": g_yoni_te,
        "bride_attr": b_yoni_te,
        "description": yoni_desc,
        "badge": yoni_badge
    })
    total_obtained += yoni_pts

    # -------------------------------------------------------------
    # 5. GRAHA MAITRI (గ్రహ మైత్రి కూటం - Max 5.0 Points)
    # Lords of Moon signs compatibility
    # -------------------------------------------------------------
    g_lord = RASHI_LORDS[g_rashi]
    b_lord = RASHI_LORDS[b_rashi]

    # Friendly planetary groups
    deva_group = ["సూర్యుడు", "చంద్రుడు", "కుజుడు", "గురుడు"]
    asura_group = ["బుధుడు", "శుక్రుడు", "శని"]

    if g_lord == b_lord:
        graha_pts = 5.0
        graha_desc = f"ఇద్దరి రాశ్యాధిపతి ఒక్కరే ({g_lord}); ఏక భావన, సంపూర్ణ మానసిక ఐకమత్యం."
        graha_badge = "success"
    elif (g_lord in deva_group and b_lord in deva_group) or (g_lord in asura_group and b_lord in asura_group):
        graha_pts = 5.0
        graha_desc = f"ఇరువురి రాశ్యాధిపతులు పరస్పర మిత్రులు ({g_lord} & {b_lord}); చక్కని అవగాహన."
        graha_badge = "success"
    elif (g_lord == "బుధుడు" and b_lord in ["సూర్యుడు", "గురుడు"]) or (b_lord == "బుధుడు" and g_lord in ["సూర్యుడు", "గురుడు"]):
        graha_pts = 4.0
        graha_desc = f"మిత్ర-సమ భావం ({g_lord} & {b_lord}); గౌరవప్రదమైన అనుబంధం."
        graha_badge = "success"
    elif (g_lord in ["శుక్రుడు", "శని"] and b_lord in ["గురుడు", "కుజుడు"]) or (b_lord in ["శుక్రుడు", "శని"] and g_lord in ["గురుడు", "కుజుడు"]):
        graha_pts = 3.0
        graha_desc = f"సమ గ్రహ సంబంధం ({g_lord} & {b_lord}); మధ్యమ మానసిక సయోధ్య."
        graha_badge = "warning"
    elif (g_lord in ["సూర్యుడు", "చంద్రుడు"] and b_lord in ["శుక్రుడు", "శని"]) or (b_lord in ["సూర్యుడు", "చంద్రుడు"] and g_lord in ["శుక్రుడు", "శని"]):
        graha_pts = 1.0
        graha_desc = f"శత్రు గ్రహ సంబంధం ({g_lord} vs {b_lord}); అభిప్రాయ భేదాలు వచ్చే అవకాశం."
        graha_badge = "danger"
    else:
        graha_pts = 0.5
        graha_desc = "గ్రహ మైత్రిలో లోపం; చర్చల ద్వారా నిర్ణయాలు తీసుకోవాలి."
        graha_badge = "danger"

    kootas.append({
        "name_te": "గ్రహ మైత్రి (Graha Maitri)",
        "name_en": "Graha Maitri Koota",
        "obtained": graha_pts,
        "max": 5.0,
        "groom_attr": f"{RASHI_NAMES_TE[g_rashi]} ({g_lord})",
        "bride_attr": f"{RASHI_NAMES_TE[b_rashi]} ({b_lord})",
        "description": graha_desc,
        "badge": graha_badge
    })
    total_obtained += graha_pts

    # -------------------------------------------------------------
    # 6. GANA KOOTA (గణ కూటం - Max 6.0 Points)
    # Deva (0), Manushya (1), Rakshasa (2)
    # -------------------------------------------------------------
    g_gana_te, g_gana_id = NAKSHATRA_GANA.get(g_nak, ("దేవ గణం", 0))
    b_gana_te, b_gana_id = NAKSHATRA_GANA.get(b_nak, ("దేవ గణం", 0))

    if g_gana_id == b_gana_id:
        gana_pts = 6.0
        gana_desc = f"ఇరువురిదీ సమాన గణం ({g_gana_te}); భావాలు, జీవన శైలి, ఆలోచనా సరళి పరిపూర్ణంగా సరిపోతాయి."
        gana_badge = "success"
    elif (g_gana_id == 0 and b_gana_id == 1): # Deva groom, Manushya bride
        gana_pts = 6.0
        gana_desc = "వరుడు దేవగణం, వధువు మనుష్యగణం; అత్యంత శుభప్రదమైన దాంపత్య పొంతన."
        gana_badge = "success"
    elif (g_gana_id == 1 and b_gana_id == 0): # Manushya groom, Deva bride
        gana_pts = 5.0
        gana_desc = "వరుడు మనుష్యగణం, వధువు దేవగణం; చక్కని అనుకూలత."
        gana_badge = "success"
    elif (g_gana_id == 0 and b_gana_id == 2): # Deva groom, Rakshasa bride
        gana_pts = 1.0
        gana_desc = "దేవ-రాక్షస గణ భేదం; పట్టువిడుపులు అవసరం."
        gana_badge = "warning"
    elif (g_gana_id == 2 and b_gana_id == 0): # Rakshasa groom, Deva bride
        gana_pts = 0.0
        gana_desc = "రాక్షస-దేవ గణ భేదం కలదు; రాశ్యాధిపతి మైత్రి లేదా నాడీ బలం ఉన్నచో దోష నివృత్తి."
        gana_badge = "danger"
    else: # Manushya + Rakshasa
        gana_pts = 0.0
        gana_desc = "మనుష్య-రాక్షస గణ విరోధం; పరస్పర సర్దుబాటు అత్యంత ముఖ్యం."
        gana_badge = "danger"

    kootas.append({
        "name_te": "గణ కూటం (Gana)",
        "name_en": "Gana Koota",
        "obtained": gana_pts,
        "max": 6.0,
        "groom_attr": g_gana_te,
        "bride_attr": b_gana_te,
        "description": gana_desc,
        "badge": gana_badge
    })
    total_obtained += gana_pts

    # -------------------------------------------------------------
    # 7. BHAKOOTA (భకూట కూటం / రాశి కూటం - Max 7.0 Points)
    # Distance from Bride to Groom
    # Auspicious: 1/1, 1/7, 3/11, 4/10
    # Inauspicious: 2/12 (Dwirdwadasha), 6/8 (Shadashtaka), 9/5 (Navapanchama)
    # Cancellations: Same lord, friendly lords
    # -------------------------------------------------------------
    rashi_dist = ((g_rashi - b_rashi) % 12) + 1 # 1 to 12
    bhakoota_cancellation = (g_lord == b_lord) or (g_lord in deva_group and b_lord in deva_group) or (g_lord in asura_group and b_lord in asura_group)

    if rashi_dist in [1, 7, 3, 11, 4, 10]:
        bhakoota_pts = 7.0
        bhakoota_desc = f"శుభ రాశి సంబంధం ({rashi_dist}వ స్థానం); కుటుంబ సౌఖ్యం, వంశాభివృద్ధి, ఐశ్వర్యం సిద్ధించును."
        bhakoota_badge = "success"
    elif rashi_dist in [6, 8]:
        if bhakoota_cancellation:
            bhakoota_pts = 7.0
            bhakoota_desc = f"షడష్టక సంబంధం (6-8) అయినప్పటికీ రాశ్యాధిపతుల మైత్రి/ఏకత్వం వలన భకూట దోషభంగం సిద్ధించినది (దోష నివృత్తి)."
            bhakoota_badge = "success"
        else:
            bhakoota_pts = 0.0
            bhakoota_desc = "షడష్టక రాశి సంబంధం (6-8); ఆరోగ్య, ఆర్థిక విషయాలలో దైవిక రక్షణ అవసరం."
            bhakoota_badge = "danger"
    elif rashi_dist in [2, 12]:
        if bhakoota_cancellation:
            bhakoota_pts = 7.0
            bhakoota_desc = f"ద్విర్ద్వాదశం (2-12) అయినప్పటికీ రాశ్యాధిపతుల మైత్రి వలన దోష నివృత్తి కలదు."
            bhakoota_badge = "success"
        else:
            bhakoota_pts = 0.0
            bhakoota_desc = "ద్విర్ద్వాదశ రాశి సంబంధం (2-12); ధన వ్యయ నియంత్రణ అవసరం."
            bhakoota_badge = "danger"
    else: # 5, 9
        if bhakoota_cancellation:
            bhakoota_pts = 7.0
            bhakoota_desc = "నవ-పంచమ సంబంధం (5-9); రాశ్యాధిపతి అనుకూలతతో సంతాన సౌఖ్యం."
            bhakoota_badge = "success"
        else:
            bhakoota_pts = 0.0
            bhakoota_desc = "నవ-పంచమ సంబంధం; సంతాన విషయాలలో దైవ ప్రార్థన అవసరం."
            bhakoota_badge = "warning"

    kootas.append({
        "name_te": "భకూట కూటం (Bhakoota)",
        "name_en": "Bhakoota Koota",
        "obtained": bhakoota_pts,
        "max": 7.0,
        "groom_attr": f"{RASHI_NAMES_TE[g_rashi]}",
        "bride_attr": f"{RASHI_NAMES_TE[b_rashi]} ({rashi_dist}వ ఇల్లు)",
        "description": bhakoota_desc,
        "badge": bhakoota_badge
    })
    total_obtained += bhakoota_pts

    # -------------------------------------------------------------
    # 8. NADI KOOTA (నాడీ కూటం - Max 8.0 Points)
    # Aadi (0), Madhya (1), Antya (2)
    # Different Nadis = 8 Points
    # Same Nadi = 0 Points (Nadi Dosha), unless cancelled
    # -------------------------------------------------------------
    g_nadi_te, g_nadi_id = NAKSHATRA_NADI.get(g_nak, ("ఆది నాడి", 0))
    b_nadi_te, b_nadi_id = NAKSHATRA_NADI.get(b_nak, ("ఆది నాడి", 0))

    if g_nadi_id != b_nadi_id:
        nadi_pts = 8.0
        nadi_desc = f"ఇరువురిదీ భిన్న నాడి ({g_nadi_te} & {b_nadi_te}); సంపూర్ణ నాడీ బలం కలదు. జన్యుపరంగా, ఆరోగ్యపరంగా సత్సంతాన ప్రాప్తి."
        nadi_badge = "success"
    else:
        # Same Nadi - Check classical cancellations
        # 1. Same Rashi but different Nakshatras
        # 2. Same Nakshatra but different Rashis (e.g. Krittika, Uttarashadha, etc.)
        # 3. Same Nakshatra with different Padas
        nadi_cancellation = (g_rashi == b_rashi and g_nak != b_nak) or (g_nak == b_nak and groom_pada != bride_pada) or (g_rashi != b_rashi and g_nak == b_nak)
        if nadi_cancellation:
            nadi_pts = 8.0
            nadi_desc = f"ఏక నాడి ({g_nadi_te}) అయినప్పటికీ పాద భేదం / నక్షత్ర భేదం వలన శాస్త్రోక్త నాడీ దోషభంగం సిద్ధించినది (పరిపూర్ణ రక్షణ)."
            nadi_badge = "success"
        else:
            nadi_pts = 0.0
            nadi_desc = f"ఏక నాడీ దోషం కలదు ({g_nadi_te}); వివాహానంతరం మహా మృత్యుంజయ జపం లేదా సువర్ణ దానం శ్రేయస్కరం."
            nadi_badge = "danger"

    kootas.append({
        "name_te": "నాడీ కూటం (Nadi)",
        "name_en": "Nadi Koota",
        "obtained": nadi_pts,
        "max": 8.0,
        "groom_attr": g_nadi_te,
        "bride_attr": b_nadi_te,
        "description": nadi_desc,
        "badge": nadi_badge
    })
    total_obtained += nadi_pts

    # -------------------------------------------------------------
    # DASHAKOOTA (దశకూటములు - 10 South Indian Poruthams)
    # -------------------------------------------------------------
    # 1. Dina Porutham
    dina_match = tara_pts >= 1.5
    # 2. Gana Porutham
    gana_match = gana_pts >= 5.0
    # 3. Mahendra Porutham (Nakshatra count: 4, 7, 10, 13, 16, 19, 22, 25)
    nak_dist = ((g_nak - b_nak) % 27) + 1
    mahendra_match = nak_dist in [4, 7, 10, 13, 16, 19, 22, 25]
    # 4. Stree Deergha (Groom > 13 nakshatras away from bride)
    stree_deergha_match = nak_dist > 9
    # 5. Yoni Porutham
    yoni_match = not is_sworn_enemy
    # 6. Rashi Porutham
    rashi_match = bhakoota_pts >= 7.0
    # 7. Rasyadhipati Porutham
    rasyadhipati_match = graha_pts >= 3.0
    # 8. Vashya Porutham
    vashya_match = vashya_pts >= 1.0
    # 9. Rajju Porutham (Different Rajju is mandatory!)
    g_rajju = NAKSHATRA_RAJJU.get(g_nak, "మధ్యమ")
    b_rajju = NAKSHATRA_RAJJU.get(b_nak, "మధ్యమ")
    rajju_match = g_rajju != b_rajju
    # 10. Vedha Porutham (Inimical Nakshatra pairs)
    vedha_pairs = {
        frozenset({0, 17}), frozenset({1, 16}), frozenset({2, 15}), frozenset({3, 14}),
        frozenset({4, 13}), frozenset({5, 12}), frozenset({6, 11}), frozenset({7, 10}),
        frozenset({8, 9}), frozenset({18, 26}), frozenset({19, 25}), frozenset({20, 24}),
        frozenset({21, 23})
    }
    vedha_match = frozenset({g_nak, b_nak}) not in vedha_pairs

    dashakoota_list = [
        {"name_te": "దిన కూటం (Dina)", "significance": "ఆయురారోగ్యాలు & సుఖ శాంతులు", "is_matched": dina_match},
        {"name_te": "గణ కూటం (Gana)", "significance": "శీల సామరస్యం & మానసిక పొందిక", "is_matched": gana_match},
        {"name_te": "మాహేంద్ర కూటం (Mahendra)", "significance": "సంతాన వృద్ధి & వంశోద్ధరణ", "is_matched": mahendra_match},
        {"name_te": "స్త్రీదీర్ఘ కూటం (Stree Deergha)", "significance": "సౌభాగ్యవృద్ధి & దాంపత్య దీర్ఘాయుష్షు", "is_matched": stree_deergha_match},
        {"name_te": "యోని కూటం (Yoni)", "significance": "శారీరక అనుకూలత & ఆకర్షణ", "is_matched": yoni_match},
        {"name_te": "రాశి కూటం (Rashi)", "significance": "వంశాభివృద్ధి & ఆర్థిక స్థిరత్వం", "is_matched": rashi_match},
        {"name_te": "రాశ్యధిపతి కూటం (Rasyadhipati)", "significance": "నిత్య సంతోషం & ఆలోచనా మైత్రి", "is_matched": rasyadhipati_match},
        {"name_te": "వశ్య కూటం (Vashya)", "significance": "పరస్పర ఆకర్షణ & ప్రేమానుబంధం", "is_matched": vashya_match},
        {"name_te": "రజ్జు కూటం (Rajju)", "significance": "మాంగళ్య బలం & పాతివ్రత్య రక్షణ", "is_matched": rajju_match, "critical": True},
        {"name_te": "వేధ కూటం (Vedha)", "significance": "వివాహ ఆటంకాలు & ఉపద్రవాల నివారణ", "is_matched": vedha_match, "critical": True}
    ]
    dashakoota_passed = sum(1 for d in dashakoota_list if d["is_matched"])

    # -------------------------------------------------------------
    # FINAL OVERALL VERDICT
    # -------------------------------------------------------------
    total_obtained = round(total_obtained, 1)

    if total_obtained >= 28.0:
        verdict_te = "అత్యుత్తమ దాంపత్య పొంతన (Excellent Match - 36 గుణ సంపన్నం)"
        verdict_badge = "success"
        verdict_desc = f"36 గుణాలలో {total_obtained} పాయింట్లు లభించినవి. అష్టకూటాలలో నాడీ, భకూట, గణ బలాలు అత్యున్నతంగా ఉన్నందున ఈ వివాహం సర్వతోముఖాభివృద్ధికి, సత్సంతాన ప్రాప్తికి పరమ శ్రేష్ఠమైనది."
    elif total_obtained >= 18.0:
        verdict_te = "ఉత్తమ దాంపత్య పొంతన (Good / Auspicious Match)"
        verdict_badge = "success"
        verdict_desc = f"36 గుణాలలో {total_obtained} పాయింట్లు లభించినవి (శాస్త్ర ప్రామాణికంగా కనీస అర్హత 18 పాయింట్లు దాటినది). దాంపత్య జీవనం సుఖసంతోషాలతో వర్ధిల్లుతుంది. వివాహానికి ఆమోదయోగ్యమైన పొంతన."
    elif total_obtained >= 14.0:
        verdict_te = "మధ్యమ పొంతన (Average Match - దోష నివారణ అవసరం)"
        verdict_badge = "warning"
        verdict_desc = f"36 గుణాలలో {total_obtained} పాయింట్లు వచ్చినవి. ప్రధాన కూటాలలో కొద్దిపాటి వ్యత్యాసాలు ఉన్నందున గురుబలం మరియు దైవిక శాంతి పూజలతో వివాహం నిశ్చయించవచ్చు."
    else:
        verdict_te = "ప్రతికూల పొంతన (Below Average - సంప్రదాయ పరిశీలన ఆవశ్యకం)"
        verdict_badge = "danger"
        verdict_desc = f"36 గుణాలలో {total_obtained} పాయింట్లు మాత్రమే వచ్చినవి. ప్రధాన నాడీ/భకూట కూటాలలో ఆటంకాలు ఉన్నందున అనుభవజ్ఞులైన పురోహితుల మార్గదర్శకంలో జాతక పరిశీలన జరపాలి."

    return {
        "total_points_obtained": total_obtained,
        "total_points_max": total_max,
        "percentage": round((total_obtained / total_max) * 100, 1),
        "verdict_te": verdict_te,
        "verdict_badge": verdict_badge,
        "verdict_desc": verdict_desc,
        "kootas": kootas,
        "dashakoota": {
            "passed_count": dashakoota_passed,
            "total_count": 10,
            "list": dashakoota_list
        },
        "shastra_quote": "బృహత్ పరాశర హోరాశాస్త్రం (అధ్యాయం 83 - వివాహ మేలనం) & ముహూర్త చింతామణి: 'అష్టాదశాధికాః శస్తా మధ్యమా ద్వాదశోర్ధ్వతః'"
    }

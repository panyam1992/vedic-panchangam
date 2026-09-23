"""
Vedic Moudhyam (Combustion) and Kartari (Solar Agni Ingress) Computation Service.
Rooted in Classical Jyotisha Siddhanta, Muhurtha Chintamani, Kalamadhaviyam,
and Panchanga Pithika Lekhana Prakriya by Sri Pidaparti Sitarama Sastry.
"""

from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from typing import Dict, Any, List, Optional
import swisseph as swe

swe.set_sid_mode(swe.SIDM_LAHIRI)

# Angular limits for planetary combustion (Moudhyam)
GURU_MOUDYAM_LIMIT = 11.0  # Jupiter: 11 degrees
SUKRA_PROGRADE_LIMIT = 10.0 # Venus prograde: 10 degrees
SUKRA_RETROGRADE_LIMIT = 8.0 # Venus retrograde: 8 degrees

# Kartari Sun Longitude Boundaries (Lahiri Sidereal)
# Bharani 3rd pada start: 20°00' Aries (20.0°)
KARTARI_CHINNA_START = 20.0
# Krittika 1st pada start: 26°40' Aries (26.666667°)
KARTARI_PEDDA_START = 26.66666667
# Rohini 1st pada start: 10°00' Taurus (40.0°)
KARTARI_ROHINI_START = 40.0
# Rohini 2nd pada end / 3rd pada start: 16°40' Taurus (46.666667°)
KARTARI_END = 46.66666667

# Multilingual strings
MOUDYAM_KARTARI_TEXTS = {
    "telugu": {
        "status_auspicious": "✨ శుద్ధ కాలం (మౌఢ్యం & కర్తరి దోషాలు లేవు)",
        "status_auspicious_desc": "వివాహాది సమస్త శుభ ముహూర్తములకు అనుకూలమైన పవిత్ర కాలం.",
        "guru_moudhyam": "గురు మౌఢ్యమి (బృహస్పతి అస్తమయం)",
        "guru_moudhyam_desc": "సూర్యుడు – గురువుల సామీప్యం (11° లోపు). వివాహం, ఉపనయనం, గృహప్రవేశం, శంకుస్థాపనలు పూర్తిగా వర్జ్యం.",
        "sukra_moudhyam": "శుక్ర మౌఢ్యమి (భార్గవ అస్తమయం)",
        "sukra_moudhyam_desc": "సూర్యుడు – శుక్రుల సామీప్యం (వక్రగతి 8° / ఋజుగతి 10° లోపు). సమస్త కామ్య శుభకార్యములు నిషిద్ధం.",
        "both_moudhyam": "గురు & శుక్ర ద్వంద్వ మౌఢ్యమి",
        "both_moudhyam_desc": "గురు, శుక్రులు ఇద్దరూ అస్తంగతులైన కాలం. శుభకార్యములు త్యాజ్యం.",
        "chinna_kartari": "చిన్న కర్తరి (పూర్వ కత్తెర)",
        "chinna_kartari_desc": "సూర్యుడు భరణి 3, 4 పాదాలలో సంచారం. గృహ శంకుస్థాపనలు, చెట్లు నరకడం అశుభం.",
        "pedda_kartari": "అగ్ని కర్తరి (పెద్ద కత్తెర / ప్రచండ భాను తాపం)",
        "pedda_kartari_desc": "సూర్యుడు కృత్తిక 4 పాదాలలో సంచారం. అత్యంత తీవ్రమైన సూర్యతాపం. నూతన గృహారంభం, స్లాబులు, కలప కోయడం, బావులు తవ్వడం నిషిద్ధం.",
        "rohini_kartari": "రోహిణి కర్తరి (ఉత్తర కత్తెర)",
        "rohini_kartari_desc": "సూర్యుడు రోహిణి 1, 2 పాదాలలో సంచారం. కర్తరి సమాప్తి దశ.",
        "vardhakya_warning": "వార్ధక్య దోషం (అస్తమయానికి పూర్వం 3 రోజులు)",
        "balya_warning": "బాల్య దోషం (ఉదయించిన పిదప 3 రోజులు)",
        "kartari_title": "అగ్ని కర్తరి నిర్ణయ పట్టిక (Kartari Schedule)",
        "kartari_desc": "సూర్యుడు భరణి 3వ పాదం ప్రవేశం మొదలు రోహిణి 2వ పాదం ముగిసే వరకు కర్తరి. గృహారంభాలు, శంకుస్థాపనలు, స్లాబులు, కలప కోయడం నిషిద్ధం.",
        "milestone_chinna_phase": "చిన్న కర్తరి ప్రారంభం",
        "milestone_chinna_transit": "సూర్యుడు భరణి 3వ పాదం ప్రవేశం (మేషం 20°00')",
        "milestone_chinna_imp": "పూర్వ కర్తరి ఆరంభం • శంకుస్థాపనలు వర్జ్యం",
        "milestone_pedda_phase": "పెద్ద కర్తరి / అగ్ని కర్తరి ప్రారంభం",
        "milestone_pedda_transit": "సూర్యుడు కృత్తిక 1వ పాదం ప్రవేశం (మేషం 26°40')",
        "milestone_pedda_imp": "ముఖ్య అగ్ని కర్తరి • ప్రచండ సూర్యతాపం • సమస్త గృహ నిర్మాణ పనులు నిషిద్ధం",
        "milestone_rohini_phase": "రోహిణి కర్తరి ప్రారంభం",
        "milestone_rohini_transit": "సూర్యుడు రోహిణి 1వ పాదం ప్రవేశం (వృషభం 10°00')",
        "milestone_rohini_imp": "ఉత్తర కర్తరి దశ",
        "milestone_end_phase": "కర్తరి త్యాగం (సమాప్తి)",
        "milestone_end_transit": "సూర్యుడు రోహిణి 2వ పాదం ముగింపు (వృషభం 16°40')",
        "milestone_end_imp": "కర్తరి విముక్తి • యథావిధిగా నిర్మాణ పనులు ప్రారంభించవచ్చు",
        "guru_name": "గురుడు (బృహస్పతి)",
        "guru_moudhyam_type": "గురు మౌఢ్యం (బృహస్పతి అస్తమయం)",
        "sukra_name": "శుక్రుడు (భార్గవుడు)",
        "sukra_moudhyam_type": "శుక్ర మౌఢ్యం (భార్గవ అస్తమయం - వక్రగతి)",
        "vardhakya_start_text": "అస్తమయానికి 3 రోజుల ముందు",
        "balya_end_text": "ఉదయించిన 3 రోజుల తర్వాత",
        "guru_prohibition": "వివాహం, ఉపనయనం, గృహప్రవేశం, శంకుస్థాపనలు, నూతన వ్రతాలు సమస్తం నిషిద్ధం.",
        "sukra_prohibition": "సమస్త శుభకార్యములు నిషిద్ధం.",
        "taboos_moudhyam": [
            "వివాహం (Marriage ceremonies)",
            "ఉపనయనం (Sacred thread ceremony)",
            "నూతన గృహప్రవేశం (Housewarming)",
            "గృహారంభం / శంకుస్థాపన (Foundation stone laying)",
            "నూతన దేవతా ప్రతిష్ఠ (Deity consecration)",
            "యజ్ఞ-యాగాదులు & కామ్య వ్రతాలు (Vedic sacrifices)"
        ],
        "taboos_kartari": [
            "నూతన గృహ నిర్మాణ ఆరంభం (New house construction)",
            "ఇంటి పైకప్పు / స్లాబ్ వేయడం (Laying roof slabs)",
            "బావులు, బోర్లు తవ్వడం (Digging wells / borewells)",
            "కలప కోయడం & తోటల పనులు (Cutting timber / tree plantation)",
            "అగ్ని సంబంధిత క్రతువులు (Fire-hazard works)"
        ],
        "permitted_karmas": [
            "నిత్య దైవ పూజలు & సంధ్యావందనం (Daily worship & Sandhyavandanam)",
            "శ్రాద్ధ కర్మలు & తర్పణాలు (Ancestral rites)",
            "శాంతి హోమాలు & జప-తపాలు (Remedial prayers & japa)",
            "జాతకర్మ, నామకరణం, అన్నప్రాశన (Infant life-cycle rites)"
        ]
    },
    "tamil": {
        "status_auspicious": "✨ சுத்த காலம் (மௌட்யம் & கர்த்தரி தோஷங்கள் இல்லை)",
        "status_auspicious_desc": "விவாஹம் உள்ளிட்ட சகல சுப முகூர்த்தங்களுக்கும் உகந்த புண்ணிய காலம்.",
        "guru_moudhyam": "குரு மௌட்யம் (குரு அஸ்தமனம்)",
        "guru_moudhyam_desc": "சூரியன் – குரு சேர்க்கை (11°க்குள்). திருமணம், உபநயனம், கிரகப்பிரவேசம், அடிக்கல் நாட்டுதல் ஆகியவை முற்றிலும் விலக்கத்தக்கவை.",
        "sukra_moudhyam": "சுக்ர மௌட்யம் (சுக்கிர அஸ்தமனம்)",
        "sukra_moudhyam_desc": "சூரியன் – சுக்கிரன் சேர்க்கை (வக்ரகதி 8° / நேர்கதி 10°க்குள்). அனைத்து சுப காரியங்களும் விலக்கப்பட வேண்டும்.",
        "both_moudhyam": "குரு & சுக்கிர இரட்டை மௌட்யம்",
        "both_moudhyam_desc": "குரு, சுக்கிரன் இருவரும் அஸ்தமனமான காலம். சுப காரியங்கள் தவிர்க்கப்பட வேண்டும்.",
        "chinna_kartari": "சின்னக் கத்தரி (பூர்வ கர்த்தரி)",
        "chinna_kartari_desc": "சூரியன் பரணி 3, 4 பாதங்களில் சஞ்சரிக்கும் காலம். புதுமனை புகுதல், மரம் வெட்டுதல் விலக்கத்தக்கவை.",
        "pedda_kartari": "அக்னி கர்த்தரி (பெரிய கத்தரி / கடும் கோடை வெயில்)",
        "pedda_kartari_desc": "சூரியன் கார்த்திகை 4 பாதங்களில் சஞ்சாரம். கடும் சூரிய வெப்பம். புதிய வீடு கட்டுதல், கான்கிரீட் போடுதல், மரம் வெட்டுதல், கிணறு வெட்டுதல் விலக்கத்தக்கவை.",
        "rohini_kartari": "ரோஹிணி கர்த்தரி (உத்தர கத்தரி)",
        "rohini_kartari_desc": "சூரியன் ரோகிணி 1, 2 பாதங்களில் சஞ்சாரம். கர்த்தரி முடியும் நிலை.",
        "vardhakya_warning": "வார்தக்ய தோஷம் (அஸ்தமனத்திற்கு 3 நாட்களுக்கு முன்)",
        "balya_warning": "பால்ய தோஷம் (உதயமான 3 நாட்களுக்குப் பின்)",
        "kartari_title": "அக்னி கர்த்தரி அட்டவணை (Kartari Schedule)",
        "kartari_desc": "சூரியன் பரணி 3-ஆம் பாதம் பிரவேசம் முதல் ரோகிணி 2-ஆம் பாதம் முடியும் வரை கர்த்தரி காலம். புதிய கட்டடப் பணிகள், அடிக்கல் நாட்டுதல், மரம் வெட்டுதல் விலக்கத்தக்கவை.",
        "milestone_chinna_phase": "சின்னக் கத்தரி ஆரம்பம்",
        "milestone_chinna_transit": "சூரியன் பரணி 3-ஆம் பாதம் பிரவேசம் (மேஷம் 20°00')",
        "milestone_chinna_imp": "பூர்வ கர்த்தரி ஆரம்பம் • அடிக்கல் நாட்டுதல் விலக்கத்தக்கது",
        "milestone_pedda_phase": "பெரிய கத்தரி / அக்னி கர்த்தரி ஆரம்பம்",
        "milestone_pedda_transit": "சூரியன் கார்த்திகை 1-ஆம் பாதம் பிரவேசம் (மேஷம் 26°40')",
        "milestone_pedda_imp": "முக்கிய அக்னி கர்த்தரி • கடும் சூரிய வெயில் • அனைத்து கட்டுமானப் பணிகளும் விலக்கப்பட வேண்டும்",
        "milestone_rohini_phase": "ரோகிணி கர்த்தரி ஆரம்பம்",
        "milestone_rohini_transit": "சூரியன் ரோகிணி 1-ஆம் பாதம் பிரவேசம் (ரிஷபம் 10°00')",
        "milestone_rohini_imp": "உத்தர கர்த்தரி நிலை",
        "milestone_end_phase": "கர்த்தரி தியாகம் (முடிவு)",
        "milestone_end_transit": "சூரியன் ரோகிணி 2-ஆம் பாதம் முடிவு (ரிஷபம் 16°40')",
        "milestone_end_imp": "கர்த்தரி முடிவு • வழக்கம்போல கட்டுமானப் பணிகளைத் தொடங்கலாம்",
        "guru_name": "குரு (வியாழன்)",
        "guru_moudhyam_type": "குரு மௌட்யம் (குரு அஸ்தமனம்)",
        "sukra_name": "சுக்கிரன் (பார்க்கவன்)",
        "sukra_moudhyam_type": "சுக்ர மௌட்யம் (சுக்கிர அஸ்தமனம் - வக்ரகதி)",
        "vardhakya_start_text": "அஸ்தமனத்திற்கு 3 நாட்களுக்கு முன்",
        "balya_end_text": "உதயமான 3 நாட்களுக்குப் பின்",
        "guru_prohibition": "திருமணம், உபநயனம், கிரகப்பிரவேசம், அடிக்கல் நாட்டுதல், புதிய விரதங்கள் அனைத்தும் விலக்கத்தக்கவை.",
        "sukra_prohibition": "அனைத்து சுப காரியங்களும் விலக்கத்தக்கவை.",
        "taboos_moudhyam": [
            "திருமணம் (Marriage ceremonies)",
            "பூணூல் / உபநயனம் (Sacred thread ceremony)",
            "புதுமனை புகுவிழா (Housewarming)",
            "அடிக்கல் நாட்டுதல் (Foundation stone laying)",
            "புதிய தெய்வப் பிரதிஷ்டை (Deity consecration)",
            "யாகங்கள் & விரதங்கள் (Vedic sacrifices)"
        ],
        "taboos_kartari": [
            "புதிய வீடு கட்டத் தொடங்குதல் (New house construction)",
            "வீட்டுக் கூரை / கான்கிரீட் போடுதல் (Laying roof slabs)",
            "கிணறு, போர்வெல் தோண்டுதல் (Digging wells / borewells)",
            "மரம் வெட்டுதல் & தோட்டம் அமைத்தல் (Cutting timber / tree plantation)",
            "நெருப்பு சார்ந்த அபாயகரப் பணிகள் (Fire-hazard works)"
        ],
        "permitted_karmas": [
            "நித்ய தெய்வ வழிபாடு & சந்தியாவந்தனம் (Daily worship & Sandhyavandanam)",
            "சிரார்த்த கர்மங்கள் & தர்ப்பணம் (Ancestral rites)",
            "சாந்தி ஹோமங்கள் & ஜப-தபங்கள் (Remedial prayers & japa)",
            "பெயர் சூட்டுதல், அன்னப்ராசனம் (Infant life-cycle rites)"
        ]
    },
    "kannada": {
        "status_auspicious": "✨ ಶುದ್ಧ ಕಾಲ (ಮೌಢ್ಯ & ಕರ್ತರಿ ದೋಷಗಳಿಲ್ಲ)",
        "status_auspicious_desc": "ವಿವಾಹಾದಿ ಸಮಸ್ತ ಶುಭ ಮುಹೂರ್ತಗಳಿಗೆ ಅನುಕೂಲಕರವಾದ ಪವಿತ್ರ ಕಾಲ.",
        "guru_moudhyam": "ಗುರು ಮೌಢ್ಯ (ಬೃಹಸ್ಪತಿ ಅಸ್ತಂಗತ)",
        "guru_moudhyam_desc": "ಸೂರ್ಯ – ಗುರುಗಳ ಸಾಮೀಪ್ಯ (11° ಒಳಗೆ). ವಿವಾಹ, ಉಪನಯನ, ಗೃಹಪ್ರವೇಶ, ಶಂಕುಸ್ಥಾಪನೆಗಳು ಸಂಪೂರ್ಣ ವರ್ಜ್ಯ.",
        "sukra_moudhyam": "ಶುಕ್ರ ಮೌಢ್ಯ (ಭಾರ್ಗವ ಅಸ್ತಂಗತ)",
        "sukra_moudhyam_desc": "ಸೂರ್ಯ – ಶುಕ್ರರ ಸಾಮೀಪ್ಯ (ವಕ್ರಗತಿ 8° / ಋಜುಗತಿ 10° ಒಳಗೆ). ಸಮಸ್ತ ಕಾಮ್ಯ ಶುಭಕಾರ್ಯಗಳು ನಿಷಿದ್ಧ.",
        "both_moudhyam": "ಗುರು & ಶುಕ್ರ ದ್ವಂದ್ವ ಮೌಢ್ಯ",
        "both_moudhyam_desc": "ಗುರು, ಶುಕ್ರರು ಇಬ್ಬರೂ ಅಸ್ತಂಗತರಾದ ಕಾಲ. ಶುಭಕಾರ್ಯಗಳು ತ್ಯಾಜ್ಯ.",
        "chinna_kartari": "ಚಿಕ್ಕ ಕರ್ತರಿ (ಪೂರ್ವ ಕತ್ತರಿ)",
        "chinna_kartari_desc": "ಸೂರ್ಯನು ಭರಣಿ 3, 4 ಪಾದಗಳಲ್ಲಿ ಸಂಚಾರ. ಗೃಹ ಶಂಕುಸ್ಥಾಪನೆ, ಮರ ಕಡಿಯುವುದು ಅಶುಭ.",
        "pedda_kartari": "ಅಗ್ನಿ ಕರ್ತರಿ (ದೊಡ್ಡ ಕತ್ತರಿ / ಪ್ರಚಂಡ ಸೂರ್ಯತಾಪ)",
        "pedda_kartari_desc": "ಸೂರ್ಯನು ಕೃತ್ತಿಕಾ 4 ಪಾದಗಳಲ್ಲಿ ಸಂಚಾರ. ತೀವ್ರ ಸೂರ್ಯತಾಪ. ನೂತನ ಗೃಹಾರಂಭ, ಸ್ಲ್ಯಾಬ್ ಹಾಕುವುದು, ಮರ ಕಡಿಯುವುದು, ಬಾವಿ ತೋಡುವುದು ನಿಷಿದ್ಧ.",
        "rohini_kartari": "ರೋಹಿಣಿ ಕರ್ತರಿ (ಉತ್ತರ ಕತ್ತರಿ)",
        "rohini_kartari_desc": "ಸೂರ್ಯನು ರೋಹಿಣಿ 1, 2 ಪಾದಗಳಲ್ಲಿ ಸಂಚಾರ. ಕರ್ತರಿ ಸಮಾಪ್ತಿ ಹಂತ.",
        "vardhakya_warning": "ವಾರ್ಧಕ್ಯ ದೋಷ (ಅಸ್ತಮಯಕ್ಕೆ 3 ದಿನಗಳ ಮೊದಲು)",
        "balya_warning": "ಬಾಲ್ಯ ದೋಷ (ಉದಯಿಸಿದ 3 ದಿನಗಳ ನಂತರ)",
        "kartari_title": "ಅಗ್ನಿ ಕರ್ತರಿ ನಿರ್ಣಯ ಪಟ್ಟಿ (Kartari Schedule)",
        "kartari_desc": "ಸೂರ್ಯನು ಭರಣಿ 3ನೇ ಪಾದ ಪ್ರವೇಶದಿಂದ ರೋಹಿಣಿ 2ನೇ ಪಾದ ಮುಗಿಯುವವರೆಗೆ ಕರ್ತರಿ. ಗೃಹಾರಂಭ, ಶಂಕುಸ್ಥಾಪನೆ, ಸ್ಲ್ಯಾಬ್, ಮರ ಕಡಿಯುವುದು ನಿಷಿದ್ಧ.",
        "milestone_chinna_phase": "ಚಿಕ್ಕ ಕರ್ತರಿ ಪ್ರಾರಂಭ",
        "milestone_chinna_transit": "ಸೂರ್ಯನು ಭರಣಿ 3ನೇ ಪಾದ ಪ್ರವೇಶ (ಮೇಷ 20°00')",
        "milestone_chinna_imp": "ಪೂರ್ವ ಕರ್ತರಿ ಆರಂಭ • ಶಂಕುಸ್ಥಾಪನೆ ವರ್ಜ್ಯ",
        "milestone_pedda_phase": "ದೊಡ್ಡ ಕರ್ತರಿ / ಅಗ್ನಿ ಕರ್ತರಿ ಪ್ರಾರಂಭ",
        "milestone_pedda_transit": "ಸೂರ್ಯನು ಕೃತ್ತಿಕಾ 1ನೇ ಪಾದ ಪ್ರವೇಶ (ಮೇಷ 26°40')",
        "milestone_pedda_imp": "ಮುಖ್ಯ ಅಗ್ನಿ ಕರ್ತರಿ • ಪ್ರಚಂಡ ಸೂರ್ಯತಾಪ • ಸಮಸ್ತ ಗೃಹ ನಿರ್ಮಾಣ ಕಾರ್ಯಗಳು ನಿಷಿದ್ಧ",
        "milestone_rohini_phase": "ರೋಹಿಣಿ ಕರ್ತರಿ ಪ್ರಾರಂಭ",
        "milestone_rohini_transit": "ಸೂರ್ಯನು ರೋಹಿಣಿ 1ನೇ ಪಾದ ಪ್ರವೇಶ (ವೃಷಭ 10°00')",
        "milestone_rohini_imp": "ಉತ್ತರ ಕರ್ತರಿ ಹಂತ",
        "milestone_end_phase": "ಕರ್ತರಿ ತ್ಯಾಗ (ಸಮಾಪ್ತಿ)",
        "milestone_end_transit": "ಸೂರ್ಯನು ರೋಹಿಣಿ 2ನೇ ಪಾದ ಮುಕ್ತಾಯ (ವೃಷಭ 16°40')",
        "milestone_end_imp": "ಕರ್ತರಿ ವಿಮುಕ್ತಿ • ಯಥಾವಿಧಿಯಾಗಿ ನಿರ್ಮಾಣ ಕಾರ್ಯ ಪ್ರಾರಂಭಿಸಬಹುದು",
        "guru_name": "ಗುರು (ಬೃಹಸ್ಪತಿ)",
        "guru_moudhyam_type": "ಗುರು ಮೌಢ್ಯ (ಬೃಹಸ್ಪತಿ ಅಸ್ತಂಗತ)",
        "sukra_name": "ಶುಕ್ರ (ಭಾರ್ಗವ)",
        "sukra_moudhyam_type": "ಶುಕ್ರ ಮೌಢ್ಯ (ಭಾರ್ಗವ ಅಸ್ತಂಗತ - ವಕ್ರಗತಿ)",
        "vardhakya_start_text": "ಅಸ್ತಮಯಕ್ಕೆ 3 ದಿನಗಳ ಮೊದಲು",
        "balya_end_text": "ಉದಯಿಸಿದ 3 ದಿನಗಳ ನಂತರ",
        "guru_prohibition": "ವಿವಾಹ, ಉಪನಯನ, ಗೃಹಪ್ರವೇಶ, ಶಂಕುಸ್ಥಾಪನೆ, ನೂತನ ವ್ರತಗಳು ಸಮಸ್ತವೂ ನಿಷಿದ್ಧ.",
        "sukra_prohibition": "ಸಮಸ್ತ ಶುಭಕಾರ್ಯಗಳು ನಿಷಿದ್ಧ.",
        "taboos_moudhyam": [
            "ವಿವಾಹ (Marriage ceremonies)",
            "ಉಪನಯನ (Sacred thread ceremony)",
            "ನೂತನ ಗೃಹಪ್ರವೇಶ (Housewarming)",
            "ಗೃಹಾರಂಭ / ಶಂಕುಸ್ಥಾಪನೆ (Foundation stone laying)",
            "ನೂತನ ದೇವತಾ ಪ್ರತಿಷ್ಠೆ (Deity consecration)",
            "ಯಜ್ಞ-ಯಾಗಾದಿಗಳು & ಕಾಮ್ಯ ವ್ರತಗಳು (Vedic sacrifices)"
        ],
        "taboos_kartari": [
            "ನೂತನ ಗೃಹ ನಿರ್ಮಾಣ ಆರಂಭ (New house construction)",
            "ಮನೆಯ ಮೇಲ್ಛಾವಣಿ / ಸ್ಲ್ಯಾಬ್ ಹಾಕುವುದು (Laying roof slabs)",
            "ಬಾವಿ, ಕೊಳವೆಬಾವಿ ತೋಡುವುದು (Digging wells / borewells)",
            "ಮರ ಕಡಿಯುವುದು & ತೋಟಗಾರಿಕೆ ಕೆಲಸ (Cutting timber / tree plantation)",
            "ಅಗ್ನಿ ಸಂಬಂಧಿತ ಕಾಮಗಾರಿಗಳು (Fire-hazard works)"
        ],
        "permitted_karmas": [
            "ನಿತ್ಯ ದೇವ ಪೂಜೆ & ಸಂಧ್ಯಾವಂದನೆ (Daily worship & Sandhyavandanam)",
            "ಶ್ರಾದ್ಧ ಕರ್ಮಗಳು & ತರ್ಪಣ (Ancestral rites)",
            "ಶಾಂತಿ ಹೋಮಗಳು & ಜಪ-ತಪ (Remedial prayers & japa)",
            "ಜಾತಕರ್ಮ, ನಾಮಕರಣ, ಅನ್ನಪ್ರಾಶನ (Infant life-cycle rites)"
        ]
    },
    "devanagari": {
        "status_auspicious": "✨ शुद्ध काल (मौढ्य एवं कर्तरी दोष रहित)",
        "status_auspicious_desc": "विवाहादि समस्त शुभ मुहूर्तों के लिए अनुकूल एवं पवित्र काल।",
        "guru_moudhyam": "गुरु मौढ्य (बृहस्पति अस्त)",
        "guru_moudhyam_desc": "सूर्य – गुरु सामीप्य (11° के भीतर)। विवाह, उपनयन, गृहप्रवेश, शिलान्यास सर्वथा वर्जित।",
        "sukra_moudhyam": "शुक्र मौढ्य (भार्गव अस्त)",
        "sukra_moudhyam_desc": "सूर्य – शुक्र सामीप्य (वक्री 8° / मार्गी 10° के भीतर)। समस्त काम्य शुभ कार्य निषिद्ध।",
        "both_moudhyam": "गुरु एवं शुक्र द्वन्द्व मौढ्य",
        "both_moudhyam_desc": "गुरु और शुक्र दोनों अस्तंगत। समस्त शुभ कार्य त्याज्य।",
        "chinna_kartari": "लघु कर्तरी (पूर्व कर्तरी)",
        "chinna_kartari_desc": "सूर्य का भरणी 3, 4 पाद में गोचर। गृह शिलान्यास, वृक्ष काटना वर्जित।",
        "pedda_kartari": "अग्नि कर्तरी (महा कर्तरी / प्रचण्ड सूर्य ताप)",
        "pedda_kartari_desc": "सूर्य का कृत्तिका 4 पाद में गोचर। प्रचण्ड ताप। नवीन गृह निर्माण, छत डालना, काष्ठ काटना, कूप खनन निषिद्ध।",
        "rohini_kartari": "रोहिणी कर्तरी (उत्तर कर्तरी)",
        "rohini_kartari_desc": "सूर्य का रोहिणी 1, 2 पाद में गोचर। कर्तरी की समाप्ति अवस्था।",
        "vardhakya_warning": "वार्धक्य दोष (अस्त से 3 दिन पूर्व)",
        "balya_warning": "बाल्य दोष (उदय के 3 दिन पश्चात्)",
        "kartari_title": "अग्नि कर्तरी निर्णय सारणी (Kartari Schedule)",
        "kartari_desc": "सूर्य का भरणी 3य पाद प्रवेश से रोहिणी 2य पाद समाप्ति पर्यन्त कर्तरी काल। गृहारम्भ, शिलान्यास, स्लैब, काष्ठ छेदन निषिद्ध।",
        "milestone_chinna_phase": "लघु कर्तरी प्रारम्भ",
        "milestone_chinna_transit": "सूर्य का भरणी 3य पाद प्रवेश (मेष 20°00')",
        "milestone_chinna_imp": "पूर्व कर्तरी प्रारम्भ • शिलान्यास वर्ज्य",
        "milestone_pedda_phase": "महा कर्तरी / अग्नि कर्तरी प्रारम्भ",
        "milestone_pedda_transit": "सूर्य का कृत्तिका 1म पाद प्रवेश (मेष 26°40')",
        "milestone_pedda_imp": "मुख्य अग्नि कर्तरी • प्रचण्ड सूर्यताप • समस्त गृह निर्माण कार्य निषिद्ध",
        "milestone_rohini_phase": "रोहिणी कर्तरी प्रारम्भ",
        "milestone_rohini_transit": "सूर्य का रोहिणी 1म पाद प्रवेश (वृषभ 10°00')",
        "milestone_rohini_imp": "उत्तर कर्तरी अवस्था",
        "milestone_end_phase": "कर्तरी त्याग (समाप्ति)",
        "milestone_end_transit": "सूर्य का रोहिणी 2य पाद पर्यन्त समाप्ति (वृषभ 16°40')",
        "milestone_end_imp": "कर्तरी मुक्ति • यथाविधि निर्माण कार्य प्रारम्भ किए जा सकते हैं",
        "guru_name": "गुरु (बृहस्पति)",
        "guru_moudhyam_type": "गुरु मौढ्य (बृहस्पति अस्त)",
        "sukra_name": "शुक्र (भार्गव)",
        "sukra_moudhyam_type": "शुक्र मौढ्य (भार्गव अस्त - वक्री)",
        "vardhakya_start_text": "अस्त से 3 दिन पूर्व",
        "balya_end_text": "उदय के 3 दिन बाद",
        "guru_prohibition": "विवाह, उपनयन, गृहप्रवेश, शिलान्यास, नवीन व्रत सर्वथा निषिद्ध।",
        "sukra_prohibition": "समस्त शुभ कार्य निषिद्ध।",
        "taboos_moudhyam": [
            "विवाह (Marriage ceremonies)",
            "उपनयन (Sacred thread ceremony)",
            "नवीन गृहप्रवेश (Housewarming)",
            "गृहारम्भ / शिलान्यास (Foundation stone laying)",
            "नवीन देव प्रतिष्ठा (Deity consecration)",
            "यज्ञ-यागादि एवं काम्य व्रत (Vedic sacrifices)"
        ],
        "taboos_kartari": [
            "नवीन गृह निर्माण आरम्भ (New house construction)",
            "छत / स्लैब डालना (Laying roof slabs)",
            "कूप / बोरवेल खनन (Digging wells / borewells)",
            "काष्ठ छेदन एवं उद्यान कार्य (Cutting timber / tree plantation)",
            "अग्नि सम्बन्धी जोखिम कार्य (Fire-hazard works)"
        ],
        "permitted_karmas": [
            "नित्य देव पूजा एवं सन्ध्यावन्दन (Daily worship & Sandhyavandanam)",
            "श्राद्ध कर्म एवं तर्पण (Ancestral rites)",
            "शान्ति होम एवं जप-तप (Remedial prayers & japa)",
            "जातकर्म, नामकरण, अन्नप्राशन (Infant life-cycle rites)"
        ]
    },
    "english": {
        "status_auspicious": "✨ Auspicious Period (Free of Moudhyam & Kartari)",
        "status_auspicious_desc": "Auspicious sidereal alignment suitable for marriages, housewarmings, and sacred ceremonies.",
        "guru_moudhyam": "Guru Moudhyam (Jupiter Combustion / Astangata)",
        "guru_moudhyam_desc": "Jupiter combust within 11° of Sun. Marriages, Upanayanams, house construction, and major auspicious events prohibited.",
        "sukra_moudhyam": "Sukra Moudhyam (Venus Combustion / Astangata)",
        "sukra_moudhyam_desc": "Venus combust within 8°–10° of Sun. All major auspicious ceremonies prohibited.",
        "both_moudhyam": "Dual Moudhyam (Both Jupiter & Venus Combust)",
        "both_moudhyam_desc": "Both major benefic planets are combust. Auspicious karmas strictly avoided.",
        "chinna_kartari": "Chinna Kartari (Minor Summer Ingress)",
        "chinna_kartari_desc": "Sun transits Bharani padas 3 & 4. Foundation ceremonies and cutting wood discouraged.",
        "pedda_kartari": "Agni Kartari / Maha Kartari (Peak Heat Ingress)",
        "pedda_kartari_desc": "Sun transits Krittika nakshatra. Peak solar heat. New building foundations, roof slabs, digging wells, and cutting timber prohibited.",
        "rohini_kartari": "Rohini Kartari (Concluding Kartari Ingress)",
        "rohini_kartari_desc": "Sun transits Rohini padas 1 & 2. Final phase before Kartari Tyagam.",
        "vardhakya_warning": "Vardhakya Period (Infirmity 3 days prior to setting)",
        "balya_warning": "Balya Period (Infancy 3 days following rising)",
        "kartari_title": "Agni Kartari Schedule (Solar Peak Heat Ingress)",
        "kartari_desc": "Kartari spans from Sun entering Bharani 3rd pada until exiting Rohini 2nd pada. New house construction, roof slabs, and cutting timber prohibited.",
        "milestone_chinna_phase": "Chinna Kartari Commencement",
        "milestone_chinna_transit": "Sun enters Bharani 3rd Pada (Aries 20°00')",
        "milestone_chinna_imp": "Preliminary Kartari begins • Laying foundations avoided",
        "milestone_pedda_phase": "Agni Kartari / Maha Kartari Commencement",
        "milestone_pedda_transit": "Sun enters Krittika 1st Pada (Aries 26°40')",
        "milestone_pedda_imp": "Core Agni Kartari • Extreme solar radiation • Building construction strictly prohibited",
        "milestone_rohini_phase": "Rohini Kartari Commencement",
        "milestone_rohini_transit": "Sun enters Rohini 1st Pada (Taurus 10°00')",
        "milestone_rohini_imp": "Concluding Kartari phase",
        "milestone_end_phase": "Kartari Tyagam (Conclusion)",
        "milestone_end_transit": "Sun exits Rohini 2nd Pada (Taurus 16°40')",
        "milestone_end_imp": "Freedom from Kartari • Building construction may resume normally",
        "guru_name": "Jupiter (Guru / Brihaspati)",
        "guru_moudhyam_type": "Guru Moudhyam (Jupiter Combustion)",
        "sukra_name": "Venus (Sukra / Bhargava)",
        "sukra_moudhyam_type": "Sukra Moudhyam (Venus Retrograde Combustion)",
        "vardhakya_start_text": "3 days prior to combustion setting",
        "balya_end_text": "3 days following combustion rising",
        "guru_prohibition": "Marriages, Upanayanams, housewarmings, foundation stone laying, and new vows strictly prohibited.",
        "sukra_prohibition": "All major auspicious ceremonies strictly prohibited.",
        "taboos_moudhyam": [
            "Vivaha (Weddings)",
            "Upanayana (Sacred Thread Ceremony)",
            "Griha Pravesha (Housewarming)",
            "Shankusthapana (Foundation Stone Laying)",
            "Devata Pratishtha (Deity Consecration)",
            "Major Kamya Yagnas"
        ],
        "taboos_kartari": [
            "Starting new building construction",
            "Casting roof slabs",
            "Digging wells or borewells",
            "Cutting timber and planting trees",
            "Fire-sensitive construction activities"
        ],
        "permitted_karmas": [
            "Daily worship and Sandhyavandana",
            "Ancestral Shradh and Tarpanam",
            "Shanti homas and japa",
            "Infant naming and Annaprashana"
        ]
    }
}

# Alias mappings
MOUDYAM_KARTARI_TEXTS["hindi"] = MOUDYAM_KARTARI_TEXTS["devanagari"]
MOUDYAM_KARTARI_TEXTS["sanskrit"] = MOUDYAM_KARTARI_TEXTS["devanagari"]
MOUDYAM_KARTARI_TEXTS["marathi"] = MOUDYAM_KARTARI_TEXTS["devanagari"]
for _l in ["malayalam", "gujarati", "bengali"]:
    if _l not in MOUDYAM_KARTARI_TEXTS:
        MOUDYAM_KARTARI_TEXTS[_l] = MOUDYAM_KARTARI_TEXTS["english"]



def _get_lang_dict(lang: str) -> Dict[str, Any]:
    l_clean = (lang or "telugu").lower().strip()
    return MOUDYAM_KARTARI_TEXTS.get(l_clean, MOUDYAM_KARTARI_TEXTS["telugu"])


def jd_to_local_datetime_str(jd: float, tz_name: str = "Asia/Kolkata") -> str:
    """
    Converts Julian Day float to localized date-time string in target timezone.
    If timezone is not IST, also appends (IST: HH:MM AM/PM) for dual awareness.
    """
    year, month, day, hour_float = swe.revjul(jd)
    whole_hours = int(hour_float)
    minute_float = (hour_float - whole_hours) * 60.0
    whole_minutes = int(minute_float)
    whole_seconds = int((minute_float - whole_minutes) * 60.0)

    dt_utc = datetime(year, month, day, whole_hours, whole_minutes, whole_seconds, tzinfo=timezone.utc)
    try:
        target_tz = ZoneInfo(tz_name)
    except Exception:
        target_tz = ZoneInfo("Asia/Kolkata")

    dt_local = dt_utc.astimezone(target_tz)
    local_str = dt_local.strftime("%Y-%m-%d %I:%M %p %Z")

    if target_tz.key != "Asia/Kolkata":
        dt_ist = dt_utc.astimezone(ZoneInfo("Asia/Kolkata"))
        return f"{local_str} (IST: {dt_ist.strftime('%I:%M %p')})"
    return local_str


def jd_to_ist_datetime_str(jd: float) -> str:
    return jd_to_local_datetime_str(jd, "Asia/Kolkata")


def compute_daily_moudhyam_kartari(jd: float, lang: str = "telugu") -> Dict[str, Any]:
    """
    Computes real-time Moudhyam and Kartari status for a given Julian Day (noon/sunrise).
    """
    texts = _get_lang_dict(lang)

    # 1. Calculate Sidereal Longitudes
    res_s, _ = swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
    res_j, _ = swe.calc_ut(jd, swe.JUPITER, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
    res_v, _ = swe.calc_ut(jd, swe.VENUS, swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED)

    sun_lon = res_s[0] % 360.0
    jup_lon = res_j[0] % 360.0
    ven_lon = res_v[0] % 360.0
    ven_speed = res_v[3]

    # Angular separations modulo 360
    diff_jup = abs(sun_lon - jup_lon)
    if diff_jup > 180.0:
        diff_jup = 360.0 - diff_jup

    diff_ven = abs(sun_lon - ven_lon)
    if diff_ven > 180.0:
        diff_ven = 360.0 - diff_ven

    # 2. Check Kartari
    is_kartari = False
    kartari_type = "NONE"
    kartari_name = None
    kartari_desc = None

    if KARTARI_CHINNA_START <= sun_lon < KARTARI_PEDDA_START:
        is_kartari = True
        kartari_type = "CHINNA_KARTARI"
        kartari_name = texts["chinna_kartari"]
        kartari_desc = texts["chinna_kartari_desc"]
    elif KARTARI_PEDDA_START <= sun_lon < KARTARI_ROHINI_START:
        is_kartari = True
        kartari_type = "PEDDA_KARTARI"
        kartari_name = texts["pedda_kartari"]
        kartari_desc = texts["pedda_kartari_desc"]
    elif KARTARI_ROHINI_START <= sun_lon <= KARTARI_END:
        is_kartari = True
        kartari_type = "ROHINI_KARTARI"
        kartari_name = texts["rohini_kartari"]
        kartari_desc = texts["rohini_kartari_desc"]

    # 3. Check Moudhyam
    is_guru_moudhyam = diff_jup <= GURU_MOUDYAM_LIMIT
    ven_limit = SUKRA_RETROGRADE_LIMIT if ven_speed < 0 else SUKRA_PROGRADE_LIMIT
    is_sukra_moudhyam = diff_ven <= ven_limit

    is_moudhyam = is_guru_moudhyam or is_sukra_moudhyam
    moudhyam_type = "NONE"
    moudhyam_name = None
    moudhyam_desc = None

    if is_guru_moudhyam and is_sukra_moudhyam:
        moudhyam_type = "BOTH"
        moudhyam_name = texts["both_moudhyam"]
        moudhyam_desc = texts["both_moudhyam_desc"]
    elif is_guru_moudhyam:
        moudhyam_type = "GURU_MOUDYAM"
        moudhyam_name = texts["guru_moudhyam"]
        moudhyam_desc = texts["guru_moudhyam_desc"]
    elif is_sukra_moudhyam:
        moudhyam_type = "SUKRA_MOUDYAM"
        moudhyam_name = texts["sukra_moudhyam"]
        moudhyam_desc = texts["sukra_moudhyam_desc"]

    # 4. Synthesize Overall Status & Badge
    if is_moudhyam:
        badge_level = "danger"
        badge_text = f"⚠️ {moudhyam_name}"
        status_title = moudhyam_name
        status_desc = moudhyam_desc
        active_taboos = texts["taboos_moudhyam"]
    elif is_kartari:
        badge_level = "warning" if kartari_type != "PEDDA_KARTARI" else "danger"
        badge_text = f"🔥 {kartari_name}"
        status_title = kartari_name
        status_desc = kartari_desc
        active_taboos = texts["taboos_kartari"]
    else:
        badge_level = "success"
        badge_text = texts["status_auspicious"]
        status_title = texts["status_auspicious"]
        status_desc = texts["status_auspicious_desc"]
        active_taboos = []

    return {
        "is_moudhyam": is_moudhyam,
        "moudhyam_type": moudhyam_type,
        "moudhyam_name": moudhyam_name,
        "moudhyam_description": moudhyam_desc,
        "is_guru_moudhyam": is_guru_moudhyam,
        "guru_angular_distance": round(diff_jup, 2),
        "is_sukra_moudhyam": is_sukra_moudhyam,
        "sukra_angular_distance": round(diff_ven, 2),
        "is_kartari": is_kartari,
        "kartari_type": kartari_type,
        "kartari_name": kartari_name,
        "kartari_description": kartari_desc,
        "sun_sidereal_longitude": round(sun_lon, 2),
        "badge_level": badge_level,  # "danger", "warning", "success"
        "badge_text": badge_text,
        "status_title": status_title,
        "status_description": status_desc,
        "prohibited_karmas": active_taboos,
        "permitted_karmas": texts["permitted_karmas"]
    }


def _find_exact_sun_ingress(target_lon: float, jd_start: float, jd_end: float) -> float:
    low = jd_start
    high = jd_end
    for _ in range(40):
        mid = (low + high) / 2.0
        res, _ = swe.calc_ut(mid, swe.SUN, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
        if res[0] < target_lon:
            low = mid
        else:
            high = mid
    return mid


def _find_exact_moudhyam_boundary(planet: int, limit: float, jd_start: float, jd_end: float, is_entry: bool = True) -> float:
    low = jd_start
    high = jd_end
    for _ in range(40):
        mid = (low + high) / 2.0
        res_s, _ = swe.calc_ut(mid, swe.SUN, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
        res_p, _ = swe.calc_ut(mid, planet, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
        diff = abs(res_s[0] - res_p[0])
        if diff > 180.0:
            diff = 360.0 - diff
        if is_entry:
            if diff > limit:
                low = mid
            else:
                high = mid
        else:
            if diff < limit:
                low = mid
            else:
                high = mid
    return mid


def get_annual_moudhyam_kartari(year: int = 2026, lang: str = "telugu", tz_name: str = "Asia/Kolkata") -> Dict[str, Any]:
    """
    Computes full-year schedule of Moudhyam periods and Kartari ingress milestones
    localized to the requested city's timezone.
    """
    texts = _get_lang_dict(lang)

    # 1. Exact Kartari Milestones for the Year (May-June)
    jd_chinna = _find_exact_sun_ingress(KARTARI_CHINNA_START, swe.julday(year, 5, 1), swe.julday(year, 5, 8))
    jd_pedda = _find_exact_sun_ingress(KARTARI_PEDDA_START, swe.julday(year, 5, 8), swe.julday(year, 5, 16))
    jd_rohini = _find_exact_sun_ingress(KARTARI_ROHINI_START, swe.julday(year, 5, 20), swe.julday(year, 5, 29))
    jd_end = _find_exact_sun_ingress(KARTARI_END, swe.julday(year, 5, 27), swe.julday(year, 6, 5))

    kartari_schedule = {
        "year": year,
        "timezone": tz_name,
        "title": texts.get("kartari_title", "అగ్ని కర్తరి నిర్ణయ పట్టిక (Kartari Schedule)"),
        "chinna_kartari_start": jd_to_local_datetime_str(jd_chinna, tz_name),
        "pedda_kartari_start": jd_to_local_datetime_str(jd_pedda, tz_name),
        "rohini_kartari_start": jd_to_local_datetime_str(jd_rohini, tz_name),
        "kartari_end": jd_to_local_datetime_str(jd_end, tz_name),
        "description": texts.get("kartari_desc", "సూర్యుడు భరణి 3వ పాదం ప్రవేశం మొదలు రోహిణి 2వ పాదం ముగిసే వరకు కర్తరి."),
        "milestones": [
            {
                "phase": texts.get("milestone_chinna_phase", "చిన్న కర్తరి ప్రారంభం"),
                "transit": texts.get("milestone_chinna_transit", "సూర్యుడు భరణి 3వ పాదం ప్రవేశం (మేషం 20°00')"),
                "timing": jd_to_local_datetime_str(jd_chinna, tz_name),
                "importance": texts.get("milestone_chinna_imp", "పూర్వ కర్తరి ఆరంభం • శంకుస్థాపనలు వర్జ్యం")
            },
            {
                "phase": texts.get("milestone_pedda_phase", "పెద్ద కర్తరి / అగ్ని కర్తరి ప్రారంభం"),
                "transit": texts.get("milestone_pedda_transit", "సూర్యుడు కృత్తిక 1వ పాదం ప్రవేశం (మేషం 26°40')"),
                "timing": jd_to_local_datetime_str(jd_pedda, tz_name),
                "importance": texts.get("milestone_pedda_imp", "ముఖ్య అగ్ని కర్తరి • ప్రచండ సూర్యతాపం • సమస్త గృహ నిర్మాణ పనులు నిషిద్ధం")
            },
            {
                "phase": texts.get("milestone_rohini_phase", "రోహిణి కర్తరి ప్రారంభం"),
                "transit": texts.get("milestone_rohini_transit", "సూర్యుడు రోహిణి 1వ పాదం ప్రవేశం (వృషభం 10°00')",),
                "timing": jd_to_local_datetime_str(jd_rohini, tz_name),
                "importance": texts.get("milestone_rohini_imp", "ఉత్తర కర్తరి దశ")
            },
            {
                "phase": texts.get("milestone_end_phase", "కర్తరి త్యాగం (సమాప్తి)"),
                "transit": texts.get("milestone_end_transit", "సూర్యుడు రోహిణి 2వ పాదం ముగింపు (వృషభం 16°40')"),
                "timing": jd_to_local_datetime_str(jd_end, tz_name),
                "importance": texts.get("milestone_end_imp", "కర్తరి విముక్తి • యథావిధిగా నిర్మాణ పనులు ప్రారంభించవచ్చు")
            }
        ]
    }

    # 2. Moudhyam Intervals (Jupiter & Venus) across the Gregorian year
    moudhyam_list = []

    # Check Guru Moudhyam in 2026 (July-August)
    if year == 2026:
        jd_g_start = _find_exact_moudhyam_boundary(swe.JUPITER, GURU_MOUDYAM_LIMIT, swe.julday(year, 7, 10), swe.julday(year, 7, 18), is_entry=True)
        jd_g_end = _find_exact_moudhyam_boundary(swe.JUPITER, GURU_MOUDYAM_LIMIT, swe.julday(year, 8, 10), swe.julday(year, 8, 20), is_entry=False)
        moudhyam_list.append({
            "graha": texts.get("guru_name", "గురుడు (బృహస్పతి)"),
            "graha_code": "jupiter",
            "type": texts.get("guru_moudhyam_type", "గురు మౌఢ్యం (బృహస్పతి అస్తమయం)"),
            "start": jd_to_local_datetime_str(jd_g_start, tz_name),
            "end": jd_to_local_datetime_str(jd_g_end, tz_name),
            "peak_conjunction": "2026-07-29",
            "vardhakya_start": texts.get("vardhakya_start_text", "అస్తమయానికి 3 రోజుల ముందు"),
            "balya_end": texts.get("balya_end_text", "ఉదయించిన 3 రోజుల తర్వాత"),
            "prohibition": texts.get("guru_prohibition", "వివాహం, ఉపనయనం, గృహప్రవేశం, శంకుస్థాపనలు, నూతన వ్రతాలు సమస్తం నిషిద్ధం."),
            "duration_days": 30
        })

        # Check Venus Moudhyam in 2026 (October)
        jd_v_start = _find_exact_moudhyam_boundary(swe.VENUS, SUKRA_RETROGRADE_LIMIT, swe.julday(year, 10, 16), swe.julday(year, 10, 22), is_entry=True)
        jd_v_end = _find_exact_moudhyam_boundary(swe.VENUS, SUKRA_RETROGRADE_LIMIT, swe.julday(year, 10, 25), swe.julday(year, 10, 31), is_entry=False)
        moudhyam_list.append({
            "graha": texts.get("sukra_name", "శుక్రుడు (భార్గవుడు)"),
            "graha_code": "venus",
            "type": texts.get("sukra_moudhyam_type", "శుక్ర మౌఢ్యం (భార్గవ అస్తమయం - వక్రగతి)"),
            "start": jd_to_local_datetime_str(jd_v_start, tz_name),
            "end": jd_to_local_datetime_str(jd_v_end, tz_name),
            "peak_conjunction": "2026-10-24",
            "vardhakya_start": texts.get("vardhakya_start_text", "అస్తమయానికి 3 రోజుల ముందు"),
            "balya_end": texts.get("balya_end_text", "ఉదయించిన 3 రోజుల తర్వాత"),
            "prohibition": texts.get("sukra_prohibition", "సమస్త శుభకార్యములు నిషిద్ధం."),
            "duration_days": 12
        })

    return {
        "year": year,
        "language": lang,
        "timezone": tz_name,
        "kartari_schedule": kartari_schedule,
        "moudhyam_schedule": moudhyam_list,
        "shastric_taboos": {
            "moudhyam_taboos": texts["taboos_moudhyam"],
            "kartari_taboos": texts["taboos_kartari"],
            "permitted_karmas": texts["permitted_karmas"]
        }
    }

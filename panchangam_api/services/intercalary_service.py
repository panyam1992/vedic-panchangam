"""
Intercalary Month (Adhika, Kshaya, Samsarpa, and Amhaspati Masa) Service.

Implements Vedic astronomical calculations from Surya Siddhanta, Vedanga Jyotisha,
and Dharmashastra (Kalamadhava) for:
1. Adhika Masa (Asankranta: 0 solar ingresses between consecutive Amavasyas)
2. Kshaya Masa (Dvi-Sankranta: 2 solar ingresses between consecutive Amavasyas)
3. Samsarpa Masa (First Asankranta in a year containing a Kshaya Masa)
4. Amhaspati Masa (Designation for the conjoined Kshaya Masa)
5. Kaliyuga Intercalary balance (168,152 - 8,718 = 159,034 Net Adhika Masas)
6. Solar-Lunar Drift & Metonic Recurrence Intervals (19, 38, 46, 65, 76, 141 years)
7. Dual-mode support: "surya_siddhanta" (Canonical/Vidwathsabha) and "drik" (Swiss Ephemeris)
"""

import math
from datetime import datetime, date
from typing import Dict, Any, List, Optional, Tuple
import swisseph as swe

from services.localization_service import transliterate_text

# 60 Jovian Samvatsaras (1=Prabhava to 60=Kshaya)
SAMVATSARA_NAMES_TE = [
    "ప్రభవ", "విభవ", "శుక్ల", "ప్రమోదూత", "ప్రజోత్పత్తి", "అంగీరస",
    "శ్రీముఖ", "భావ", "యువ", "ధాత", "ఈశ్వర", "బహుధాన్య",
    "ప్రమాథి", "విక్రమ", "వృష", "చిత్రభాను", "సుభాను", "తారణ",
    "పార్థివ", "వ్యయ", "సర్వజిత్తు", "సర్వధారి", "విరోధి", "వికృతి",
    "ఖర", "నందన", "విజయ", "జయ", "మన్మథ", "దుర్ముఖి",
    "హేవిళంబి", "విళంబి", "వికారి", "శార్వరి", "ప్లవ", "శుభకృతు",
    "శోభకృతు", "క్రోధి", "విశ్వావసు", "పరాభవ", "ప్లవంగ", "కీలక",
    "సౌమ్య", "సాధారణ", "విరోధికృతు", "పరిధావి", "ప్రమాదీచ", "ఆనంద",
    "రాక్షస", "నల", "పింగళ", "కాళయుక్తి", "సిద్ధార్థి", "రౌద్రి",
    "దుర్మతి", "దుందుభి", "రుధిరోద్గారి", "రక్తాక్షి", "క్రోధన", "క్షయ"
]

SAMVATSARA_NAMES_SA = [
    "प्रभव", "विभव", "शुक्ल", "प्रमोदूत", "प्रजोत्पत्ति", "अङ्गीरस",
    "श्रीमुख", "भाव", "युव", "धातृ", "ईश्वर", "बहुधान्य",
    "प्रमाथिन्", "विक्रम", "वृष", "चित्रभानु", "सुभानु", "तारण",
    "पार्थिव", "व्यय", "सर्वजित्", "सर्वधारिन्", "विरोधिन्", "विकृति",
    "खर", "नन्दन", "विजय", "जय", "मन्मथ", "दुर्मुख",
    "हेविलम्बिन्", "विलम्बिन्", "विकारिन्", "शार्वरी", "प्लव", "शुभकृत्",
    "शोभकृत्", "क्रोधन्", "विश्वावसु", "पराभव", "प्लवङ्ग", "कीलक",
    "सौम्य", "साधारण", "विरोधकृत्", "परिधाविन्", "प्रमादिन्", "आनन्द",
    "राक्षस", "नल", "पिङ्गल", "कालयुक्त", "सिद्धार्थिन्", "रौद्र",
    "दुर्मति", "दुन्दुभि", "रुधिरोद्गारिन्", "रक्ताक्ष", "क्रोधन", "क्षय"
]

RASHI_TO_MASA_TE = {
    0: "చైత్ర", 1: "వైశాఖ", 2: "జ్యేష్ఠ", 3: "ఆషాఢ", 4: "శ్రావణ", 5: "భాద్రపద",
    6: "ఆశ్వయుజ", 7: "కార్తిక", 8: "మార్గశిర", 9: "పుష్య", 10: "మాఘ", 11: "ఫాల్గుణ"
}

RASHI_TO_MASA_SA = {
    0: "चैत्र", 1: "वैशाख", 2: "ज्येष्ठ", 3: "आषाढ", 4: "श्रावण", 5: "भाद्रपद",
    6: "आश्वयुज", 7: "कार्तिक", 8: "मार्गशीर्ष", 9: "पौष", 10: "माघ", 11: "फाल्गुन"
}

RASHI_NAMES_TE = [
    "మేషం", "వృషభం", "మిథునం", "కర్కాటకం", "సింహం", "కన్య",
    "తుల", "వృశ్చికం", "ధనుస్సు", "మకరం", "కుంభం", "మీనం"
]

# Canonical Shastric Verses & Metadata
KALAMADHAVA_VERSE_TELUGU = "అసంక్రాంతావేకవర్షౌ ద్వౌచేత్ సంసర్ప ఆదిమః । క్షయమాసో ద్విసంక్రాంతః సచాంహస్పతి సంజ్ఞకః ॥"
KALAMADHAVA_VERSE_DEVANAGARI = "असंक्रान्तावेकवर्षौ द्वौचेत् संसर्प आदिमः । क्षयमासो द्विसंक्रान्तः सचांहस्पति संज्ञकः ॥"
KALAMADHAVA_VERSE_IAST = "asaṅkrāntāv-ekavarṣe dvau cet saṁsarpa ādimaḥ | kṣayamāso dvisaṅkrāntaḥ sa cāmhaspati-saṁjñakaḥ ||"

KSHAYA_RECURRENCE_INTERVALS = [19, 38, 46, 65, 76, 141]


def calculate_solar_lunar_drift() -> Dict[str, Any]:
    """
    Computes solar-lunar calendar drift based on Vedanga Jyotisha and canonical constants.
    """
    solar_year_days = 365.25
    lunar_year_days = 354.0  # 12 * 29.5 approx
    diff_per_year = round(solar_year_days - lunar_year_days, 2)  # ~11.25 / 11 days
    months_for_adhika = 32.5  # approx 32.5 solar months for 1 full lunar month accumulation

    return {
        "solar_year_days": solar_year_days,
        "lunar_year_days": lunar_year_days,
        "diff_per_year_days": 11,
        "exact_diff_per_year_days": diff_per_year,
        "accumulation_3_years_days": 33,
        "months_for_adhika_masa": months_for_adhika,
        "vedanga_jyotisha_rule": {
            "solar_years": 5,
            "solar_months": 60,
            "lunar_months": 62,
            "adhika_masas_in_5_years": 2,
            "principle": "పంచసంవత్సరాత్మక యుగం (In a 5-year Yuga: 60 Solar Months = 62 Lunar Months, yielding 2 Adhika Masas)"
        }
    }


def get_kaliyuga_epoch_statistics() -> Dict[str, Any]:
    """
    Returns canonical Kaliyuga (432,000 years) intercalary statistics from Surya Siddhanta.
    Net Adhika Masas = Total Adhika Masas (168,152) - Total Kshaya Masas (8,718) = 159,034.
    """
    return {
        "kaliyuga_duration_years": 432000,
        "total_adhika_masas": 168152,
        "total_kshaya_masas": 8718,
        "net_adhika_masas": 159034,
        "formula": "Net Adhika Masas = Total Intercalary Months (168,152) - Total Kshaya Masas (8,718) = 159,034",
        "ratio_approx": "సుమారు ప్రతి 49.5 సంవత్సరాలకు ఒక క్షయ మాసపు సంభావ్యత గణిత పద్ధతిలో ఉంటుంది"
    }


def _get_moon_sun_diff(jd: float) -> float:
    """Returns Moon Longitude - Sun Longitude (modulo 360)."""
    swe.set_ephe_path('')
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    sun = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)[0][0]
    moon = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0][0]
    return (moon - sun) % 360.0


def _find_amavasya(jd_approx: float) -> float:
    """Finds exact moment of Amavasya conjunction using binary search."""
    t0 = jd_approx - 2.5
    t1 = jd_approx + 2.5
    for _ in range(50):
        t_mid = (t0 + t1) / 2.0
        d = _get_moon_sun_diff(t_mid)
        if d > 180.0:
            d -= 360.0
        if abs(d) < 1e-6:
            return t_mid
        if d < 0:
            t0 = t_mid
        else:
            t1 = t_mid
    return (t0 + t1) / 2.0


def _get_sun_rashi(jd: float) -> int:
    """Returns Sidereal Rashi (0=Mesha to 11=Meena)."""
    sun_lon = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)[0][0]
    return int(sun_lon // 30) % 12


def _count_solar_ingresses(jd_start: float, jd_end: float) -> Tuple[int, List[int]]:
    """
    Counts number of solar ingresses (Sankrantis) between two JD instants.
    Returns (count, [entered_rashi_indices]).
    """
    step = 0.05
    t = jd_start
    prev_rashi = _get_sun_rashi(t)
    entered_rashis = []
    
    while t <= jd_end:
        curr_rashi = _get_sun_rashi(t)
        if curr_rashi != prev_rashi:
            entered_rashis.append(curr_rashi)
            prev_rashi = curr_rashi
        t += step
        
    return len(entered_rashis), entered_rashis


def calculate_amanta_months_for_civil_year(year: int) -> List[Dict[str, Any]]:
    """
    Computes all Amanta lunar months beginning in or covering the civil year.
    Each month has:
    - start_jd, end_jd, start_date, end_date
    - ingress_count: 0 (Asankranta), 1 (Sankranta), 2 (Dvi-Sankranta)
    - entered_rashis
    - preliminary_masa_index
    """
    jd_start = swe.julday(year, 1, 1, 0)
    jd_end = swe.julday(year + 1, 2, 15, 0)
    
    jd = jd_start
    amavasyas = []
    
    # Pre-align to previous Amavasya
    ama_first = _find_amavasya(jd)
    if ama_first > jd_start:
        ama_first = _find_amavasya(jd_start - 29.5)
    amavasyas.append(ama_first)
    jd = ama_first + 25.0
    
    while jd < jd_end:
        diff = _get_moon_sun_diff(jd)
        if diff > 350.0 or diff < 10.0:
            ama = _find_amavasya(jd)
            if ama - amavasyas[-1] > 20.0:
                amavasyas.append(ama)
                jd = ama + 25.0
                continue
        jd += 0.5

    months = []
    for i in range(len(amavasyas) - 1):
        m_s = amavasyas[i]
        m_e = amavasyas[i + 1]
        
        y_s, m_s_num, d_s, _ = swe.revjul(m_s)
        y_e, m_e_num, d_e, _ = swe.revjul(m_e)
        
        count, entered = _count_solar_ingresses(m_s, m_e)
        
        # Base Rashi at month start
        start_rashi = _get_sun_rashi(m_s)
        
        # Samvatsara index for month:
        # Ugadi is usually March/April (Mesha ingress or Chaitra Amavasya)
        # Year 2026 Ugadi is Parabhava (#40)
        # Approximate Samvatsara:
        samvatsara_id = (y_s - 1567) % 60 + 1
        if m_s_num < 3 or (m_s_num == 3 and d_s < 20):
            # Still in previous Jovian/Ugadi year
            samvatsara_id = (samvatsara_id - 2) % 60 + 1
            
        months.append({
            "index": i + 1,
            "start_jd": m_s,
            "end_jd": m_e,
            "start_date": f"{y_s:04d}-{m_s_num:02d}-{int(d_s):02d}",
            "end_date": f"{y_e:04d}-{m_e_num:02d}-{int(d_e):02d}",
            "sankranti_count": count,
            "entered_rashis": entered,
            "start_rashi": start_rashi,
            "samvatsara_id": samvatsara_id,
            "samvatsara_name_te": SAMVATSARA_NAMES_TE[samvatsara_id - 1],
            "samvatsara_name_sa": SAMVATSARA_NAMES_SA[samvatsara_id - 1]
        })
        
    return months


def get_intercalary_months_range(
    start_year: int = 2026,
    end_year: int = 2036,
    system: str = "surya_siddhanta",
    lang: str = "telugu"
) -> List[Dict[str, Any]]:
    """
    Computes all Adhika, Kshaya, and Samsarpa months between start_year and end_year.
    Under 'surya_siddhanta', incorporates the canonical Kalamadhava resolution
    and the Telangana Vidwathsabha (2026) resolution:
    - 2026: Adhika Jyeshtha
    - 2028-2029 (Keelaka): Samsarpa Kartika (Adhika) & Margashirsha-Pushya Kshaya (Amhaspati)
    - 2029: Adhika Chaitra
    - 2031: Adhika Bhadrapada
    - 2034: Adhika Ashadha
    """
    results = []
    
    # Multilingual description helpers
    def _get_adhika_desc(l: str) -> str:
        d = {
            "telugu": "ఒక చాంద్రమాసంలో సూర్యుని రాశి ప్రవేశం జరగలేదు (0 సంక్రాంతి - అసంక్రాంతం).",
            "tamil": "ஒரு சந்திர மாதத்தில் சூரியனின் ராசிப் பெயர்ச்சி நிகழவில்லை (0 சங்கராந்தி - அசங்கிராந்தம்).",
            "kannada": "ಒಂದು ಚಾಂದ್ರಮಾಸದಲ್ಲಿ ಸೂರ್ಯನ ರಾಶಿ ಪ್ರವೇಶವಿಲ್ಲ (0 ಸಂಕ್ರಾಂತಿ - ಅಸಂಕ್ರಾಂತ).",
            "devanagari": "एक चान्द्रमास में कोई सूर्य संक्रान्ति नहीं (0 संक्रान्ति - असंक्रान्त)।",
            "english": "No solar ingress occurs during this lunar month (0 Sankrantis - Asankranta)."
        }
        return d.get(l, d["english"])

    def _get_samsarpa_desc(l: str) -> str:
        d = {
            "telugu": "క్షయమాసానికి ముందు వచ్చే అసంక్రాంత మాసం. శాస్త్రప్రకారం నిత్య, నైమిత్తిక కర్మలు చేయదగినవి.",
            "tamil": "க்ஷய மாதத்திற்கு முன் வரும் அசங்கிராந்த மாதம். சாஸ்திரப்படி நித்ய, நைமித்திக கர்மங்கள் செய்யத்தக்கவை.",
            "kannada": "ಕ್ಷಯಮಾಸಕ್ಕಿಂತ ಮೊದಲು ಬರುವ ಅಸಂಕ್ರಾಂತ ಮಾಸ. ನಿತ್ಯ, ನೈಮಿತ್ತಿಕ ಕರ್ಮಗಳು ಮಾಡಬಹುದು.",
            "devanagari": "क्षय मास से पूर्व आने वाला असंक्रान्त मास। नित्य एवं नैमित्तिक कर्म ग्राह्य।",
            "english": "Intercalary month preceding a Kshaya Masa. Regular Vedic and seasonal rites permitted."
        }
        return d.get(l, d["english"])

    def _get_kshaya_desc(l: str) -> str:
        d = {
            "telugu": "ఒకే చాంద్రమాసంలో ధనుస్సు మరియు మకర సంక్రాంతులు రెండూ (2 సంక్రాంతులు) సంభవిస్తాయి. శుభకార్యాలు వర్జ్యం.",
            "tamil": "ஒரே சந்திர மாதத்தில் இரண்டு சூரிய சங்கராந்திகள் நிகழ்கின்றன (துவிசங்கிராந்தம்). சுபகாரியங்கள் விலக்கத்தக்கவை.",
            "kannada": "ಒಂದೇ ಚಾಂದ್ರಮಾಸದಲ್ಲಿ ಎರಡು ಸೂರ್ಯ ಸಂಕ್ರಾಂತಿಗಳು ಸಂಭವಿಸುತ್ತವೆ. ಶುಭಕಾರ್ಯಗಳು ವರ್ಜ್ಯ.",
            "devanagari": "एक ही चान्द्रमास में दो सूर्य संक्रान्तियां (द्विसंक्रान्त)। शुभ कार्य वर्जित।",
            "english": "Two solar ingresses occur within a single lunar month (Dvi-Sankranta). Auspicious ceremonies prohibited."
        }
        return d.get(l, d["english"])

    asankranta_verse = "సంక్రాంతి వర్జితో మాసః అధిమాసః ప్రకీర్తితః" if lang == "telugu" else transliterate_text("संक्रान्ति वर्जितो मासः अधिमासः प्रकीर्तितः", lang)
    kalamadhava_verse = KALAMADHAVA_VERSE_TELUGU if lang == "telugu" else (KALAMADHAVA_VERSE_DEVANAGARI if lang in ["devanagari", "hindi", "sanskrit"] else (transliterate_text(KALAMADHAVA_VERSE_DEVANAGARI, lang) if lang in ["tamil", "kannada", "malayalam", "bengali", "gujarati"] else KALAMADHAVA_VERSE_IAST))

    # Scan year by year
    for yr in range(start_year, end_year + 1):
        # 1. Surya Siddhanta / Vidwathsabha Canonical Mode
        if system.lower() in ["surya_siddhanta", "canonical", "shastric", "purva"]:
            # Year 2026: Adhika Jyeshtha
            if yr == 2026:
                results.append({
                    "year": 2026,
                    "samvatsara_name": transliterate_text("पराभव", lang),
                    "samvatsara_name_telugu": "శ్రీ పరాభవ",
                    "masa_name": transliterate_text("ज्येष्ठ", lang),
                    "masa_name_telugu": "జ్యేష్ఠ మాసం",
                    "full_display_name": "అధిక జ్యేష్ఠ మాసం" if lang == "telugu" else transliterate_text("अधिक ज्येष्ठ मास", lang),
                    "classification": "ADHIKA",
                    "classification_name": "అధిక మాసం" if lang == "telugu" else transliterate_text("अधिक मास", lang),
                    "sankranti_count": 0,
                    "start_date": "2026-05-17",
                    "end_date": "2026-06-15",
                    "description": _get_adhika_desc(lang),
                    "shastra_verse": asankranta_verse
                })
            # Year 2028: Sri Keelaka Nama Samvatsaram (Samsarpa Kartika & Margashirsha-Pushya Kshaya)
            elif yr == 2028:
                # Samsarpa Kartika
                results.append({
                    "year": 2028,
                    "samvatsara_name": transliterate_text("कीलक", lang),
                    "samvatsara_name_telugu": "శ్రీ కీలక",
                    "masa_name": transliterate_text("कार्तिक", lang),
                    "masa_name_telugu": "కార్తిక మాసం",
                    "full_display_name": "సంసర్ప కార్తిక మాసం" if lang == "telugu" else transliterate_text("संसर्प कार्तिक मास", lang),
                    "classification": "SAMSARPA",
                    "classification_name": "సంసర్ప మాసం (ప్రథమ అధిక మాసం)" if lang == "telugu" else transliterate_text("संसर्प मास (प्रथम अधिक)", lang),
                    "sankranti_count": 0,
                    "start_date": "2028-10-18",
                    "end_date": "2028-11-16",
                    "description": _get_samsarpa_desc(lang),
                    "shastra_verse": kalamadhava_verse
                })
                # Margashirsha-Pushya Yugalibhuta Kshaya (Amhaspati)
                results.append({
                    "year": 2028,
                    "samvatsara_name": transliterate_text("कीलक", lang),
                    "samvatsara_name_telugu": "శ్రీ కీలక",
                    "masa_name": transliterate_text("मार्गशीर्ष-पौष", lang),
                    "masa_name_telugu": "మార్గశిర – పుష్య",
                    "full_display_name": "మార్గశిర–పుష్య యుగళీభూత అంహస్పతి (క్షయ మాసం)" if lang == "telugu" else transliterate_text("मार्गशीर्ष–पौष युगलीभूत अंहस्पति (क्षय मास)", lang),
                    "classification": "KSHAYA",
                    "classification_name": "క్షయ మాసం (ద్విసంక్రాంత అంహస్పతి)" if lang == "telugu" else transliterate_text("क्षय मास (अंहस्पति)", lang),
                    "sankranti_count": 2,
                    "conjoined_months": ["Margashirsha", "Pushya"],
                    "start_date": "2028-11-17",
                    "end_date": "2028-12-16",
                    "description": _get_kshaya_desc(lang),
                    "shastra_verse": kalamadhava_verse
                })
            # Year 2029: Adhika Chaitra
            elif yr == 2029:
                results.append({
                    "year": 2029,
                    "samvatsara_name": transliterate_text("सौम्य", lang),
                    "samvatsara_name_telugu": "శ్రీ సౌమ్య",
                    "masa_name": transliterate_text("चैत्र", lang),
                    "masa_name_telugu": "చైత్ర మాసం",
                    "full_display_name": "అధిక చైత్ర మాసం" if lang == "telugu" else transliterate_text("अधिक चैत्र मास", lang),
                    "classification": "ADHIKA",
                    "classification_name": "అధిక మాసం" if lang == "telugu" else transliterate_text("अधिक मास", lang),
                    "sankranti_count": 0,
                    "start_date": "2029-03-15",
                    "end_date": "2029-04-13",
                    "description": _get_adhika_desc(lang),
                    "shastra_verse": asankranta_verse
                })
            # Year 2031: Adhika Bhadrapada
            elif yr == 2031:
                results.append({
                    "year": 2031,
                    "samvatsara_name": transliterate_text("विरोधकृत्", lang),
                    "samvatsara_name_telugu": "శ్రీ విరోధికృత్",
                    "masa_name": transliterate_text("भाद्रपद", lang),
                    "masa_name_telugu": "భాద్రపద మాసం",
                    "full_display_name": "అధిక భాద్రపద మాసం" if lang == "telugu" else transliterate_text("अधिक भाद्रपद मास", lang),
                    "classification": "ADHIKA",
                    "classification_name": "అధిక మాసం" if lang == "telugu" else transliterate_text("अधिक मास", lang),
                    "sankranti_count": 0,
                    "start_date": "2031-08-18",
                    "end_date": "2031-09-16",
                    "description": _get_adhika_desc(lang),
                    "shastra_verse": asankranta_verse
                })
            # Year 2034: Adhika Ashadha
            elif yr == 2034:
                results.append({
                    "year": 2034,
                    "samvatsara_name": transliterate_text("आनन्द", lang),
                    "samvatsara_name_telugu": "శ్రీ ఆనంద",
                    "masa_name": transliterate_text("आषाढ", lang),
                    "masa_name_telugu": "ఆషాఢ మాసం",
                    "full_display_name": "అధిక ఆషాఢ మాసం" if lang == "telugu" else transliterate_text("अधिक आषाढ मास", lang),
                    "classification": "ADHIKA",
                    "classification_name": "అధిక మాసం" if lang == "telugu" else transliterate_text("अधिक मास", lang),
                    "sankranti_count": 0,
                    "start_date": "2034-06-16",
                    "end_date": "2034-07-15",
                    "description": _get_adhika_desc(lang),
                    "shastra_verse": asankranta_verse
                })

        # 2. Drik Ganitha (Swiss Ephemeris Astronomical Mode)
        else:
            m_list = calculate_amanta_months_for_civil_year(yr)
            for m in m_list:
                # Check for year match
                if not m["start_date"].startswith(str(yr)):
                    continue
                sc = m["sankranti_count"]
                if sc == 0:
                    rashi = m["start_rashi"]
                    masa_name_sa = RASHI_TO_MASA_SA.get(rashi, "अज्ञात")
                    masa_user = transliterate_text(masa_name_sa, lang)
                    results.append({
                        "year": yr,
                        "samvatsara_name": transliterate_text(m["samvatsara_name_sa"], lang),
                        "samvatsara_name_telugu": m["samvatsara_name_te"],
                        "masa_name": masa_user,
                        "masa_name_telugu": f"{RASHI_TO_MASA_TE.get(rashi, '')} మాసం",
                        "full_display_name": f"అధిక {RASHI_TO_MASA_TE.get(rashi, '')} మాసం" if lang == "telugu" else transliterate_text(f"अधिक {masa_name_sa} मास", lang),
                        "classification": "ADHIKA",
                        "classification_name": "అధిక మాసం" if lang == "telugu" else transliterate_text("अधिक मास", lang),
                        "sankranti_count": 0,
                        "start_date": m["start_date"],
                        "end_date": m["end_date"],
                        "description": "ఈ చాంద్రమాసంలో ఎటువంటి సూర్య సంక్రమణం లేదు (0 సంక్రాంతి).",
                        "shastra_verse": "సంక్రాంతి వర్జితో మాసః అధిమాసః ప్రకీర్తితః"
                    })
                elif sc == 2:
                    entered = m["entered_rashis"]
                    m1 = RASHI_TO_MASA_SA.get(entered[0], "")
                    m2 = RASHI_TO_MASA_SA.get(entered[1], "")
                    dual_name = f"{m1}-{m2}"
                    results.append({
                        "year": yr,
                        "samvatsara_name": transliterate_text(m["samvatsara_name_sa"], lang),
                        "samvatsara_name_telugu": m["samvatsara_name_te"],
                        "masa_name": transliterate_text(dual_name, lang),
                        "masa_name_telugu": f"{RASHI_TO_MASA_TE.get(entered[0], '')}-{RASHI_TO_MASA_TE.get(entered[1], '')}",
                        "full_display_name": f"{RASHI_TO_MASA_TE.get(entered[0], '')}-{RASHI_TO_MASA_TE.get(entered[1], '')} క్షయ మాసం",
                        "classification": "KSHAYA",
                        "classification_name": "క్షయ మాసం (ద్విసంక్రాంతం)",
                        "sankranti_count": 2,
                        "conjoined_months": [m1, m2],
                        "start_date": m["start_date"],
                        "end_date": m["end_date"],
                        "description": "ఒకే చాంద్రమాసంలో రెండు సూర్య సంక్రాంతులు సంభవించాయి.",
                        "shastra_verse": KALAMADHAVA_VERSE_TELUGU if lang == "telugu" else KALAMADHAVA_VERSE_DEVANAGARI
                    })

    return results


def get_intercalary_status_for_date(
    jd: float,
    system: str = "surya_siddhanta",
    lang: str = "telugu"
) -> Dict[str, Any]:
    """
    Determines whether a specific Julian Day falls in an Adhika, Kshaya, Samsarpa, or Nija month.
    """
    y, m, d, _ = swe.revjul(jd)
    date_str = f"{y:04d}-{m:02d}-{int(d):02d}"
    
    # Check against known canonical intercalary windows in Surya Siddhanta
    if system.lower() in ["surya_siddhanta", "canonical", "shastric", "purva"]:
        # 2026 Adhika Jyeshtha: 2026-05-17 to 2026-06-15
        if "2026-05-17" <= date_str <= "2026-06-15":
            return {
                "classification": "ADHIKA",
                "is_adhika": True,
                "is_kshaya": False,
                "is_samsarpa": False,
                "sankranti_count": 0,
                "prefix": "అధిక " if lang == "telugu" else transliterate_text("अधिक ", lang),
                "badge_label": "అధిక మాసం" if lang == "telugu" else transliterate_text("अधिक मास", lang),
                "shastra_name": "మలమాసం / అధిక జ్యేష్ఠ మాసం" if lang == "telugu" else transliterate_text("मलमास / अधिक ज्येष्ठ मास", lang)
            }
        # 2028 Samsarpa Kartika: 2028-10-18 to 2028-11-16
        if "2028-10-18" <= date_str <= "2028-11-16":
            return {
                "classification": "SAMSARPA",
                "is_adhika": True,
                "is_kshaya": False,
                "is_samsarpa": True,
                "sankranti_count": 0,
                "prefix": "సంసర్ప " if lang == "telugu" else transliterate_text("संसर्प ", lang),
                "badge_label": "సంసర్ప మాసం" if lang == "telugu" else transliterate_text("संसर्प मास", lang),
                "shastra_name": "సంసర్ప కార్తిక మాసం (ప్రథమ అధిక)" if lang == "telugu" else transliterate_text("संसर्प कार्तिक मास (प्रथम अधिक)", lang)
            }
        # 2028 Margashirsha-Pushya Kshaya: 2028-11-17 to 2028-12-16
        if "2028-11-17" <= date_str <= "2028-12-16":
            return {
                "classification": "KSHAYA",
                "is_adhika": False,
                "is_kshaya": True,
                "is_samsarpa": False,
                "sankranti_count": 2,
                "prefix": "క్షయ " if lang == "telugu" else transliterate_text("क्षय ", lang),
                "badge_label": "క్షయ మాసం" if lang == "telugu" else transliterate_text("क्षय मास (अंहस्पति)", lang),
                "shastra_name": "మార్గశిర–పుష్య యుగళీభూత అంహస్పతి మాసం" if lang == "telugu" else transliterate_text("मार्गशीर्ष–पौष युगलीभूत अंहस्पति मास", lang)
            }
        # 2029 Adhika Chaitra: 2029-03-15 to 2029-04-13
        if "2029-03-15" <= date_str <= "2029-04-13":
            return {
                "classification": "ADHIKA",
                "is_adhika": True,
                "is_kshaya": False,
                "is_samsarpa": False,
                "sankranti_count": 0,
                "prefix": "అధిక " if lang == "telugu" else transliterate_text("अधिक ", lang),
                "badge_label": "అధిక మాసం" if lang == "telugu" else transliterate_text("अधिक मास", lang),
                "shastra_name": "అధిక చైత్ర మాసం" if lang == "telugu" else transliterate_text("अधिक चैत्र मास", lang)
            }

    # Default Normal Month (Nija Masa)
    return {
        "classification": "NIJA",
        "is_adhika": False,
        "is_kshaya": False,
        "is_samsarpa": False,
        "sankranti_count": 1,
        "prefix": "నిజ " if lang == "telugu" else transliterate_text("निज ", lang),
        "badge_label": "సాధారణ మాసం" if lang == "telugu" else transliterate_text("शुद्ध मास", lang),
        "shastra_name": "నిజ మాసం (శుద్ధ మాసం)" if lang == "telugu" else transliterate_text("निज मास (शुद्ध मास)", lang)
    }


def get_intercalary_theory_and_formulas(lang: str = "telugu") -> Dict[str, Any]:
    """
    Returns complete canonical treatises, mathematical formulas, and Dharma Shastra rules.
    """
    drift = calculate_solar_lunar_drift()
    kali = get_kaliyuga_epoch_statistics()

    return {
        "title": "అధిక మాసం & క్షయ మాస ఖగోళ-ధర్మశాస్త్ర విజ్ఞానం" if lang == "telugu" else transliterate_text("अधिक मास एवं क्षय मास खगोल-धर्मशास्त्र विज्ञान", lang),
        "principles": [
            {
                "name": "అధిక మాసం (Asankranta Criterion)",
                "formula": "Number of Solar Ingresses (Sankrantis) = 0",
                "shastra_verse": "సంక్రాంతి వర్జితో మాసః అధిమాసః ప్రకీర్తితః",
                "explanation": "ఒక అమావాస్య నుండి తర్వాతి అమావాస్య మధ్య కాలంలో సూర్యుడు ఏ రాశి లోకీ ప్రవేశించకపోతే అది అధిక మాసం (మలమాసం)."
            },
            {
                "name": "సాధారణ మాసం (Sankranta Criterion)",
                "formula": "Number of Solar Ingresses (Sankrantis) = 1",
                "shastra_verse": "ఏక సంక్రాంతి సంయుక్తః శుద్ధ మాసః ప్రకీర్తితః",
                "explanation": "ఒక చాంద్రమాసంలో ఖచ్చితంగా ఒకే సూర్య సంక్రమణం సంభవిస్తే అది నిజ/శుద్ధ మాసం."
            },
            {
                "name": "క్షయ మాసం (Dvi-Sankranta Criterion)",
                "formula": "Number of Solar Ingresses (Sankrantis) = 2",
                "shastra_verse": "ద్వి సంక్రాంతి సమో మాసః క్షయమాసః ప్రకీర్తితః",
                "explanation": "ఒకే చాంద్రమాసంలో సూర్యుని రెండు రాశి ప్రవేశాలు (2 సంక్రాంతులు) సంభవిస్తే అది క్షయ మాసం (అంహస్పతి)."
            }
        ],
        "kalamadhava_canonical_rule": {
            "verse_telugu": KALAMADHAVA_VERSE_TELUGU,
            "verse_devanagari": KALAMADHAVA_VERSE_DEVANAGARI,
            "verse_iast": KALAMADHAVA_VERSE_IAST,
            "rules": [
                "ఒకే సంవత్సరంలో రెండు అసంక్రాంత మాసాలు (అధిక మాసాలు) వస్తే, మొదటి దానిని 'సంసర్పం' అంటారు.",
                "మధ్యలో వచ్చే ద్విసంక్రాంత మాసమే 'క్షయ మాసం' లేదా 'అంహస్పతి మాసం'.",
                "రెండవ అసంక్రాంత మాసమే నిజమైన 'అధిక మాసం' అవుతుంది.",
                "సంసర్ప మాసంలో నిత్య-నైమిత్తిక కర్మలు చేయవచ్చు; అంహస్పతి (క్షయ) మాసంలో వివాహాది శుభకార్యాలు వర్జ్యం."
            ]
        },
        "solar_lunar_drift": drift,
        "kaliyuga_epoch_balance": kali,
        "kshaya_recurrence_intervals": {
            "cycle_years": KSHAYA_RECURRENCE_INTERVALS,
            "derivations": [
                "38 = 2 × 19",
                "46 = 38 + 8",
                "65 = 46 + 19",
                "76 = 4 × 19",
                "141 = 65 + 76"
            ],
            "note": "క్షయ మాసాలు మెటోనిక్ సౌర-చాంద్ర అనుసంధాన చక్రాల ఆధారంగా మాత్రమే 19, 38, 46, 65, 76, లేదా 141 సంవత్సరాల వ్యవధులలో సంభవిస్తాయి."
        }
    }

"""
Worldwide Solar and Lunar Eclipses Engine (సూర్య & చంద్ర గ్రహణ దర్శిని).
Supports global city-specific calculations (మీ నగరంలో గ్రహణ సమయాలు):
- Local beginning (Sparsha), peak (Madhya), and ending (Moksha) times in city's timezone (e.g. America/Chicago, Asia/Kolkata).
- Total eclipse duration in hours and minutes.
- City visibility determination (మీ నగరంలో కనిపిస్తుంది / కనిపించదు).
- Sutaka timings (12 hours before for Solar, 9 hours before for Lunar, ending at Moksha).
- Eclipse category: పాక్షికం (Partial), సంపూర్ణం (Total), కంకణాకారం (Annular), ఛాయ/ఉపచ్ఛాయ (Penumbral).
- Sidereal Rashi and Nakshatra affected.
- 12-Rashi astrological impacts (శుభ, మధ్యమ, అనిష్ట ఫలితాలు).
- Classical Moksha Puja, Shanti, and pregnant women guidelines.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
import swisseph as swe

from jyotishyam.services.ephemeris_service import calculate_lagna_and_houses, calculate_planet_positions
from jyotishyam.services.kundali_calculator import enrich_lagna_details, enrich_planets, build_charts

# Accurate Astronomical Data for Worldwide Eclipses (2024 - 2028)
ECLIPSES_DATABASE = {
    2024: [
        {
            "id": "ecl_2024_01",
            "type": "చంద్ర గ్రహణం (Lunar Eclipse)",
            "sub_type": "ఉపచ్ఛాయ చంద్ర గ్రహణం (Penumbral Lunar Eclipse)",
            "category": "ఛాయ / ఉపచ్ఛాయ (Penumbral)",
            "date": "2024-03-25",
            "date_formatted": "25 మార్చి 2024 (సోమవారం)",
            "rashi_name_te": "కన్య రాశి",
            "nakshatra_name_te": "ఉత్తర ఫల్గుణి / హస్త",
            "utc_sparsha_iso": "2024-03-25T04:53:00Z",
            "utc_madhya_iso": "2024-03-25T07:12:00Z",
            "utc_moksha_iso": "2024-03-25T09:32:00Z",
            "utc_sparsha": "04:53 UTC",
            "utc_madhya": "07:12 UTC",
            "utc_moksha": "09:32 UTC",
            "ist_sparsha": "10:23 AM IST",
            "ist_madhya": "12:42 PM IST",
            "ist_moksha": "03:02 PM IST",
            "global_visibility": "ఉత్తర అమెరికా, దక్షిణ అమెరికా, పసిఫిక్, అట్లాంటిక్",
            "visible_in_india": False,
            "visible_regions": ["north_america", "south_america", "us", "usa", "texas", "mexico", "canada"],
            "visibility_summary_te": "అమెరికా (USA), కెనడా మరియు దక్షిణ అమెరికా దేశాలలో రాత్రి వేళ స్పష్టంగా కనిపిస్తుంది. భారతదేశంలో పగటి వేళ అగుటచే కనిపించదు.",
            "rashi_impacts": {
                "subha": ["వృషభం", "కర్కాటకం", "ధనుస్సు", "మకరం"],
                "madhyama": ["మేషం", "మిథునం", "తుల", "కుంభం"],
                "arishta": ["కన్య (గ్రహణ రాశి)", "సింహం", "వృశ్చికం", "మీనం"]
            }
        },
        {
            "id": "ecl_2024_02",
            "type": "సూర్య గ్రహణం (Solar Eclipse)",
            "sub_type": "సంపూర్ణ సూర్య గ్రహణం (Great North American Total Solar Eclipse)",
            "category": "సంపూర్ణం (Total)",
            "date": "2024-04-08",
            "date_formatted": "08 ఏప్రిల్ 2024 (సోమవారం)",
            "rashi_name_te": "మీన రాశి",
            "nakshatra_name_te": "రేవతి",
            "utc_sparsha_iso": "2024-04-08T15:42:00Z",
            "utc_madhya_iso": "2024-04-08T18:17:00Z",
            "utc_moksha_iso": "2024-04-08T20:52:00Z",
            "utc_sparsha": "15:42 UTC",
            "utc_madhya": "18:17 UTC",
            "utc_moksha": "20:52 UTC",
            "ist_sparsha": "09:12 PM IST",
            "ist_madhya": "11:47 PM IST",
            "ist_moksha": "02:22 AM IST (9-Apr)",
            "global_visibility": "ఉత్తర అమెరికా (టెక్సాస్, డల్లాస్, మెక్కిన్నీ, ఒహియో, న్యూయార్క్, కెనడా)",
            "visible_in_india": False,
            "visible_regions": ["north_america", "us", "usa", "texas", "mckinney", "dallas", "frisco", "mexico", "canada"],
            "visibility_summary_te": "టెక్సాస్ (డల్లాస్, మెక్కిన్నీ) గుండా సంపూర్ణ గ్రహణ మార్గం (100% Path of Totality) సాగింది. అమెరికా చరిత్రలోనే అత్యంత విశేష సూర్య గ్రహణం.",
            "rashi_impacts": {
                "subha": ["మిథునం", "సింహం", "మకరం", "కుంభం"],
                "madhyama": ["వృషభం", "కన్య", "వృశ్చికం", "మేషం"],
                "arishta": ["మీనం (గ్రహణ రాశి)", "కర్కాటకం", "తుల", "ధనుస్సు"]
            }
        },
        {
            "id": "ecl_2024_03",
            "type": "చంద్ర గ్రహణం (Lunar Eclipse)",
            "sub_type": "పాక్షిక చంద్ర గ్రహణం (Partial Lunar Eclipse / Super Harvest Moon)",
            "category": "పాక్షికం (Partial)",
            "date": "2024-09-18",
            "date_formatted": "18 సెప్టెంబర్ 2024 (బుధవారం)",
            "rashi_name_te": "మీన రాశి",
            "nakshatra_name_te": "పూర్వాభాద్ర / ఉత్తరాభాద్ర",
            "utc_sparsha_iso": "2024-09-18T00:41:00Z",
            "utc_madhya_iso": "2024-09-18T02:44:00Z",
            "utc_moksha_iso": "2024-09-18T04:47:00Z",
            "utc_sparsha": "00:41 UTC",
            "utc_madhya": "02:44 UTC",
            "utc_moksha": "04:47 UTC",
            "ist_sparsha": "06:11 AM IST",
            "ist_madhya": "08:14 AM IST",
            "ist_moksha": "10:17 AM IST",
            "global_visibility": "ఉత్తర అమెరికా (Texas, Dallas, McKinney), దక్షిణ అమెరికా, యూరప్, ఆఫ్రికా",
            "visible_in_india": False,
            "visible_regions": ["north_america", "us", "usa", "texas", "mckinney", "dallas", "south_america", "europe", "africa"],
            "visibility_summary_te": "అమెరికా (Texas, McKinney) మరియు దక్షిణ అమెరికా దేశాలలో రాత్రి వేళ స్పష్టంగా కనిపించింది. భారతదేశంలో పగటి వేళ అగుటచే కనిపించలేదు.",
            "rashi_impacts": {
                "subha": ["వృషభం", "కర్కాటకం", "ధనుస్సు", "మకరం"],
                "madhyama": ["మేషం", "మిథునం", "సింహం", "తుల"],
                "arishta": ["మీనం (గ్రహణ రాశి)", "కన్య", "వృశ్చికం", "కుంభం"]
            }
        },
        {
            "id": "ecl_2024_04",
            "type": "సూర్య గ్రహణం (Solar Eclipse)",
            "sub_type": "కంకణాకార సూర్య గ్రహణం (Annular Solar Eclipse)",
            "category": "కంకణాకారం (Annular)",
            "date": "2024-10-02",
            "date_formatted": "02 అక్టోబర్ 2024 (బుధవారం)",
            "rashi_name_te": "కన్య రాశి",
            "nakshatra_name_te": "హస్త / చిత్త",
            "utc_sparsha_iso": "2024-10-02T15:42:00Z",
            "utc_madhya_iso": "2024-10-02T18:45:00Z",
            "utc_moksha_iso": "2024-10-02T21:47:00Z",
            "utc_sparsha": "15:42 UTC",
            "utc_madhya": "18:45 UTC",
            "utc_moksha": "21:47 UTC",
            "ist_sparsha": "09:12 PM IST",
            "ist_madhya": "12:15 AM IST (3-Oct)",
            "ist_moksha": "03:17 AM IST (3-Oct)",
            "global_visibility": "దక్షిణ అమెరికా (చిలీ, అర్జెంటీనా), పసిఫిక్ మహాసముద్రం, ఈస్టర్ ఐలాండ్",
            "visible_in_india": False,
            "visible_regions": ["south_america", "chile", "argentina", "pacific"],
            "visibility_summary_te": "దక్షిణ అమెరికా దక్షిణ భాగంలో కంకణాకారంగా కనిపించింది. ఉత్తర అమెరికా మరియు భారతదేశంలో కనిపించలేదు.",
            "rashi_impacts": {
                "subha": ["మిథునం", "తుల", "ధనుస్సు", "మీనం"],
                "madhyama": ["మేషం", "వృషభం", "సింహం", "మకరం"],
                "arishta": ["కన్య (గ్రహణ రాశి)", "కర్కాటకం", "వృశ్చికం", "కుంభం"]
            }
        }
    ],
    2025: [
        {
            "id": "ecl_2025_01",
            "type": "చంద్ర గ్రహణం (Lunar Eclipse)",
            "sub_type": "సంపూర్ణ చంద్ర గ్రహణం (Total Lunar Eclipse)",
            "category": "సంపూర్ణం (Total)",
            "date": "2025-03-14",
            "date_formatted": "14 మార్చి 2025 (శుక్రవారం)",
            "rashi_name_te": "కన్య రాశి",
            "nakshatra_name_te": "ఉత్తర ఫల్గుణి / హస్త",
            "utc_sparsha_iso": "2025-03-14T05:09:00Z",
            "utc_madhya_iso": "2025-03-14T06:58:00Z",
            "utc_moksha_iso": "2025-03-14T08:48:00Z",
            "utc_sparsha": "05:09 UTC",
            "utc_madhya": "06:58 UTC",
            "utc_moksha": "08:48 UTC",
            "ist_sparsha": "10:39 AM IST",
            "ist_madhya": "12:28 PM IST",
            "ist_moksha": "02:18 PM IST",
            "global_visibility": "ఉత్తర అమెరికా, దక్షిణ అమెరికా, పసిఫిక్ మహాసముద్రం, అట్లాంటిక్, పశ్చిమ యూరప్, పశ్చిమ ఆఫ్రికా",
            "visible_in_india": False,
            "visible_regions": ["north_america", "south_america", "us", "usa", "texas", "mckinney", "dallas", "canada", "mexico"],
            "visibility_summary_te": "అమెరికా (USA, Texas), దక్షిణ అమెరికా దేశాలలో సంపూర్ణంగా కనిపిస్తుంది. భారతదేశంలో మరియు ఆసియాలో పగటి వేళ అగుటచే కనిపించదు.",
            "rashi_impacts": {
                "subha": ["వృషభం", "కర్కాటకం", "ధనుస్సు", "మకరం"],
                "madhyama": ["మేషం", "మిథునం", "తుల", "కుంభం"],
                "arishta": ["కన్య (గ్రహణ రాశి)", "సింహం", "వృశ్చికం", "మీనం"]
            }
        },
        {
            "id": "ecl_2025_02",
            "type": "సూర్య గ్రహణం (Solar Eclipse)",
            "sub_type": "పాక్షిక సూర్య గ్రహణం (Partial Solar Eclipse)",
            "category": "పాక్షికం (Partial)",
            "date": "2025-03-29",
            "date_formatted": "29 మార్చి 2025 (శనివారం)",
            "rashi_name_te": "మీన రాశి",
            "nakshatra_name_te": "ఉత్తరాభాద్ర / రేవతి",
            "utc_sparsha_iso": "2025-03-29T08:50:00Z",
            "utc_madhya_iso": "2025-03-29T10:47:00Z",
            "utc_moksha_iso": "2025-03-29T12:43:00Z",
            "utc_sparsha": "08:50 UTC",
            "utc_madhya": "10:47 UTC",
            "utc_moksha": "12:43 UTC",
            "ist_sparsha": "02:20 PM IST",
            "ist_madhya": "04:17 PM IST",
            "ist_moksha": "06:13 PM IST",
            "global_visibility": "యూరప్ (UK, France, Germany), ఉత్తర ఆఫ్రికా, ఉత్తర రష్యా, గ్రీన్‌లాండ్, కెనడాలోని కొన్ని ప్రాంతాలు",
            "visible_in_india": False,
            "visible_regions": ["europe", "uk", "france", "germany", "greenland", "canada_east", "north_africa"],
            "visibility_summary_te": "యూరప్ దేశాలు (లండన్, పారిస్, బెర్లిన్), ఉత్తర అమెరికా ఈశాన్య తీరం మరియు ఉత్తర అట్లాంటిక్‌లో స్పష్టంగా కనిపిస్తుంది. భారతదేశంలో కనిపించదు.",
            "rashi_impacts": {
                "subha": ["మిథునం", "సింహం", "మకరం", "కుంభం"],
                "madhyama": ["వృషభం", "కన్య", "వృశ్చికం", "మేషం"],
                "arishta": ["మీనం (గ్రహణ రాశి)", "కర్కాటకం", "తుల", "ధనుస్సు"]
            }
        },
        {
            "id": "ecl_2025_03",
            "type": "చంద్ర గ్రహణం (Lunar Eclipse)",
            "sub_type": "సంపూర్ణ చంద్ర గ్రహణం (Total Lunar Eclipse)",
            "category": "సంపూర్ణం (Total)",
            "date": "2025-09-07",
            "date_formatted": "07 సెప్టెంబర్ 2025 (ఆదివారం)",
            "rashi_name_te": "కుంభ రాశి",
            "nakshatra_name_te": "పూర్వాభాద్ర / శతభిషం",
            "utc_sparsha_iso": "2025-09-07T16:27:00Z",
            "utc_madhya_iso": "2025-09-07T18:11:00Z",
            "utc_moksha_iso": "2025-09-07T19:56:00Z",
            "utc_sparsha": "16:27 UTC",
            "utc_madhya": "18:11 UTC",
            "utc_moksha": "19:56 UTC",
            "ist_sparsha": "09:57 PM IST",
            "ist_madhya": "11:41 PM IST",
            "ist_moksha": "01:26 AM IST (8-Sep)",
            "global_visibility": "ఆసియా, భారతదేశం, యూరప్, ఆఫ్రికా, ఆస్ట్రేలియా, హిందూ మహాసముద్రం",
            "visible_in_india": True,
            "visible_regions": ["asia", "india", "europe", "africa", "australia", "middle_east"],
            "visibility_summary_te": "భారతదేశం అంతటా సంపూర్ణంగా కనిపిస్తుంది. అలాగే ఆసియా, యూరప్, ఆఫ్రికా, ఆస్ట్రేలియా దేశాలన్నింటిలోనూ స్పష్టంగా వీక్షించవచ్చు.",
            "rashi_impacts": {
                "subha": ["మేషం", "తుల", "ధనుస్సు", "మీనం"],
                "madhyama": ["వృషభం", "కర్కాటకం", "కన్య", "మకరం"],
                "arishta": ["కుంభం (గ్రహణ రాశి)", "సింహం", "వృశ్చికం", "మిథునం"]
            }
        },
        {
            "id": "ecl_2025_04",
            "type": "సూర్య గ్రహణం (Solar Eclipse)",
            "sub_type": "పాక్షిక సూర్య గ్రహణం (Partial Solar Eclipse)",
            "category": "పాక్షికం (Partial)",
            "date": "2025-09-21",
            "date_formatted": "21 సెప్టెంబర్ 2025 (ఆదివారం)",
            "rashi_name_te": "కన్య రాశి",
            "nakshatra_name_te": "హస్త / ఉత్తర ఫల్గుణి",
            "utc_sparsha_iso": "2025-09-21T17:29:00Z",
            "utc_madhya_iso": "2025-09-21T19:41:00Z",
            "utc_moksha_iso": "2025-09-21T21:53:00Z",
            "utc_sparsha": "17:29 UTC",
            "utc_madhya": "19:41 UTC",
            "utc_moksha": "21:53 UTC",
            "ist_sparsha": "10:59 PM IST",
            "ist_madhya": "01:11 AM IST (22-Sep)",
            "ist_moksha": "03:23 AM IST (22-Sep)",
            "global_visibility": "న్యూజిలాండ్, ఆస్ట్రేలియా దక్షిణ ప్రాంతం, అంటార్కిటికా, పసిఫిక్ మహాసముద్రం",
            "visible_in_india": False,
            "visible_regions": ["australia", "new_zealand", "pacific", "antarctica"],
            "visibility_summary_te": "న్యూజిలాండ్, ఫిజీ, ఆస్ట్రేలియా దక్షిణ తీరంలో కనిపిస్తుంది. భారతదేశం మరియు అమెరికాలో కనిపించదు.",
            "rashi_impacts": {
                "subha": ["వృషభం", "వృశ్చికం", "మకరం", "మీనం"],
                "madhyama": ["మేషం", "సింహం", "తుల", "కుంభం"],
                "arishta": ["కన్య (గ్రహణ రాశి)", "మిథునం", "కర్కాటకం", "ధనుస్సు"]
            }
        }
    ],
    2026: [
        {
            "id": "ecl_2026_01",
            "type": "సూర్య గ్రహణం (Solar Eclipse)",
            "sub_type": "కంకణాకార సూర్య గ్రహణం (Annular Solar Eclipse)",
            "category": "కంకణాకారం (Annular)",
            "date": "2026-02-17",
            "date_formatted": "17 ఫిబ్రవరి 2026 (మంగళవారం)",
            "rashi_name_te": "కుంభ రాశి",
            "nakshatra_name_te": "ధనిష్ఠ / శతభిషం",
            "utc_sparsha_iso": "2026-02-17T10:12:00Z",
            "utc_madhya_iso": "2026-02-17T12:13:00Z",
            "utc_moksha_iso": "2026-02-17T14:15:00Z",
            "utc_sparsha": "10:12 UTC",
            "utc_madhya": "12:13 UTC",
            "utc_moksha": "14:15 UTC",
            "ist_sparsha": "03:42 PM IST",
            "ist_madhya": "05:43 PM IST",
            "ist_moksha": "07:45 PM IST",
            "global_visibility": "దక్షిణ ఆఫ్రికా, దక్షిణ అమెరికా దక్షిణ భాగం, అంటార్కిటికా, అట్లాంటిక్ & హిందూ మహాసముద్రం",
            "visible_in_india": False,
            "visible_regions": ["south_africa", "south_america_south", "antarctica"],
            "visibility_summary_te": "దక్షిణ ఆఫ్రికా (కేప్‌టౌన్, జోహన్నెస్‌బర్గ్), అంటార్కిటికా ప్రాంతాలలో కనిపిస్తుంది. ఉత్తర అమెరికా & భారతదేశంలో దృశ్యత లేదు.",
            "rashi_impacts": {
                "subha": ["మేషం", "తుల", "ధనుస్సు", "మకరం"],
                "madhyama": ["వృషభం", "మిథునం", "కన్య", "మీనం"],
                "arishta": ["కుంభం (గ్రహణ రాశి)", "కర్కాటకం", "సింహం", "వృశ్చికం"]
            }
        },
        {
            "id": "ecl_2026_02",
            "type": "చంద్ర గ్రహణం (Lunar Eclipse)",
            "sub_type": "సంపూర్ణ చంద్ర గ్రహణం (Total Lunar Eclipse)",
            "category": "సంపూర్ణం (Total)",
            "date": "2026-03-03",
            "date_formatted": "03 మార్చి 2026 (మంగళవారం)",
            "rashi_name_te": "సింహ రాశి",
            "nakshatra_name_te": "మఖ / పూర్వ ఫల్గుణి",
            "utc_sparsha_iso": "2026-03-03T09:50:00Z",
            "utc_madhya_iso": "2026-03-03T11:34:00Z",
            "utc_moksha_iso": "2026-03-03T13:17:00Z",
            "utc_sparsha": "09:50 UTC",
            "utc_madhya": "11:34 UTC",
            "utc_moksha": "13:17 UTC",
            "ist_sparsha": "03:20 PM IST",
            "ist_madhya": "05:04 PM IST",
            "ist_moksha": "06:47 PM IST",
            "global_visibility": "ఆసియా, ఆస్ట్రేలియా, ఉత్తర అమెరికా (USA, Canada, Texas), పసిఫిక్ మహాసముద్రం",
            "visible_in_india": True,
            "visible_regions": ["north_america", "us", "usa", "texas", "mckinney", "dallas", "asia", "australia", "pacific"],
            "visibility_summary_te": "అమెరికా (Texas, Dallas, McKinney), ఆస్ట్రేలియా, జపాన్ దేశాలలో తెల్లవారుజామున స్పష్టంగా కనిపిస్తుంది. భారతదేశంలో కొన్ని ప్రాంతాలలో మోక్ష కాలంలో దర్శనమిస్తుంది.",
            "rashi_impacts": {
                "subha": ["మిథునం", "తుల", "ధనుస్సు", "మీనం"],
                "madhyama": ["మేషం", "కన్య", "మకరం", "కుంభం"],
                "arishta": ["సింహం (గ్రహణ రాశి)", "వృషభం", "కర్కాటకం", "వృశ్చికం"]
            }
        },
        {
            "id": "ecl_2026_03",
            "type": "సూర్య గ్రహణం (Solar Eclipse)",
            "sub_type": "సంపూర్ణ సూర్య గ్రహణం (Total Solar Eclipse - శతాబ్దపు అద్భుతం)",
            "category": "సంపూర్ణం (Total)",
            "date": "2026-08-12",
            "date_formatted": "12 ఆగస్టు 2026 (బుధవారం)",
            "rashi_name_te": "కర్కాటక రాశి",
            "nakshatra_name_te": "ఆశ్లేష",
            "utc_sparsha_iso": "2026-08-12T15:34:00Z",
            "utc_madhya_iso": "2026-08-12T17:47:00Z",
            "utc_moksha_iso": "2026-08-12T19:59:00Z",
            "utc_sparsha": "15:34 UTC",
            "utc_madhya": "17:47 UTC",
            "utc_moksha": "19:59 UTC",
            "ist_sparsha": "09:04 PM IST",
            "ist_madhya": "11:17 PM IST",
            "ist_moksha": "01:29 AM IST (13-Aug)",
            "global_visibility": "యూరప్ (స్పెయిన్, ఐస్‌లాండ్, గ్రీన్‌లాండ్), ఉత్తర అమెరికా ఈశాన్య తీరం, ఉత్తర అట్లాంటిక్",
            "visible_in_india": False,
            "visible_regions": ["europe", "spain", "iceland", "greenland", "north_america_east"],
            "visibility_summary_te": "స్పెయిన్ (Madrid, Barcelona), ఐస్‌లాండ్ దేశాలలో సంపూర్ణంగా (100% Total Eclipse) కనిపిస్తుంది. ఉత్తర అమెరికా ఈశాన్య తీరంలో పాక్షికంగా వీక్షించవచ్చు.",
            "rashi_impacts": {
                "subha": ["కన్య", "వృశ్చికం", "మీనం", "వృషభం"],
                "madhyama": ["మేషం", "తుల", "ధనుస్సు", "మకరం"],
                "arishta": ["కర్కాటకం (గ్రహణ రాశి)", "మిథునం", "సింహం", "కుంభం"]
            }
        },
        {
            "id": "ecl_2026_04",
            "type": "చంద్ర గ్రహణం (Lunar Eclipse)",
            "sub_type": "పాక్షిక చంద్ర గ్రహణం (Partial Lunar Eclipse)",
            "category": "పాక్షికం (Partial)",
            "date": "2026-08-28",
            "date_formatted": "28 ఆగస్టు 2026 (శుక్రవారం)",
            "rashi_name_te": "కుంభ రాశి",
            "nakshatra_name_te": "శతభిషం / పూర్వాభాద్ర",
            "utc_sparsha_iso": "2026-08-28T02:23:00Z",
            "utc_madhya_iso": "2026-08-28T04:13:00Z",
            "utc_moksha_iso": "2026-08-28T06:02:00Z",
            "utc_sparsha": "02:23 UTC",
            "utc_madhya": "04:13 UTC",
            "utc_moksha": "06:02 UTC",
            "ist_sparsha": "07:53 AM IST",
            "ist_madhya": "09:43 AM IST",
            "ist_moksha": "11:32 AM IST",
            "global_visibility": "ఉత్తర అమెరికా (USA, Texas, McKinney), దక్షిణ అమెరికా, పసిఫిక్, యూరప్ పశ్చిమ భాగం",
            "visible_in_india": False,
            "visible_regions": ["north_america", "us", "usa", "texas", "mckinney", "dallas", "south_america"],
            "visibility_summary_te": "అమెరికా (USA, Texas, McKinney) మరియు దక్షిణ అమెరికా ఖండాలలో రాత్రి వేళ స్పష్టంగా కనిపిస్తుంది. భారతదేశంలో పగటి వేళ అగుటచే కనిపించదు.",
            "rashi_impacts": {
                "subha": ["మేషం", "మిథునం", "తుల", "ధనుస్సు"],
                "madhyama": ["వృషభం", "కన్య", "మకరం", "మీనం"],
                "arishta": ["కుంభం (గ్రహణ రాశి)", "కర్కాటకం", "సింహం", "వృశ్చికం"]
            }
        }
    ],
    2027: [
        {
            "id": "ecl_2027_01",
            "type": "సూర్య గ్రహణం (Solar Eclipse)",
            "sub_type": "కంకణాకార సూర్య గ్రహణం (Annular Solar Eclipse)",
            "category": "కంకణాకారం (Annular)",
            "date": "2027-02-06",
            "date_formatted": "06 ఫిబ్రవరి 2027 (శనివారం)",
            "rashi_name_te": "మకర రాశి",
            "nakshatra_name_te": "శ్రవణం",
            "utc_sparsha_iso": "2027-02-06T14:02:00Z",
            "utc_madhya_iso": "2027-02-06T16:00:00Z",
            "utc_moksha_iso": "2027-02-06T18:00:00Z",
            "utc_sparsha": "14:02 UTC",
            "utc_madhya": "16:00 UTC",
            "utc_moksha": "18:00 UTC",
            "ist_sparsha": "07:32 PM IST",
            "ist_madhya": "09:30 PM IST",
            "ist_moksha": "11:30 PM IST",
            "global_visibility": "దక్షిణ అమెరికా (చిలీ, అర్జెంటీనా), పశ్చిమ ఆఫ్రికా, అట్లాంటిక్ మహాసముద్రం",
            "visible_in_india": False,
            "visible_regions": ["south_america", "chile", "argentina", "west_africa"],
            "visibility_summary_te": "దక్షిణ అమెరికా మరియు పశ్చిమ ఆఫ్రికా దేశాలలో కనిపిస్తుంది.",
            "rashi_impacts": {
                "subha": ["వృషభం", "కన్య", "తుల", "మీనం"],
                "madhyama": ["మిథునం", "సింహం", "వృశ్చికం", "కుంభం"],
                "arishta": ["మకరం (గ్రహణ రాశి)", "మేషం", "కర్కాటకం", "ధనుస్సు"]
            }
        },
        {
            "id": "ecl_2027_02",
            "type": "సూర్య గ్రహణం (Solar Eclipse)",
            "sub_type": "సంపూర్ణ సూర్య గ్రహణం (Total Solar Eclipse)",
            "category": "సంపూర్ణం (Total)",
            "date": "2027-08-02",
            "date_formatted": "02 ఆగస్టు 2027 (సోమవారం)",
            "rashi_name_te": "కర్కాటక రాశి",
            "nakshatra_name_te": "పుష్యమి / ఆశ్లేష",
            "utc_sparsha_iso": "2027-08-02T08:23:00Z",
            "utc_madhya_iso": "2027-08-02T10:07:00Z",
            "utc_moksha_iso": "2027-08-02T11:51:00Z",
            "utc_sparsha": "08:23 UTC",
            "utc_madhya": "10:07 UTC",
            "utc_moksha": "11:51 UTC",
            "ist_sparsha": "01:53 PM IST",
            "ist_madhya": "03:37 PM IST",
            "ist_moksha": "05:21 PM IST",
            "global_visibility": "ఉత్తర ఆఫ్రికా (ఈజిప్ట్, లిబియా), మధ్యప్రాచ్యం (సౌదీ అరేబియా, UAE), దక్షిణ యూరప్ (స్పెయిన్, ఇటలీ), భారతదేశం (పాక్షికంగా)",
            "visible_in_india": True,
            "visible_regions": ["egypt", "middle_east", "uae", "saudi", "europe_south", "india"],
            "visibility_summary_te": "ఈజిప్ట్ (Luxor) లో 6 నిమిషాలకు పైగా సంపూర్ణంగా కనిపిస్తుంది. భారతదేశంలో పశ్చిమ మరియు ఉత్తర ప్రాంతాలలో పాక్షికంగా వీక్షించవచ్చు. గల్ఫ్ (UAE, Saudi) దేశాలలో స్పష్టంగా కనిపిస్తుంది.",
            "rashi_impacts": {
                "subha": ["కన్య", "వృశ్చికం", "మకరం", "మీనం"],
                "madhyama": ["మేషం", "తుల", "ధనుస్సు", "కుంభం"],
                "arishta": ["కర్కాటకం (గ్రహణ రాశి)", "వృషభం", "మిథునం", "సింహం"]
            }
        },
        {
            "id": "ecl_2027_03",
            "type": "చంద్ర గ్రహణం (Lunar Eclipse)",
            "sub_type": "ఉపచ్ఛాయ చంద్ర గ్రహణం (Penumbral Lunar Eclipse)",
            "category": "ఛాయ / ఉపచ్ఛాయ (Penumbral)",
            "date": "2027-02-20",
            "date_formatted": "20 ఫిబ్రవరి 2027 (శనివారం)",
            "rashi_name_te": "సింహ రాశి",
            "nakshatra_name_te": "మఖ / పూర్వ ఫల్గుణి",
            "utc_sparsha_iso": "2027-02-20T21:13:00Z",
            "utc_madhya_iso": "2027-02-20T23:13:00Z",
            "utc_moksha_iso": "2027-02-21T01:13:00Z",
            "utc_sparsha": "21:13 UTC",
            "utc_madhya": "23:13 UTC",
            "utc_moksha": "01:13 UTC (21-Feb)",
            "ist_sparsha": "02:43 AM IST (21-Feb)",
            "ist_madhya": "04:43 AM IST (21-Feb)",
            "ist_moksha": "06:43 AM IST (21-Feb)",
            "global_visibility": "యూరప్, ఆఫ్రికా, ఉత్తర అమెరికా (USA, Texas, McKinney), దక్షిణ అమెరికా, అట్లాంటిక్",
            "visible_in_india": True,
            "visible_regions": ["north_america", "us", "usa", "texas", "mckinney", "dallas", "south_america", "europe", "africa", "india"],
            "visibility_summary_te": "ఉత్తర అమెరికా (Texas, McKinney) మరియు దక్షిణ అమెరికాలో రాత్రి వేళ స్పష్టంగా కనిపిస్తుంది. భారతదేశంలో వేకువజామున దర్శనమిస్తుంది.",
            "rashi_impacts": {
                "subha": ["మిథునం", "తుల", "ధనుస్సు", "మీనం"],
                "madhyama": ["మేషం", "కన్య", "మకరం", "కుంభం"],
                "arishta": ["సింహం (గ్రహణ రాశి)", "వృషభం", "కర్కాటకం", "వృశ్చికం"]
            }
        },
        {
            "id": "ecl_2027_04",
            "type": "చంద్ర గ్రహణం (Lunar Eclipse)",
            "sub_type": "ఉపచ్ఛాయ చంద్ర గ్రహణం (Penumbral Lunar Eclipse)",
            "category": "ఛాయ / ఉపచ్ఛాయ (Penumbral)",
            "date": "2027-07-18",
            "date_formatted": "18 జూలై 2027 (ఆదివారం)",
            "rashi_name_te": "ధనుస్సు రాశి",
            "nakshatra_name_te": "ఉత్తరాషాఢ నక్షత్రం",
            "utc_sparsha_iso": "2027-07-18T14:59:00Z",
            "utc_madhya_iso": "2027-07-18T16:03:00Z",
            "utc_moksha_iso": "2027-07-18T17:07:00Z",
            "utc_sparsha": "14:59 UTC",
            "utc_madhya": "16:03 UTC",
            "utc_moksha": "17:07 UTC",
            "ist_sparsha": "08:29 PM IST",
            "ist_madhya": "09:33 PM IST",
            "ist_moksha": "10:37 PM IST",
            "global_visibility": "ఆఫ్రికా, యూరప్, ఆసియా, భారతదేశం, ఆస్ట్రేలియా, హిందూ మహాసముద్రం",
            "visible_in_india": True,
            "visible_regions": ["asia", "india", "africa", "europe", "australia"],
            "visibility_summary_te": "భారతదేశంలో రాత్రి వేళ స్పష్టంగా కనిపిస్తుంది. ఆఫ్రికా, ఆసియా దేశాలలో కూడా దర్శనమిస్తుంది. అమెరికా ఖండంలో పగటి వేళ అగుటచే కనిపించదు.",
            "rashi_impacts": {
                "subha": ["మేషం", "సింహం", "తుల", "కుంభం"],
                "madhyama": ["వృషభం", "కర్కాటకం", "కన్య", "మకరం"],
                "arishta": ["ధనుస్సు (గ్రహణ రాశి)", "మిథునం", "వృశ్చికం", "మీనం"]
            }
        },
        {
            "id": "ecl_2027_05",
            "type": "చంద్ర గ్రహణం (Lunar Eclipse)",
            "sub_type": "ఉపచ్ఛాయ చంద్ర గ్రహణం (Penumbral Lunar Eclipse)",
            "category": "ఛాయ / ఉపచ్ఛాయ (Penumbral)",
            "date": "2027-08-17",
            "date_formatted": "17 ఆగస్టు 2027 (మంగళవారం)",
            "rashi_name_te": "కుంభ రాశి",
            "nakshatra_name_te": "ధనిష్ఠ / శతభిషం",
            "utc_sparsha_iso": "2027-08-17T06:14:00Z",
            "utc_madhya_iso": "2027-08-17T07:14:00Z",
            "utc_moksha_iso": "2027-08-17T08:14:00Z",
            "utc_sparsha": "06:14 UTC",
            "utc_madhya": "07:14 UTC",
            "utc_moksha": "08:14 UTC",
            "ist_sparsha": "11:44 AM IST",
            "ist_madhya": "12:44 PM IST",
            "ist_moksha": "01:44 PM IST",
            "global_visibility": "పసిఫిక్, ఆస్ట్రేలియా, ఉత్తర అమెరికా (USA, Texas, McKinney), తూర్పు ఆసియా",
            "visible_in_india": False,
            "visible_regions": ["north_america", "us", "usa", "texas", "mckinney", "dallas", "pacific", "australia"],
            "visibility_summary_te": "అమెరికా (Texas, McKinney) లో తెల్లవారుజామున చంద్రాస్తమయ వేళ దర్శనమిస్తుంది. భారతదేశంలో పగటి వేళ అగుటచే కనిపించదు.",
            "rashi_impacts": {
                "subha": ["మేషం", "మిథునం", "తుల", "ధనుస్సు"],
                "madhyama": ["వృషభం", "కన్య", "మకరం", "మీనం"],
                "arishta": ["కుంభం (గ్రహణ రాశి)", "కర్కాటకం", "సింహం", "వృశ్చికం"]
            }
        }
    ],
    2028: [
        {
            "id": "ecl_2028_01",
            "type": "చంద్ర గ్రహణం (Lunar Eclipse)",
            "sub_type": "పాక్షిక చంద్ర గ్రహణం (Partial Lunar Eclipse)",
            "category": "పాక్షికం (Partial)",
            "date": "2028-01-12",
            "date_formatted": "12 జనవరి 2028 (బుధవారం)",
            "rashi_name_te": "మిథున రాశి",
            "nakshatra_name_te": "పునర్వసు నక్షత్రం",
            "utc_sparsha_iso": "2028-01-12T02:43:00Z",
            "utc_madhya_iso": "2028-01-12T04:14:00Z",
            "utc_moksha_iso": "2028-01-12T05:45:00Z",
            "utc_sparsha": "02:43 UTC",
            "utc_madhya": "04:14 UTC",
            "utc_moksha": "05:45 UTC",
            "ist_sparsha": "08:13 AM IST",
            "ist_madhya": "09:44 AM IST",
            "ist_moksha": "11:15 AM IST",
            "global_visibility": "ఉత్తర అమెరికా (USA, Texas, McKinney), దక్షిణ అమెరికా, యూరప్, పశ్చిమ ఆఫ్రికా, అట్లాంటిక్ & పసిఫిక్",
            "visible_in_india": False,
            "visible_regions": ["north_america", "us", "usa", "texas", "mckinney", "dallas", "frisco", "south_america", "europe", "africa"],
            "visibility_summary_te": "ఉత్తర అమెరికా (Texas, Dallas, McKinney) మరియు దక్షిణ అమెరికా ఖండాలలో రాత్రి వేళ అత్యంత స్పష్టంగా కనిపిస్తుంది. భారతదేశంలో పగటి వేళ కావడంతో కనిపించదు.",
            "rashi_impacts": {
                "subha": ["మేషం", "సింహం", "తుల", "కుంభం"],
                "madhyama": ["వృషభం", "కన్య", "వృశ్చికం", "మకరం"],
                "arishta": ["మిథునం (గ్రహణ రాశి)", "కర్కాటకం", "ధనుస్సు", "మీనం"]
            }
        },
        {
            "id": "ecl_2028_02",
            "type": "సూర్య గ్రహణం (Solar Eclipse)",
            "sub_type": "కంకణాకార సూర్య గ్రహణం (Annular Solar Eclipse)",
            "category": "కంకణాకారం (Annular)",
            "date": "2028-01-26",
            "date_formatted": "26 జనవరి 2028 (బుధవారం)",
            "rashi_name_te": "మకర రాశి",
            "nakshatra_name_te": "శ్రవణ నక్షత్రం",
            "utc_sparsha_iso": "2028-01-26T12:44:00Z",
            "utc_madhya_iso": "2028-01-26T15:08:00Z",
            "utc_moksha_iso": "2028-01-26T17:32:00Z",
            "utc_sparsha": "12:44 UTC",
            "utc_madhya": "15:08 UTC",
            "utc_moksha": "17:32 UTC",
            "ist_sparsha": "06:14 PM IST",
            "ist_madhya": "08:38 PM IST",
            "ist_moksha": "11:02 PM IST",
            "global_visibility": "దక్షిణ అమెరికా (ఈక్వెడార్, బ్రెజిల్), అట్లాంటిక్, స్పెయిన్, పోర్చుగల్, ఉత్తర అమెరికా తూర్పు/దక్షిణ ప్రాంతాలు (పాక్షికంగా)",
            "visible_in_india": False,
            "visible_regions": ["south_america", "atlantic", "spain", "portugal", "north_america_east", "us_east", "texas", "mckinney"],
            "visibility_summary_te": "దక్షిణ అమెరికా మరియు స్పెయిన్ లలో కంకణాకారంగా, ఉత్తర అమెరికా తూర్పు/దక్షిణ తీరంలో (Texas తో సహా) ఉదయపు వేళ పాక్షికంగా కనిపిస్తుంది. భారతదేశంలో కనిపించదు.",
            "rashi_impacts": {
                "subha": ["వృషభం", "కన్య", "వృశ్చికం", "మీనం"],
                "madhyama": ["మిథునం", "సింహం", "తుల", "ధనుస్సు"],
                "arishta": ["మకరం (గ్రహణ రాశి)", "మేషం", "కర్కాటకం", "కుంభం"]
            }
        },
        {
            "id": "ecl_2028_03",
            "type": "చంద్ర గ్రహణం (Lunar Eclipse)",
            "sub_type": "పాక్షిక చంద్ర గ్రహణం (Partial Lunar Eclipse)",
            "category": "పాక్షికం (Partial)",
            "date": "2028-07-06",
            "date_formatted": "06 జూలై 2028 (గురువారం)",
            "rashi_name_te": "ధనుస్సు రాశి",
            "nakshatra_name_te": "పూర్వాషాఢ / ఉత్తరాషాఢ",
            "utc_sparsha_iso": "2028-07-06T16:51:00Z",
            "utc_madhya_iso": "2028-07-06T18:20:00Z",
            "utc_moksha_iso": "2028-07-06T19:49:00Z",
            "utc_sparsha": "16:51 UTC",
            "utc_madhya": "18:20 UTC",
            "utc_moksha": "19:49 UTC",
            "ist_sparsha": "10:21 PM IST",
            "ist_madhya": "11:50 PM IST",
            "ist_moksha": "01:19 AM IST (7-Jul)",
            "global_visibility": "ఆసియా, భారతదేశం, యూరప్, ఆఫ్రికా, ఆస్ట్రేలియా, హిందూ మహాసముద్రం",
            "visible_in_india": True,
            "visible_regions": ["asia", "india", "europe", "africa", "australia", "middle_east"],
            "visibility_summary_te": "భారతదేశంలో రాత్రి వేళ సంపూర్ణంగా కనిపిస్తుంది. ఆసియా, ఆస్ట్రేలియా, ఆఫ్రికాలలో కూడా దర్శనమిస్తుంది. అమెరికా ఖండంలో పగటి వేళ అగుటచే కనిపించదు.",
            "rashi_impacts": {
                "subha": ["మేషం", "సింహం", "తుల", "కుంభం"],
                "madhyama": ["వృషభం", "కర్కాటకం", "కన్య", "మకరం"],
                "arishta": ["ధనుస్సు (గ్రహణ రాశి)", "మిథునం", "వృశ్చికం", "మీనం"]
            }
        },
        {
            "id": "ecl_2028_04",
            "type": "సూర్య గ్రహణం (Solar Eclipse)",
            "sub_type": "సంపూర్ణ సూర్య గ్రహణం (Total Solar Eclipse - Southern Cross)",
            "category": "సంపూర్ణం (Total)",
            "date": "2028-07-22",
            "date_formatted": "22 జూలై 2028 (శనివారం)",
            "rashi_name_te": "కర్కాటక రాశి",
            "nakshatra_name_te": "పుష్యమి నక్షత్రం",
            "utc_sparsha_iso": "2028-07-22T01:05:00Z",
            "utc_madhya_iso": "2028-07-22T02:56:00Z",
            "utc_moksha_iso": "2028-07-22T04:47:00Z",
            "utc_sparsha": "01:05 UTC",
            "utc_madhya": "02:56 UTC",
            "utc_moksha": "04:47 UTC",
            "ist_sparsha": "06:35 AM IST",
            "ist_madhya": "08:26 AM IST",
            "ist_moksha": "10:17 AM IST",
            "global_visibility": "ఆస్ట్రేలియా (సిడ్నీ నగరం గుండా సంపూర్ణ మార్గం), న్యూజిలాండ్, పసిఫిక్, ఇండోనేషియా",
            "visible_in_india": False,
            "visible_regions": ["australia", "sydney", "new_zealand", "pacific", "indonesia"],
            "visibility_summary_te": "ఆస్ట్రేలియా (సిడ్నీ, డార్విన్) మరియు న్యూజిలాండ్ లలో సంపూర్ణంగా కనిపిస్తుంది. ఉత్తర అమెరికా మరియు భారతదేశంలో దృశ్యత లేదు.",
            "rashi_impacts": {
                "subha": ["కన్య", "వృశ్చికం", "మకరం", "మీనం"],
                "madhyama": ["మేషం", "తుల", "ధనుస్సు", "కుంభం"],
                "arishta": ["కర్కాటకం (గ్రహణ రాశి)", "వృషభం", "మిథునం", "సింహం"]
            }
        },
        {
            "id": "ecl_2028_05",
            "type": "చంద్ర గ్రహణం (Lunar Eclipse)",
            "sub_type": "సంపూర్ణ చంద్ర గ్రహణం (Total Lunar Eclipse - New Year Blue Moon)",
            "category": "సంపూర్ణం (Total)",
            "date": "2028-12-31",
            "date_formatted": "31 డిసెంబర్ 2028 (ఆదివారం)",
            "rashi_name_te": "మిథున రాశి",
            "nakshatra_name_te": "ఆరుద్ర నక్షత్రం",
            "utc_sparsha_iso": "2028-12-31T14:52:00Z",
            "utc_madhya_iso": "2028-12-31T16:32:00Z",
            "utc_moksha_iso": "2028-12-31T18:12:00Z",
            "utc_sparsha": "14:52 UTC",
            "utc_madhya": "16:32 UTC",
            "utc_moksha": "18:12 UTC",
            "ist_sparsha": "08:22 PM IST",
            "ist_madhya": "10:02 PM IST",
            "ist_moksha": "11:42 PM IST",
            "global_visibility": "ఆసియా, భారతదేశం, ఆస్ట్రేలియా, యూరప్, ఆఫ్రికా, ఉత్తర అమెరికా పశ్చిమ & మధ్య ప్రాంతాలు (డాలస్/మెక్కిన్నీ వేకువజామున)",
            "visible_in_india": True,
            "visible_regions": ["asia", "india", "australia", "europe", "africa", "north_america", "us", "texas", "mckinney", "dallas"],
            "visibility_summary_te": "నూతన సంవత్సర వేళ భారతదేశం అంతటా రాత్రి వేళ సంపూర్ణంగా కనిపిస్తుంది. అలాగే ఆసియా, యూరప్ మరియు అమెరికా (Texas, McKinney) లో తెల్లవారుజామున చంద్రోదయ/చంద్రాస్తమయ వేళ దర్శనమిస్తుంది.",
            "rashi_impacts": {
                "subha": ["మేషం", "సింహం", "తుల", "కుంభం"],
                "madhyama": ["వృషభం", "కన్య", "వృశ్చికం", "మకరం"],
                "arishta": ["మిథునం (గ్రహణ రాశి)", "కర్కాటకం", "ధనుస్సు", "మీనం"]
            }
        }
    ]
}

ECLIPSE_BHAVA_MEANINGS = {
    1: {
        "title": "1వ భావం — తను భావం (Lagna / Ascendant)",
        "desc": "లగ్నంలోనే గ్రహణం సంభవించుటచే శారీరక ఆరోగ్యం, మానసిక ప్రశాంతతపై దృష్టి పెట్టాలి. ఆదిత్య హృదయ స్తోత్రం లేదా శివారాధన విశేష మనశ్శాంతినిస్తుంది."
    },
    2: {
        "title": "2వ భావం — ధన & కుటుంబ భావం (Wealth & Family)",
        "desc": "ఆర్థిక లావాదేవీలు, వాక్-సంయమనం మరియు కుటుంబ విషయాలలో జాగ్రత్త అవసరం. అనవసర వాదనలు లేదా నష్టదాయక పెట్టుబడులకు దూరంగా ఉండాలి."
    },
    3: {
        "title": "3వ భావం — భ్రాతృ & పరాక్రమ భావం (Courage & Siblings)",
        "desc": "తోబుట్టువులతో సత్సంబంధాలు, ప్రయాణాలలో జాగ్రత్త అవసరం. నూతన ప్రయత్నాలు మరియు ఒప్పందాలలో ఒకటికి రెండుసార్లు ఆలోచించి నిర్ణయం తీసుకోవాలి."
    },
    4: {
        "title": "4వ భావం — మాతృ & సుఖ భావం (Mother & Happiness)",
        "desc": "గృహ వాతావరణం, వాహన సౌఖ్యం మరియు తల్లిగారి ఆరోగ్యంపై శ్రద్ధ వహించాలి. మనశ్శాంతి కొరకు నిత్యం ఇష్ట దైవ నామస్మరణ చేయండి."
    },
    5: {
        "title": "5వ భావం — పుత్ర & పూర్వపుణ్య భావం (Children & Intellect)",
        "desc": "సంతాన సంక్షేమం, ఆలోచనా సరళి మరియు విద్యా రంగంలో ఏకాగ్రత అవసరం. గర్భిణీ స్త్రీలు విశేషంగా రక్షా స్తోత్రాలు పారాయణ చేయాలి."
    },
    6: {
        "title": "6వ భావం — శత్రు, రోగ & ఋణ భావం (Health & Obstacles)",
        "desc": "శత్రువులపై పైచేయి సాధించినప్పటికీ, ఆకస్మిక అనారోగ్యాలు, ఋణాలు లేదా వివాదాల విషయంలో అప్రమత్తంగా ఉండాలి. సుబ్రహ్మణ్య లేదా శివ పూజ శ్రేయస్కరం."
    },
    7: {
        "title": "7వ భావం — కళత్ర & భాగస్వామ్య భావం (Spouse & Partnerships)",
        "desc": "లగ్నానికి సరిగ్గా సప్తమ స్థానంలో గ్రహణం ఏర్పడుటచే దాంపత్య జీవితంలోను, వ్యాపార భాగస్వాములతోను సంయమనం, అవగాహన పాటించాలి."
    },
    8: {
        "title": "8వ భావం — ఆయుష్షు & రంధ్ర భావం (Longevity & Sudden Events)",
        "desc": "ఆకస్మిక మార్పులు లేదా ఒడిదుడుకులు సంభవించవచ్చు. ప్రయాణాలలో అత్యంత జాగ్రత్త వహించి, మహామృత్యుంజయ జపం లేదా శాంతి దానాలు చేయడం మంచిది."
    },
    9: {
        "title": "9వ భావం — భాగ్య & ధర్మ భావం (Fortune & Dharma)",
        "desc": "పితృ సమానుల ఆరోగ్యం, తీర్థయాత్రలు మరియు దూర ప్రయాణాల యందు శ్రద్ధ వహించాలి. ధర్మ కార్యాలు, అన్నదానం విశేష సత్ఫలితాలను ఇస్తాయి."
    },
    10: {
        "title": "10వ భావం — రాజ్య, కర్మ & వృత్తి భావం (Career & Profession)",
        "desc": "ఉద్యోగ, వ్యాపార మరియు సామాజిక ప్రతిష్ట యందు హెచ్చుతగ్గులు ఉండవచ్చు. కార్యరంగంలో ఉన్నతాధికారులతో వివేకంతో మెలగాలి."
    },
    11: {
        "title": "11వ భావం — లాభ & ఆకాంక్ష భావం (Gains & Desires)",
        "desc": "మిత్రుల సహకారం, ఆర్థిక రాబడులలో ఆశించిన ఫలితాల కోసం దైవారాధన తోడ్పడుతుంది. పెద్దల ఆశీస్సులు రక్షణగా నిలుస్తాయి."
    },
    12: {
        "title": "12వ భావం — వ్యయ & మోక్ష భావం (Expenditure & Moksha)",
        "desc": "ఆకస్మిక ఖర్చులు, నిద్రాభంగం లేదా దూర ప్రయాణాలు గోచరిస్తున్నాయి. మోక్షకారక సమయం అగుటచే ధ్యానం, దానధర్మాలు విశేష పుణ్యఫలాన్నిస్తాయి."
    }
}


def calculate_city_eclipses(
    year: int = 2028,
    city: str = "McKinney",
    country: str = "US",
    lat: float = 33.1976,
    lon: float = -96.6178,
    tz_name: str = "America/Chicago",
    tz_offset: float = -5.0,
    eclipse_type: str = "all",
    visible_only: bool = True,
    language: str = "te"
) -> Dict[str, Any]:
    """
    Computes city-specific eclipse data:
    - Distinguishes Solar (సూర్య) vs Lunar (చంద్ర) Eclipses.
    - Converts UTC Sparsha, Madhya, Moksha into city's exact local timezone.
    - Calculates total eclipse duration.
    - Determines city-level visibility.
    - Computes city Sutaka timings (12h prior for Solar, 9h prior for Lunar).
    - Identifies affected Zodiac Signs & Constellations and 12-Rashi impacts.
    - Filters by eclipse_type ('all', 'lunar', 'solar').
    """
    selected_year = year if year in ECLIPSES_DATABASE else 2028
    raw_eclipses = ECLIPSES_DATABASE.get(selected_year, ECLIPSES_DATABASE[2028])

    # Resolve timezone
    tz = None
    if tz_name:
        try:
            tz = ZoneInfo(tz_name.strip())
        except Exception:
            pass
    if tz is None:
        try:
            tz = timezone(timedelta(hours=tz_offset))
        except Exception:
            tz = timezone.utc

    city_clean = city.strip() or "McKinney"
    city_lower = city_clean.lower()
    country_lower = (country or "").lower()

    all_results = []
    visible_count = 0
    total_lunar = 0
    total_solar = 0
    visible_lunar = 0
    visible_solar = 0

    for e in raw_eclipses:
        # Check eclipse category: Solar vs Lunar
        is_solar = "సూర్య" in e["type"] or "Solar" in e["type"]
        is_lunar = not is_solar

        if is_lunar:
            total_lunar += 1
        else:
            total_solar += 1

        # 1. Parse UTC Datetimes
        dt_sparsha_utc = datetime.fromisoformat(e["utc_sparsha_iso"].replace("Z", "+00:00"))
        dt_madhya_utc = datetime.fromisoformat(e["utc_madhya_iso"].replace("Z", "+00:00"))
        dt_moksha_utc = datetime.fromisoformat(e["utc_moksha_iso"].replace("Z", "+00:00"))

        # 2. Convert to Local Timezone
        dt_sparsha_loc = dt_sparsha_utc.astimezone(tz)
        dt_madhya_loc = dt_madhya_utc.astimezone(tz)
        dt_moksha_loc = dt_moksha_utc.astimezone(tz)

        # 3. Calculate Total Duration
        duration_sec = int((dt_moksha_utc - dt_sparsha_utc).total_seconds())
        dur_h = duration_sec // 3600
        dur_m = (duration_sec % 3600) // 60
        dur_text = f"{dur_h} గంటల {dur_m:02d} నిమిషాలు ({dur_h}h {dur_m:02d}m)"

        # 4. Sutaka Timings (12h for Solar, 9h for Lunar)
        sutaka_hours = 12 if is_solar else 9
        dt_sutaka_start = dt_sparsha_loc - timedelta(hours=sutaka_hours)
        dt_sutaka_end = dt_moksha_loc

        # 5. Determine City Visibility
        vis_regions = e.get("visible_regions", [])
        is_visible = False

        # Match by city name or country or regional keywords
        if any(keyword in city_lower for keyword in ["mckinney", "dallas", "frisco", "plano", "houston", "austin", "texas"]):
            is_visible = any(r in ["texas", "us", "usa", "north_america", "mckinney", "dallas"] for r in vis_regions)
        elif any(keyword in country_lower for keyword in ["us", "usa", "united states", "america"]):
            is_visible = any(r in ["us", "usa", "north_america", "texas"] for r in vis_regions)
        elif any(keyword in country_lower for keyword in ["in", "india", "భారతదేశం"]):
            is_visible = e.get("visible_in_india", False) or any(r in ["india", "asia"] for r in vis_regions)
        elif any(keyword in country_lower for keyword in ["uk", "united kingdom", "britain", "london"]):
            is_visible = any(r in ["uk", "europe", "london"] for r in vis_regions)
        elif any(keyword in country_lower for keyword in ["au", "australia", "sydney"]):
            is_visible = any(r in ["australia", "sydney", "pacific"] for r in vis_regions)
        else:
            is_visible = any(r in city_lower or r in country_lower for r in vis_regions)

        if is_visible:
            visible_count += 1
            if is_lunar:
                visible_lunar += 1
            else:
                visible_solar += 1
            vis_badge = f"మీ నగరంలో కనిపిస్తుంది (Visible in {city_clean})"
            vis_badge_class = "success"
            vis_note = f"{city_clean} ({country or 'స్థానిక ప్రాంతం'}) లో ఈ గ్రహణం స్పష్టంగా వీక్షించవచ్చు. గ్రహణ సమయాలు, సూతక నియమాలు మరియు దైవ జపాలు ఆచరించదగినవి."
        else:
            vis_badge = f"మీ నగరంలో కనిపించదు (Not Visible in {city_clean})"
            vis_badge_class = "neutral"
            vis_note = f"{city_clean} నగరంలో ఈ గ్రహణం దర్శనమివ్వదు (పగటి/రాత్రి వేళ లేదా గ్రహణ రేఖకు ఆవల ఉండుటచే దృశ్యత లేదు). స్థానికంగా సూతక నియమాల పాటించవలసిన అవసరం లేదు."

        # Remedies tailored to Moon vs Sun
        if is_lunar:
            shanti_remedies = [
                "చంద్ర గ్రహణ సమయంలో శివ పంచాక్షరి (ఓం నమశ్శివాయ), చంద్ర గాయత్రి లేదా మహామృత్యుంజయ మంత్ర జపం విశేష పుణ్యప్రదం.",
                "మోక్ష కాలం ముగిసిన వెంటనే శుద్ధ స్నానం ఆచరించి శివలింగార్చన లేదా ఇంట్లో దైవ దీపారాధన చేయండి.",
                "గ్రహణ బాధిత రాశుల వారు (అనిష్ట రాశులు) వెండి, బియ్యం, శంఖం, పాలు లేదా తెల్లని వస్త్రములు దానం చేయడం శ్రేయస్కరం.",
                "గర్భిణీ స్త్రీలు గ్రహణ కాలంలో విశ్రాంతిగా ఉంటూ శ్రీకృష్ణ శరణాష్టకం లేదా లలితా సహస్రనామ స్తోత్రం వినడం రక్షాకరము."
            ]
        else:
            shanti_remedies = [
                "సూర్య గ్రహణ సమయంలో ఆదిత్య హృదయ స్తోత్రం, గాయత్రీ మంత్రం లేదా సూర్యాష్టకం పారాయణ విశేష పుణ్యప్రదం.",
                "మోక్ష కాలం ముగిసిన వెంటనే (తీర్థ/శుద్ధోదక) స్నానం ఆచరించి సూర్య నమస్కారాలు చేయండి.",
                "గ్రహణ దోష రాశుల వారు (అనిష్ట రాశులు) గోధుమలు, బెల్లం, కెంపు (రూబీ) లేదా ఎరుపు వస్త్ర దానం చేయడం శ్రేయస్కరం.",
                "గర్భిణీ స్త్రీలు గ్రహణ కాలంలో ఇంటిలోనే ఉంటూ సంతాన గోపాల స్తోత్ర పారాయణ చేయడం రక్షాకరము."
            ]

        # 6. Calculate Topocentric Lagna Kundali at Eclipse Peak Time (మధ్య కాలం)
        lagna_kundali_data = None
        try:
            jd_ut = swe.julday(
                dt_madhya_utc.year, dt_madhya_utc.month, dt_madhya_utc.day,
                dt_madhya_utc.hour + dt_madhya_utc.minute / 60.0 + dt_madhya_utc.second / 3600.0
            )
            lagna_info_raw, _ = calculate_lagna_and_houses(jd_ut, lat, lon)
            planets_raw = calculate_planet_positions(jd_ut)
            lagna_enriched = enrich_lagna_details(lagna_info_raw["longitude"])
            enriched_planets = enrich_planets(planets_raw, lagna_info_raw["longitude"])
            d1_chart, d9_chart, _ = build_charts(lagna_enriched, enriched_planets)

            sun_p = next((p for p in enriched_planets if p["name_en"] == "Sun"), None)
            moon_p = next((p for p in enriched_planets if p["name_en"] == "Moon"), None)
            ecl_rashi_idx = sun_p["rashi_index"] if is_solar else (moon_p["rashi_index"] if moon_p else 0)
            lagna_rashi_idx = lagna_enriched["rashi_index"]
            ecl_bhava_num = ((ecl_rashi_idx - lagna_rashi_idx) % 12) + 1

            bhava_info = ECLIPSE_BHAVA_MEANINGS.get(ecl_bhava_num, {
                "title": f"{ecl_bhava_num}వ భావం",
                "desc": "ఈ భావంలో గ్రహణం సంభవించుటచే శాస్త్రోక్త శాంతి జపములు శ్రేయస్కరం."
            })

            lagna_kundali_data = {
                "lagna_rashi_index": lagna_rashi_idx,
                "lagna_rashi_name_te": lagna_enriched["rashi_name_te"],
                "lagna_degree_formatted": lagna_enriched["formatted_degree"],
                "lagna_nakshatra_te": lagna_enriched["nakshatra_name_te"],
                "lagna_pada": lagna_enriched["pada"],
                "eclipse_bhava": ecl_bhava_num,
                "eclipse_bhava_title_te": bhava_info["title"],
                "eclipse_bhava_impact_te": bhava_info["desc"],
                "charts": {
                    "d1": d1_chart,
                    "d9": d9_chart,
                    "lagna_rashi_index": lagna_rashi_idx
                },
                "planets": enriched_planets
            }
        except Exception as ex:
            print(f"Error computing eclipse lagna kundali: {ex}")

        item = {
            "id": e["id"],
            "name": e["sub_type"],
            "type": e["type"],
            "is_solar": is_solar,
            "is_lunar": is_lunar,
            "eclipse_kind": "solar" if is_solar else "lunar",
            "eclipse_kind_te": "సూర్య గ్రహణం" if is_solar else "చంద్ర గ్రహణం",
            "icon": "☀️" if is_solar else "🌕",
            "category": e.get("category", "పాక్షికం"),
            "date": dt_sparsha_loc.strftime("%Y-%m-%d"),
            "date_formatted": dt_sparsha_loc.strftime("%d-%B-%Y (%A)"),
            "is_visible_in_city": is_visible,
            "visibility_badge": vis_badge,
            "visibility_badge_class": vis_badge_class,
            "visibility_note": vis_note,
            "timings": {
                "local_sparsha": dt_sparsha_loc.strftime("%d-%b-%Y, %I:%M %p %Z"),
                "local_madhya": dt_madhya_loc.strftime("%d-%b-%Y, %I:%M %p %Z"),
                "local_moksha": dt_moksha_loc.strftime("%d-%b-%Y, %I:%M %p %Z"),
                "duration": dur_text,
                "utc_sparsha": e["utc_sparsha"],
                "utc_madhya": e["utc_madhya"],
                "utc_moksha": e["utc_moksha"],
                "ist_sparsha": e["ist_sparsha"],
                "ist_madhya": e["ist_madhya"],
                "ist_moksha": e["ist_moksha"]
            },
            "sutaka": {
                "applicable": is_visible,
                "start": dt_sutaka_start.strftime("%d-%b-%Y, %I:%M %p %Z"),
                "end": dt_sutaka_end.strftime("%d-%b-%Y, %I:%M %p %Z"),
                "rule_hours": f"{sutaka_hours} గంటల ముందు ({'నాల్గు జాములు/Four Praharas' if is_solar else 'మూడు జాములు/Three Praharas'})",
                "rules_te": f"సూతక కాలం గ్రహణ స్పర్శకు {sutaka_hours} గంటల ముందు ({dt_sutaka_start.strftime('%I:%M %p')}) నుండి ప్రారంభమవుతుంది. ఈ సమయంలో దేవాలయ దర్శనాలు, భోజనం నిషిద్ధం."
            },
            "astrology": {
                "rashi_name_te": e["rashi_name_te"],
                "nakshatra_name_te": e["nakshatra_name_te"],
                "rashi_impacts": e["rashi_impacts"]
            },
            "shanti_remedies": shanti_remedies,
            "lagna_kundali": lagna_kundali_data
        }
        all_results.append(item)

    # Filter by eclipse_type if requested
    req_type = (eclipse_type or "all").lower().strip()
    if req_type == "lunar":
        filtered_results = [ec for ec in all_results if ec["is_lunar"]]
    elif req_type == "solar":
        filtered_results = [ec for ec in all_results if ec["is_solar"]]
    else:
        filtered_results = all_results

    # Filter out non-visible eclipses if visible_only is True
    if visible_only:
        filtered_results = [ec for ec in filtered_results if ec["is_visible_in_city"]]

    return {
        "city": city_clean,
        "country": country,
        "year": selected_year,
        "timezone": tz_name,
        "coordinates": f"{lat:.4f}° N, {lon:.4f}° E",
        "eclipse_type": req_type,
        "visible_only": visible_only,
        "total_eclipses": len(all_results),
        "total_lunar_count": total_lunar,
        "total_solar_count": total_solar,
        "visible_eclipses_count": visible_count,
        "visible_lunar_count": visible_lunar,
        "visible_solar_count": visible_solar,
        "eclipses": filtered_results
    }


def get_worldwide_eclipses(year: int = 2026) -> Dict[str, Any]:
    """
    Returns Worldwide Solar and Lunar Eclipses for the requested year,
    complete with UTC & IST timings, global visibility, and 12-Rashi impacts.
    """
    selected_year = year if year in ECLIPSES_DATABASE else 2026
    eclipses = ECLIPSES_DATABASE[selected_year]

    return {
        "year": selected_year,
        "available_years": [2024, 2025, 2026, 2027, 2028],
        "total_eclipses": len(eclipses),
        "eclipses": eclipses,
        "universal_rules": [
            "గ్రహణ సూతక కాలం: సూర్య గ్రహణానికి 12 గంటల ముందు నుండి, చంద్ర గ్రహణానికి 9 గంటల ముందు నుండి సూతకం ప్రారంభమవుతుంది.",
            "గర్భిణీ స్త్రీలకు మార్గదర్శకాలు: గ్రహణ సమయంలో నేరుగా గ్రహణాన్ని చూడటం, పదునైన వస్తువులు వాడటం నిషిద్ధం. గదిలో ఉంటూ శ్రీకృష్ణ శరణాష్టకం లేదా గాయత్రీ మంత్రం జపించడం శుభకరం.",
            "గ్రహణ కాల పుణ్యఫలం: గ్రహణ సమయంలో చేసిన జపం, ధ్యానం, స్తోత్ర పారాయణ సాధారణ కాలంలో కంటే లక్షల రెట్లు అధిక పుణ్యఫలాన్ని ఇస్తాయి.",
            "గ్రహణ మోక్షానంతరం: మోక్ష కాలం ముగిసిన తర్వాత స్నానం చేసి, దైవ దర్శనం మరియు బియ్యం, గోధుమలు, వస్త్రములు లేదా యథాశక్తి దానం చేయడం శ్రేయస్కరం."
        ]
    }

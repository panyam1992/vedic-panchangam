"""
Comprehensive Top-to-Bottom End-to-End Test Suite for Vedic Samhita:
Unified Panchangam & Jyotishyam Web Platform.
Tests all APIs, astronomical calculations, Shastric rules, and frontend endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# ==============================================================================
# 1. WEB APP & STATIC ASSET TESTS (PWA & FRONTEND ENDPOINTS)
# ==============================================================================

class TestWebAppsAndStaticAssets:
    """Tests all HTML pages, switchers, stylesheets, and scripts."""

    def test_panchangam_root_serves_html(self):
        """Verify root / serves Panchangam app with Jyotishyam button when requested by browser."""
        resp = client.get("/", headers={"accept": "text/html"})
        assert resp.status_code == 200
        assert "వేద సంహిత" in resp.text or "Panchangam" in resp.text
        # Must contain bidirectional link to Jyotishyam
        assert 'href="/jyotishyam"' in resp.text
        assert "జ్యోతిష్యం & ముహూర్తం" in resp.text

    def test_panchangam_app_endpoint(self):
        """Verify /app direct endpoint serves Panchangam."""
        resp = client.get("/app")
        assert resp.status_code == 200
        assert len(resp.text) > 1000

    def test_jyotishyam_web_endpoint(self):
        """Verify /jyotishyam serves Jyotishyam app with Panchangam switcher."""
        resp = client.get("/jyotishyam")
        assert resp.status_code == 200
        assert "జ్యోతిష్యం" in resp.text
        # Must contain bidirectional link back to Panchangam
        assert 'href="/"' in resp.text
        assert "పంచాంగం (Panchangam)" in resp.text
        # Check module navigation buttons
        assert 'data-module="moduleKundali"' in resp.text
        assert 'data-module="moduleMuhurtam"' in resp.text
        assert 'data-module="moduleShishu"' in resp.text
        assert 'data-module="modulePrashna"' in resp.text
        assert 'data-module="moduleEclipses"' in resp.text

    def test_jyotishyam_trailing_slash(self):
        """Verify /jyotishyam/ works identically."""
        resp = client.get("/jyotishyam/")
        assert resp.status_code == 200
        assert "జ్యోతిష్యం" in resp.text

    def test_static_css_and_js_accessibility(self):
        """Verify that all CSS and JS files exist and are served with 200."""
        css_resp = client.get("/static/jyotishyam/css/style.css")
        assert css_resp.status_code == 200
        assert len(css_resp.text) > 500

        app_js_resp = client.get("/static/jyotishyam/js/app.js")
        assert app_js_resp.status_code == 200
        assert len(app_js_resp.text) > 5000

        chart_js_resp = client.get("/static/jyotishyam/js/chart_renderer.js")
        assert chart_js_resp.status_code == 200
        assert len(chart_js_resp.text) > 1000

    def test_health_check(self):
        """Verify health check endpoint."""
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


# ==============================================================================
# 2. PANCHANGAM CORE API TESTS
# ==============================================================================

class TestPanchangamCoreApi:
    """Tests Daily Panchangam, Monthly, Cities, Sankalpam, and Rashi Phalalu."""

    def test_daily_panchangam_hyderabad_telugu(self):
        """Test daily Panchangam for Hyderabad with complete 5 Angas."""
        resp = client.get("/api/v1/panchangam/daily?city=Hyderabad&language=telugu")
        assert resp.status_code == 200
        data = resp.json()
        assert "angas" in data
        assert "tithis" in data["angas"]
        assert len(data["angas"]["tithis"]) > 0
        assert "nakshatras" in data["angas"]
        assert len(data["angas"]["nakshatras"]) > 0
        assert "yogas" in data["angas"]
        assert "karanas" in data["angas"]
        assert "vara" in data["angas"]
        assert "sun_moon" in data
        assert "sunrise" in data["sun_moon"]
        assert "sunset" in data["sun_moon"]
        assert "lagnas" in data
        assert len(data["lagnas"]) > 0

    def test_daily_panchangam_diaspora_frisco_english(self):
        """Test daily Panchangam for diaspora city (Frisco, TX, USA) with negative UTC offset."""
        resp = client.get("/api/v1/panchangam/daily?city=Frisco&language=english")
        assert resp.status_code == 200
        data = resp.json()
        assert "angas" in data
        assert "tithis" in data["angas"]
        assert "nakshatras" in data["angas"]
        assert "sun_moon" in data
        assert "sunrise" in data["sun_moon"]

    def test_monthly_panchangam(self):
        """Test monthly calendar generation."""
        resp = client.get("/api/v1/panchangam/monthly?city=Hyderabad&year=2026&month=4&language=telugu")
        assert resp.status_code == 200
        data = resp.json()
        assert "days" in data
        assert len(data["days"]) >= 28

    def test_city_search(self):
        """Test city autocomplete search."""
        resp = client.get("/api/v1/cities/search?q=Hyd&limit=5")
        assert resp.status_code == 200
        data = resp.json()
        assert "cities" in data
        assert len(data["cities"]) > 0
        assert any("hyderabad" in c["name"].lower() for c in data["cities"])

    def test_city_popular(self):
        """Test popular cities list."""
        resp = client.get("/api/v1/cities/popular")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_sankalpam_generator_india(self):
        """Test Deśa-Kāla Sankalpam for India (Jambu Dveepe)."""
        resp = client.get("/api/v1/sankalpam/generate?city=Hyderabad&language=telugu&gotra=Kashyapa&sharma_name=Rama")
        assert resp.status_code == 200
        data = resp.json()
        assert "sankalpam" in data
        assert "sankalpam_text" in data["sankalpam"]
        assert len(data["sankalpam"]["sankalpam_text"]) > 50

    def test_sankalpam_generator_usa(self):
        """Test Deśa-Kāla Sankalpam for Americas (Krauncha Dveepe)."""
        resp = client.get("/api/v1/sankalpam/generate?city=Dallas&language=telugu")
        assert resp.status_code == 200
        data = resp.json()
        assert "sankalpam" in data
        assert "sankalpam_text" in data["sankalpam"]
        assert len(data["sankalpam"]["sankalpam_text"]) > 50

    def test_daily_rashi_phalalu(self):
        """Test daily 12 rashi horoscope and Chandrashtama detection."""
        resp = client.get("/api/v1/rashi/daily?language=telugu")
        assert resp.status_code == 200
        data = resp.json()
        assert "rashis" in data
        assert len(data["rashis"]) == 12


# ==============================================================================
# 3. JYOTISHYAM KUNDALI & SHASTRA ENGINE TESTS
# ==============================================================================

class TestJyotishyamKundaliEngine:
    """Tests birth horoscope generation, D1, D9, Santana, and Remedies."""

    def test_purusha_jataka_generation(self):
        """Verify Purusha (Male) horoscope calculation with D1 and D9."""
        payload = {
            "name": "శ్రీధర్ శర్మ",
            "gender": "male",
            "dob": "1990-08-25",
            "tob": "06:45",
            "place_name": "Hyderabad",
            "latitude": 17.3850,
            "longitude": 78.4867,
            "timezone_offset": 5.5,
            "ayanamsa": "lahiri"
        }
        resp = client.post("/api/v1/kundali/generate", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["input"]["gender"] == "male"
        assert "d1_chart" in data
        assert "d9_chart" in data
        assert "lagna" in data
        assert "planets" in data
        assert len(data["planets"]) >= 8  # Sun through Rahu
        assert "panchangam" in data
        assert "dasha" in data
        assert "yogas" in data
        assert "gender_highlights" in data

    def test_stree_jataka_generation(self):
        """Verify Stree (Female) horoscope with classical Stree Jataka Saubhagya indicators."""
        payload = {
            "name": "లక్ష్మి ప్రసన్న",
            "gender": "female",
            "dob": "1994-11-12",
            "tob": "14:20",
            "place_name": "Tirupati",
            "latitude": 13.6288,
            "longitude": 79.4192,
            "timezone_offset": 5.5,
            "ayanamsa": "lahiri"
        }
        resp = client.post("/api/v1/kundali/generate", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["input"]["gender"] == "female"
        assert "gender_highlights" in data
        assert "స్త్రీ" in data["gender_highlights"].get("gender_category", "") or "స్త్రీ" in data["gender_highlights"].get("title_te", "")

    def test_couple_joint_dosha_audit(self):
        """Verify Couple Joint Dosha audit endpoint."""
        payload = {
            "husband": {
                "name": "రాము",
                "gender": "male",
                "dob": "1990-05-10",
                "tob": "07:15",
                "place_name": "Hyderabad",
                "latitude": 17.3850,
                "longitude": 78.4867,
                "timezone_offset": 5.5
            },
            "wife": {
                "name": "సీత",
                "gender": "female",
                "dob": "1993-08-20",
                "tob": "11:30",
                "place_name": "Hyderabad",
                "latitude": 17.3850,
                "longitude": 78.4867,
                "timezone_offset": 5.5
            }
        }
        resp = client.post("/api/v1/kundali/couple-analyze", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "success"
        assert "husband_kundali" in data
        assert "wife_kundali" in data
        assert "joint_analysis" in data
        assert "santana_joint" in data["joint_analysis"]
        assert "kuja_samya" in data["joint_analysis"]

    def test_santana_sphuta_analysis(self):
        """Verify Santana Sphuta and Pregnancy Loss analysis."""
        payload = {
            "name": "శ్రీధర్ శర్మ",
            "gender": "male",
            "dob": "1990-08-25",
            "tob": "06:45",
            "place_name": "Hyderabad",
            "latitude": 17.3850,
            "longitude": 78.4867,
            "timezone_offset": 5.5,
            "ayanamsa": "lahiri"
        }
        resp = client.post("/api/v1/muhurtam/santana-analysis", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "success"
        assert "santana_analysis" in data
        assert "sphutas" in data["santana_analysis"]
        assert "beeja_sphuta" in data["santana_analysis"]["sphutas"]
        assert "kshetra_sphuta" in data["santana_analysis"]["sphutas"]
        assert "recommended_muhurtams" in data

    def test_remedy_audit_verification(self):
        """Verify Shastric Remedy Verification & Recheck engine."""
        payload = {
            "name": "శ్రీధర్ శర్మ",
            "gender": "male",
            "dob": "1990-08-25",
            "tob": "06:45",
            "place_name": "Hyderabad",
            "latitude": 17.3850,
            "longitude": 78.4867,
            "timezone_offset": 5.5,
            "ayanamsa": "lahiri"
        }
        resp = client.post("/api/v1/kundali/verify-remedy", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "success"
        assert "remedy_verification" in data
        assert len(data["remedy_verification"]) > 0


# ==============================================================================
# 4. VEDIC MUHURTAM CALCULATOR (WITH NO-DOB/PRIEST STANDALONE SUPPORT)
# ==============================================================================

class TestVedicMuhurtamCalculator:
    """Tests all 3 Muhurtam modes including Universal Panchanga & Abhijit Shuddhi."""

    def test_muhurtam_universal_panchanga_no_dob(self):
        """
        Verify Mode 3: Universal Panchanga & Abhijit Shuddhi.
        Native has NO birth details (native_nakshatra_index=None, native_rashi_index=None).
        Must calculate valid slots based on Tithi, Vara, Nakshatra, Shiva Vasa, Abhijit.
        """
        payload = {
            "event_type": "naga_pratishtha",
            "start_date": "2026-10-01",
            "days_range": 30,
            "latitude": 17.3850,
            "longitude": 78.4867,
            "timezone_offset": 5.5,
            "native_nakshatra_index": None,
            "native_rashi_index": None,
            "participant_mode": "individual",
            "limit": 5
        }
        resp = client.post("/api/v1/muhurtam/calculate", json=payload)
        assert resp.status_code == 200
        res = resp.json()
        assert res["status"] == "success"
        data = res["data"]
        assert "top_muhurtams" in data
        picks = data["top_muhurtams"]
        assert len(picks) > 0
        # Check first ranked Muhurtam slot details
        m1 = picks[0]
        assert "formatted_date" in m1
        assert "best_window" in m1
        assert "classification" in m1
        assert "tithi" in m1
        assert "nakshatra" in m1
        assert "rahu_kalam" in m1
        assert "yamagandam" in m1
        assert "varjyam" in m1

    def test_muhurtam_with_nakshatra_tara_bala(self):
        """
        Verify Mode 2: Direct Nakshatra pick.
        Calculates personalized Tara Bala & Chandra Bala for Rohini (idx 3) & Vrishabha (idx 1).
        """
        payload = {
            "event_type": "vivaha",
            "start_date": "2026-11-01",
            "days_range": 45,
            "latitude": 17.3850,
            "longitude": 78.4867,
            "timezone_offset": 5.5,
            "native_nakshatra_index": 3,  # Rohini
            "native_rashi_index": 1,      # Vrishabha
            "participant_mode": "individual",
            "limit": 5
        }
        resp = client.post("/api/v1/muhurtam/calculate", json=payload)
        assert resp.status_code == 200
        res = resp.json()
        assert res["status"] == "success"
        picks = res["data"]["top_muhurtams"]
        assert len(picks) > 0
        assert "tara_bala" in picks[0]
        assert "chandra_bala" in picks[0]

    def test_muhurtam_couple_mode_harmony(self):
        """
        Verify Couple Mode: Both husband & wife evaluated simultaneously,
        avoiding Ashtama Chandra and Naidhana Tara for both.
        """
        payload = {
            "event_type": "santana_gopala",
            "start_date": "2026-10-15",
            "days_range": 30,
            "latitude": 17.3850,
            "longitude": 78.4867,
            "timezone_offset": 5.5,
            "participant_mode": "couple",
            "family_members": [
                {"name": "శ్రీనివాస్ (భర్త)", "role": "husband", "nakshatra_index": 0, "rashi_index": 0},
                {"name": "పద్మ (భార్య)", "role": "wife", "nakshatra_index": 3, "rashi_index": 1}
            ],
            "limit": 5
        }
        resp = client.post("/api/v1/muhurtam/calculate", json=payload)
        assert resp.status_code == 200
        res = resp.json()
        assert res["status"] == "success"
        picks = res["data"]["top_muhurtams"]
        assert len(picks) > 0
        # Verify couple breakdown exists
        assert "family_compatibility" in picks[0]
        assert len(picks[0]["family_compatibility"]["members"]) == 2

    def test_muhurtam_events_catalog(self):
        """Verify catalog of all 36 supported Vedic Muhurtam ceremonies."""
        resp = client.get("/api/v1/muhurtam/event-types")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "success"
        assert "pariharams" in data
        assert "samskaras" in data
        assert data["total_events"] == 36
        all_codes = [e["code"] for e in data["pariharams"]] + [e["code"] for e in data["samskaras"]]
        assert "naga_pratishtha" in all_codes
        assert "kuja_shanti_subrahmanya" in all_codes
        assert "santana_gopala" in all_codes
        assert "vivaha" in all_codes
        assert "grihapravesha" in all_codes
        # New additions
        assert "aksharabhyasa" in all_codes
        assert "shanku_sthapana" in all_codes
        assert "dwara_bandha" in all_codes
        assert "bhoomi_puja" in all_codes
        assert "borewell_kupa" in all_codes
        assert "udyoga_pravesha" in all_codes
        assert "runa_vimukthi" in all_codes
        assert "swarnabharana_dharana" in all_codes
        assert "satyanarayana_vratam" in all_codes
        assert "mrityunjaya_ayushya" in all_codes
        assert "devata_pratishtha" in all_codes

    def test_muhurtam_new_events_calculation(self):
        """Verify calculation for newly added Muhurtams (Aksharabhyasa & Shanku Sthapana)."""
        payload = {
            "event_type": "aksharabhyasa",
            "start_date": "2026-10-01",
            "days_range": 30,
            "latitude": 17.3850,
            "longitude": 78.4867,
            "timezone_offset": 5.5,
            "native_nakshatra_index": 3,
            "native_rashi_index": 1,
            "limit": 3
        }
        resp = client.post("/api/v1/muhurtam/calculate", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "success"
        assert len(data["data"]["top_muhurtams"]) > 0
        assert "అక్షరాభ్యాసం" in data["data"]["event_title_te"]


# ==============================================================================
# 5. NEWBORN HOROSCOPE (SHISHU JATAKAM)
# ==============================================================================

class TestShishuJatakamEngine:
    """Tests baby naming syllables, Gandanta Doshas, Nakshatra Paya."""

    def test_shishu_jatakam_ashwini(self):
        """Test infant born in Ashwini: naming syllables and Nakshatra Paya."""
        payload = {
            "name": "చిరంజీవి కార్తికేయ",
            "gender": "male",
            "dob": "2026-05-10",
            "tob": "09:30",
            "place_name": "Hyderabad",
            "latitude": 17.3850,
            "longitude": 78.4867,
            "timezone_offset": 5.5,
            "ayanamsa": "lahiri"
        }
        resp = client.post("/api/v1/shishu/generate", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "recommended_naming_syllables" in data
        assert len(data["recommended_naming_syllables"]) == 4
        assert "panchangam" in data
        assert "charts" in data
        assert "d1" in data["charts"]
        assert "d9" in data["charts"]
        assert "doshas" in data


# ==============================================================================
# 6. HORARY PRASHNA (PRASHNA MARGA & TAJIKA)
# ==============================================================================

class TestPrashnaEngine:
    """Tests 1-249 Horary query calculation, Karya Bhava, and Tajika Yogas."""

    def test_prashna_career_query(self):
        """Test career question with Tajika aspect analysis."""
        payload = {
            "query_text": "నాతో నూతన ప్రాజెక్ట్ ప్రారంభం సఫలమౌతుందా?",
            "prashna_number": 72,
            "category": "job",
            "latitude": 17.3850,
            "longitude": 78.4867,
            "timezone_offset": 5.5
        }
        resp = client.post("/api/v1/prashna/calculate", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "question_id" in data
        assert "karya_bhava" in data
        assert data["karya_bhava"] == 10  # 10th house for career/job
        assert "verdict" in data
        assert "score_percent" in data
        assert "timing_estimate" in data
        assert "remedies" in data

    def test_prashna_categories_list(self):
        """Test list of supported Prashna categories."""
        resp = client.get("/api/v1/prashna/categories")
        assert resp.status_code == 200
        data = resp.json()
        assert "categories" in data
        assert len(data["categories"]) >= 8


# ==============================================================================
# 7. ECLIPSE CALCULATOR (GRAHANA DARSHINI)
# ==============================================================================

class TestEclipseEngine:
    """Tests city-specific Solar & Lunar eclipse visibility & timings."""

    def test_city_eclipse_mckinney_2028(self):
        """Verify McKinney, TX 2028 eclipses."""
        payload = {
            "year": 2028,
            "country": "US",
            "city": "McKinney",
            "latitude": 33.1976,
            "longitude": -96.6178,
            "timezone_name": "America/Chicago",
            "timezone_offset": -5.0,
            "eclipse_type": "all",
            "visible_only": False,
            "language": "te"
        }
        resp = client.post("/api/v1/eclipses/calculate-city", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "city" in data
        assert data["city"] == "McKinney"
        assert "eclipses" in data
        assert len(data["eclipses"]) > 0
        first_ecl = data["eclipses"][0]
        assert "timings" in first_ecl
        assert "category" in first_ecl
        assert "visibility_badge" in first_ecl

    def test_worldwide_eclipses(self):
        """Verify worldwide astronomical eclipse catalog."""
        resp = client.get("/api/v1/eclipses/2028")
        assert resp.status_code == 200
        data = resp.json()
        assert "eclipses" in data
        assert len(data["eclipses"]) > 0


# ==============================================================================
# 8. MULTI-SCRIPT INDIC TRANSLITERATION ENGINE
# ==============================================================================

class TestTransliterationEngine:
    """Tests Aksharamukha script conversion across Indian languages."""

    @pytest.mark.parametrize("target_script", [
        "Devanagari", "Tamil", "Kannada", "Malayalam", "Bengali", "Gujarati", "Oriya", "Gurmukhi", "IAST"
    ])
    def test_telugu_to_indic_scripts(self, target_script):
        """Test Telugu to all supported Indian scripts."""
        sample_text = ["శ్రీరస్తు", "శుభమస్తు", "అవిఘ్నమస్తు"]
        payload = {
            "texts": sample_text,
            "target_script": target_script,
            "source_script": "Telugu"
        }
        resp = client.post("/api/v1/languages/transliterate", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "texts" in data
        assert len(data["texts"]) == len(sample_text)
        # Transliterated output must not be empty and must differ from original if not Telugu
        for t in data["texts"]:
            assert len(t) > 0
            if target_script != "Telugu":
                assert t != sample_text[0]

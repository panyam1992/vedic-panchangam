"""
Integration tests for Jyotishyam module mounted in Vedic Samhita Panchangam system.
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_jyotishyam_web_endpoint():
    """Verify that /jyotishyam serves the HTML interface."""
    resp = client.get("/jyotishyam")
    assert resp.status_code == 200
    assert "జ్యోతిష్యం" in resp.text
    assert "/static/jyotishyam/css/style.css" in resp.text


def test_kundali_generate_api():
    """Verify that birth horoscope calculation functions seamlessly."""
    payload = {
        "name": "వెంకటేశ్వర రావు",
        "gender": "male",
        "dob": "1992-05-15",
        "tob": "08:30",
        "place_name": "Hyderabad",
        "latitude": 17.3850,
        "longitude": 78.4867,
        "timezone_offset": 5.5,
        "ayanamsa": "lahiri"
    }
    resp = client.post("/api/v1/kundali/generate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "panchangam" in data
    assert "d1_chart" in data
    assert "d9_chart" in data


def test_muhurtam_calculate_api():
    """Verify that Muhurtam calculator works with universal Panchanga Shuddhi."""
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
    res_data = resp.json()
    assert res_data["status"] == "success"
    assert "top_muhurtams" in res_data["data"]
    assert len(res_data["data"]["top_muhurtams"]) > 0


def test_shishu_jatakam_api():
    """Verify newborn horoscope naming syllables and Gandanta check."""
    payload = {
        "name": "చిరు ప్రద్యుమ్న",
        "gender": "male",
        "dob": "2026-08-20",
        "tob": "10:15",
        "place_name": "Proddatur",
        "latitude": 14.7504,
        "longitude": 78.5528,
        "timezone_offset": 5.5
    }
    resp = client.post("/api/v1/shishu/generate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "recommended_naming_syllables" in data


def test_prashna_calculate_api():
    """Verify Horary Prashna Kundali generation."""
    payload = {
        "query_text": "ఉద్యోగంలో అభివృద్ధి కలుగుతుందా?",
        "prashna_number": 108,
        "latitude": 17.3850,
        "longitude": 78.4867,
        "timezone_offset": 5.5
    }
    resp = client.post("/api/v1/prashna/calculate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "question_id" in data
    assert "verdict" in data


def test_city_eclipses_api():
    """Verify eclipse calculations for worldwide cities."""
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
    assert "eclipses" in data
    assert len(data["eclipses"]) > 0


def test_transliteration_api():
    """Verify multi-script Indic transliteration via Aksharamukha."""
    payload = {
        "texts": ["శ్రీ వేద సంహిత", "జ్యోతిష్య శాస్త్రం"],
        "target_script": "Devanagari",
        "source_script": "Telugu"
    }
    resp = client.post("/api/v1/languages/transliterate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "texts" in data
    assert len(data["texts"]) == 2

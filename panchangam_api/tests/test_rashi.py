"""
Tests for Rashi Phalalu (Daily, Monthly, Yearly) API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
API_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, API_ROOT)

from main import app

client = TestClient(app)


def test_daily_rashi_endpoint():
    res = client.get("/api/v1/rashi/daily?date=2026-03-19&language=telugu")
    assert res.status_code == 200
    data = res.json()
    assert "rashis" in data
    assert len(data["rashis"]) == 12
    assert data["date"] == "2026-03-19"
    assert data["language"] == "telugu"

    # Verify each rashi structure
    chandrashtama_count = 0
    for item in data["rashis"]:
        assert "rashi" in item
        assert "moon_house" in item
        assert 1 <= item["moon_house"] <= 12
        assert "score_percent" in item
        assert 35 <= item["score_percent"] <= 95
        assert "lucky_number" in item
        assert "lucky_color" in item
        assert "predictions" in item
        assert "general" in item["predictions"]
        assert "career" in item["predictions"]
        assert "remedy" in item

        if item["is_chandrashtama"]:
            chandrashtama_count += 1
            assert item["moon_house"] == 8
            assert "చంద్రాష్టమ" in item["chandra_bala_status"]

    # Exactly one rashi must be in Chandrashtama on any given day
    assert chandrashtama_count == 1


def test_monthly_rashi_endpoint():
    res = client.get("/api/v1/rashi/monthly?year=2026&month=3&language=telugu")
    assert res.status_code == 200
    data = res.json()
    assert "rashis" in data
    assert len(data["rashis"]) == 12
    assert data["year"] == 2026
    assert data["month"] == 3
    assert data["solar_month"] != ""

    for item in data["rashis"]:
        assert 1 <= item["sun_house"] <= 12
        assert "is_sun_favorable" in item
        assert "highlights" in item
        assert len(item["highlights"]) > 0


def test_yearly_rashi_kandadayam():
    res = client.get("/api/v1/rashi/yearly?year=2026&language=telugu")
    assert res.status_code == 200
    data = res.json()
    assert "rashis" in data
    assert len(data["rashis"]) == 12
    assert "పరాభవ" in data["samvatsara"]

    for item in data["rashis"]:
        kd = item["kandadayam"]
        assert "aadhayam" in kd
        assert "vyayam" in kd
        assert "rajapujyam" in kd
        assert "avamanam" in kd
        assert 0 <= kd["aadhayam"] <= 15
        assert 0 <= kd["vyayam"] <= 15
        assert 0 <= kd["rajapujyam"] <= 8
        assert 0 <= kd["avamanam"] <= 8
        assert "finance_status" in kd
        assert "social_status" in kd

        # Check planetary status
        assert 1 <= item["jupiter_house"] <= 12
        assert "has_guru_balam" in item
        assert 1 <= item["saturn_house"] <= 12
        assert "sade_sati_status" in item
        assert "rahu_ketu_status" in item


def test_rashi_multilingual():
    # Test English
    res_en = client.get("/api/v1/rashi/daily?date=2026-03-19&language=english")
    assert res_en.status_code == 200
    data_en = res_en.json()
    assert data_en["rashis"][0]["rashi"]["name"] == "Aries"
    assert data_en["rashis"][0]["rashi"]["lord"] == "Mars"

    # Test Devanagari
    res_dev = client.get("/api/v1/rashi/daily?date=2026-03-19&language=devanagari")
    assert res_dev.status_code == 200
    data_dev = res_dev.json()
    assert data_dev["rashis"][0]["rashi"]["name"] == "मेष"

    # Test Tamil
    res_ta = client.get("/api/v1/rashi/daily?date=2026-03-19&language=tamil")
    assert res_ta.status_code == 200
    data_ta = res_ta.json()
    assert data_ta["rashis"][0]["rashi"]["name"] == "மேஷம்"


def test_comprehensive_kandadayam_endpoint():
    res = client.get("/api/v1/rashi/kandadayam-all?year=2026&language=telugu")
    assert res.status_code == 200
    data = res.json()

    assert "samvatsara" in data
    assert "పరాభవ" in data["samvatsara"]
    assert "explanation" in data
    assert "rashis" in data
    assert len(data["rashis"]) == 12
    assert "nakshatras" in data
    assert len(data["nakshatras"]) == 27

    # Check 1st Nakshatra (Ashwini)
    ashwini = data["nakshatras"][0]
    assert ashwini["id"] == 1
    assert "అశ్వినీ" in ashwini["name"]
    assert ashwini["trimester_1"]["score"] == 4
    assert ashwini["trimester_2"]["score"] == 2
    assert ashwini["trimester_3"]["score"] == 1
    assert "చైత్రం" in ashwini["trimester_1"]["months"]
    assert "శ్రావణం" in ashwini["trimester_2"]["months"]
    assert "మార్గశిరం" in ashwini["trimester_3"]["months"]

    # Check 2nd Nakshatra (Bharani: 7, 0, 3)
    bharani = data["nakshatras"][1]
    assert bharani["id"] == 2
    assert "భరణీ" in bharani["name"]
    assert bharani["trimester_1"]["score"] == 7
    assert bharani["trimester_2"]["score"] == 0
    assert bharani["trimester_3"]["score"] == 3

    # Check English localization
    res_en = client.get("/api/v1/rashi/kandadayam-all?year=2026&language=english")
    assert res_en.status_code == 200
    data_en = res_en.json()
    assert data_en["nakshatras"][0]["name"] == "Ashwini"


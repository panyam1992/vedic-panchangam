import pytest
from fastapi.testclient import TestClient
from main import app
from services.intercalary_service import (
    calculate_solar_lunar_drift,
    get_kaliyuga_epoch_statistics,
    get_intercalary_months_range,
    get_intercalary_status_for_date
)

client = TestClient(app)


def test_solar_lunar_drift():
    drift = calculate_solar_lunar_drift()
    assert drift["diff_per_year_days"] == 11
    assert drift["months_for_adhika_masa"] == 32.5
    assert drift["vedanga_jyotisha_rule"]["solar_months"] == 60
    assert drift["vedanga_jyotisha_rule"]["lunar_months"] == 62
    assert drift["vedanga_jyotisha_rule"]["adhika_masas_in_5_years"] == 2


def test_kaliyuga_epoch_statistics():
    kali = get_kaliyuga_epoch_statistics()
    assert kali["kaliyuga_duration_years"] == 432000
    assert kali["total_adhika_masas"] == 168152
    assert kali["total_kshaya_masas"] == 8718
    assert kali["net_adhika_masas"] == 159034


def test_intercalary_months_surya_siddhanta():
    months = get_intercalary_months_range(2026, 2036, "surya_siddhanta", "telugu")
    assert len(months) >= 5
    
    # 2026: Adhika Jyeshtha
    m2026 = [m for m in months if m["year"] == 2026 and m["classification"] == "ADHIKA"]
    assert len(m2026) == 1
    assert "జ్యేష్ఠ" in m2026[0]["masa_name_telugu"]

    # 2028: Keelaka has Samsarpa Kartika and Kshaya Margashirsha-Pushya
    m2028_samsarpa = [m for m in months if m["year"] == 2028 and m["classification"] == "SAMSARPA"]
    assert len(m2028_samsarpa) == 1
    assert "కార్తిక" in m2028_samsarpa[0]["masa_name_telugu"]

    m2028_kshaya = [m for m in months if m["year"] == 2028 and m["classification"] == "KSHAYA"]
    assert len(m2028_kshaya) == 1
    assert m2028_kshaya[0]["sankranti_count"] == 2


def test_api_intercalary_endpoints():
    # 1. Months range endpoint
    res = client.get("/api/v1/panchangam/intercalary-months?start_year=2026&end_year=2036&system=surya_siddhanta&language=telugu")
    assert res.status_code == 200
    data = res.json()
    assert data["count"] >= 5
    assert data["calculation_system"] == "surya_siddhanta"
    assert any(m["classification"] == "KSHAYA" for m in data["months"])
    assert any(m["classification"] == "SAMSARPA" for m in data["months"])

    # 2. Theory endpoint
    res_th = client.get("/api/v1/panchangam/intercalary-theory?language=telugu")
    assert res_th.status_code == 200
    theory = res_th.json()
    assert "అసంక్రాంతావేకవర్షౌ" in theory["kalamadhava_canonical_rule"]["verse_telugu"]
    assert theory["kaliyuga_epoch_balance"]["net_adhika_masas"] == 159034

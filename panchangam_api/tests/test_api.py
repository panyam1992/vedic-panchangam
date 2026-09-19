"""
Comprehensive automated test suite for Global Vedic Panchangam API.
Validates:
1. Endpoints availability (Root, Health, Cities, Daily, Monthly, Sankalpam)
2. All 3 traditional Mana Systems (Chandramana, Sauramana, Barhaspatyamana)
3. Ugadi 2026 Samvatsara transition to Parabhava (పరాభవః)
4. Multilingual transliteration across Indian languages (Telugu, Devanagari, Tamil, Kannada, English)
5. Vedic Deśa-Kāla Sankalpa customization
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_and_health():
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "online"
    assert "telugu" in data["supported_languages"]

    h_res = client.get("/health")
    assert h_res.status_code == 200
    assert h_res.json()["status"] == "healthy"


def test_cities_search():
    res = client.get("/api/v1/cities/search?q=Frisco")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 1
    frisco = data["cities"][0]
    assert frisco["name"] == "Frisco"
    assert frisco["state"] == "Texas"
    assert frisco["tz"] == "America/Chicago"


def test_popular_cities():
    res = client.get("/api/v1/cities/popular")
    assert res.status_code == 200
    cities = res.json()
    names = [c["name"] for c in cities]
    assert "Hyderabad" in names
    assert "Frisco" in names


def test_daily_panchangam_ugadi_2026_telugu():
    """Test Parabhava Samvatsara Ugadi on 2026-03-19 for Frisco in Telugu."""
    res = client.get("/api/v1/panchangam/daily?city=Frisco&date=2026-03-19&language=telugu")
    assert res.status_code == 200
    data = res.json()

    # 1. Chandramana Check
    chandramana = data["chandramana"]
    assert "పరాభవ" in chandramana["samvatsara"]["name"]
    assert "శుక్ల" in chandramana["paksha"] or "Shukla" in chandramana["paksha"]

    # 2. Sauramana Check (Tamil, Malayalam, Bengali, Odia)
    sauramana = data["sauramana"]
    assert "regional_solar_calendars" in sauramana
    assert "tamil" in sauramana["regional_solar_calendars"]
    assert "malayalam_kollam" in sauramana["regional_solar_calendars"]

    # 3. Barhaspatyamana Check (Jupiter Jovian Cycle & Pushkaram)
    barhaspatya = data["barhaspatyamana"]
    assert "jupiter_position" in barhaspatya
    assert "jovian_cycle_12_year" in barhaspatya
    assert "sacred_river_pushkaram" in barhaspatya

    # 4. Five Angas & Temporal Coordinates
    angas = data["angas"]
    assert len(angas["tithis"]) >= 1
    assert len(angas["nakshatras"]) >= 1
    assert len(angas["yogas"]) >= 1
    assert len(angas["karanas"]) >= 1
    assert "పరాభవ" in angas["samvatsara"]
    assert "ఉత్తరాయణ" in angas["ayanam"]
    assert "వసంత" in angas["rutu"]
    assert "చైత్ర" in angas["masam"]
    assert "శుక్ల" in angas["paksham"]

    # 5. Sun/Moon Timings
    sun_moon = data["sun_moon"]
    assert "sunrise" in sun_moon
    assert "sunset" in sun_moon
    assert "moonrise" in sun_moon

    # 6. Muhurthams
    muhurthams = data["muhurthams"]
    assert "rahu_kalam" in muhurthams
    assert "yama_gandam" in muhurthams
    assert "gulika_kalam" in muhurthams

    # 7. Sankalpam
    sankalpa = data["sankalpam"]
    assert "sankalpam_text" in sankalpa
    assert "అమేరికా" in sankalpa["sankalpam_text"] or "Frisco" in sankalpa["sankalpam_text"]


def test_multilingual_support():
    """Verify transliteration across Devanagari, Tamil, Kannada, and English."""
    # Devanagari
    res_dev = client.get("/api/v1/panchangam/daily?city=Frisco&date=2026-03-19&language=devanagari")
    assert res_dev.status_code == 200
    assert "पराभव" in res_dev.json()["chandramana"]["samvatsara"]["name"]

    # Tamil
    res_tam = client.get("/api/v1/panchangam/daily?city=Frisco&date=2026-03-19&language=tamil")
    assert res_tam.status_code == 200
    assert res_tam.json()["chandramana"]["samvatsara"]["name"] != ""

    # Kannada
    res_kan = client.get("/api/v1/panchangam/daily?city=Frisco&date=2026-03-19&language=kannada")
    assert res_kan.status_code == 200
    assert "ಪರಾಭವ" in res_kan.json()["chandramana"]["samvatsara"]["name"]

    # English
    res_en = client.get("/api/v1/panchangam/daily?city=Frisco&date=2026-03-19&language=english")
    assert res_en.status_code == 200
    assert "parābhava" in res_en.json()["chandramana"]["samvatsara"]["name"].lower() or "parabhava" in res_en.json()["chandramana"]["samvatsara"]["name"].lower()


def test_monthly_panchangam():
    res = client.get("/api/v1/panchangam/monthly?city=Frisco&year=2026&month=3&language=telugu")
    assert res.status_code == 200
    data = res.json()
    assert data["year"] == 2026
    assert data["month"] == 3
    assert len(data["days"]) == 31


def test_sankalpam_endpoint():
    res = client.get("/api/v1/sankalpam/generate?city=Frisco&date=2026-03-19&language=telugu&gotra=Kashyapa&sharma_name=Rama")
    assert res.status_code == 200
    data = res.json()
    assert "sankalpam" in data
    assert "కాష్యప" in data["sankalpam"]["full_sankalpam_text"] or "గోత్ర" in data["sankalpam"]["full_sankalpam_text"]


def test_web_app_serving():
    res = client.get("/app")
    assert res.status_code == 200
    assert "వేద సంహిత • పంచాంగం" in res.text
    assert "RAMACHANDRA SASTRY MUNIMADUGU" in res.text
    assert "Vedic Samhita" in res.text
    assert "<!DOCTYPE html>" in res.text

    # Test root with Accept text/html
    html_res = client.get("/", headers={"accept": "text/html,application/xhtml+xml"})
    assert html_res.status_code == 200
    assert "<!DOCTYPE html>" in html_res.text


def test_cities_nearest():
    # Frisco TX coordinates
    res = client.get("/api/v1/cities/nearest?lat=33.1507&lon=-96.8236")
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "Frisco"
    assert data["country"] == "USA"


def test_lagnas_and_festivals_telugu():
    """Verify 24-hour Lagna schedule, Pushkara Navamsha, and Telugu festival transliteration."""
    res = client.get("/api/v1/panchangam/daily?city=Frisco&date=2026-09-18&language=telugu")
    assert res.status_code == 200
    data = res.json()

    # 1. Festivals in Telugu
    assert len(data["festivals"]) >= 1
    fest_names = [f["name"] for f in data["festivals"]]
    # Check that Telugu characters exist in the festival names
    has_telugu = any(any('\u0c00' <= char <= '\u0c7f' for char in fname) for fname in fest_names)
    assert has_telugu, f"Festivals should be in Telugu: {fest_names}"
    assert any("దూర్వాష్టమీ" in fname or "రాధాష్టమీ" in fname for fname in fest_names)

    # 2. Lagnas with Pushkara Navamsha
    lagnas = data["lagnas"]
    assert len(lagnas) == 12
    for l in lagnas:
        assert "start_time" in l and l["start_time"] is not None
        assert "end_time" in l and l["end_time"] is not None
        assert "rashi_name" in l and "లగ్నం" in l["rashi_name"]
        assert "duration" in l and "గం." in l["duration"]
        assert "pushkara_amsha" in l and l["pushkara_amsha"] is not None
        assert "is_next_day" in l

    # Verify next-day lagna (e.g. Mithuna ends past midnight)
    next_day_lagnas = [l for l in lagnas if l["is_next_day"]]
    assert len(next_day_lagnas) >= 3, "Lagnas ending past midnight should be flagged is_next_day"


def test_vedic_vasaram_names():
    """Verify all 7 Vedic Vasaram names in Telugu and English."""
    from services.localization_service import get_weekday_name

    expected_telugu = {
        0: "భాను వాసరం (రవి వాసరం)",
        1: "ఇందు వాసరం (సోమ వాసరం)",
        2: "భౌమ వాసరం (మంగళ వాసరం)",
        3: "సౌమ్య వాసరం (బుధ వాసరం)",
        4: "బృహస్పతి వాసరం (గురు వాసరం)",
        5: "భృగు వాసరం (శుక్ర వాసరం)",
        6: "స్థిర వాసరం (శని వాసరం)"
    }
    expected_english = {
        0: "Bhanu vasaram ( Ravi vasaram )",
        1: "Indu vasaram ( Soma vasaram )",
        2: "Bhouma vasaram ( Mangala vasaram )",
        3: "Soumya vasaram ( Budha vasaram )",
        4: "Bruhaspati vasaram ( Guru vasaram )",
        5: "Bhrugu vasaram ( Sukra vasaram )",
        6: "Sthira vasaram ( Shani vasaram )"
    }

    for day_idx in range(7):
        assert get_weekday_name(day_idx, "telugu") == expected_telugu[day_idx]
        assert get_weekday_name(day_idx, "english") == expected_english[day_idx]

    # Verify via API for Friday 2026-09-18
    res_fri = client.get("/api/v1/panchangam/daily?city=Frisco&date=2026-09-18&language=telugu")
    assert res_fri.status_code == 200
    data_fri = res_fri.json()
    assert data_fri["angas"]["vara"] == "భృగు వాసరం (శుక్ర వాసరం)"
    assert data_fri["angas"]["vara_english"] == "Bhrugu vasaram ( Sukra vasaram )"

    # Verify via API for Thursday 2026-03-19
    res_thu = client.get("/api/v1/panchangam/daily?city=Frisco&date=2026-03-19&language=telugu")
    assert res_thu.status_code == 200
    data_thu = res_thu.json()
    assert data_thu["angas"]["vara"] == "బృహస్పతి వాసరం (గురు వాసరం)"
    assert data_thu["angas"]["vara_english"] == "Bruhaspati vasaram ( Guru vasaram )"


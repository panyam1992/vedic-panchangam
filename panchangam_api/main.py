"""
Global Vedic Panchangam REST API.
High-performance backend service powered by Jyotisha astronomical engine,
Swiss Ephemeris, Aksharamukha multilingual transliteration, and Vedic mana systems.
"""

import os
import sys
from datetime import datetime, timezone
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

# Ensure API directory and Jyotisha are in sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
JYOTISHA_DIR = os.path.join(PROJECT_ROOT, "Jyotisha")
STATIC_DIR = os.path.join(CURRENT_DIR, "static")

for p in [CURRENT_DIR, JYOTISHA_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from config import SUPPORTED_LANGUAGES, DEFAULT_LANG
from routers import panchangam, cities, sankalpam, rashi
from jyotishyam.routers import kundali as j_kundali
from jyotishyam.routers import prashna as j_prashna
from jyotishyam.routers import shishu as j_shishu
from jyotishyam.routers import eclipses as j_eclipses
from jyotishyam.routers import languages as j_languages
from jyotishyam.routers import chat as j_chat
from jyotishyam.routers import muhurtam as j_muhurtam

app = FastAPI(
    title="Vedic Samhita - Panchangam & Jyotishyam Unified Vedic Platform API",
    description="""
**Vedic Astronomy, Panchangam & Jyotishyam Computation System • [www.vedicsamhita.com](https://www.vedicsamhita.com)**

Created & Formulated by: **RAMACHANDRA SASTRY MUNIMADUGU** (శ్రీ రామచంద్ర శాస్త్రి మునిమడుగు)
*All credits for research, astronomical computations, Dharma Shastra correlation, and algorithmic architecture go to RAMACHANDRA SASTRY MUNIMADUGU.*

Key Capabilities:
- **పంచాంగం (Panchangam)**: 5 Angas, 3 Traditional Mana Systems, Lagna Schedule, Auspicious & Inauspicious Periods, Deśa-Kāla Sankalpam.
- **జన్మ కుండలి (Horoscope)**: D1 & D9 Chakras, Bhava Sphuta, Vimshottari Dasha-Bhukti, Gocharam & Sade Sati, Classical Yogas, Santana & Pregnancy Dosha Audit.
- **ముహూర్త నిర్ణయం (Vedic Muhurtam)**: Avakahada Pada Name detection, Direct Nakshatra pick, Universal Panchanga & Abhijit Shuddhi, Muhurta Lagna & Ashtama Shuddhi, Couple & Family harmony, Print Muhurta Patrika & WhatsApp sharing.
- **శిశు జాతకం (Newborn)**: Baby naming syllables, Moola/Gandanta Dosha audit, Nakshatra Paya.
- **ప్రశ్న జ్యోతిష్యం (Horary)**: 1-249 KP / Vedic Prashna query resolution.
- **గ్రహణ దర్శిని (Eclipses)**: Solar & Lunar eclipses with Sparsha, Madhya, Moksha timings worldwide.
- **బహుభాషా (All Indian Languages)**: Telugu, Devanagari (Hindi/Sanskrit), Tamil, Kannada, Malayalam, Gujarati, Bengali, Odia, Punjabi, and English/IAST.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for all frontends (Web, Mobile, App)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Include Panchangam API Routers
app.include_router(panchangam.router)
app.include_router(cities.router)
app.include_router(sankalpam.router)
app.include_router(rashi.router)

# Include Jyotishyam API Routers
app.include_router(j_kundali.router)
app.include_router(j_prashna.router)
app.include_router(j_shishu.router)
app.include_router(j_eclipses.router)
app.include_router(j_languages.router)
app.include_router(j_chat.router)
app.include_router(j_muhurtam.router)


@app.get("/", tags=["General"])
def root(request: Request):
    """
    Root endpoint.
    Serves interactive Web App (PWA) when requested by a browser (Accept: text/html),
    or JSON service status when requested by API clients.
    """
    accept = request.headers.get("accept", "")
    index_path = os.path.join(STATIC_DIR, "index.html")
    if "text/html" in accept and os.path.exists(index_path):
        return FileResponse(index_path)

    return {
        "service": "Vedic Samhita Unified Panchangam & Jyotishyam API",
        "version": "1.0.0",
        "status": "online",
        "web_app": "/",
        "jyotishyam_app": "/jyotishyam",
        "documentation": "/docs",
        "supported_languages": list(SUPPORTED_LANGUAGES.keys()),
        "mana_systems": [
            "chandramana (Amanta & Purnimanta)",
            "sauramana (Tamil, Malayalam Kollam, Bengali, Odia)",
            "barhaspatyamana (Jupiter cycle & Pushkaram)"
        ],
        "endpoints": {
            "web_app": "/",
            "jyotishyam_app": "/jyotishyam",
            "daily_panchangam": "/api/v1/panchangam/daily?city=Frisco&language=telugu",
            "monthly_panchangam": "/api/v1/panchangam/monthly?city=Frisco&year=2026&month=3&language=telugu",
            "search_cities": "/api/v1/cities/search?q=Frisco",
            "popular_cities": "/api/v1/cities/popular",
            "sankalpam": "/api/v1/sankalpam/generate?city=Frisco&language=telugu&gotra=Kashyapa",
            "generate_kundali": "POST /api/v1/kundali/generate",
            "calculate_muhurtam": "POST /api/v1/muhurtam/calculate",
            "shishu_jatakam": "POST /api/v1/shishu/generate",
            "prashna_kundali": "POST /api/v1/prashna/calculate"
        }
    }


@app.get("/app", tags=["General"])
def serve_app():
    """Direct URL to open the Panchangam Web App."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    return FileResponse(index_path)


@app.get("/jyotishyam", tags=["Jyotishyam"])
@app.get("/jyotishyam/", tags=["Jyotishyam"])
def serve_jyotishyam():
    """Direct endpoint to serve Jyotishyam Web Platform."""
    jyotishyam_index = os.path.join(STATIC_DIR, "jyotishyam", "index.html")
    if os.path.exists(jyotishyam_index):
        return FileResponse(jyotishyam_index)
    return JSONResponse(status_code=404, content={"detail": "Jyotishyam UI not found"})


@app.get("/health", tags=["General"])
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

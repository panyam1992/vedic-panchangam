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

app = FastAPI(
    title="Vedic Samhita - Panchangam & Vedic Computation API",
    description="""
**Vedic Astronomy & Dharma Shastra Computation System • [www.vedicsamhita.com](https://www.vedicsamhita.com)**

Created & Formulated by: **RAMACHANDRA SASTRY MUNIMADUGU** (శ్రీ రామచంద్ర శాస్త్రి మునిమడుగు)
*All credits for research, astronomical computations, Dharma Shastra correlation, and algorithmic architecture go to RAMACHANDRA SASTRY MUNIMADUGU.*

Key Capabilities:
- **బహుభాషా (All Indian Languages)**: Telugu, Devanagari (Hindi/Sanskrit), Tamil, Kannada, Malayalam, Gujarati, Bengali, and English/IAST.
- **3 Traditional Mana Systems**: 
  1. చాంద్రమానం (Chandramana) - Amanta & Purnimanta, Samvatsara, Adhika/Nija/Kshaya
  2. సౌరమానం (Sauramana) - Tamil, Malayalam (Kollam), Bengali, Odia solar dates & Sankranti
  3. బార్హస్పత్యమానం (Barhaspatyamana) - Jupiter Jovian 60-year & 12-year Maha-Masa cycle, Sacred River Pushkaram
- **Full 5 Angas**: Tithi, Nakshatra, Yoga, Karana, Classical Vedic Vasaram names with exact sunrise and end times
- **Auspicious & Inauspicious Periods**: Rahu Kalam, Yama Gandam, Gulika Kalam, Durmuhurtham, Abhijit, Varjyam, Amrita Kalam
- **24-Hour Lagna Schedule**: Complete 12 ascendants with Pushkara Navamsha timings
- **Vedic Deśa-Kāla Sankalpam**: Geographically accurate puja sankalpa for India, Americas, Europe, and worldwide
- **Global Cities**: Fast search across 500+ worldwide cities with coordinate resolution
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

# Include API Routers
app.include_router(panchangam.router)
app.include_router(cities.router)
app.include_router(sankalpam.router)
app.include_router(rashi.router)


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
        "service": "Vedic Panchangam Global API",
        "version": "1.0.0",
        "status": "online",
        "web_app": "/",
        "documentation": "/docs",
        "supported_languages": list(SUPPORTED_LANGUAGES.keys()),
        "mana_systems": [
            "chandramana (Amanta & Purnimanta)",
            "sauramana (Tamil, Malayalam Kollam, Bengali, Odia)",
            "barhaspatyamana (Jupiter cycle & Pushkaram)"
        ],
        "endpoints": {
            "web_app": "/",
            "daily_panchangam": "/api/v1/panchangam/daily?city=Frisco&language=telugu",
            "monthly_panchangam": "/api/v1/panchangam/monthly?city=Frisco&year=2026&month=3&language=telugu",
            "search_cities": "/api/v1/cities/search?q=Frisco",
            "popular_cities": "/api/v1/cities/popular",
            "sankalpam": "/api/v1/sankalpam/generate?city=Frisco&language=telugu&gotra=Kashyapa"
        }
    }


@app.get("/app", tags=["General"])
def serve_app():
    """Direct URL to open the Web App."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    return FileResponse(index_path)


@app.get("/health", tags=["General"])
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

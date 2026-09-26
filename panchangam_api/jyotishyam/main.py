"""
Main FastAPI server for Jyotishyam Web Platform & Siddhanta Karta AI.
"""

import os
import sys
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

# Ensure backend directory is in sys.path
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))
from jyotishyam.config import STATIC_DIR
from routers import kundali, cities, chat, prashna, shishu, eclipses, languages, muhurtam

app = FastAPI(
    title="జ్యోతిష్యం (Jyotishyam) - Vedic Kundali & Siddhanta Karta AI",
    description="""
**ఆధునిక వైదిక జ్యోతిష్య వేదిక • Modern Vedic Astrology & Shastra Platform**
- High-precision Swiss Ephemeris astronomical calculations (pyswisseph)
- South Indian & North Indian Visual Kundali (D1 Rashi & D9 Navamsha)
- Birth Panchangam, Graha Spashta, Vimshottari Dasha-Bhukti Timeline
- Current Gocharam & Sade Sati (ఏలినాటి శని) Analysis
- Stree Jataka (స్త్రీ జాతకం) & Purusha Jataka (పురుష జాతకం) Classical Differentiation
- 'సిద్ధాంత కర్త / జ్యోతిష్య బ్రహ్మ' AI Astrological Consultation grounded in Uttara Kalamritam & Jataka Chandrika
- Aksharamukha Multi-Script Indic Engine (తెలుగు, हिन्दी, தமிழ், ಕನ್ನಡ, മലയാളം, বাংলা, ગુજરાતી, ଓଡ଼ିଆ, ਪੰਜਾਬੀ, IAST)
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files (Frontend)
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Include Routers
app.include_router(kundali.router)
app.include_router(cities.router)
app.include_router(prashna.router)
app.include_router(shishu.router)
app.include_router(eclipses.router)
app.include_router(languages.router)
app.include_router(chat.router)
app.include_router(muhurtam.router)


@app.get("/", tags=["General"])
def root(request: Request):
    """Serve the Web Application index.html or API status."""
    accept = request.headers.get("accept", "")
    index_file = STATIC_DIR / "index.html"
    if index_file.exists() and (accept == "" or "text/html" in accept or "*/*" in accept):
        return FileResponse(str(index_file))

    return {
        "service": "Jyotishyam Vedic Kundali & AI Siddhanta Karta API",
        "version": "1.0.0",
        "status": "online",
        "app_ui": "/",
        "documentation": "/docs",
        "endpoints": {
            "generate_kundali": "POST /api/v1/kundali/generate",
            "search_cities": "GET /api/v1/cities/search?q=Hyderabad",
            "chat_siddhanta_karta": "POST /api/v1/chat/consult"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)

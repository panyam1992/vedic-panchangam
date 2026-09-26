"""
Application configuration for Jyotishyam Web Platform.
"""

import os
from pathlib import Path

# Paths
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
REPO_ROOT = PROJECT_ROOT.parent

# Swiss Ephemeris data files path
EPHEMERIS_DIR = REPO_ROOT / "ephemeris"
BOOKS_DIR = REPO_ROOT / "Books"

# Frontend Static Path
STATIC_DIR = PROJECT_ROOT / "static" / "jyotishyam"

def _load_env_file():
    """Auto-loads key-value pairs from .env if present."""
    candidates = [
        PROJECT_ROOT / ".env",
        CURRENT_DIR / ".env",
        REPO_ROOT / ".env"
    ]
    for env_path in candidates:
        if env_path.exists():
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'\"")
                        if k and k not in os.environ:
                            os.environ[k] = v
            except Exception as e:
                print(f"Notice: Failed loading {env_path}: {e}")

_load_env_file()

# Gemini API Key (Configured once by server admin/owner)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", os.getenv("GOOGLE_API_KEY", ""))

# Swiss Ephemeris Ayanamsa Setting
# Default: Lahiri (Chitrapaksha) = 1 in SwissEph (SIDM_LAHIRI)
DEFAULT_AYANAMSA = "lahiri"


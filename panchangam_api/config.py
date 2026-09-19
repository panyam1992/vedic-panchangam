import os
import sys

# Base directories
API_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(API_DIR)
JYOTISHA_DIR = os.path.join(PROJECT_ROOT, "Jyotisha")

# Add Jyotisha to sys.path so its modules can be imported directly
if JYOTISHA_DIR not in sys.path:
    sys.path.insert(0, JYOTISHA_DIR)

COMPUTATION_SYSTEM_PATH = os.path.join(
    JYOTISHA_DIR, "computation_systems", "vishvAsa_bhAskara.toml"
)

DEFAULT_CITY = "Hyderabad"
DEFAULT_LAT = 17.3850
DEFAULT_LON = 78.4867
DEFAULT_TZ = "Asia/Kolkata"
DEFAULT_LANG = "telugu"

SUPPORTED_LANGUAGES = {
    "telugu": "telugu",
    "devanagari": "devanagari",
    "hindi": "devanagari",
    "sanskrit": "devanagari",
    "tamil": "tamil",
    "kannada": "kannada",
    "malayalam": "malayalam",
    "gujarati": "gujarati",
    "bengali": "bengali",
    "oriya": "oriya",
    "odia": "oriya",
    "gurmukhi": "gurmukhi",
    "punjabi": "gurmukhi",
    "assamese": "bengali",
    "english": "iast",
    "iast": "iast"
}
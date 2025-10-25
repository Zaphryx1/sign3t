import os
from dotenv import load_dotenv
load_dotenv()

# Local AI Configuration - No cloud APIs needed!
# Using Ollama for local LLM and sentence-transformers for embeddings

# Application Configuration
APP_NAME = "Sign3T - AI Threat Assessment"
VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Threat Assessment Configuration
THREAT_LEVELS = {
    "LOW": {"score": 1, "color": "green", "description": "Minimal risk"},
    "MEDIUM": {"score": 2, "color": "yellow", "description": "Moderate risk"},
    "HIGH": {"score": 3, "color": "orange", "description": "Significant risk"},
    "CRITICAL": {"score": 4, "color": "red", "description": "Extreme risk"}
}

# Data Sources Configuration
DATA_SOURCES = {
    "911_calls": "Real-time emergency call data",
    "prior_incidents": "Historical incident reports",
    "gis_maps": "Geographic information system data",
    "body_cam": "Body camera footage analysis",
    "dispatch": "Dispatch records and communications"
}
import os

# ============================================================================
# STREAMLIT CONFIGURATION
# ============================================================================

# API URLs
# Tenta pegar da variável de ambiente (útil para Docker), senão usa localhost
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Timeouts
REQUEST_TIMEOUT = 10
CACHE_TIMEOUT = 3600

# UI Colors
COLORS = {
    "primary": "#1f77b4",
    "success": "#2ca02c",
    "danger": "#d62728",
    "warning": "#ff7f0e",
    "info": "#17becf"
}

# Weather Conditions
WEATHER_CONDITIONS = [
    "sunny",
    "cloudy",
    "rainy",
    "snowy",
    "unknown"
]

# Activity Types
ACTIVITY_TYPES = [
    "Run",
    "Ride",
    "Swim",
    "Walk",
    "Hike",
    "Workout",
    "Kayaking",
    "Other"
]

# Pace Ranges (min/km for running)
PACE_RANGES = {
    "Easy": (7.0, 10.0),
    "Moderate": (5.5, 7.0),
    "Fast": (4.0, 5.5),
    "Very Fast": (0, 4.0)
}

# Page Names for Navigation
PAGE_NAMES = {
    "dashboard": "📈 Dashboard",
    "analytics": "📊 Analytics",
    "activities": "🚴 Activities"
}

# Sidebar
SIDEBAR_TITLE = "🚴 Strava Insights"
SIDEBAR_SUBTITLE = "Intelligent Sports Analytics"

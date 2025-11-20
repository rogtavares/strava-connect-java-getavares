from fastapi import FastAPI, HTTPException
import requests
import os
from datetime import datetime

app = FastAPI()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080")
OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")


@app.get("/enrich")
def enrich_activities():
    # fetch activities export from Java backend
    r = requests.get(f"{BACKEND_URL}/activities/export")
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="Failed to fetch activities from backend")
    activities = r.json()

    enriched = []
    for a in activities:
        item = dict(a)
        # if has latlng, try to fetch weather (use start_latlng)
        latlng = a.get("start_latlng")
        if latlng and len(latlng) >= 2 and OPENWEATHER_KEY:
            lat, lon = latlng[0], latlng[1]
            # OpenWeather One Call historic requires timestamp; use start_date
            ts = a.get("start_date")
            try:
                dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                unix = int(dt.timestamp())
                ow_url = f"https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={unix}&appid={OPENWEATHER_KEY}&units=metric"
                w = requests.get(ow_url)
                if w.status_code == 200:
                    item['weather'] = w.json()
            except Exception:
                item['weather_error'] = 'invalid_date'
        enriched.append(item)

    return enriched

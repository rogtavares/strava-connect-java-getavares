from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio
import os
from datetime import datetime
from statistics import mean, median
from collections import defaultdict
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Strava Insights API", version="2.2.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8000/callback")

class StravaInsights:
    """Generate intelligent insights from Strava activities and weather data"""
    
    def __init__(self, activities):
        self.activities = activities
        self.enriched_activities = []
    
    def extract_weather(self, activity):
        """Extract weather data from activity if available"""
        weather = activity.get('weather', {})
        if isinstance(weather, dict) and 'current' in weather:
            return {
                'temperature': weather['current'].get('temp'),
                'humidity': weather['current'].get('humidity'),
                'wind_speed': weather['current'].get('wind_speed'),
                'clouds': weather['current'].get('clouds'),
                'weather_main': weather['current'].get('weather', [{}])[0].get('main'),
                'feels_like': weather['current'].get('feels_like'),
                'pressure': weather['current'].get('pressure'),
            }
        return None
    
    def calculate_pace(self, activity):
        """Calculate pace in min/km or min/mile"""
        distance = activity.get('distance', 0)  # meters
        moving_time = activity.get('moving_time', 1)  # seconds
        
        if distance <= 0 or moving_time <= 0:
            return None
        
        km = distance / 1000
        minutes = moving_time / 60
        pace_min_per_km = minutes / km if km > 0 else None
        return pace_min_per_km
    
    def get_activity_conditions(self, activity):
        """Classify activity weather conditions"""
        weather = self.extract_weather(activity)
        if not weather:
            return "unknown"
        
        temp = weather.get('temperature', 0)
        
        if temp < 5:
            return "cold"
        elif temp < 15:
            return "cool"
        elif temp < 22:
            return "ideal"
        elif temp < 28:
            return "warm"
        else:
            return "hot"
    
    def analyze_performance_by_condition(self):
        """Analyze performance metrics grouped by weather conditions"""
        conditions_stats = defaultdict(list)
        
        for activity in self.enriched_activities:
            pace = self.calculate_pace(activity)
            condition = activity.get('weather_condition', 'unknown')
            
            if pace and condition != 'unknown':
                conditions_stats[condition].append(pace)
        
        result = {}
        for condition, paces in conditions_stats.items():
            if paces:
                result[condition] = {
                    'avg_pace': round(mean(paces), 2),
                    'median_pace': round(median(paces), 2),
                    'count': len(paces),
                    'best_pace': round(min(paces), 2),
                    'worst_pace': round(max(paces), 2),
                }
        
        return result
    
    def analyze_performance_by_temperature_range(self):
        """Analyze performance by temperature ranges"""
        temp_ranges = {
            'cold_below_5': [],
            'cool_5_to_15': [],
            'ideal_15_to_22': [],
            'warm_22_to_28': [],
            'hot_above_28': []
        }
        
        for activity in self.enriched_activities:
            pace = self.calculate_pace(activity)
            weather = self.extract_weather(activity)
            
            if pace and weather and 'temperature' in weather:
                temp = weather['temperature']
                
                if temp < 5:
                    temp_ranges['cold_below_5'].append(pace)
                elif temp < 15:
                    temp_ranges['cool_5_to_15'].append(pace)
                elif temp < 22:
                    temp_ranges['ideal_15_to_22'].append(pace)
                elif temp < 28:
                    temp_ranges['warm_22_to_28'].append(pace)
                else:
                    temp_ranges['hot_above_28'].append(pace)
        
        result = {}
        for range_name, paces in temp_ranges.items():
            if paces:
                result[range_name] = {
                    'avg_pace': round(mean(paces), 2),
                    'count': len(paces),
                    'best_pace': round(min(paces), 2),
                }
        
        return result
    
    def find_best_conditions(self):
        """Find the weather conditions where you perform best"""
        performance_by_condition = self.analyze_performance_by_condition()
        
        if not performance_by_condition:
            return None
        
        best_condition = min(
            performance_by_condition.items(),
            key=lambda x: x[1]['avg_pace']
        )
        
        return {
            'condition': best_condition[0],
            'avg_pace': best_condition[1]['avg_pace'],
            'count': best_condition[1]['count'],
            'insight': f"🏃 Você corre melhor em dias {best_condition[0]}! "
                      f"Pace médio: {best_condition[1]['avg_pace']:.2f} min/km"
        }
    
    def find_wind_impact(self):
        """Analyze impact of wind on performance"""
        low_wind = []
        high_wind = []
        
        for activity in self.enriched_activities:
            pace = self.calculate_pace(activity)
            weather = self.extract_weather(activity)
            
            if pace and weather and 'wind_speed' in weather:
                wind = weather['wind_speed']
                if wind < 5:
                    low_wind.append(pace)
                elif wind > 10:
                    high_wind.append(pace)
        
        if low_wind and high_wind:
            avg_low = mean(low_wind)
            avg_high = mean(high_wind)
            difference = ((avg_high - avg_low) / avg_low) * 100
            
            return {
                'avg_pace_low_wind': round(avg_low, 2),
                'avg_pace_high_wind': round(avg_high, 2),
                'impact_percent': round(difference, 1),
                'insight': f"💨 Vento reduz seu pace em ~{difference:.1f}% (comparado a dias com pouco vento)"
            }
        
        return None
    
    def generate_summary_insights(self):
        """Generate a summary of all insights"""
        insights = []
        
        # Best condition
        best_cond = self.find_best_conditions()
        if best_cond:
            insights.append(best_cond['insight'])
        
        # Wind impact
        wind_impact = self.find_wind_impact()
        if wind_impact:
            insights.append(wind_impact['insight'])
        
        # Activity count
        if self.enriched_activities:
            insights.append(f"📊 Total de atividades analisadas: {len(self.enriched_activities)}")
        
        return insights
    
    def process(self):
        """Process all activities and enrich with weather and insights"""
        for activity in self.activities:
            enriched = dict(activity)
            
            # Add weather info
            weather = self.extract_weather(activity)
            if weather:
                enriched['weather_data'] = weather
                enriched['weather_condition'] = self.get_activity_conditions(activity)
            
            # Add pace calculation
            pace = self.calculate_pace(activity)
            if pace:
                enriched['pace_min_per_km'] = round(pace, 2)
            
            self.enriched_activities.append(enriched)
        
        return self.enriched_activities


async def fetch_weather_for_activity(client, activity):
    """Async helper to fetch weather for a single activity"""
    item = dict(activity)
    latlng = activity.get("start_latlng")

    if latlng and len(latlng) >= 2 and OPENWEATHER_KEY:
        lat, lon = latlng[0], latlng[1]
        ts = activity.get("start_date")
        try:
            dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
            unix = int(dt.timestamp())
            ow_url = f"https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={unix}&appid={OPENWEATHER_KEY}&units=metric"

            resp = await client.get(ow_url, timeout=5.0)
            if resp.status_code == 200:
                item['weather'] = resp.json()
        except Exception as e:
            logger.warning(f"Failed to fetch weather: {e}")
            item['weather_error'] = str(e)

    return item

async def enrich_activities_data(activities):
    """Enrich a list of activities with weather data concurrently"""
    async with httpx.AsyncClient() as client:
        tasks = [fetch_weather_for_activity(client, a) for a in activities]
        return await asyncio.gather(*tasks)

# --- Auth Helpers ---
def get_token(request: Request):
    """Retrieve token from Cookie, Authorization Header, or Query Param"""
    # 1. Try Query Param (Easiest for browser testing)
    token = request.query_params.get("access_token")
    if token:
        return token

    # 2. Try Cookie
    token = request.cookies.get("access_token")
    if token:
        return token
    
    # 3. Try Authorization Header (Bearer <token>)
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
        
    raise HTTPException(status_code=401, detail="Not authenticated. Please login at /login or provide Bearer token.")

# --- Routes ---

@app.get("/")
def root():
    """Root endpoint with API info"""
    return {
        "name": "Strava Insights API (Python Edition)",
        "version": "2.2.0",
        "endpoints": {
            "/login": "Start OAuth flow",
            "/callback": "OAuth callback",
            "/activities": "Get raw activities from Strava",
            "/enrich": "Get enriched activities with weather and insights",
            "/insights": "Get AI-generated insights about your performance",
        }
    }

@app.get("/login")
def login():
    """Redirect user to Strava for authentication"""
    scope = "activity:read_all"
    auth_url = (
        f"https://www.strava.com/oauth/authorize"
        f"?client_id={STRAVA_CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        f"&approval_prompt=auto"
        f"&scope={scope}"
    )
    return RedirectResponse(auth_url)

@app.get("/callback")
async def callback(code: str, scope: str = None):
    """Handle Strava OAuth callback"""
    token_url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=payload)
        
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to retrieve token")
    
    data = response.json()
    access_token = data.get("access_token")
    
    response = RedirectResponse(url="/insights")
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@app.get("/activities")
async def get_activities(access_token: str = Depends(get_token)):
    """Fetch activities directly from Strava"""
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://www.strava.com/api/v3/athlete/activities?per_page=30"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch activities from Strava")
        
    return response.json()

@app.get("/enrich")
async def enrich_activities_endpoint(access_token: str = Depends(get_token)):
    """
    Enrich activities with weather data and calculate performance metrics.
    """
    try:
        # Fetch activities from Strava
        headers = {"Authorization": f"Bearer {access_token}"}
        url = "https://www.strava.com/api/v3/athlete/activities?per_page=30"
        
        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers=headers)

        if r.status_code != 200:
            raise HTTPException(status_code=502, detail="Failed to fetch activities from Strava")
        
        activities = r.json()
        
        # Enrich with weather concurrently
        enriched = await enrich_activities_data(activities)
        
        return enriched
    
    except Exception as e:
        logger.error(f"Error in /enrich: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/insights")
async def get_insights(access_token: str = Depends(get_token)):
    """
    Generate intelligent insights about your performance based on weather conditions.
    """
    try:
        # Fetch activities
        headers = {"Authorization": f"Bearer {access_token}"}
        url = "https://www.strava.com/api/v3/athlete/activities?per_page=30"
        
        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers=headers)

        if r.status_code != 200:
            raise HTTPException(status_code=502, detail="Failed to fetch activities from Strava")
        
        activities = r.json()
        
        # Enrich activities with weather concurrently
        enriched = await enrich_activities_data(activities)
        
        # Create insights processor
        processor = StravaInsights(activities)
        processor.activities = enriched
        processor.process()
        
        # Generate insights
        return JSONResponse(content={
            "summary": processor.generate_summary_insights(),
            "performance_by_condition": processor.analyze_performance_by_condition(),
            "performance_by_temperature": processor.analyze_performance_by_temperature_range(),
            "best_conditions": processor.find_best_conditions(),
            "wind_impact": processor.find_wind_impact(),
            "total_activities_analyzed": len(processor.enriched_activities),
        })

    except Exception as e:
        logger.error(f"Error in /insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))

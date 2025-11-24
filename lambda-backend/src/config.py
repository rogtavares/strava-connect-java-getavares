"""
Configurações centralizadas para Backend APIs

🏃 Adaptado para: ROGERIO TAVARES (ID: 3329857)
   Perfil: https://www.strava.com/athletes/3329857
"""
import os
from typing import Dict, Any

# Strava OAuth
STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
STRAVA_REDIRECT_URI = os.getenv('STRAVA_REDIRECT_URI', 'https://yourdomain.com/auth/callback')
STRAVA_AUTH_URL = 'https://www.strava.com/oauth/authorize'
STRAVA_TOKEN_URL = 'https://www.strava.com/oauth/token'
STRAVA_API_URL = 'https://www.strava.com/api/v3'

# Athlete Info (Rogerio Tavares)
STRAVA_ATHLETE_ID = int(os.getenv('STRAVA_ATHLETE_ID', '3329857'))
STRAVA_ATHLETE_NAME = os.getenv('STRAVA_ATHLETE_NAME', 'Rogerio Tavares')
STRAVA_ACCESS_TOKEN = os.getenv('STRAVA_ACCESS_TOKEN')

# AWS
DYNAMODB_TABLE_USERS = os.getenv('DYNAMODB_TABLE_USERS', 'strava-users')
DYNAMODB_TABLE_ACTIVITIES = os.getenv('DYNAMODB_TABLE_ACTIVITIES', 'strava-activities')
DYNAMODB_TABLE_CACHE = os.getenv('DYNAMODB_TABLE_CACHE', 'strava-cache')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

# Cache
CACHE_TTL_ATHLETE = 3600  # 1 hora
CACHE_TTL_ACTIVITIES = 1800  # 30 minutos
CACHE_TTL_STATS = 7200  # 2 horas

# Limites
MAX_ACTIVITIES_PER_REQUEST = 50
PAGINATION_SIZE = 20

# ML Models
ML_MODEL_PATH = os.getenv('ML_MODEL_PATH', '/opt/ml/model')

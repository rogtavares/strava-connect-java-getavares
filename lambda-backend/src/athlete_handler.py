"""
Handler para Perfil do Atleta - GET /athlete
"""
import json
import logging
from typing import Dict, Any
import requests
from datetime import datetime

from config import STRAVA_API_URL, CACHE_TTL_ATHLETE
from utils import response_success, response_error, CacheManager, TokenManager, generate_cache_key
from auth_handler import refresh_access_token

logger = logging.getLogger()
logger.setLevel(logging.INFO)

cache_manager = CacheManager()
token_manager = TokenManager()


def lambda_handler(event, context):
    """
    Handler para GET /athlete
    
    Pathparameters:
    - user_id (via path ou JWT)
    
    Query parameters:
    - detailed (opcional, padrão: false)
    """
    try:
        # Extrair user_id
        user_id = event.get('pathParameters', {}).get('user_id')
        if not user_id:
            return response_error('User ID is required', 400, 'MISSING_USER_ID')
        
        detailed = event.get('queryStringParameters', {}).get('detailed', 'false').lower() == 'true'
        
        # Verificar cache
        cache_key = generate_cache_key('athlete', user_id, 'detailed' if detailed else 'basic')
        cached_data = cache_manager.get(cache_key)
        
        if cached_data:
            return response_success({
                'cached': True,
                'athlete': cached_data
            })
        
        # Recuperar token
        tokens = token_manager.get_token(user_id)
        if not tokens:
            return response_error('User not authenticated', 401, 'UNAUTHENTICATED')
        
        access_token = tokens.get('access_token')
        
        # Chamar Strava API
        logger.info(f"Buscando perfil do atleta: {user_id}")
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
        
        athlete_response = requests.get(
            f'{STRAVA_API_URL}/athlete',
            headers=headers
        )
        
        # Se token expirou, renovar
        if athlete_response.status_code == 401:
            logger.info("Token expirado, renovando...")
            try:
                new_tokens = refresh_access_token(user_id)
                access_token = new_tokens.get('access_token')
                headers['Authorization'] = f'Bearer {access_token}'
                athlete_response = requests.get(
                    f'{STRAVA_API_URL}/athlete',
                    headers=headers
                )
            except Exception as e:
                return response_error('Token refresh failed', 401, 'TOKEN_REFRESH_FAILED')
        
        if athlete_response.status_code != 200:
            logger.error(f"Erro ao buscar atleta: {athlete_response.text}")
            return response_error('Failed to fetch athlete data', 400, 'ATHLETE_FETCH_FAILED')
        
        athlete_data = athlete_response.json()
        
        # Formatar dados
        athlete_info = {
            'id': athlete_data.get('id'),
            'firstname': athlete_data.get('firstname'),
            'lastname': athlete_data.get('lastname'),
            'email': athlete_data.get('email'),
            'profile': athlete_data.get('profile'),
            'profile_medium': athlete_data.get('profile_medium'),
            'city': athlete_data.get('city'),
            'state': athlete_data.get('state'),
            'country': athlete_data.get('country'),
            'sex': athlete_data.get('sex'),
            'premium': athlete_data.get('premium'),
            'created_at': athlete_data.get('created_at'),
            'updated_at': athlete_data.get('updated_at')
        }
        
        if detailed:
            athlete_info.update({
                'follower_count': athlete_data.get('follower_count'),
                'friend_count': athlete_data.get('friend_count'),
                'ftp': athlete_data.get('ftp'),
                'weight': athlete_data.get('weight'),
                'stats': athlete_data.get('stats', {})
            })
        
        # Armazenar em cache
        cache_manager.set(cache_key, athlete_info, CACHE_TTL_ATHLETE)
        
        logger.info(f"Perfil do atleta recuperado com sucesso: {athlete_info['id']}")
        
        return response_success({
            'cached': False,
            'athlete': athlete_info
        })
        
    except Exception as e:
        logger.error(f"Erro ao buscar perfil: {str(e)}")
        return response_error(f'Internal server error: {str(e)}', 500, 'INTERNAL_ERROR')

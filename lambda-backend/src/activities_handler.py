"""
Handler para Atividades - GET /activities
"""
import json
import logging
from typing import Dict, Any, List
import requests
from datetime import datetime, timedelta

from config import STRAVA_API_URL, CACHE_TTL_ACTIVITIES, PAGINATION_SIZE, MAX_ACTIVITIES_PER_REQUEST
from utils import response_success, response_error, CacheManager, TokenManager, generate_cache_key
from auth_handler import refresh_access_token

logger = logging.getLogger()
logger.setLevel(logging.INFO)

cache_manager = CacheManager()
token_manager = TokenManager()


def lambda_handler(event, context):
    """
    Handler para GET /activities
    
    Path parameters:
    - user_id
    
    Query parameters:
    - page (padrão: 1)
    - per_page (padrão: 20, máximo: 50)
    - after (timestamp Unix, opcional)
    - before (timestamp Unix, opcional)
    - sport_type (opcional, ex: Run, Ride, Swim)
    """
    try:
        # Extrair user_id
        user_id = event.get('pathParameters', {}).get('user_id')
        if not user_id:
            return response_error('User ID is required', 400, 'MISSING_USER_ID')
        
        # Query parameters
        query_params = event.get('queryStringParameters', {}) or {}
        page = int(query_params.get('page', '1'))
        per_page = min(int(query_params.get('per_page', str(PAGINATION_SIZE))), MAX_ACTIVITIES_PER_REQUEST)
        after = query_params.get('after')
        before = query_params.get('before')
        sport_type = query_params.get('sport_type')
        
        # Validar página
        if page < 1:
            page = 1
        
        # Verificar cache
        cache_key = generate_cache_key('activities', user_id, f'page_{page}_limit_{per_page}')
        cached_data = cache_manager.get(cache_key)
        
        if cached_data:
            return response_success({
                'cached': True,
                'activities': cached_data.get('activities'),
                'pagination': cached_data.get('pagination')
            })
        
        # Recuperar token
        tokens = token_manager.get_token(user_id)
        if not tokens:
            return response_error('User not authenticated', 401, 'UNAUTHENTICATED')
        
        access_token = tokens.get('access_token')
        
        # Chamar Strava API
        logger.info(f"Buscando atividades para usuário: {user_id}")
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
        
        params = {
            'page': page,
            'per_page': per_page
        }
        
        if after:
            params['after'] = after
        if before:
            params['before'] = before
        
        activities_response = requests.get(
            f'{STRAVA_API_URL}/athlete/activities',
            headers=headers,
            params=params
        )
        
        # Se token expirou, renovar
        if activities_response.status_code == 401:
            logger.info("Token expirado, renovando...")
            try:
                new_tokens = refresh_access_token(user_id)
                access_token = new_tokens.get('access_token')
                headers['Authorization'] = f'Bearer {access_token}'
                activities_response = requests.get(
                    f'{STRAVA_API_URL}/athlete/activities',
                    headers=headers,
                    params=params
                )
            except Exception as e:
                return response_error('Token refresh failed', 401, 'TOKEN_REFRESH_FAILED')
        
        if activities_response.status_code != 200:
            logger.error(f"Erro ao buscar atividades: {activities_response.text}")
            return response_error('Failed to fetch activities', 400, 'ACTIVITIES_FETCH_FAILED')
        
        activities_data = activities_response.json()
        
        # Formatar atividades
        activities_list = []
        for activity in activities_data:
            # Filtrar por sport_type se especificado
            if sport_type and activity.get('sport_type') != sport_type:
                continue
            
            activity_info = {
                'id': activity.get('id'),
                'name': activity.get('name'),
                'type': activity.get('type'),
                'sport_type': activity.get('sport_type'),
                'distance': activity.get('distance'),
                'moving_time': activity.get('moving_time'),
                'elapsed_time': activity.get('elapsed_time'),
                'elevation_gain': activity.get('total_elevation_gain'),
                'average_speed': activity.get('average_speed'),
                'max_speed': activity.get('max_speed'),
                'average_heartrate': activity.get('average_heartrate'),
                'max_heartrate': activity.get('max_heartrate'),
                'average_cadence': activity.get('average_cadence'),
                'start_date': activity.get('start_date'),
                'start_date_local': activity.get('start_date_local'),
                'timezone': activity.get('timezone'),
                'location_city': activity.get('location_city'),
                'location_state': activity.get('location_state'),
                'location_country': activity.get('location_country'),
                'kudos_count': activity.get('kudos_count'),
                'comment_count': activity.get('comment_count'),
                'athlete_count': activity.get('athlete_count'),
                'photo_count': activity.get('photo_count'),
                'trainer': activity.get('trainer'),
                'commute': activity.get('commute'),
                'manual': activity.get('manual'),
                'private': activity.get('private'),
                'flagged': activity.get('flagged'),
                'workout_type': activity.get('workout_type'),
            }
            activities_list.append(activity_info)
        
        # Preparar resposta com paginação
        response_data = {
            'activities': activities_list,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_activities': len(activities_list)
            }
        }
        
        # Armazenar em cache
        cache_manager.set(cache_key, response_data, CACHE_TTL_ACTIVITIES)
        
        logger.info(f"{len(activities_list)} atividades recuperadas para usuário: {user_id}")
        
        return response_success({
            'cached': False,
            'activities': activities_list,
            'pagination': response_data['pagination']
        })
        
    except Exception as e:
        logger.error(f"Erro ao buscar atividades: {str(e)}")
        return response_error(f'Internal server error: {str(e)}', 500, 'INTERNAL_ERROR')

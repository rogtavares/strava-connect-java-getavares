"""
Handler para Estatísticas Agregadas - GET /stats
"""
import json
import logging
from typing import Dict, Any
import requests
from datetime import datetime, timedelta
from collections import defaultdict

from config import STRAVA_API_URL, CACHE_TTL_STATS
from utils import response_success, response_error, CacheManager, TokenManager, generate_cache_key
from auth_handler import refresh_access_token

logger = logging.getLogger()
logger.setLevel(logging.INFO)

cache_manager = CacheManager()
token_manager = TokenManager()


def lambda_handler(event, context):
    """
    Handler para GET /stats
    
    Path parameters:
    - user_id
    
    Query parameters:
    - period (week, month, year, all - padrão: month)
    - sport_type (opcional)
    """
    try:
        # Extrair user_id
        user_id = event.get('pathParameters', {}).get('user_id')
        if not user_id:
            return response_error('User ID is required', 400, 'MISSING_USER_ID')
        
        # Query parameters
        query_params = event.get('queryStringParameters', {}) or {}
        period = query_params.get('period', 'month')
        sport_type = query_params.get('sport_type')
        
        # Validar período
        if period not in ['week', 'month', 'year', 'all']:
            period = 'month'
        
        # Verificar cache
        cache_key = generate_cache_key('stats', user_id, f'{period}_{sport_type or "all"}')
        cached_data = cache_manager.get(cache_key)
        
        if cached_data:
            return response_success({
                'cached': True,
                'stats': cached_data
            })
        
        # Recuperar token
        tokens = token_manager.get_token(user_id)
        if not tokens:
            return response_error('User not authenticated', 401, 'UNAUTHENTICATED')
        
        access_token = tokens.get('access_token')
        
        # Calcular data limite baseado no período
        now = datetime.now()
        if period == 'week':
            start_date = (now - timedelta(days=7)).timestamp()
        elif period == 'month':
            start_date = (now - timedelta(days=30)).timestamp()
        elif period == 'year':
            start_date = (now - timedelta(days=365)).timestamp()
        else:  # all
            start_date = 0
        
        # Chamar Strava API para atividades
        logger.info(f"Buscando estatísticas para usuário: {user_id}, período: {period}")
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
        
        activities_response = requests.get(
            f'{STRAVA_API_URL}/athlete/activities',
            headers=headers,
            params={
                'after': int(start_date),
                'per_page': 200
            }
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
                    params={
                        'after': int(start_date),
                        'per_page': 200
                    }
                )
            except Exception as e:
                return response_error('Token refresh failed', 401, 'TOKEN_REFRESH_FAILED')
        
        if activities_response.status_code != 200:
            logger.error(f"Erro ao buscar atividades: {activities_response.text}")
            return response_error('Failed to fetch activities for stats', 400, 'STATS_FETCH_FAILED')
        
        activities_data = activities_response.json()
        
        # Calcular estatísticas
        stats = calculate_stats(activities_data, sport_type)
        
        # Armazenar em cache
        cache_manager.set(cache_key, stats, CACHE_TTL_STATS)
        
        logger.info(f"Estatísticas calculadas para usuário: {user_id}")
        
        return response_success({
            'cached': False,
            'period': period,
            'sport_type': sport_type or 'all',
            'stats': stats
        })
        
    except Exception as e:
        logger.error(f"Erro ao calcular estatísticas: {str(e)}")
        return response_error(f'Internal server error: {str(e)}', 500, 'INTERNAL_ERROR')


def calculate_stats(activities: list, sport_type: str = None) -> Dict[str, Any]:
    """Calcula estatísticas agregadas a partir de atividades"""
    
    stats = {
        'total_activities': 0,
        'total_distance': 0,
        'total_moving_time': 0,
        'total_elevation_gain': 0,
        'average_speed': 0,
        'max_speed': 0,
        'average_heartrate': 0,
        'max_heartrate': 0,
        'activities_by_type': defaultdict(int),
        'distance_by_type': defaultdict(float),
        'time_by_type': defaultdict(int),
        'top_activities': []
    }
    
    total_distance = 0
    valid_activities = 0
    heartrates = []
    
    for activity in activities:
        # Filtrar por sport_type se especificado
        if sport_type and activity.get('sport_type') != sport_type:
            continue
        
        activity_type = activity.get('sport_type', activity.get('type', 'Unknown'))
        
        stats['total_activities'] += 1
        distance = activity.get('distance', 0) / 1000  # Converter para km
        stats['total_distance'] += distance
        stats['total_moving_time'] += activity.get('moving_time', 0)
        stats['total_elevation_gain'] += activity.get('total_elevation_gain', 0)
        
        # Por tipo
        stats['activities_by_type'][activity_type] += 1
        stats['distance_by_type'][activity_type] += distance
        stats['time_by_type'][activity_type] += activity.get('moving_time', 0)
        
        # Velocidade
        avg_speed = activity.get('average_speed', 0)
        if avg_speed > 0:
            total_distance += avg_speed * activity.get('moving_time', 1)
            valid_activities += 1
        
        max_speed = activity.get('max_speed', 0)
        if max_speed > stats['max_speed']:
            stats['max_speed'] = round(max_speed * 3.6, 2)  # m/s para km/h
        
        # Frequência cardíaca
        if activity.get('average_heartrate'):
            heartrates.append(activity.get('average_heartrate'))
            stats['average_heartrate'] = sum(heartrates) / len(heartrates)
        
        if activity.get('max_heartrate') and activity.get('max_heartrate') > stats['max_heartrate']:
            stats['max_heartrate'] = activity.get('max_heartrate')
        
        # Top atividades (top 5)
        if len(stats['top_activities']) < 5:
            stats['top_activities'].append({
                'id': activity.get('id'),
                'name': activity.get('name'),
                'distance': round(distance, 2),
                'moving_time': activity.get('moving_time'),
                'date': activity.get('start_date'),
                'type': activity_type
            })
    
    # Calcular médias
    if stats['total_activities'] > 0:
        stats['average_distance'] = round(stats['total_distance'] / stats['total_activities'], 2)
        stats['average_moving_time'] = stats['total_moving_time'] // stats['total_activities']
        stats['average_speed'] = round((total_distance / stats['total_moving_time'] * 3.6), 2) if stats['total_moving_time'] > 0 else 0
    
    # Converter defaultdict para dict
    stats['activities_by_type'] = dict(stats['activities_by_type'])
    stats['distance_by_type'] = {k: round(v, 2) for k, v in stats['distance_by_type'].items()}
    stats['time_by_type'] = dict(stats['time_by_type'])
    
    # Arredondar valores
    stats['total_distance'] = round(stats['total_distance'], 2)
    stats['total_elevation_gain'] = round(stats['total_elevation_gain'], 0)
    stats['average_heartrate'] = round(stats['average_heartrate'], 0) if stats['average_heartrate'] > 0 else 0
    
    return stats

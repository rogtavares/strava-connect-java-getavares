"""
Handler para Análises com ML - GET /insights (Opcional)
"""
import json
import logging
from typing import Dict, Any, List
import numpy as np
from datetime import datetime, timedelta
import boto3
import requests

from config import STRAVA_API_URL, AWS_REGION
from utils import response_success, response_error, CacheManager, TokenManager, generate_cache_key
from stats_handler import calculate_stats
from auth_handler import refresh_access_token

logger = logging.getLogger()
logger.setLevel(logging.INFO)

cache_manager = CacheManager()
token_manager = TokenManager()
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)


def lambda_handler(event, context):
    """
    Handler para GET /insights
    
    Análises com Machine Learning (opcional)
    - Predições de desempenho
    - Recomendações de treino
    - Análises de tendências
    - Anomalias em atividades
    
    Path parameters:
    - user_id
    
    Query parameters:
    - type (performance, recommendations, trends, anomalies - padrão: all)
    - days (número de dias para análise - padrão: 30)
    """
    try:
        # Extrair user_id
        user_id = event.get('pathParameters', {}).get('user_id')
        if not user_id:
            return response_error('User ID is required', 400, 'MISSING_USER_ID')
        
        # Query parameters
        query_params = event.get('queryStringParameters', {}) or {}
        insight_type = query_params.get('type', 'all')
        days = int(query_params.get('days', '30'))
        
        # Validar tipo
        valid_types = ['all', 'performance', 'recommendations', 'trends', 'anomalies']
        if insight_type not in valid_types:
            insight_type = 'all'
        
        # Recuperar token
        tokens = token_manager.get_token(user_id)
        if not tokens:
            return response_error('User not authenticated', 401, 'UNAUTHENTICATED')
        
        access_token = tokens.get('access_token')
        
        # Buscar atividades
        logger.info(f"Buscando atividades para insights: {user_id}, dias: {days}")
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
        
        start_date = (datetime.now() - timedelta(days=days)).timestamp()
        
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
            return response_error('Failed to fetch activities for insights', 400, 'INSIGHTS_FETCH_FAILED')
        
        activities_data = activities_response.json()
        
        # Gerar insights
        insights = {
            'generated_at': datetime.now().isoformat(),
            'period_days': days,
            'total_activities': len(activities_data)
        }
        
        if insight_type in ['all', 'performance']:
            insights['performance'] = analyze_performance(activities_data)
        
        if insight_type in ['all', 'recommendations']:
            insights['recommendations'] = generate_recommendations(activities_data)
        
        if insight_type in ['all', 'trends']:
            insights['trends'] = analyze_trends(activities_data)
        
        if insight_type in ['all', 'anomalies']:
            insights['anomalies'] = detect_anomalies(activities_data)
        
        logger.info(f"Insights gerados para usuário: {user_id}")
        
        return response_success({
            'insights': insights
        })
        
    except Exception as e:
        logger.error(f"Erro ao gerar insights: {str(e)}")
        return response_error(f'Internal server error: {str(e)}', 500, 'INTERNAL_ERROR')


def analyze_performance(activities: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analisa desempenho e tendências de velocidade"""
    
    performance = {
        'analysis': 'Performance over time',
        'metrics': {}
    }
    
    if not activities:
        return performance
    
    # Agrupar por tipo de esporte
    by_type = {}
    for activity in activities:
        sport_type = activity.get('sport_type', activity.get('type', 'Unknown'))
        if sport_type not in by_type:
            by_type[sport_type] = []
        by_type[sport_type].append(activity)
    
    # Calcular métricas por tipo
    for sport_type, acts in by_type.items():
        speeds = [a.get('average_speed', 0) * 3.6 for a in acts if a.get('average_speed')]
        
        if speeds:
            performance['metrics'][sport_type] = {
                'avg_speed_kmh': round(np.mean(speeds), 2),
                'max_speed_kmh': round(np.max(speeds), 2),
                'std_dev_speed': round(np.std(speeds), 2) if len(speeds) > 1 else 0,
                'improvement': calculate_improvement(speeds),
                'consistency': calculate_consistency(speeds)
            }
    
    return performance


def generate_recommendations(activities: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Gera recomendações de treino baseado em padrões"""
    
    recommendations = {
        'suggestions': []
    }
    
    if not activities:
        return recommendations
    
    # Calcular frequência
    now = datetime.now()
    last_7_days = [a for a in activities if 
                   datetime.fromisoformat(a.get('start_date', '').replace('Z', '+00:00')) > 
                   now - timedelta(days=7)]
    
    # Recomendação 1: Frequência de treino
    activity_freq = len(last_7_days)
    if activity_freq < 3:
        recommendations['suggestions'].append({
            'category': 'frequency',
            'severity': 'warning',
            'message': f'Apenas {activity_freq} atividades nos últimos 7 dias. Considere aumentar a frequência de treino.',
            'recommendation': 'Objetivo: 3-5 atividades por semana para melhores resultados'
        })
    elif activity_freq > 7:
        recommendations['suggestions'].append({
            'category': 'recovery',
            'severity': 'info',
            'message': f'{activity_freq} atividades nos últimos 7 dias.',
            'recommendation': 'Considere incluir dias de recuperação ativa ou repouso'
        })
    
    # Recomendação 2: Varietà
    sport_types = set(a.get('sport_type', a.get('type', 'Unknown')) for a in activities)
    if len(sport_types) < 2:
        recommendations['suggestions'].append({
            'category': 'variety',
            'severity': 'info',
            'message': f'Treino focado em {list(sport_types)[0]}.',
            'recommendation': 'Adicionar outras modalidades para trabalhar diferentes grupos musculares'
        })
    
    # Recomendação 3: Intensidade
    total_distance = sum(a.get('distance', 0) for a in last_7_days) / 1000  # km
    avg_distance = total_distance / len(last_7_days) if last_7_days else 0
    
    if avg_distance > 50:
        recommendations['suggestions'].append({
            'category': 'intensity',
            'severity': 'warning',
            'message': f'Média de {avg_distance:.1f}km por atividade.',
            'recommendation': 'Considere balancear com atividades de menor intensidade'
        })
    elif avg_distance < 5 and last_7_days:
        recommendations['suggestions'].append({
            'category': 'intensity',
            'severity': 'info',
            'message': f'Média de {avg_distance:.1f}km por atividade.',
            'recommendation': 'Considere aumentar distância ou intensidade'
        })
    
    return recommendations


def analyze_trends(activities: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analisa tendências ao longo do tempo"""
    
    trends = {
        'trend_analysis': 'Performance trends over time',
        'data': {}
    }
    
    if not activities:
        return trends
    
    # Agrupar por data (semanal)
    weekly_data = {}
    for activity in sorted(activities, key=lambda x: x.get('start_date', '')):
        date = datetime.fromisoformat(activity.get('start_date', '').replace('Z', '+00:00'))
        week_start = date - timedelta(days=date.weekday())
        week_key = week_start.strftime('%Y-W%U')
        
        if week_key not in weekly_data:
            weekly_data[week_key] = {
                'activities': 0,
                'distance': 0,
                'time': 0,
                'elevation': 0
            }
        
        weekly_data[week_key]['activities'] += 1
        weekly_data[week_key]['distance'] += activity.get('distance', 0) / 1000
        weekly_data[week_key]['time'] += activity.get('moving_time', 0)
        weekly_data[week_key]['elevation'] += activity.get('total_elevation_gain', 0)
    
    trends['data'] = weekly_data
    
    return trends


def detect_anomalies(activities: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Detecta anomalias nas atividades (valores atípicos)"""
    
    anomalies = {
        'anomalies_detected': [],
        'analysis': 'Detects unusual activity patterns'
    }
    
    if len(activities) < 3:
        return anomalies
    
    # Anomalias de velocidade
    speeds = [a.get('average_speed', 0) * 3.6 for a in activities if a.get('average_speed')]
    if speeds:
        mean_speed = np.mean(speeds)
        std_speed = np.std(speeds)
        
        for i, activity in enumerate(activities):
            activity_speed = activity.get('average_speed', 0) * 3.6
            if abs(activity_speed - mean_speed) > 2 * std_speed and activity_speed > 0:
                anomalies['anomalies_detected'].append({
                    'activity_id': activity.get('id'),
                    'name': activity.get('name'),
                    'type': 'speed_anomaly',
                    'value': round(activity_speed, 2),
                    'mean': round(mean_speed, 2),
                    'std_dev': round(std_speed, 2),
                    'z_score': round((activity_speed - mean_speed) / std_speed, 2)
                })
    
    # Anomalias de distância
    distances = [a.get('distance', 0) / 1000 for a in activities if a.get('distance')]
    if distances:
        mean_distance = np.mean(distances)
        std_distance = np.std(distances)
        
        for activity in activities:
            activity_distance = activity.get('distance', 0) / 1000
            if abs(activity_distance - mean_distance) > 2 * std_distance and activity_distance > 0:
                existing = any(anom.get('activity_id') == activity.get('id') 
                              for anom in anomalies['anomalies_detected'])
                if not existing:
                    anomalies['anomalies_detected'].append({
                        'activity_id': activity.get('id'),
                        'name': activity.get('name'),
                        'type': 'distance_anomaly',
                        'value': round(activity_distance, 2),
                        'mean': round(mean_distance, 2),
                        'std_dev': round(std_distance, 2),
                        'z_score': round((activity_distance - mean_distance) / std_distance, 2)
                    })
    
    return anomalies


def calculate_improvement(values: List[float]) -> str:
    """Calcula melhoria comparando primeira e última metade"""
    if len(values) < 2:
        return 'insufficient_data'
    
    mid = len(values) // 2
    first_half = np.mean(values[:mid])
    second_half = np.mean(values[mid:])
    
    improvement_pct = ((second_half - first_half) / first_half * 100) if first_half > 0 else 0
    
    if improvement_pct > 5:
        return f'improving_{int(improvement_pct)}%'
    elif improvement_pct < -5:
        return f'declining_{int(-improvement_pct)}%'
    else:
        return 'stable'


def calculate_consistency(values: List[float]) -> str:
    """Calcula consistência do desempenho"""
    if len(values) < 2:
        return 'insufficient_data'
    
    cv = (np.std(values) / np.mean(values) * 100) if np.mean(values) > 0 else 0
    
    if cv < 10:
        return 'very_consistent'
    elif cv < 20:
        return 'consistent'
    elif cv < 30:
        return 'moderate'
    else:
        return 'variable'

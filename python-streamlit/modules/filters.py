"""
Filters Module
Widgets de filtro reutilizáveis
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
import pandas as pd
from config import ACTIVITY_TYPES, WEATHER_CONDITIONS

def filter_by_sport() -> List[str]:
    """Widget para filtrar por tipo de esporte"""
    return st.multiselect(
        "🏃 Tipo de Esporte",
        options=ACTIVITY_TYPES,
        default=ACTIVITY_TYPES[:3],
        key="sport_filter"
    )

def filter_by_date_range() -> Tuple[datetime, datetime]:
    """Widget para filtrar por intervalo de data"""
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input(
            "📅 Data Inicial",
            value=datetime.now() - timedelta(days=30),
            key="start_date_filter"
        )
    
    with col2:
        end_date = st.date_input(
            "📅 Data Final",
            value=datetime.now(),
            key="end_date_filter"
        )
    
    return start_date, end_date

def filter_by_weather() -> List[str]:
    """Widget para filtrar por condição climática"""
    return st.multiselect(
        "🌤️ Condição Climática",
        options=WEATHER_CONDITIONS,
        default=WEATHER_CONDITIONS[:3],
        key="weather_filter"
    )

def filter_by_pace_range() -> Tuple[float, float]:
    """Widget para filtrar por range de pace"""
    col1, col2 = st.columns(2)
    
    with col1:
        min_pace = st.number_input(
            "Min Pace (min/km)",
            value=4.0,
            step=0.5,
            key="min_pace_filter"
        )
    
    with col2:
        max_pace = st.number_input(
            "Max Pace (min/km)",
            value=10.0,
            step=0.5,
            key="max_pace_filter"
        )
    
    return min_pace, max_pace

def search_activity(activities: List[Dict]) -> List[Dict]:
    """Widget para buscar atividade por nome"""
    search_term = st.text_input(
        "🔍 Buscar por nome da atividade",
        key="search_filter"
    )
    
    if not search_term:
        return activities
    
    df = pd.DataFrame(activities)
    if 'name' not in df.columns:
        return activities
    
    filtered = df[df['name'].str.contains(search_term, case=False, na=False)]
    return filtered.to_dict('records')

def apply_filters(
    activities: List[Dict],
    sport_types: List[str] = None,
    start_date: datetime = None,
    end_date: datetime = None,
    weather_conditions: List[str] = None,
    pace_min: float = None,
    pace_max: float = None
) -> List[Dict]:
    """
    Aplica múltiplos filtros nas atividades
    """
    if not activities:
        return []
    
    df = pd.DataFrame(activities)
    
    # Filtro por tipo de esporte
    if sport_types:
        if 'type' in df.columns:
            df = df[df['type'].isin(sport_types)]
    
    # Filtro por data
    if start_date or end_date:
        if 'start_date' in df.columns:
            df['start_date'] = pd.to_datetime(df['start_date'])
            if start_date:
                df = df[df['start_date'].dt.date >= start_date]
            if end_date:
                df = df[df['start_date'].dt.date <= end_date]
    
    # Filtro por condição climática
    if weather_conditions:
        if 'weather_condition' in df.columns:
            df = df[df['weather_condition'].isin(weather_conditions)]
    
    # Filtro por pace
    if pace_min is not None or pace_max is not None:
        if 'distance' in df.columns and 'moving_time' in df.columns:
            df['pace'] = (df['moving_time'] / 60) / (df['distance'] / 1000)
            if pace_min is not None:
                df = df[df['pace'] >= pace_min]
            if pace_max is not None:
                df = df[df['pace'] <= pace_max]
    
    return df.to_dict('records')

def create_filter_panel() -> Dict[str, Any]:
    """Cria painel com todos os filtros e retorna configuração"""
    with st.expander("🔍 Filtros Avançados", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            sports = filter_by_sport()
            start_date, end_date = filter_by_date_range()
        
        with col2:
            weather = filter_by_weather()
            min_pace, max_pace = filter_by_pace_range()
        
        return {
            'sports': sports,
            'start_date': start_date,
            'end_date': end_date,
            'weather': weather,
            'min_pace': min_pace,
            'max_pace': max_pace
        }

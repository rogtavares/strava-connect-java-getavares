"""
Charts Module
Gráficos interativos com Plotly
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

def plot_activities_per_month(activities: List[Dict]) -> go.Figure:
    """Gráfico de atividades por mês"""
    if not activities:
        return empty_chart("Nenhuma atividade")
    
    try:
        df = pd.DataFrame(activities)
        if 'start_date' not in df.columns:
            return empty_chart("Sem dados de data")
        
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['month'] = df['start_date'].dt.to_period('M')
        monthly = df.groupby('month').size()
        
        fig = px.bar(
            x=monthly.index.astype(str),
            y=monthly.values,
            labels={'x': 'Mês', 'y': 'Quantidade'},
            title='📊 Atividades por Mês'
        )
        fig.update_layout(height=400, showlegend=False)
        return fig
    except Exception as e:
        logger.error(f"Erro ao plotar atividades por mês: {e}")
        return empty_chart(f"Erro: {str(e)}")

def plot_pace_vs_temperature(activities: List[Dict]) -> go.Figure:
    """Scatter: Pace vs Temperatura"""
    if not activities:
        return empty_chart("Nenhuma atividade")
    
    try:
        df = pd.DataFrame(activities)
        
        # Filtrar dados válidos
        if 'distance' not in df.columns or 'moving_time' not in df.columns:
            return empty_chart("Sem dados de distância/tempo")
        
        df['pace'] = (df['moving_time'] / 60) / (df['distance'] / 1000)  # min/km
        
        # Tentar obter temperatura do weather se enriquecido
        if 'weather_temperature' in df.columns:
            fig = px.scatter(
                df,
                x='weather_temperature',
                y='pace',
                color='weather_condition',
                size='distance',
                hover_data=['name', 'type'],
                title='🌡️ Pace vs Temperatura',
                labels={'weather_temperature': 'Temperatura (°C)', 'pace': 'Pace (min/km)'}
            )
        else:
            fig = px.scatter(
                df,
                y='pace',
                size='distance',
                hover_data=['name', 'type'],
                title='🌡️ Pace vs Distância'
            )
        
        fig.update_layout(height=500)
        return fig
    except Exception as e:
        logger.error(f"Erro ao plotar pace vs temperatura: {e}")
        return empty_chart(f"Erro: {str(e)}")

def plot_performance_by_condition(insights: Dict) -> go.Figure:
    """Bar chart: Performance por condição climática"""
    try:
        if 'performance_by_condition' not in insights:
            return empty_chart("Sem insights de condição")
        
        data = insights['performance_by_condition']
        conditions = list(data.keys())
        paces = [data[c].get('avg_pace', 0) for c in conditions]
        
        fig = go.Figure(data=[
            go.Bar(x=conditions, y=paces, marker_color='#2ca02c')
        ])
        
        fig.update_layout(
            title='🌤️ Desempenho por Condição Climática',
            xaxis_title='Condição',
            yaxis_title='Pace Médio (min/km)',
            height=400,
            showlegend=False
        )
        return fig
    except Exception as e:
        logger.error(f"Erro ao plotar performance por condição: {e}")
        return empty_chart(f"Erro: {str(e)}")

def plot_wind_impact(insights: Dict) -> go.Figure:
    """Line chart: Impacto do vento"""
    try:
        if 'wind_impact_percentage' not in insights:
            return empty_chart("Sem dados de vento")
        
        wind_impact = insights['wind_impact_percentage']
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=[wind_impact],
            mode='markers+lines',
            marker=dict(size=15, color='#ff7f0e'),
            name='Impacto do Vento'
        ))
        
        fig.update_layout(
            title='💨 Impacto do Vento no Desempenho',
            yaxis_title='Impacto (%)',
            height=400,
            showlegend=True
        )
        return fig
    except Exception as e:
        logger.error(f"Erro ao plotar impacto do vento: {e}")
        return empty_chart(f"Erro: {str(e)}")

def plot_metric_cards(activities: List[Dict]) -> tuple:
    """Retorna métricas para cards (total_activities, total_distance, total_time)"""
    if not activities:
        return 0, 0, 0
    
    try:
        df = pd.DataFrame(activities)
        total_activities = len(df)
        total_distance = df['distance'].sum() / 1000  # converter para km
        total_time = df['moving_time'].sum() / 3600  # converter para horas
        
        return total_activities, round(total_distance, 1), round(total_time, 1)
    except Exception as e:
        logger.error(f"Erro ao calcular métricas: {e}")
        return 0, 0, 0

def empty_chart(message: str = "Nenhum dado disponível") -> go.Figure:
    """Retorna gráfico vazio com mensagem"""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=20, color="gray")
    )
    fig.update_layout(height=400, showlegend=False)
    return fig

def create_summary_chart(insights: Dict) -> go.Figure:
    """Cria gráfico de resumo com os insights principais"""
    try:
        insights_list = insights.get('insights_summary', [])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=insights_list[:5] if insights_list else [],
            mode='markers',
            marker=dict(size=10),
            text=insights_list[:5] if insights_list else [],
            hovertext=insights_list[:5] if insights_list else []
        ))
        
        fig.update_layout(
            title='📝 Resumo de Insights',
            height=300,
            showlegend=False
        )
        return fig
    except Exception as e:
        logger.error(f"Erro ao criar gráfico de resumo: {e}")
        return empty_chart()

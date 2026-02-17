"""
Dashboard Page
Visão geral com métricas principais
"""

import streamlit as st
import pandas as pd
from modules.api_client import get_api_client
from modules.charts import (
    plot_activities_per_month,
    plot_metric_cards,
    empty_chart,
    create_summary_chart
)
import logging

logger = logging.getLogger(__name__)

st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide")

st.title("📈 Dashboard")
st.markdown("Visão geral de suas atividades e desempenho")

# Verificar autenticação
if not st.session_state.authenticated:
    st.warning("⚠️ Autentique-se no Strava para ver o dashboard")
    st.stop()

# Client API
api_client = get_api_client()

# ============================================================================
# SEÇÃO 1: MÉTRICAS PRINCIPAIS
# ============================================================================

st.subheader("📊 Métricas Principais")

# Buscar atividades se não houver em session state
if not st.session_state.activities:
    with st.spinner("📥 Buscando atividades..."):
        activities = api_client.get_activities()
        if activities:
            st.session_state.activities = activities
            st.success(f"✅ {len(activities)} atividades carregadas")
        else:
            st.error("❌ Erro ao buscar atividades")

# Calcular métricas
if st.session_state.activities:
    total_activities, total_distance, total_hours = plot_metric_cards(st.session_state.activities)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📊 Total de Atividades",
            f"{total_activities}",
            delta="desde sempre"
        )
    
    with col2:
        st.metric(
            "🏃 Distância Total",
            f"{total_distance:.1f} km",
            delta=f"{total_distance/max(1, total_activities):.1f} km/atividade"
        )
    
    with col3:
        st.metric(
            "⏱️ Tempo Total",
            f"{total_hours:.1f} h",
            delta=f"{total_hours/max(1, total_activities):.1f} h/atividade"
        )
    
    with col4:
        st.metric(
            "📈 Este Mês",
            "Calculando...",
            delta="ver gráfico abaixo"
        )

# ============================================================================
# SEÇÃO 2: GRÁFICOS
# ============================================================================

st.markdown("---")
st.subheader("📈 Atividades por Período")

if st.session_state.activities:
    # Gráfico de atividades por mês
    fig = plot_activities_per_month(st.session_state.activities)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Nenhuma atividade carregada")

# ============================================================================
# SEÇÃO 3: INSIGHTS
# ============================================================================

st.markdown("---")
st.subheader("✨ Insights Gerados")

if st.session_state.insights:
    # Exibir insights
    insights = st.session_state.insights
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'best_conditions' in insights:
            st.info(f"☀️ **Melhor condição para treinar**: {insights['best_conditions']}")
    
    with col2:
        if 'wind_impact_percentage' in insights:
            st.warning(f"💨 **Impacto do vento**: {insights['wind_impact_percentage']:.1f}%")
    
    # Resumo de insights
    if 'insights_summary' in insights:
        st.markdown("### 📝 Resumo de Insights")
        for insight in insights['insights_summary'][:5]:
            st.write(f"• {insight}")
else:
    st.info("Carregue atividades para gerar insights")

# ============================================================================
# SEÇÃO 4: AÇÕES
# ============================================================================

st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Atualizar Dados", use_container_width=True):
        st.session_state.activities = []
        st.session_state.enriched_activities = []
        st.session_state.insights = {}
        st.rerun()

with col2:
    if st.button("💡 Gerar Insights", use_container_width=True):
        if st.session_state.activities:
            with st.spinner("Enriquecendo atividades..."):
                enriched = api_client.enrich_activities(st.session_state.activities)
                st.session_state.enriched_activities = enriched
            
            with st.spinner("Gerando insights..."):
                insights = api_client.get_insights(enriched)
                st.session_state.insights = insights
                st.success("✅ Insights gerados!")
                st.rerun()
        else:
            st.error("Carregue atividades primeiro")

with col3:
    if st.button("📊 Ver Analytics", use_container_width=True):
        st.switch_page("pages/2_📊_Analytics.py")

# Footer
st.markdown("---")
st.caption(f"Última atualização: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}")

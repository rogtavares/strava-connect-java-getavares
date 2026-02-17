"""
Strava Insights - Streamlit Dashboard
Dashboard interativo para análise inteligente de atividades de treino
"""

import streamlit as st
import logging
import os
from config import SIDEBAR_TITLE, API_URL

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="🚴 Strava Insights",
    page_icon="🚴",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Dashboard de análise inteligente de atividades Strava"
    }
)

# ============================================================================
# STYLING
# ============================================================================

st.markdown("""
<style>
    [data-testid="stMetric"] {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    
    h1 {
        color: #1f77b4;
    }
    
    h2 {
        color: #1f77b4;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'access_token' not in st.session_state:
    st.session_state.access_token = None

if 'activities' not in st.session_state:
    st.session_state.activities = []

if 'enriched_activities' not in st.session_state:
    st.session_state.enriched_activities = []

if 'insights' not in st.session_state:
    st.session_state.insights = {}

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.title(SIDEBAR_TITLE)
    st.markdown("---")
    
    # Status
    if st.session_state.authenticated:
        st.success("✅ Autenticado no Strava")
        if st.button("🔄 Sincronizar Atividades", use_container_width=True):
            st.info("Sincronizando... (implementado nas páginas)")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.access_token = None
            st.session_state.activities = []
            st.session_state.insights = {}
            st.rerun()
    else:
        st.warning("❌ Não autenticado")

        # Simple Token Input for Demo
        token_input = st.text_input("Insira seu Access Token:", type="password")
        if st.button("🔗 Conectar", use_container_width=True, type="primary"):
            if token_input:
                st.session_state.access_token = token_input
                st.session_state.authenticated = True
                st.success("Token salvo! Carregue as atividades.")
                st.rerun()
            else:
                st.error("Por favor, insira um token válido.")

        st.caption("Obtenha seu token em: https://www.strava.com/settings/api")
    
    st.markdown("---")
    
    # Info
    st.markdown(f"""
    ### ℹ️ Sobre
    
    Dashboard inteligente para análise de atividades Strava com insights sobre:
    - 🌡️ Impacto de temperatura
    - 💨 Influência do vento
    - 🌤️ Desempenho por condição climática
    - 📊 Análise detalhada de performance
    
    ### 🔧 Requisitos
    - API Python rodando em: `{API_URL}`
    - Autenticação Strava
    
    ### 📖 Documentação
    - [README](./README.md)
    - [Strava API Docs](https://developers.strava.com)
    """)
    
    st.markdown("---")
    st.caption("Strava Insights v2.0 (Python) | 2026")

# ============================================================================
# MAIN PAGE
# ============================================================================

if st.session_state.authenticated:
    st.title("🚴 Strava Insights Dashboard")
    st.markdown("Análise inteligente de suas atividades de treino")
    
    # Info sobre páginas
    st.info("""
    Use a navegação à esquerda para acessar:
    - **📈 Dashboard**: Visão geral e métricas principais
    - **📊 Analytics**: Análise detalhada com gráficos interativos
    - **🚴 Activities**: Lista completa de atividades com filtros
    """)
    
    # Status das atividades
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Atividades Carregadas", len(st.session_state.activities))
    with col2:
        st.metric("💾 Atividades Enriquecidas", len(st.session_state.enriched_activities))
    with col3:
        st.metric("✨ Insights Gerados", "Sim" if st.session_state.insights else "Não")

else:
    st.title("🚴 Strava Insights")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"""
        ## Bem-vindo ao Strava Insights! 🎉
        
        Dashboard inteligente para análise de seus treinos com insights sobre:
        
        ### ✨ Features Principais
        
        🌡️ **Análise de Temperatura**
        - Como sua performance varia com a temperatura
        - Identificar condições ideais para treinar
        
        💨 **Impacto do Vento**
        - Quantificar o efeito do vento nos seus treinos
        - Comparar desempenho com/sem vento
        
        🌤️ **Insights por Condição Climática**
        - Performance em dias ensolarados vs chuvosos
        - Recomendações de treino por clima
        
        📈 **Analytics Detalhado**
        - Gráficos interativos com Plotly
        - Filtros avançados (data, esporte, pace)
        - Dados de temperatura e vento enriquecidos
        
        ### 🚀 Como Começar
        
        1. Insira seu **Access Token** no menu lateral.
        2. Clique em **Conectar**.
        3. Explore o dashboard!
        
        ### 🔧 Status da API
        Conectado a: `{API_URL}`
        """)
    
    with col2:
        st.image(
            "https://d3nn82uaxijpm6.cloudfront.net/assets/strava/logo-strava-40194db3766117548c92742e9015d2d0.png" if False else None,
            width=200,
            use_column_width=True
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <p style="text-align: center; color: gray;">
    Made with ❤️ using Streamlit & FastAPI |
    <a href="https://github.com">GitHub</a> | 
    <a href="https://developers.strava.com">Strava Docs</a>
    </p>
    """, unsafe_allow_html=True)

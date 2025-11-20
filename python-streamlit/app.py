"""
Strava Insights - Streamlit Dashboard
Dashboard interativo para análise inteligente de atividades de treino
"""

import streamlit as st
import logging
from config import SIDEBAR_TITLE, PAGE_NAMES

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
            st.session_state.activities = []
            st.session_state.insights = {}
            st.rerun()
    else:
        st.warning("❌ Não autenticado")
        if st.button("🔗 Conectar ao Strava", use_container_width=True, type="primary"):
            st.info("Redirecionando para autenticação... (implementado nas páginas)")
    
    st.markdown("---")
    
    # Info
    st.markdown("""
    ### ℹ️ Sobre
    
    Dashboard inteligente para análise de atividades Strava com insights sobre:
    - 🌡️ Impacto de temperatura
    - 💨 Influência do vento
    - 🌤️ Desempenho por condição climática
    - 📊 Análise detalhada de performance
    
    ### 🔧 Requisitos
    - Spring Boot rodando (porta 8080)
    - FastAPI rodando (porta 8000)
    - Autenticação Strava
    
    ### 📖 Documentação
    - [README](./README.md)
    - [Strava API Docs](https://developers.strava.com)
    """)
    
    st.markdown("---")
    st.caption("Strava Insights v1.0 | 2025")

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
        st.markdown("""
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
        
        1. Clique em "Conectar ao Strava" no menu lateral
        2. Autorize o acesso às suas atividades
        3. Explore o dashboard, analytics e atividades
        4. Veja seus insights gerados automaticamente
        
        ### 🔧 Requisitos
        - Spring Boot rodando em `http://localhost:8080`
        - FastAPI rodando em `http://localhost:8000`
        - Credenciais Strava OAuth 2.0
        """)
    
    with col2:
        st.image(
            "https://www.strava.com/logo.png" if False else None,
            width=200,
            use_column_width=True
        )
        
        st.button(
            "🔗 Conectar ao Strava",
            use_container_width=True,
            type="primary",
            key="main_connect_btn"
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <p style="text-align: center; color: gray;">
    Made with ❤️ using Streamlit | 
    <a href="https://github.com">GitHub</a> | 
    <a href="https://developers.strava.com">Strava Docs</a>
    </p>
    """, unsafe_allow_html=True)

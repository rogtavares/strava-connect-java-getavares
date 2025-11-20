"""
Analytics Page
Análise detalhada com gráficos interativos
"""

import streamlit as st
import pandas as pd
from modules.api_client import get_api_client
from modules.charts import (
    plot_pace_vs_temperature,
    plot_performance_by_condition,
    plot_wind_impact,
    empty_chart
)
from modules.filters import apply_filters, create_filter_panel
import logging

logger = logging.getLogger(__name__)

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")

st.title("📊 Analytics")
st.markdown("Análise detalhada com gráficos interativos")

# Verificar autenticação
if not st.session_state.authenticated:
    st.warning("⚠️ Autentique-se no Strava para ver analytics")
    st.stop()

# Client API
api_client = get_api_client()

# ============================================================================
# SEÇÃO 1: FILTROS
# ============================================================================

st.subheader("🔍 Filtros")

# Garantir que temos atividades
if not st.session_state.activities:
    with st.spinner("📥 Buscando atividades..."):
        activities = api_client.get_activities()
        if activities:
            st.session_state.activities = activities
        else:
            st.error("❌ Erro ao buscar atividades")
            st.stop()

# Garantir que temos insights
if not st.session_state.insights and st.session_state.activities:
    with st.spinner("✨ Gerando insights..."):
        enriched = api_client.enrich_activities(st.session_state.activities)
        st.session_state.enriched_activities = enriched
        insights = api_client.get_insights(enriched)
        st.session_state.insights = insights

# Aplicar filtros
filter_config = create_filter_panel()

filtered_activities = apply_filters(
    st.session_state.activities,
    sport_types=filter_config['sports'] if filter_config['sports'] else None,
    start_date=filter_config['start_date'],
    end_date=filter_config['end_date'],
    weather_conditions=filter_config['weather'] if filter_config['weather'] else None,
    pace_min=filter_config['min_pace'],
    pace_max=filter_config['max_pace']
)

st.info(f"📊 {len(filtered_activities)} atividades após filtros (de {len(st.session_state.activities)} total)")

# ============================================================================
# SEÇÃO 2: GRÁFICOS DE ANÁLISE
# ============================================================================

st.markdown("---")

# Tabs para diferentes gráficos
tab1, tab2, tab3, tab4 = st.tabs(
    ["🌡️ Pace vs Temp", "🌤️ Por Condição", "💨 Vento", "📊 Tabela"]
)

with tab1:
    st.subheader("Pace vs Temperatura")
    fig = plot_pace_vs_temperature(filtered_activities)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    **Interpretação:**
    - **X-axis**: Temperatura em Celsius
    - **Y-axis**: Pace em minutos por km (menor é melhor)
    - **Cor**: Condição climática
    - **Tamanho**: Distância da atividade
    
    Procure por padrões: em que temperatura você corre melhor?
    """)

with tab2:
    st.subheader("Desempenho por Condição Climática")
    if st.session_state.insights:
        fig = plot_performance_by_condition(st.session_state.insights)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        **Interpretação:**
        - Compare seu pace médio em diferentes condições climáticas
        - Identifique em qual clima você tem melhor desempenho
        - Use para planejar treinos importantes
        """)
    else:
        st.info("Execute 'Gerar Insights' no Dashboard primeiro")

with tab3:
    st.subheader("Impacto do Vento")
    if st.session_state.insights:
        fig = plot_wind_impact(st.session_state.insights)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"""
        **Impacto do vento no seu desempenho:**
        - {st.session_state.insights.get('wind_impact_percentage', '?')}%
        
        **Interpretação:**
        - Percentual positivo = vento afeta negativamente seu tempo
        - Use para desculpar um treino com vento! 💨
        """)
    else:
        st.info("Execute 'Gerar Insights' no Dashboard primeiro")

with tab4:
    st.subheader("Dados Detalhados")
    if filtered_activities:
        df = pd.DataFrame(filtered_activities)
        
        # Selecionar colunas para exibir
        display_cols = ['name', 'type', 'distance', 'moving_time', 'start_date']
        available_cols = [col for col in display_cols if col in df.columns]
        
        if 'pace' not in df.columns and 'distance' in df.columns and 'moving_time' in df.columns:
            df['pace'] = (df['moving_time'] / 60) / (df['distance'] / 1000)
            available_cols.append('pace')
        
        # Exibir tabela
        st.dataframe(
            df[available_cols],
            use_container_width=True,
            height=400,
            hide_index=True
        )
        
        # Download CSV
        csv = df[available_cols].to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="activities.csv",
            mime="text/csv"
        )
    else:
        st.info("Nenhuma atividade após filtros")

# ============================================================================
# SEÇÃO 3: INSIGHTS RESUMIDOS
# ============================================================================

st.markdown("---")
st.subheader("✨ Insights Resumidos")

if st.session_state.insights:
    col1, col2 = st.columns(2)
    
    with col1:
        if 'best_conditions' in st.session_state.insights:
            st.info(f"☀️ **Melhor Condição**: {st.session_state.insights['best_conditions']}")
    
    with col2:
        if 'wind_impact_percentage' in st.session_state.insights:
            wind_impact = st.session_state.insights['wind_impact_percentage']
            if wind_impact < 0:
                st.success(f"💨 **Vento Ajuda**: {abs(wind_impact):.1f}% de melhora")
            else:
                st.warning(f"💨 **Vento Prejudica**: {wind_impact:.1f}% de piora")
    
    # Lista de insights
    if 'insights_summary' in st.session_state.insights:
        st.markdown("### 📝 Dicas")
        for insight in st.session_state.insights['insights_summary'][:3]:
            st.write(f"✓ {insight}")
else:
    st.info("Gere insights no Dashboard para ver recomendações")

# Footer
st.markdown("---")
st.caption("💡 Dica: Use os filtros à esquerda para explorar padrões nas suas atividades")

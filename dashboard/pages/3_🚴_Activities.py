"""
Activities Page
Lista de atividades com filtros e exportação
"""

import streamlit as st
import pandas as pd
from modules.api_client import get_api_client
from modules.filters import search_activity, apply_filters, create_filter_panel
import logging

logger = logging.getLogger(__name__)

st.set_page_config(page_title="Activities", page_icon="🚴", layout="wide")

st.title("🚴 Activities")
st.markdown("Lista completa de suas atividades com filtros avançados")

# Verificar autenticação
if not st.session_state.authenticated:
    st.warning("⚠️ Autentique-se no Strava para ver atividades")
    st.stop()

# Client API
api_client = get_api_client()

# ============================================================================
# SEÇÃO 1: BUSCA E FILTROS
# ============================================================================

st.subheader("🔍 Busca e Filtros")

# Garantir que temos atividades
if not st.session_state.activities:
    with st.spinner("📥 Buscando atividades..."):
        activities = api_client.get_activities()
        if activities:
            st.session_state.activities = activities
            st.success(f"✅ {len(activities)} atividades carregadas")
        else:
            st.error("❌ Erro ao buscar atividades")
            st.stop()

# Busca por texto
search_term = st.text_input("🔍 Buscar por nome", key="activities_search")

# Aplicar filtros
filter_config = create_filter_panel()

activities = st.session_state.activities

# Aplicar busca de texto
if search_term:
    activities = search_activity(activities)

# Aplicar filtros
activities = apply_filters(
    activities,
    sport_types=filter_config['sports'] if filter_config['sports'] else None,
    start_date=filter_config['start_date'],
    end_date=filter_config['end_date'],
    weather_conditions=filter_config['weather'] if filter_config['weather'] else None,
    pace_min=filter_config['min_pace'],
    pace_max=filter_config['max_pace']
)

st.info(f"📊 Mostrando {len(activities)} de {len(st.session_state.activities)} atividades")

# ============================================================================
# SEÇÃO 2: TABELA DE ATIVIDADES
# ============================================================================

st.subheader("📋 Tabela de Atividades")

if activities:
    df = pd.DataFrame(activities)
    
    # Preparar colunas para exibição
    display_cols = []
    
    # Colunas padrão
    if 'name' in df.columns:
        display_cols.append('name')
    if 'type' in df.columns:
        display_cols.append('type')
    if 'distance' in df.columns:
        display_cols.append('distance')
        df['distance_km'] = df['distance'] / 1000
    if 'moving_time' in df.columns:
        display_cols.append('moving_time')
        df['duration_min'] = df['moving_time'] / 60
    if 'start_date' in df.columns:
        display_cols.append('start_date')
    
    # Colunas opcionais (weather se enriquecidas)
    if 'weather_temperature' in df.columns:
        display_cols.append('weather_temperature')
    if 'weather_condition' in df.columns:
        display_cols.append('weather_condition')
    
    # Criar colunas calculadas
    if 'distance' in df.columns and 'moving_time' in df.columns:
        df['pace_min_km'] = (df['moving_time'] / 60) / (df['distance'] / 1000)
        display_cols.append('pace_min_km')
    
    # Exibir tabela
    st.dataframe(
        df[display_cols],
        use_container_width=True,
        height=500,
        hide_index=True
    )
    
    # ========================================================================
    # SEÇÃO 3: EXPORTAÇÃO
    # ========================================================================
    
    st.markdown("---")
    st.subheader("📥 Exportar Dados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # CSV
        csv_data = df[display_cols].to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name="activities.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # JSON
        json_data = df[display_cols].to_json(orient='records', indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name="activities.json",
            mime="application/json",
            use_container_width=True
        )
    
    # ========================================================================
    # SEÇÃO 4: ESTATÍSTICAS
    # ========================================================================
    
    st.markdown("---")
    st.subheader("📊 Estatísticas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📊 Total",
            len(activities),
            f"de {len(st.session_state.activities)}"
        )
    
    if 'distance' in df.columns:
        with col2:
            total_km = df['distance'].sum() / 1000
            st.metric(
                "🏃 Distância",
                f"{total_km:.1f} km",
                f"{total_km / len(activities):.1f} km/ativ"
            )
    
    if 'moving_time' in df.columns:
        with col3:
            total_hours = df['moving_time'].sum() / 3600
            st.metric(
                "⏱️ Tempo",
                f"{total_hours:.1f} h",
                f"{total_hours / len(activities):.1f} h/ativ"
            )
    
    if 'type' in df.columns:
        with col4:
            most_common = df['type'].mode()[0] if len(df['type'].mode()) > 0 else "N/A"
            st.metric(
                "🏅 Tipo Principal",
                most_common,
                f"{len(df[df['type'] == most_common])} vezes"
            )
    
    # ========================================================================
    # SEÇÃO 5: ATIVIDADES POR TIPO
    # ========================================================================
    
    st.markdown("---")
    st.subheader("📈 Atividades por Tipo")
    
    if 'type' in df.columns:
        activity_counts = df['type'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.bar_chart(activity_counts, use_container_width=True)
        
        with col2:
            st.write("### Resumo por Tipo")
            for activity_type, count in activity_counts.items():
                st.write(f"**{activity_type}**: {count} atividades")

else:
    st.warning("Nenhuma atividade encontrada com os filtros selecionados")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.caption("💡 Dica: Exporte seus dados e importe em outras ferramentas de análise")

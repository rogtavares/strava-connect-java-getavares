# 📊 BLOCO 3: Streamlit Dashboard - Plano Detalhado

**Duração:** 60 minutos  
**Status:** ⏳ EM PROGRESSO  
**Objetivo:** Criar dashboard visual interativo com Streamlit

---

## 🎯 Visão Geral

Dashboard Streamlit com 3 páginas principais:
1. **📈 Dashboard** - Overview com métricas principais
2. **📊 Analytics** - Análise detalhada por condições
3. **🚴 Activities** - Lista de atividades com filtros

---

## 📋 Estrutura de Arquivos

```
python-streamlit/
├── app.py                      (main entry - 150 linhas)
├── config.py                   (configuration - 50 linhas)
├── pages/
│   ├── 1_📈_Dashboard.py       (150 linhas)
│   ├── 2_📊_Analytics.py       (200 linhas)
│   └── 3_🚴_Activities.py      (150 linhas)
├── modules/
│   ├── api_client.py           (80 linhas - comunicação com APIs)
│   ├── charts.py               (150 linhas - gráficos Plotly)
│   └── filters.py              (80 linhas - widgets de filtro)
├── requirements.txt            (6 linhas)
├── Dockerfile                  (20 linhas)
├── docker-compose.yml          (refência ao FastAPI)
└── README.md                   (install, usage, features)
```

**Total:** ~1000 linhas de código

---

## ⏱️ Timeline de Implementação

| Min | Tarefa | Linhas | Status |
|-----|--------|--------|--------|
| 0-8 | Estrutura básica + config | 100 | ⏳ |
| 8-16 | API Client module | 80 | ⏳ |
| 16-26 | Charts module | 150 | ⏳ |
| 26-34 | Filters module | 80 | ⏳ |
| 34-49 | app.py (main) | 150 | ⏳ |
| 49-64 | 3 Pages (Dashboard, Analytics, Activities) | 500 | ⏳ |
| 64-75 | Configuração Docker + requirements | 30 | ⏳ |
| 75-90 | Testes + ajustes finais | ... | ⏳ |

---

## 🔨 Implementação

### 1. **config.py** (5 min) - 50 linhas

Configurações centralizadas:
- URLs das APIs (Spring, FastAPI)
- Temas Streamlit
- Constantes de cores
- Configuração de timeouts

```python
# Exemplo
STRAVA_API_URL = "http://localhost:8080/api"
FASTAPI_URL = "http://localhost:8000"
COLORS = {"primary": "#1f77b4", "success": "#2ca02c"}
```

### 2. **api_client.py** (10 min) - 80 linhas

Cliente HTTP para comunicação:
- `get_activities()` - Spring
- `enrich_activities()` - FastAPI
- `get_insights()` - FastAPI
- Error handling com retry

```python
import requests
from functools import lru_cache

class StravaAPIClient:
    def get_activities(self):
        # Chamada ao Spring
    
    def enrich_activities(self, activities):
        # Chamada ao FastAPI /enrich
    
    def get_insights(self, activities):
        # Chamada ao FastAPI /insights
```

### 3. **charts.py** (15 min) - 150 linhas

Gráficos interativos com Plotly:
- `plot_pace_vs_temp()` - Scatter plot
- `plot_performance_by_condition()` - Bar chart
- `plot_wind_impact()` - Line chart
- `plot_stats_cards()` - Metric cards
- `plot_heatmap()` - Performance heatmap

```python
import plotly.graph_objects as go
import plotly.express as px

def plot_pace_vs_temp(data):
    # Scatter com hover customizado
    
def plot_performance_by_condition(insights):
    # Agrupado por weather condition
```

### 4. **filters.py** (10 min) - 80 linhas

Widgets de filtro reutilizáveis:
- `filter_by_sport()` - Tipos de atividade
- `filter_by_date_range()` - Date picker
- `filter_by_weather()` - Condições
- `search_activity()` - Busca por nome

```python
import streamlit as st
from datetime import datetime, timedelta

def filter_by_date_range():
    col1, col2 = st.columns(2)
    with col1:
        start = st.date_input("Data inicial")
    with col2:
        end = st.date_input("Data final")
    return start, end
```

### 5. **app.py** (main) - 150 linhas

Configuração principal do Streamlit:
- Page config (title, icon, layout)
- Sidebar com navegação
- Session state management
- CSS customizações

```python
import streamlit as st
from config import *

st.set_page_config(
    page_title="Strava Insights",
    page_icon="🚴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state
if 'activities' not in st.session_state:
    st.session_state.activities = []

# Sidebar
with st.sidebar:
    st.title("⚙️ Configurações")
    # Navigation handled by Pages
```

### 6. **pages/1_📈_Dashboard.py** - 150 linhas

Dashboard com métricas principais:
- Cards com KPIs (Total Atividades, Dist Total, Tempo Total)
- Gráfico de atividades por mês
- Velocidade média por tipo de atividade
- Atividade recente

```python
import streamlit as st
from modules.api_client import StravaAPIClient
from modules.charts import *

st.title("📈 Dashboard")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Atividades", 42)
with col2:
    st.metric("Km Totais", "1,234 km")
with col3:
    st.metric("Horas", "156h")

# Gráficos
st.plotly_chart(plot_activities_per_month(activities))
```

### 7. **pages/2_📊_Analytics.py** - 200 linhas

Análise detalhada:
- Filtros avançados (esporte, data, clima)
- Pace vs Temperatura (scatter)
- Performance por condição climática (bar)
- Impacto do vento (line)
- Tabela comparativa

```python
import streamlit as st
from modules.filters import *
from modules.charts import *

st.title("📊 Analytics")

# Filtros
col1, col2 = st.columns(2)
with col1:
    sport = st.multiselect("Tipo de Atividade", [...])
with col2:
    conditions = st.multiselect("Condições Climáticas", [...])

# Gráficos
st.plotly_chart(plot_pace_vs_temp(filtered_data))
st.plotly_chart(plot_performance_by_condition(insights))
```

### 8. **pages/3_🚴_Activities.py** - 150 linhas

Lista de atividades:
- Tabela com search/filtros
- Ordenação por colunas
- Detalhes expandíveis por atividade
- Export para CSV
- Mapa de atividades (com Folium)

```python
import streamlit as st
import pandas as pd

st.title("🚴 Activities")

# Search
search = st.text_input("🔍 Buscar atividade...")

# Tabela com filtros
df = pd.DataFrame(activities)
st.dataframe(
    df,
    use_container_width=True,
    height=400,
    hide_index=True
)

# Export
csv = df.to_csv(index=False)
st.download_button(
    "📥 Download CSV",
    csv,
    "activities.csv",
    "text/csv"
)
```

### 9. **requirements.txt** - 6 linhas

```
streamlit==1.28.1
plotly==5.17.0
pandas==2.1.1
requests==2.31.0
python-dotenv==1.0.0
folium==0.14.0
```

### 10. **Dockerfile + docker-compose.yml** - 20 linhas

Containerização do Streamlit

---

## 🎨 Features Principais

### Dashboard (Página 1)
- 📊 3 KPI Cards (Atividades, Km, Horas)
- 📈 Gráfico de atividades por mês
- 🏃 Velocidade média por tipo
- 🆕 Atividades recentes
- 📍 Map com últimas atividades

### Analytics (Página 2)
- 🔥 **Pace vs Temperatura** - Scatter interativo
  - X: Temperatura
  - Y: Pace (min/km)
  - Color: Condição climática
  - Size: Distância
  
- 🌤️ **Performance por Condição** - Bar chart
  - Média de pace por (sunny, cloudy, rainy, etc)
  - Comparação com baseline
  
- 💨 **Impacto do Vento** - Line chart
  - Variação de pace vs velocidade do vento
  
- 📊 **Tabela Comparativa**
  - Filtros dinâmicos
  - Ordenação

### Activities (Página 3)
- 📋 **Tabela de Atividades**
  - Busca em tempo real
  - Filtro por tipo/data
  - Ordenação por coluna
  
- 📥 **Export**
  - Download CSV
  - Download PNG dos gráficos
  
- 🗺️ **Mapa Interativo**
  - Plotar rotas
  - Ver detalhes ao clicar

---

## 🔌 Integração com APIs

### Spring Boot (Porta 8080)
```
GET /api/authorize - Iniciar OAuth
GET /api/authorize/callback - Callback OAuth
GET /api/activities/export - Listar atividades
```

### FastAPI (Porta 8000)
```
GET / - Health check
POST /enrich - Enriquecer com weather
POST /insights - Gerar insights
```

**Flow:**
1. User clica "Conectar Strava" no Streamlit
2. Redireciona para Spring OAuth
3. Token salvo em session_state
4. Buscar atividades via Spring
5. Enriquecer via FastAPI
6. Gerar insights via FastAPI
7. Exibir no dashboard

---

## 🎯 Checklist

- [ ] `config.py` criado
- [ ] `api_client.py` criado
- [ ] `charts.py` criado
- [ ] `filters.py` criado
- [ ] `app.py` criado
- [ ] `pages/1_📈_Dashboard.py` criado
- [ ] `pages/2_📊_Analytics.py` criado
- [ ] `pages/3_🚴_Activities.py` criado
- [ ] `requirements.txt` atualizado
- [ ] `Dockerfile` criado
- [ ] `docker-compose.yml` atualizado
- [ ] `README.md` criado
- [ ] Testes básicos (session state)
- [ ] Commit e push
- [ ] Docker build funcionando

---

## 🚀 Inicialização Local

```bash
cd python-streamlit

# Install
pip install -r requirements.txt

# Run
streamlit run app.py

# Acesso
# Abrir http://localhost:8501
```

---

## ⚠️ Requisitos

- **Python:** 3.11+
- **Spring Boot:** Rodando em http://localhost:8080
- **FastAPI:** Rodando em http://localhost:8000
- **Streamlit:** Port 8501 disponível

---

**Tempo Total Estimado:** 60 minutos  
**Linhas de Código:** ~1000  
**Complexidade:** Média (muitos componentes, mas cada um simples)

**Iniciado:** Agora  
**Estimado para conclusão:** +60 minutos (total ~117 min até aqui)

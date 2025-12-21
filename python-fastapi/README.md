# 🏃 Strava Insights API (FastAPI)

API inteligente que enriquece dados de atividades do Strava com dados climáticos e gera insights automáticos sobre seu desempenho.

## 🚀 Features

### ✅ Enriquecimento de Dados
- Busca clima histórico via OpenWeather API (free tier)
- Calcula pace (min/km) automaticamente
- Classifica condições climáticas (frio, ideal, quente)
- Extrai dados de temperatura, umidade, vento, pressão

### ✅ Insights Inteligentes (100% Gratuito)
- **Análise por Condição Climática**: Seu melhor pace é em dias frios ou quentes?
- **Análise por Temperatura**: Performance em 5 faixas diferentes
- **Impacto do Vento**: Como o vento afeta seu desempenho?
- **Melhores Condições**: Quando você corre melhor?
- **Comparações Estatísticas**: Média, mediana, melhor, pior pace

## 📦 Instalação

### 1. Pré-requisitos
- Python 3.8+
- Pip
- OpenWeather API Key (grátis em https://openweathermap.org/api)

### 2. Instalação de Dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente
```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env com suas credenciais
# BACKEND_URL=http://localhost:8080
# OPENWEATHER_API_KEY=sua_chave_aqui
```

## 🏃 Como Usar

### Iniciar o servidor de desenvolvimento
```bash
python run.py
# ou
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

### Acessar a API
- **Documentação Interativa**: http://localhost:8000/docs
- **Documentação (ReDoc)**: http://localhost:8000/redoc

## 📡 Endpoints

### `GET /` - Info da API
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "name": "Strava Insights API",
  "version": "1.0.0",
  "endpoints": {
    "/enrich": "Get enriched activities with weather and insights",
    "/insights": "Get AI-generated insights about your performance",
    "/health": "Health check"
  }
}
```

---

### `GET /health` - Health Check
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy"
}
```

---

### `GET /enrich` - Enriquecer Atividades com Clima
Busca atividades do backend Java, adiciona dados climáticos históricos e calcula métricas de performance.

```bash
curl http://localhost:8000/enrich
```

**Response Example:**
```json
[
  {
    "id": 123456,
    "name": "Morning Run",
    "distance": 10000,
    "moving_time": 2700,
    "average_heartrate": 165,
    "start_date": "2025-11-20T06:30:00Z",
    "start_latlng": [-23.5505, -46.6333],
    "weather": {
      "current": {
        "temp": 21.5,
        "feels_like": 20.8,
        "humidity": 75,
        "wind_speed": 3.2,
        "clouds": 45,
        "pressure": 1013,
        "weather": [{"main": "Partly Cloudy"}]
      }
    },
    "pace_min_per_km": 4.5,
    "weather_data": {
      "temperature": 21.5,
      "humidity": 75,
      "wind_speed": 3.2,
      "clouds": 45,
      "weather_main": "Partly Cloudy",
      "feels_like": 20.8,
      "pressure": 1013
    },
    "weather_condition": "ideal"
  },
  ...
]
```

---

### `GET /insights` - Insights Inteligentes 🧠
Analisa padrões de desempenho em relação às condições climáticas e gera insights automáticos.

```bash
curl http://localhost:8000/insights
```

**Response Example:**
```json
{
  "summary": [
    "🏃 Você corre melhor em dias ideal! Pace médio: 4.35 min/km",
    "💨 Vento reduz seu pace em ~8.5% (comparado a dias com pouco vento)",
    "📊 Total de atividades analisadas: 42"
  ],
  "performance_by_condition": {
    "cold": {
      "avg_pace": 4.65,
      "median_pace": 4.58,
      "count": 8,
      "best_pace": 4.12,
      "worst_pace": 5.30
    },
    "ideal": {
      "avg_pace": 4.35,
      "median_pace": 4.32,
      "count": 25,
      "best_pace": 3.85,
      "worst_pace": 5.10
    },
    "warm": {
      "avg_pace": 4.55,
      "median_pace": 4.52,
      "count": 9,
      "best_pace": 4.20,
      "worst_pace": 5.05
    }
  },
  "performance_by_temperature": {
    "ideal_15_to_22": {
      "avg_pace": 4.35,
      "count": 25,
      "best_pace": 3.85
    },
    "warm_22_to_28": {
      "avg_pace": 4.55,
      "count": 9,
      "best_pace": 4.20
    },
    "cold_below_5": {
      "avg_pace": 4.65,
      "count": 8,
      "best_pace": 4.12
    }
  },
  "best_conditions": {
    "condition": "ideal",
    "avg_pace": 4.35,
    "count": 25,
    "insight": "🏃 Você corre melhor em dias ideal! Pace médio: 4.35 min/km"
  },
  "wind_impact": {
    "avg_pace_low_wind": 4.38,
    "avg_pace_high_wind": 4.75,
    "impact_percent": 8.5,
    "insight": "💨 Vento reduz seu pace em ~8.5% (comparado a dias com pouco vento)"
  },
  "total_activities_analyzed": 42
}
```

## 🔧 Configuração

### Variáveis de Ambiente (.env)

```bash
# Backend Java Spring URL (obrigatório)
BACKEND_URL=http://localhost:8080

# OpenWeather API Key (obrigatório para clima)
# Registre-se grátis: https://openweathermap.org/api
OPENWEATHER_API_KEY=sua_chave_aqui

# FastAPI Server
FASTAPI_HOST=127.0.0.1
FASTAPI_PORT=8000
```


## 🔐 Segurança

- ✅ Variáveis sensíveis em `.env` (não commitidas no Git)
- ✅ Timeouts em requisições HTTP
- ✅ Tratamento de erros robusto
- ✅ Logging estruturado

## 🆓 Por que é Gratuito?

1. **OpenWeather Free API**: Histórico climático sem limite
2. **FastAPI**: Framework open-source
3. **Python**: Linguagem gratuita
4. **Insights Inteligentes**: Algoritmos próprios, sem dependência de IA paga

## 🚀 Próximos Passos

1. [ ] Integrar com Streamlit Dashboard
2. [ ] Cache de requisições (Redis opcional)
3. [ ] Análise de desempenho por hora do dia
4. [ ] Previsão de performance futura
5. [ ] Exportar relatórios em PDF

## 📚 Recursos Úteis

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenWeather API](https://openweathermap.org/api)
- [Strava API v3](https://developers.strava.com/docs/reference/)

## 👨‍💻 Desenvolvedor

Projeto Strava Connect - 2025

## 📄 Licença

MIT

---

**Dúvidas?** Abra uma issue ou consulte a documentação interativa em `/docs`

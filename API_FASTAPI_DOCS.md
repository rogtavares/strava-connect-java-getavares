# 🚀 API FastAPI - Strava Insights

## 📌 Visão Geral

API REST que enriquece atividades do Strava com dados climáticos e gera insights inteligentes sobre desempenho.

---

## 🎯 Funcionalidades

### ✅ O que a API faz:
1. **Busca atividades** do backend Java
2. **Enriquece com clima** usando OpenWeather API
3. **Calcula métricas** (pace, frequência cardíaca)
4. **Gera insights** sobre desempenho vs clima
5. **Analisa padrões** (melhor temperatura, impacto do vento)

---

## 📡 Endpoints Disponíveis

### 1. **GET /** - Info da API
```bash
curl http://localhost:8000/
```

**Resposta:**
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

### 2. **GET /health** - Health Check
```bash
curl http://localhost:8000/health
```

**Resposta:**
```json
{
  "status": "healthy"
}
```

---

### 3. **GET /enrich** - Atividades Enriquecidas
Busca atividades e adiciona dados climáticos.

```bash
curl http://localhost:8000/enrich
```

**Resposta:**
```json
[
  {
    "id": 123456,
    "name": "Morning Run",
    "distance": 5000,
    "moving_time": 1800,
    "pace_min_per_km": 6.0,
    "weather": {
      "current": {
        "temp": 18,
        "humidity": 65,
        "wind_speed": 3.5,
        "weather": [{"main": "Clear"}]
      }
    },
    "weather_condition": "ideal"
  }
]
```

---

### 4. **GET /insights** - Insights Inteligentes
Gera análises sobre seu desempenho.

```bash
curl http://localhost:8000/insights
```

**Resposta:**
```json
{
  "summary": [
    "🏃 Você corre melhor em dias ideal! Pace médio: 5.8 min/km",
    "💨 Vento reduz seu pace em ~8.5% (comparado a dias com pouco vento)",
    "📊 Total de atividades analisadas: 30"
  ],
  "performance_by_condition": {
    "cold": {
      "avg_pace": 6.2,
      "median_pace": 6.1,
      "count": 5,
      "best_pace": 5.9,
      "worst_pace": 6.5
    },
    "ideal": {
      "avg_pace": 5.8,
      "median_pace": 5.7,
      "count": 15,
      "best_pace": 5.4,
      "worst_pace": 6.2
    },
    "warm": {
      "avg_pace": 6.4,
      "median_pace": 6.3,
      "count": 10,
      "best_pace": 6.0,
      "worst_pace": 7.0
    }
  },
  "performance_by_temperature": {
    "ideal_15_to_22": {
      "avg_pace": 5.8,
      "count": 15,
      "best_pace": 5.4
    },
    "warm_22_to_28": {
      "avg_pace": 6.4,
      "count": 10,
      "best_pace": 6.0
    }
  },
  "best_conditions": {
    "condition": "ideal",
    "avg_pace": 5.8,
    "count": 15,
    "insight": "🏃 Você corre melhor em dias ideal! Pace médio: 5.80 min/km"
  },
  "wind_impact": {
    "avg_pace_low_wind": 5.9,
    "avg_pace_high_wind": 6.4,
    "impact_percent": 8.5,
    "insight": "💨 Vento reduz seu pace em ~8.5% (comparado a dias com pouco vento)"
  },
  "total_activities_analyzed": 30
}
```

---

## 🔧 Como Rodar

### Pré-requisitos:
```bash
# Instalar Python 3.11+
# Verificar instalação
python --version
```

### 1. Instalar Dependências
```bash
cd python-fastapi
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente
```bash
# Windows PowerShell
$env:BACKEND_URL="http://localhost:8080"
$env:OPENWEATHER_API_KEY="sua_chave_aqui"

# Linux/Mac
export BACKEND_URL="http://localhost:8080"
export OPENWEATHER_API_KEY="sua_chave_aqui"
```

### 3. Rodar a API
```bash
python app.py
```

### 4. Acessar
```
http://localhost:8000
http://localhost:8000/docs  # Swagger UI
```

---

## 📊 Análises Geradas

### 1. **Performance por Condição Climática**
- Agrupa atividades por: cold, cool, ideal, warm, hot
- Calcula: pace médio, mediana, melhor e pior

### 2. **Performance por Temperatura**
- Faixas: <5°C, 5-15°C, 15-22°C, 22-28°C, >28°C
- Identifica temperatura ideal para treino

### 3. **Impacto do Vento**
- Compara pace com vento baixo (<5 m/s) vs alto (>10 m/s)
- Calcula percentual de impacto

### 4. **Melhores Condições**
- Identifica condição climática com melhor desempenho
- Gera insight personalizado

---

## 🧪 Testar com cURL

### Teste 1: Health Check
```bash
curl http://localhost:8000/health
```

### Teste 2: Ver Documentação
```bash
curl http://localhost:8000/
```

### Teste 3: Buscar Atividades Enriquecidas
```bash
curl http://localhost:8000/enrich
```

### Teste 4: Gerar Insights
```bash
curl http://localhost:8000/insights
```

---

## 🔗 Integração

### Com Backend Java:
```
FastAPI → http://localhost:8080/activities/export
```

### Com OpenWeather:
```
FastAPI → https://api.openweathermap.org/data/2.5/onecall/timemachine
```

### Com Dashboard Streamlit:
```
Streamlit → http://localhost:8000/insights
```

---

## 📝 Dependências

```txt
fastapi==0.104.1
uvicorn==0.24.0
requests==2.31.0
python-dotenv==1.0.0
```

---

## 🐛 Troubleshooting

### Erro: "Python não encontrado"
```bash
# Instalar Python 3.11+
# Adicionar ao PATH
```

### Erro: "Module not found"
```bash
pip install -r requirements.txt
```

### Erro: "Connection refused"
```bash
# Verificar se backend Java está rodando
curl http://localhost:8080/health
```

### Erro: "OpenWeather API error"
```bash
# Verificar chave da API
echo $env:OPENWEATHER_API_KEY
```

---

## 📚 Documentação Relacionada

- **Backend Java:** `BACKEND_JAVA_CORRIGIDO.md`
- **OAuth 2.0:** `OAUTH2_GUIDE.md`
- **Guia Prático:** `GUIA_PRATICO_USO.md`

---

**✨ API FastAPI pronta para gerar insights inteligentes sobre seus treinos!**

**Criado por:** Rogério Tavares | **Data:** 25/11/2025
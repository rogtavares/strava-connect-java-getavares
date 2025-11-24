# 🏗️ ARCHITECTURE.md - Arquitetura Técnica

**Data:** 20 de novembro de 2025  
**Versão:** 1.0  
**Status:** ✅ Design Complete

---

## 📊 Diagrama de Componentes

```
┌──────────────────────────────────────────────────────────────────┐
│                         USUÁRIO FINAL                             │
│                    (Web Browser / App)                            │
└────────┬─────────────────────────────────────────────────┬───────┘
         │                                                 │
    ┌────▼────────┐                              ┌────────▼────┐
    │  Java Spring│                              │  Streamlit  │
    │  Backend    │                              │  Dashboard  │
    │  :8080      │                              │  :8501      │
    └────┬────────┘                              └────────┬────┘
         │                                                 │
         │  HTTP GET /activities/export                   │
         │                                                 │
    ┌────▼─────────────────────────────────────────┬──────┘
    │                                              │
    │         FastAPI Enrichment Service          │
    │              :8000                          │
    │  (Atividades + Clima + Insights)            │
    │                                              │
    └────┬──────────────────────────────┬──────────┘
         │                              │
    ┌────▼──────┐             ┌────────▼────┐
    │  Strava   │             │ OpenWeather │
    │   API     │             │  API (Free) │
    │ (OAuth)   │             │             │
    └───────────┘             └─────────────┘
```

---

## 🔄 Fluxo de Dados

### 1. AUTENTICAÇÃO

```
Usuário
    ↓
[1] GET /authorize (Java Spring)
    ↓
Redireciona para Strava OAuth
    ↓
Usuário autoriza
    ↓
[2] Redirect com code para /callback
    ↓
Java Spring troca code por tokens
    ↓
Salva tokens em tokens.json
    ↓
✅ Autenticado
```

### 2. BUSCAR ATIVIDADES

```
GET /activities/export (Java Spring)
    ↓
Valida token (com refresh se necessário)
    ↓
Chama Strava API v3 /athlete/activities
    ↓
Retorna JSON puro com:
  - id, name, distance, moving_time
  - average_heartrate, start_date
  - start_latlng, etc
    ↓
✅ Atividades Recuperadas
```

### 3. ENRIQUECER COM CLIMA

```
GET /enrich (FastAPI)
    ↓
[1] Busca /activities/export do Java Spring
    ↓
[2] Para cada atividade:
    - Extrai latitude/longitude
    - Extrai data/hora do treino
    - Chama OpenWeather Historic API
    - Recupera clima da data/local
    ↓
[3] Monta estrutura:
  {
    "atividade": {...atividade_original...},
    "weather": {...dados_clima...},
    "pace_min_per_km": 4.35,
    "weather_condition": "ideal"
  }
    ↓
✅ Atividades Enriquecidas
```

### 4. GERAR INSIGHTS

```
GET /insights (FastAPI)
    ↓
Carrega atividades enriquecidas
    ↓
Cria instância StravaInsights
    ↓
[1] Análise por Condição Climática
    └─ Agrupa por temperatura
    └─ Calcula pace médio/mediano
    └─ Retorna: avg, median, count, best, worst
    ↓
[2] Análise por Faixa de Temperatura
    └─ 5 ranges diferentes
    └─ Retorna: avg_pace, count, best_pace
    ↓
[3] Impacto do Vento
    └─ Low wind (< 5 m/s) vs High wind (> 10 m/s)
    └─ Calcula percentual de impacto
    ↓
[4] Melhores Condições
    └─ Encontra condition com menor pace
    └─ Gera insight: "Você corre melhor em..."
    ↓
[5] Resumo em Linguagem Natural
    └─ 3 principais insights
    └─ Em português, amigável
    ↓
✅ Insights Gerados
```

### 5. VISUALIZAR DASHBOARD

```
Streamlit App
    ↓
[1] Página Principal
    ├─ Carrega dados do FastAPI /insights
    ├─ Exibe métricas principais
    ├─ Cards com últimas atividades
    ↓
[2] Dashboard de Análises
    ├─ Tab: Performance por Condição
    │  └─ Gráfico Plotly interativo
    ├─ Tab: Performance por Temperatura
    │  └─ Gráfico Plotly interativo
    ├─ Tab: Impacto do Vento
    │  └─ Gráfico comparativo
    ↓
[3] Analytics Avançado
    ├─ Pace vs Temperatura (scatter plot)
    ├─ Performance vs Vento
    ├─ Comparação com média pessoal
    ↓
[4] Tabela de Atividades
    ├─ Filtrável (período, tipo, etc)
    ├─ Ordenável
    ├─ Busca por texto
    ↓
[5] Exportar Relatório
    ├─ Botão: Download PDF
    ├─ Inclui gráficos e insights
    ├─ Formatação profissional
    ↓
✅ Dashboard Visual Completo
```

---

## 🗂️ Estrutura de Pastas - Versão Final

```
strava-connect-java-getavares/
│
├── 📄 README.md                  ← Overview do projeto
├── 📄 ARCHITECTURE.md            ← Este arquivo
├── 📄 SETUP.md                   ← Guia de instalação
├── 📄 ROADMAP.md                 ← Planejamento
├── 📄 LICENSE                    ← MIT License
├── 📄 CONTRIBUTING.md            ← Diretrizes
├── 📄 .gitignore                 ← Git ignore rules
├── 📄 .env.example               ← Template de variáveis
│
├── 📂 strava-spring/             ← Java Spring Backend
│   ├── pom.xml
│   ├── src/
│   │   ├── main/java/com/getavares/strava/
│   │   │   ├── StravaSpringApplication.java
│   │   │   ├── StravaController.java       (MELHORADO)
│   │   │   ├── exception/
│   │   │   │   ├── StravaException.java
│   │   │   │   ├── GlobalExceptionHandler.java
│   │   │   │   └── UnauthorizedException.java
│   │   │   ├── service/
│   │   │   │   ├── StravaService.java      (NOVO)
│   │   │   │   ├── ActivityService.java    (NOVO)
│   │   │   │   └── TokenService.java       (NOVO)
│   │   │   └── validation/
│   │   │       └── InputValidator.java
│   │   │
│   │   └── test/java/com/getavares/strava/
│   │       ├── StravaServiceTest.java
│   │       └── ActivityServiceTest.java
│   │
│   └── src/main/resources/
│       └── application.properties          (NOVO)
│
├── 📂 python-fastapi/            ← FastAPI Enrichment (✅ PRONTO)
│   ├── app.py                    ← Main app (354 lines)
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── .env.example
│   ├── run.py
│   ├── setup.sh
│   ├── test_api.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── README.md
│   ├── INSIGHTS.md
│   └── IMPLEMENTATION_SUMMARY.md
│
├── 📂 python-streamlit/          ← Streamlit Dashboard (NOVO)
│   ├── app.py                    ← Main Streamlit app
│   ├── pages/
│   │   ├── 01_Dashboard.py       ← Overview visual
│   │   ├── 02_Analytics.py       ← Análises detalhadas
│   │   └── 03_Activities.py      ← Tabela interativa
│   ├── modules/
│   │   ├── api_client.py         ← Chamadas HTTP
│   │   ├── charts.py             ← Gráficos Plotly
│   │   ├── filters.py            ← Filtros e busca
│   │   └── export.py             ← Exportar PDF
│   ├── config.py                 ← Configurações
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── 📂 docs/                      ← Documentação adicional
│   ├── API.md
│   ├── TROUBLESHOOTING.md
│   └── FAQ.md
│
└── 📄 docker-compose.yml         ← Orquestração principal
```

---

## 🔌 Endpoints Principais

### Java Spring (Backend)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/authorize` | Inicia fluxo OAuth Strava |
| GET | `/callback?code=...` | Callback de autenticação |
| GET | `/activities/export` | Retorna atividades em JSON |

### FastAPI (Enrichment)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Info da API |
| GET | `/health` | Health check |
| GET | `/enrich` | Atividades + clima |
| GET | `/insights` | Análise inteligente |

### Streamlit (Dashboard)

| Página | Descrição |
|--------|-----------|
| `/` | Página principal com overview |
| `/Dashboard` | Gráficos interativos |
| `/Analytics` | Análises detalhadas |
| `/Activities` | Tabela filtrável |

---

## 📡 Comunicação Entre Serviços

### Spring → FastAPI

```
Spring chama:
GET http://localhost:8000/insights

Response:
{
  "summary": [...],
  "performance_by_condition": {...},
  "performance_by_temperature": {...},
  "best_conditions": {...},
  "wind_impact": {...}
}
```

### FastAPI → Streamlit

```
Streamlit carrega:
GET http://localhost:8000/insights

Exibe em gráficos e cards
```

### Segurança

- ✅ Variáveis de ambiente (.env)
- ✅ Tokens JWT em cookies (opcional)
- ✅ HTTPS em produção
- ✅ Rate limiting no FastAPI
- ✅ CORS configurado

---

## 💾 Persistência de Dados

### Tokens Strava
- **Local:** `strava-spring/tokens.json`
- **Formato:** JSON
- **Conteúdo:** access_token, refresh_token, expires_at

### Cache (Futuro)
- **Opcional:** Redis para cache de atividades
- **TTL:** 1 hora (configurável)

### Banco de Dados (Futuro)
- **Opcional:** PostgreSQL para histórico
- **Tabelas:** activities, weather_history, insights

---

## 🔐 Segurança

### Variáveis Sensíveis
```
.env (local) - não comitado
├── STRAVA_CLIENT_ID
├── STRAVA_CLIENT_SECRET
├── STRAVA_REDIRECT_URI
└── OPENWEATHER_API_KEY
```

### Tokens
- Access token: Curta duração (6 horas Strava)
- Refresh token: Longa duração (pode expirar)
- Armazenado: Criptografado (futuro)

### API Keys
- OpenWeather: Public key (sem limite de rate)
- Strava: Private (manter seguro)

---

## 🚀 Deployment

### Local Development
```bash
docker-compose up
```

### Produção (Exemplo)
```bash
# AWS/Azure/GCP
1. Deploy Spring em ECS/App Service
2. Deploy FastAPI em Lambda/Cloud Run
3. Deploy Streamlit em Streamlit Cloud / Vercel
```

---

## 📈 Performance

### Tempos Esperados

| Operação | Tempo |
|----------|-------|
| Autenticar | ~2-3s |
| Buscar 50 atividades | ~1-2s |
| Enriquecer com clima | ~5-10s |
| Gerar insights | ~0.5-1s |
| Renderizar dashboard | ~1-2s |
| **Total** | **~10-20s** |

### Otimizações Futuras
- Cache de atividades
- Processamento async
- Batch requests OpenWeather
- CDN para assets estáticos

---

## 🔄 Ciclo de Vida das Atividades

```
[1] Strava API
    ↓ (atividade bruta)
[2] Java Spring
    ↓ (com tokens válidos)
[3] FastAPI - /enrich
    ↓ (adiciona clima)
[4] FastAPI - /insights
    ↓ (gera análises)
[5] Streamlit
    ↓ (exibe visual)
[6] Usuário vê insights!
```

---

## 🧪 Testing Strategy

### Unit Tests
- Spring: JUnit 5
- FastAPI: pytest
- Streamlit: pytest (pages)

### Integration Tests
- Spring → FastAPI
- FastAPI → OpenWeather
- Streamlit → FastAPI

### E2E Tests
- OAuth flow
- Full data pipeline
- Dashboard rendering

---

## 📝 Versionamento

- **Semver:** MAJOR.MINOR.PATCH
- **Atual:** 1.0.0
- **Próximas:** 1.1.0 (cache), 1.2.0 (DB)

---

**Criado em:** 20 de novembro de 2025  
**Última atualização:** 20 de novembro de 2025  
**Status:** ✅ Design Review Complete

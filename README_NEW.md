# 🏃 Strava Connect - Integração Completa

![Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-blue)
![Java](https://img.shields.io/badge/java-21-red)
![Python](https://img.shields.io/badge/python-3.11-blue)

**Integração completa com API do Strava** | **Análises Inteligentes** | **Dashboard Visual** | **100% Gratuito** 🆓

---

## 🎯 O Que Você Tem

### ✅ Java Spring (Backend)
- Autenticação OAuth 2.0 com Strava
- Endpoints: `/authorize`, `/callback`, `/activities/export`
- Tokens persistidos em JSON
- Pronto para melhorias profissionais

### ✅ FastAPI (Enriquecimento)
- 354 linhas de código Python
- Classe StravaInsights com 8 métodos
- 4 endpoints funcionais: `/`, `/health`, `/enrich`, `/insights`
- 4 tipos de análises inteligentes

### ✅ Insights Inteligentes
- 📊 Análise por Condição Climática (5 categorias)
- 🌡️ Análise por Faixa de Temperatura (5 ranges)
- 💨 Cálculo de Impacto do Vento (em %)
- 🎯 Busca de Melhores Condições
- 📈 Insights em Linguagem Natural

### ⏳ Em Desenvolvimento (AGORA!)
- 🎨 Streamlit Dashboard Visual
- 🔧 Java Spring Melhorado (validação, logging, service layer)
- 📋 Estrutura Profissional do Repositório

---

## 📊 Arquitetura

```
┌─────────────────┐
│  Streamlit      │ ← Dashboard Visual
│  Dashboard      │
│  :8501          │
└────────┬────────┘
         │
    ┌────┴──────┐
    │            │
┌───▼────┐   ┌──▼──────┐
│ Spring │   │ FastAPI  │ ← Insights
│ :8080  │   │ :8000    │   Inteligentes
└────┬───┘   └──┬───────┘
     │          │
     └────┬─────┘
          │
      ┌───┴──────────┐
      │              │
   ┌──▼────┐    ┌───▼─────────┐
   │Strava │    │OpenWeather  │
   │OAuth  │    │API (Free)   │
   └───────┘    └─────────────┘
```

---

## 🚀 Quick Start

### Option 1: Com Docker
```bash
docker-compose up --build
```

### Option 2: Localmente

**Java (Backend):**
```bash
cd strava-spring
mvn spring-boot:run
# http://localhost:8080
```

**FastAPI (Insights):**
```bash
cd python-fastapi
pip install -r requirements.txt
cp .env.example .env
python run.py
# http://localhost:8000/docs
```

**Streamlit (Dashboard):** - EM DESENVOLVIMENTO
```bash
cd python-streamlit
pip install -r requirements.txt
streamlit run app.py
# http://localhost:8501
```

---

## 📁 Estrutura Atual

```
├── strava-spring/          ← Backend Java
│   ├── src/main/java/...
│   └── pom.xml
├── python-fastapi/         ← Insights (✅ Pronto!)
│   ├── app.py (354 lines)
│   ├── requirements.txt
│   └── test_api.py
├── python-streamlit/       ← Dashboard (Em desenvolvimento)
│   ├── app.py
│   └── pages/
└── docs/                   ← Documentação
```

---

## 🧠 Insights Inteligentes

### 1. Análise por Condição
- ❄️ COLD (< 5°C)
- 🌤️ COOL (5-15°C)
- 😍 IDEAL (15-22°C)
- 🌞 WARM (22-28°C)
- 🔥 HOT (> 28°C)

### 2. Análise por Temperatura
5 ranges detalhados com estatísticas

### 3. Impacto do Vento
Percentual de redução de pace

### 4. Melhores Condições
Identifica automaticamente

---

## 🛠️ Stack

| Componente | Tecnologia | Versão |
|-----------|-----------|--------|
| Backend | Java + Spring Boot | 21 + 3.2 |
| API | FastAPI + Uvicorn | 0.104 + 0.24 |
| Dashboard | Streamlit | Latest |
| Clima | OpenWeather Free | - |

---

## 📚 Documentação

- [SETUP.md](./SETUP.md) - Guia de instalação
- [ARCHITECTURE.md](./ARCHITECTURE.md) - Arquitetura técnica
- [ROADMAP.md](./ROADMAP.md) - Planejamento
- [python-fastapi/INSIGHTS.md](./python-fastapi/INSIGHTS.md) - Algoritmos
- [EXECUTION_PLAN.md](./EXECUTION_PLAN.md) - Plano de execução (Opção 4)

---

## 🆓 100% Gratuito

- FastAPI (open-source)
- Python & Java (livres)
- OpenWeather Free API
- Streamlit (gratuito)
- Docker (grátis)

**Custo: R$ 0,00** 🎉

---

## ✅ Checklist Status

### FastAPI ✅
- [x] Classe StravaInsights
- [x] 4 endpoints funcionais
- [x] Análises inteligentes
- [x] Documentação técnica
- [x] Testes

### Java Spring ⏳
- [ ] Melhorrias profissionais
- [ ] Logging estruturado
- [ ] Service layer
- [ ] Validação
- [ ] Testes JUnit

### Streamlit ⏳
- [ ] Dashboard visual
- [ ] Gráficos interativos
- [ ] Filtros
- [ ] Exportação PDF

### Estrutura ⏳
- [ ] README global
- [ ] ARCHITECTURE.md
- [ ] SETUP.md
- [ ] ROADMAP.md
- [ ] LICENSE

---

## 📞 Próximas Ações

Você escolheu **OPÇÃO 4 - FAZER TUDO DE UMA VEZ**!

**Em Execução Agora:**
1. Estrutura de Repositório (30 min)
2. Melhorar Java Spring (45 min)
3. Streamlit Dashboard (60 min)
4. Integração & Finalização (15 min)

Tempo total: **150 minutos (2h30min)**

---

## 🔐 Configuração

```bash
cp .env.example .env
# Editar com credenciais Strava e OpenWeather API Key
```

---

## 📖 Links

- [Strava API](https://developers.strava.com/)
- [OpenWeather API](https://openweathermap.org/api)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Spring Boot Docs](https://spring.io/projects/spring-boot)
- [Streamlit Docs](https://docs.streamlit.io/)

---

**Made with ❤️ for runners** 🏃‍♂️

Last updated: November 20, 2025

# 🏃 Strava Connect

![Java](https://img.shields.io/badge/java-21-red)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![Private](https://img.shields.io/badge/repo-private-important)

> **Integração Completa com Análises Inteligentes e Dashboard Visual** ( futuro)

---

## 📋 Visão Geral

O **Strava Connect** é uma solução de ponta a ponta que demonstra a integração completa com a API do Strava, combinando arquitetura híbrida **Java + Python**, análises inteligentes de dados esportivos e visualização interativa em dashboard.

O projeto foi concebido para evidenciar boas práticas de engenharia de software, interoperabilidade entre linguagens, arquitetura orientada a APIs e fundamentos de análise de dados, com forte aderência a cenários reais de mercado.

🔗 **Repositório:** [github.com/rogtavares/strava-connect-java-getavares](https://github.com/rogtavares/strava-connect-java-getavares)

---

## 🏗️ Arquitetura da Solução

A solução adota uma arquitetura híbrida e desacoplada, explorando o melhor de cada stack:

```mermaid
graph TD
    User([👤 Usuário]) -->|Acessa| Frontend[💻 Dashboard Streamlit]
    Frontend -->|Consome| PyAPI[🐍 Camada Analítica (FastAPI)]
    Frontend -->|Consome| JavaAPI[☕ Backend Core (Spring Boot)]
    
    subgraph Backend Services
        JavaAPI -->|OAuth 2.0 / Dados| Strava[☁️ Strava API]
        PyAPI -->|Enriquecimento| Weather[☁️ OpenWeather]
        JavaAPI <-->|Persistência| DB[(🐘 PostgreSQL)]
    end
```

### ☕ Camada Backend – Java (Spring Boot)
- Integração segura com a API oficial do Strava.
- Implementação completa de **OAuth 2.0**.
- Orquestração e normalização dos dados de atividades.
- Exposição de APIs REST para consumo analítico.
- Estrutura preparada para escalabilidade e observabilidade.

### 🐍 Camada Analítica – Python (FastAPI)
- Processamento e enriquecimento dos dados esportivos.
- Cálculo de métricas inteligentes (ritmo, carga, evolução, tendências).
- APIs leves e performáticas para análise sob demanda.

### 📊 Camada de Visualização – Streamlit
- Dashboard interativo e intuitivo.
- Visualização de performance, evolução e padrões de treino.
- Foco em insights acionáveis, não apenas gráficos.

---

## 🧠 Análises Inteligentes

O projeto vai além da simples integração com a API:

- 📊 **Análise de volume e intensidade** de treinos.
- 📈 **Evolução de performance** ao longo do tempo.
- 🧠 **Base preparada para ML/IA:** Detecção de padrões, sugestão de carga e prevenção de overtraining.

---

## 🛠️ Quick Start

### Backend Java
```bash
# Certifique-se de configurar as variáveis de ambiente antes (veja abaixo)
cd strava-spring
mvn spring-boot:run
# 📡 API rodando em: http://localhost:8081
```
```

### API FastAPI
```bash
cd python-fastapi
pip install -r requirements.txt
python app.py
# ⚡ API Python rodando em: http://localhost:8000
```

---

## 📚 Documentação

**[→ Ver Documentação Completa](./docs/)**

### Principais:
- 📖 [Case Study](./docs/CASE_STUDY.md)
- 🔐 [OAuth 2.0](./docs/OAUTH2/)
- 🔧 [Scripts](./scripts/)

---

## 🏗️ Arquitetura

```
Frontend (Streamlit/Next.js)
        ↓
API Gateway (Spring Boot)
        ↓
Backend (Java/Python/Lambda)
        ↓
Strava API + OpenWeather
```

---

## 🔧 Stack

| Camada | Tecnologia |
|--------|-----------|
| Backend | Java 21, Spring Boot 3.2 |
| APIs | FastAPI, Python 3.11+ |
| Serverless | AWS Lambda |
| Frontend | Streamlit, Next.js 14 |
| Database | PostgreSQL |

---

## 📁 Estrutura

```
📁 strava-spring/        Backend Java
📁 python-fastapi/       API FastAPI
📁 lambda-backend/       AWS Lambda
📁 python-streamlit/     Dashboard
📁 portfolio-site/       Site (Next.js)
📁 docs/                 Documentação
📁 scripts/              Scripts automação
```

---

## 🤝 Colaboradores

- **Rogério Tavares** (Autor)
- **Lucas Pajarita** (Colaborador)

---

---

**Status:** 🟢 Ativo | **Acesso:** 🔒 Privado | **Último Update:** 16/12/2025

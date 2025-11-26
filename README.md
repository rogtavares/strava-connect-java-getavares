# 🏃 Strava Connect - Integração Completa com Análises Inteligentes

![Version](https://img.shields.io/badge/version-1.25.0-blue)
![Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Java](https://img.shields.io/badge/java-21-red)
![FastAPI](https://img.shields.io/badge/fastapi-0.104-green)
![Spring Boot](https://img.shields.io/badge/spring%20boot-3.2-green)
![Streamlit](https://img.shields.io/badge/streamlit-latest-red)

> **Integração completa com API do Strava** | **Análises Inteligentes** | **Dashboard Visual** | **100% Gratuito** 🆓

**Versão:** 1.25.0 | **Projeto criado por:** [Rogério Tavares](https://github.com/rogtavares) | **Ano:** 2025

---

## 🎯 Objetivo

Solução integrada: **OAuth 2.0** → **Atividades Strava** → **Enriquecimento Climático** → **Insights** → **Dashboard**

## 📁 Estrutura

```
strava-spring/      # Java 21 + Spring Boot 3.2
python-fastapi/     # Python + FastAPI
python-streamlit/   # Dashboard Streamlit
portfolio-site/     # Next.js 14
```

## 🚀 Quick Start

```bash
# Backend Java (porta 8081)
cd strava-spring && mvn spring-boot:run

# API FastAPI (porta 8000)
cd python-fastapi && python app.py

# Dashboard (porta 8501)
cd python-streamlit && streamlit run app.py

# Portfolio (porta 3000)
cd portfolio-site && npm install && npm run dev
```


## ⚡ Setup Rápido - Java 21

```bash
# 1. Instalar Java 21
winget install EclipseAdoptium.Temurin.21.JDK

# 2. Instalar Maven
winget install Apache.Maven

# 3. Build
mvn clean package
```

## 🔧 Configuração Strava

1. Acesse: https://www.strava.com/settings/api
2. Crie app e configure variáveis:

```bash
STRAVA_CLIENT_ID=your_client_id
STRAVA_CLIENT_SECRET=your_client_secret
STRAVA_REDIRECT_URI=http://localhost:8081/callback
```

---

## 🔄 Fluxo OAuth 2.0

```bash
# 1. Autorizar
https://www.strava.com/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=REDIRECT_URI&scope=read,activity:read_all

# 2. Trocar código por token
curl -X POST https://www.strava.com/oauth/token \
  -d client_id=YOUR_CLIENT_ID \
  -d client_secret=YOUR_CLIENT_SECRET \
  -d code=AUTHORIZATION_CODE \
  -d grant_type=authorization_code

# 3. Usar token
curl -H "Authorization: Bearer ACCESS_TOKEN" https://www.strava.com/api/v3/athlete
```

## 📚 Documentação

- [Strava API Reference](https://developers.strava.com/docs/reference/)
- [OAuth 2.0 Guide](./OAUTH2_GUIDE.md)
- [Apresentação Markmap](./APRESENTACAO_MARKMAP.md)oard (Streamlit / front-end) e gere insights comparativos (desempenho vs clima).

Use os links e exemplos acima como complemento prático para entender e adaptar o fluxo OAuth para este projeto em Java (backend) e Python (enriquecimento/clima).

versão 1.25.0 - 2025 - Rogério Tavares
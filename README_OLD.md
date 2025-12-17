# 🏃 Strava Connect - Integração Completa com Análises Inteligentes

![Version](https://img.shields.io/badge/version-4.11.25-blue)
![Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Java](https://img.shields.io/badge/java-21-red)
![FastAPI](https://img.shields.io/badge/fastapi-0.104-green)
![Spring Boot](https://img.shields.io/badge/spring%20boot-3.2-green)
![Streamlit](https://img.shields.io/badge/streamlit-latest-red)

> **Integração completa com API do Strava** | **Análises Inteligentes** | **Dashboard Visual** | **100% Gratuito** 🆓

**Versão:** 4.11.25 | **Projeto criado por:** [Rogério Tavares](https://github.com/rogtavares) | **Ano:** 2025

---

## 🎯 Objetivo

Solução integrada: **OAuth 2.0** → **Atividades Strava** → **Enriquecimento Climático** → **Insights** → **Dashboard**

## 📁 Estrutura

```
strava-spring/      # Backend Java 21 + Spring Boot
python-fastapi/     # API Python + FastAPI
python-streamlit/   # Dashboard Streamlit
portfolio-site/     # Site Next.js
```

## 🚀 Quick Start

```bash
# Backend (8081)
cd strava-spring && mvn spring-boot:run

# API (8000)
cd python-fastapi && python app.py

# Dashboard (8501)
cd python-streamlit && streamlit run app.py
```

## 🔧 Setup

```bash
# Java 21 + Maven
winget install EclipseAdoptium.Temurin.21.JDK
winget install Apache.Maven

# Strava API: https://www.strava.com/settings/api
STRAVA_CLIENT_ID=your_id
STRAVA_CLIENT_SECRET=your_secret
STRAVA_REDIRECT_URI=http://localhost:8081/callback
```

## 📚 Documentação

- [Strava API Reference](https://developers.strava.com/docs/reference/)
- [Strava Playground - Testes](https://developers.strava.com/playground/)
- [Perfil Atleta](https://www.strava.com/athletes/3329857)
- [Portfólio AWS - Projetos Cloud](https://rogtavares.github.io/AWS_getavares.github.io/)
- [Portfólio Artes - Gé Tavares](https://rogeriotavares.myportfolio.com/)
- [OAuth 2.0 Guide](./OAUTH2_GUIDE.md)
- [Apresentação Markmap](./APRESENTACAO_MARKMAP.md)

---

**versão 4.11.25 - 2025 - Rogério Tavares**
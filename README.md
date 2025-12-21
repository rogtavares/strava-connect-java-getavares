# 🏃 Strava Connect

![Version](https://img.shields.io/badge/version-1.25.0-blue)
![Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-blue)
![Java](https://img.shields.io/badge/java-21-red)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![Private](https://img.shields.io/badge/repo-private-important)

> 🔐 **Repositório Privado - Case de Estudos**

Integração completa com API do Strava + Análises Inteligentes + Dashboard Visual
Uma arquitetura híbrida demonstrando interoperabilidade entre Java (Spring Boot) e Python (FastAPI/Streamlit).

**Versão:** 1.25.0 | **Autor:** Rogério Tavares | **Data:** 16/12/2025

---

## 🎯 Sobre o Projeto

O **Strava Connect** é uma solução de engenharia de software projetada para ingerir, processar e visualizar dados de performance atlética. O sistema orquestra múltiplos serviços para:

1.  **Ingestão:** Autenticação OAuth 2.0 e coleta de dados via API do Strava.
2.  **Enriquecimento:** Cruzamento de dados de atividades com condições climáticas (OpenWeather).
3.  **Processamento:** Geração de insights e estatísticas agregadas.
4.  **Visualização:** Dashboard interativo para análise de performance.

---

## 🚀 Quick Start

### Backend Java
```bash
# Certifique-se de configurar as variáveis de ambiente antes (veja abaixo)
cd strava-spring
mvn spring-boot:run
# 📡 API rodando em: http://localhost:8080
```

### Dashboard Streamlit
```bash
cd python-streamlit
streamlit run app.py
# Acessa em http://localhost:8501
```

### API FastAPI
```bash
cd python-fastapi
python app.py
# Acessa em http://localhost:8000
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

## 📄 Licença

MIT - Veja [LICENSE](./LICENSE)

---

**Status:** 🟢 Ativo | **Acesso:** 🔒 Privado | **Último Update:** 16/12/2025

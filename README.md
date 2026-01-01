# 🏃 Strava Connect - GE TAVARES

![Java](https://img.shields.io/badge/java-21-red)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![Private](https://img.shields.io/badge/repo-private-important)

> **Conecte-se ao Strava e analise seus treinos de forma inteligente**

---

## 💡 O que é isso?

Um projeto que conecta com sua conta do Strava e transforma seus dados de treino em análises úteis. Combina **Java** para integração segura com a API do Strava e **Python** para análises e visualizações.

Perfeito para quem quer entender melhor sua performance, ver evolução ao longo do tempo e ter insights sobre seus treinos.

🔗 **Repositório:** [github.com/rogtavares/strava-connect-java-getavares](https://github.com/rogtavares/strava-connect-java-getavares)

---

## 🏗️ Como funciona?

O projeto é dividido em 3 partes que trabalham juntas:

### ☕ Backend Java (Spring Boot)
- Faz a conexão segura com o Strava
- Autentica sua conta usando OAuth 2.0
- Busca e organiza seus dados de atividades
- **Novos Endpoints:** Perfil e Detalhes de Atividades

### 🐍 Análises Python (FastAPI)
- Processa os dados dos seus treinos
- Calcula métricas como ritmo médio, evolução e tendências
- Gera insights sobre sua performance e clima (OpenWeather)

### 📊 Dashboard (Streamlit) - Em desenvolvimento
- Interface visual para ver seus dados

---

## 🚀 Como rodar?

### 1. Backend Java (Porta 8080)
```bash
cd strava-spring
mvn spring-boot:run
```
📡 **Endpoints Principais:**
- `http://localhost:8080/authorize` (Login/Autenticação)
- `http://localhost:8080/activities/export` (Lista de Atividades)

### 2. API Python (Porta 8000)
```bash
cd python-fastapi
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```
⚡ **Endpoints Principais:**
- `http://localhost:8000/insights` (Análise Inteligente + Clima)

---

## 🔒 Segurança e Configuração

Este projeto segue boas práticas de segurança. **NUNCA** commite arquivos de tokens ou chaves de API.

### Arquivos Ignorados (.gitignore)
- `strava-spring/strava_tokens.json`: Armazena seus tokens de acesso do Strava.
- `python-fastapi/.env`: Armazena sua chave do OpenWeatherMap.
- `application.properties` (com senhas reais): Use variáveis de ambiente ou configure localmente sem commitar.

### Configuração Local
Para rodar, você precisará configurar suas credenciais localmente:
1. **Java:** Configure `strava.client-id` e `strava.client-secret` no `application.properties` ou via variáveis de ambiente.
2. **Python:** Crie um arquivo `.env` na pasta `python-fastapi` com `OPENWEATHER_API_KEY`.

---

## 📚 Documentação

- 📖 [Case Study completo](./docs/CASE_STUDY.md)
- 🔐 [Como funciona o OAuth 2.0](./docs/OAUTH2/)
- 🔧 [Scripts úteis](./scripts/)

---

## 🔧 Tecnologias

- **Backend:** Java 21 + Spring Boot 3.2
- **Análises:** Python 3.11+ + FastAPI + HTTPX (Async)
- **Dashboard:** Streamlit (em desenvolvimento)

---

## 🤝 Colaboradores

- **Rogério Tavares** (Autor)
- **Lucas Pajarita** (Colaborador)


**Versão Atual:** v26.1 (Janeiro/2026)

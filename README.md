# 🏃 Strava Connect - Python Edition

![Python](https://img.shields.io/badge/python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red)
![AWS Lambda](https://img.shields.io/badge/AWS_Lambda-Serverless-orange)

> **Foco Total em Dados: Coleta, Processamento e Visualização com Python**

---

## 💡 Sobre o Projeto

Este projeto é um laboratório avançado de **Engenharia de Dados e Backend com Python**. 
Migramos de uma arquitetura híbrida para uma solução **100% Python** para maximizar a agilidade na análise de dados e desenvolvimento de funcionalidades.

O objetivo é conectar aos dados do Strava, processar métricas avançadas (como impacto do clima no rendimento) e visualizar tudo em dashboards interativos.

---

## 🏗️ Arquitetura da Solução

O sistema é composto por três pilares principais:

### 1. API de Integração e Inteligência (FastAPI)
Localizado em `/python-fastapi`
- Gerencia a autenticação OAuth 2.0 com o Strava.
- Expõe endpoints RESTful para consumo de dados.
- Realiza o enriquecimento de dados (ex: cruzar treino com dados meteorológicos).

### 2. Processamento Serverless (AWS Lambda)
Localizado em `/lambda-backend`
- Processamento assíncrono de atividades.
- Webhooks para receber notificações de novas atividades do Strava em tempo real.
- Arquitetura escalável e orientada a eventos.

### 3. Visualização Interativa (Streamlit)
Localizado em `/python-streamlit`
- Dashboards interativos para análise de performance.
- Gráficos de evolução, comparação de equipamentos e análise climática.
- Interface amigável para o usuário final.

---

## 🚀 Guia de Início Rápido

### Pré-requisitos
- Python 3.11 ou superior
- Conta no Strava Developers (para obter Client ID e Secret)

### 1. Configurando a API (FastAPI)
```bash
cd python-fastapi
# Crie um ambiente virtual (recomendado)
python -m venv .venv
# Ative o ambiente (Windows)
.venv\Scripts\activate
# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente (.env)
cp .env.example .env
# Edite o arquivo .env com suas credenciais do Strava

# Execute o servidor
uvicorn app:app --reload
```
Acesse a documentação da API em: `http://localhost:8000/docs`

### 2. Executando o Dashboard (Streamlit)
```bash
cd python-streamlit
pip install -r requirements.txt
streamlit run app.py
```

---

## 📂 Estrutura do Projeto

```
/
├── python-fastapi/      # Backend API (FastAPI)
├── python-streamlit/    # Frontend Dashboard (Streamlit)
├── lambda-backend/      # Funções Serverless (AWS Lambda)
├── scripts/             # Scripts utilitários e automação
└── archived/            # Código legado (Java, versões antigas)
```

---

## 🤝 Autor

- **Rogério Tavares**

**Versão Atual:** Python Focus v1.0 (Janeiro/2026)

# 🚴 Strava Insights - Streamlit Dashboard

Dashboard interativo para análise inteligente de atividades de treino com insights sobre temperatura, vento e condições climáticas.

## ✨ Features

### 📈 Dashboard
- 📊 3 KPI Cards (Total de Atividades, Km, Horas)
- 📈 Gráfico de atividades por mês
- 🏃 Velocidade média por tipo de atividade
- 🆕 Atividades recentes
- ✨ Insights gerados automaticamente

### 📊 Analytics
- 🌡️ **Pace vs Temperatura** - Scatter interativo
  - Identifique em qual temperatura você corre melhor
  - Comparação com condições climáticas
  
- 🌤️ **Performance por Condição** - Bar chart
  - Desempenho em dias ensolarados vs chuvosos
  - Comparação com baseline
  
- 💨 **Impacto do Vento** - Quantificação percentual
  - Vento afeta quanto seu tempo?
  - Use para desculpar treinos ruins 😄
  
- 📊 **Tabela Comparativa**
  - Filtros dinâmicos (esporte, data, clima, pace)
  - Ordenação por coluna
  - Download em CSV

### 🚴 Activities
- 📋 **Tabela de Atividades**
  - Busca em tempo real
  - Filtros avançados
  - Ordenação inteligente
  
- 📥 **Exportação**
  - Download CSV
  - Download JSON
  
- 📊 **Estatísticas**
  - Total de atividades
  - Distância total e média
  - Tempo total e médio
  - Tipo de atividade mais comum

## 🚀 Quick Start

### Requisitos
- Python 3.11+
- Spring Boot rodando em `http://localhost:8080`
- FastAPI rodando em `http://localhost:8000`
- Credenciais Strava OAuth 2.0

### Instalação

```bash
# Clone ou navegue até o diretório
cd python-streamlit

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### Configuração

1. **Variáveis de Ambiente** (opcional)
```bash
# Criar arquivo .env
export STRAVA_CLIENT_ID=seu_client_id
export STRAVA_CLIENT_SECRET=seu_client_secret
export STRAVA_REDIRECT_URI=http://localhost:8080/api/authorize/callback
```

2. **Editar config.py**
```python
STRAVA_API_URL = "http://localhost:8080/api"
FASTAPI_URL = "http://localhost:8000"
```

### Execução

```bash
# Iniciar Streamlit
streamlit run app.py

# Abrir em browser
# http://localhost:8501
```

## 📁 Estrutura do Projeto

```
python-streamlit/
├── app.py                          # Main entry point
├── config.py                       # Configurações centralizadas
├── requirements.txt                # Dependências Python
├── README.md                       # Este arquivo
├── pages/
│   ├── 1_📈_Dashboard.py           # Dashboard com métricas
│   ├── 2_📊_Analytics.py           # Análise detalhada
│   └── 3_🚴_Activities.py          # Lista de atividades
└── modules/
    ├── api_client.py               # Cliente HTTP para APIs
    ├── charts.py                   # Gráficos Plotly
    └── filters.py                  # Widgets de filtro
```

## 🔌 Integração com APIs

### Spring Boot (Porta 8080)
```
GET /api/authorize                  - Iniciar OAuth flow
GET /api/authorize/callback         - Callback OAuth
GET /api/activities/export          - Listar atividades
```

### FastAPI (Porta 8000)
```
GET /                               - Health check
POST /enrich                        - Enriquecer atividades com weather
POST /insights                      - Gerar insights inteligentes
```

## 📊 Flow de Dados

```
1. Usuario clica "Conectar Strava"
   ↓
2. Redirecionado para Spring OAuth
   ↓
3. Token salvo em session_state
   ↓
4. Buscar atividades via Spring
   ↓
5. Enriquecer com weather via FastAPI
   ↓
6. Gerar insights via FastAPI
   ↓
7. Exibir no Dashboard
```

## 🎨 Customização

### Cores e Tema
Edite `config.py`:
```python
COLORS = {
    "primary": "#1f77b4",
    "success": "#2ca02c",
    "danger": "#d62728",
    ...
}
```

### Tipos de Esportes
Modifique `ACTIVITY_TYPES` em `config.py`:
```python
ACTIVITY_TYPES = ["Run", "Ride", "Swim", "Walk", ...]
```

### Condições Climáticas
Customize `WEATHER_CONDITIONS`:
```python
WEATHER_CONDITIONS = ["sunny", "cloudy", "rainy", ...]
```

## ⚠️ Requisitos de API

### Strava OAuth 2.0
- Aplicação registrada em developers.strava.com
- Client ID e Client Secret configurados
- Redirect URI configurado

### OpenWeather API
- Free tier gratuita
- Não requer rate limiting para dados históricos
- Configurado automaticamente via FastAPI

## 🐳 Docker

```bash
# Build
docker build -t strava-streamlit .

# Run
docker run -p 8501:8501 \
  -e STRAVA_API_URL=http://spring:8080/api \
  -e FASTAPI_URL=http://fastapi:8000 \
  strava-streamlit
```

## 🔧 Troubleshooting

### "Spring Boot não está rodando"
- Verifique se Spring está rodando em http://localhost:8080
- Teste com `curl http://localhost:8080/api/health`

### "FastAPI não está rodando"
- Verifique se FastAPI está rodando em http://localhost:8000
- Teste com `curl http://localhost:8000/health`

### "Erro ao autenticar com Strava"
- Verifique Client ID/Secret
- Confirme Redirect URI
- Teste OAuth flow em browser direto

### "Nenhuma atividade encontrada"
- Certifique-se de estar autenticado
- Clique "Sincronizar Atividades" no Dashboard
- Confirme que tem atividades no Strava

## 📈 Próximos Passos

- [ ] Autenticação persistente entre sessões
- [ ] Cache de dados (Redis)
- [ ] Predict ions com ML
- [ ] Mapas com rotas (Folium)
- [ ] Competições entre amigos
- [ ] Integração com Garmin
- [ ] App mobile (React Native)

## 📚 Documentação

- [Streamlit Docs](https://docs.streamlit.io)
- [Plotly Docs](https://plotly.com/python)
- [Pandas Docs](https://pandas.pydata.org)
- [Strava API Docs](https://developers.strava.com)

## 📄 Licença

MIT License - veja LICENSE para detalhes

## 🤝 Contribuição

Veja [CONTRIBUTING.md](../CONTRIBUTING.md)

## 💬 Suporte

- [GitHub Issues](https://github.com/getavares/strava-connect-java-getavares/issues)
- [Strava Developers Community](https://developers.strava.com)

---

Made with ❤️ | 2025

# 📖 SETUP.md - Guia de Instalação

**Tempo estimado:** 15 minutos  
**Dificuldade:** Fácil ⭐  
**Data:** 20 de novembro de 2025

---

## 📋 Pré-requisitos

### Software Necessário

- **Java 21 LTS** (para Spring)
- **Python 3.11+** (para FastAPI/Streamlit)
- **Git** (para clonar repositório)
- **Docker & Docker Compose** (opcional, mas recomendado)

### Credenciais Necessárias

1. **Strava API Credentials** - Grátis em https://www.strava.com/settings/apps
2. **OpenWeather API Key** - Grátis em https://openweathermap.org/api

---

## 🔑 Passo 1: Obter Credenciais

### Strava OAuth

1. Acesse https://www.strava.com/settings/apps
2. Clique em "Create & Manage Your App"
3. Preencha os dados:
   - **App Name:** Strava Connect
   - **Category:** Training
   - **Website:** http://localhost
   - **Authorization Callback Domain:** localhost

4. Copie:
   - `STRAVA_CLIENT_ID`
   - `STRAVA_CLIENT_SECRET`

### OpenWeather API

1. Acesse https://openweathermap.org/api
2. Clique em "Sign Up" (grátis)
3. Vá para "API Keys" no painel
4. Copie sua API key (`OPENWEATHER_API_KEY`)

---

## 🚀 Passo 2: Clonar e Configurar

### Terminal / PowerShell

```bash
# Clonar repositório
git clone https://github.com/rogtavares/strava-connect-java-getavares.git
cd strava-connect-java-getavares

# Copiar arquivo de configuração
cp .env.example .env

# Editar .env com suas credenciais
# Windows: notepad .env
# Mac/Linux: nano .env
```

### Editar .env

```ini
# Strava OAuth
STRAVA_CLIENT_ID=seu_client_id_aqui
STRAVA_CLIENT_SECRET=seu_client_secret_aqui
STRAVA_REDIRECT_URI=http://localhost:8080/callback

# OpenWeather API
OPENWEATHER_API_KEY=sua_openweather_key_aqui

# Backend URLs
BACKEND_URL=http://localhost:8080

# FastAPI Server
FASTAPI_HOST=127.0.0.1
FASTAPI_PORT=8000
```

---

## 🐳 OPÇÃO A: Com Docker (Recomendado)

### Pré-requisitos

- Docker Desktop instalado
- 4GB RAM disponível

### Executar

```bash
# Na raiz do projeto
docker-compose up --build

# Aguardar ~1 minuto

# Acessar:
# Java Spring: http://localhost:8080
# FastAPI: http://localhost:8000/docs
# Streamlit: http://localhost:8501
```

### Parar Serviços

```bash
docker-compose down
```

---

## 💻 OPÇÃO B: Localmente

### Java Spring Backend (Port 8080)

```bash
# Ir para pasta
cd strava-spring

# Verificar Java
java -version  # Deve ser 21+

# Build
mvn clean install

# Executar
mvn spring-boot:run

# Ou com IDE
# IntelliJ: Clique em StravaSpringApplication.java → Run
# VS Code: Com extension Java Language Support, clique Run
```

**Testes:**
```bash
curl http://localhost:8080/authorize
```

### FastAPI (Port 8000)

```bash
# Ir para pasta
cd python-fastapi

# Criar virtual environment
python -m venv venv

# Ativar
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar
python run.py

# Ou
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

**Testes:**
```bash
curl http://localhost:8000/docs
```

### Streamlit Dashboard (Port 8501)

```bash
# Ir para pasta
cd python-streamlit

# Criar virtual environment
python -m venv venv

# Ativar
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar
streamlit run app.py

# Automaticamente abre: http://localhost:8501
```

---

## ✅ Verificação

### 1. Java Spring
```bash
curl http://localhost:8080/authorize
# Deve retornar HTML com link de autorização
```

### 2. FastAPI
```bash
curl http://localhost:8000/health
# Deve retornar: {"status": "healthy"}
```

### 3. Streamlit
```bash
# Acesse http://localhost:8501 no navegador
# Deve carregar a página inicial
```

---

## 🔐 Fluxo de Autenticação

### Passo a Passo

1. Acesse http://localhost:8080/authorize
2. Clique no link "Authorize with Strava"
3. Você será redirecionado para Strava
4. Clique em "Authorize"
5. Será redirecionado de volta para http://localhost:8080/callback
6. Verá mensagem de sucesso
7. Agora pode acessar /activities/export

### Se der erro

- Verifique se STRAVA_REDIRECT_URI está correto em .env
- Certifique-se de que está usando domínio exato em Strava Settings
- Limpe cookies do navegador

---

## 🧪 Testando Endpoints

### FastAPI - GET /insights

```bash
curl http://localhost:8000/insights
```

Resposta esperada:
```json
{
  "summary": [...],
  "performance_by_condition": {...},
  "best_conditions": {...},
  ...
}
```

### FastAPI - GET /enrich

```bash
curl http://localhost:8000/enrich
```

Retorna atividades + dados de clima

### Java Spring - GET /activities/export

```bash
curl http://localhost:8080/activities/export
```

Retorna atividades em JSON

---

## 🐛 Troubleshooting

### Problema: "Connection refused" na port 8080

**Solução:**
```bash
# Verificar se Java está rodando
jps
# Deve listar StravaSpringApplication

# Se não estiver, reiniciar:
cd strava-spring
mvn spring-boot:run
```

### Problema: Python: "ModuleNotFoundError"

**Solução:**
```bash
# Verificar venv ativado
which python  # Mac/Linux
where python  # Windows

# Se não estiver:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Reinstalar dependências
pip install -r requirements.txt
```

### Problema: Strava OAuth "invalid redirect_uri"

**Solução:**
1. Verifique em .env: STRAVA_REDIRECT_URI=http://localhost:8080/callback
2. Acesse https://www.strava.com/settings/apps
3. Certifique-se que "Authorization Callback Domain" é: localhost
4. Salve e tente novamente

### Problema: OpenWeather retorna erro 401

**Solução:**
1. Verifique se API Key está correta em .env
2. Registre-se novamente em https://openweathermap.org/api
3. Aguarde alguns minutos para ativar
4. Teste: curl "https://api.openweathermap.org/data/2.5/weather?lat=0&lon=0&appid=SUA_KEY"

### Problema: Docker: "port already in use"

**Solução:**
```bash
# Verificar portas
netstat -ano  # Windows
lsof -i :8080 # Mac/Linux

# Parar container
docker-compose down

# Ou alterar em docker-compose.yml:
# 8080:8080 → 8081:8080 (mude primeira porta)
```

---

## 📝 Variáveis de Ambiente Completas

```ini
# ===== STRAVA OAUTH =====
STRAVA_CLIENT_ID=123456789
STRAVA_CLIENT_SECRET=abc123xyz789
STRAVA_REDIRECT_URI=http://localhost:8080/callback

# ===== OPENWEATHER API =====
OPENWEATHER_API_KEY=sua_api_key_gratis_aqui

# ===== BACKEND URLs =====
BACKEND_URL=http://localhost:8080

# ===== FASTAPI SERVER =====
FASTAPI_HOST=127.0.0.1
FASTAPI_PORT=8000

# ===== STREAMLIT (OPCIONAL) =====
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
```

---

## 🎯 Checklist Final

- [ ] Java 21+ instalado: `java -version`
- [ ] Python 3.11+ instalado: `python --version`
- [ ] Git instalado: `git --version`
- [ ] Strava Client ID obtido
- [ ] Strava Client Secret obtido
- [ ] OpenWeather API Key obtida
- [ ] .env criado e preenchido
- [ ] Java Spring rodando na porta 8080
- [ ] FastAPI rodando na port 8000
- [ ] Streamlit rodando na port 8501
- [ ] OAuth flow testado com sucesso
- [ ] /activities/export retorna atividades
- [ ] /insights retorna análises

---

## 🚀 Próximos Passos

1. **Autenticar:** Acesse http://localhost:8080/authorize
2. **Testar FastAPI:** http://localhost:8000/docs
3. **Visualizar Dashboard:** http://localhost:8501
4. **Explorar dados:** Veja seus insights no dashboard!

---

## 📞 Precisa de Ajuda?

- 📖 Verifique [TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)
- 🐛 Abra uma issue no GitHub
- 💬 Verifique [FAQ.md](./docs/FAQ.md)

---

**Criado:** 20 de novembro de 2025  
**Última atualização:** 20 de novembro de 2025  
**Status:** ✅ Tested and Ready

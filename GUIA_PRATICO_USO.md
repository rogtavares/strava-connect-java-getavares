# 🚀 Guia Prático - Como Usar Cada Componente

> **Guia hands-on para rodar todos os componentes do projeto na prática**

---

## 📋 Pré-requisitos

### Instalar:
- ✅ **Java 21** (JDK)
- ✅ **Maven 3.8+**
- ✅ **Python 3.11+**
- ✅ **Node.js 18+**
- ✅ **Git**

### Configurar Variáveis de Ambiente:
```bash
# Windows (PowerShell)
$env:STRAVA_CLIENT_ID="seu_client_id"
$env:STRAVA_CLIENT_SECRET="seu_client_secret"
$env:STRAVA_REDIRECT_URI="http://localhost:8080/callback"

# Linux/Mac
export STRAVA_CLIENT_ID="seu_client_id"
export STRAVA_CLIENT_SECRET="seu_client_secret"
export STRAVA_REDIRECT_URI="http://localhost:8080/callback"
```

---

## 1️⃣ Backend Java (Spring Boot)

### 📍 Localização: `strava-spring/`

### 🚀 Como Rodar:

```bash
# Navegar para o diretório
cd strava-spring

# Compilar o projeto
mvn clean install

# Rodar a aplicação
mvn spring-boot:run
```

### 🌐 Acessar:
```
http://localhost:8080
```

### 📌 Endpoints Disponíveis:

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/auth` | GET | Inicia fluxo OAuth |
| `/callback` | GET | Recebe código de autorização |
| `/athlete` | GET | Dados do atleta |
| `/activities` | GET | Lista atividades |

### 🧪 Testar:
```bash
# 1. Abrir no navegador
http://localhost:8080/auth

# 2. Autorizar no Strava

# 3. Testar endpoint
curl http://localhost:8080/athlete
```

### 🛑 Parar:
```
Ctrl + C
```

---

## 2️⃣ API FastAPI (Python)

### 📍 Localização: `python-fastapi/`

### 🚀 Como Rodar:

```bash
# Navegar para o diretório
cd python-fastapi

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Rodar a aplicação
python app.py
```

### 🌐 Acessar:
```
http://localhost:8000
http://localhost:8000/docs  # Swagger UI
```

### 📌 Endpoints Disponíveis:

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/` | GET | Health check |
| `/auth/authorize` | GET | Inicia OAuth |
| `/auth/callback` | GET | Callback OAuth |
| `/activities` | GET | Lista atividades |
| `/activities/{id}` | GET | Detalhes atividade |
| `/weather/{lat}/{lon}` | GET | Dados climáticos |

### 🧪 Testar:
```bash
# Health check
curl http://localhost:8000

# Ver documentação interativa
# Abrir no navegador: http://localhost:8000/docs
```

### 🛑 Parar:
```
Ctrl + C
deactivate  # Desativar venv
```

---

## 3️⃣ Dashboard Streamlit (Python)

### 📍 Localização: `python-streamlit/`

### 🚀 Como Rodar:

```bash
# Navegar para o diretório
cd python-streamlit

# Criar ambiente virtual (se não criou)
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Rodar o dashboard
streamlit run app.py
```

### 🌐 Acessar:
```
http://localhost:8501
```

### 📊 Funcionalidades:
- ✅ Login com Strava
- ✅ Visualização de atividades
- ✅ Gráficos de desempenho
- ✅ Análise de clima vs treino
- ✅ Estatísticas personalizadas

### 🛑 Parar:
```
Ctrl + C
deactivate
```

---

## 4️⃣ Site Portfólio (Next.js)

### 📍 Localização: `portfolio-site/`

### 🚀 Como Rodar:

```bash
# Navegar para o diretório
cd portfolio-site

# Instalar dependências
npm install

# Rodar em desenvolvimento
npm run dev
```

### 🌐 Acessar:
```
http://localhost:3000
```

### 📦 Build para Produção:
```bash
# Build
npm run build

# Export para GitHub Pages
npm run export
```

### 🛑 Parar:
```
Ctrl + C
```

---

## 5️⃣ Backend Serverless (AWS Lambda)

### 📍 Localização: `lambda-backend/`

### 🚀 Como Rodar Localmente:

```bash
# Navegar para o diretório
cd lambda-backend

# Instalar dependências
pip install -r requirements.txt

# Rodar testes locais
python test_local.py
```

### ☁️ Deploy AWS:
```bash
# Instalar Serverless Framework
npm install -g serverless

# Configurar AWS credentials
aws configure

# Deploy
serverless deploy
```

---

## 🔄 Fluxo Completo de Uso

### Cenário 1: Desenvolvimento Local Completo

```bash
# Terminal 1 - Backend Java
cd strava-spring
mvn spring-boot:run

# Terminal 2 - API FastAPI
cd python-fastapi
python app.py

# Terminal 3 - Dashboard Streamlit
cd python-streamlit
streamlit run app.py

# Terminal 4 - Site Portfólio
cd portfolio-site
npm run dev
```

### Acessar:
- **Backend Java:** http://localhost:8080
- **API FastAPI:** http://localhost:8000
- **Dashboard:** http://localhost:8501
- **Portfólio:** http://localhost:3000

---

## 🧪 Testes Práticos

### Teste 1: Fluxo OAuth Completo
```bash
# 1. Iniciar backend Java
cd strava-spring && mvn spring-boot:run

# 2. Abrir navegador
http://localhost:8080/auth

# 3. Autorizar no Strava

# 4. Ver dados retornados
```

### Teste 2: API FastAPI + Swagger
```bash
# 1. Iniciar FastAPI
cd python-fastapi && python app.py

# 2. Abrir Swagger UI
http://localhost:8000/docs

# 3. Testar endpoints interativamente
```

### Teste 3: Dashboard Completo
```bash
# 1. Iniciar Streamlit
cd python-streamlit && streamlit run app.py

# 2. Fazer login com Strava

# 3. Explorar visualizações
```

---

## 🐛 Troubleshooting

### Erro: "Port already in use"
```bash
# Windows - Matar processo na porta
netstat -ano | findstr :8080
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8080 | xargs kill -9
```

### Erro: "Module not found"
```bash
# Python
pip install -r requirements.txt

# Node.js
npm install
```

### Erro: "JAVA_HOME not set"
```bash
# Windows
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-21.0.x"

# Linux/Mac
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk
```

---

## 📊 Monitoramento

### Logs em Tempo Real:

```bash
# Java Spring Boot
tail -f logs/spring-boot-app.log

# FastAPI
# Logs aparecem no terminal

# Streamlit
# Logs aparecem no terminal
```

---

## 🚀 Próximos Passos

1. ✅ Rodar cada componente individualmente
2. ✅ Testar fluxo OAuth completo
3. ✅ Integrar componentes
4. ✅ Adicionar funcionalidades
5. ✅ Deploy em produção

---

## 📚 Documentação Adicional

- **OAuth 2.0:** `OAUTH2_GUIDE.md`
- **Arquitetura:** `ARCHITECTURE.md`
- **Setup:** `SETUP.md`
- **Roadmap:** `ROADMAP.md`

---

**Criado por:** Rogério Tavares | **Data:** 2025 | **Versão:** 1.25.0
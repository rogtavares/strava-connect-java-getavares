# ⚡ Quick Start - Guia Rápido

## 🎯 Status Atual do Projeto

### ✅ Componentes Disponíveis:
1. **Backend Java (Spring Boot)** - `strava-spring/` ⚠️ (precisa correção)
2. **API Python (FastAPI)** - `python-fastapi/` ✅
3. **Dashboard (Streamlit)** - `python-streamlit/` ✅
4. **Backend Serverless (Lambda)** - `lambda-backend/` ✅
5. **Site Portfólio (Next.js)** - `portfolio-site/` ✅

---

## 🚀 Como Rodar Cada Componente

### 1️⃣ API FastAPI (Recomendado para começar)

```bash
cd python-fastapi
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
**Acesse:** http://localhost:8000/docs

---

### 2️⃣ Dashboard Streamlit

```bash
cd python-streamlit
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
**Acesse:** http://localhost:8501

---

### 3️⃣ Site Portfólio

```bash
cd portfolio-site
npm install
npm run dev
```
**Acesse:** http://localhost:3000

---

### 4️⃣ Backend Java (Spring Boot)

⚠️ **Atenção:** Há erros de compilação que precisam ser corrigidos primeiro.

**Erro atual:** Classes duplicadas em `exception/`

**Solução:**
1. Remover arquivo `CustomExceptions.java`
2. Manter classes separadas em arquivos individuais

```bash
cd strava-spring
mvn clean install -DskipTests
mvn spring-boot:run
```

---

## 📝 Configuração Necessária

### Variáveis de Ambiente:

```bash
# Windows PowerShell
$env:STRAVA_CLIENT_ID="seu_client_id"
$env:STRAVA_CLIENT_SECRET="seu_client_secret"
$env:STRAVA_REDIRECT_URI="http://localhost:8080/callback"
```

### Obter Credenciais Strava:
1. Acesse: https://www.strava.com/settings/api
2. Crie um aplicativo
3. Copie Client ID e Client Secret

---

## 🧪 Teste Rápido

### Teste 1: Verificar se FastAPI está funcionando
```bash
curl http://localhost:8000
```

### Teste 2: Ver documentação interativa
Abra no navegador: http://localhost:8000/docs

### Teste 3: Testar OAuth
1. Inicie FastAPI
2. Acesse: http://localhost:8000/auth/authorize
3. Autorize no Strava
4. Veja os dados retornados

---

## 📚 Documentação Completa

- **Guia Prático Completo:** `GUIA_PRATICO_USO.md`
- **OAuth 2.0:** `OAUTH2_GUIDE.md`
- **Arquitetura:** `ARCHITECTURE.md`
- **Setup:** `SETUP.md`

---

## 🐛 Problemas Comuns

### Porta já em uso:
```bash
# Matar processo
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Módulo não encontrado:
```bash
pip install -r requirements.txt
```

### Java não encontrado:
```bash
# Verificar instalação
java -version
```

---

**Criado por:** Rogério Tavares | **Versão:** 1.25.0
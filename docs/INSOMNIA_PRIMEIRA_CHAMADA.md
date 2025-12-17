# 🚀 Guia Completo: Primeira Chamada API (Insomnia)

## 📋 Passo 0: Preparação (Antes de Tudo!)

### ✅ Verificar Pré-requisitos
- ✅ Insomnia instalado? (`choco install insomnia-rest-api-client`)
- ✅ Java 21+ instalado? (`java -version`)
- ✅ Python 3.11+ instalado? (`python --version`)
- ✅ Maven instalado? (`mvn -version`)

---

## 🎯 Passo 1: Importar Coleção no Insomnia

### 1.1 Abrir Insomnia
- Clique em iniciar Insomnia (desktop app)

### 1.2 Importar
1. Clique no menu **"Create"** (ou **"+"**)
2. Selecione **"Import From"**
3. Escolha **"File"**
4. Navegue até:
   ```
   c:\Users\Cliente\Desktop\JAVA\strava-connect-java-getavares\
   insomnia-collection.json
   ```
5. Clique em **"Import"**

### 1.3 Verificar
Você verá na tela:
```
📁 Strava Connect - Case de Estudos
│
├── 1️⃣ Backend Spring Boot (8080)
│   ├── GET / - Home
│   ├── GET /authorize - Iniciar OAuth
│   ├── GET /callback - Receber Token
│   ├── GET /activities/export
│   └── GET /stats
│
├── 2️⃣ API FastAPI (8000)
│   ├── ℹ️ Info
│   ├── 💚 Health Check
│   ├── 🌡️ Enrich Activities
│   └── 🧠 AI Insights
│
├── 3️⃣ Dashboard Streamlit (8501)
│
└── 🔄 Fluxo Completo (Sequencial)
```

✅ **Coleção importada com sucesso!**

---

## 🚀 Passo 2: Iniciar Backends

Abra **3 terminais** para rodar os backends em paralelo:

### Terminal 1: Spring Boot (Porta 8080)
```powershell
cd "c:\Users\Cliente\Desktop\JAVA\strava-connect-java-getavares\strava-spring"
mvn spring-boot:run
```

**Espere até ver:**
```
Tomcat started on port(s): 8080
```

### Terminal 2: FastAPI (Porta 8000)
```powershell
cd "c:\Users\Cliente\Desktop\JAVA\strava-connect-java-getavares\python-fastapi"
python app.py
```

**Espere até ver:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 3: Streamlit (Porta 8501) [OPCIONAL]
```powershell
cd "c:\Users\Cliente\Desktop\JAVA\strava-connect-java-getavares\python-streamlit"
streamlit run app.py
```

**Espere até ver:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

---

## 🔧 Passo 3: Testar Primeira Chamada

### 3.1 Teste Simples (Recomendado para Começar)

**No Insomnia**, vá para:
```
1️⃣ Backend Spring Boot (8080) 
  → GET / - Home
```

**Clique em "Send"** (ou `Ctrl + Enter`)

### ✅ Resultado Esperado:
```json
{
  "status": "Strava API is running!"
}
```

---

## 🎯 Passo 4: Testar Segundo Endpoint (FastAPI Health)

**No Insomnia**, vá para:
```
2️⃣ API FastAPI (8000)
  → 💚 Health Check
```

**Clique em "Send"**

### ✅ Resultado Esperado:
```json
{
  "status": "healthy"
}
```

---

## 🔐 Passo 5: Autenticação OAuth 2.0 (Completo)

### 5.1 Obter Link de Autorização

**No Insomnia**, vá para:
```
1️⃣ Backend Spring Boot (8080)
  → GET /authorize - Iniciar OAuth
```

**Clique em "Send"**

### ✅ Resultado:
```html
<a href="https://www.strava.com/oauth/authorize?client_id=...&...">
  Clique aqui para autorizar com Strava
</a>
```

---

### 5.2 Abrir Link no Navegador

1. **Copie** o link da resposta
2. **Abra** em um novo navegador
3. **Clique** em "Authorize Application"
4. **Você será redirecionado** para um callback com um código

---

### 5.3 Obter Código da URL

Na URL de retorno, você verá algo como:
```
http://localhost:8080/callback?code=ABCD1234EFGH5678&scope=...
```

**Copie** o valor de `code` (ex: `ABCD1234EFGH5678`)

---

### 5.4 Fazer Callback

**No Insomnia**, vá para:
```
1️⃣ Backend Spring Boot (8080)
  → GET /callback - Receber Token
```

**Edite a URL:**
```
http://localhost:8080/callback?code=ABCD1234EFGH5678
```

(Substitua `ABCD1234EFGH5678` pelo código que você copiou)

**Clique em "Send"**

### ✅ Resultado:
```json
{
  "message": "Token recebido com sucesso!",
  "access_token": "seu_token_aqui...",
  "athlete": {
    "id": 12345,
    "firstname": "Seu Nome",
    "profile": "https://..."
  }
}
```

✅ **Agora você tem um token válido!**

---

## 📊 Passo 6: Buscar Atividades

### 6.1 Atividades Básicas (Spring Boot)

**No Insomnia**, vá para:
```
1️⃣ Backend Spring Boot (8080)
  → GET /activities/export
```

**Clique em "Send"**

### ✅ Resultado:
```json
{
  "activities": [
    {
      "id": 123456789,
      "name": "Corrida matinal",
      "distance": 5.42,
      "moving_time": 1860,
      "type": "Run"
    },
    ...
  ]
}
```

---

### 6.2 Atividades Enriquecidas (com Clima)

**No Insomnia**, vá para:
```
2️⃣ API FastAPI (8000)
  → 🌡️ Enrich Activities
```

**Clique em "Send"**

### ✅ Resultado:
```json
{
  "activities": [
    {
      "id": 123456789,
      "name": "Corrida matinal",
      "distance": 5.42,
      "weather": {
        "temperature": 22.5,
        "humidity": 65,
        "wind_speed": 3.2,
        "condition": "Partly Cloudy"
      }
    },
    ...
  ]
}
```

---

### 6.3 Insights Inteligentes

**No Insomnia**, vá para:
```
2️⃣ API FastAPI (8000)
  → 🧠 AI Insights
```

**Clique em "Send"**

### ✅ Resultado:
```json
{
  "insights": [
    {
      "activity_id": 123456789,
      "summary": "Excelente sessão em condições quentes",
      "performance": "8.5/10",
      "weather_impact": "Calor reduziu performance em 12%",
      "recommendation": "Aumentar hidratação em dias quentes"
    },
    ...
  ]
}
```

---

## 🎯 Fluxo Completo em Sequência

Se você quiser testar **tudo na ordem correta**, use a pasta:
```
🔄 Fluxo Completo (Sequencial)
```

Execute os passos **na ordem**:
1. ✅ Verificar Backends
2. ✅ Obter Link OAuth
3. ✅ Fazer Callback com Código
4. ✅ Buscar Atividades
5. ✅ Enriquecer com Clima
6. ✅ Gerar Insights

---

## 🔧 Dicas Pro

### 💡 Usar Variáveis de Ambiente

1. No Insomnia, clique no **dropdown de environments** (canto superior esquerdo)
2. Selecione **"Base Environment"**
3. As URLs já estarão usando:
   - `{{ _.backend_url }}` → `http://localhost:8080`
   - `{{ _.fastapi_url }}` → `http://localhost:8000`
   - `{{ _.streamlit_url }}` → `http://localhost:8501`

Isso facilita trocar entre **dev** e **prod** depois!

---

### 🖥️ Ver Respostas Anteriores

1. Clique no **ícone de relógio** ⏰ na resposta
2. Você verá o **histórico completo** de respostas anteriores

---

### 💾 Salvar Requisição Personalizada

Se fizer mudanças, clique em **Ctrl + S** para salvar

---

### 🔗 Encadear Requisições

Para usar a resposta de uma requisição em outra:

1. Clique em **"Send Request"** (menu direito)
2. Configure para executar automaticamente depois

---

## 🐛 Troubleshooting

### Erro: "Connection refused"
```
❌ Problema: Backend não está rodando
✅ Solução: Verifique os 3 terminais acima
```

### Erro: "no_token"
```
❌ Problema: Token expirou ou não foi obtido
✅ Solução: Refaça o fluxo OAuth (passos 5.1 a 5.4)
```

### Erro: "404 Not Found"
```
❌ Problema: Endpoint não existe
✅ Solução: Verifique a URL na requisição
```

### Erro: "CORS Error"
```
❌ Problema: Configuração de CORS faltando
✅ Solução: Verifique application.properties (Spring Boot)
```

---

## ✅ Checklist de Sucesso

- [ ] Insomnia instalado
- [ ] Coleção importada
- [ ] 3 terminais com backends rodando
- [ ] GET / retorna status 200
- [ ] GET /health retorna status 200
- [ ] OAuth 2.0 concluído com token
- [ ] GET /activities/export retorna atividades
- [ ] GET /enrich retorna dados com clima
- [ ] GET /insights retorna análises

✅ **Se todos marcados = SUCESSO!** 🎉

---

## 📚 Documentação Completa

- **[INSOMNIA_SETUP.md](./INSOMNIA_SETUP.md)** - Referência técnica
- **[INSOMNIA_QUICK_START.md](./INSOMNIA_QUICK_START.md)** - Resumo rápido

---

**Versão:** 1.25.0  
**Última Atualização:** 16/12/2025  
**Status:** ✅ Pronto para usar!

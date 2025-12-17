# 🔧 Configuração do Insomnia - Strava Connect

## 📥 Importar Coleção

1. Abra o Insomnia
2. Clique em **Create** → **Import From** → **File**
3. Selecione o arquivo `insomnia-collection.json` (na raiz do projeto)
4. Pronto! Todos os endpoints estarão configurados

---

## 🎯 Endpoints Disponíveis

### 1️⃣ Backend Spring Boot (porta 8080)

#### **GET /** - Home
- URL: `http://localhost:8080/`
- Descrição: Verifica se o backend está rodando

#### **GET /authorize** - Iniciar OAuth
- URL: `http://localhost:8080/authorize`
- Descrição: Retorna link para autorizar com Strava
- Ação: Copie o link e abra no navegador

#### **GET /callback** - Callback OAuth
- URL: `http://localhost:8080/callback?code=SEU_CODIGO_AQUI`
- Descrição: Recebe código de autorização e troca por token
- Parâmetro: `code` (obtido após autorizar no Strava)

#### **GET /activities/export** - Exportar Atividades
- URL: `http://localhost:8080/activities/export`
- Descrição: Retorna suas atividades do Strava
- Requer: Token válido (obtido no callback)

---

### 2️⃣ API FastAPI (porta 8000)

#### **GET /** - Info da API
- URL: `http://localhost:8000/`
- Descrição: Informações sobre a API de insights

#### **GET /health** - Health Check
- URL: `http://localhost:8000/health`
- Descrição: Verifica se a API está saudável

#### **GET /enrich** - Atividades Enriquecidas
- URL: `http://localhost:8000/enrich`
- Descrição: Retorna atividades com dados climáticos
- Requer: Backend Spring rodando + Token válido

#### **GET /insights** - Insights Inteligentes
- URL: `http://localhost:8000/insights`
- Descrição: Análises de performance baseadas no clima
- Requer: Backend Spring rodando + Token válido

---

### 3️⃣ Dashboard Streamlit (porta 8501)

#### **GET /** - Dashboard
- URL: `http://localhost:8501/`
- Descrição: Interface visual do dashboard
- Nota: Abrir no navegador, não no Insomnia

---

## 🔄 Fluxo de Teste Completo

### Passo 1: Verificar Backends
```
1. GET http://localhost:8080/          → "Strava API is running!"
2. GET http://localhost:8000/          → Info da API
3. GET http://localhost:8000/health    → {"status": "healthy"}
```

### Passo 2: Autenticar com Strava
```
1. GET http://localhost:8080/authorize
2. Copiar link retornado
3. Abrir no navegador
4. Autorizar aplicação
5. Copiar código da URL de callback
6. GET http://localhost:8080/callback?code=CODIGO_AQUI
```

### Passo 3: Buscar Atividades
```
1. GET http://localhost:8080/activities/export  → Atividades básicas
2. GET http://localhost:8000/enrich             → Com dados climáticos
3. GET http://localhost:8000/insights           → Com análises
```

---

## ⚙️ Variáveis de Ambiente (Opcional)

Crie um **Environment** no Insomnia:

```json
{
  "backend_url": "http://localhost:8080",
  "fastapi_url": "http://localhost:8000",
  "streamlit_url": "http://localhost:8501"
}
```

Use nas requisições:
- `{{ _.backend_url }}/activities/export`
- `{{ _.fastapi_url }}/insights`

---

## 🐛 Troubleshooting

### Erro: "Connection refused"
- ✅ Verifique se o backend está rodando
- ✅ Confirme a porta correta (8080 ou 8000)

### Erro: "no_token"
- ✅ Execute o fluxo OAuth primeiro (/authorize → /callback)
- ✅ Verifique se o arquivo `tokens.json` foi criado

### Erro: "Failed to fetch activities"
- ✅ Token pode ter expirado (refaça OAuth)
- ✅ Verifique credenciais no `.env`

---

## 📝 Dicas

1. **Organize por Pastas**: Crie pastas no Insomnia para cada API
2. **Use Variáveis**: Facilita trocar entre ambientes (dev/prod)
3. **Salve Respostas**: Use "Response History" para comparar
4. **Teste Sequencial**: Use "Chain Requests" para fluxos automáticos

---

**Versão:** 1.25.0  
**Última Atualização:** 16/12/2025

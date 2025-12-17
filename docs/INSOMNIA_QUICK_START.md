# ⚡ Insomnia Quick Start

## 🚀 Importar em 3 Passos

### 1. Abrir Insomnia
- Inicie o aplicativo Insomnia

### 2. Importar Coleção
- Clique em **Create** (ou **+**)
- Selecione **Import From** → **File**
- Navegue até: `strava-connect-java-getavares/insomnia-collection.json`
- Clique em **Import**

### 3. Pronto!
Você verá 4 pastas:
- 1️⃣ Backend Spring Boot (8080)
- 2️⃣ API FastAPI (8000)
- 3️⃣ Dashboard Streamlit (8501)
- 🔄 Fluxo Completo (Sequencial)

---

## 🎯 Teste Rápido (5 minutos)

### Passo 1: Iniciar Backends
```bash
# Terminal 1 - Spring Boot
cd strava-spring
mvn spring-boot:run

# Terminal 2 - FastAPI
cd python-fastapi
python app.py
```

### Passo 2: Testar Conexão
No Insomnia, execute:
1. `GET http://localhost:8080/` → ✅ "Strava API is running!"
2. `GET http://localhost:8000/health` → ✅ {"status": "healthy"}

### Passo 3: Autenticar (OAuth 2.0)
1. Execute: `GET /authorize`
2. Copie o link da resposta
3. Abra no navegador
4. Clique em "Authorize"
5. Copie o `code` da URL de retorno
6. Execute: `GET /callback?code=SEU_CODIGO`

### Passo 4: Buscar Dados
1. `GET /activities/export` → Suas atividades
2. `GET /enrich` → Com dados climáticos
3. `GET /insights` → Com análises inteligentes

---

## 📋 Atalhos Úteis

| Ação | Atalho |
|------|--------|
| Nova requisição | `Ctrl + N` |
| Enviar requisição | `Ctrl + Enter` |
| Duplicar requisição | `Ctrl + D` |
| Buscar | `Ctrl + P` |
| Alternar sidebar | `Ctrl + \` |

---

## 🔧 Configuração Avançada

### Criar Environment
1. Clique no dropdown de environments (canto superior esquerdo)
2. Clique em **Manage Environments**
3. Adicione:
```json
{
  "backend_url": "http://localhost:8080",
  "fastapi_url": "http://localhost:8000",
  "auth_code": "COLE_SEU_CODIGO_AQUI"
}
```

### Usar Variáveis
Nas URLs, use:
- `{{ _.backend_url }}/activities/export`
- `{{ _.fastapi_url }}/insights`
- `{{ _.auth_code }}` nos parâmetros

---

## 💡 Dicas Pro

1. **Response History**: Clique no relógio para ver respostas anteriores
2. **Code Generation**: Gere código em várias linguagens (Python, cURL, etc)
3. **Chain Requests**: Use respostas de uma requisição em outra
4. **Organize**: Crie pastas para diferentes ambientes (dev, prod)

---

## 🐛 Problemas Comuns

### "Connection refused"
- ✅ Backend não está rodando
- ✅ Porta incorreta

### "no_token"
- ✅ Execute o fluxo OAuth primeiro
- ✅ Verifique `strava-spring/tokens.json`

### "502 Bad Gateway"
- ✅ Backend Spring não está acessível
- ✅ Verifique se está na porta 8080

---

## 📚 Documentação Completa

Ver: [INSOMNIA_SETUP.md](./INSOMNIA_SETUP.md)

---

**Versão:** 1.25.0  
**Última Atualização:** 16/12/2025

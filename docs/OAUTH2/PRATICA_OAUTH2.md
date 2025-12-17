# 🚀 Prática OAuth 2.0 - Implementação Real

> **Guia hands-on para testar OAuth 2.0 com Strava** | Passo a passo | Testado e funcionando

**Versão:** 4.11.25 | **Autor:** Rogério Tavares | **Data:** Nov/2025

---

## ✅ Pré-requisitos

- [ ] Java 21 instalado
- [ ] Maven instalado
- [ ] Conta Strava criada
- [ ] App registrado no Strava

---

## 📋 Passo 1: Configurar App no Strava

### 1.1 Acessar painel de API
```
URL: https://www.strava.com/settings/api
```

### 1.2 Criar aplicação
```
Application Name: Strava Connect Test
Category: Data Importer
Website: http://localhost:8081
Authorization Callback Domain: localhost
```

### 1.3 Anotar credenciais
```
Client ID: [seu_client_id]
Client Secret: [seu_client_secret]
```

---

## 📋 Passo 2: Configurar Variáveis de Ambiente

### 2.1 Criar arquivo .env na raiz do projeto
```bash
# strava-spring/.env
STRAVA_CLIENT_ID=181788
STRAVA_CLIENT_SECRET=9b73316f1bad61de6e0be4822afc55c4278b20f2
STRAVA_REDIRECT_URI=http://localhost:8081/callback
```

### 2.2 Verificar .gitignore
```bash
# Confirmar que .env está ignorado
cat .gitignore | grep .env
```

---

## 📋 Passo 3: Testar Backend Java

### 3.1 Iniciar aplicação
```bash
cd strava-spring
mvn spring-boot:run
```

### 3.2 Verificar logs
```
Aguardar mensagem: "Started StravaApplication in X seconds"
Porta: 8081
```

### 3.3 Testar endpoint de saúde
```bash
curl http://localhost:8081/health
```

**Resposta esperada:**
```json
{
  "status": "UP",
  "timestamp": "2025-11-XX..."
}
```

---

## 📋 Passo 4: Fluxo OAuth Completo

### 4.1 Gerar URL de autorização
```bash
# Abrir no navegador
http://localhost:8081/auth
```

**O que acontece:**
- Backend gera URL com client_id
- Redireciona para Strava
- Você vê tela de autorização

### 4.2 Autorizar aplicação
```
1. Login no Strava (se necessário)
2. Clicar "Authorize"
3. Aguardar redirecionamento
```

### 4.3 Callback automático
```
URL de retorno: http://localhost:8081/callback?code=XXXXX
Backend troca código por tokens automaticamente
```

**Resposta esperada:**
```json
{
  "access_token": "abc123...",
  "refresh_token": "xyz789...",
  "expires_at": 1234567890,
  "athlete": {
    "id": 3329857,
    "username": "rogtavares",
    "firstname": "Rogério",
    "lastname": "Tavares"
  }
}
```

---

## 📋 Passo 5: Testar Endpoints da API

### 5.1 Buscar dados do atleta
```bash
# Usar access_token obtido no passo anterior
curl -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  http://localhost:8081/api/athlete
```

### 5.2 Listar atividades
```bash
curl -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  http://localhost:8081/api/activities?per_page=5
```

### 5.3 Buscar atividade específica
```bash
curl -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  http://localhost:8081/api/activities/12345678
```

---

## 📋 Passo 6: Testar API Python (FastAPI)

### 6.1 Instalar dependências
```bash
cd python-fastapi
pip install -r requirements.txt
```

### 6.2 Iniciar servidor
```bash
python app.py
```

### 6.3 Testar endpoint de enriquecimento
```bash
curl -X POST http://localhost:8000/enrich \
  -H "Content-Type: application/json" \
  -d '{
    "access_token": "SEU_ACCESS_TOKEN",
    "activity_id": 12345678
  }'
```

---

## 🧪 Testes Automatizados

### Teste 1: Verificar configuração
```bash
# Verificar variáveis de ambiente
echo $STRAVA_CLIENT_ID
echo $STRAVA_CLIENT_SECRET
```

### Teste 2: Verificar conectividade
```bash
# Testar API do Strava
curl https://www.strava.com/api/v3/athlete \
  -H "Authorization: Bearer SEU_TOKEN"
```

### Teste 3: Validar tokens
```bash
# Verificar se token está válido
curl http://localhost:8081/api/validate-token \
  -H "Authorization: Bearer SEU_TOKEN"
```

---

## 🐛 Troubleshooting

### Erro: "Invalid client_id"
```
Solução: Verificar STRAVA_CLIENT_ID no .env
Confirmar que app está ativo no Strava
```

### Erro: "Redirect URI mismatch"
```
Solução: Verificar STRAVA_REDIRECT_URI
Deve ser exatamente: http://localhost:8081/callback
Confirmar no painel do Strava: Authorization Callback Domain = localhost
```

### Erro: "Token expired"
```
Solução: Usar refresh_token para renovar
curl -X POST https://www.strava.com/oauth/token \
  -d client_id=SEU_CLIENT_ID \
  -d client_secret=SEU_CLIENT_SECRET \
  -d grant_type=refresh_token \
  -d refresh_token=SEU_REFRESH_TOKEN
```

### Erro: "Port 8081 already in use"
```
Solução: Matar processo na porta
# Windows
netstat -ano | findstr :8081
taskkill /PID [PID] /F

# Linux/Mac
lsof -ti:8081 | xargs kill -9
```

---

## ✅ Checklist de Validação

- [ ] App registrado no Strava
- [ ] Variáveis de ambiente configuradas
- [ ] Backend Java rodando na porta 8081
- [ ] Fluxo OAuth completo funcionando
- [ ] Access token obtido com sucesso
- [ ] Dados do atleta retornados
- [ ] Atividades listadas corretamente
- [ ] API Python rodando na porta 8000
- [ ] Enriquecimento de dados funcionando

---

## 📊 Resultados Esperados

### Sucesso no OAuth:
```json
{
  "status": "success",
  "athlete_id": 3329857,
  "access_token": "presente",
  "refresh_token": "presente",
  "expires_at": "timestamp futuro"
}
```

### Dados do Atleta:
```json
{
  "id": 3329857,
  "username": "rogtavares",
  "firstname": "Rogério",
  "lastname": "Tavares",
  "city": "São Paulo",
  "country": "Brazil",
  "profile": "https://...",
  "created_at": "2015-XX-XX"
}
```

---

## 🎯 Próximos Passos

1. ✅ OAuth 2.0 funcionando
2. ⏭️ Implementar refresh automático de tokens
3. ⏭️ Adicionar persistência de tokens (Redis/DB)
4. ⏭️ Criar dashboard com dados reais
5. ⏭️ Integrar análises climáticas
6. ⏭️ Deploy na AWS

---

**versão 4.11.25 - 2025 - Rogério Tavares**

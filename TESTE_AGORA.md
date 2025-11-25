# 🎮 Teste e Brinque Agora!

## ✅ O que já está funcionando:

1. **API FastAPI** - http://localhost:8000 ✅
2. **Suas credenciais** configuradas ✅
3. **Backend Java** pronto (porta 8081) ⚠️

---

## 🚀 Opção 1: Teste Rápido (SEM rodar backend)

### Use o Strava Playground:

**1. Configure seu app:**
- Acesse: https://www.strava.com/settings/api
- Mude "Authorization Callback Domain" para: `developers.strava.com`

**2. Teste no Playground:**
- Acesse: https://developers.strava.com/playground/
- Clique em "Authorize"
- Escolha scopes: `activity:read_all`
- Autorize

**3. Brinque com os endpoints:**
```
GET /athlete - Ver seus dados
GET /athlete/activities - Ver suas atividades
GET /activities/{id} - Detalhes de uma atividade
GET /athlete/stats - Suas estatísticas
```

---

## 🎯 Opção 2: Teste Completo (COM backend)

### Passo 1: Rodar Backend Java

**Abra um NOVO terminal e execute:**
```bash
cd c:\Users\Cliente\Desktop\JAVA\strava-connect-java-getavares
run_backend.bat
```

**Aguarde ver:**
```
Started StravaSpringApplication
Tomcat started on port(s): 8081
```

### Passo 2: Fazer OAuth

**Abra no navegador:**
```
http://localhost:8081/api/auth
```

**Clique em "Authorize" no Strava**

### Passo 3: Testar Endpoints

**Abra outro terminal:**
```bash
# Ver seus dados
curl http://localhost:8081/api/athlete

# Ver suas atividades
curl http://localhost:8081/api/activities

# Ver insights
curl http://localhost:8000/insights
```

---

## 🌐 Teste no Navegador

### API FastAPI (já rodando):
```
http://localhost:8000/docs
```
**Aqui você pode:**
- ✅ Clicar em cada endpoint
- ✅ Clicar "Try it out"
- ✅ Clicar "Execute"
- ✅ Ver a resposta

### Endpoints para testar:
```
GET / - Info da API
GET /health - Health check
GET /enrich - Atividades + clima (precisa backend)
GET /insights - Análises (precisa backend)
```

---

## 🧪 Testes Divertidos

### 1. Ver seus dados do Strava:
```bash
curl http://localhost:8081/api/athlete
```

### 2. Ver suas últimas corridas:
```bash
curl http://localhost:8081/api/activities
```

### 3. Gerar insights sobre seu desempenho:
```bash
curl http://localhost:8000/insights
```

### 4. Ver atividades enriquecidas com clima:
```bash
curl http://localhost:8000/enrich
```

---

## 🎨 Brinque com o Swagger UI

**Acesse:**
```
http://localhost:8000/docs
```

**Teste:**
1. Clique em `GET /health`
2. Clique em "Try it out"
3. Clique em "Execute"
4. Veja a resposta: `{"status": "healthy"}`

**Repita para outros endpoints!**

---

## 📊 O que você vai ver:

### Seus dados:
```json
{
  "id": 3329857,
  "username": "seu_nome",
  "firstname": "Seu",
  "lastname": "Nome",
  "city": "Sua Cidade"
}
```

### Suas atividades:
```json
[
  {
    "name": "Morning Run",
    "distance": 5000,
    "moving_time": 1800,
    "type": "Run",
    "average_speed": 2.78
  }
]
```

### Insights:
```json
{
  "summary": [
    "Você corre melhor em dias com 18°C",
    "Vento reduz seu pace em 8.5%"
  ]
}
```

---

## 🎯 Escolha seu caminho:

### Caminho Fácil (5 min):
1. Use Strava Playground
2. Teste endpoints direto no navegador
3. Veja seus dados

### Caminho Completo (10 min):
1. Rode backend Java
2. Faça OAuth
3. Teste todos os endpoints
4. Veja insights inteligentes

---

## 🔗 Links Úteis

- **Strava Settings:** https://www.strava.com/settings/api
- **Playground:** https://developers.strava.com/playground/
- **Seu Perfil:** https://www.strava.com/athletes/3329857
- **API Docs:** http://localhost:8000/docs
- **Backend:** http://localhost:8081/api/auth

---

**Qual você quer testar primeiro? Playground ou Backend completo?**
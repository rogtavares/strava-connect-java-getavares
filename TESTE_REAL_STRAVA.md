# 🏃 Teste Real com Perfil Strava

**Atleta:** https://www.strava.com/athletes/3329857  
**Objetivo:** Testar fluxo completo OAuth + buscar atividades reais

---

## 📋 Passo a Passo Completo

### 1️⃣ Configurar App no Strava

**Acesse:** https://www.strava.com/settings/api

**Configure:**
- ✅ **Application Name:** "Strava Connect Test"
- ✅ **Category:** "Data Importer"
- ✅ **Website:** http://localhost:8080
- ✅ **Authorization Callback Domain:** `localhost` (para teste local)
  - **OU** `developers.strava.com` (para usar Playground)

**Anote:**
- 📝 **Client ID:** (copie o número)
- 📝 **Client Secret:** (copie o código)

---

### 2️⃣ Configurar Variáveis de Ambiente

**Windows PowerShell:**
```powershell
$env:STRAVA_CLIENT_ID="SEU_CLIENT_ID_AQUI"
$env:STRAVA_CLIENT_SECRET="SEU_CLIENT_SECRET_AQUI"
$env:STRAVA_REDIRECT_URI="http://localhost:8080/api/callback"
```

**Verificar:**
```powershell
echo $env:STRAVA_CLIENT_ID
echo $env:STRAVA_CLIENT_SECRET
```

---

### 3️⃣ Rodar Backend Java

**Terminal 1:**
```bash
cd strava-spring
mvn spring-boot:run
```

**Aguarde ver:**
```
Started StravaSpringApplication in X seconds
Tomcat started on port(s): 8080
```

---

### 4️⃣ Fazer OAuth (Autorização)

**Opção A - Usando Backend Java:**

1. **Abrir no navegador:**
```
http://localhost:8080/api/auth
```

2. **Você será redirecionado para Strava**
3. **Clique em "Authorize"**
4. **Será redirecionado de volta com seus dados**

**Opção B - Usando Strava Playground:**

1. **Configure callback domain:** `developers.strava.com`
2. **Acesse:** https://developers.strava.com/playground/
3. **Clique em "Authorize"**
4. **Copie o Access Token gerado**

---

### 5️⃣ Testar Endpoints

**Com Backend Java rodando:**

```bash
# Ver dados do atleta
curl http://localhost:8080/api/athlete

# Listar atividades
curl http://localhost:8080/api/activities

# Ver token info
curl http://localhost:8080/api/token-info
```

---

### 6️⃣ Testar API FastAPI (Insights)

**Terminal 2 (API FastAPI já está rodando):**

```bash
# Buscar atividades enriquecidas
curl http://localhost:8000/enrich

# Gerar insights inteligentes
curl http://localhost:8000/insights
```

---

## 🎮 Usando Strava Playground

### Vantagens:
- ✅ Não precisa configurar OAuth local
- ✅ Testa endpoints direto no navegador
- ✅ Vê respostas em tempo real
- ✅ Copia tokens facilmente

### Como usar:

1. **Acesse:** https://developers.strava.com/playground/

2. **Configure seu app:**
   - Authorization Callback Domain: `developers.strava.com`

3. **No Playground:**
   - Clique em "Authorize"
   - Escolha os scopes: `activity:read_all`
   - Autorize

4. **Testar endpoints:**
   - `GET /athlete` - Seus dados
   - `GET /athlete/activities` - Suas atividades
   - `GET /activities/{id}` - Detalhes de uma atividade

5. **Copiar Access Token:**
   - Use no seu backend Java
   - Salve em `tokens.json`

---

## 📊 Dados do Seu Perfil

**Atleta ID:** 3329857  
**URL:** https://www.strava.com/athletes/3329857

### O que vamos buscar:
- ✅ Nome e foto
- ✅ Estatísticas (distância total, tempo)
- ✅ Últimas 30 atividades
- ✅ Dados de cada corrida/treino
- ✅ Métricas (pace, FC, elevação)

---

## 🧪 Exemplo de Resposta Esperada

### GET /athlete
```json
{
  "id": 3329857,
  "username": "seu_username",
  "firstname": "Seu",
  "lastname": "Nome",
  "city": "Sua Cidade",
  "country": "Brasil",
  "profile": "url_da_foto",
  "created_at": "2015-XX-XXT00:00:00Z"
}
```

### GET /activities
```json
[
  {
    "id": 123456789,
    "name": "Morning Run",
    "distance": 5000.0,
    "moving_time": 1800,
    "elapsed_time": 1900,
    "total_elevation_gain": 50.0,
    "type": "Run",
    "start_date": "2025-11-25T06:00:00Z",
    "average_speed": 2.78,
    "max_speed": 3.5,
    "average_heartrate": 145.0,
    "max_heartrate": 165.0
  }
]
```

---

## 🔧 Troubleshooting

### Erro: "Invalid client_id"
```bash
# Verificar variável
echo $env:STRAVA_CLIENT_ID
# Reconfigurar
$env:STRAVA_CLIENT_ID="SEU_ID_CORRETO"
```

### Erro: "Redirect URI mismatch"
```bash
# Verificar no Strava settings/api
# Deve ser exatamente: localhost
# Ou: developers.strava.com (para Playground)
```

### Erro: "Token expired"
```bash
# Fazer novo OAuth
http://localhost:8080/api/auth
```

### Erro: "Port 8080 already in use"
```bash
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

---

## 📝 Checklist de Teste

- [ ] App configurado no Strava
- [ ] Client ID e Secret copiados
- [ ] Variáveis de ambiente configuradas
- [ ] Backend Java rodando (porta 8080)
- [ ] API FastAPI rodando (porta 8000)
- [ ] OAuth realizado com sucesso
- [ ] Token salvo em tokens.json
- [ ] Endpoint /athlete funcionando
- [ ] Endpoint /activities retornando dados
- [ ] API FastAPI gerando insights

---

## 🎯 Resultado Esperado

Ao final, você terá:

1. ✅ **Autenticação OAuth** funcionando
2. ✅ **Suas atividades** sendo buscadas
3. ✅ **Dados enriquecidos** com clima
4. ✅ **Insights inteligentes:**
   - "Você corre melhor em dias com 18°C"
   - "Vento reduz seu pace em 8.5%"
   - "Melhor horário: manhã"

---

**Vamos começar? Primeiro passo: configurar o app no Strava!**

**Data:** 25/11/2025 | **Atleta:** 3329857
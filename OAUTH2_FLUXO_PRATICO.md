# 🔐 Fluxo OAuth 2.0 - Guia Prático Completo

## 📋 Pré-requisitos

1. **Configurar aplicação no Strava**
   - Acesse: https://www.strava.com/settings/api
   - Clique em "Create & Manage Your App"
   - Preencha os campos (Application Name, Category, Website, etc.)
   - Configure o **Authorization Callback Domain**: `localhost`

2. **Obter credenciais**
   - **Client ID** (público)
   - **Client Secret** (secreto - mantenha confidencial!)
   - **Redirect URI**: `http://localhost:8080/callback`

---

## 🚀 PASSO 1: Gerar URL de Autorização

A primeira etapa é gerar uma URL que o usuário vai acessar no navegador para autorizar sua aplicação.

### Código Python para Gerar URL

```python
# File: generate_auth_url.py
import os
from urllib.parse import urlencode

# Suas credenciais Strava
CLIENT_ID = "YOUR_CLIENT_ID"  # Substitua
REDIRECT_URI = "http://localhost:8080/callback"
SCOPE = "read,activity:read_all"  # read,write,profile:read_all,activity:read_all

# Parâmetros da URL
params = {
    "client_id": CLIENT_ID,
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "approval_prompt": "auto"  # ou "force" para sempre solicitar autorização
}

# Gerar URL
auth_url = f"https://www.strava.com/oauth/authorize?{urlencode(params)}"

print("=" * 80)
print("🔗 COPIE E COLE ESTA URL NO NAVEGADOR:")
print("=" * 80)
print(auth_url)
print("=" * 80)
```

### Executar:
```bash
python generate_auth_url.py
```

### Saída esperada:
```
================================================================================
🔗 COPIE E COLE ESTA URL NO NAVEGADOR:
================================================================================
https://www.strava.com/oauth/authorize?client_id=123456&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Fcallback&scope=read%2Cactivity%3Aread_all&approval_prompt=auto
================================================================================
```

---

## 🌐 PASSO 2: Autorizar no Navegador e Receber o Código

### O que fazer:

1. **Abra o navegador** e acesse a URL gerada acima
2. **Faça login** no Strava (se não estiver logado)
3. **Autorize** a aplicação clicando em "Authorize"
4. **Você será redirecionado** para: `http://localhost:8080/callback?code=XXXXX`

### O Código (Authorization Code)

Você receberá um código assim:
```
http://localhost:8080/callback?code=abc123def456ghi789jkl012mno345pqr678
```

**Copie o valor do `code`**: `abc123def456ghi789jkl012mno345pqr678`

---

## 💱 PASSO 3: Trocar Código por Tokens

Agora você vai usar o código para obter os tokens (access_token e refresh_token).

### Código Python para Trocar Código por Tokens

```python
# File: exchange_code_for_tokens.py
import requests
import json

# Suas credenciais
CLIENT_ID = "YOUR_CLIENT_ID"           # Substitua
CLIENT_SECRET = "YOUR_CLIENT_SECRET"   # Substitua
REDIRECT_URI = "http://localhost:8080/callback"

# O código que você recebeu no navegador
AUTHORIZATION_CODE = input("Cole o código recebido no navegador: ").strip()

print(f"\n📝 Usando código: {AUTHORIZATION_CODE}\n")

# Endpoint para trocar código por tokens
token_url = "https://www.strava.com/oauth/token"

# Dados para enviar
payload = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "code": AUTHORIZATION_CODE,
    "grant_type": "authorization_code"
}

print("🔄 Trocando código por tokens...")

try:
    # Fazer requisição POST
    response = requests.post(token_url, data=payload)
    
    if response.status_code == 200:
        tokens = response.json()
        
        print("\n✅ SUCESSO! Tokens recebidos:\n")
        print("=" * 80)
        print(json.dumps(tokens, indent=2))
        print("=" * 80)
        
        # Extrair e salvar tokens
        access_token = tokens.get("access_token")
        refresh_token = tokens.get("refresh_token")
        expires_in = tokens.get("expires_in")
        
        print(f"\n📌 Access Token: {access_token}")
        print(f"📌 Refresh Token: {refresh_token}")
        print(f"⏱️  Expira em: {expires_in} segundos ({expires_in/3600:.1f} horas)")
        
        # Salvar em arquivo para usar depois
        with open("tokens.json", "w") as f:
            json.dump(tokens, f, indent=2)
        
        print("\n✅ Tokens salvos em 'tokens.json'")
        
    else:
        print(f"\n❌ ERRO: {response.status_code}")
        print(response.json())
        
except Exception as e:
    print(f"\n❌ ERRO: {e}")
```

### Executar:
```bash
python exchange_code_for_tokens.py
```

### Saída esperada:
```json
{
  "token_type": "Bearer",
  "expires_at": 1700000000,
  "expires_in": 21600,
  "refresh_token": "refresh_token_123456...",
  "access_token": "access_token_123456...",
  "athlete": {
    "id": 12345,
    "username": "seu_username",
    "firstname": "Seu",
    "lastname": "Nome",
    "city": "São Paulo",
    "state": "SP",
    "country": "Brasil",
    "sex": "M",
    "premium": true,
    "profile_medium": "https://example.com/profile.jpg",
    "profile": "https://example.com/profile.jpg"
  }
}
```

---

## 📱 PASSO 4: Usar o Access Token para Chamar a API do Strava

Agora com o `access_token`, você pode fazer requisições autenticadas na API do Strava.

### Código Python para Chamar API

```python
# File: fetch_athlete_profile.py
import requests
import json

# Carregar tokens do arquivo anterior
try:
    with open("tokens.json", "r") as f:
        tokens = json.load(f)
except FileNotFoundError:
    print("❌ Arquivo 'tokens.json' não encontrado!")
    print("Execute 'exchange_code_for_tokens.py' primeiro.")
    exit()

access_token = tokens.get("access_token")

if not access_token:
    print("❌ Access token não encontrado!")
    exit()

print(f"✅ Usando Access Token: {access_token[:20]}...\n")

# Headers da requisição
headers = {
    "Authorization": f"Bearer {access_token}"
}

print("=" * 80)
print("🔄 BUSCANDO DADOS DO ATLETA...")
print("=" * 80)

try:
    # 1️⃣ PERFIL DO ATLETA
    print("\n1️⃣ Perfil do Atleta (GET /api/v3/athlete)")
    response = requests.get("https://www.strava.com/api/v3/athlete", headers=headers)
    
    if response.status_code == 200:
        athlete = response.json()
        print("✅ SUCESSO!\n")
        print(json.dumps(athlete, indent=2))
        
        print(f"\n📊 Dados do Atleta:")
        print(f"  • ID: {athlete.get('id')}")
        print(f"  • Nome: {athlete.get('firstname')} {athlete.get('lastname')}")
        print(f"  • Username: {athlete.get('username')}")
        print(f"  • Cidade: {athlete.get('city')}, {athlete.get('state')}")
        print(f"  • Premium: {'Sim' if athlete.get('premium') else 'Não'}")
    else:
        print(f"❌ ERRO: {response.status_code}")
        print(response.json())
    
    # 2️⃣ ATIVIDADES RECENTES
    print("\n" + "=" * 80)
    print("2️⃣ Últimas 10 Atividades (GET /api/v3/athlete/activities)")
    response = requests.get(
        "https://www.strava.com/api/v3/athlete/activities",
        headers=headers,
        params={"per_page": 10}
    )
    
    if response.status_code == 200:
        activities = response.json()
        print("✅ SUCESSO!\n")
        
        if activities:
            print(f"📊 {len(activities)} Atividades encontradas:\n")
            for i, activity in enumerate(activities, 1):
                print(f"{i}. {activity.get('name')}")
                print(f"   • Tipo: {activity.get('type')}")
                print(f"   • Data: {activity.get('start_date')}")
                print(f"   • Distância: {activity.get('distance')/1000:.2f} km")
                print(f"   • Tempo: {activity.get('moving_time')/60:.0f} min")
                print()
        else:
            print("Sem atividades encontradas!")
    else:
        print(f"❌ ERRO: {response.status_code}")
        print(response.json())
    
    # 3️⃣ ESTATÍSTICAS DO MÊS
    print("=" * 80)
    print("3️⃣ Estatísticas (GET /api/v3/athlete/stats)")
    response = requests.get(
        "https://www.strava.com/api/v3/athlete/stats",
        headers=headers
    )
    
    if response.status_code == 200:
        stats = response.json()
        print("✅ SUCESSO!\n")
        
        print("📊 Stats do Mês:")
        print(f"  • Atividades: {stats.get('all_run_totals', {}).get('count', 0)}")
        print(f"  • Distância: {stats.get('all_run_totals', {}).get('distance', 0)/1000:.2f} km")
        print(f"  • Tempo: {stats.get('all_run_totals', {}).get('elapsed_time', 0)/3600:.1f} horas")
    else:
        print(f"❌ ERRO: {response.status_code}")
        print(response.json())
        
except Exception as e:
    print(f"\n❌ ERRO: {e}")

print("\n" + "=" * 80)
```

### Executar:
```bash
python fetch_athlete_profile.py
```

### Saída esperada:
```
================================================================================
🔄 BUSCANDO DADOS DO ATLETA...
================================================================================

1️⃣ Perfil do Atleta (GET /api/v3/athlete)
✅ SUCESSO!

{
  "id": 12345,
  "username": "rogtavares",
  "firstname": "Rogério",
  "lastname": "Tavares",
  ...
}

📊 Dados do Atleta:
  • ID: 12345
  • Nome: Rogério Tavares
  • Username: rogtavares
  • Cidade: São Paulo, SP
  • Premium: Sim

2️⃣ Últimas 10 Atividades (GET /api/v3/athlete/activities)
✅ SUCESSO!

📊 10 Atividades encontradas:

1. Morning Run
   • Tipo: Run
   • Data: 2025-11-24T07:30:00Z
   • Distância: 5.23 km
   • Tempo: 32 min
...
```

---

## 🔄 PASSO 5: Renovar o Access Token (quando expirar)

O `access_token` expira em 6 horas. Use o `refresh_token` para obter um novo.

```python
# File: refresh_access_token.py
import requests
import json

# Suas credenciais
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"

# Carregar tokens anterior
with open("tokens.json", "r") as f:
    tokens = json.load(f)

refresh_token = tokens.get("refresh_token")

print(f"🔄 Renovando token com refresh_token: {refresh_token[:20]}...\n")

# Endpoint para renovar token
token_url = "https://www.strava.com/oauth/token"

# Dados para enviar
payload = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "grant_type": "refresh_token",
    "refresh_token": refresh_token
}

try:
    response = requests.post(token_url, data=payload)
    
    if response.status_code == 200:
        new_tokens = response.json()
        
        print("✅ Token renovado com sucesso!\n")
        
        # Atualizar arquivo
        with open("tokens.json", "w") as f:
            json.dump(new_tokens, f, indent=2)
        
        access_token = new_tokens.get("access_token")
        print(f"📌 Novo Access Token: {access_token[:20]}...")
        print(f"⏱️  Expira em: {new_tokens.get('expires_in')} segundos")
        
    else:
        print(f"❌ ERRO: {response.status_code}")
        print(response.json())
        
except Exception as e:
    print(f"❌ ERRO: {e}")
```

---

## 📊 Resumo do Fluxo Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLUXO OAUTH 2.0 COMPLETO                     │
└─────────────────────────────────────────────────────────────────┘

1. generate_auth_url.py
   └─> Gera URL de autorização
       └─> Você acessa no navegador e autoriza

2. Navegador (Manual)
   └─> Autoriza a app
       └─> Recebe: http://localhost:8080/callback?code=XXXX

3. exchange_code_for_tokens.py
   └─> Cole o código
       └─> Obtém: access_token + refresh_token
           └─> Salva em tokens.json

4. fetch_athlete_profile.py
   └─> Usa access_token
       └─> Faz requisições autenticadas
           └─> Recebe dados do Strava (atleta, atividades, stats)

5. refresh_access_token.py (quando expirar)
   └─> Usa refresh_token
       └─> Obtém novo access_token
           └─> Continua fazendo requisições
```

---

## 🛠️ Como Implementar no Java (Spring Boot)

Se quiser implementar no seu projeto Spring:

```java
// StravaController.java
@RestController
@RequestMapping("/api/strava")
public class StravaController {
    
    @Autowired
    private StravaService stravaService;
    
    @Autowired
    private TokenService tokenService;
    
    // 1. Gerar URL de autorização
    @GetMapping("/auth-url")
    public ResponseEntity<?> getAuthUrl() {
        String authUrl = stravaService.generateAuthUrl();
        return ResponseEntity.ok(new AuthUrlResponse(authUrl));
    }
    
    // 2. Callback - receber código e trocar por token
    @GetMapping("/callback")
    public ResponseEntity<?> handleCallback(@RequestParam String code) {
        TokenResponse tokens = tokenService.exchangeCodeForTokens(code);
        return ResponseEntity.ok(tokens);
    }
    
    // 3. Buscar perfil do atleta
    @GetMapping("/athlete")
    public ResponseEntity<?> getAthleteProfile(
        @RequestHeader("Authorization") String token
    ) {
        AthleteProfile profile = stravaService.fetchAthleteProfile(token);
        return ResponseEntity.ok(profile);
    }
    
    // 4. Buscar atividades
    @GetMapping("/activities")
    public ResponseEntity<?> getActivities(
        @RequestHeader("Authorization") String token,
        @RequestParam(defaultValue = "10") int limit
    ) {
        List<Activity> activities = stravaService.fetchActivities(token, limit);
        return ResponseEntity.ok(activities);
    }
}
```

---

## 🚀 Próximos Passos

1. **Substitua suas credenciais** nos scripts
2. **Execute `generate_auth_url.py`**
3. **Acesse a URL no navegador**
4. **Execute `exchange_code_for_tokens.py`**
5. **Execute `fetch_athlete_profile.py`**
6. **Adapte para seu projeto Java/Python**

---

**Versão:** 1.25.0  
**Data:** 24 de Novembro de 2025  
**Autor:** Rogério Tavares

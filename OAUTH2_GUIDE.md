# 🔐 OAuth 2.0 - Guia Prático Completo

> **Guia definitivo para implementar OAuth 2.0 na prática** | Exemplos funcionais | Para engenheiros

**Autor:** Rogério Tavares | **Data:** 2025 | **Projeto:** Strava Connect

---

## 🎯 O que é OAuth 2.0?

OAuth 2.0 é um protocolo de autorização que permite aplicações acessarem recursos de usuários sem expor credenciais.

### Fluxo Básico:
1. **Usuário** clica "Login com Strava"
2. **App** redireciona para Strava
3. **Usuário** autoriza no Strava
4. **Strava** retorna código de autorização
5. **App** troca código por tokens
6. **App** usa tokens para acessar dados

---

## 🚀 Configuração Inicial

### 1. Registrar App no Strava
```
URL: https://www.strava.com/settings/api
Campos obrigatórios:
- Application Name: "Meu App Strava"
- Category: "Data Importer"
- Website: "http://localhost:8080"
- Authorization Callback Domain: "localhost"
```

### 2. Variáveis de Ambiente
```bash
# .env
STRAVA_CLIENT_ID=123456
STRAVA_CLIENT_SECRET=abc123def456
STRAVA_REDIRECT_URI=http://localhost:8080/callback
```

---

## 💻 Implementação Java (Spring Boot)

### 1. Dependências (pom.xml)
```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.apache.httpcomponents.client5</groupId>
        <artifactId>httpclient5</artifactId>
    </dependency>
    <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
    </dependency>
</dependencies>
```

### 2. Controller OAuth
```java
@RestController
public class OAuthController {
    
    private final String CLIENT_ID = System.getenv("STRAVA_CLIENT_ID");
    private final String CLIENT_SECRET = System.getenv("STRAVA_CLIENT_SECRET");
    private final String REDIRECT_URI = System.getenv("STRAVA_REDIRECT_URI");
    
    // PASSO 1: Gerar URL de autorização
    @GetMapping("/auth")
    public ResponseEntity<String> authorize() {
        String authUrl = "https://www.strava.com/oauth/authorize" +
            "?client_id=" + CLIENT_ID +
            "&response_type=code" +
            "&redirect_uri=" + REDIRECT_URI +
            "&scope=read,activity:read_all" +
            "&approval_prompt=auto";
        
        return ResponseEntity.ok()
            .header("Location", authUrl)
            .body("Redirect to: " + authUrl);
    }
    
    // PASSO 2: Receber callback e trocar código por tokens
    @GetMapping("/callback")
    public ResponseEntity<Map<String, Object>> callback(@RequestParam String code) {
        try {
            // Trocar código por tokens
            Map<String, Object> tokens = exchangeCodeForTokens(code);
            
            // Buscar dados do atleta
            Map<String, Object> athlete = getAthleteData((String) tokens.get("access_token"));
            
            Map<String, Object> response = new HashMap<>();
            response.put("tokens", tokens);
            response.put("athlete", athlete);
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            return ResponseEntity.badRequest()
                .body(Map.of("error", e.getMessage()));
        }
    }
    
    private Map<String, Object> exchangeCodeForTokens(String code) throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        
        String formData = "client_id=" + CLIENT_ID +
            "&client_secret=" + CLIENT_SECRET +
            "&code=" + code +
            "&grant_type=authorization_code";
        
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://www.strava.com/oauth/token"))
            .header("Content-Type", "application/x-www-form-urlencoded")
            .POST(HttpRequest.BodyPublishers.ofString(formData))
            .build();
        
        HttpResponse<String> response = client.send(request, 
            HttpResponse.BodyHandlers.ofString());
        
        ObjectMapper mapper = new ObjectMapper();
        return mapper.readValue(response.body(), Map.class);
    }
    
    private Map<String, Object> getAthleteData(String accessToken) throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://www.strava.com/api/v3/athlete"))
            .header("Authorization", "Bearer " + accessToken)
            .GET()
            .build();
        
        HttpResponse<String> response = client.send(request, 
            HttpResponse.BodyHandlers.ofString());
        
        ObjectMapper mapper = new ObjectMapper();
        return mapper.readValue(response.body(), Map.class);
    }
}
```

### 3. Aplicação Principal
```java
@SpringBootApplication
public class StravaOAuthApp {
    public static void main(String[] args) {
        SpringApplication.run(StravaOAuthApp.class, args);
        
        // Abrir navegador automaticamente
        try {
            Desktop.getDesktop().browse(new URI("http://localhost:8080/auth"));
        } catch (Exception e) {
            System.out.println("Acesse: http://localhost:8080/auth");
        }
    }
}
```

---

## 🐍 Implementação Python (FastAPI)

### 1. Dependências
```bash
pip install fastapi uvicorn requests python-dotenv
```

### 2. Código Python
```python
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REDIRECT_URI = os.getenv("STRAVA_REDIRECT_URI")

@app.get("/auth")
def authorize():
    auth_url = (
        f"https://www.strava.com/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=read,activity:read_all"
        f"&approval_prompt=auto"
    )
    return RedirectResponse(auth_url)

@app.get("/callback")
def callback(code: str):
    # Trocar código por tokens
    token_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    }
    
    token_response = requests.post(
        "https://www.strava.com/oauth/token",
        data=token_data
    )
    tokens = token_response.json()
    
    # Buscar dados do atleta
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    athlete_response = requests.get(
        "https://www.strava.com/api/v3/athlete",
        headers=headers
    )
    athlete = athlete_response.json()
    
    return {
        "tokens": tokens,
        "athlete": athlete
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 🌐 Implementação JavaScript (Node.js)

### 1. Dependências
```bash
npm init -y
npm install express axios dotenv
```

### 2. Código Node.js
```javascript
const express = require('express');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = 3000;

const CLIENT_ID = process.env.STRAVA_CLIENT_ID;
const CLIENT_SECRET = process.env.STRAVA_CLIENT_SECRET;
const REDIRECT_URI = process.env.STRAVA_REDIRECT_URI;

// PASSO 1: Redirecionar para autorização
app.get('/auth', (req, res) => {
    const authUrl = `https://www.strava.com/oauth/authorize` +
        `?client_id=${CLIENT_ID}` +
        `&response_type=code` +
        `&redirect_uri=${REDIRECT_URI}` +
        `&scope=read,activity:read_all` +
        `&approval_prompt=auto`;
    
    res.redirect(authUrl);
});

// PASSO 2: Callback e troca de tokens
app.get('/callback', async (req, res) => {
    const { code } = req.query;
    
    try {
        // Trocar código por tokens
        const tokenResponse = await axios.post('https://www.strava.com/oauth/token', {
            client_id: CLIENT_ID,
            client_secret: CLIENT_SECRET,
            code: code,
            grant_type: 'authorization_code'
        });
        
        const tokens = tokenResponse.data;
        
        // Buscar dados do atleta
        const athleteResponse = await axios.get('https://www.strava.com/api/v3/athlete', {
            headers: {
                'Authorization': `Bearer ${tokens.access_token}`
            }
        });
        
        const athlete = athleteResponse.data;
        
        res.json({
            tokens: tokens,
            athlete: athlete
        });
        
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

app.listen(PORT, () => {
    console.log(`Servidor rodando em http://localhost:${PORT}`);
    console.log(`Acesse: http://localhost:${PORT}/auth`);
});
```

---

## 🔄 Renovação de Tokens

### Java
```java
public Map<String, Object> refreshToken(String refreshToken) throws Exception {
    String formData = "client_id=" + CLIENT_ID +
        "&client_secret=" + CLIENT_SECRET +
        "&refresh_token=" + refreshToken +
        "&grant_type=refresh_token";
    
    HttpRequest request = HttpRequest.newBuilder()
        .uri(URI.create("https://www.strava.com/oauth/token"))
        .header("Content-Type", "application/x-www-form-urlencoded")
        .POST(HttpRequest.BodyPublishers.ofString(formData))
        .build();
    
    HttpResponse<String> response = HttpClient.newHttpClient()
        .send(request, HttpResponse.BodyHandlers.ofString());
    
    return new ObjectMapper().readValue(response.body(), Map.class);
}
```

### Python
```python
def refresh_token(refresh_token):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    
    response = requests.post("https://www.strava.com/oauth/token", data=data)
    return response.json()
```

---

## 🧪 Testando na Prática

### 1. Teste Manual (cURL)
```bash
# 1. Abrir no navegador:
https://www.strava.com/oauth/authorize?client_id=YOUR_ID&response_type=code&redirect_uri=http://localhost:8080/callback&scope=read,activity:read_all

# 2. Após autorizar, pegar o código da URL e executar:
curl -X POST https://www.strava.com/oauth/token \
  -d "client_id=YOUR_ID" \
  -d "client_secret=YOUR_SECRET" \
  -d "code=AUTHORIZATION_CODE" \
  -d "grant_type=authorization_code"

# 3. Usar o access_token:
curl -H "Authorization: Bearer ACCESS_TOKEN" \
  https://www.strava.com/api/v3/athlete
```

### 2. Teste com Postman
1. **GET** `http://localhost:8080/auth` → Copiar URL de redirecionamento
2. Abrir URL no navegador → Autorizar
3. Copiar código da URL de callback
4. **POST** `https://www.strava.com/oauth/token` com form-data
5. **GET** `https://www.strava.com/api/v3/athlete` com Bearer token

---

## ⚠️ Tratamento de Erros

### Códigos de Status Comuns
```java
switch (response.statusCode()) {
    case 200: // Sucesso
        break;
    case 401: // Token inválido/expirado
        throw new UnauthorizedException("Token inválido");
    case 403: // Sem permissão
        throw new ForbiddenException("Acesso negado");
    case 429: // Rate limit
        throw new RateLimitException("Muitas requisições");
    case 500: // Erro do servidor
        throw new ServerException("Erro no Strava");
}
```

### Rate Limits do Strava
- **15 minutos:** 100 requests
- **Diário:** 1.000 requests
- **Headers importantes:** `X-RateLimit-Limit`, `X-RateLimit-Usage`

---

## 🔒 Segurança e Boas Práticas

### ✅ Fazer:
- Usar HTTPS em produção
- Validar `state` parameter (CSRF protection)
- Armazenar tokens de forma segura
- Implementar refresh automático
- Logs de auditoria

### ❌ Não fazer:
- Expor client_secret no frontend
- Armazenar tokens em localStorage
- Ignorar rate limits
- Usar tokens expirados

### Exemplo com State (CSRF Protection):
```java
// Gerar state aleatório
String state = UUID.randomUUID().toString();
session.setAttribute("oauth_state", state);

String authUrl = "https://www.strava.com/oauth/authorize" +
    "?client_id=" + CLIENT_ID +
    "&state=" + state + // Adicionar state
    "&response_type=code" +
    "&redirect_uri=" + REDIRECT_URI;

// No callback, validar state
@GetMapping("/callback")
public ResponseEntity<?> callback(@RequestParam String code, 
                                 @RequestParam String state,
                                 HttpSession session) {
    String sessionState = (String) session.getAttribute("oauth_state");
    if (!state.equals(sessionState)) {
        throw new SecurityException("Invalid state parameter");
    }
    // ... resto do código
}
```

---

## 📊 Monitoramento e Logs

### Estrutura de Logs
```java
@Slf4j
@Component
public class OAuthLogger {
    
    public void logAuthStart(String clientId) {
        log.info("OAuth flow started - client_id: {}", clientId);
    }
    
    public void logTokenExchange(String code, boolean success) {
        log.info("Token exchange - code: {}... success: {}", 
                code.substring(0, 8), success);
    }
    
    public void logApiCall(String endpoint, int statusCode, long duration) {
        log.info("API call - endpoint: {} status: {} duration: {}ms", 
                endpoint, statusCode, duration);
    }
}
```

---

## 🚀 Deploy em Produção

### Variáveis de Ambiente
```bash
# Produção
STRAVA_CLIENT_ID=prod_client_id
STRAVA_CLIENT_SECRET=prod_secret
STRAVA_REDIRECT_URI=https://meuapp.com/callback

# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# Security
JWT_SECRET=super_secret_key
ENCRYPT_KEY=encryption_key
```

### Docker
```dockerfile
FROM openjdk:21-jdk-slim
COPY target/strava-oauth-1.0.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

---

## 📚 Recursos Adicionais

### Links Úteis
- **Strava API Docs:** https://developers.strava.com/docs/
- **OAuth 2.0 RFC:** https://tools.ietf.org/html/rfc6749
- **Playground:** https://developers.strava.com/playground/

### Bibliotecas Recomendadas
- **Java:** Spring Security OAuth2, Apache HttpClient
- **Python:** requests-oauthlib, authlib
- **Node.js:** passport-oauth2, axios

---

**✨ Este guia fornece tudo que você precisa para implementar OAuth 2.0 na prática!**

**Criado por:** Rogério Tavares | **Projeto:** Strava Connect | **Ano:** 2025
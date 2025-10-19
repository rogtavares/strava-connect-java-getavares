# 🏃♂️ getavares-strava-api

Integração local com a **API do Strava**, desenvolvida em **Java (IntelliJ IDEA)**, para explorar dados de atleta, atividades e estatísticas via autenticação **OAuth 2.0**.  
Projeto criado por [Rogério Tavares](https://github.com/rogtavares) — 🎨

---

## 🚀 Objetivo
Este projeto demonstra como conectar uma aplicação Java local à **API do Strava**, realizar a autenticação do usuário e consumir dados reais do perfil de atleta.

Ele serve como base para futuras integrações com análise de performance, monitoramento via Datadog e extensões com AWS.

---

## 🧩 Tecnologias Utilizadas
- **Java 17+**
- **Maven**
- **IntelliJ IDEA**
- **Gson (Google)** — manipulação de JSON  
- **Apache HttpClient 5** — comunicação HTTP  
- **Strava API v3**

---

## ⚙️ Estrutura do Projeto

getavares-strava-api/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── rogtavares/
│   │   │           └── strava/
│   │   │               ├── StravaApp.java
│   │   │               └── StravaService.java
│   │   └── resources/
│   │       └── application.properties
│   └── test/
│       └── java/
│           └── com/rogtavares/strava/
├── pom.xml
└── README.md

Observação: execute StravaApp.java (package com.rogtavares.strava) para iniciar o fluxo local de OAuth.

---

## 🔧 Criar e configurar o aplicativo Strava

1. Faça login e acesse: https://www.strava.com/settings/api  
2. Clique em "Create & Manage Your App" e preencha os campos.

O que significa cada item na página "Meu Aplicativo de API":
- Categoria: categoria da sua aplicação no Strava.  
- Clube: mostra se há um clube associado.  
- ID do cliente: identifcador público da sua app (use em URLs de autorização).  
- Segredo do cliente: secreto — mantenha confidencial.  
- Token de autorização (access token): token temporário usado nas requisições (expira).  
- Token de atualização (refresh token): usado para renovar o access token.  
- Limites de taxa: seu rate limit atual.  
- Domínio de Retorno de Autorização: defina `localhost` (ou `http://localhost:8080/callback`) para testes locais; em produção use seu domínio real.

---

## ⚙️ Configuração local (recomendada)

- Use variáveis de ambiente ou um arquivo fora do VCS para credenciais:
  - STRAVA_CLIENT_ID
  - STRAVA_CLIENT_SECRET
  - STRAVA_REDIRECT_URI (ex.: http://localhost:8080/callback)

Exemplo application.properties (somente para referência—não comitar):
STRAVA_CLIENT_ID=your_client_id
STRAVA_CLIENT_SECRET=your_client_secret
STRAVA_REDIRECT_URI=http://localhost:8080/callback

No código Java, leia via System.getenv("STRAVA_CLIENT_ID") ou Properties.

---

## ▶️ Fluxo rápido para testar localmente

1. Gere a URL de autorização no navegador:
   https://www.strava.com/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=REDIRECT_URI&scope=read,activity:read_all&approval_prompt=auto

2. Após autorizar você receberá: REDIRECT_URI?code=AUTHORIZATION_CODE

3. Troque o código por tokens:
```bash
curl -X POST https://www.strava.com/oauth/token \
  -d client_id=YOUR_CLIENT_ID \
  -d client_secret=YOUR_CLIENT_SECRET \
  -d code=AUTHORIZATION_CODE \
  -d grant_type=authorization_code
```

4. Use o access token nas requisições:
```bash
curl -H "Authorization: Bearer ACCESS_TOKEN" https://www.strava.com/api/v3/athlete
```

5. Para renovar:
```bash
curl -X POST https://www.strava.com/oauth/token \
  -d client_id=YOUR_CLIENT_ID \
  -d client_secret=YOUR_CLIENT_SECRET \
  -d grant_type=refresh_token \
  -d refresh_token=REFRESH_TOKEN
```

---

Se quiser, atualizo o README aplicando esse bloco no arquivo agora. Quer que eu
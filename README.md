# 🏃♂️ getavares-strava-api

Integração local com a **API do Strava**, desenvolvida em **Java (IntelliJ IDEA)**, para explorar dados de atleta, atividades e estatísticas via autenticação **OAuth 2.0**.  
Projeto criado por [Rogério Tavares](https://github.com/rogtavares) — *"Simples artista em busca de conqueista."* 🎨

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
│   │   │               ├── StravaApp.java       // class com.rogtavares.strava.StravaApp (main)
│   │   │               └── StravaService.java   // class com.rogtavares.strava.StravaService
│   │   └── resources/
│   │       └── application.properties (ex.: client id/secret via vars de ambiente)
│   └── test/
│       └── java/
│           └── com/
│               └── rogtavares/
│                   └── strava/
│                       └── StravaServiceTest.java
├── pom.xml
└── README.md

Observações:
- As declarações de package em StravaApp.java e StravaService.java devem ser: package com.rogtavares.strava;
- Recomendo manter client_id e client_secret fora do repositório (usar variáveis de ambiente ou arquivo fora do controle de versão).
- Dependências (Maven) ficam no pom.xml — removi o trecho XML do README para evitar confusões.

---

## 🔑 Criação da Aplicação no Strava

1. Acesse: [https://www.strava.com/settings/api](https://www.strava.com/settings/api)  
2. Clique em **Create & Manage Your App**
3. Preencha:
   - **Application Name:** `StravaLocalApp`
   - **Website:** `http://localhost`
   - **Authorization Callback Domain:** `localhost`
   - **Category:** `Other`
4. Salve e anote o `Client ID` e `Client Secret`

---

## 🔐 Autenticação OAuth 2.0

A autenticação segue o fluxo padrão do Strava: Autorização → Código → Troca por Token → Uso do Access Token.

1️⃣ Obtenha o Código de Autorização  
- Abra no navegador (substitua YOUR_CLIENT_ID e REDIRECT_URI):

https://www.strava.com/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=REDIRECT_URI&scope=read,activity:read_all&approval_prompt=auto

- Parâmetros importantes:
  - client_id: seu Client ID (da app Strava)
  - response_type: sempre "code"
  - redirect_uri: URL de callback registrada (ex.: http://localhost:8080/callback)
  - scope: escopos necessários (ex.: read, activity:read_all)
  - approval_prompt: "auto" ou "force"

- Após autorizar, o Strava redireciona para:
  REDIRECT_URI?code=AUTHORIZATION_CODE

2️⃣ Troque o código por tokens (access + refresh)  
- Exemplo cURL (substitua valores):
```bash
curl -X POST https://www.strava.com/oauth/token \
  -d client_id=YOUR_CLIENT_ID \
  -d client_secret=YOUR_CLIENT_SECRET \
  -d code=AUTHORIZATION_CODE \
  -d grant_type=authorization_code
```
- Resposta JSON típica:
{
  "token_type": "Bearer",
  "access_token": "ACCESS_TOKEN",
  "expires_at": 1670000000,
  "refresh_token": "REFRESH_TOKEN",
  "athlete": { ... }
}

3️⃣ Usando o Access Token nas requisições  
- Exemplo para obter perfil do atleta:
```bash
curl -H "Authorization: Bearer ACCESS_TOKEN" https://www.strava.com/api/v3/athlete
```

4️⃣ Atualizando (refresh) o Access Token  
- Access tokens expiram (ver campo expires_at). Para renovar:
```bash
curl -X POST https://www.strava.com/oauth/token \
  -d client_id=YOUR_CLIENT_ID \
  -d client_secret=YOUR_CLIENT_SECRET \
  -d grant_type=refresh_token \
  -d refresh_token=REFRESH_TOKEN
```

Boas práticas
- Armazene client_secret e refresh_token de forma segura (não comite no repositório).  
- Solicite apenas os escopos necessários.  
- Trate erros e limites de rate-limit (HTTP 429).  

---

## 📊 Endpoints Utilizados

| Endpoint               | Descrição                                 |
| ---------------------- | ----------------------------------------- |
| `/athlete`             | Retorna informações do atleta autenticado |
| `/athlete/activities`  | Lista atividades recentes do atleta       |
| `/athletes/{id}/stats` | Estatísticas agregadas do atleta (por período) |
| `/activities/{id}`     | Detalhes de uma atividade específica      |

Exemplos rápidos (usar Authorization: Bearer <token>):

- Perfil do atleta:
```bash
curl -H "Authorization: Bearer ACCESS_TOKEN" https://www.strava.com/api/v3/athlete
```

- Listar atividades:
```bash
curl -G https://www.strava.com/api/v3/athlete/activities \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  --data-urlencode "per_page=30" --data-urlencode "page=1"
```

---

## 🔗 Perfil Strava do Autor

Você pode ver meu perfil público no Strava: https://www.strava.com/athletes/3329857

Breve explicação:
- É um perfil público que mostra atividades, estatísticas básicas e segmentos, conforme as configurações de privacidade do usuário.  
- Dados públicos podem ser visualizados diretamente no site; para acessar dados via API (especialmente dados privados ou detalhes completos), é preciso autorizar a aplicação via OAuth 2.0 e obter um access token.  
- Para testes locais você pode usar o athlete id `3329857` em consultas que aceitarem identificadores públicos, mas a maioria das operações úteis requer autenticação do próprio atleta (consentimento).

Uso sugerido no projeto:
- Linkar para o perfil no README para referência.  
- Se quiser integrar ou demonstrar com esse perfil, faça o fluxo OAuth com as credenciais do atleta e armazene o refresh_token de forma segura.

---

## 📄 Licença

Este projeto é de uso livre para fins educacionais e demonstrações técnicas.  
© 2025 Rogério Tavares – Todos os direitos reservados.
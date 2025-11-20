# 🏃 getavares-strava-api

Integração local com a **API do Strava**, desenvolvida em **Java** com suporte para **Visual Studio Code** e **IntelliJ IDEA**, para explorar dados de atleta, atividades e estatísticas via autenticação **OAuth 2.0**.  
Projeto criado por [Rogério Tavares](https://github.com/rogtavares) em 2025

---

## 🚀 Objetivo
Este projeto demonstra como conectar uma aplicação Java local à **API do Strava**, realizar a autenticação do usuário e consumir dados reais do perfil de atleta.


## 🧩 Tecnologias Utilizadas


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


## Atualizar Java para JDK 21 (LTS)

Este projeto foi atualizado para usar Java 21. Passos recomendados para configurar o ambiente no Windows:

1. Instalar Temurin (Adoptium) JDK 21 via winget (recomendado):

  winget install --id EclipseAdoptium.Temurin.21.JDK -e --accept-package-agreements --accept-source-agreements

2. Definir JAVA_HOME na sessão ou globalmente (PowerShell):

  $env:JAVA_HOME = 'C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.x'
  $env:PATH = $env:JAVA_HOME + '\\bin;' + $env:PATH

3. Instalar Apache Maven (recomendado) ou adicionar Maven Wrapper ao projeto:

  - Via winget (se disponível):
    winget install --id Apache.Maven -e --accept-package-agreements --accept-source-agreements

4. Build do projeto:

  mvn -U package

Se você não tiver Maven instalado, pode instalar manualmente ou adicionar o Maven Wrapper (`mvnw`).

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

## ▶️ Fluxo rápido para testar localmente.

1. Gere a URL de autorização no navegador:
   https://www.strava.com/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=REDIRECT_URI&scope=read,activity:read_all&approval_prompt=auto

2. Após autorizar você receberá: REDIRECT_URI?code=AUTHORIZATION_CODE

3. Troque o código por tokens:
```bash
curl -X POST https://www.strava.com/oauth/token \
  -d client_id=YOUR_CLIENT_ID \
  -d client_secret=YOUR_CLIENT_SECRET \
  -d code=AUTHORIZATION_CODE \
  -d grant_type=authorization_code## 📚 Documentação Oficial
  
  - [https://developers.strava.com/](https://developers.strava.com/)
  - [https://communityhub.strava.com/](https://communityhub.strava.com/)
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

## 🔄 Métodos HTTP da API

A API V3 do Strava utiliza verbos HTTP apropriados para cada ação:

- **HEAD** — Obter apenas informações do cabeçalho HTTP
- **GET** — Recuperar recursos
- **POST** — Criar recursos ou executar ações personalizadas
- **PUT** — Atualizar ou substituir recursos
- **DELETE** — Remover recursos

---

## 📊 Códigos de Status HTTP

| Código | Descrição |
| ------ | --------- |
| **200** | Solicitação bem-sucedida |
| **201** | Recurso criado com sucesso |
| **401** | Não autorizado|
| **403** | Proibido; você não pode acessar |
| **404** | Não encontrado; o recurso não existe ou você não está autorizado |
| **429** | Muitas solicitações; você excedeu os limites de taxa |
| **500** | Erro no servidor Strava — verifique [status.strava.com](https://status.strava.com) |

---

## 📚 Documentação Oficial

- [https://developers.strava.com/](https://developers.strava.com/)
- [https://communityhub.strava.com/](https://communityhub.strava.com/)

### Exemplos e tutoriais úteis

- Strava Simple OAuth API Example: python & requests-oauthlib
- Strava Simple OAuth API Example: python & requests-oauthlib
  - [Documentação de referência do Strava](https://developers.strava.com/docs/reference/)
  - Português: "Exemplo simples de OAuth com a API do Strava (Python + requests-oauthlib): registramos uma aplicação no Strava, configuramos o ambiente de desenvolvimento, implementamos um exemplo que obtém um código de autorização, troca o código por um token e, por fim, realiza uma chamada à API do Strava para retornar o perfil do atleta."

Use esses recursos como complemento prático para entender o fluxo OAuth e adaptar para este projeto em Java (backend) e Python (enriquecimento/clima).

versão 1.7.0 - 2025 - Rogério Tavares
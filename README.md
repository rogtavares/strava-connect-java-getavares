# 🏃 Strava Connect - Integração Completa com Análises Inteligentes

![Version](https://img.shields.io/badge/version-1.25.0-blue)
![Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Java](https://img.shields.io/badge/java-21-red)
![FastAPI](https://img.shields.io/badge/fastapi-0.104-green)
![Spring Boot](https://img.shields.io/badge/spring%20boot-3.2-green)
![Streamlit](https://img.shields.io/badge/streamlit-latest-red)

> **Integração completa com API do Strava** | **Análises Inteligentes** | **Dashboard Visual** | **100% Gratuito** 🆓

**Versão:** 1.25.0 | **Projeto criado por:** [Rogério Tavares](https://github.com/rogtavares) | **Ano:** 2025

---

## 🎯 Objetivo

Construir uma **solução integrada** que:
1. ✅ **Autentica** com Strava via OAuth 2.0
2. ✅ **Puxa** atividades do usuário autenticado
3. ✅ **Enriquece** com dados climáticos históricos (OpenWeather)
4. ✅ **Gera** insights inteligentes sobre desempenho vs clima
5. ✅ **Visualiza** em dashboard interativo e profissional



## 📁 Estrutura do Projeto

```
strava-connect-java-getavares/
├── strava-spring/          # Backend Java Spring Boot
├── lambda-backend/         # AWS Lambda (Serverless)
├── python-fastapi/         # API REST Python
├── python-streamlit/       # Dashboard interativo
├── portfolio-site/         # Site Next.js
└── docs/                   # Documentação
```

### 🎯 Componentes Principais

| Componente | Descrição | Stack |
|-----------|-----------|-------|
| **strava-spring** | Backend API - Autenticação OAuth | Java 21, Spring Boot 3.2 |
| **lambda-backend** | Processamento serverless | Python 3.11+, AWS Lambda |
| **python-fastapi** | API enriquecida com dados | Python, FastAPI |
| **python-streamlit** | Dashboard interativo | Python, Streamlit |
| **portfolio-site** | Site profissional | TypeScript, Next.js 14 |

### 🚀 Como Usar Cada Componente

#### 1️⃣ Backend Java (Spring Boot)
```bash
cd strava-spring
mvn spring-boot:run
# Acessa em http://localhost:8080
```

#### 2️⃣ Dashboard Streamlit
```bash
cd python-streamlit
streamlit run app.py
# Acessa em http://localhost:8501
```

#### 3️⃣ API FastAPI
```bash
cd python-fastapi
python app.py
# Acessa em http://localhost:8000
```

#### 4️⃣ Portfolio Next.js
```bash
cd portfolio-site
npm install && npm run dev
# Acessa em http://localhost:3000
```

### 📝 Observações Importantes

- **Execução Local**: Execute `StravaApp.java` (package `com.getavares.strava`) para iniciar o fluxo OAuth local
- **Variáveis de Ambiente**: Configure `STRAVA_CLIENT_ID`, `STRAVA_CLIENT_SECRET` e `STRAVA_REDIRECT_URI`
- **Banco de Dados**: Projetos Python usam PostgreSQL/Redis quando necessário
- **Containerização**: Use Docker Compose para stack completo


## ⚡ Setup Rápido - Java 21

```bash
# 1. Instalar Java 21
winget install EclipseAdoptium.Temurin.21.JDK

# 2. Instalar Maven
winget install Apache.Maven

# 3. Build
mvn clean package
```

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
### Exemplos e tutoriais úteis

- Strava — fluxo OAuth (exemplo prático)
  - Resumo: registre sua aplicação no painel do Strava, configure variáveis de ambiente (client_id, client_secret, redirect_uri), gere a URL de autorização, troque o código por tokens (access + refresh) e faça chamadas autenticadas à API (/athlete, /activities, etc.).
  - URL de autorização (modelo):
    https://www.strava.com/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=REDIRECT_URI&scope=read,activity:read_all&approval_prompt=auto
  - Troca de código por tokens (exemplo curl):
    ```bash
    curl -X POST https://www.strava.com/oauth/token \
      -d client_id=YOUR_CLIENT_ID \
      -d client_secret=YOUR_CLIENT_SECRET \
      -d code=AUTHORIZATION_CODE \
      -d grant_type=authorization_code
    ```
  - Dicas: valide scopes necessários, armazene refresh_token para renovação automática, trate erros 429 (rate limit).

- Exemplo Python (requests-oauthlib)
  - Propósito: fluxo completo para obter authorization_code e trocar por access_token; ideal para testes e para pipelines de enriquecimento/clima.
  - Fluxo típico: registrar app → abrir URL de autorização → receber ?code no redirect → trocar por token → usar Authorization: Bearer ACCESS_TOKEN.
  - Use requests-oauthlib para simplificar o handshake OAuth2 em scripts de backend/enriquecimento.

- Adaptação para Java (Spring Boot)
  - Recomendações: use WebClient (Spring WebFlux) ou RestTemplate para chamadas HTTP, leia credenciais via System.getenv() ou arquivo externo, implemente endpoint /callback para receber o authorization_code e efetuar a troca por tokens.
  - Exemplo de passos: criar URL de autorização, redirecionar usuário, receber code, POST para /oauth/token, persistir access/refresh tokens.

- Ferramentas úteis
  - Strava API Reference: https://developers.strava.com/docs/reference/
  - Strava API Playground (testes interativos): https://developers.strava.com/playground/ — execute endpoints com tokens e veja respostas reais.
  - Postman / Insomnia — para testar chamadas e fluxos OAuth rapidamente.

- Uso prático com este projeto
  - Backend Java: implemente o fluxo OAuth e endpoints que retornem atividades do usuário.
  - Enriquecimento (Python): consuma as atividades, recupere coordenadas/tempo e chame API de clima (ex.: OpenWeather) para anexar dados climáticos históricos.
  - Visualização: exporte os dados enriquecidos para o dashboard (Streamlit / front-end) e gere insights comparativos (desempenho vs clima).

Use os links e exemplos acima como complemento prático para entender e adaptar o fluxo OAuth para este projeto em Java (backend) e Python (enriquecimento/clima).

versão 1.25.0 - 2025 - Rogério Tavares
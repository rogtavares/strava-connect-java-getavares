# 📂 Índice de Arquivos de Código

## 🏗️ BACKEND JAVA - SPRING BOOT

### Localização: `strava-spring/src/main/java/com/getavares/strava/`

#### Arquivos Principais:
- **StravaSpringApplication.java** - Classe principal da aplicação Spring
- **StravaController.java** - Endpoints REST e rotas da API

#### Subdiretórios:

##### `service/`
- **StravaService.java** - Lógica de negócio e integração com API Strava
- **TokenService.java** - Gerenciamento de tokens OAuth 2.0

##### `exception/`
- **CustomExceptions.java** - Exceções personalizadas
- **GlobalExceptionHandler.java** - Tratamento global de exceções
- **StravaAPIException.java** - Exceções específicas da API Strava

### Testes Java: `strava-spring/src/test/java/`
- **StravaSpringApplicationTests.java** - Testes unitários

### Configuração:
- `strava-spring/pom.xml` - Dependências Maven
- `strava-spring/src/main/resources/application.properties` - Configurações Spring

---

## 🐍 BACKEND PYTHON - AWS LAMBDA

### Localização: `lambda-backend/src/`

#### Manipuladores (Handlers):
- **auth_handler.py** - Autenticação e fluxo OAuth
- **athlete_handler.py** - Dados e informações do atleta
- **activities_handler.py** - Busca e processamento de atividades
- **stats_handler.py** - Cálculos e estatísticas
- **insights_handler.py** - Geração de insights inteligentes

#### Clientes e Utilitários:
- **strava_client.py** - Cliente HTTP para API Strava
- **config.py** - Configurações e variáveis de ambiente
- **monitoring.py** - Logs e monitoramento
- **utils.py** - Funções utilitárias

### Testes: `lambda-backend/tests/`
- `test_auth.py` - Testes de autenticação
- `unit/test_strava_client.py` - Testes unitários
- `integration/test_integration.py` - Testes de integração
- `performance/load_test.py` - Testes de performance

### Configuração:
- `lambda-backend/requirements.txt` - Dependências Python
- `lambda-backend/serverless.yml` - Configuração Serverless Framework

---

## 🌐 API REST - FASTAPI

### Localização: `python-fastapi/`

#### Arquivos Principais:
- **app.py** - Aplicação FastAPI (rotas e endpoints)
- **run.py** - Script para executar a aplicação

#### Configuração e Setup:
- **requirements.txt** - Dependências
- **requirements-dev.txt** - Dependências de desenvolvimento
- **.env.example** - Exemplo de variáveis de ambiente
- **Dockerfile** - Imagem Docker
- **docker-compose.yml** - Stack Docker local
- **setup.sh** - Script de configuração

#### Testes:
- **test_api.py** - Testes da API

#### Documentação:
- **README.md** - Guia de setup e uso
- **IMPLEMENTATION_SUMMARY.md** - Resumo de implementação
- **INSIGHTS.md** - Documentação de insights

---

## 📊 DASHBOARD - STREAMLIT

### Localização: `python-streamlit/`

#### Arquivo Principal:
- **app.py** - Aplicação Streamlit (página inicial)

#### Módulos:
- `modules/api_client.py` - Cliente para consumir API
- `modules/charts.py` - Gráficos e visualizações
- `modules/filters.py` - Filtros e buscas

#### Páginas:
- `pages/1_📈_Dashboard.py` - Dashboard principal
- `pages/2_📊_Analytics.py` - Análises detalhadas
- `pages/3_🚴_Activities.py` - Detalhes de atividades

#### Configuração:
- **config.py** - Configurações da aplicação
- **requirements.txt** - Dependências

---

## 🎨 PORTFOLIO - NEXT.JS

### Localização: `portfolio-site/app/`

#### Páginas:
- **page.tsx** - Home page (TypeScript React)
- **layout.tsx** - Layout principal da aplicação

#### Estilos:
- **globals.css** - Estilos globais

#### Configuração:
- `../package.json` - Dependências Node.js
- `../tsconfig.json` - Configuração TypeScript
- `../tailwind.config.js` - Configuração Tailwind CSS
- `../next.config.js` - Configuração Next.js

---

## 📝 Projeto Root - Raiz

### Localização: `src/main/java/com/getavares/strava/`
- **StravaApp.java** - App original (Java puro)

---

## 🔗 Como Abrir os Arquivos no VS Code

### Via Terminal PowerShell:
```powershell
# Abrir arquivo específico
code "strava-spring/src/main/java/com/getavares/strava/StravaController.java"

# Abrir diretório
code strava-spring
code python-fastapi
code python-streamlit
code portfolio-site
```

### Via VS Code (direto):
1. **Ctrl+P** - Abre paleta de comandos
2. Digite o nome do arquivo (ex: `StravaController.java`)
3. Pressione Enter

### Recomendações de Leitura:

#### 🟡 Para Iniciantes:
1. `README.md` - Entender o projeto
2. `strava-spring/src/main/java/com/getavares/strava/StravaSpringApplication.java` - Ver como inicia
3. `python-fastapi/app.py` - Ver endpoints
4. `python-streamlit/app.py` - Ver interface

#### 🟠 Para Intermediários:
1. `strava-spring/src/main/java/com/getavares/strava/StravaController.java` - Rotas
2. `strava-spring/src/main/java/com/getavares/strava/service/TokenService.java` - OAuth
3. `lambda-backend/src/activities_handler.py` - Processamento
4. `python-streamlit/modules/charts.py` - Visualizações

#### 🔴 Para Avançados:
1. `strava-spring/src/main/java/com/getavares/strava/exception/GlobalExceptionHandler.java` - Tratamento de erros
2. `lambda-backend/src/strava_client.py` - Cliente HTTP
3. `python-fastapi/app.py` - Arquitetura API
4. `portfolio-site/app/layout.tsx` - Componentes React

---

**Versão:** 1.25.0  
**Última Atualização:** 24 de Novembro de 2025  
**Criado por:** Rogério Tavares

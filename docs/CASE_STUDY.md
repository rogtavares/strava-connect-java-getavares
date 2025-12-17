# 📚 CASE STUDY - Strava Connect

## 📌 Informações Gerais

- **Projeto:** Strava Connect - Integração com API do Strava
- **Autor:** Rogério Tavares
- **Colaborador:** Lucas Pajarita
- **Status:** Privado - Case de Estudos
- **Data de Início:** 2025
- **Versão Atual:** 1.25.0
- **Licença:** MIT

---

## 🎯 Objetivo do Projeto

Construir uma **solução integrada completa** que:

1. ✅ **Autentica** com Strava via OAuth 2.0
2. ✅ **Puxa dados** de atividades do usuário
3. ✅ **Enriquece** com dados climáticos históricos
4. ✅ **Gera insights** inteligentes sobre desempenho
5. ✅ **Visualiza** em dashboard interativo

---

## 🧠 Conceitos de Aprendizado

### Backend
- [x] **Java 21 + Spring Boot 3.2**
  - REST API com Spring MVC
  - OAuth 2.0 implementation
  - Exception Handling Global
  - Tratamento de Tokens

- [x] **Python Serverless (AWS Lambda)**
  - Processamento assíncrono
  - Event-driven architecture
  - Integração com APIs externas

- [x] **API FastAPI (Python)**
  - Async/await patterns
  - Validation com Pydantic
  - Auto documentation

### Frontend
- [x] **Streamlit (Dashboard)**
  - Interactive data visualization
  - Real-time updates
  - Multi-page apps

- [x] **Next.js 14 (Portfolio)**
  - TypeScript + React
  - Tailwind CSS
  - Modern web development

### DevOps
- [x] **Docker & Docker Compose**
  - Containerização
  - Local stack setup

- [x] **Git & GitHub**
  - Version control
  - Branch strategy
  - Collaboration

---

## 🏗️ Arquitetura do Projeto

```
┌─────────────────────────────────────────────────────┐
│              STRAVA CONNECT ARCHITECTURE            │
└─────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐     ┌────────────┐
│   Cliente    │      │   Cliente    │     │  Browser   │
│  (App/Web)   │      │  (Dashboard) │     │ (Portfolio)│
└──────┬───────┘      └──────┬───────┘     └────────┬───┘
       │                     │                      │
       │                     │                      │
       ▼                     ▼                      ▼
┌──────────────────────────────────────────────────────┐
│         API GATEWAY / LOAD BALANCER                  │
└──────────────────────────────────────────────────────┘
       │                     │                      │
       ▼                     ▼                      ▼
┌────────────────┐  ┌──────────────┐  ┌─────────────────┐
│  Spring Boot   │  │  FastAPI     │  │  Streamlit      │
│  (Backend)     │  │  (Enrich)    │  │  (Dashboard)    │
└────────────────┘  └──────────────┘  └─────────────────┘
       │                     │
       └─────────┬───────────┘
               │
       ▼
┌──────────────────────────────────────────────┐
│  AWS Lambda / Serverless                     │
│  - Auth Handler                              │
│  - Activities Handler                        │
│  - Stats Handler                             │
│  - Insights Generator                        │
└──────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│  APIs Externas                               │
│  - Strava API                                │
│  - OpenWeather API                           │
│  - Database (PostgreSQL)                     │
└──────────────────────────────────────────────┘
```

---

## 📚 Stack Tecnológico

### Backend
| Tecnologia | Versão | Propósito |
|-----------|--------|----------|
| **Java** | 21 (LTS) | Linguagem principal backend |
| **Spring Boot** | 3.2 | Framework REST API |
| **Maven** | 3.9+ | Build tool |
| **Spring Security** | 6.x | OAuth 2.0 |
| **PostgreSQL** | 15 | Database |
| **Docker** | Latest | Containerização |

### APIs & Serviços
| Serviço | Propósito |
|--------|----------|
| **Strava API** | Dados de atividades |
| **OpenWeather API** | Dados climáticos históricos |
| **AWS Lambda** | Processamento serverless |

### Frontend
| Tecnologia | Versão | Propósito |
|-----------|--------|----------|
| **Python** | 3.11+ | Backend/Data processing |
| **FastAPI** | 0.104 | API enriquecida |
| **Streamlit** | Latest | Dashboard interativo |
| **Next.js** | 14 | Site portfolio |
| **TypeScript** | 5.x | Type safety |
| **Tailwind CSS** | 3.x | Styling |

---

## 🔑 Pontos de Aprendizado Principais

### 1. **OAuth 2.0 Implementation**
- ✅ Authorization Code Flow
- ✅ Token Management (access + refresh)
- ✅ Secure credential storage
- ✅ Token expiration handling

**Arquivos relevantes:**
- `strava-spring/src/main/java/com/getavares/strava/service/TokenService.java`
- `lambda-backend/src/auth_handler.py`

### 2. **REST API Design**
- ✅ RESTful principles
- ✅ HTTP methods (GET, POST, PUT, DELETE)
- ✅ Status codes (200, 201, 401, 403, 429)
- ✅ Error handling

**Arquivos relevantes:**
- `strava-spring/src/main/java/com/getavares/strava/StravaController.java`
- `python-fastapi/app.py`

### 3. **Async Processing**
- ✅ Event-driven architecture
- ✅ Lambda functions
- ✅ Queue processing
- ✅ Background jobs

**Arquivos relevantes:**
- `lambda-backend/src/activities_handler.py`
- `lambda-backend/src/insights_handler.py`

### 4. **Data Visualization**
- ✅ Interactive charts
- ✅ Real-time dashboards
- ✅ User engagement
- ✅ Data storytelling

**Arquivos relevantes:**
- `python-streamlit/modules/charts.py`
- `python-streamlit/app.py`

### 5. **Modern Web Development**
- ✅ TypeScript + React
- ✅ Component architecture
- ✅ CSS-in-JS (Tailwind)
- ✅ Responsive design

**Arquivos relevantes:**
- `portfolio-site/app/page.tsx`
- `portfolio-site/app/layout.tsx`

---

## 📖 Estrutura de Estudos Recomendada

### **Semana 1: Fundamentos**
1. Entender OAuth 2.0
2. Estudar REST API
3. Análise da arquitetura

**Documentos:**
- `docs/OAUTH2/README.md`
- `docs/ARQUIVOS_CODIGO.md`
- `ARCHITECTURE.md`

### **Semana 2: Backend Java**
1. Spring Boot fundamentals
2. Controllers e Services
3. Token management

**Código para estudar:**
- `StravaSpringApplication.java`
- `StravaController.java`
- `TokenService.java`

### **Semana 3: APIs & Processamento**
1. FastAPI patterns
2. Lambda functions
3. Event processing

**Código para estudar:**
- `python-fastapi/app.py`
- `lambda-backend/src/activities_handler.py`
- `lambda-backend/src/strava_client.py`

### **Semana 4: Frontend & Visualização**
1. Streamlit dashboards
2. Next.js components
3. Data visualization

**Código para estudar:**
- `python-streamlit/app.py`
- `python-streamlit/modules/charts.py`
- `portfolio-site/app/page.tsx`

### **Semana 5: Integração Completa**
1. Testar fluxo end-to-end
2. Deploy local
3. Troubleshooting

**Documentos:**
- `docs/TESTING.md`
- `docs/SETUP.md`

---

## 🎓 Exercícios Práticos

### **Exercício 1: OAuth 2.0 Flow**
- [ ] Gerar URL de autorização
- [ ] Receber authorization code
- [ ] Trocar por tokens
- [ ] Usar access token para fazer requisições

**Recurso:** `docs/OAUTH2/fluxo_pratico.md`

### **Exercício 2: Estender API**
- [ ] Criar novo endpoint em Spring
- [ ] Adicionar validação
- [ ] Implementar error handling
- [ ] Testar com Postman/Insomnia

### **Exercício 3: Adicionar Visualização**
- [ ] Criar novo gráfico em Streamlit
- [ ] Conectar com dados reais
- [ ] Adicionar filtros interativos
- [ ] Publicar no Streamlit Cloud

### **Exercício 4: Deploy Local**
- [ ] Build com Docker
- [ ] Executar stack completo
- [ ] Testar integração
- [ ] Validar fluxo end-to-end

---

## 🚀 Como Usar Este Repository

### Para Estudar:
```bash
# 1. Clone o repositório
git clone https://github.com/rogtavares/strava-connect-java-getavares.git

# 2. Leia a documentação
docs/INDEX.md              # Índice
docs/SETUP.md              # Setup local
docs/OAUTH2/README.md      # OAuth 2.0

# 3. Estude o código
# Comece com StravaController.java
# Depois TokenService.java
# Depois FastAPI app.py

# 4. Execute localmente
cd strava-spring
mvn spring-boot:run

cd python-streamlit
streamlit run app.py
```

---

## 📊 Benchmarks & Métricas

### Performance
- OAuth token exchange: ~500ms
- API responses: <100ms average
- Dashboard load: <2s

### Escalabilidade
- Suporta múltiplos usuários
- Rate limiting implementado
- Caching de dados

### Confiabilidade
- Error handling completo
- Retry mechanisms
- Logging e monitoring

---

## 🔒 Segurança

- ✅ OAuth 2.0 (não armazena senha)
- ✅ HTTPS (em produção)
- ✅ Token refresh automático
- ✅ Rate limiting
- ✅ Input validation
- ✅ SQL injection prevention

---

## 🤝 Contribuições

Este é um projeto de estudos. Para contribuir:

1. Crie uma branch: `git checkout -b feature/sua-feature`
2. Faça commit: `git commit -m 'Add sua-feature'`
3. Push: `git push origin feature/sua-feature`
4. Abra um Pull Request

---

## 📞 Contato

- **Autor:** Rogério Tavares
- **Email:** (seu email)
- **GitHub:** https://github.com/rogtavares

---

## 📄 Licença

MIT License - Veja LICENSE file para detalhes

---

**Versão:** 1.25.0  
**Data:** 16 de Dezembro de 2025  
**Status:** Case de Estudos Privado

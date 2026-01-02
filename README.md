# 🏃 Strava Connect - GE TAVARES

![Java](https://img.shields.io/badge/java-21-red)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![Private](https://img.shields.io/badge/repo-private-important)

> **Transforme seu suor em dados e seus dados em resultados.**

---

## 💡 A Proposta de Valor

Este projeto não é apenas sobre conectar APIs. É sobre **entender a jornada do atleta**.

Criamos uma ponte inteligente entre seus esforços físicos (registrados no Strava) e a ciência de dados. O objetivo é responder perguntas que o aplicativo padrão não responde:
- *"Como o clima impactou meu rendimento hoje?"*
- *"Qual é a tendência real da minha evolução?"*

Utilizamos a robustez do **Java** para garantir que seus dados sejam coletados com segurança e a agilidade do **Python** para gerar inteligência competitiva.

🔗 **Repositório:** [github.com/rogtavares/strava-connect-java-getavares](https://github.com/rogtavares/strava-connect-java-getavares)

---

## 🏗️ Arquitetura da Solução

O sistema opera como uma linha de produção de dados em três estágios:

### 1. Coleta e Segurança (Java Spring Boot)
Atua como o "porteiro" seguro da aplicação.
- Gerencia sua identidade e permissões (OAuth 2.0).
- Busca o histórico de atividades diretamente da fonte.
- **Foco:** Segurança, Estabilidade e Integração.

### 2. Inteligência de Dados (Python FastAPI)
O "cérebro" analítico.
- Recebe os dados brutos e aplica regras de negócio.
- Cruza informações de treino com dados meteorológicos (OpenWeather).
- **Foco:** Ciência de Dados, Insights e Enriquecimento.

### 3. Visualização (Streamlit)
*Em construção.* Será o painel de controle onde o atleta toma decisões baseadas em gráficos intuitivos.

---

## 🚀 Guia de Uso Rápido

Para ver a mágica acontecer na sua máquina local:

### Passo 1: Iniciar o Motor de Integração
Responsável por logar e buscar os dados.
```bash
cd strava-spring
mvn spring-boot:run
```
📍 **Acesse no navegador:**
- `http://localhost:8080/authorize` (Para conectar sua conta Strava)

### Passo 2: Ativar a Inteligência
Responsável por processar e analisar.
```bash
cd python-fastapi
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```
📍 **Acesse no navegador:**
- `http://localhost:8000/insights` (Para ver a análise climática e de performance)

---

## 🔒 Privacidade e Segurança

Tratamos dados pessoais com seriedade. Este projeto foi desenhado com **Privacy by Design**:

- **Credenciais Locais:** Suas senhas e tokens ficam apenas no seu computador.
- **Arquivos Protegidos:** O sistema ignora automaticamente arquivos sensíveis (`.env`, `tokens.json`) para evitar vazamentos acidentais.

> **Nota para Desenvolvedores:** Configure suas chaves (`strava.client-id`, `OPENWEATHER_API_KEY`) apenas em variáveis de ambiente ou arquivos locais não versionados.

---

## 📚 Central de Conhecimento

Para quem deseja entender a engenharia e as decisões de negócio por trás do código:

- 📖 **[Estudo de Caso (Business Case)](./docs/CASE_STUDY.md)**
  *Entenda o problema que resolvemos, as escolhas arquiteturais e o roadmap do produto.*
  
- 🔐 **[Guia de Autenticação (OAuth 2.0)](./docs/OAUTH2/)**
  *Uma explicação didática sobre como garantimos o acesso seguro aos dados do usuário.*

- 🔧 **[Ferramentas e Scripts](./scripts/)**
  *Utilitários para automação e manutenção.*

---

## 🛠️ Ecossistema Tecnológico

- **Integração:** Java 21 + Spring Boot 3.2
- **Analytics:** Python 3.11+ + FastAPI
- **Frontend & Visualização:** Streamlit (Roadmap)

---
## 🤝
- **Rogério Tavares**

**Versão Atual:** v26.4 (Janeiro/2026)

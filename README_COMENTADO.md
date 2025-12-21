# 🏃 Strava Connect

<!-- Badges informativos sobre as tecnologias e status do projeto -->
![Java](https://img.shields.io/badge/java-21-red)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![Private](https://img.shields.io/badge/repo-private-important)

<!-- Descrição resumida do projeto -->
> **Conecte-se ao Strava e analise seus treinos de forma inteligente**

---

## 💡 O que é isso?

<!-- Explicação clara do propósito do projeto -->
Um projeto que conecta com sua conta do Strava e transforma seus dados de treino em análises úteis. Combina **Java** para integração segura com a API do Strava e **Python** para análises e visualizações.

<!-- Benefícios para o usuário -->
Perfeito para quem quer entender melhor sua performance, ver evolução ao longo do tempo e ter insights sobre seus treinos.

<!-- Link do repositório -->
🔗 **Repositório:** [github.com/rogtavares/strava-connect-java-getavares](https://github.com/rogtavares/strava-connect-java-getavares)

---

## 🏗️ Como funciona?

<!-- Arquitetura dividida em componentes claros -->
O projeto é dividido em 3 partes que trabalham juntas:

### ☕ Backend Java (Spring Boot)
<!-- Responsabilidades do backend -->
- Faz a conexão segura com o Strava
- Autentica sua conta usando OAuth 2.0
- Busca e organiza seus dados de atividades
- Disponibiliza APIs para outras partes do sistema

### 🐍 Análises Python (FastAPI)
<!-- Responsabilidades da API de análises -->
- Processa os dados dos seus treinos
- Calcula métricas como ritmo médio, evolução e tendências
- Gera insights sobre sua performance

### 📊 Dashboard (Streamlit) - Em desenvolvimento
<!-- Interface visual (ainda em desenvolvimento) -->
- Interface visual para ver seus dados
- Gráficos de evolução e performance
- Insights fáceis de entender

---

## 🧠 O que você pode fazer?

<!-- Lista de funcionalidades disponíveis -->
- 📊 Ver volume e intensidade dos seus treinos
- 📈 Acompanhar sua evolução ao longo do tempo
- 🔍 Identificar padrões nos seus treinos
- 💪 Entender melhor sua performance

---

## 🚀 Como rodar?

<!-- Instruções passo a passo para executar o projeto -->

### 1. Backend Java
```bash
# Navegar para o diretório do Spring Boot
cd strava-spring
# Executar o projeto Maven
mvn spring-boot:run
```
📡 Acesse: http://localhost:8081

### 2. API Python
```bash
# Navegar para o diretório da API Python
cd python-fastapi
# Instalar dependências
pip install -r requirements.txt
# Executar a aplicação
python app.py
```
⚡ Acesse: http://localhost:8000

<!-- Aviso importante sobre configuração -->
> **Importante:** Configure as variáveis de ambiente do Strava antes (veja a documentação)

---

## 📚 Documentação

<!-- Links para documentação adicional -->
- 📖 [Case Study completo](./docs/CASE_STUDY.md)
- 🔐 [Como funciona o OAuth 2.0](./docs/OAUTH2/)
- 🔧 [Scripts úteis](./scripts/)

---

## 🔧 Tecnologias

<!-- Stack tecnológico utilizado -->
- **Backend:** Java 21 + Spring Boot 3.2
- **Análises:** Python 3.11+ + FastAPI
- **Dashboard:** Streamlit (em desenvolvimento)
- **Cloud:** AWS Lambda (planejado)
- **Banco:** PostgreSQL (planejado)

---

## 📁 Estrutura do Projeto

<!-- Organização dos diretórios -->
```
📁 strava-spring/        → Backend Java (integração Strava)
📁 python-fastapi/       → API Python (análises)
📁 python-streamlit/     → Dashboard visual
📁 docs/                 → Documentação
📁 scripts/              → Scripts úteis
```

---

## 🤝 Colaboradores

<!-- Equipe do projeto -->
- **Rogério Tavares** (Autor)
- **Lucas Pajarita** (Colaborador)

<!-- Status e última atualização -->
**Status:** 🟢 Ativo | **Último Update:** 16/12/2025

<!-- 
COMENTÁRIOS GERAIS SOBRE O README:

1. ESTRUTURA: O README segue uma estrutura lógica que guia o leitor do "o que é" até "como usar"

2. EMOJIS: Usados para tornar o documento mais visual e fácil de navegar

3. BADGES: Mostram informações técnicas importantes de forma visual

4. SEÇÕES CLARAS: Cada seção tem um propósito específico:
   - Introdução e propósito
   - Arquitetura técnica
   - Funcionalidades
   - Instruções de uso
   - Documentação adicional
   - Stack tecnológico
   - Organização do código
   - Créditos

5. LINGUAGEM: Tom informal e direto, focado no usuário final

6. LINKS: Referências para documentação mais detalhada

7. COMANDOS: Instruções práticas para executar o projeto
-->
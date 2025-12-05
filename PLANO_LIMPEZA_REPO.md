# 🧹 Plano de Limpeza e Reorganização do Repositório

## 📊 Análise da Situação Atual

### Problemas Identificados:

1. **Raiz do Repositório Poluída**
   - Muitos arquivos .md na raiz
   - Scripts .bat desorganizados
   - Falta de estrutura clara

2. **Arquivos Redundantes/Duplicados**
   - `OAUTH2_GUIDE.md` (14.59 KB)
   - `PRATICA_OAUTH2.md` (5.86 KB)
   - `OAUTH2_FLUXO_PRATICO.md` (novo)
   - → Mesmos conteúdos em diferentes formatos

3. **Arquivos de Teste Desorganizados**
   - `TESTE_MANUAL.md`
   - `RESUMO_TESTES.md`
   - `CONCLUSAO_TESTES.md`
   - → Devem estar em pasta `docs/`

4. **Scripts de Inicialização Espalhados**
   - `start-backend.bat`
   - `restart-backend.bat`
   - `test-oauth.bat`
   - → Devem estar em pasta `scripts/`

---

## 🎯 Estrutura Proposta (Limpa)

```
strava-connect-java-getavares/
│
├── 📄 README.md                    # Guia principal (ÚNICO)
├── 📄 LICENSE                      # MIT
├── 📄 .gitignore                   # Exclusões Git
├── 📄 pom.xml                      # Config Maven raiz
│
├── 📁 docs/                        # TODA documentação
│   ├── INDEX.md                    # Índice de documentação
│   ├── SETUP.md                    # Como configurar
│   ├── ARCHITECTURE.md             # Arquitetura
│   ├── OAUTH2/
│   │   ├── README.md               # Guia OAuth (ÚNICO)
│   │   ├── fluxo_pratico.md       # Passo a passo
│   │   └── exemplos_python/        # Códigos de exemplo
│   ├── API_REFERENCE.md            # Endpoints da API
│   ├── TESTING.md                  # Testes
│   └── TROUBLESHOOTING.md          # Soluções de problemas
│
├── 📁 scripts/                     # Scripts de automação
│   ├── start-backend.bat
│   ├── restart-backend.bat
│   ├── test-oauth.bat
│   ├── setup-env.sh
│   └── README.md
│
├── 📁 src/                         # Código Java (raiz original)
│   └── main/java/com/getavares/strava/
│
├── 📁 strava-spring/               # Backend Spring
├── 📁 lambda-backend/              # Backend Serverless
├── 📁 python-fastapi/              # API FastAPI
├── 📁 python-streamlit/            # Dashboard
├── 📁 portfolio-site/              # Site Next.js
│
├── 📁 .github/                     # CI/CD
└── 📁 target/                      # Build (em .gitignore)
```

---

## 📋 Plano de Ação

### FASE 1: Backup e Preparação
- [ ] Criar branch `cleanup/reorganize-repo`
- [ ] Fazer backup de todos os .md importantes

### FASE 2: Criar Estrutura de Pastas
```bash
mkdir docs
mkdir docs/OAUTH2
mkdir scripts
```

### FASE 3: Mover e Organizar Arquivos

#### Documentação → `docs/`
- `ARQUIVOS_CODIGO.md` → `docs/ARQUIVOS_CODIGO.md`
- `GUIA_ABRIR_ARQUIVOS.md` → `docs/COMO_ABRIR.md`
- `STATUS_FINAL.md` → `docs/STATUS.md`
- `TESTE_MANUAL.md` → `docs/TESTES.md`
- `RESUMO_TESTES.md` → (mesclar em TESTES.md)
- `CONCLUSAO_TESTES.md` → (mesclar em TESTES.md)
- `APRESENTACAO_MARKMAP.md` → `docs/VISUAL.md`

#### OAuth → `docs/OAUTH2/`
- `OAUTH2_GUIDE.md` → `docs/OAUTH2/README.md`
- `PRATICA_OAUTH2.md` → (mesclar em README.md)
- `OAUTH2_FLUXO_PRATICO.md` → `docs/OAUTH2/fluxo_pratico.md`

#### Scripts → `scripts/`
- `start-backend.bat` → `scripts/start-backend.bat`
- `restart-backend.bat` → `scripts/restart-backend.bat`
- `test-oauth.bat` → `scripts/test-oauth.bat`
- Criar `scripts/README.md` com instruções

### FASE 4: Atualizar README.md
- Manter ÚNICO README.md na raiz
- Referenciar documentação em `docs/`
- Adicionar índice com links

### FASE 5: Atualizar .gitignore
- Adicionar exclusões de cache
- Manter build artifacts excluídos

---

## 🗂️ Novo Arquivo: docs/INDEX.md

```markdown
# 📚 Documentação Completa

## 🚀 Quick Start
- [Setup Inicial](./SETUP.md)
- [Como Abrir Códigos](./COMO_ABRIR.md)

## 🔐 OAuth 2.0
- [Guia OAuth](./OAUTH2/README.md)
- [Fluxo Prático](./OAUTH2/fluxo_pratico.md)

## 🏗️ Arquitetura
- [Arquitetura Geral](./ARCHITECTURE.md)
- [Estrutura de Arquivos](./ARQUIVOS_CODIGO.md)

## 🧪 Testes
- [Guia de Testes](./TESTES.md)
- [Troubleshooting](./TROUBLESHOOTING.md)

## 📊 Referência
- [API Reference](./API_REFERENCE.md)
```

---

## ⚙️ Novo README.md (Simplificado)

```markdown
# 🏃 Strava Connect - Integração Completa

**Versão:** 1.25.0 | **Status:** ✅ Ativo | **Licença:** MIT

> Integração completa com API do Strava + Análises Inteligentes + Dashboard Visual

## 🚀 Quick Start

```bash
# 1. Setup
cd strava-spring
mvn spring-boot:run

# 2. Dashboard
cd python-streamlit
streamlit run app.py

# 3. API
cd python-fastapi
python app.py
```

## 📚 Documentação

- **[Setup Completo](./docs/SETUP.md)** - Como configurar ambiente
- **[OAuth 2.0](./docs/OAUTH2/README.md)** - Fluxo de autenticação
- **[Arquitetura](./docs/ARCHITECTURE.md)** - Design do projeto
- **[Índice Completo](./docs/INDEX.md)** - Toda documentação

## 🔧 Tecnologias

- **Backend:** Java 21, Spring Boot 3.2
- **APIs:** Python, FastAPI
- **Dashboard:** Streamlit
- **Site:** Next.js 14
- **Cloud:** AWS Lambda

## 🤝 Contribuindo

Veja [CONTRIBUTING.md](./CONTRIBUTING.md)

## 📄 Licença

MIT - Veja [LICENSE](./LICENSE)

---

**Criado por:** Rogério Tavares | **2025**
```

---

## 🚀 Opções de Implementação

### Opção 1: Limpeza Local (Recomendado)
1. Fazer limpeza e reorganização
2. Testar tudo funciona
3. Fazer commit único grande
4. Push para main

### Opção 2: Novo Repositório (Se muito quebrado)
1. Criar novo repo `strava-connect-clean`
2. Copiar apenas estrutura essencial
3. Mover projetos individuais
4. Arquivar repo antigo

### Opção 3: Repositórios Separados (Monorepo → Polyrepo)
Se quiser separar em múltiplos repos:
- `strava-backend` (Java + Python Lambda)
- `strava-dashboard` (Streamlit)
- `strava-api` (FastAPI)
- `strava-portfolio` (Next.js)
- `strava-docs` (Documentação)

---

## ✅ Checklist de Limpeza

- [ ] Criar branch `cleanup/reorganize-repo`
- [ ] Criar pasta `docs/` e `scripts/`
- [ ] Mover arquivos de documentação
- [ ] Mover scripts de inicialização
- [ ] Atualizar README.md
- [ ] Atualizar .gitignore
- [ ] Testar que tudo funciona
- [ ] Criar PR para revisão
- [ ] Merge para main
- [ ] Deletar branch

---

## 📞 Recomendação Final

**Opção 1 (Limpeza Local) é a melhor porque:**
- ✅ Mantém histórico Git
- ✅ Menos disruptivo
- ✅ Pode fazer incrementalmente
- ✅ Fácil reverter se algo quebrar

**Próximas Etapas:**
1. Você quer fazer limpeza local?
2. Criar novo repositório limpo?
3. Separar em múltiplos repositórios?

---

**Data:** 5 de Dezembro de 2025  
**Versão:** 1.0  
**Status:** Proposta

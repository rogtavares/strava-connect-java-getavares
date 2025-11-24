# 🎯 Guia Rápido - Abrir Arquivos de Código

## 📋 Copie e Cole os Caminhos Abaixo no Terminal

### Java - Spring Boot
```
strava-spring/src/main/java/com/getavares/strava/StravaSpringApplication.java
strava-spring/src/main/java/com/getavares/strava/StravaController.java
strava-spring/src/main/java/com/getavares/strava/service/StravaService.java
strava-spring/src/main/java/com/getavares/strava/service/TokenService.java
strava-spring/src/main/java/com/getavares/strava/exception/GlobalExceptionHandler.java
```

### Python - Lambda Backend
```
lambda-backend/src/auth_handler.py
lambda-backend/src/activities_handler.py
lambda-backend/src/athlete_handler.py
lambda-backend/src/stats_handler.py
lambda-backend/src/insights_handler.py
lambda-backend/src/strava_client.py
lambda-backend/src/config.py
```

### Python - FastAPI
```
python-fastapi/app.py
python-fastapi/run.py
```

### Python - Streamlit
```
python-streamlit/app.py
python-streamlit/config.py
python-streamlit/modules/api_client.py
python-streamlit/modules/charts.py
```

### TypeScript - Next.js
```
portfolio-site/app/page.tsx
portfolio-site/app/layout.tsx
portfolio-site/app/globals.css
```

---

## 🖱️ Opções de Abrir no VS Code

### Opção 1: Usar o Terminal
```powershell
cd "c:\Users\Cliente\Desktop\JAVA\strava-connect-java-getavares"
code strava-spring/src/main/java/com/getavares/strava/StravaController.java
```

### Opção 2: Abrir Todo o Diretório
```powershell
code strava-spring
code python-fastapi
code python-streamlit
code portfolio-site
```

### Opção 3: Atalho no VS Code
1. Pressione **Ctrl + P**
2. Digite o nome do arquivo
3. Pressione **Enter**

---

## 📚 Arquivos Mais Importantes para Ver

| Prioridade | Arquivo | O que faz |
|-----------|---------|----------|
| 🔴 CRÍTICO | `StravaSpringApplication.java` | Inicia a app Java |
| 🔴 CRÍTICO | `StravaController.java` | Define rotas REST |
| 🟠 IMPORTANTE | `TokenService.java` | Gerencia OAuth 2.0 |
| 🟠 IMPORTANTE | `auth_handler.py` | Autentica com Strava |
| 🟠 IMPORTANTE | `app.py` (FastAPI) | API enriquecida |
| 🟡 SECUNDÁRIO | `activities_handler.py` | Processa atividades |
| 🟡 SECUNDÁRIO | `app.py` (Streamlit) | Dashboard visual |
| 🟢 OPCIONAL | `page.tsx` | Site portfolio |

---

## 🚀 Próximos Passos

1. **Explorar a Estrutura**
   - Abra o diretório do projeto no VS Code
   - Navegue pelos arquivos listados

2. **Entender o Fluxo**
   - Leia `StravaSpringApplication.java` → entenda como inicia
   - Leia `StravaController.java` → veja as rotas
   - Leia `TokenService.java` → aprenda sobre OAuth

3. **Ver os Dados**
   - Abra `activities_handler.py` → veja como busca atividades
   - Abra `charts.py` → veja visualizações
   - Abra `app.py` (Streamlit) → veja a interface

4. **Modificar/Desenvolver**
   - Escolha qual arquivo quer editar
   - Faça as mudanças
   - Teste localmente
   - Faça commit e push

---

**Precisa de ajuda com algum arquivo específico? Só chamar!** 😊

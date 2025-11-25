# ✅ Ambiente Configurado!

## 🔐 Credenciais Strava

**Client ID:** 181788  
**Client Secret:** 9b73316f1bad61de6e0be4822afc55c4278b20f2  
**Redirect URI:** http://localhost:8080/api/callback

---

## 🚀 Como Rodar Backend Java

### Opção 1: Script Automático
```bash
run_backend.bat
```

### Opção 2: Manual
```bash
cd strava-spring
set STRAVA_CLIENT_ID=181788
set STRAVA_CLIENT_SECRET=9b73316f1bad61de6e0be4822afc55c4278b20f2
set STRAVA_REDIRECT_URI=http://localhost:8080/api/callback
mvn spring-boot:run
```

---

## 🔗 Próximo Passo: Fazer OAuth

**Abra no navegador:**
```
http://localhost:8080/api/auth
```

**Você será redirecionado para Strava para autorizar.**

---

## 📡 Endpoints Disponíveis

Após autorizar:

```bash
# Ver seus dados
curl http://localhost:8080/api/athlete

# Ver suas atividades
curl http://localhost:8080/api/activities

# Ver insights
curl http://localhost:8000/insights
```

---

**Ambiente pronto! Execute `run_backend.bat` para iniciar.**
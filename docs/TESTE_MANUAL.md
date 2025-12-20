# 🧪 Teste Manual OAuth 2.0

## Passo 1: Iniciar Backend

```bash
cd strava-spring
mvn spring-boot:run
```

Aguarde mensagem: `Started StravaApplication`

---

## Passo 2: Abrir Navegador

Acesse: **http://localhost:8081/authorize**

Você verá um link: "Authorize with Strava"

---

## Passo 3: Clicar no Link

O navegador será redirecionado para:
```
https://www.strava.com/oauth/authorize?client_id=181788&...
```

---

## Passo 4: Fazer Login no Strava

- Login: seu email/senha Strava
- Clicar: "Authorize"

---

## Passo 5: Callback Automático

Você será redirecionado para:
```
http://localhost:8081/callback?code=XXXXX
```

Verá mensagem: "Token armazenado. Você pode acessar /activities/export"

---

## Passo 6: Ver Atividades

Acesse: **http://localhost:8081/activities/export**

Verá JSON com suas atividades do Strava!

---

## ✅ Sucesso!

Se viu suas atividades, o OAuth 2.0 está funcionando! 🎉

---

**versão 4.11.25 - 2025 - Rogério Tavares**

# 🔒 Segurança - Credenciais Expostas

## ⚠️ AÇÃO URGENTE NECESSÁRIA

As credenciais do Strava foram expostas publicamente no commit:
https://github.com/rogtavares/strava-connect-java-getavares/commit/008b3f075fdffad46cbe9eae32364e72edb18f1a

**Client ID:** 181788  
**Client Secret:** 9b73316f1bad61de6e0be4822afc55c4278b20f2

## 🚨 O que fazer AGORA

### 1. Revogar credenciais atuais
```
1. Acesse: https://www.strava.com/settings/api
2. Localize sua aplicação
3. Clique em "Delete Application" ou "Revoke"
4. Confirme a revogação
```

### 2. Criar nova aplicação
```
1. Acesse: https://www.strava.com/settings/api
2. Clique em "Create & Manage Your App"
3. Preencha os dados:
   - Application Name: Strava Connect
   - Category: Data Importer
   - Website: http://localhost:8081
   - Authorization Callback Domain: localhost
4. Anote as NOVAS credenciais
```

### 3. Atualizar variáveis de ambiente
```bash
# Atualize com as NOVAS credenciais
STRAVA_CLIENT_ID=novo_client_id
STRAVA_CLIENT_SECRET=novo_client_secret
STRAVA_REDIRECT_URI=http://localhost:8081/callback
```

### 4. NUNCA commitar credenciais novamente
```bash
# Adicione ao .gitignore
echo ".env" >> .gitignore
echo "*.env" >> .gitignore
echo "**/tokens.json" >> .gitignore
```

## 🛡️ Boas Práticas

### ✅ FAZER
- Usar variáveis de ambiente
- Manter credenciais em arquivos .env (fora do Git)
- Usar placeholders em documentação (your_id, your_secret)
- Revogar credenciais imediatamente se expostas

### ❌ NÃO FAZER
- Commitar arquivos .env
- Colocar credenciais em código
- Compartilhar credenciais em documentação
- Deixar credenciais em histórico do Git

## 🔧 Limpar histórico do Git (opcional)

**ATENÇÃO:** Isso reescreve o histórico e pode causar problemas!

```bash
# Usar BFG Repo-Cleaner
git clone --mirror https://github.com/rogtavares/strava-connect-java-getavares.git
bfg --replace-text passwords.txt strava-connect-java-getavares.git
cd strava-connect-java-getavares.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

Ou use: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository

## 📝 Checklist de Segurança

- [ ] Credenciais antigas revogadas no Strava
- [ ] Nova aplicação criada no Strava
- [ ] Novas credenciais anotadas em local seguro
- [ ] Variáveis de ambiente atualizadas
- [ ] .gitignore atualizado
- [ ] Arquivos .env não commitados
- [ ] Histórico do Git limpo (opcional)

---

**IMPORTANTE:** Após revogar as credenciais antigas, elas não funcionarão mais e ninguém poderá usar para acessar seus dados do Strava.

**versão 4.11.25 - 2025 - Rogério Tavares**

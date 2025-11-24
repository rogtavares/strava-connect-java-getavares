# 🚀 Quick Start - Lambda Backend Strava Connect

## ⚡ Início Rápido (5 minutos)

### 1. Clone e Configure
```bash
cd lambda-backend

# Instalar dependências
pip install -r requirements.txt
npm install -g serverless
npm install --save-dev serverless-python-requirements
```

### 2. Configure AWS Credentials
```bash
aws configure
# AWS Access Key ID: [cole sua chave]
# AWS Secret Access Key: [cole sua chave secreta]
# Default region: us-east-1
# Default output format: json
```

### 3. Adicione Credenciais Strava
```bash
# Obter em: https://www.strava.com/settings/api

aws ssm put-parameter \
  --name /strava/client_id \
  --value "seu_client_id" \
  --type SecureString

aws ssm put-parameter \
  --name /strava/client_secret \
  --value "seu_client_secret" \
  --type SecureString

aws ssm put-parameter \
  --name /strava/redirect_uri \
  --value "https://yourdomain.com/auth/callback" \
  --type String
```

### 4. Deploy
```bash
# Development
serverless deploy --stage dev --region us-east-1

# Ou use o script
chmod +x deploy.sh
./deploy.sh dev us-east-1
```

### 5. Teste
```bash
# Obter informações do deploy
serverless info --stage dev

# Testar endpoint
curl https://xxxxx.execute-api.us-east-1.amazonaws.com/dev/athlete/123456 \
  -H "Authorization: Bearer seu_token"
```

---

## 📁 Estrutura de Arquivos

```
lambda-backend/
├── src/                          # Código das Lambdas
│   ├── config.py                 # Configurações
│   ├── utils.py                  # Utilitários (cache, tokens)
│   ├── auth_handler.py           # OAuth callback
│   ├── athlete_handler.py        # GET /athlete
│   ├── activities_handler.py     # GET /activities
│   ├── stats_handler.py          # GET /stats
│   └── insights_handler.py       # GET /insights (ML)
│
├── tests/                        # Testes unitários
│   └── test_auth.py
│
├── serverless.yml               # Config Serverless
├── requirements.txt             # Deps Python
├── README.md                     # Doc completa
├── SUMMARY.md                    # Sumário executivo
├── ARCHITECTURE.md              # Diagrama & fluxos
├── INTEGRATION.md               # Frontend integration
├── SETUP.md                      # Setup detalhado
├── deploy.sh                     # Script deploy
└── test_local.py               # Testes locais
```

---

## 📡 Endpoints

| Método | URL | Descrição |
|--------|-----|-----------|
| POST | `/auth/callback` | OAuth callback |
| GET | `/athlete/{user_id}?detailed=true` | Perfil |
| GET | `/activities/{user_id}?page=1&per_page=20` | Atividades |
| GET | `/stats/{user_id}?period=month` | Estatísticas |
| GET | `/insights/{user_id}?type=all&days=30` | Análises |

---

## 🧪 Executar Testes

```bash
# Instalar pytest
pip install pytest pytest-mock

# Rodar testes
pytest tests/ -v

# Com cobertura
pytest tests/ --cov=src --cov-report=html
```

---

## 🔍 Troubleshooting

### Erro: "Unable to locate credentials"
```bash
aws configure
# OU
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=xxx
```

### Erro: "TableNotFoundException"
As tabelas são criadas automaticamente no primeiro deploy. Se precisar recriar:
```bash
serverless deploy --force
```

### Erro: "CORS policy"
Verificar `serverless.yml`:
```yaml
cors:
  origins:
    - 'https://yourdomain.com'
```

---

## 📊 Monitoramento

### Ver Logs em Tempo Real
```bash
serverless logs -f authCallback --stage dev --tail
```

### Remover Stack
```bash
serverless remove --stage dev
```

---

## 🔐 Checklist de Segurança

- [ ] Credenciais no AWS Parameter Store (não no código)
- [ ] CORS configurado apenas para domínios autorizados
- [ ] HTTPS/SSL habilitado
- [ ] IAM roles com privilégios mínimos
- [ ] DynamoDB encryption habilitado
- [ ] CloudWatch logs habilitados
- [ ] WAF rules configuradas

---

## 📞 Próximos Passos

1. ✅ **Setup Completo** → Deploy dev funcionando
2. 🔗 **Integrar Frontend** → Adicionar endpoints no Next.js
3. 🧪 **E2E Tests** → Testar fluxo completo
4. 🚀 **Deploy Production** → `./deploy.sh prod us-east-1`
5. 📈 **Monitor** → CloudWatch + Alarms

---

## 🆘 Precisa de Ajuda?

- 📖 Leia `README.md` para documentação completa
- 🏗️ Veja `ARCHITECTURE.md` para entender a arquitetura
- 🔗 Consulte `INTEGRATION.md` para integrar com frontend
- 🐛 Rode `test_local.py` para testes locais

---

## ✨ Features Implementados

✅ OAuth 2.0 authentication  
✅ Cache inteligente (DynamoDB TTL)  
✅ Paginação de atividades  
✅ Estatísticas agregadas  
✅ Machine Learning insights  
✅ Token refresh automático  
✅ Error handling robusto  
✅ Logging & monitoring  
✅ Testes unitários  
✅ Deploy automático  

---

**Versão:** 1.0.0  
**Status:** 🟢 Pronto para usar  
**Última atualização:** 24 de novembro de 2025

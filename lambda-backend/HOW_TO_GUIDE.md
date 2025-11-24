# 🎓 How-To Guides - Practical Examples

## 1. How to Run Testes Localmente

### Opção A: Quick (todos os testes em 1 comando)
```bash
cd lambda-backend
pytest tests/ -v --cov=src --cov-fail-under=80
```

**Esperado:**
```
======================== 38 passed in 2.34s ========================
Coverage: 85.9% (target: 80%)
✅ PASSED
```

### Opção B: Passo a Passo
```bash
# 1. Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt pytest pytest-cov

# 2. Unit tests apenas
pytest tests/unit/ -v

# 3. Integration tests
pytest tests/integration/ -v -m integration

# 4. Com cobertura
pytest tests/ --cov=src --cov-report=html

# 5. Ver relatório
open htmlcov/index.html  # macOS
start htmlcov/index.html # Windows
```

---

## 2. How to Setup Local Server

### Opção A: SAM CLI (recomendado)
```bash
# 1. Instalar SAM
# macOS: brew tap aws/tap && brew install aws-sam-cli
# Windows: choco install aws-sam-cli

# 2. Rodar localmente
cd lambda-backend
sam local start-api --port 3000

# 3. Testar em outro terminal
curl http://localhost:3000/athlete/123
```

### Opção B: LocalStack
```bash
# 1. Instalar Docker
# https://docs.docker.com/get-docker/

# 2. Rodar
docker-compose -f docker-compose.yml up

# 3. Endpoints automáticos em localhost:4566
```

### Opção C: Script Automático
```bash
bash dev-setup.sh
# Escolher opção 6 (Start Local Server)
```

---

## 3. How to Manual Test API

### Opção A: Script Interativo
```bash
bash test-api.sh
# Menu com 11 opções de teste
```

### Opção B: cURL Direto
```bash
# 1. Get Athlete
curl -X GET http://localhost:3000/athlete/123456 \
  -H "Authorization: Bearer token123" \
  -H "Content-Type: application/json"

# 2. Get Activities com paginação
curl -X GET 'http://localhost:3000/activities/123456?page=1&per_page=20' \
  -H "Authorization: Bearer token123"

# 3. Get Stats
curl -X GET 'http://localhost:3000/stats/123456?period=month' \
  -H "Authorization: Bearer token123"

# 4. Get Insights
curl -X GET 'http://localhost:3000/insights/123456?type=all' \
  -H "Authorization: Bearer token123"

# 5. OAuth Callback
curl -X POST 'http://localhost:3000/auth/callback?code=abc123&state=xyz789' \
  -H "Content-Type: application/json"
```

### Opção C: Postman
```
1. Importar collection (se existir)
2. Set variables:
   - base_url: http://localhost:3000
   - auth_token: seu_token_aqui
   - user_id: 123456
3. Rodar requests
```

---

## 4. How to Load Test

### Opção A: Web UI (recomendado)
```bash
# 1. Terminal 1 - Servidor
sam local start-api --port 3000

# 2. Terminal 2 - Locust
locust -f tests/performance/load_test.py -H http://localhost:3000

# 3. Browser
# Acesse http://localhost:8089
# - Users: 100
# - Spawn rate: 10
# - Start swarming

# 4. Visualizar estatísticas em tempo real
```

### Opção B: Headless (CLI)
```bash
locust -f tests/performance/load_test.py \
  -H http://localhost:3000 \
  --users 100 \
  --spawn-rate 10 \
  --run-time 5m \
  --headless \
  --csv=results

# Resultados em results_stats.csv e results_requests.csv
```

### Opção C: Custom Script
```python
# load_custom.py
from locust import HttpUser, task, between

class CustomUser(HttpUser):
    wait_time = between(1, 2)
    
    @task
    def test_athlete(self):
        self.client.get("/athlete/123")
        
    @task
    def test_activities(self):
        self.client.get("/activities/123?page=1&per_page=20")

# Rodar:
# locust -f load_custom.py -H http://localhost:3000
```

---

## 5. How to Deploy

### Opção A: Deploy Local (Dev)
```bash
cd lambda-backend
export STRAVA_CLIENT_ID=seu_client_id
export STRAVA_CLIENT_SECRET=seu_secret
serverless deploy --stage dev
```

### Opção B: Deploy Prod (com CI/CD)
```bash
# 1. Push para main branch
git push origin main

# 2. GitHub Actions roda automaticamente:
#    - Testes
#    - Coverage check
#    - Security scan
#    - Deploy

# 3. Monitorar em: https://github.com/seu-repo/actions
```

### Opção C: Manual com Script
```bash
cd lambda-backend
bash deploy.sh dev us-east-1
# ou
bash deploy.sh prod us-east-1
```

---

## 6. How to Check Coverage

### Ver Cobertura no Terminal
```bash
pytest tests/ --cov=src --cov-report=term-missing
```

**Output:**
```
Name                    Stmts   Miss  Cover   Missing
────────────────────────────────────────────────────
src/strava_client.py     150     20   86.7%   45-47,89-91
src/utils.py              60      5   91.7%   15-20
TOTAL                    210     25   88.1%
```

### Gerar Relatório HTML
```bash
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html  # Abre no navegador
```

### Aumentar Coverage
```bash
# 1. Ver quais linhas não estão cobertas
pytest --cov=src --cov-report=term-missing

# 2. Adicionar testes para essas linhas
# Exemplo: linha 45-47 não coberta
# Criar teste que executa aquele código

# 3. Rodar novamente
pytest --cov=src
```

---

## 7. How to Monitor com Datadog

### Setup
```bash
# 1. Instalar Datadog
pip install datadog ddtrace

# 2. Configurar env vars
export DD_API_KEY=your_key_here
export DD_SERVICE=strava-connect
export DD_ENVIRONMENT=production

# 3. Inicializar
python -c "from src.monitoring import DatadogConfig; DatadogConfig.initialize()"
```

### Usar em Código
```python
from src.monitoring import datadog_trace, DatadogMetrics

# Auto-trace
@datadog_trace("get_athlete")
def get_athlete(user_id):
    # Automaticamente enviado para Datadog
    DatadogMetrics.increment("athlete.requests", tags={"user": user_id})
    return {...}
```

### Ver em Datadog
```
1. Acessar https://app.datadoghq.com
2. APM → Traces
3. Service: strava-connect
4. Ver latência, erros, dependências
```

---

## 8. How to Debug

### Opção A: Logs
```bash
# 1. Ver logs do Lambda local
sam local start-api --debug

# 2. Ver logs CloudWatch (prod)
aws logs tail /aws/lambda/strava-connect --follow
```

### Opção B: Debugger Python
```python
# No seu código
import pdb
pdb.set_trace()  # Pausa aqui

# Ou use debugger do VS Code:
# Adicionar breakpoint e rodar pytest --pdb
```

### Opção C: Verbose Output
```bash
pytest tests/ -vv -s --tb=long
# -vv: mais verbose
# -s: mostra prints
# --tb=long: stack trace completo
```

---

## 9. How to Fix Failing Tests

### Cenário 1: ImportError
```
Error: ModuleNotFoundError: No module named 'strava_client'

Solução:
1. Verificar PYTHONPATH
2. export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
3. Ou rodar: python -m pytest tests/
```

### Cenário 2: Connection Error
```
Error: ConnectionError: Failed to establish a new connection

Solução:
1. Verificar se server está rodando (sam local start-api)
2. Verificar URL no teste
3. Usar mock para testes unitários (não requer server)
```

### Cenário 3: Coverage Baixa
```
Error: FAILED because coverage is 75% (required 80%)

Solução:
1. pytest --cov=src --cov-report=term-missing (ver quais linhas)
2. Adicionar testes para aquelas linhas
3. Rodar novamente: pytest --cov=src
```

---

## 10. How to Troubleshoot Performance

### Problema: Latência Alta
```bash
# 1. Verificar em CloudWatch
aws logs tail /aws/lambda/strava-connect --follow

# 2. Ver distribuição de latência
pytest tests/performance/ --benchmark-only

# 3. Usar Locust para stress test
locust -f tests/performance/load_test.py -H http://localhost:3000

# 4. Verificar cache
curl http://localhost:3000/athlete/123 \
  -H "Authorization: Bearer token"
# Segunda vez deve ser mais rápida (cached)
```

### Problema: Rate Limit Atingido
```bash
# 1. Ver headers de rate limit
curl -i http://localhost:3000/athlete/123

# 2. Verificar Logs
grep "rate_limit" log.txt

# 3. Aumentar delay entre requisições
# Em test: wait_time = between(2, 5)  # de 1-3
```

### Problema: Memory High
```bash
# 1. Check Lambda memory
serverless info --stage dev

# 2. Aumentar
serverless deploy --stage dev -m 512

# 3. Verificar code
# Procurar por: loops infinitos, muitos objetos em memória
```

---

## 11. How to Review Code

### Checklist Antes de Commit
```bash
# 1. Testes passam?
pytest tests/ -v

# 2. Coverage OK?
pytest --cov=src --cov-fail-under=80

# 3. Estilo OK?
flake8 src/ tests/ --max-line-length=100

# 4. Sem erros de tipo?
mypy src/ --ignore-missing-imports

# 5. Segurança OK?
bandit -r src/

# Tudo OK? Commit!
git commit -m "feat: description"
```

### Code Review Checklist
```
- [ ] Testes cobrindo novo código
- [ ] Sem hardcoded values
- [ ] Logs apropriados
- [ ] Tratamento de erro
- [ ] Performance considerada
- [ ] Docs atualizadas
- [ ] Backward compatible
```

---

## 12. How to Contribute

### Setup Dev Environment
```bash
# 1. Clone
git clone repo-url
cd lambda-backend

# 2. Setup
bash dev-setup.sh
# Escolher: 1 (Setup completo)

# 3. Create branch
git checkout -b feature/sua-feature

# 4. Desenvolver
# - Escrever código
# - Escrever testes
# - Rodar localmente

# 5. Testes devem passar
bash dev-setup.sh test

# 6. Commit
git commit -m "feat: description"

# 7. Push
git push origin feature/sua-feature

# 8. Criar PR no GitHub
# - Descrever mudanças
# - Linkar issue
# - Aguardar review
```

---

## 13. Quick Reference - Comandos Mais Usados

```bash
# Setup
bash dev-setup.sh setup

# Tests
pytest tests/ -v --cov=src

# Server
sam local start-api --port 3000

# Manual testing
bash test-api.sh

# Load test
locust -f tests/performance/load_test.py -H http://localhost:3000

# Deploy
serverless deploy --stage dev

# Logs
aws logs tail /aws/lambda/strava-connect --follow

# Monitor
curl http://localhost:3000/athlete/123 -H "Authorization: Bearer token"
```

---

## 🆘 Need Help?

- **Documentação:** Ver `TESTING.md`, `MONITORING.md`
- **Quick Start:** Ver `QUICK_REFERENCE.md`
- **Issues:** Abrir issue no GitHub
- **Logs:** Ver CloudWatch
- **Monitoramento:** Ver Datadog Dashboard

---

**Last Updated:** 2024  
**Status:** 🟢 Ready to Use

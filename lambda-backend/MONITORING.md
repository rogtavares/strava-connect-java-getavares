# 📊 Monitoring & Observability Guide

## 📋 Overview

Guia completo para monitoramento, logging e observabilidade da API Strava Connect Lambda.

**Tecnologias:**
- 🔍 **CloudWatch Logs** - Logging centralizado
- 📈 **X-Ray** - Distributed tracing
- 📊 **Datadog** - APM & Analytics
- ⚠️ **CloudWatch Alarms** - Alertas

---

## 1️⃣ CloudWatch Logs

### Setup Automático (serverless.yml)

```yaml
# Lambda com logs automáticos
functions:
  getAthlete:
    handler: src.athlete_handler.lambda_handler
    environment:
      LOG_LEVEL: INFO
    events:
      - http:
          path: athlete/{user_id}
          method: get
```

### Padrão de Log Recomendado

```python
# src/athlete_handler.py
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """Get athlete data"""
    
    # Log de entrada
    logger.info(
        "Athlete request",
        extra={
            "user_id": event['pathParameters']['user_id'],
            "request_id": context.request_id,
            "timestamp": datetime.now().isoformat()
        }
    )
    
    try:
        # Lógica do handler
        athlete = strava_client.get_athlete(user_id)
        
        # Log de sucesso
        logger.info(
            "Athlete retrieved successfully",
            extra={
                "user_id": user_id,
                "athlete_id": athlete['id'],
                "response_time": elapsed_ms
            }
        )
        
        return response_success(athlete)
        
    except Exception as e:
        # Log de erro
        logger.error(
            "Error retrieving athlete",
            extra={
                "error": str(e),
                "error_type": type(e).__name__,
                "user_id": user_id
            },
            exc_info=True
        )
        return response_error("Failed to retrieve athlete", 500)
```

### Consultas CloudWatch Logs Insights

```sql
-- Testes latência p95
fields @timestamp, @duration
| stats pct(@duration, 95) as p95

-- Erros por tipo
fields @message, error_type
| stats count() as error_count by error_type

-- Requisições por endpoint
fields @logStream, path
| stats count() as requests by path

-- Taxa de erro
fields @message
| stats sum(strpos(@message, "ERROR")) as errors, count() as total
| stats errors/total * 100 as error_rate
```

---

## 2️⃣ X-Ray Distributed Tracing

### Ativar X-Ray (serverless.yml)

```yaml
provider:
  name: aws
  runtime: python3.11
  tracing:
    lambda: true
    apiGateway: true

functions:
  athlete:
    handler: src/athlete_handler.lambda_handler
    tracing: Active
```

### Código com X-Ray

```python
# src/athlete_handler.py
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()  # Auto-patch AWS SDK

@xray_recorder.capture('get_athlete')
def get_athlete_data(user_id):
    """Retrieve athlete - com tracing automático"""
    
    # Sub-segment customizado
    with xray_recorder.capture('fetch_athlete_info'):
        athlete = strava_client.get_athlete(user_id)
    
    # Adicionar metadata
    xray_recorder.current_subsegment().put_annotation('user_id', user_id)
    xray_recorder.current_subsegment().put_metadata('athlete_id', athlete['id'])
    
    return athlete
```

### Visualizar Traces (Console AWS)

1. CloudWatch → X-Ray → Traces
2. Service Map → Ver fluxo completo
3. Analytics → Consultas customizadas

---

## 3️⃣ Datadog Integration

### Setup

```bash
# 1. Instalar dependências
pip install datadog ddtrace

# 2. Configurar variáveis de ambiente
export DD_API_KEY=your_api_key
export DD_APP_KEY=your_app_key
export DD_SERVICE=strava-connect
export DD_ENVIRONMENT=production
export DD_VERSION=1.0.0
export DD_AGENT_HOST=localhost
export DD_AGENT_PORT=8126

# 3. Inicializar Datadog
python -c "from src.monitoring import DatadogConfig; DatadogConfig.initialize()"
```

### Instrumentar Código

```python
# src/athlete_handler.py
from src.monitoring import datadog_trace, DatadogMetrics

@datadog_trace(
    "get_athlete",
    tags={"resource": "athlete", "method": "GET"}
)
def get_athlete_data(user_id):
    """Handler com Datadog tracing"""
    
    start = time.time()
    athlete = strava_client.get_athlete(user_id)
    duration = (time.time() - start) * 1000
    
    # Enviar métricas customizadas
    DatadogMetrics.increment(
        "athlete.requests",
        tags={"user_id": user_id}
    )
    
    DatadogMetrics.timing(
        "athlete.response_time",
        duration,
        tags={"user_id": user_id}
    )
    
    return athlete
```

### Datadog Dashboard

```python
# criar_dashboard.py
from src.monitoring import DatadogDashboard

# Criar dashboard automaticamente
dashboard_id = DatadogDashboard.create_monitoring_dashboard()
print(f"Dashboard criado: {dashboard_id}")
```

### Métricas Disponíveis

| Métrica | Descrição | Threshold |
|---------|-----------|-----------|
| `request_duration` | Tempo de resposta | p95 < 500ms |
| `cache.hit_rate` | Taxa de acerto de cache | > 80% |
| `error_rate` | Taxa de erro | < 1% |
| `rate_limit_hits` | Vezes que atingiu rate limit | 0 |
| `token_refresh` | Renovações de token | monitor |

---

## 4️⃣ Alertas & Alarmes

### CloudWatch Alarms (serverless.yml)

```yaml
plugins:
  - serverless-plugin-tracing
  - serverless-plugin-aws-alerts

custom:
  alerts:
    topics:
      alarm: arn:aws:sns:${aws:region}:${aws:accountId}:strava-alarms
    alarms:
      - functionErrors
      - functionThrottles
      - functionDuration
      - functionInvocations

functions:
  athlete:
    handler: src/athlete_handler.lambda_handler
    alarms:
      - name: athlete-duration
        description: 'Alerta se resposta > 1000ms'
        metric: Duration
        threshold: 1000
        statistic: Average
        period: 300
        evaluationPeriods: 2
        comparisonOperator: GreaterThanThreshold
```

### Alarmes Recomendados

```json
{
  "alarms": [
    {
      "name": "HighErrorRate",
      "metric": "Errors",
      "threshold": "5%",
      "period": "5min",
      "action": "send-to-slack"
    },
    {
      "name": "HighLatency",
      "metric": "Duration",
      "threshold": "1000ms",
      "period": "5min",
      "action": "page-on-call"
    },
    {
      "name": "LowCacheHitRate",
      "metric": "cache.hit_rate",
      "threshold": "<50%",
      "period": "15min",
      "action": "investigate"
    },
    {
      "name": "RateLimitExceeded",
      "metric": "rate_limit_hits",
      "threshold": ">0",
      "period": "1min",
      "action": "scale-up"
    }
  ]
}
```

---

## 5️⃣ Performance Monitoring

### Métricas Chave

#### Latência

```bash
# CloudWatch Insights
fields @duration
| stats avg(@duration), pct(@duration, 50), pct(@duration, 95), pct(@duration, 99)
```

**Targets:**
- p50 < 100ms
- p95 < 500ms
- p99 < 1000ms

#### Taxa de Erro

```bash
# CloudWatch Insights
fields @message
| stats sum(strpos(@message, 'ERROR')) as errors, count() as total
| stats errors/total * 100 as error_rate
```

**Target:** < 1%

#### Throughput

```bash
# CloudWatch Insights
stats count() as requests, count()/300 as rps
```

**Target:** 100+ req/s com Lambda

#### Cache Hit Rate

```python
# src/strava_client.py
cache_stats = client.get_cache_stats()
hit_rate = cache_stats['hits'] / (cache_stats['hits'] + cache_stats['misses'])
print(f"Cache hit rate: {hit_rate:.1%}")
```

**Target:** > 80%

---

## 6️⃣ Logs Estruturados (JSON)

### Formato Recomendado

```python
import json
import logging

class JSONFormatter(logging.Formatter):
    """Formatar logs como JSON"""
    
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "function": record.funcName,
            "line": record.lineno,
            "request_id": getattr(record, 'request_id', 'N/A'),
            "user_id": getattr(record, 'user_id', 'N/A'),
        }
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)

# Usar no handler
logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
```

### Parsing no CloudWatch Logs Insights

```bash
fields @timestamp, level, message, user_id, request_id
| filter level = "ERROR"
| stats count() by user_id
```

---

## 7️⃣ Troubleshooting

### Problema: Latência Alta

```sql
-- 1. Identificar função lenta
fields @logStream, @duration
| filter @duration > 1000
| stats avg(@duration) by @logStream

-- 2. Verificar cache
fields cache_hit, @duration
| stats avg(@duration) by cache_hit

-- 3. Verificar taxa de erro
fields @message, error_type
| filter strpos(@message, 'ERROR') > 0
```

### Problema: Cache Hit Rate Baixo

```python
# Verificar por quê cache não funciona
stats = client.get_cache_stats()
print(f"Cache size: {stats['size']} items")
print(f"Misses: {stats['misses']}")
print(f"Expired: {stats['expired']}")

# Aumentar TTL se necessário
# Verificar se clear_cache está sendo chamado desnecessariamente
```

### Problema: Rate Limiting

```bash
# CloudWatch Logs - verificar quantas vezes atingiu limite
fields @message
| filter strpos(@message, "rate_limit_exceeded") > 0
| stats count()

# X-Ray - ver duração de waits
# Se muito alto, aumentar delay entre requisições
```

---

## 8️⃣ Dashboard Recomendado

### Widget 1: Overview

```
┌─────────────────────────────────────┐
│ Strava Connect - Last 1 Hour        │
├─────────────────────────────────────┤
│ Requests: 15,420                    │
│ Error Rate: 0.3%                    │
│ Avg Latency: 125ms                  │
│ Cache Hit: 87%                      │
└─────────────────────────────────────┘
```

### Widget 2: Latência P95

```
┌─────────────────────────────────────┐
│ P95 Latency (ms) - Last 24 Hours    │
│                                     │
│ 600 ──────────────────────────      │
│ 500 ──────────────────────────      │
│ 400 ──────────────────────────      │
│ 300 ────────────────────────────    │
│ 200 ────────────────────────────    │
│ 100 ────────────────────────────    │
│   0 ────────────────────────────    │
└─────────────────────────────────────┘
```

### Widget 3: Taxa de Erro

```
┌─────────────────────────────────────┐
│ Error Rate by Endpoint              │
│                                     │
│ /athlete       0.2%  ▌              │
│ /activities    0.4%  ▌▌             │
│ /stats         0.1%  ▌              │
│ /insights      2.1%  ▌▌▌▌▌▌▌▌      │
└─────────────────────────────────────┘
```

---

## 9️⃣ Runbook - Incident Response

### Cenário 1: Error Rate > 5%

```markdown
1. [Verificar] CloudWatch Logs - quais erros?
2. [Verificar] X-Ray - qual função falhando?
3. [Verificar] AWS Status - há problemas de serviço?
4. [Ação] Rollback última deploy se recente
5. [Ação] Aumentar logs de DEBUG temporariamente
6. [Comunicar] Status em Slack
```

### Cenário 2: Latência P95 > 1000ms

```markdown
1. [Verificar] Cache hit rate - está baixo?
2. [Verificar] Strava API - respondendo lentamente?
3. [Verificar] Lambda memory - suficiente?
4. [Ação] Aumentar memory provisioning
5. [Ação] Revisar queries DynamoDB
6. [Monitor] Por 15 min
```

### Cenário 3: Throttling

```markdown
1. [Verificar] CloudWatch - muitas requisições simultâneas?
2. [Verificar] Rate limiting - atingindo limites Strava?
3. [Ação] Ativar provisioned concurrency
4. [Ação] Aumentar DynamoDB capacity
5. [Escalate] Se padrão, considerar arquitetura
```

---

## 🔟 Checklist de Deploy

- [ ] Logs funcionando em CloudWatch
- [ ] X-Ray traces aparecem no console
- [ ] Datadog APM recebendo spans
- [ ] Alarmes configurados e testados
- [ ] Dashboard visível em Datadog
- [ ] Runbooks documentados
- [ ] Contato on-call configurado
- [ ] Testes de carga passando
- [ ] Coverage > 80%
- [ ] Zero problemas de segurança

---

**Status:** 🟢 Pronto para Produção  
**Última Atualização:** 2024  
**Manutenção:** Equipe DevOps

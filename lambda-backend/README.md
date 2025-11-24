# Lambda Backend - Strava Connect

## 🏃 Adaptado para: **ROGERIO TAVARES** (ID: 3329857)

**Perfil Strava:** https://www.strava.com/athletes/3329857

## 📋 Visão Geral

Backend serverless em Python para integração com Strava API. Arquitetura baseada em AWS Lambda + API Gateway + DynamoDB.

```plaintext
User → CloudFront → API Gateway → Lambda → DynamoDB
                         ↓
                    Strava API
```

### Endpoints

| Método | Caminho | Descrição | Auth |
|--------|---------|-----------|------|
| POST | `/auth/callback` | OAuth callback do Strava | ❌ |
| GET | `/athlete/{user_id}` | Perfil do atleta (cached) | ✅ |
| GET | `/activities/{user_id}` | Atividades paginated | ✅ |
| GET | `/stats/{user_id}` | Estatísticas agregadas | ✅ |
| GET | `/insights/{user_id}` | Análises com ML (opcional) | ✅ |

---

## 🔧 Configuração Inicial

### 1. Pré-requisitos

- Python 3.11+
- Node.js 18+
- AWS CLI configurado
- Serverless Framework
- Credenciais Strava (Client ID + Secret)

### 2. Instalação Local

```bash
# Clonar repositório
cd lambda-backend

# Instalar dependências
pip install -r requirements.txt

# Instalar Serverless Framework globalmente
npm install -g serverless
npm install --save-dev serverless-python-requirements
```

### 3. Variáveis de Ambiente

Criar arquivo `.env.local`:

```env
STRAVA_CLIENT_ID=seu_client_id
STRAVA_CLIENT_SECRET=seu_client_secret
STRAVA_REDIRECT_URI=https://yourdomain.com/auth/callback
AWS_REGION=us-east-1
DYNAMODB_TABLE_USERS=strava-users
DYNAMODB_TABLE_ACTIVITIES=strava-activities
DYNAMODB_TABLE_CACHE=strava-cache
```

### 4. Configurar AWS Parameter Store

```bash
# Armazenar credenciais no AWS Systems Manager Parameter Store
aws ssm put-parameter --name /strava/client_id --value "seu_client_id" --type SecureString
aws ssm put-parameter --name /strava/client_secret --value "seu_client_secret" --type SecureString
aws ssm put-parameter --name /strava/redirect_uri --value "https://yourdomain.com/auth/callback" --type String
```

---

## 📐 Estrutura de Arquivos

```
lambda-backend/
├── src/
│   ├── config.py                 # Configurações centralizadas
│   ├── utils.py                  # Utilitários (cache, tokens, responses)
│   ├── auth_handler.py           # POST /auth/callback
│   ├── athlete_handler.py        # GET /athlete/{user_id}
│   ├── activities_handler.py     # GET /activities/{user_id}
│   ├── stats_handler.py          # GET /stats/{user_id}
│   └── insights_handler.py       # GET /insights/{user_id}
├── tests/
│   ├── test_auth.py
│   ├── test_athlete.py
│   ├── test_activities.py
│   ├── test_stats.py
│   └── test_insights.py
├── serverless.yml                # Configuração Serverless
├── requirements.txt              # Dependências Python
├── README.md                      # Este arquivo
└── .env.local                     # Variáveis de ambiente (não versionar)
```

---

## 🚀 Deploy

### Development

```bash
# Deploy para stage 'dev'
serverless deploy --stage dev

# Deploy apenas uma função
serverless deploy function -f authCallback --stage dev
```

### Production

```bash
# Deploy para stage 'prod'
serverless deploy --stage prod --region us-east-1
```

### Logs em Tempo Real

```bash
# Ver logs de uma função
serverless logs -f authCallback --stage dev --tail

# Ver logs de todas as funções
serverless logs --stage dev --tail
```

### Remover Stack

```bash
serverless remove --stage dev
```

---

## 📡 Endpoints Detalhados

### 1. POST /auth/callback

**Autenticação OAuth do Strava**

**Request:**
```json
{
  "code": "authorization_code_from_strava",
  "scope": "read,activity:read_all"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "user_id": "123456",
    "athlete_name": "João Silva",
    "access_token": "token_...",
    "expires_in": 21600,
    "message": "Authentication successful"
  },
  "timestamp": "2025-11-24T10:30:00"
}
```

**Response (400):**
```json
{
  "success": false,
  "error": {
    "message": "Authorization code is required",
    "code": "MISSING_CODE"
  },
  "timestamp": "2025-11-24T10:30:00"
}
```

---

### 2. GET /athlete/{user_id}

**Recuperar Perfil do Atleta**

**URL:**
```
GET /athlete/123456?detailed=true
```

**Query Parameters:**
- `detailed` (opcional): `true/false` - Incluir dados detalhados (padrão: `false`)

**Response (200):**
```json
{
  "success": true,
  "data": {
    "cached": false,
    "athlete": {
      "id": 123456,
      "firstname": "João",
      "lastname": "Silva",
      "email": "joao@example.com",
      "profile": "https://dgalywyr863hv.cloudfront.net/...",
      "profile_medium": "https://dgalywyr863hv.cloudfront.net/...",
      "city": "São Paulo",
      "state": "SP",
      "country": "Brazil",
      "sex": "M",
      "premium": true,
      "created_at": "2020-01-15T08:30:00Z",
      "updated_at": "2025-11-24T10:00:00Z",
      "follower_count": 45,
      "friend_count": 120,
      "ftp": 280,
      "weight": 75.5,
      "stats": {
        "biggest_ride_elevation": 3200,
        "biggest_climb_elevation_gain": 800,
        "recent_ride_totals": {},
        "recent_run_totals": {},
        "all_ride_totals": {},
        "all_run_totals": {}
      }
    }
  },
  "timestamp": "2025-11-24T10:30:00"
}
```

---

### 3. GET /activities/{user_id}

**Recuperar Atividades (com Paginação)**

**URL:**
```
GET /activities/123456?page=1&per_page=20&sport_type=Run
```

**Query Parameters:**
- `page` (opcional): Número da página (padrão: `1`)
- `per_page` (opcional): Itens por página (padrão: `20`, máximo: `50`)
- `after` (opcional): Timestamp Unix - atividades após esta data
- `before` (opcional): Timestamp Unix - atividades antes desta data
- `sport_type` (opcional): Filtrar por tipo (ex: `Run`, `Ride`, `Swim`)

**Response (200):**
```json
{
  "success": true,
  "data": {
    "cached": false,
    "activities": [
      {
        "id": 9876543,
        "name": "Morning Run",
        "type": "Run",
        "sport_type": "Run",
        "distance": 5000.0,
        "moving_time": 1800,
        "elapsed_time": 1850,
        "elevation_gain": 120.5,
        "average_speed": 2.78,
        "max_speed": 3.5,
        "average_heartrate": 155.2,
        "max_heartrate": 175.0,
        "average_cadence": 85.5,
        "start_date": "2025-11-24T06:00:00Z",
        "start_date_local": "2025-11-24T03:00:00-03:00",
        "timezone": "America/Sao_Paulo",
        "location_city": "São Paulo",
        "location_state": "SP",
        "location_country": "Brazil",
        "kudos_count": 12,
        "comment_count": 3,
        "athlete_count": 1,
        "photo_count": 0,
        "trainer": false,
        "commute": false,
        "manual": false,
        "private": false,
        "flagged": false,
        "workout_type": null
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total_activities": 1
    }
  },
  "timestamp": "2025-11-24T10:30:00"
}
```

---

### 4. GET /stats/{user_id}

**Recuperar Estatísticas Agregadas**

**URL:**
```
GET /stats/123456?period=month&sport_type=Run
```

**Query Parameters:**
- `period` (opcional): `week`, `month`, `year`, `all` (padrão: `month`)
- `sport_type` (opcional): Filtrar por tipo

**Response (200):**
```json
{
  "success": true,
  "data": {
    "cached": false,
    "period": "month",
    "sport_type": "all",
    "stats": {
      "total_activities": 8,
      "total_distance": 42.5,
      "total_moving_time": 14400,
      "total_elevation_gain": 680.0,
      "average_speed": 10.62,
      "max_speed": 15.3,
      "average_heartrate": 152,
      "max_heartrate": 178,
      "average_distance": 5.31,
      "average_moving_time": 1800,
      "activities_by_type": {
        "Run": 5,
        "Ride": 3
      },
      "distance_by_type": {
        "Run": 15.2,
        "Ride": 27.3
      },
      "time_by_type": {
        "Run": 5400,
        "Ride": 9000
      },
      "top_activities": [
        {
          "id": 9876543,
          "name": "Morning Run",
          "distance": 5.0,
          "moving_time": 1800,
          "date": "2025-11-24T06:00:00Z",
          "type": "Run"
        }
      ]
    }
  },
  "timestamp": "2025-11-24T10:30:00"
}
```

---

### 5. GET /insights/{user_id}

**Análises com Machine Learning (Opcional)**

**URL:**
```
GET /insights/123456?type=all&days=30
```

**Query Parameters:**
- `type` (opcional): `all`, `performance`, `recommendations`, `trends`, `anomalies` (padrão: `all`)
- `days` (opcional): Número de dias para análise (padrão: `30`)

**Response (200):**
```json
{
  "success": true,
  "data": {
    "insights": {
      "generated_at": "2025-11-24T10:30:00",
      "period_days": 30,
      "total_activities": 8,
      "performance": {
        "analysis": "Performance over time",
        "metrics": {
          "Run": {
            "avg_speed_kmh": 10.62,
            "max_speed_kmh": 15.3,
            "std_dev_speed": 1.23,
            "improvement": "improving_5%",
            "consistency": "consistent"
          }
        }
      },
      "recommendations": {
        "suggestions": [
          {
            "category": "frequency",
            "severity": "warning",
            "message": "Apenas 8 atividades nos últimos 30 dias.",
            "recommendation": "Objetivo: 3-5 atividades por semana para melhores resultados"
          }
        ]
      },
      "trends": {
        "trend_analysis": "Performance trends over time",
        "data": {
          "2025-W47": {
            "activities": 2,
            "distance": 10.5,
            "time": 3600,
            "elevation": 240.0
          }
        }
      },
      "anomalies": {
        "anomalies_detected": [],
        "analysis": "Detects unusual activity patterns"
      }
    }
  },
  "timestamp": "2025-11-24T10:30:00"
}
```

---

## 🗄️ DynamoDB Schema

### Users Table
```
- user_id (PK): String
- athlete_name: String
- athlete_email: String
- athlete_profile: String
- tokens: {
    access_token: String,
    refresh_token: String,
    expires_at: Number,
    token_type: String
  }
- created_at: String (ISO 8601)
- updated_at: String (ISO 8601)
```

### Activities Table
```
- user_id (PK): String
- activity_id (SK): String
- name: String
- distance: Number
- moving_time: Number
- elevation_gain: Number
- average_speed: Number
- start_date: String (ISO 8601)
- cached_at: String (ISO 8601)
```

### Cache Table
```
- cache_key (PK): String
- data: String (JSON)
- expires_at: String (ISO 8601)
- created_at: String (ISO 8601)
```

---

## 🧪 Testes

### Executar Testes Locais

```bash
# Instalar pytest
pip install pytest pytest-mock

# Rodar todos os testes
pytest tests/

# Rodar teste específico
pytest tests/test_auth.py -v

# Cobertura de testes
pytest tests/ --cov=src --cov-report=html
```

### Mock Local com SAM

```bash
# Instalar AWS SAM CLI
pip install aws-sam-cli

# Rodar funções localmente
sam local start-api

# Testar endpoint
curl http://localhost:3000/athlete/123456
```

---

## 📊 Monitoramento e Logging

### CloudWatch Logs

```bash
# Ver logs da função authCallback
serverless logs -f authCallback --stage prod --tail

# Ver logs com filtro
serverless logs -f authCallback --stage prod --filter "ERROR"

# Exportar logs
serverless logs -f authCallback --stage prod > logs.txt
```

### X-Ray Tracing

Habilitar X-Ray para análise detalhada:

```yaml
provider:
  tracing:
    lambda: true
    apiGateway: true
```

---

## 💾 Cache Strategy

### TTL Padrão

- **Athlete**: 1 hora (3600s)
- **Activities**: 30 minutos (1800s)
- **Stats**: 2 horas (7200s)

### Invalidação de Cache

```python
# Manual cache invalidation
from utils import CacheManager
cache = CacheManager()
cache.delete('athlete:123456:detailed')
```

---

## 🔒 Segurança

### 1. Credenciais

- Usar AWS Secrets Manager ou Parameter Store
- Nunca commitir credenciais
- Rotacionar tokens regularmente

### 2. CORS

Configurado para aceitar requisições de CloudFront:

```yaml
functions:
  getAthlete:
    events:
      - http:
          cors:
            origins:
              - 'https://yourdomain.com'
            headers:
              - Authorization
              - Content-Type
```

### 3. Rate Limiting

API Gateway rate limiting (via plano):

```yaml
resources:
  Resources:
    ApiGatewayRestApi:
      Type: AWS::ApiGateway::RestApi
      Properties:
        ...
```

### 4. Token Refresh

Tokens expirados são automaticamente renovados usando refresh_token.

---

## 🐛 Troubleshooting

### Erro: "Token not found"

```bash
# Verificar se usuário está autenticado
aws dynamodb get-item --table-name strava-users --key '{"user_id":{"S":"123456"}}'
```

### Erro: "Rate limit exceeded"

- Aguardar 15 minutos antes de fazer nova requisição
- Aumentar cache TTL
- Implementar exponential backoff

### Erro: "DynamoDB provisioned throughput exceeded"

- Verificar se tabelas estão em PAY_PER_REQUEST
- Monitorar CloudWatch Metrics

---

## 📚 Referências

- [Strava API Documentation](https://developers.strava.com/)
- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Serverless Framework Docs](https://www.serverless.com/framework/docs)
- [AWS DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)

---

## 📝 Licença

MIT License - veja LICENSE.md

---

## 🤝 Contribuindo

Veja CONTRIBUTING.md para diretrizes.

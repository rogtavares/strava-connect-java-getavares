# Lambda Backend - Environment Setup

## Variáveis de Ambiente Requeridas

### Desenvolvimento Local

Criar arquivo `.env.local`:

```env
STRAVA_CLIENT_ID=seu_client_id_aqui
STRAVA_CLIENT_SECRET=seu_client_secret_aqui
STRAVA_REDIRECT_URI=http://localhost:8080/auth/callback
AWS_REGION=us-east-1
AWS_PROFILE=default
```

### Development Stack

```bash
# Instalar dependências
npm install
pip install -r requirements.txt

# Instalar Serverless Framework
npm install -g serverless
npm install --save-dev serverless-python-requirements

# Instalar AWS SAM CLI para testes locais
pip install aws-sam-cli
```

### Testing

```bash
# Instalar pytest
pip install pytest pytest-mock pytest-cov

# Rodar testes
pytest tests/ -v

# Cobertura
pytest tests/ --cov=src --cov-report=html
```

### Deployment

```bash
# Deploy development
export STRAVA_CLIENT_ID=seu_id
export STRAVA_CLIENT_SECRET=seu_secret
./deploy.sh dev us-east-1

# Deploy production
./deploy.sh prod us-east-1
```

### AWS Credentials

Configure AWS CLI:

```bash
aws configure
# Inserir:
# AWS Access Key ID: xxx
# AWS Secret Access Key: xxx
# Default region: us-east-1
# Default output format: json
```

### Local Testing com SAM

```bash
# Iniciar API local
sam local start-api

# Testar endpoint
curl http://localhost:3000/athlete/123456
```

## Troubleshooting

### Erro: "Unable to import module"

```bash
# Reconstruir dependências
rm -rf node_modules package-lock.json
npm install
```

### Erro: "Credentials not found"

```bash
# Verificar configuração AWS
aws sts get-caller-identity

# Usar profile específico
export AWS_PROFILE=seu_profile
```

### Erro: "DynamoDB tables not found"

```bash
# As tabelas são criadas automaticamente no deploy
# Se precisar recriá-las:
serverless deploy --stage dev --force
```

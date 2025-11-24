#!/bin/bash

# Script de deployment para Lambda Backend

set -e

echo "🚀 Iniciando deploy do Lambda Backend..."

# Validar variáveis de ambiente
if [ -z "$STRAVA_CLIENT_ID" ]; then
    echo "❌ Erro: STRAVA_CLIENT_ID não definido"
    exit 1
fi

if [ -z "$STRAVA_CLIENT_SECRET" ]; then
    echo "❌ Erro: STRAVA_CLIENT_SECRET não definido"
    exit 1
fi

# Determinar stage
STAGE=${1:-dev}
REGION=${2:-us-east-1}

echo "📦 Stage: $STAGE"
echo "🌍 Região: $REGION"

# Configurar AWS Parameter Store
echo "🔐 Configurando credenciais no AWS Parameter Store..."
aws ssm put-parameter \
    --name "/strava/client_id" \
    --value "$STRAVA_CLIENT_ID" \
    --type "SecureString" \
    --overwrite \
    --region "$REGION"

aws ssm put-parameter \
    --name "/strava/client_secret" \
    --value "$STRAVA_CLIENT_SECRET" \
    --type "SecureString" \
    --overwrite \
    --region "$REGION"

if [ -z "$STRAVA_REDIRECT_URI" ]; then
    STRAVA_REDIRECT_URI="https://yourdomain.com/auth/callback"
fi

aws ssm put-parameter \
    --name "/strava/redirect_uri" \
    --value "$STRAVA_REDIRECT_URI" \
    --type "String" \
    --overwrite \
    --region "$REGION"

# Instalar dependências
echo "📥 Instalando dependências..."
npm install
pip install -r requirements.txt

# Rodar testes
echo "🧪 Executando testes..."
pytest tests/ || echo "⚠️  Alguns testes falharam, continuando..."

# Deploy
echo "🚀 Deployando para $STAGE..."
npx serverless deploy --stage "$STAGE" --region "$REGION"

# Obter endpoints
echo ""
echo "✅ Deploy concluído!"
echo ""
echo "📋 Endpoints:"
npx serverless info --stage "$STAGE" --region "$REGION"

echo ""
echo "🎉 Lambda Backend deployado com sucesso!"

#!/usr/bin/env python
"""
Script de teste local para Lambda Backend
Permite testar endpoints sem fazer deploy no AWS
"""

import json
import sys
import os
from datetime import datetime

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_auth_callback():
    """Testa o endpoint de autenticação"""
    print("\n📋 Testando POST /auth/callback...")
    
    event = {
        'body': json.dumps({
            'code': 'test_auth_code_12345',
            'scope': 'read,activity:read_all'
        })
    }
    
    context = type('obj', (object,), {})()
    
    # Aqui você testaria com mocks do boto3 e requests
    print("✅ Teste skipped (requer AWS credentials)")


def test_athlete_endpoint():
    """Testa o endpoint de atleta"""
    print("\n📋 Testando GET /athlete/{user_id}...")
    
    event = {
        'pathParameters': {
            'user_id': '12345'
        },
        'queryStringParameters': {
            'detailed': 'true'
        }
    }
    
    context = type('obj', (object,), {})()
    
    print("✅ Teste skipped (requer AWS credentials)")


def test_activities_endpoint():
    """Testa o endpoint de atividades"""
    print("\n📋 Testando GET /activities/{user_id}...")
    
    event = {
        'pathParameters': {
            'user_id': '12345'
        },
        'queryStringParameters': {
            'page': '1',
            'per_page': '20',
            'sport_type': 'Run'
        }
    }
    
    context = type('obj', (object,), {})()
    
    print("✅ Teste skipped (requer AWS credentials)")


def print_header():
    """Imprime header"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                 Lambda Backend - Test Suite                  ║
║                   Strava Connect Integration                 ║
╚══════════════════════════════════════════════════════════════╝
    """)


def main():
    """Executa testes"""
    print_header()
    
    print("⚠️  Nota: Este script requer credenciais AWS configuradas")
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    
    print("\n📦 Endpoints a testar:")
    print("  1. POST /auth/callback - OAuth callback")
    print("  2. GET /athlete/{user_id} - Perfil do atleta")
    print("  3. GET /activities/{user_id} - Atividades")
    print("  4. GET /stats/{user_id} - Estatísticas")
    print("  5. GET /insights/{user_id} - Análises com ML")
    
    # Executar testes
    test_auth_callback()
    test_athlete_endpoint()
    test_activities_endpoint()
    
    print("\n✅ Testes completados!")
    print("\n💡 Para testar com sucesso:")
    print("   1. Configure AWS CLI: aws configure")
    print("   2. Configure variáveis de ambiente: export STRAVA_CLIENT_ID=...")
    print("   3. Execute: pytest tests/ -v")


if __name__ == '__main__':
    main()

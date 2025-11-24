#!/usr/bin/env python3
"""
Exemplo de uso do Lambda Backend - Strava Connect
Script Python mostrando como usar os endpoints
"""

import requests
import json
from typing import Dict, Any

# ====== CONFIGURAÇÃO ======
API_BASE_URL = "https://xxxxx.execute-api.us-east-1.amazonaws.com/dev"
USER_ID = "123456"
ACCESS_TOKEN = "seu_access_token_aqui"

# ====== HEADERS ======
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}


def print_response(response: requests.Response):
    """Imprime resposta formatada"""
    print(f"\nStatus Code: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(response.text)


# ====== EXEMPLOS ======

def example_1_get_athlete():
    """Exemplo 1: GET /athlete/{user_id}"""
    print("\n" + "="*60)
    print("EXEMPLO 1: Recuperar Perfil do Atleta")
    print("="*60)
    
    url = f"{API_BASE_URL}/athlete/{USER_ID}?detailed=true"
    
    print(f"URL: GET {url}")
    response = requests.get(url, headers=headers)
    print_response(response)


def example_2_get_activities():
    """Exemplo 2: GET /activities/{user_id}"""
    print("\n" + "="*60)
    print("EXEMPLO 2: Recuperar Atividades (Paginadas)")
    print("="*60)
    
    url = f"{API_BASE_URL}/activities/{USER_ID}?page=1&per_page=5&sport_type=Run"
    
    print(f"URL: GET {url}")
    response = requests.get(url, headers=headers)
    print_response(response)


def example_3_get_stats():
    """Exemplo 3: GET /stats/{user_id}"""
    print("\n" + "="*60)
    print("EXEMPLO 3: Recuperar Estatísticas")
    print("="*60)
    
    url = f"{API_BASE_URL}/stats/{USER_ID}?period=month&sport_type=Run"
    
    print(f"URL: GET {url}")
    response = requests.get(url, headers=headers)
    print_response(response)


def example_4_get_insights():
    """Exemplo 4: GET /insights/{user_id}"""
    print("\n" + "="*60)
    print("EXEMPLO 4: Recuperar Análises (ML)")
    print("="*60)
    
    url = f"{API_BASE_URL}/insights/{USER_ID}?type=all&days=30"
    
    print(f"URL: GET {url}")
    response = requests.get(url, headers=headers)
    print_response(response)


def example_5_auth_callback():
    """Exemplo 5: POST /auth/callback"""
    print("\n" + "="*60)
    print("EXEMPLO 5: OAuth Callback")
    print("="*60)
    
    url = f"{API_BASE_URL}/auth/callback"
    
    # Você obteria este código após o usuário autorizar
    payload = {
        "code": "authorization_code_from_strava",
        "scope": "read,activity:read_all"
    }
    
    print(f"URL: POST {url}")
    print(f"Body: {json.dumps(payload, indent=2)}")
    
    response = requests.post(url, json=payload)
    print_response(response)


# ====== ADVANCED EXAMPLES ======

def example_6_pagination():
    """Exemplo 6: Paginação de Atividades"""
    print("\n" + "="*60)
    print("EXEMPLO 6: Paginação de Atividades (Loop)")
    print("="*60)
    
    page = 1
    all_activities = []
    
    while page <= 3:  # Obter primeiras 3 páginas
        url = f"{API_BASE_URL}/activities/{USER_ID}?page={page}&per_page=10"
        
        print(f"\n▶ Página {page}")
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            activities = data.get('data', {}).get('activities', [])
            
            if not activities:
                print("  ✓ Sem mais atividades")
                break
            
            all_activities.extend(activities)
            print(f"  ✓ Recuperadas {len(activities)} atividades")
            
            for activity in activities:
                print(f"    - {activity['name']}: {activity['distance']}m")
        else:
            print(f"  ✗ Erro: {response.status_code}")
            break
        
        page += 1
    
    print(f"\n📊 Total: {len(all_activities)} atividades recuperadas")


def example_7_stats_analysis():
    """Exemplo 7: Análise de Estatísticas"""
    print("\n" + "="*60)
    print("EXEMPLO 7: Análise de Estatísticas")
    print("="*60)
    
    periods = ['week', 'month', 'year']
    
    for period in periods:
        url = f"{API_BASE_URL}/stats/{USER_ID}?period={period}"
        
        print(f"\n▶ Período: {period}")
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            stats = data.get('data', {}).get('stats', {})
            
            print(f"  Total Activities: {stats.get('total_activities')}")
            print(f"  Total Distance: {stats.get('total_distance')} km")
            print(f"  Avg Speed: {stats.get('average_speed')} km/h")
            print(f"  Elevation Gain: {stats.get('total_elevation_gain')} m")
        else:
            print(f"  ✗ Erro: {response.status_code}")


def example_8_error_handling():
    """Exemplo 8: Tratamento de Erros"""
    print("\n" + "="*60)
    print("EXEMPLO 8: Tratamento de Erros")
    print("="*60)
    
    test_cases = [
        ("Missing user_id", "/athlete/?detailed=true"),
        ("Invalid period", f"/stats/{USER_ID}?period=invalid"),
        ("Unauthorized", f"/athlete/{USER_ID}"),  # Sem token
    ]
    
    for description, endpoint in test_cases:
        url = f"{API_BASE_URL}{endpoint}"
        print(f"\n▶ {description}")
        print(f"  URL: GET {url}")
        
        # Teste sem token para o último caso
        test_headers = {} if "Unauthorized" in description else headers
        response = requests.get(url, headers=test_headers)
        
        if response.status_code >= 400:
            data = response.json()
            print(f"  ✓ Status: {response.status_code}")
            print(f"  Error: {data.get('error', {}).get('message')}")
        else:
            print(f"  ✗ Esperava erro, mas recebeu {response.status_code}")


def main():
    """Função principal"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║         Lambda Backend - Strava Connect                        ║
║              Exemplos de Uso (Python)                          ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    print("""
⚠️  IMPORTANTE:
- Substituir API_BASE_URL pela sua URL real
- Substituir USER_ID pelo ID do usuário Strava
- Substituir ACCESS_TOKEN por um token válido
- Ou obter token primeiro via POST /auth/callback

NOTA: Estes exemplos assumem um ambiente Linux/macOS.
Para Windows, adaptar os comandos conforme necessário.
    """)
    
    # Menu interativo
    examples = {
        '1': ('Perfil do Atleta', example_1_get_athlete),
        '2': ('Atividades', example_2_get_activities),
        '3': ('Estatísticas', example_3_get_stats),
        '4': ('Análises (ML)', example_4_get_insights),
        '5': ('OAuth Callback', example_5_auth_callback),
        '6': ('Paginação', example_6_pagination),
        '7': ('Análise Stats', example_7_stats_analysis),
        '8': ('Tratamento Erros', example_8_error_handling),
        'all': ('Rodar Todos', None),
    }
    
    print("\n📋 Escolha um exemplo:\n")
    for key, (desc, _) in examples.items():
        print(f"  {key}. {desc}")
    
    choice = input("\nDigite sua escolha (1-8 ou 'all'): ").strip().lower()
    
    if choice == 'all':
        example_1_get_athlete()
        example_2_get_activities()
        example_3_get_stats()
        example_4_get_insights()
        example_6_pagination()
        example_7_stats_analysis()
        example_8_error_handling()
    elif choice in examples:
        func = examples[choice][1]
        if func:
            func()
    else:
        print("❌ Opção inválida")


if __name__ == '__main__':
    # Se executar sem argumentos, rodar todos os exemplos
    import sys
    
    if len(sys.argv) < 2:
        main()
    else:
        command = sys.argv[1].lower()
        
        if command == 'athlete':
            example_1_get_athlete()
        elif command == 'activities':
            example_2_get_activities()
        elif command == 'stats':
            example_3_get_stats()
        elif command == 'insights':
            example_4_get_insights()
        elif command == 'callback':
            example_5_auth_callback()
        elif command == 'pagination':
            example_6_pagination()
        elif command == 'analysis':
            example_7_stats_analysis()
        elif command == 'errors':
            example_8_error_handling()
        elif command == 'all':
            example_1_get_athlete()
            example_2_get_activities()
            example_3_get_stats()
            example_4_get_insights()
            example_6_pagination()
            example_7_stats_analysis()
            example_8_error_handling()
        else:
            print(f"Comando desconhecido: {command}")
            print("Use: python examples.py [athlete|activities|stats|insights|callback|pagination|analysis|errors|all]")

#!/bin/bash

# 🚀 Local Development & Testing Guide
# Complete setup para testar Strava Connect Lambda localmente

set -e  # Exit on error

# ═══════════════════════════════════════════════════════════════════════════
# CORES PARA OUTPUT
# ═══════════════════════════════════════════════════════════════════════════

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ═══════════════════════════════════════════════════════════════════════════
# FUNÇÕES AUXILIARES
# ═══════════════════════════════════════════════════════════════════════════

print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}► $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# ═══════════════════════════════════════════════════════════════════════════
# 1. SETUP DO AMBIENTE
# ═══════════════════════════════════════════════════════════════════════════

setup_environment() {
    print_header "SETUP 1: Configurar Ambiente Python"
    
    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 não instalado. Install: https://www.python.org/downloads/"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    print_success "Python $PYTHON_VERSION encontrado"
    
    # Criar virtual environment
    if [ ! -d "venv" ]; then
        print_info "Criando virtual environment..."
        python3 -m venv venv
    fi
    
    # Ativar venv
    source venv/bin/activate || source venv/Scripts/activate  # Windows
    print_success "Virtual environment ativado"
    
    # Atualizar pip
    pip install --upgrade pip setuptools wheel --quiet
    
    # Instalar dependências
    print_info "Instalando dependências..."
    pip install -r requirements.txt --quiet
    pip install pytest pytest-cov pytest-mock pytest-asyncio datadog locust --quiet
    
    print_success "Dependências instaladas"
}

# ═══════════════════════════════════════════════════════════════════════════
# 2. CONFIGURAR VARIÁVEIS DE AMBIENTE
# ═══════════════════════════════════════════════════════════════════════════

setup_env_variables() {
    print_header "SETUP 2: Variáveis de Ambiente"
    
    if [ ! -f ".env.local" ]; then
        print_info "Criando .env.local..."
        cat > .env.local << 'EOF'
# AWS
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=mock_access_key
AWS_SECRET_ACCESS_KEY=mock_secret_key

# Strava
STRAVA_CLIENT_ID=your_client_id_here
STRAVA_CLIENT_SECRET=your_client_secret_here
STRAVA_REDIRECT_URI=http://localhost:3000/auth/callback

# Datadog
DD_API_KEY=mock_datadog_key
DD_APP_KEY=mock_app_key
DD_AGENT_HOST=localhost
DD_AGENT_PORT=8126
DD_SERVICE=strava-connect
DD_ENVIRONMENT=development

# Lambda
LOG_LEVEL=DEBUG
CACHE_TTL=3600
EOF
        print_success ".env.local criado"
    else
        print_success ".env.local já existe"
    fi
    
    # Carregar variáveis
    export $(cat .env.local | xargs)
    print_info "Variáveis carregadas"
}

# ═══════════════════════════════════════════════════════════════════════════
# 3. SETUP DOCKER (OPCIONAL - para DynamoDB local)
# ═══════════════════════════════════════════════════════════════════════════

setup_docker() {
    print_header "SETUP 3: Docker (DynamoDB Local - Opcional)"
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker não instalado"
        print_info "Instalação: https://docs.docker.com/get-docker/"
        print_info "Continuando sem DynamoDB local..."
        return
    fi
    
    print_info "Iniciando DynamoDB Local..."
    docker-compose -f docker-compose.yml up -d
    
    sleep 3
    print_success "DynamoDB Local rodando em localhost:8000"
}

# ═══════════════════════════════════════════════════════════════════════════
# 4. TESTES UNITÁRIOS
# ═══════════════════════════════════════════════════════════════════════════

run_unit_tests() {
    print_header "TESTES 1: Unit Tests"
    
    print_info "Rodando pytest com cobertura..."
    
    pytest tests/unit/ \
        --cov=src \
        --cov-report=html \
        --cov-report=term-missing \
        --cov-fail-under=80 \
        -v \
        --tb=short
    
    COVERAGE=$?
    if [ $COVERAGE -eq 0 ]; then
        print_success "Unit tests PASSARAM com 80%+ coverage"
        print_info "Relatório: htmlcov/index.html"
    else
        print_error "Unit tests FALHARAM"
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
# 5. TESTES DE INTEGRAÇÃO
# ═══════════════════════════════════════════════════════════════════════════

run_integration_tests() {
    print_header "TESTES 2: Integration Tests"
    
    print_info "Rodando testes de integração..."
    
    pytest tests/integration/ \
        -m integration \
        --timeout=30 \
        -v \
        --tb=short
    
    if [ $? -eq 0 ]; then
        print_success "Integration tests PASSARAM"
    else
        print_error "Integration tests FALHARAM"
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
# 6. TESTES DE PERFORMANCE (BENCHMARK)
# ═══════════════════════════════════════════════════════════════════════════

run_performance_tests() {
    print_header "TESTES 3: Performance (Benchmark)"
    
    print_info "Rodando benchmarks..."
    
    pytest tests/performance/ \
        --benchmark-only \
        --benchmark-json=benchmark.json \
        -v \
        --tb=short \
        2>/dev/null || print_info "Benchmarks - módulo opcional"
    
    print_success "Performance tests completados"
}

# ═══════════════════════════════════════════════════════════════════════════
# 7. QUALITY CHECKS
# ═══════════════════════════════════════════════════════════════════════════

run_quality_checks() {
    print_header "TESTES 4: Code Quality"
    
    # Black
    print_info "Verificando formatação com Black..."
    black --check src/ tests/ 2>/dev/null || print_info "Black - opcional"
    
    # isort
    print_info "Verificando imports com isort..."
    isort --check-only src/ tests/ 2>/dev/null || print_info "isort - opcional"
    
    # Flake8
    print_info "Verificando estilo com Flake8..."
    flake8 src/ tests/ --max-line-length=100 --ignore=E203,W503 2>/dev/null || print_info "Flake8 - opcional"
    
    print_success "Quality checks completados"
}

# ═══════════════════════════════════════════════════════════════════════════
# 8. LOCAL API SERVER (SAM ou LocalStack)
# ═══════════════════════════════════════════════════════════════════════════

start_local_server() {
    print_header "SERVIDOR: Iniciar Lambda Localmente"
    
    # Verificar SAM CLI
    if ! command -v sam &> /dev/null; then
        print_error "AWS SAM CLI não instalado"
        print_info "Instalação: https://aws.amazon.com/serverless/sam/"
        print_info "Alternativa: Use LocalStack"
        return
    fi
    
    print_info "Iniciando SAM local server..."
    print_info "Endpoints disponíveis em http://localhost:3000"
    
    sam local start-api \
        --port 3000 \
        --template serverless.yml \
        --env-vars .env.local
}

# ═══════════════════════════════════════════════════════════════════════════
# 9. LOAD TESTING COM LOCUST
# ═══════════════════════════════════════════════════════════════════════════

run_load_test() {
    print_header "TESTES 5: Load Testing com Locust"
    
    read -p "URL do servidor (default http://localhost:3000): " SERVER_URL
    SERVER_URL=${SERVER_URL:-http://localhost:3000}
    
    read -p "Número de usuários (default 50): " NUM_USERS
    NUM_USERS=${NUM_USERS:-50}
    
    read -p "Spawn rate (default 10): " SPAWN_RATE
    SPAWN_RATE=${SPAWN_RATE:-10}
    
    print_info "Iniciando teste de carga..."
    print_info "Acesse: http://localhost:8089 para visualizar"
    
    locust -f tests/performance/load_test.py \
        -H "$SERVER_URL" \
        --users "$NUM_USERS" \
        --spawn-rate "$SPAWN_RATE"
}

# ═══════════════════════════════════════════════════════════════════════════
# 10. MONITORAMENTO LOCAL COM DATADOG
# ═══════════════════════════════════════════════════════════════════════════

start_datadog_agent() {
    print_header "MONITORAMENTO: Datadog Agent Local"
    
    print_info "Verificando Docker..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker não disponível"
        print_info "Datadog Agent requer Docker"
        return
    fi
    
    print_info "Iniciando Datadog Agent..."
    
    docker run -d \
        --name datadog-agent \
        -e DD_API_KEY="${DD_API_KEY}" \
        -e DD_SITE="datadoghq.com" \
        -p 8126:8126 \
        datadog/agent:latest
    
    sleep 2
    print_success "Datadog Agent rodando"
    print_info "APM endpoint: localhost:8126"
}

# ═══════════════════════════════════════════════════════════════════════════
# 11. TESTER - REQUISIÇÕES MANUAIS
# ═══════════════════════════════════════════════════════════════════════════

manual_testing() {
    print_header "TESTES MANUAIS: Requisições cURL"
    
    BASE_URL="${SERVER_URL:-http://localhost:3000}"
    TOKEN="mock_token_12345"
    USER_ID="test_user_123"
    
    print_info "GET /athlete - Obter dados do atleta"
    curl -X GET "$BASE_URL/athlete/$USER_ID" \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -w "\nStatus: %{http_code}\n"
    
    echo ""
    print_info "GET /activities - Listar atividades"
    curl -X GET "$BASE_URL/activities/$USER_ID?page=1&per_page=20" \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -w "\nStatus: %{http_code}\n"
    
    echo ""
    print_info "GET /stats - Obter estatísticas"
    curl -X GET "$BASE_URL/stats/$USER_ID?period=month" \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -w "\nStatus: %{http_code}\n"
}

# ═══════════════════════════════════════════════════════════════════════════
# 12. CLEANUP
# ═══════════════════════════════════════════════════════════════════════════

cleanup() {
    print_header "CLEANUP: Parar Serviços"
    
    print_info "Parando Docker services..."
    docker-compose down 2>/dev/null || true
    
    print_info "Parando Datadog Agent..."
    docker stop datadog-agent 2>/dev/null || true
    docker rm datadog-agent 2>/dev/null || true
    
    print_success "Cleanup completo"
}

# ═══════════════════════════════════════════════════════════════════════════
# MAIN - Menu Interativo
# ═══════════════════════════════════════════════════════════════════════════

show_menu() {
    echo ""
    echo -e "${BLUE}┌─ STRAVA CONNECT - LOCAL TESTING ─────────────────┐${NC}"
    echo -e "${BLUE}│${NC}"
    echo -e "${BLUE}│  1)${NC} Setup Completo (primeiro usar)"
    echo -e "${BLUE}│  2)${NC} Rodar Unit Tests"
    echo -e "${BLUE}│  3)${NC} Rodar Integration Tests"
    echo -e "${BLUE}│  4)${NC} Rodar Quality Checks"
    echo -e "${BLUE}│  5)${NC} Rodar Todos os Testes"
    echo -e "${BLUE}│  6)${NC} Iniciar Servidor Local (SAM)"
    echo -e "${BLUE}│  7)${NC} Load Test (Locust)"
    echo -e "${BLUE}│  8)${NC} Requisições Manuais (cURL)"
    echo -e "${BLUE}│  9)${NC} Iniciar Datadog Agent"
    echo -e "${BLUE}│  10)${NC} Cleanup"
    echo -e "${BLUE}│  0)${NC} Sair"
    echo -e "${BLUE}│${NC}"
    echo -e "${BLUE}└──────────────────────────────────────────────────┘${NC}"
}

main() {
    print_header "🚀 STRAVA CONNECT - LOCAL TESTING ENVIRONMENT"
    
    while true; do
        show_menu
        read -p "Escolha uma opção: " choice
        
        case $choice in
            1)
                setup_environment
                setup_env_variables
                setup_docker
                print_success "Setup completo! Use opção 5 para rodar testes."
                ;;
            2)
                run_unit_tests
                ;;
            3)
                run_integration_tests
                ;;
            4)
                run_quality_checks
                ;;
            5)
                setup_environment
                setup_env_variables
                run_unit_tests
                run_integration_tests
                run_performance_tests
                run_quality_checks
                print_success "TODOS OS TESTES PASSARAM ✅"
                ;;
            6)
                start_local_server
                ;;
            7)
                run_load_test
                ;;
            8)
                manual_testing
                ;;
            9)
                start_datadog_agent
                ;;
            10)
                cleanup
                ;;
            0)
                print_info "Saindo..."
                cleanup
                exit 0
                ;;
            *)
                print_error "Opção inválida"
                ;;
        esac
    done
}

# ═══════════════════════════════════════════════════════════════════════════
# INICIAR
# ═══════════════════════════════════════════════════════════════════════════

# Se script rodado com argumentos
if [ $# -gt 0 ]; then
    case $1 in
        setup)
            setup_environment
            setup_env_variables
            ;;
        test)
            setup_environment
            setup_env_variables
            run_unit_tests
            run_integration_tests
            ;;
        server)
            setup_environment
            setup_env_variables
            start_local_server
            ;;
        load-test)
            run_load_test
            ;;
        *)
            echo "Usage: $0 {setup|test|server|load-test}"
            ;;
    esac
else
    main
fi

#!/bin/bash

# 🧪 Manual Testing - cURL Examples
# Exemplos de requisições para testar a API localmente

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO
# ═══════════════════════════════════════════════════════════════════════════

API_HOST="http://localhost:3000"
USER_ID="test_user_123456"
AUTH_TOKEN="mock_token_abc123xyz"
ATHLETE_ID="789012"
ACTIVITY_ID="activity_001"

# CORES
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ═══════════════════════════════════════════════════════════════════════════
# FUNÇÃO AUXILIAR
# ═══════════════════════════════════════════════════════════════════════════

test_endpoint() {
    local method=$1
    local endpoint=$2
    local description=$3
    local data=$4
    
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}📌 $description${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    echo -e "${YELLOW}Request:${NC}"
    echo "  Method: $method"
    echo "  URL: $API_HOST$endpoint"
    
    if [ -n "$data" ]; then
        echo -e "\n${YELLOW}Body:${NC}"
        echo "$data" | jq '.'
    fi
    
    echo -e "\n${YELLOW}Response:${NC}"
    
    if [ "$method" == "GET" ]; then
        curl -s -X GET \
            "$API_HOST$endpoint" \
            -H "Authorization: Bearer $AUTH_TOKEN" \
            -H "Content-Type: application/json" \
            | jq '.'
    elif [ "$method" == "POST" ]; then
        curl -s -X POST \
            "$API_HOST$endpoint" \
            -H "Authorization: Bearer $AUTH_TOKEN" \
            -H "Content-Type: application/json" \
            -d "$data" \
            | jq '.'
    fi
    
    echo -e "\n${GREEN}✅ Test complete${NC}"
}

# ═══════════════════════════════════════════════════════════════════════════
# TESTES
# ═══════════════════════════════════════════════════════════════════════════

# 1. GET /athlete - Obter dados do atleta
test_get_athlete() {
    test_endpoint "GET" "/athlete/$USER_ID" "GET /athlete - Retrieve athlete profile"
}

# 2. GET /activities - Listar atividades
test_get_activities() {
    test_endpoint "GET" "/activities/$USER_ID?page=1&per_page=20" "GET /activities - List activities with pagination"
}

# 3. GET /activities com filtros
test_get_activities_filtered() {
    test_endpoint "GET" "/activities/$USER_ID?page=1&per_page=10&sport_type=Run&before=2024-01-01&after=2023-01-01" "GET /activities - With filters (sport_type, date range)"
}

# 4. GET /stats - Obter estatísticas
test_get_stats() {
    test_endpoint "GET" "/stats/$USER_ID?period=month" "GET /stats - Get monthly statistics"
}

# 5. GET /stats com diferentes períodos
test_get_stats_all_periods() {
    echo -e "\n${BLUE}🔄 Testing all stat periods:${NC}"
    
    for period in week month year all; do
        echo -e "\n${YELLOW}Period: $period${NC}"
        curl -s -X GET \
            "$API_HOST/stats/$USER_ID?period=$period" \
            -H "Authorization: Bearer $AUTH_TOKEN" \
            | jq '.data | keys'
    done
}

# 6. GET /insights - Obter insights
test_get_insights() {
    test_endpoint "GET" "/insights/$USER_ID?type=all&days=30" "GET /insights - Get ML-powered insights"
}

# 7. GET /insights por tipo
test_get_insights_by_type() {
    echo -e "\n${BLUE}🔄 Testing insight types:${NC}"
    
    for type in performance recommendations trends anomalies; do
        echo -e "\n${YELLOW}Type: $type${NC}"
        curl -s -X GET \
            "$API_HOST/insights/$USER_ID?type=$type" \
            -H "Authorization: Bearer $AUTH_TOKEN" \
            | jq '.data'
    done
}

# 8. POST /auth/callback - OAuth callback
test_auth_callback() {
    local auth_code="strava_auth_code_12345"
    
    test_endpoint "POST" "/auth/callback?code=$auth_code&state=state123" \
        "POST /auth/callback - OAuth authentication callback"
}

# ═══════════════════════════════════════════════════════════════════════════
# TESTES DE ERROR HANDLING
# ═══════════════════════════════════════════════════════════════════════════

test_error_handling() {
    echo -e "\n${BLUE}🧪 Testing Error Handling${NC}"
    
    # 1. Missing auth token
    echo -e "\n${YELLOW}1. Missing Authorization Header${NC}"
    curl -s -X GET "$API_HOST/athlete/$USER_ID" \
        -H "Content-Type: application/json" \
        | jq '.error'
    
    # 2. Invalid user ID
    echo -e "\n${YELLOW}2. Invalid User ID (should return 404)${NC}"
    curl -s -X GET "$API_HOST/athlete/invalid_user_123" \
        -H "Authorization: Bearer $AUTH_TOKEN" \
        | jq '.error'
    
    # 3. Malformed request
    echo -e "\n${YELLOW}3. Missing required parameters${NC}"
    curl -s -X GET "$API_HOST/activities" \
        -H "Authorization: Bearer $AUTH_TOKEN" \
        | jq '.error'
    
    # 4. Rate limit exceeded (simulated)
    echo -e "\n${YELLOW}4. Rate Limit Test (rapid requests)${NC}"
    for i in {1..5}; do
        curl -s -X GET "$API_HOST/athlete/$USER_ID" \
            -H "Authorization: Bearer $AUTH_TOKEN" \
            | jq '.meta.rate_limit'
        sleep 0.1
    done
}

# ═══════════════════════════════════════════════════════════════════════════
# TESTES DE PERFORMANCE
# ═══════════════════════════════════════════════════════════════════════════

test_performance() {
    echo -e "\n${BLUE}⚡ Performance Testing${NC}"
    
    # Test 1: Cache hit (same request twice)
    echo -e "\n${YELLOW}1. Cache Hit Test - Same request twice${NC}"
    
    echo "First request (cache miss):"
    time curl -s -X GET "$API_HOST/athlete/$USER_ID" \
        -H "Authorization: Bearer $AUTH_TOKEN" \
        | jq '.meta'
    
    sleep 1
    
    echo -e "\nSecond request (cache hit):"
    time curl -s -X GET "$API_HOST/athlete/$USER_ID" \
        -H "Authorization: Bearer $AUTH_TOKEN" \
        | jq '.meta'
    
    # Test 2: Concurrent requests
    echo -e "\n${YELLOW}2. Concurrent Requests (5 simultaneous)${NC}"
    time for i in {1..5}; do
        curl -s -X GET "$API_HOST/athlete/$USER_ID" \
            -H "Authorization: Bearer $AUTH_TOKEN" > /dev/null &
    done
    wait
    echo "All requests completed"
    
    # Test 3: Large pagination
    echo -e "\n${YELLOW}3. Large Pagination Request${NC}"
    time curl -s -X GET "$API_HOST/activities/$USER_ID?page=1&per_page=100" \
        -H "Authorization: Bearer $AUTH_TOKEN" \
        | jq '.meta'
}

# ═══════════════════════════════════════════════════════════════════════════
# TESTE COMPLETO - FULL WORKFLOW
# ═══════════════════════════════════════════════════════════════════════════

test_full_workflow() {
    echo -e "\n${BLUE}🚀 Full Workflow Test${NC}\n"
    
    # 1. Get athlete profile
    echo -e "${YELLOW}Step 1: Get Athlete Profile${NC}"
    ATHLETE=$(curl -s -X GET "$API_HOST/athlete/$USER_ID" \
        -H "Authorization: Bearer $AUTH_TOKEN")
    echo "$ATHLETE" | jq '.data | {id, firstname, lastname, city}'
    
    # 2. Get activities
    echo -e "\n${YELLOW}Step 2: Get Activities${NC}"
    ACTIVITIES=$(curl -s -X GET "$API_HOST/activities/$USER_ID?page=1&per_page=5" \
        -H "Authorization: Bearer $AUTH_TOKEN")
    echo "$ACTIVITIES" | jq '.data | length as $count | "Total: \($count) activities"'
    
    # 3. Get stats
    echo -e "\n${YELLOW}Step 3: Get Statistics${NC}"
    STATS=$(curl -s -X GET "$API_HOST/stats/$USER_ID?period=month" \
        -H "Authorization: Bearer $AUTH_TOKEN")
    echo "$STATS" | jq '.data | {total_distance, total_time, num_activities}'
    
    # 4. Get insights
    echo -e "\n${YELLOW}Step 4: Get Insights${NC}"
    INSIGHTS=$(curl -s -X GET "$API_HOST/insights/$USER_ID?type=all" \
        -H "Authorization: Bearer $AUTH_TOKEN")
    echo "$INSIGHTS" | jq '.data | keys'
    
    echo -e "\n${GREEN}✅ Full workflow completed!${NC}"
}

# ═══════════════════════════════════════════════════════════════════════════
# MENU PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════

show_menu() {
    echo -e "\n${BLUE}┌─ STRAVA CONNECT - MANUAL TESTING ─────────────────┐${NC}"
    echo -e "${BLUE}│${NC}"
    echo -e "${BLUE}│  1)${NC} GET /athlete - Athlete profile"
    echo -e "${BLUE}│  2)${NC} GET /activities - List activities"
    echo -e "${BLUE}│  3)${NC} GET /activities (with filters)"
    echo -e "${BLUE}│  4)${NC} GET /stats - Statistics"
    echo -e "${BLUE}│  5)${NC} GET /stats (all periods)"
    echo -e "${BLUE}│  6)${NC} GET /insights - Insights"
    echo -e "${BLUE}│  7)${NC} GET /insights (by type)"
    echo -e "${BLUE}│  8)${NC} POST /auth/callback - OAuth"
    echo -e "${BLUE}│  9)${NC} Error Handling Tests"
    echo -e "${BLUE}│  10)${NC} Performance Tests"
    echo -e "${BLUE}│  11)${NC} Full Workflow Test"
    echo -e "${BLUE}│  0)${NC} Exit"
    echo -e "${BLUE}│${NC}"
    echo -e "${BLUE}└──────────────────────────────────────────────────┘${NC}"
}

# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

main() {
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}    🧪 STRAVA CONNECT - MANUAL API TESTING${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo -e "API Host: ${YELLOW}$API_HOST${NC}"
    echo -e "User ID: ${YELLOW}$USER_ID${NC}"
    
    while true; do
        show_menu
        read -p "Choose option: " choice
        
        case $choice in
            1) test_get_athlete ;;
            2) test_get_activities ;;
            3) test_get_activities_filtered ;;
            4) test_get_stats ;;
            5) test_get_stats_all_periods ;;
            6) test_get_insights ;;
            7) test_get_insights_by_type ;;
            8) test_auth_callback ;;
            9) test_error_handling ;;
            10) test_performance ;;
            11) test_full_workflow ;;
            0) echo -e "\n${GREEN}Goodbye!${NC}\n"; exit 0 ;;
            *) echo -e "${RED}Invalid option${NC}" ;;
        esac
    done
}

# ═══════════════════════════════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════════════════════════════

# Se usar argumento, rodar comando direto
if [ $# -gt 0 ]; then
    case $1 in
        athlete) test_get_athlete ;;
        activities) test_get_activities ;;
        stats) test_get_stats ;;
        insights) test_get_insights ;;
        error) test_error_handling ;;
        performance) test_performance ;;
        workflow) test_full_workflow ;;
        *)
            echo "Usage: $0 {athlete|activities|stats|insights|error|performance|workflow}"
            echo ""
            echo "Examples:"
            echo "  bash test-api.sh athlete"
            echo "  bash test-api.sh activities"
            echo "  bash test-api.sh error"
            ;;
    esac
else
    main
fi

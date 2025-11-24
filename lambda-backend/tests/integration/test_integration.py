"""
Testes de Integração para Strava API
Marca: @integration
"""
import pytest
import time
from unittest.mock import patch, MagicMock
import requests
from strava_client import StravaClient


@pytest.mark.integration
class TestStravaAPIIntegration:
    """Testes de integração com API Strava"""
    
    @pytest.mark.skip(reason="Requer credenciais reais de Strava")
    def test_real_auth_flow(self, client_credentials):
        """Teste: Fluxo real de autenticação (requer manualmente)"""
        client = StravaClient(
            client_id=client_credentials["client_id"],
            client_secret=client_credentials["client_secret"]
        )
        
        # 1. Obter URL de autorização
        auth_url, state = client.get_authorization_url(
            redirect_uri="http://localhost:8080/callback"
        )
        
        assert "https://www.strava.com/oauth/authorize" in auth_url
        assert state is not None
        
        # 2. Usuário autoriza (manualmente via browser)
        # ... código de autorização recebido ...
        
        # 3. Trocar código por token
        # authorization_code = "received_from_strava"
        # tokens = client.get_access_token(authorization_code, "http://localhost:8080/callback")
        # assert "access_token" in tokens
    
    @patch('requests.request')
    def test_get_athlete_with_cache(self, mock_request, strava_client, mock_athlete_response):
        """Teste: obter atleta com cache funciona"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {
            "X-RateLimit-Limit": "600",
            "X-RateLimit-Reset": str(int(time.time()) + 3600)
        }
        mock_response.json.return_value = mock_athlete_response
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        # Primeira requisição - vai fazer HTTP
        result1 = strava_client.get_athlete()
        assert result1["id"] == 123456
        
        # Segunda requisição - deve vir do cache
        assert mock_request.call_count == 1
        result2 = strava_client.get_athlete()
        assert result2["id"] == 123456
        
        # Não deve fazer nova requisição (ainda 1)
        assert mock_request.call_count == 1
    
    @patch('requests.request')
    def test_full_workflow(self, mock_request, strava_client, mock_athlete_response, mock_activities_response, mock_stats_response):
        """Teste: workflow completo (atleta → atividades → stats)"""
        
        # Setup mock responses
        def mock_request_side_effect(*args, **kwargs):
            url = args[1] if len(args) > 1 else kwargs.get('url', '')
            
            response = MagicMock()
            response.status_code = 200
            response.headers = {
                "X-RateLimit-Limit": "600",
                "X-RateLimit-Reset": str(int(time.time()) + 3600)
            }
            response.raise_for_status.return_value = None
            
            if "/athlete/activities" in url:
                response.json.return_value = mock_activities_response
            elif "/stats" in url:
                response.json.return_value = mock_stats_response
            else:
                response.json.return_value = mock_athlete_response
            
            return response
        
        mock_request.side_effect = mock_request_side_effect
        
        # 1. Obter dados do atleta
        athlete = strava_client.get_athlete()
        assert athlete["id"] == 123456
        
        # 2. Obter atividades
        activities = strava_client.get_activities()
        assert len(activities) == 2
        assert activities[0]["type"] == "Run"
        assert activities[1]["type"] == "Ride"
        
        # 3. Obter estatísticas
        stats = strava_client.get_athlete_stats(athlete_id=123456)
        assert "all_ride_totals" in stats
        assert "all_run_totals" in stats
        
        # Verificar que foram 3 requisições HTTP
        assert mock_request.call_count == 3


@pytest.mark.integration
class TestCachePerformance:
    """Testes de performance do cache"""
    
    @patch('requests.request')
    def test_cache_reduces_requests(self, mock_request, strava_client, mock_athlete_response):
        """Teste: cache reduz número de requisições"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {
            "X-RateLimit-Limit": "600",
            "X-RateLimit-Reset": str(int(time.time()) + 3600)
        }
        mock_response.json.return_value = mock_athlete_response
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        # Fazer 10 requisições
        for i in range(10):
            strava_client.get_athlete()
        
        # Deve ter feito apenas 1 requisição HTTP real
        assert mock_request.call_count == 1
    
    @patch('requests.request')
    def test_cache_expiration(self, mock_request, strava_client, mock_athlete_response):
        """Teste: cache expira após TTL"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {
            "X-RateLimit-Limit": "600",
            "X-RateLimit-Reset": str(int(time.time()) + 3600)
        }
        mock_response.json.return_value = mock_athlete_response
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        # Primeira requisição
        strava_client.get_athlete()
        assert mock_request.call_count == 1
        
        # Simular expiração de cache
        strava_client._cache_ttl = 1  # 1 segundo
        time.sleep(1.1)  # Aguardar expiração
        
        # Segunda requisição deve fazer nova chamada HTTP
        strava_client.get_athlete()
        assert mock_request.call_count == 2


@pytest.mark.integration
class TestRateLimitHandling:
    """Testes de tratamento de rate limiting"""
    
    @patch('requests.request')
    @patch('time.sleep')
    def test_rate_limit_handling(self, mock_sleep, mock_request, strava_client):
        """Teste: tratar rate limit corretamente"""
        future_time = int(time.time()) + 10
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {
            "X-RateLimit-Limit": "600",
            "X-RateLimit-Reset": str(future_time)
        }
        mock_response.json.return_value = {"id": 123456}
        mock_response.raise_for_status.return_value = None
        
        mock_request.return_value = mock_response
        
        # Configurar rate limit como se estivesse atingido
        strava_client._rate_limit_reset = time.time() + 5
        
        # Fazer requisição
        strava_client.get_athlete()
        
        # Deve ter aguardado
        assert mock_sleep.called


@pytest.mark.integration
class TestTokenRefresh:
    """Testes de renovação de token"""
    
    @patch('requests.post')
    def test_token_refresh_flow(self, mock_post, strava_client):
        """Teste: Fluxo de renovação de token"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",
            "expires_at": int(time.time()) + 21600,
            "token_type": "Bearer"
        }
        mock_post.return_value = mock_response
        
        result = strava_client.refresh_access_token("old_refresh_token")
        
        assert result["access_token"] == "new_access_token"
        assert strava_client.access_token == "new_access_token"


@pytest.mark.integration
class TestErrorRecovery:
    """Testes de recuperação de erros"""
    
    @patch('requests.request')
    def test_retry_on_network_error(self, mock_request, strava_client):
        """Teste: não fazer retry automático (deixar para o client)"""
        mock_request.side_effect = requests.exceptions.ConnectionError("Network error")
        
        with pytest.raises(requests.exceptions.ConnectionError):
            strava_client.get_athlete()
    
    @patch('requests.request')
    def test_handle_invalid_json_response(self, mock_request, strava_client):
        """Teste: tratamento de JSON inválido"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        with pytest.raises(ValueError):
            strava_client.get_athlete()

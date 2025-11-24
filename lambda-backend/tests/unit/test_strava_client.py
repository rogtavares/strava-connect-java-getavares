"""
Testes unitários para StravaClient
Cobertura: 85%+
"""
import pytest
import time
from unittest.mock import Mock, patch, MagicMock
import requests
from strava_client import StravaClient


class TestStravaClientInit:
    """Testes de inicialização do cliente"""
    
    def test_init_with_all_parameters(self, client_credentials):
        """Teste: inicializar com todos os parâmetros"""
        client = StravaClient(
            client_id=client_credentials["client_id"],
            client_secret=client_credentials["client_secret"],
            access_token=client_credentials["access_token"]
        )
        
        assert client.client_id == client_credentials["client_id"]
        assert client.client_secret == client_credentials["client_secret"]
        assert client.access_token == client_credentials["access_token"]
        assert client._cache == {}
        assert client._cache_ttl == 300
    
    def test_init_without_access_token(self, client_credentials):
        """Teste: inicializar sem token de acesso"""
        client = StravaClient(
            client_id=client_credentials["client_id"],
            client_secret=client_credentials["client_secret"]
        )
        
        assert client.access_token is None
        assert client._rate_limit_remaining is None


class TestCacheKey:
    """Testes de geração de chave de cache"""
    
    def test_cache_key_generation(self, strava_client):
        """Teste: gerar chave de cache"""
        key1 = strava_client._cache_key("GET", "/athlete")
        key2 = strava_client._cache_key("GET", "/athlete")
        
        assert key1 == key2
        assert "GET" in key1
        assert "athlete" in key1
    
    def test_cache_key_different_params(self, strava_client):
        """Teste: chaves diferentes para parâmetros diferentes"""
        key1 = strava_client._cache_key("GET", "/activities", page=1)
        key2 = strava_client._cache_key("GET", "/activities", page=2)
        
        assert key1 != key2
    
    def test_cache_key_order_independent(self, strava_client):
        """Teste: ordem de parâmetros não importa"""
        key1 = strava_client._cache_key("GET", "/endpoint", a=1, b=2)
        key2 = strava_client._cache_key("GET", "/endpoint", b=2, a=1)
        
        assert key1 == key2


class TestCacheValidation:
    """Testes de validação de cache"""
    
    def test_cache_is_valid(self, strava_client):
        """Teste: cache válido"""
        key = "test_key"
        data = {"test": "data"}
        strava_client._cache[key] = (data, time.time())
        
        assert strava_client._is_cache_valid(key) is True
    
    def test_cache_is_expired(self, strava_client):
        """Teste: cache expirado"""
        key = "test_key"
        data = {"test": "data"}
        old_time = time.time() - strava_client._cache_ttl - 10
        strava_client._cache[key] = (data, old_time)
        
        assert strava_client._is_cache_valid(key) is False
    
    def test_cache_key_not_found(self, strava_client):
        """Teste: chave não encontrada no cache"""
        assert strava_client._is_cache_valid("nonexistent_key") is False
    
    def test_clear_cache(self, strava_client):
        """Teste: limpar cache"""
        strava_client._cache["key1"] = ("data1", time.time())
        strava_client._cache["key2"] = ("data2", time.time())
        
        strava_client.clear_cache()
        
        assert strava_client._cache == {}


class TestRateLimit:
    """Testes de rate limiting"""
    
    def test_rate_limit_not_exceeded(self, strava_client):
        """Teste: rate limit não atingido"""
        strava_client._rate_limit_reset = time.time() - 100
        
        assert strava_client._rate_limit_exceeded() is False
    
    def test_rate_limit_exceeded(self, strava_client):
        """Teste: rate limit atingido"""
        strava_client._rate_limit_reset = time.time() + 100
        
        assert strava_client._rate_limit_exceeded() is True
    
    def test_rate_limit_none(self, strava_client):
        """Teste: rate limit não configurado"""
        strava_client._rate_limit_reset = None
        
        assert strava_client._rate_limit_exceeded() is False


class TestAuthorizationURL:
    """Testes de URL de autorização"""
    
    def test_get_authorization_url_default_scopes(self, strava_client):
        """Teste: obter URL de autorização com escopos padrão"""
        auth_url, state = strava_client.get_authorization_url(
            redirect_uri="http://localhost:8080/callback"
        )
        
        assert "https://www.strava.com/oauth/authorize" in auth_url
        assert strava_client.client_id in auth_url
        assert state is not None
    
    def test_get_authorization_url_custom_scopes(self, strava_client):
        """Teste: obter URL com escopos customizados"""
        scopes = ["read", "activity:read_all", "profile:read_all"]
        auth_url, state = strava_client.get_authorization_url(
            redirect_uri="http://localhost:8080/callback",
            scopes=scopes
        )
        
        assert auth_url is not None
        assert state is not None


class TestGetAccessToken:
    """Testes de obtenção de token de acesso"""
    
    @patch('requests.post')
    def test_get_access_token_success(self, mock_post, strava_client, client_credentials):
        """Teste: obter token com sucesso"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "new_token_12345",
            "refresh_token": "refresh_token_xyz",
            "expires_at": 1234567890,
            "token_type": "Bearer"
        }
        mock_post.return_value = mock_response
        
        result = strava_client.get_access_token(
            code="auth_code_123",
            redirect_uri="http://localhost:8080/callback"
        )
        
        assert result["access_token"] == "new_token_12345"
        assert result["refresh_token"] == "refresh_token_xyz"
        assert strava_client.access_token == "new_token_12345"
    
    @patch('requests.post')
    def test_get_access_token_failure(self, mock_post, strava_client):
        """Teste: falha ao obter token"""
        mock_post.side_effect = requests.exceptions.RequestException("API Error")
        
        with pytest.raises(requests.exceptions.RequestException):
            strava_client.get_access_token(
                code="invalid_code",
                redirect_uri="http://localhost:8080/callback"
            )


class TestRefreshAccessToken:
    """Testes de renovação de token"""
    
    @patch('requests.post')
    def test_refresh_access_token_success(self, mock_post, strava_client):
        """Teste: renovar token com sucesso"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "new_token_after_refresh",
            "refresh_token": "new_refresh_token",
            "expires_at": 9999999999,
            "token_type": "Bearer"
        }
        mock_post.return_value = mock_response
        
        result = strava_client.refresh_access_token("old_refresh_token")
        
        assert result["access_token"] == "new_token_after_refresh"
        assert strava_client.access_token == "new_token_after_refresh"


class TestGetAthlete:
    """Testes para obter dados do atleta"""
    
    @patch('requests.request')
    def test_get_athlete_authenticated(self, mock_request, strava_client, mock_athlete_response):
        """Teste: obter atleta autenticado"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {
            "X-RateLimit-Limit": "600",
            "X-RateLimit-Reset": str(int(time.time()) + 3600)
        }
        mock_response.json.return_value = mock_athlete_response
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        result = strava_client.get_athlete()
        
        assert result["id"] == 123456
        assert result["firstname"] == "Test"
        assert result["lastname"] == "Athlete"
    
    @patch('requests.request')
    def test_get_athlete_specific(self, mock_request, strava_client, mock_athlete_response):
        """Teste: obter atleta específico"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {
            "X-RateLimit-Limit": "600",
            "X-RateLimit-Reset": str(int(time.time()) + 3600)
        }
        mock_response.json.return_value = mock_athlete_response
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        result = strava_client.get_athlete(athlete_id=123456)
        
        assert result["id"] == 123456


class TestGetActivities:
    """Testes para obter atividades"""
    
    @patch('requests.request')
    def test_get_activities_default_params(self, mock_request, strava_client, mock_activities_response):
        """Teste: obter atividades com parâmetros padrão"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {
            "X-RateLimit-Limit": "600",
            "X-RateLimit-Reset": str(int(time.time()) + 3600)
        }
        mock_response.json.return_value = mock_activities_response
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        result = strava_client.get_activities()
        
        assert len(result) == 2
        assert result[0]["name"] == "Morning Run"
        assert result[1]["name"] == "Evening Ride"
    
    @patch('requests.request')
    def test_get_activities_with_pagination(self, mock_request, strava_client, mock_activities_response):
        """Teste: obter atividades com paginação"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {
            "X-RateLimit-Limit": "600",
            "X-RateLimit-Reset": str(int(time.time()) + 3600)
        }
        mock_response.json.return_value = mock_activities_response
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        result = strava_client.get_activities(page=2, per_page=10)
        
        assert len(result) == 2
    
    @patch('requests.request')
    def test_get_activities_with_date_filters(self, mock_request, strava_client, mock_activities_response):
        """Teste: obter atividades com filtro de data"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {
            "X-RateLimit-Limit": "600",
            "X-RateLimit-Reset": str(int(time.time()) + 3600)
        }
        mock_response.json.return_value = mock_activities_response
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        before_timestamp = int(time.time())
        after_timestamp = int(time.time()) - 86400 * 30  # 30 dias atrás
        
        result = strava_client.get_activities(
            before=before_timestamp,
            after=after_timestamp
        )
        
        assert len(result) == 2


class TestGetActivity:
    """Testes para obter detalhes de uma atividade"""
    
    @patch('requests.request')
    def test_get_activity_default(self, mock_request, strava_client):
        """Teste: obter detalhes da atividade"""
        activity_data = {
            "id": 9876543210,
            "name": "Morning Run",
            "type": "Run",
            "distance": 5000,
            "moving_time": 1800
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {
            "X-RateLimit-Limit": "600",
            "X-RateLimit-Reset": str(int(time.time()) + 3600)
        }
        mock_response.json.return_value = activity_data
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        result = strava_client.get_activity(activity_id=9876543210)
        
        assert result["id"] == 9876543210
        assert result["name"] == "Morning Run"


class TestCacheStatistics:
    """Testes para estatísticas de cache"""
    
    def test_get_cache_stats_empty(self, strava_client):
        """Teste: estatísticas com cache vazio"""
        stats = strava_client.get_cache_stats()
        
        assert stats["cache_size"] == 0
        assert stats["cache_ttl"] == 300
        assert stats["total_requests"] == 0
    
    def test_get_cache_stats_with_data(self, strava_client):
        """Teste: estatísticas com dados em cache"""
        strava_client._cache["key1"] = ({"data": "test"}, time.time())
        strava_client._cache["key2"] = ({"data": "test2"}, time.time())
        strava_client._request_count = 5
        strava_client._total_requests = 10
        
        stats = strava_client.get_cache_stats()
        
        assert stats["cache_size"] == 2
        assert stats["total_requests"] == 10


class TestErrorHandling:
    """Testes de tratamento de erros"""
    
    @patch('requests.request')
    def test_http_error_handling(self, mock_request, strava_client):
        """Teste: tratamento de erro HTTP"""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_request.return_value = mock_response
        
        with pytest.raises(requests.exceptions.HTTPError):
            strava_client.get_athlete()
    
    @patch('requests.request')
    def test_timeout_error_handling(self, mock_request, strava_client):
        """Teste: tratamento de timeout"""
        mock_request.side_effect = requests.exceptions.Timeout("Connection timeout")
        
        with pytest.raises(requests.exceptions.Timeout):
            strava_client.get_athlete()
    
    @patch('requests.request')
    def test_connection_error_handling(self, mock_request, strava_client):
        """Teste: tratamento de erro de conexão"""
        mock_request.side_effect = requests.exceptions.ConnectionError("Connection refused")
        
        with pytest.raises(requests.exceptions.ConnectionError):
            strava_client.get_athlete()

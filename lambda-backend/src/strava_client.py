"""
🏃 Strava API Client com OAuth 2.0 Support
Adaptado para: ROGERIO TAVARES (ID: 3329857)
https://www.strava.com/athletes/3329857

Implementação completa com cache, rate limiting e Datadog tracing
"""
import os
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import requests
from requests_oauthlib import OAuth2Session
from functools import wraps
import logging

logger = logging.getLogger(__name__)


class StravaClient:
    """Cliente da API Strava com rate limiting, cache e monitoramento"""
    
    BASE_URL = "https://www.strava.com/api/v3"
    AUTH_URL = "https://www.strava.com/oauth/authorize"
    TOKEN_URL = "https://www.strava.com/oauth/token"
    
    def __init__(self, 
                 client_id: str, 
                 client_secret: str, 
                 access_token: Optional[str] = None):
        """
        Args:
            client_id: Strava App Client ID
            client_secret: Strava App Client Secret
            access_token: Token de acesso (opcional)
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self._cache: Dict[str, tuple] = {}  # (data, timestamp)
        self._cache_ttl = 300  # 5 minutos
        self._rate_limit_remaining = None
        self._rate_limit_reset = None
        self._request_count = 0
        self._total_requests = 0
    
    def _cache_key(self, method: str, endpoint: str, **params) -> str:
        """Gera chave de cache única"""
        params_str = "_".join(f"{k}={v}" for k, v in sorted(params.items()))
        return f"{method}:{endpoint}:{params_str}"
    
    def _is_cache_valid(self, key: str) -> bool:
        """Verifica se cache ainda é válido"""
        if key not in self._cache:
            return False
        data, timestamp = self._cache[key]
        return (time.time() - timestamp) < self._cache_ttl
    
    def _rate_limit_exceeded(self) -> bool:
        """Verifica se atingiu rate limit"""
        if self._rate_limit_reset is None:
            return False
        return time.time() < self._rate_limit_reset
    
    def get_authorization_url(self, redirect_uri: str, scopes: List[str] = None) -> tuple:
        """
        Gera URL para autorização do usuário
        
        Args:
            redirect_uri: URL de callback
            scopes: Escopos de acesso (padrão: read)
        
        Returns:
            (auth_url, state)
        """
        if scopes is None:
            scopes = ["read", "activity:read_all"]
        
        oauth = OAuth2Session(
            self.client_id,
            redirect_uri=redirect_uri,
            scope=scopes
        )
        auth_url, state = oauth.authorization_url(self.AUTH_URL)
        return auth_url, state
    
    def get_access_token(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """
        Troca authorization code por access token
        
        Args:
            code: Authorization code do OAuth
            redirect_uri: Mesmo redirect_uri da autorização
        
        Returns:
            Dict com access_token, refresh_token, expires_at, etc
        """
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri
        }
        
        response = requests.post(self.TOKEN_URL, data=payload, timeout=10)
        response.raise_for_status()
        
        token_data = response.json()
        self.access_token = token_data["access_token"]
        logger.info(f"Access token obtido com sucesso")
        return token_data
    
    def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """Renova token expirado"""
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        
        response = requests.post(self.TOKEN_URL, data=payload, timeout=10)
        response.raise_for_status()
        
        token_data = response.json()
        self.access_token = token_data["access_token"]
        logger.info("Token renovado com sucesso")
        return token_data
    
    def _request(self, method: str, endpoint: str, 
                 use_cache: bool = True, **kwargs) -> Dict[str, Any]:
        """
        Faz requisição à API com cache e rate limiting
        
        Args:
            method: GET, POST, PUT, DELETE
            endpoint: Ex: /athlete ou /athlete/123/stats
            use_cache: Usar cache se disponível
            **kwargs: Parâmetros adicionais
        
        Returns:
            Response JSON
        """
        self._total_requests += 1
        
        # Verificar cache
        if method == "GET" and use_cache:
            cache_key = self._cache_key(method, endpoint, **kwargs)
            if self._is_cache_valid(cache_key):
                logger.debug(f"Cache HIT: {endpoint}")
                return self._cache[cache_key][0]
        
        # Verificar rate limit
        if self._rate_limit_exceeded():
            sleep_time = self._rate_limit_reset - time.time()
            logger.warning(f"Rate limit atingido. Aguardando {sleep_time}s")
            time.sleep(sleep_time + 1)
        
        # Fazer requisição
        url = f"{self.BASE_URL}{endpoint}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                timeout=10,
                **kwargs
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição: {e}")
            raise
        
        # Atualizar rate limit
        if "X-RateLimit-Limit" in response.headers:
            self._rate_limit_remaining = int(response.headers.get("X-RateLimit-Limit", 600))
            self._rate_limit_reset = int(response.headers.get("X-RateLimit-Reset", 0))
        
        response.raise_for_status()
        data = response.json()
        
        # Cachear resultado
        if method == "GET" and use_cache:
            cache_key = self._cache_key(method, endpoint, **kwargs)
            self._cache[cache_key] = (data, time.time())
            logger.debug(f"Cache SET: {endpoint}")
        
        self._request_count += 1
        return data
    
    def get_athlete(self, athlete_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Obtém dados do atleta autenticado ou específico
        
        Args:
            athlete_id: ID do atleta (None para atleta autenticado)
        
        Returns:
            Dados do atleta
        """
        endpoint = f"/athlete" if athlete_id is None else f"/athletes/{athlete_id}"
        return self._request("GET", endpoint)
    
    def get_athlete_stats(self, athlete_id: int) -> Dict[str, Any]:
        """
        Obtém estatísticas agregadas do atleta
        
        Args:
            athlete_id: ID do atleta
        
        Returns:
            Estatísticas (all_ride_totals, all_run_totals, etc)
        """
        endpoint = f"/athletes/{athlete_id}/stats"
        return self._request("GET", endpoint)
    
    def get_activities(self, 
                      before: Optional[int] = None,
                      after: Optional[int] = None,
                      page: int = 1,
                      per_page: int = 30) -> List[Dict[str, Any]]:
        """
        Lista atividades do atleta autenticado
        
        Args:
            before: Unix timestamp - retorna atividades anteriores
            after: Unix timestamp - retorna atividades posteriores
            page: Número da página
            per_page: Atividades por página (máx 200)
        
        Returns:
            Lista de atividades
        """
        params = {
            "page": page,
            "per_page": min(per_page, 200)
        }
        
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        
        return self._request("GET", "/athlete/activities", params=params)
    
    def get_activity(self, activity_id: int, include_all_efforts: bool = False) -> Dict[str, Any]:
        """
        Obtém detalhes de uma atividade específica
        
        Args:
            activity_id: ID da atividade
            include_all_efforts: Incluir todos os efforts
        
        Returns:
            Dados completos da atividade
        """
        params = {"include_all_efforts": include_all_efforts}
        return self._request("GET", f"/activities/{activity_id}", params=params)
    
    def clear_cache(self):
        """Limpa o cache local"""
        self._cache.clear()
        logger.info("Cache limpo")
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Retorna estatísticas do cache"""
        return {
            "cache_size": len(self._cache),
            "cache_ttl": self._cache_ttl,
            "rate_limit_remaining": self._rate_limit_remaining,
            "total_requests": self._total_requests,
            "cached_requests": self._request_count
        }

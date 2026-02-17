"""
API Client Module
Comunicação com Spring Boot e FastAPI
"""

import requests
import streamlit as st
from typing import List, Dict, Any
import logging
from config import STRAVA_API_URL, FASTAPI_URL, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

class StravaAPIClient:
    """Cliente para comunicação com APIs (Spring + FastAPI)"""
    
    def __init__(self):
        self.spring_url = STRAVA_API_URL
        self.fastapi_url = FASTAPI_URL
        self.timeout = REQUEST_TIMEOUT
    
    def get_authorization_url(self) -> str:
        """Obtém URL de autorização OAuth"""
        try:
            response = requests.get(
                f"{self.spring_url}/authorize",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json().get("authorization_url", "")
        except Exception as e:
            logger.error(f"Erro ao obter URL de autorização: {e}")
            st.error("Erro ao conectar com Strava")
            return ""
    
    def exchange_code_for_token(self, code: str) -> bool:
        """Troca código de autorização por token"""
        try:
            response = requests.post(
                f"{self.spring_url}/authorize/callback",
                params={"code": code},
                timeout=self.timeout
            )
            response.raise_for_status()
            st.session_state.authenticated = True
            st.success("✅ Conectado ao Strava!")
            return True
        except Exception as e:
            logger.error(f"Erro ao fazer exchange de código: {e}")
            st.error("Erro ao autenticar")
            return False
    
    def get_activities(self) -> List[Dict[str, Any]]:
        """Busca atividades do usuário"""
        try:
            response = requests.get(
                f"{self.spring_url}/activities/export",
                timeout=self.timeout,
                headers={"Accept": "application/json"}
            )
            response.raise_for_status()
            activities = response.json()
            logger.info(f"Recuperadas {len(activities)} atividades")
            return activities if isinstance(activities, list) else []
        except requests.exceptions.ConnectionError:
            st.error("❌ Spring Boot não está rodando (porta 8080)")
            return []
        except Exception as e:
            logger.error(f"Erro ao buscar atividades: {e}")
            st.error(f"Erro ao buscar atividades: {str(e)}")
            return []
    
    def enrich_activities(self, activities: List[Dict]) -> List[Dict]:
        """Enriquece atividades com dados de weather"""
        if not activities:
            return []
        
        try:
            payload = {"activities": activities}
            response = requests.post(
                f"{self.fastapi_url}/enrich",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            enriched = response.json().get("activities", activities)
            logger.info(f"Enriquecidas {len(enriched)} atividades")
            return enriched
        except requests.exceptions.ConnectionError:
            st.warning("⚠️ FastAPI não está rodando (porta 8000)")
            return activities
        except Exception as e:
            logger.error(f"Erro ao enriquecer atividades: {e}")
            st.warning(f"Usando atividades sem enriquecimento")
            return activities
    
    def get_insights(self, activities: List[Dict]) -> Dict[str, Any]:
        """Gera insights das atividades"""
        if not activities:
            return {}
        
        try:
            payload = {"activities": activities}
            response = requests.post(
                f"{self.fastapi_url}/insights",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            insights = response.json()
            logger.info("Insights gerados com sucesso")
            return insights
        except requests.exceptions.ConnectionError:
            st.warning("⚠️ FastAPI não está rodando")
            return {}
        except Exception as e:
            logger.error(f"Erro ao gerar insights: {e}")
            return {}

@st.cache_resource
def get_api_client() -> StravaAPIClient:
    """Retorna instância única do API client (cached)"""
    return StravaAPIClient()

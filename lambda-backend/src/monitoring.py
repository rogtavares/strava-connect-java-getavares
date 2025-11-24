"""
📊 Datadog Integration & Monitoring
APM tracing, metrics, and dashboards for Strava Connect
"""

import logging
import os
from functools import wraps
from datetime import datetime
from typing import Callable, Any

# Datadog imports
try:
    from ddtrace import tracer, initialize, config
    from ddtrace.profiling import prof
    from datadog import initialize as dd_initialize, api
    DATADOG_AVAILABLE = True
except ImportError:
    DATADOG_AVAILABLE = False
    print("⚠️  Datadog SDK não instalado. Instale: pip install datadog ddtrace")


logger = logging.getLogger(__name__)


class DatadogConfig:
    """Configuração centralizada do Datadog"""
    
    # Environment variables
    AGENT_HOST = os.getenv("DD_AGENT_HOST", "localhost")
    AGENT_PORT = int(os.getenv("DD_AGENT_PORT", "8126"))
    SERVICE_NAME = os.getenv("DD_SERVICE", "strava-connect")
    ENVIRONMENT = os.getenv("DD_ENVIRONMENT", "development")
    VERSION = os.getenv("DD_VERSION", "1.0.0")
    API_KEY = os.getenv("DD_API_KEY", "")
    APP_KEY = os.getenv("DD_APP_KEY", "")
    
    @classmethod
    def initialize(cls):
        """Inicializar Datadog APM"""
        if not DATADOG_AVAILABLE:
            logger.warning("Datadog não disponível")
            return
        
        try:
            # Configurar tracer
            config.env = cls.ENVIRONMENT
            config.version = cls.VERSION
            
            initialize(
                statsd_host=cls.AGENT_HOST,
                statsd_port=cls.AGENT_PORT
            )
            
            # Tracer setup
            tracer.configure(
                hostname=cls.AGENT_HOST,
                port=cls.AGENT_PORT,
                enabled=True
            )
            
            # Start profiler
            prof.start()
            
            logger.info(
                f"✅ Datadog inicializado - "
                f"Service: {cls.SERVICE_NAME}, "
                f"Env: {cls.ENVIRONMENT}"
            )
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar Datadog: {e}")


def datadog_trace(
    operation_name: str,
    tags: dict = None,
    error_callback: Callable = None
):
    """
    Decorator para trace automático com Datadog
    
    Exemplo:
        @datadog_trace("get_athlete", {"user_id": "123"})
        def get_athlete(user_id):
            return {...}
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not DATADOG_AVAILABLE:
                return func(*args, **kwargs)
            
            with tracer.trace(
                operation_name,
                service=DatadogConfig.SERVICE_NAME,
                tags=tags or {}
            ) as span:
                try:
                    # Adicionar informações do contexto
                    span.set_tag("function_name", func.__name__)
                    span.set_tag("environment", DatadogConfig.ENVIRONMENT)
                    span.set_tag("version", DatadogConfig.VERSION)
                    
                    # Executar função
                    result = func(*args, **kwargs)
                    
                    # Marcar sucesso
                    span.set_tag("status", "success")
                    return result
                    
                except Exception as e:
                    # Registrar erro
                    span.set_tag("error", True)
                    span.set_tag("error_type", type(e).__name__)
                    span.set_tag("error_message", str(e))
                    span.log_exception(e)
                    
                    # Callback customizado se fornecido
                    if error_callback:
                        error_callback(e, span)
                    
                    raise
        
        return wrapper
    return decorator


class DatadogMetrics:
    """Gerenciador de métricas customizadas"""
    
    @staticmethod
    def increment(
        metric_name: str,
        value: float = 1,
        tags: dict = None
    ):
        """Incrementar métrica"""
        if not DATADOG_AVAILABLE:
            return
        
        try:
            metric_path = f"strava_connect.{metric_name}"
            dd_tags = [f"{k}:{v}" for k, v in (tags or {}).items()]
            dd_tags.extend([
                f"env:{DatadogConfig.ENVIRONMENT}",
                f"service:{DatadogConfig.SERVICE_NAME}"
            ])
            
            api.Metric.send(
                metric=metric_path,
                points=value,
                type="gauge",
                tags=dd_tags
            )
        except Exception as e:
            logger.error(f"Erro ao enviar métrica {metric_name}: {e}")
    
    @staticmethod
    def timing(metric_name: str, duration_ms: float, tags: dict = None):
        """Enviar métrica de tempo"""
        DatadogMetrics.increment(metric_name, duration_ms, tags)
    
    @staticmethod
    def histogram(
        metric_name: str,
        value: float,
        tags: dict = None
    ):
        """Enviar históograma (distribuição)"""
        if not DATADOG_AVAILABLE:
            return
        
        try:
            api.Metric.send(
                metric=f"strava_connect.{metric_name}",
                points=value,
                type="histogram",
                tags=[f"{k}:{v}" for k, v in (tags or {}).items()]
            )
        except Exception as e:
            logger.error(f"Erro ao enviar histogram {metric_name}: {e}")


class DatadogDashboard:
    """Criar dashboards no Datadog"""
    
    @staticmethod
    def create_monitoring_dashboard():
        """Criar dashboard de monitoramento"""
        if not DATADOG_AVAILABLE or not DatadogConfig.API_KEY:
            logger.warning("Não é possível criar dashboard sem credenciais")
            return
        
        dashboard_config = {
            "title": "Strava Connect - Lambda Monitoring",
            "description": "Performance, errors, and cache metrics",
            "widgets": [
                {
                    "type": "timeseries",
                    "definition": {
                        "title": "Request Latency (P95)",
                        "queries": [
                            {
                                "name": "p95",
                                "data_source": "metrics",
                                "query": "p95:strava_connect.request_duration{*}"
                            }
                        ]
                    }
                },
                {
                    "type": "timeseries",
                    "definition": {
                        "title": "Cache Hit Rate",
                        "queries": [
                            {
                                "name": "hit_rate",
                                "data_source": "metrics",
                                "query": "avg:strava_connect.cache.hit_rate{*}"
                            }
                        ]
                    }
                },
                {
                    "type": "number",
                    "definition": {
                        "title": "Error Rate",
                        "queries": [
                            {
                                "name": "errors",
                                "data_source": "metrics",
                                "query": "sum:strava_connect.errors{*}"
                            }
                        ]
                    }
                }
            ]
        }
        
        try:
            response = api.Dashboard.create(**dashboard_config)
            logger.info(f"✅ Dashboard criado: {response}")
            return response
        except Exception as e:
            logger.error(f"❌ Erro ao criar dashboard: {e}")


class DatadogLogger:
    """Logger integrado com Datadog"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        
        # Handler de eventos para Datadog
        if DATADOG_AVAILABLE:
            try:
                from ddtrace.profiling import enable_event_tracing
                enable_event_tracing()
            except Exception as e:
                logger.debug(f"Event tracing não disponível: {e}")
    
    def log_event(
        self,
        title: str,
        text: str,
        tags: dict = None,
        alert_type: str = "info"
    ):
        """Enviar evento para Datadog"""
        if not DATADOG_AVAILABLE or not DatadogConfig.API_KEY:
            self.logger.info(f"{title}: {text}")
            return
        
        try:
            event_data = {
                "title": title,
                "text": text,
                "alert_type": alert_type,  # "info", "success", "warning", "error"
                "tags": [f"{k}:{v}" for k, v in (tags or {}).items()],
                "timestamp": int(datetime.now().timestamp())
            }
            
            api.Event.create(**event_data)
            self.logger.info(f"✅ Evento enviado: {title}")
        except Exception as e:
            self.logger.error(f"Erro ao enviar evento: {e}")


# Exemplos de uso nos handlers

def example_strava_client_with_datadog():
    """Exemplo: Integrar Datadog no StravaClient"""
    
    code_example = """
    # src/strava_client.py
    
    from monitoring import datadog_trace, DatadogMetrics
    
    class StravaClient:
        
        @datadog_trace("get_athlete", tags={"resource": "athlete"})
        def get_athlete(self, athlete_id=None):
            # Traço automático
            return {...}
        
        @datadog_trace("get_activities", tags={"resource": "activities"})
        def get_activities(self, before=None, after=None, page=1, per_page=30):
            # Métrica customizada
            DatadogMetrics.increment(
                "activities.retrieved",
                per_page,
                tags={"page": page}
            )
            return {...}
        
        @datadog_trace("cache.operations")
        def _is_cache_valid(self, cache_key, ttl):
            valid = self._cache.get(cache_key) is not None
            
            # Enviar métrica de cache
            DatadogMetrics.increment(
                "cache.hit" if valid else "cache.miss"
            )
            
            return valid
    """
    
    return code_example


# Arquivo: docker-compose.yml com Datadog Agent

docker_compose_example = """
version: '3.8'

services:
  # Datadog Agent
  datadog-agent:
    image: datadog/agent:latest
    container_name: datadog-agent
    environment:
      - DD_API_KEY=${DD_API_KEY}
      - DD_SITE=datadoghq.com
      - DD_APM_ENABLED=true
      - DD_LOGS_ENABLED=true
      - DD_PROCESS_AGENT_ENABLED=true
      - DD_ENV=development
      - DD_SERVICE=strava-connect
      - DD_VERSION=1.0.0
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /proc/:/host/proc/:ro
      - /sys/fs/cgroup/:/host/sys/fs/cgroup:ro
    ports:
      - "8126:8126"  # APM
      - "8125:8125"  # StatsD
      - "5000:5000"  # Admin
    networks:
      - strava-network

  # Lambda (local com SAM ou LocalStack)
  lambda:
    build: .
    environment:
      - DD_AGENT_HOST=datadog-agent
      - DD_AGENT_PORT=8126
      - DD_SERVICE=strava-connect
      - DD_ENVIRONMENT=development
      - DD_API_KEY=${DD_API_KEY}
    ports:
      - "3000:3000"
    depends_on:
      - datadog-agent
    networks:
      - strava-network

networks:
  strava-network:
    driver: bridge
"""


# Arquivo: .env.example para Datadog

env_example = """
# Datadog Configuration
DD_API_KEY=your_datadog_api_key_here
DD_APP_KEY=your_datadog_app_key_here
DD_AGENT_HOST=localhost
DD_AGENT_PORT=8126
DD_SERVICE=strava-connect
DD_ENVIRONMENT=development
DD_VERSION=1.0.0

# AWS
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret

# Strava
STRAVA_CLIENT_ID=your_strava_client_id
STRAVA_CLIENT_SECRET=your_strava_secret
"""


if __name__ == "__main__":
    # Inicializar Datadog
    DatadogConfig.initialize()
    
    # Exemplo de uso
    logger = DatadogLogger(__name__)
    
    # Enviar evento
    logger.log_event(
        title="Strava Connect - Deployment",
        text="Lambda backend deployed successfully",
        tags={"version": "1.0.0", "environment": "production"},
        alert_type="success"
    )
    
    # Enviar métrica
    DatadogMetrics.increment(
        "deployment.success",
        tags={"service": "strava-connect"}
    )
    
    print("✅ Datadog integrado com sucesso!")

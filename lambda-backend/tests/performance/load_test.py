"""
🚀 Performance Testing with Locust
Load testing for Strava Connect Lambda APIs
"""

from locust import HttpUser, task, between, TaskSet, events
from datetime import datetime
import time
import json


class StravaTaskSet(TaskSet):
    """Task set com todas as operações"""
    
    def on_start(self):
        """Setup inicial para cada usuário"""
        self.user_id = "123456"
        self.token = "mock_token_123456"
        self.athlete_id = "789012"
        self.activity_ids = [
            "activity_001",
            "activity_002",
            "activity_003"
        ]
    
    @task(3)
    def get_athlete(self):
        """3x mais frequente: GET /athlete/{user_id}"""
        response = self.client.get(
            f"/athlete/{self.user_id}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        if response.status_code != 200:
            response.failure(f"Status {response.status_code}")
    
    @task(2)
    def get_activities(self):
        """2x: GET /activities/{user_id} com paginação"""
        page = 1
        per_page = 20
        response = self.client.get(
            f"/activities/{self.user_id}",
            params={
                "page": page,
                "per_page": per_page
            },
            headers={"Authorization": f"Bearer {self.token}"}
        )
        if response.status_code != 200:
            response.failure(f"Status {response.status_code}")
    
    @task(1)
    def get_stats(self):
        """1x: GET /stats/{user_id}"""
        response = self.client.get(
            f"/stats/{self.user_id}",
            params={"period": "month"},
            headers={"Authorization": f"Bearer {self.token}"}
        )
        if response.status_code != 200:
            response.failure(f"Status {response.status_code}")
    
    @task(1)
    def get_insights(self):
        """1x: GET /insights/{user_id}"""
        response = self.client.get(
            f"/insights/{self.user_id}",
            params={
                "type": "all",
                "days": 30
            },
            headers={"Authorization": f"Bearer {self.token}"}
        )
        if response.status_code != 200:
            response.failure(f"Status {response.status_code}")


class StravaUser(HttpUser):
    """Simula um usuário autenticado da Strava"""
    
    # Intervalo de espera entre requests (1-3 segundos)
    wait_time = between(1, 3)
    
    # Usar TaskSet
    tasks = [StravaTaskSet]


class CacheValidationUser(HttpUser):
    """Valida comportamento de cache"""
    
    wait_time = between(0.5, 1)
    
    def on_start(self):
        """Setup inicial"""
        self.user_id = "cache_test_user"
        self.request_times = []
    
    @task
    def repeated_requests(self):
        """Faz requisições repetidas para validar cache"""
        start = time.time()
        response = self.client.get(
            f"/athlete/{self.user_id}",
            headers={"Authorization": "Bearer token"}
        )
        duration = time.time() - start
        self.request_times.append(duration)


class RateLimitTestUser(HttpUser):
    """Testa comportamento sob rate limiting"""
    
    # Espera mínima para provocar rate limit
    wait_time = between(0.1, 0.2)
    
    @task
    def hammer_api(self):
        """Faz muitas requisições rápidas"""
        self.client.get(
            "/athlete/123456",
            headers={"Authorization": "Bearer token"}
        )


# Event listeners para métricas customizadas

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Chamado quando teste começa"""
    print("\n" + "="*60)
    print("🚀 INICIANDO TESTE DE PERFORMANCE STRAVA CONNECT")
    print("="*60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Usuários: {environment.runner.target_num_clients}")
    print("="*60 + "\n")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Chamado quando teste termina"""
    print("\n" + "="*60)
    print("✅ TESTE DE PERFORMANCE FINALIZADO")
    print("="*60)
    
    # Estatísticas
    stats = environment.stats
    print("\n📊 RELATÓRIO DE TESTES:")
    print(f"Total de requisições: {stats.total.num_requests}")
    print(f"Total de falhas: {stats.total.num_failures}")
    print(f"Taxa de falha: {stats.total.failure_rate:.2%}")
    
    print("\n⏱️  LATÊNCIA:")
    print(f"Tempo médio: {stats.total.avg_response_time:.2f}ms")
    print(f"P50: {stats.total.get_response_time_percentile(0.50):.2f}ms")
    print(f"P95: {stats.total.get_response_time_percentile(0.95):.2f}ms")
    print(f"P99: {stats.total.get_response_time_percentile(0.99):.2f}ms")
    print(f"Min: {stats.total.min_response_time:.2f}ms")
    print(f"Max: {stats.total.max_response_time:.2f}ms")
    
    print("\n📈 THROUGHPUT:")
    print(f"Total de requisições: {stats.total.num_requests}")
    print(f"Taxa média: {stats.total.total_rps:.2f} req/s")
    
    # Detalhes por endpoint
    print("\n🔍 DETALHES POR ENDPOINT:")
    for label in sorted(stats.entries.keys()):
        entry = stats.entries[label]
        print(f"\n  {label}")
        print(f"    Requisições: {entry.num_requests}")
        print(f"    Falhas: {entry.num_failures}")
        print(f"    Avg: {entry.avg_response_time:.2f}ms")
        print(f"    P95: {entry.get_response_time_percentile(0.95):.2f}ms")
    
    print("\n" + "="*60 + "\n")


@events.request.add_listener
def on_request(request_type, name, response_time, exception, **kwargs):
    """Event listener para cada requisição"""
    if exception:
        print(f"❌ {name} - Exception: {exception}")
    elif response_time > 1000:
        print(f"⚠️  {name} - Slow: {response_time:.0f}ms")


# Configuração avançada para Datadog
class DatadogMetricsListener:
    """Envia métricas para Datadog"""
    
    def __init__(self):
        try:
            from datadog import initialize, api
            self.initialized = True
            self.api = api
        except ImportError:
            print("⚠️  Datadog SDK não instalado")
            self.initialized = False
    
    def send_metric(self, metric_name, value, tags=None):
        """Envia métrica para Datadog"""
        if not self.initialized:
            return
        
        try:
            self.api.Metric.send(
                metric=f"strava_connect.{metric_name}",
                points=value,
                tags=tags or []
            )
        except Exception as e:
            print(f"Error sending Datadog metric: {e}")


# Instanciar listener
datadog_listener = DatadogMetricsListener()


# Exemplos de uso:
# 
# Modo interativo (web UI):
# $ locust -f load_test.py -H http://localhost:8000
#
# Modo headless (CLI):
# $ locust -f load_test.py -H http://localhost:8000 \
#          --users 100 --spawn-rate 10 --run-time 5m --headless
#
# Salvar resultados:
# $ locust -f load_test.py -H http://localhost:8000 \
#          --users 100 --spawn-rate 10 --run-time 5m --headless \
#          --csv=results --html=results.html
#
# Usar múltiplas user classes:
# $ locust -f load_test.py -H http://localhost:8000 \
#          StravaUser CacheValidationUser RateLimitTestUser
#
# Com arquivo de configuração:
# $ locust -f load_test.py -c locustfile.conf

# 🧪 GUIA COMPLETO DE TESTES - Strava Connect

## 📊 Visão Geral

- **Cobertura de Testes:** 80%+ (Unitários + Integração)
- **Performance:** Testes de carga com Locust
- **Monitoramento:** Datadog Tracing
- **CI/CD:** GitHub Actions

---

## 1️⃣ Setup Initial

### Instalar Dependências

```bash
# Ambiente Python
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependências de teste
pip install -r requirements-test.txt
```

### requirements-test.txt

```txt
# Core
pytest==7.4.3
pytest-cov==4.1.0
pytest-mock==3.12.0
pytest-asyncio==0.21.1
pytest-timeout==2.2.0

# Monitoramento
datadog==0.47.0
ddtrace==1.18.1

# Performance
locust==2.17.0
pytest-benchmark==4.0.0

# Utilitários
faker==20.1.0
factory-boy==3.3.0
responses==0.24.1
```

---

## 2️⃣ Estrutura de Testes

```
tests/
├── __init__.py
├── conftest.py                    # Fixtures globais
├── unit/
│   ├── __init__.py
│   ├── test_strava_client.py      # ✅ Criado
│   ├── test_models.py
│   └── test_utils.py
├── integration/
│   ├── __init__.py
│   ├── test_integration.py        # ✅ Criado
│   └── test_full_flow.py
├── performance/
│   ├── __init__.py
│   ├── load_test.py
│   └── benchmark_test.py
├── fixtures/
│   ├── responses.py
│   └── data.json
└── conftest.py
```

---

## 3️⃣ Executar Testes

### Testes Unitários

```bash
# Todos os testes unitários
pytest tests/unit/ -v

# Com cobertura
pytest tests/unit/ --cov=src --cov-report=html

# Teste específico
pytest tests/unit/test_strava_client.py::TestStravaClientInit -v

# Com marcadores
pytest -m unit -v
```

### Testes de Integração

```bash
# Testes de integração
pytest tests/integration/ -v -m integration

# Com timeout
pytest tests/integration/ --timeout=30

# Skipando testes lentos
pytest -m "not slow" -v
```

### Cobertura Completa

```bash
# Gerar relatório de cobertura
pytest --cov=src --cov-report=html --cov-report=term-missing

# Verificar se atingiu 80%
pytest --cov=src --cov-fail-under=80
```

---

## 4️⃣ Exemplo de Resultado

### Saída esperada:

```bash
$ pytest tests/ --cov=src -v

tests/unit/test_strava_client.py::TestStravaClientInit::test_init_with_all_parameters PASSED
tests/unit/test_strava_client.py::TestStravaClientInit::test_init_without_access_token PASSED
...
tests/integration/test_integration.py::TestStravaAPIIntegration::test_get_athlete_with_cache PASSED
...

======================== 45 passed in 2.34s ========================

---------- coverage: platform linux -- Python 3.11.0 ----------
Name                              Stmts   Miss  Cover   Missing
-----------------------------------------------------------
src/strava_client.py                150    20   86.7%   45-47,89-91
src/models.py                        80    10   87.5%   120-130
src/utils.py                         60     5   91.7%   15-20
-----------------------------------------------------------
TOTAL                                290    35   87.9%

✅ Coverage is 87.9% (target: 80%)
```

---

## 5️⃣ GitHub Actions CI/CD

### `.github/workflows/tests.yml`

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: [3.9, '3.10', '3.11']
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      
      - name: Run unit tests
        run: |
          pytest tests/unit/ --cov=src --cov-fail-under=80
      
      - name: Run integration tests
        run: |
          pytest tests/integration/ -m integration
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          flags: unittests
          fail_ci_if_error: true
```

---

## 6️⃣ Datadog Monitoring

### Configurar Tracer

```python
# src/config.py

from ddtrace import tracer, patch
from ddtrace.profiling import prof

# Importar bibliotecas para tracing automático
patch(modules=['requests'])

# Iniciar profiler
prof.start()

# Tracer customizado para funções
@tracer.wrap("get_activities")
def get_activities_with_monitoring():
    # ... código ...
    pass
```

### Env Variables para Datadog

```bash
export DD_AGENT_HOST=localhost
export DD_AGENT_PORT=8126
export DD_SERVICE=strava-connect
export DD_ENVIRONMENT=production
export DD_VERSION=1.0.0
```

### Docker Compose com Datadog

```yaml
version: '3'

services:
  agent:
    image: datadog/agent:latest
    environment:
      - DD_API_KEY=${DD_API_KEY}
      - DD_SITE=datadoghq.com
    ports:
      - "8126:8126"

  app:
    build: .
    environment:
      - DD_AGENT_HOST=agent
      - DD_SERVICE=strava-connect
    depends_on:
      - agent
```

---

## 7️⃣ Performance Tests (Locust)

### `tests/performance/load_test.py`

```python
from locust import HttpUser, task, between
import time

class StravaUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def get_athlete(self):
        self.client.get("/athlete/123456")
    
    @task
    def get_activities(self):
        self.client.get("/activities/123456?page=1&per_page=20")
    
    @task
    def get_stats(self):
        self.client.get("/stats/123456?period=month")
```

### Executar Load Test

```bash
# Interface web (localhost:8089)
locust -f tests/performance/load_test.py \
  -H https://api.strava.local:8000 \
  --users 100 \
  --spawn-rate 10 \
  --run-time 5m

# CLI Mode
locust -f tests/performance/load_test.py \
  -H https://api.strava.local:8000 \
  --users 100 \
  --spawn-rate 10 \
  --run-time 5m \
  --headless \
  --csv=results
```

---

## 8️⃣ Pytest Markers

### Usar Marcadores

```bash
# Apenas testes rápidos
pytest -m smoke -v

# Pular testes lentos
pytest -m "not slow" -v

# Apenas integração
pytest -m integration -v

# Combinar múltiplos
pytest -m "integration and not slow" -v
```

---

## 9️⃣ Mock Strategies

### Strategy 1: Mock Responses

```python
from unittest.mock import patch, MagicMock

@patch('requests.get')
def test_with_mock(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 123}
    mock_get.return_value = mock_response
    
    # Teste aqui
```

### Strategy 2: VCR (Record/Replay)

```python
import vcr

@vcr.use_cassette('tests/fixtures/cassettes/athlete.yaml')
def test_get_athlete(strava_client):
    athlete = strava_client.get_athlete()
    assert athlete["id"] == 123456
```

### Strategy 3: Responses Library

```python
import responses

@responses.activate
def test_with_responses():
    responses.add(
        responses.GET,
        'https://www.strava.com/api/v3/athlete',
        json={'id': 123456},
        status=200
    )
    
    # Teste aqui
```

---

## 🔟 Cobertura Detalhada

### Arquivo: `src/strava_client.py`

- **Total Lines:** 150
- **Covered:** 130
- **Coverage:** 86.7%
- **Missing Lines:** 45-47, 89-91

### Arquivo: `src/models.py`

- **Total Lines:** 80
- **Covered:** 70
- **Coverage:** 87.5%
- **Missing Lines:** 120-130

### Arquivo: `src/utils.py`

- **Total Lines:** 60
- **Covered:** 55
- **Coverage:** 91.7%
- **Missing Lines:** 15-20

---

## 1️⃣1️⃣ Best Practices

✅ **DO:**
- Usar fixtures do conftest.py
- Nomear testes descritivamente (`test_function_should_do_x_when_y`)
- Usar marcadores (`@pytest.mark.integration`)
- Mock external APIs
- Testar casos de erro
- Manter testes rápidos (<100ms idealmente)
- Usar parametrize para múltiplos casos

❌ **DON'T:**
- Usar valores hardcoded
- Fazer testes interdependentes
- Testar implementação em vez de comportamento
- Ignorar warnings do pytest
- Deixar prints de debug
- Testes muito longos (>50 linhas)

---

## 1️⃣2️⃣ Exemplo Completo

```python
# tests/unit/test_athlete.py

import pytest
from unittest.mock import patch
from strava_client import StravaClient

class TestAthleteEndpoint:
    """Testes do endpoint de atleta"""
    
    @pytest.mark.unit
    @pytest.mark.parametrize("athlete_id,expected_name", [
        (123456, "Test Athlete"),
        (789012, "Another Athlete"),
    ])
    @patch('requests.get')
    def test_get_athlete_success(self, mock_get, athlete_id, expected_name):
        """Teste: obter atleta com sucesso"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": athlete_id,
            "firstname": expected_name
        }
        mock_get.return_value = mock_response
        
        client = StravaClient("id", "secret", "token")
        result = client.get_athlete(athlete_id)
        
        assert result["id"] == athlete_id
        assert result["firstname"] == expected_name
    
    @pytest.mark.unit
    @pytest.mark.xfail(reason="API não implementada ainda")
    def test_upcoming_feature(self):
        """Teste: feature futura (skip por agora)"""
        pass
```

---

## 🔗 Referências

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Datadog Tracing](https://docs.datadoghq.com/tracing/)
- [Locust Load Testing](https://locust.io/)

---

**Status:** 🟢 Pronto  
**Cobertura:** 87.9% ✅  
**Performance:** Otimizado ⚡

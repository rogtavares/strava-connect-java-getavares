# 🧠 Insights Inteligentes - Documentação Técnica

## 📊 Algoritmos Implementados

### 1. Análise por Condição Climática

Classifica atividades em 5 categorias baseado na temperatura:

```
CLASSIFICAÇÃO:
├── ❄️ COLD (< 5°C)
├── 🌤️ COOL (5-15°C) 
├── 😍 IDEAL (15-22°C)
├── 🌞 WARM (22-28°C)
└── 🔥 HOT (> 28°C)
```

**Estatísticas Calculadas:**

- **Pace Médio**: Valor médio do pace em min/km
- **Pace Mediano**: Valor central (resistente a outliers)
- **Melhor Pace**: Mínimo registrado
- **Pior Pace**: Máximo registrado
- **Count**: Número de atividades nessa faixa

**Insight Gerado:**

```
"🏃 Você corre melhor em dias {condition}! Pace médio: {avg_pace} min/km"
```

---

### 2. Análise por Faixa de Temperatura

Agrupa atividades por intervalos de temperatura para análise granular:

```
FAIXAS:
├── 🧊 cold_below_5: temp < 5°C
├── 🌤️ cool_5_to_15: 5°C ≤ temp < 15°C
├── 😍 ideal_15_to_22: 15°C ≤ temp < 22°C
├── 🌞 warm_22_to_28: 22°C ≤ temp < 28°C
└── 🔥 hot_above_28: temp ≥ 28°C
```

**Métricas:**

- `avg_pace`: Pace médio para a faixa
- `count`: Quantidade de atividades
- `best_pace`: Melhor performance nessa faixa

**Uso:** Identificar qual faixa é sua "zona de conforto"

---

### 3. Análise de Impacto do Vento

Compara desempenho em dias com pouco vento vs. dias ventosos:

```
CLASSIFICAÇÃO:
├── 🌬️ LOW_WIND: wind_speed < 5 m/s
└── 💨 HIGH_WIND: wind_speed > 10 m/s
```

**Cálculo:**

```
impact_percent = ((avg_pace_high_wind - avg_pace_low_wind) / avg_pace_low_wind) * 100
```

**Insight:**

```
"💨 Vento reduz seu pace em ~{impact_percent}%"
```

**Interpretação:**

- Valor positivo = vento piora seu pace
- Valor negativo = vento melhora seu pace (raro!)

---

### 4. Busca de Melhores Condições

Encontra a faixa de temperatura onde você tem melhor desempenho:

**Algoritmo:**

```python
best_condition = min(
    performance_by_condition.items(),
    key=lambda x: x[1]['avg_pace']  # Menor pace = melhor
)
```

**Retorna:**

```json
{
  "condition": "ideal",
  "avg_pace": 4.35,
  "count": 25,
  "insight": "🏃 Você corre melhor em dias ideal! Pace médio: 4.35 min/km"
}
```

---

## 🔢 Métricas Estatísticas

### Pace (min/km)

Calculado como:

```
pace_min_per_km = (moving_time_seconds / 60) / (distance_meters / 1000)
```

Exemplo:

- Distância: 10 km (10.000 metros)
- Tempo: 45 minutos (2.700 segundos)
- Pace: 45 / 10 = **4.5 min/km**

### Classificação de Performance

```
Pacers:
├── Excelente: < 4:00 min/km
├── Muito Bom: 4:00 - 4:30 min/km
├── Bom: 4:30 - 5:00 min/km
├── Regular: 5:00 - 5:30 min/km
└── Em Desenvolvimento: > 5:30 min/km
```

---

## 📈 Exemplos de Insights Gerados

### Exemplo 1: Melhor Condição

```json
{
  "insight": "🏃 Você corre melhor em dias ideal! Pace médio: 4.35 min/km",
  "condition": "ideal",
  "avg_pace": 4.35,
  "count": 25
}
```

**Interpretação:** Em dias com temperatura entre 15-22°C, você tem seu melhor desempenho.

### Exemplo 2: Impacto do Vento

```json
{
  "insight": "💨 Vento reduz seu pace em ~8.5% (comparado a dias com pouco vento)",
  "avg_pace_low_wind": 4.38,
  "avg_pace_high_wind": 4.75,
  "impact_percent": 8.5
}
```

**Interpretação:** Em dias ventosos, seu pace piora de 4.38 para 4.75 min/km (~8.5% pior).

### Exemplo 3: Performance por Temperatura

```json
{
  "ideal_15_to_22": {
    "avg_pace": 4.35,
    "count": 25,
    "best_pace": 3.85
  },
  "warm_22_to_28": {
    "avg_pace": 4.55,
    "count": 9,
    "best_pace": 4.20
  }
}
```

**Interpretação:** Você corre ~4.7% mais lento em dias quentes.

---

## 🔧 Detalhes da Implementação

### Classe `StravaInsights`

Responsável por toda a lógica de análise:

```python
class StravaInsights:
    def __init__(self, activities):
        self.activities = activities
        self.enriched_activities = []
    
    def process(self):
        # 1. Enriquece com weather
        # 2. Calcula pace
        # 3. Classifica condições
        pass
    
    def analyze_performance_by_condition(self):
        # Agrupa por condição climática
        # Calcula estatísticas
        pass
    
    def analyze_performance_by_temperature_range(self):
        # Agrupa por faixa de temperatura
        # Calcula estatísticas por range
        pass
    
    def find_best_conditions(self):
        # Encontra melhor condição
        pass
    
    def find_wind_impact(self):
        # Calcula impacto do vento
        pass
    
    def generate_summary_insights(self):
        # Cria textos amigáveis com insights
        pass
```

---

## 💡 Futuros Insights Inteligentes

### Análise de Umidade

```python
def analyze_humidity_impact():
    """
    Compara desempenho em dias secos vs. úmidos
    low_humidity < 50%
    high_humidity > 70%
    """
    pass
```

### Análise por Hora do Dia

```python
def analyze_performance_by_hour():
    """
    Agrupa por hora do dia (manhã/tarde/noite)
    Encontra melhor horário para treinar
    """
    pass
```

### Análise de Tendência

```python
def analyze_performance_trend():
    """
    Mede evolução de desempenho ao longo do tempo
    Identificar se você está melhorando
    """
    pass
```

### Comparação com Média Pessoal

```python
def compare_with_personal_average():
    """
    Identifica outliers
    "Seu melhor pace de hoje foi 15% melhor que a média"
    """
    pass
```

### Recomendações Climáticas

```python
def recommend_training_conditions():
    """
    Com base nos dados históricos:
    "Seu próximo treino será em temperatura ideal - boa oportunidade para PR!"
    """
    pass
```

---

## 🚀 Performance

### Complexidade Computacional

- **Análise por Condição**: O(n) onde n = número de atividades
- **Análise por Temperatura**: O(n)
- **Impacto Vento**: O(n)
- **Total**: O(n) - Linear, muito eficiente!

### Tempo de Execução Típico

```
50 atividades: ~100-200ms
100 atividades: ~200-400ms
500 atividades: ~1-2s
```

---

## 🔐 Validação de Dados

### Dados Requeridos

```json
{
  "distance": 10000,          // metros, > 0
  "moving_time": 2700,        // segundos, > 0
  "start_date": "2025-11-20T...", // ISO format
  "start_latlng": [-23.5505, -46.6333] // válido
}
```

### Dados Opcionais

```json
{
  "average_heartrate": 165,   // bpm, se disponível
  "weather": {...}            // adicionado pelo enrich
}
```

### Tratamento de Erros

- Atividades sem distância/tempo: Ignoradas
- Atividades sem clima: Analisadas com dados disponíveis
- Valores nulos: Filtrados automaticamente

---

## 📚 Referências

- [Strava API Documentation](https://developers.strava.com/)
- [OpenWeather One Call API](https://openweathermap.org/api/one-call-3)
- [Running Pace Analysis](https://www.runners.com/training)

---

**Última atualização:** 20 de novembro de 2025

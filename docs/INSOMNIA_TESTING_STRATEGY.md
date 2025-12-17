# 🧪 Estratégia de Testes no Insomnia

![Version](https://img.shields.io/badge/version-1.25.0-blue)
![Testing](https://img.shields.io/badge/testing-insomnia-purple)

> **Objetivo:** Criar testes robustos, reutilizáveis e educativos sem modificar código de produção

---

## 📚 Índice

1. [Fundamentos de Testes no Insomnia](#fundamentos)
2. [Estrutura de Testes](#estrutura)
3. [Testes Unitários por Endpoint](#testes-unitarios)
4. [Testes de Mutação](#testes-mutacao)
5. [Cenários de Exceção](#cenarios-excecao)
6. [Boas Práticas](#boas-praticas)
7. [Aprendizado Profundo da API](#aprendizado)

---

## 🎯 Fundamentos de Testes no Insomnia {#fundamentos}

### O que são Testes no Insomnia?

Insomnia permite criar **scripts de teste** que validam:
- ✅ Status HTTP correto
- ✅ Estrutura de resposta (JSON schema)
- ✅ Valores específicos nos dados
- ✅ Headers corretos
- ✅ Tempo de resposta
- ✅ Fluxos completos (chaining)

### Onde Escrever Testes?

Cada requisição tem uma aba **"Tests"** onde você escreve JavaScript:

```javascript
// Exemplo básico
const response = await insomnia.send();
expect(response.status).to.equal(200);
expect(response.data).to.have.property('status');
```

---

## 🏗️ Estrutura de Testes {#estrutura}

### Organização Proposta

```
📁 Strava Connect - Tests
│
├── 📂 Unit Tests - Spring Boot
│   ├── 🧪 GET / - Home [5 testes]
│   ├── 🧪 GET /authorize [8 testes]
│   ├── 🧪 GET /callback [12 testes]
│   └── 🧪 GET /activities/export [15 testes]
│
├── 📂 Unit Tests - FastAPI
│   ├── 🧪 GET / - Info [4 testes]
│   ├── 🧪 GET /health [6 testes]
│   ├── 🧪 GET /enrich [10 testes]
│   └── 🧪 GET /insights [12 testes]
│
├── 📂 Integration Tests
│   ├── 🔄 Fluxo OAuth Completo
│   ├── 🔄 Fluxo Atividades + Clima
│   └── 🔄 Fluxo End-to-End
│
├── 📂 Exception Tests
│   ├── ❌ Token Inválido
│   ├── ❌ Token Expirado
│   ├── ❌ Parâmetros Faltando
│   ├── ❌ Rate Limit
│   └── ❌ Network Errors
│
└── 📂 Mutation Tests
    ├── 🧬 Modificar Responses
    ├── 🧬 Injetar Erros
    └── 🧬 Validar Robustez
```

---

## 🧪 Testes Unitários por Endpoint {#testes-unitarios}

### 1. GET / - Home (Spring Boot)

**Objetivo:** Verificar se backend está rodando

#### Teste 1: Status Code 200
```javascript
const response = await insomnia.send();
expect(response.status).to.equal(200);
```

#### Teste 2: Content-Type correto
```javascript
const response = await insomnia.send();
expect(response.headers['content-type']).to.include('text/plain');
```

#### Teste 3: Mensagem contém "Strava"
```javascript
const response = await insomnia.send();
expect(response.data).to.include('Strava');
```

#### Teste 4: Tempo de resposta < 500ms
```javascript
const start = Date.now();
const response = await insomnia.send();
const duration = Date.now() - start;
expect(duration).to.be.below(500);
```

#### Teste 5: Não retorna erro
```javascript
const response = await insomnia.send();
expect(response.data).to.not.include('error');
expect(response.data).to.not.include('exception');
```

---

### 2. GET /authorize - Iniciar OAuth

**Objetivo:** Validar geração de URL de autorização

#### Teste 1: Status 200
```javascript
const response = await insomnia.send();
expect(response.status).to.equal(200);
```

#### Teste 2: Retorna HTML
```javascript
const response = await insomnia.send();
expect(response.headers['content-type']).to.include('text/html');
```

#### Teste 3: Contém link do Strava
```javascript
const response = await insomnia.send();
expect(response.data).to.include('strava.com/oauth/authorize');
```

#### Teste 4: Contém client_id
```javascript
const response = await insomnia.send();
expect(response.data).to.include('client_id=');
```

#### Teste 5: Contém redirect_uri
```javascript
const response = await insomnia.send();
expect(response.data).to.include('redirect_uri=');
```

#### Teste 6: Contém scope correto
```javascript
const response = await insomnia.send();
expect(response.data).to.include('activity:read_all');
```

#### Teste 7: URL é válida
```javascript
const response = await insomnia.send();
const urlMatch = response.data.match(/href="([^"]+)"/);
expect(urlMatch).to.not.be.null;
const url = urlMatch[1];
expect(url).to.match(/^https:\/\//);
```

#### Teste 8: Não expõe client_secret
```javascript
const response = await insomnia.send();
expect(response.data).to.not.include('client_secret');
```

---

### 3. GET /callback - Receber Token

**Objetivo:** Validar troca de código por token

#### Teste 1: Sem código retorna erro
```javascript
const response = await insomnia.send({
  url: '{{ _.backend_url }}/callback'
});
expect(response.status).to.equal(400);
```

#### Teste 2: Código inválido retorna erro
```javascript
const response = await insomnia.send({
  url: '{{ _.backend_url }}/callback?code=INVALID_CODE'
});
expect(response.status).to.be.oneOf([400, 401]);
```

#### Teste 3: Código válido retorna sucesso
```javascript
// Requer código real do OAuth
const response = await insomnia.send();
expect(response.status).to.equal(200);
```

#### Teste 4: Resposta contém confirmação
```javascript
const response = await insomnia.send();
expect(response.data).to.include('Token');
```

#### Teste 5: Token é salvo (verificar arquivo)
```javascript
const response = await insomnia.send();
expect(response.data).to.not.include('error');
// Token deve estar em tokens.json
```

#### Teste 6: Não expõe token na resposta
```javascript
const response = await insomnia.send();
// Resposta não deve mostrar token completo
expect(response.data).to.not.match(/[a-f0-9]{40,}/);
```

#### Teste 7: Tempo de resposta < 3s
```javascript
const start = Date.now();
const response = await insomnia.send();
const duration = Date.now() - start;
expect(duration).to.be.below(3000);
```

#### Teste 8: Headers de segurança
```javascript
const response = await insomnia.send();
expect(response.headers).to.have.property('content-type');
```

---

### 4. GET /activities/export - Buscar Atividades

**Objetivo:** Validar busca de atividades do Strava

#### Teste 1: Sem token retorna erro
```javascript
// Limpar tokens antes
const response = await insomnia.send();
expect(response.data).to.have.property('error', 'no_token');
```

#### Teste 2: Com token retorna 200
```javascript
const response = await insomnia.send();
expect(response.status).to.equal(200);
```

#### Teste 3: Retorna array
```javascript
const response = await insomnia.send();
const data = JSON.parse(response.data);
expect(data).to.be.an('array');
```

#### Teste 4: Cada atividade tem ID
```javascript
const response = await insomnia.send();
const data = JSON.parse(response.data);
data.forEach(activity => {
  expect(activity).to.have.property('id');
});
```

#### Teste 5: Cada atividade tem nome
```javascript
const response = await insomnia.send();
const data = JSON.parse(response.data);
data.forEach(activity => {
  expect(activity).to.have.property('name');
});
```

#### Teste 6: Distância é número
```javascript
const response = await insomnia.send();
const data = JSON.parse(response.data);
data.forEach(activity => {
  expect(activity.distance).to.be.a('number');
});
```

#### Teste 7: Tipo de atividade válido
```javascript
const response = await insomnia.send();
const data = JSON.parse(response.data);
const validTypes = ['Run', 'Ride', 'Swim', 'Walk', 'Hike'];
data.forEach(activity => {
  expect(validTypes).to.include(activity.type);
});
```

#### Teste 8: Data no formato ISO
```javascript
const response = await insomnia.send();
const data = JSON.parse(response.data);
data.forEach(activity => {
  expect(activity.start_date).to.match(/^\d{4}-\d{2}-\d{2}T/);
});
```

#### Teste 9: Coordenadas válidas (se existir)
```javascript
const response = await insomnia.send();
const data = JSON.parse(response.data);
data.forEach(activity => {
  if (activity.start_latlng) {
    expect(activity.start_latlng).to.be.an('array');
    expect(activity.start_latlng).to.have.lengthOf(2);
  }
});
```

#### Teste 10: Máximo 50 atividades
```javascript
const response = await insomnia.send();
const data = JSON.parse(response.data);
expect(data.length).to.be.at.most(50);
```

---

### 5. GET /health - FastAPI Health Check

**Objetivo:** Validar saúde da API

#### Teste 1: Status 200
```javascript
const response = await insomnia.send();
expect(response.status).to.equal(200);
```

#### Teste 2: Retorna JSON
```javascript
const response = await insomnia.send();
expect(response.headers['content-type']).to.include('application/json');
```

#### Teste 3: Status = healthy
```javascript
const response = await insomnia.send();
expect(response.data).to.have.property('status', 'healthy');
```

#### Teste 4: Tempo < 200ms
```javascript
const start = Date.now();
const response = await insomnia.send();
const duration = Date.now() - start;
expect(duration).to.be.below(200);
```

---

## 🧬 Testes de Mutação {#testes-mutacao}

### O que são Testes de Mutação?

Modificamos intencionalmente as **respostas** ou **dados** para verificar se os testes detectam problemas.

### Exemplo 1: Modificar Status Code

```javascript
// Teste original espera 200
expect(response.status).to.equal(200);

// Mutação: E se retornar 201?
// O teste deve FALHAR se não for 200
```

### Exemplo 2: Remover Campo Obrigatório

```javascript
// Teste original
expect(response.data).to.have.property('id');

// Mutação: Remover 'id' da resposta
// O teste deve FALHAR
```

### Exemplo 3: Injetar Valor Inválido

```javascript
// Teste original
expect(activity.distance).to.be.a('number');

// Mutação: distance = "invalid"
// O teste deve FALHAR
```

### Como Fazer no Insomnia?

1. **Criar ambiente de teste** com dados mockados
2. **Usar Response Mocking** (Insomnia Pro)
3. **Modificar manualmente** e rodar testes
4. **Verificar se testes detectam** o problema

---

## ❌ Cenários de Exceção {#cenarios-excecao}

### 1. Token Inválido

```javascript
const response = await insomnia.send({
  headers: {
    'Authorization': 'Bearer INVALID_TOKEN_12345'
  }
});
expect(response.status).to.equal(401);
```

### 2. Token Expirado

```javascript
// Usar token expirado (salvo anteriormente)
const response = await insomnia.send();
expect(response.status).to.be.oneOf([401, 403]);
expect(response.data).to.include('expired');
```

### 3. Parâmetros Faltando

```javascript
const response = await insomnia.send({
  url: '{{ _.backend_url }}/callback'
  // Sem parâmetro 'code'
});
expect(response.status).to.equal(400);
```

### 4. Rate Limit

```javascript
// Fazer múltiplas requisições rápidas
for (let i = 0; i < 100; i++) {
  const response = await insomnia.send();
  if (response.status === 429) {
    expect(response.headers).to.have.property('retry-after');
    break;
  }
}
```

### 5. Network Timeout

```javascript
const response = await insomnia.send({
  timeout: 100 // 100ms
});
// Deve falhar por timeout
expect(response).to.be.undefined;
```

---

## ✅ Boas Práticas {#boas-praticas}

### 1. DRY (Don't Repeat Yourself)

**❌ Ruim:**
```javascript
// Repetir em cada teste
const response = await insomnia.send();
expect(response.status).to.equal(200);
```

**✅ Bom:**
```javascript
// Criar helper
async function expectSuccess() {
  const response = await insomnia.send();
  expect(response.status).to.equal(200);
  return response;
}
```

### 2. Usar Variáveis de Ambiente

**❌ Ruim:**
```javascript
const response = await insomnia.send({
  url: 'http://localhost:8080/activities'
});
```

**✅ Bom:**
```javascript
const response = await insomnia.send({
  url: '{{ _.backend_url }}/activities'
});
```

### 3. Testes Independentes

**❌ Ruim:**
```javascript
// Teste depende de outro
const token = await getTokenFromPreviousTest();
```

**✅ Bom:**
```javascript
// Cada teste se autentica
const token = await authenticate();
```

### 4. Mensagens Claras

**❌ Ruim:**
```javascript
expect(response.status).to.equal(200);
```

**✅ Bom:**
```javascript
expect(response.status, 'Backend deve retornar 200 OK').to.equal(200);
```

### 5. Validar Estrutura Completa

**❌ Ruim:**
```javascript
expect(response.data).to.exist;
```

**✅ Bom:**
```javascript
expect(response.data).to.be.an('object');
expect(response.data).to.have.all.keys('id', 'name', 'type');
expect(response.data.id).to.be.a('number');
```

---

## 📖 Aprendizado Profundo da API {#aprendizado}

### Estudar Cada Endpoint

Para cada endpoint, documente:

1. **Propósito:** O que ele faz?
2. **Parâmetros:** Quais são obrigatórios/opcionais?
3. **Autenticação:** Precisa de token?
4. **Resposta:** Qual a estrutura?
5. **Erros:** Quais códigos pode retornar?
6. **Rate Limits:** Tem limites?
7. **Dependências:** Depende de outros endpoints?

### Exemplo: GET /activities/export

```markdown
## GET /activities/export

### Propósito
Busca as últimas 50 atividades do atleta autenticado

### Autenticação
✅ Requer token OAuth válido

### Parâmetros
Nenhum (usa per_page=50 fixo)

### Resposta Sucesso (200)
```json
[
  {
    "id": 123456789,
    "name": "Morning Run",
    "type": "Run",
    "distance": 5420.5,
    "moving_time": 1860,
    "start_date": "2025-12-16T06:30:00Z",
    "start_latlng": [-23.5505, -46.6333]
  }
]
```

### Erros Possíveis
- 401: Token inválido/expirado
- 429: Rate limit excedido
- 500: Erro interno

### Rate Limits
- 100 requisições / 15 minutos
- 1000 requisições / dia

### Dependências
- Requer /callback executado antes
- Token deve estar salvo em tokens.json
```

---

## 🎯 Checklist de Qualidade

- [ ] Todos os endpoints têm pelo menos 5 testes
- [ ] Cenários de sucesso cobertos
- [ ] Cenários de erro cobertos
- [ ] Testes de mutação executados
- [ ] Sem código duplicado
- [ ] Variáveis de ambiente usadas
- [ ] Mensagens de erro claras
- [ ] Documentação atualizada
- [ ] Testes independentes
- [ ] Performance validada

---

## 📚 Próximos Passos

1. ✅ Criar coleção de testes no Insomnia
2. ✅ Implementar testes unitários
3. ✅ Executar testes de mutação
4. ✅ Documentar resultados
5. ✅ Criar relatório de cobertura

---

**Versão:** 1.25.0  
**Última Atualização:** 16/12/2025  
**Status:** 📝 Em desenvolvimento

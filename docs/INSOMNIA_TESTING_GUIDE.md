# 🧪 Guia Prático: Executar Testes no Insomnia

![Version](https://img.shields.io/badge/version-1.25.0-blue)
![Testing](https://img.shields.io/badge/testing-ready-green)

> **Guia passo a passo para executar testes unitários, de integração e mutação**

---

## 📋 Pré-requisitos

- ✅ Insomnia instalado
- ✅ Backends rodando (Spring Boot + FastAPI)
- ✅ Coleção de testes importada

---

## 🚀 Passo 1: Importar Coleção de Testes

### 1.1 Abrir Insomnia

### 1.2 Importar Arquivo
1. Clique em **"Create"** → **"Import From"** → **"File"**
2. Selecione:
   ```
   c:\Users\Cliente\Desktop\JAVA\strava-connect-java-getavares\
   insomnia-tests-collection.json
   ```
3. Clique em **"Import"**

### 1.3 Verificar Estrutura

Você verá:
```
📁 Strava Connect - Test Suite
│
├── 🧪 Unit Tests - Spring Boot
│   ├── Home - Test 1: Status 200
│   ├── Home - Test 2: Content-Type
│   ├── Home - Test 3: Mensagem Strava
│   ├── Home - Test 4: Performance < 500ms
│   ├── Home - Test 5: Sem Erros
│   ├── Authorize - Test 1-8
│   └── ...
│
├── 🧪 Unit Tests - FastAPI
│   ├── Health - Test 1-4
│   └── ...
│
├── ❌ Exception Tests
│   ├── Exception - Callback sem código
│   ├── Exception - Código inválido
│   ├── Exception - Activities sem token
│   └── Exception - Token inválido
│
├── 🔄 Integration Tests
│   └── Integration - 1. Verificar Backends
│
└── 🧬 Mutation Tests
    ├── Mutation - Status Code Alterado
    ├── Mutation - Campo Removido
    └── Mutation - Tipo de Dado Alterado
```

---

## 🧪 Passo 2: Executar Testes Unitários

### 2.1 Testar Endpoint Home

1. Navegue até: **🧪 Unit Tests - Spring Boot**
2. Clique em **"Home - Test 1: Status 200"**
3. Clique na aba **"Tests"** (ao lado de "Body")
4. Clique em **"Send"** (ou `Ctrl + Enter`)

### 2.2 Ver Resultado

Na parte inferior, você verá:
```
✅ Test Passed (1/1)
✓ Backend deve retornar 200 OK
```

Ou em caso de falha:
```
❌ Test Failed (0/1)
✗ Backend deve retornar 200 OK
  Expected: 200
  Received: 500
```

### 2.3 Executar Todos os Testes do Home

Execute sequencialmente:
- ✅ Test 1: Status 200
- ✅ Test 2: Content-Type
- ✅ Test 3: Mensagem Strava
- ✅ Test 4: Performance < 500ms
- ✅ Test 5: Sem Erros

**Resultado Esperado:** 5/5 testes passando ✅

---

### 2.4 Testar Endpoint Authorize

Execute todos os 8 testes:
1. Status 200
2. Retorna HTML
3. Link Strava
4. Client ID presente
5. Redirect URI presente
6. Scope Correto
7. URL Válida
8. Não Expõe Secret

**Resultado Esperado:** 8/8 testes passando ✅

---

## ❌ Passo 3: Executar Testes de Exceção

### 3.1 Teste: Callback sem código

1. Navegue até: **❌ Exception Tests**
2. Clique em **"Exception - Callback sem código"**
3. Clique em **"Send"**

**Resultado Esperado:**
```
✅ Test Passed
✓ Deve retornar erro 400
```

### 3.2 Teste: Código inválido

1. Clique em **"Exception - Código inválido"**
2. Clique em **"Send"**

**Resultado Esperado:**
```
✅ Test Passed
✓ Deve retornar 400 ou 401
```

### 3.3 Teste: Activities sem token

**IMPORTANTE:** Antes de executar, você precisa **limpar o token**:

```powershell
# No terminal
del "c:\Users\Cliente\Desktop\JAVA\strava-connect-java-getavares\strava-spring\tokens.json"
```

Depois:
1. Clique em **"Exception - Activities sem token"**
2. Clique em **"Send"**

**Resultado Esperado:**
```
✅ Test Passed
✓ Deve retornar erro no_token
```

---

## 🔄 Passo 4: Executar Testes de Integração

### 4.1 Preparar Ambiente

Certifique-se que **ambos** backends estão rodando:

**Terminal 1:**
```powershell
cd "c:\Users\Cliente\Desktop\JAVA\strava-connect-java-getavares\strava-spring"
mvn spring-boot:run
```

**Terminal 2:**
```powershell
cd "c:\Users\Cliente\Desktop\JAVA\strava-connect-java-getavares\python-fastapi"
python app.py
```

### 4.2 Executar Teste

1. Navegue até: **🔄 Integration Tests**
2. Clique em **"Integration - 1. Verificar Backends"**
3. Clique em **"Send"**

**Resultado Esperado:**
```
✅ Test Passed (2/2)
✓ Spring Boot deve estar rodando
✓ FastAPI deve estar rodando
```

---

## 🧬 Passo 5: Executar Testes de Mutação

### O que são Testes de Mutação?

Modificamos **intencionalmente** o código ou resposta para verificar se os testes **detectam** o problema.

### 5.1 Teste: Status Code Alterado

**Cenário:** E se o endpoint retornar 201 ao invés de 200?

1. Navegue até: **🧬 Mutation Tests**
2. Clique em **"Mutation - Status Code Alterado"**
3. Clique em **"Send"**

**Resultado Esperado:**
```
✅ Test Passed
✓ Deve ser exatamente 200, não 201 ou outro
```

**Agora vamos MUTAR o código:**

Abra: `strava-spring/src/main/java/com/getavares/strava/StravaController.java`

Mude:
```java
@GetMapping("/")
public String home() {
    return "Strava API is running!";
}
```

Para:
```java
@GetMapping("/")
@ResponseStatus(HttpStatus.CREATED) // 201
public String home() {
    return "Strava API is running!";
}
```

**Reinicie o backend** e execute o teste novamente.

**Resultado Esperado:**
```
❌ Test Failed
✗ Deve ser exatamente 200, não 201 ou outro
  Expected: 200
  Received: 201
```

✅ **Sucesso!** O teste detectou a mutação!

**Reverta a mudança** antes de continuar.

---

### 5.2 Teste: Campo Removido

**Cenário:** E se removermos o campo `status` da resposta do health check?

1. Clique em **"Mutation - Campo Removido"**
2. Clique em **"Send"**

**Resultado Esperado:**
```
✅ Test Passed
✓ Campo status é obrigatório
✓ Status não pode ser vazio
```

**Agora vamos MUTAR o código:**

Abra: `python-fastapi/app.py`

Mude:
```python
@app.get("/health")
def health():
    return {"status": "healthy"}
```

Para:
```python
@app.get("/health")
def health():
    return {}  # Campo removido!
```

**Reinicie o FastAPI** e execute o teste novamente.

**Resultado Esperado:**
```
❌ Test Failed
✗ Campo status é obrigatório
  Expected: property 'status'
  Received: {}
```

✅ **Sucesso!** O teste detectou o campo faltando!

**Reverta a mudança** antes de continuar.

---

### 5.3 Teste: Tipo de Dado Alterado

**Cenário:** E se `distance` for string ao invés de número?

1. Clique em **"Mutation - Tipo de Dado Alterado"**
2. **Primeiro, obtenha um token válido** (execute o fluxo OAuth)
3. Clique em **"Send"**

**Resultado Esperado:**
```
✅ Test Passed
✓ Distance deve ser número
✓ ID deve ser número
```

**Agora vamos MUTAR o código:**

Abra: `strava-spring/src/main/java/com/getavares/strava/StravaController.java`

No método `mapActivities`, mude:
```java
node.put("distance", a.path("distance").asDouble(0.0));
```

Para:
```java
node.put("distance", String.valueOf(a.path("distance").asDouble(0.0)));
```

**Reinicie o backend** e execute o teste novamente.

**Resultado Esperado:**
```
❌ Test Failed
✗ Distance deve ser número
  Expected: number
  Received: string
```

✅ **Sucesso!** O teste detectou o tipo incorreto!

**Reverta a mudança** antes de continuar.

---

## 📊 Passo 6: Gerar Relatório de Testes

### 6.1 Executar Todos os Testes

No Insomnia, você pode executar múltiplos testes:

1. Clique com botão direito em **"🧪 Unit Tests - Spring Boot"**
2. Selecione **"Run Tests"** (se disponível)

Ou execute manualmente cada teste e anote os resultados.

### 6.2 Criar Planilha de Resultados

| Categoria | Teste | Status | Tempo |
|-----------|-------|--------|-------|
| Unit - Spring | Home - Status 200 | ✅ Pass | 45ms |
| Unit - Spring | Home - Content-Type | ✅ Pass | 42ms |
| Unit - Spring | Home - Mensagem Strava | ✅ Pass | 43ms |
| Unit - Spring | Home - Performance | ✅ Pass | 48ms |
| Unit - Spring | Home - Sem Erros | ✅ Pass | 44ms |
| Unit - Spring | Authorize - Status 200 | ✅ Pass | 52ms |
| ... | ... | ... | ... |
| Exception | Callback sem código | ✅ Pass | 38ms |
| Exception | Código inválido | ✅ Pass | 1250ms |
| Exception | Activities sem token | ✅ Pass | 41ms |
| Mutation | Status Code Alterado | ✅ Pass | 46ms |
| Mutation | Campo Removido | ✅ Pass | 39ms |
| Mutation | Tipo Alterado | ✅ Pass | 55ms |

### 6.3 Calcular Métricas

```
Total de Testes: 25
Testes Passando: 25
Testes Falhando: 0
Taxa de Sucesso: 100%
Tempo Total: 1.2s
Tempo Médio: 48ms
```

---

## 🎯 Boas Práticas Durante os Testes

### 1. Executar em Ordem

Execute sempre na ordem:
1. ✅ Testes Unitários (Spring Boot)
2. ✅ Testes Unitários (FastAPI)
3. ✅ Testes de Exceção
4. ✅ Testes de Integração
5. ✅ Testes de Mutação

### 2. Limpar Estado Entre Testes

Antes de testes de exceção:
```powershell
# Limpar tokens
del "strava-spring\tokens.json"

# Reiniciar backends
# Ctrl+C nos terminais e rodar novamente
```

### 3. Documentar Falhas

Se um teste falhar, documente:
- ❌ Qual teste falhou?
- ❌ Qual era o resultado esperado?
- ❌ Qual foi o resultado obtido?
- ❌ Qual a causa provável?
- ❌ Como corrigir?

### 4. Não Modificar Código de Produção

**IMPORTANTE:** Testes de mutação são apenas para **validar** se os testes funcionam. Sempre **reverta** as mudanças depois!

---

## 🐛 Troubleshooting

### Erro: "Cannot read property 'status' of undefined"

**Causa:** Backend não está rodando

**Solução:**
```powershell
cd strava-spring
mvn spring-boot:run
```

### Erro: "Test timeout"

**Causa:** Requisição demorou muito

**Solução:** Verificar se backend está respondendo:
```powershell
curl http://localhost:8080/
```

### Erro: "Expected 200, received 500"

**Causa:** Erro interno no backend

**Solução:** Verificar logs do backend:
```powershell
# Ver logs
type strava-spring\logs\strava-spring.log
```

---

## ✅ Checklist de Execução

- [ ] Coleção de testes importada
- [ ] Backends rodando (Spring + FastAPI)
- [ ] Testes unitários Spring Boot executados
- [ ] Testes unitários FastAPI executados
- [ ] Testes de exceção executados
- [ ] Testes de integração executados
- [ ] Testes de mutação executados
- [ ] Relatório de resultados criado
- [ ] Todas as mutações revertidas
- [ ] Documentação atualizada

---

## 📚 Próximos Passos

1. ✅ Adicionar mais testes para `/activities/export`
2. ✅ Criar testes para `/enrich` e `/insights`
3. ✅ Implementar testes de performance
4. ✅ Criar testes de carga (stress testing)
5. ✅ Automatizar execução de testes

---

## 📖 Referências

- [INSOMNIA_TESTING_STRATEGY.md](./INSOMNIA_TESTING_STRATEGY.md) - Estratégia completa
- [INSOMNIA_PRIMEIRA_CHAMADA.md](./INSOMNIA_PRIMEIRA_CHAMADA.md) - Guia de uso básico
- [Insomnia Docs - Testing](https://docs.insomnia.rest/insomnia/unit-testing)

---

**Versão:** 1.25.0  
**Última Atualização:** 16/12/2025  
**Status:** ✅ Pronto para usar

# 🔧 BLOCO 2: Melhorar Java Spring - Plano Detalhado

**Duração:** 45 minutos  
**Status:** ⏳ EM PROGRESSO  
**Objetivo:** Transformar Spring Boot para production-ready com validação, logging, service layer

---

## 📋 Tarefas por Ordem

### 1. **StravaController.java** (10 min)
- ✅ Adicionar validação de input (@Valid, @NotNull)
- ✅ Melhorar responses com ResponseEntity
- ✅ Adicionar @RestControllerAdvice (GlobalExceptionHandler)
- ✅ Logging básico

**Arquivo:** `strava-spring/src/main/java/com/getavares/strava/StravaController.java`

### 2. **StravaService.java** (NOVO - 10 min)
- ✅ Criar service layer para business logic
- ✅ Separar OAuth logic
- ✅ Token refresh automático
- ✅ Tratamento de erros

**Arquivo:** `strava-spring/src/main/java/com/getavares/strava/StravaService.java`

### 3. **TokenService.java** (NOVO - 8 min)
- ✅ Gerenciamento de tokens
- ✅ Refresh automático
- ✅ Persistência em arquivo
- ✅ Validação de expiração

**Arquivo:** `strava-spring/src/main/java/com/getavares/strava/TokenService.java`

### 4. **GlobalExceptionHandler.java** (NOVO - 5 min)
- ✅ Tratamento centralizado de exceções
- ✅ Custom exceptions
- ✅ Respostas de erro consistentes

**Arquivo:** `strava-spring/src/main/java/com/getavares/strava/exception/GlobalExceptionHandler.java`

### 5. **CustomExceptions.java** (NOVO - 3 min)
- ✅ StravaAPIException
- ✅ TokenRefreshException
- ✅ ActivityFetchException

**Arquivo:** `strava-spring/src/main/java/com/getavares/strava/exception/CustomExceptions.java`

### 6. **application.properties** (2 min)
- ✅ Configuração de logging
- ✅ Server port, profiles
- ✅ Timeout settings

**Arquivo:** `strava-spring/src/main/resources/application.properties`

### 7. **pom.xml** Updates (2 min)
- ✅ Adicionar SLF4J/Logback
- ✅ Validação (Jakarta Validation)
- ✅ Versão Java 21

**Arquivo:** `strava-spring/pom.xml`

### 8. **StravaSpringApplicationTests.java** (5 min)
- ✅ Testes unitários básicos
- ✅ Teste de controller
- ✅ Teste de service

**Arquivo:** `strava-spring/src/test/java/com/getavares/strava/StravaSpringApplicationTests.java`

---

## 🎯 Estrutura de Pacotes Resultante

```
strava-spring/src/main/java/com/getavares/strava/
├── StravaSpringApplication.java      (Main - sem mudanças)
├── StravaController.java             (REFATORADO - validação, responses)
├── StravaService.java                (NOVO - business logic)
├── config/
│   ├── WebConfig.java                (NOVO - CORS, interceptors)
│   └── RestTemplateConfig.java       (NOVO - HTTP client config)
├── service/
│   ├── StravaService.java            (Alternativa: mover aqui)
│   ├── TokenService.java             (Token management)
│   └── ActivityService.java          (NOVO - atividades)
├── exception/
│   ├── GlobalExceptionHandler.java   (Centralized error handling)
│   ├── StravaAPIException.java       (Custom exception)
│   ├── TokenRefreshException.java    (Custom exception)
│   └── ActivityFetchException.java   (Custom exception)
├── model/
│   ├── Activity.java                 (NOVO - JPA entity)
│   ├── Token.java                    (NOVO - Token entity)
│   └── ApiResponse.java              (NOVO - Response wrapper)
├── dto/
│   ├── TokenRequest.java             (NOVO - DTO)
│   ├── ActivityDTO.java              (NOVO - DTO)
│   └── ErrorResponse.java            (NOVO - Error DTO)
└── repository/
    ├── ActivityRepository.java       (NOVO - Spring Data JPA)
    └── TokenRepository.java          (NOVO - Spring Data JPA)
```

---

## 📝 Implementação Rápida (Ordem Recomendada)

### Passo 1: CustomExceptions.java (3 min)
Criar arquivo base de exceções

### Passo 2: TokenService.java (8 min)
Gerenciador de tokens com refresh automático

### Passo 3: StravaService.java (10 min)
Lógica de negócio separada do controller

### Passo 4: GlobalExceptionHandler.java (5 min)
Tratamento centralizado de erros

### Passo 5: StravaController.java (10 min)
Refatorar controller com validação

### Passo 6: application.properties (2 min)
Configurar logging e profiles

### Passo 7: pom.xml (2 min)
Adicionar dependências

### Passo 8: Testes (5 min)
Implementar testes JUnit 5

---

## 🚀 Quick Implementation Guide

**CustomExceptions** (3 min):
```java
public class StravaAPIException extends RuntimeException { }
public class TokenRefreshException extends RuntimeException { }
public class ActivityFetchException extends RuntimeException { }
```

**TokenService** (8 min):
- readTokens() - Lê de tokens.json
- saveTokens() - Salva tokens
- refreshTokenIfNeeded() - Refresh automático
- isTokenExpired() - Validação

**StravaService** (10 min):
- authorizeUser(code) - OAuth flow
- getActivities(accessToken) - Buscar atividades
- enrichWithWeather(activities) - Chama FastAPI

**GlobalExceptionHandler** (5 min):
- @ExceptionHandler(StravaAPIException.class)
- @ExceptionHandler(TokenRefreshException.class)
- ErrorResponse wrapper

**StravaController** (10 min):
- Validar inputs com @Valid
- Usar ResponseEntity
- Delegar lógica para StravaService
- Retornar ApiResponse<T>

---

## ✅ Checklist de Conclusão

- [ ] CustomExceptions criadas
- [ ] TokenService implementado
- [ ] StravaService implementado
- [ ] GlobalExceptionHandler criado
- [ ] StravaController refatorado
- [ ] application.properties atualizado
- [ ] pom.xml atualizado
- [ ] Testes criados e passando
- [ ] Build sem erros (`mvn clean package`)
- [ ] Docker build funciona
- [ ] Commit e push realizados

---

## ⏱️ Timeline

| Minuto | Tarefa | Status |
|--------|--------|--------|
| 0-3 | CustomExceptions | ⏳ |
| 3-11 | TokenService | ⏳ |
| 11-21 | StravaService | ⏳ |
| 21-26 | GlobalExceptionHandler | ⏳ |
| 26-36 | StravaController refactor | ⏳ |
| 36-38 | application.properties | ⏳ |
| 38-40 | pom.xml updates | ⏳ |
| 40-45 | Testes + verificação final | ⏳ |

---

**Iniciado:** Agora  
**Estimado para conclusão:** +45 minutos

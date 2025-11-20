# 🤝 CONTRIBUTING.md - Guia de Contribuição

Obrigado por interesse em contribuir para o **Strava Connect**! Este documento delineia as diretrizes para contribuir ao projeto.

---

## 📋 Índice

- [Código de Conduta](#código-de-conduta)
- [Como Contribuir](#como-contribuir)
- [Processo de Contribuição](#processo-de-contribuição)
- [Padrões de Código](#padrões-de-código)
- [Convenção de Commits](#convenção-de-commits)
- [Dúvidas e Suporte](#dúvidas-e-suporte)

---

## 💬 Código de Conduta

### Nossas Responsabilidades

- Usar linguagem respeitosa e inclusiva
- Ser receptivo a críticas construtivas
- Focar no que é melhor para a comunidade
- Demonstrar empatia com outros membros

### Comportamentos Inaceitáveis

- Linguagem ou imagery sexualizada
- Trolagem, comentários insultuosos ou ataques pessoais
- Assédio público ou privado
- Publicar informações privadas de terceiros
- Qualquer comportamento que viole a ética profissional

**Consequências:** Comportamento inaceitável resultará em ban da comunidade.

---

## 💡 Como Contribuir

### 1️⃣ Reportando Bugs

Encontrou um bug? Ótimo! Aqui está como reportar:

**Antes de Reportar:**
- Verifique se o bug já foi reportado em Issues
- Teste em múltiplos navegadores/ambientes
- Reúna informações de debug

**Ao Reportar:**

```markdown
## Descrição do Bug
[Descrição clara do bug]

## Como Reproduzir
1. Fazer isso...
2. Depois isso...
3. Bug ocorre

## Comportamento Esperado
[O que deveria acontecer]

## Informações do Ambiente
- OS: [Windows/Linux/macOS]
- Navegador: [Chrome/Firefox/Safari]
- Versão Java: [21/17/11]
- Versão Python: [3.11/3.12]
- Versão Docker: [20.10+]

## Logs/Screenshots
[Anexe logs ou screenshots]

## Contexto Adicional
[Qualquer outra informação relevante]
```

**Issue Template:** Use a template de bug do GitHub

---

### 2️⃣ Sugestões de Features

Quer uma nova feature? Vamos ajudar!

**Antes de Sugerir:**
- Cheque o ROADMAP.md
- Pesquise issues e discussions
- Considere o escopo do projeto

**Ao Sugerir:**

```markdown
## Descrição da Feature
[Descrição clara e concisa]

## Problema que Resolve
[Qual problema esse feature resolve?]

## Exemplo de Uso
[Como seria usado?]

## Possível Implementação
[Ideias técnicas (opcional)]

## Contexto Adicional
[Screenshots, links, referências]
```

---

### 3️⃣ Pull Requests

**Tipos de Contribuições Bem-Vindas:**

- Bug fixes
- Feature implementations
- Documentação melhorada
- Testes adicionais
- Otimizações de performance
- Melhorias de UI/UX

**Tipos de Contribuições Menos Prioridade:**

- Mudanças cosméticas
- Refatoração sem propósito
- Mudanças de estilo

---

## 🔄 Processo de Contribuição

### Passo 1: Fork o Repositório

```bash
# No GitHub, clique "Fork"
https://github.com/getavares/strava-connect-java-getavares
```

### Passo 2: Clone seu Fork

```bash
git clone https://github.com/seu-usuario/strava-connect-java-getavares.git
cd strava-connect-java-getavares
```

### Passo 3: Crie uma Branch

```bash
# Para features:
git checkout -b feature/sua-feature-descritiva

# Para bugs:
git checkout -b fix/bug-descritivo

# Para documentação:
git checkout -b docs/sua-documentacao

# Para testes:
git checkout -b test/sua-test-descritiva
```

### Passo 4: Faça suas Mudanças

**Trabalhe na sua feature:**
- Mantenha commits pequenos e focados
- Siga os padrões de código
- Adicione testes para novas funcionalidades
- Atualize documentação

### Passo 5: Commit suas Mudanças

Veja [Convenção de Commits](#convenção-de-commits) abaixo.

```bash
git add .
git commit -m "feat: adicionar feature incrível"
```

### Passo 6: Push para seu Fork

```bash
git push origin feature/sua-feature-descritiva
```

### Passo 7: Abra um Pull Request

**No GitHub:**
1. Vá para seu fork
2. Clique "Compare & pull request"
3. Descreva suas mudanças
4. Submita o PR

**Descrição do PR:**

```markdown
## Descrição
[O que essa PR faz?]

## Tipo de Mudança
- [ ] Bug fix
- [ ] Nova feature
- [ ] Breaking change
- [ ] Documentação

## Checklist
- [ ] Código segue style guidelines
- [ ] Testes adicionados
- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Sem breaking changes

## Testing
[Como testar?]

## Screenshots/Resultados
[Anexe se relevante]

## Closes
Closes #[issue number]
```

### Passo 8: Code Review

- Revise comentários do review
- Faça mudanças conforme necessário
- Responda com "LGTM" ou novo push

### Passo 9: Merge

Mantainers darão merge quando aprovado!

---

## 🎨 Padrões de Código

### Java (Spring Boot)

```java
// ✅ BOM
public class UserService {
    private final UserRepository userRepository;
    
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
    
    public User findById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException("User not found"));
    }
}

// ❌ RUIM
public class UserService {
    public static UserRepository userRepository = new UserRepository();
    
    public User findById(Long id) {
        return userRepository.findById(id);
    }
}
```

**Guia de Estilo Java:**
- Use Google Java Style Guide
- Máximo 100 caracteres por linha
- Use meaningful names
- DRY principle
- SOLID principles

**Testes:**
```java
@Test
@DisplayName("should find user by id when user exists")
void shouldFindUserByIdWhenUserExists() {
    // Arrange
    User expected = new User(1L, "John");
    when(userRepository.findById(1L)).thenReturn(Optional.of(expected));
    
    // Act
    User actual = userService.findById(1L);
    
    // Assert
    assertEquals(expected, actual);
}
```

### Python (FastAPI)

```python
# ✅ BOM
from typing import Optional
from fastapi import HTTPException

class StravaInsights:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def get_weather(self, latitude: float, longitude: float) -> dict:
        """Get weather data for coordinates."""
        return self.api_client.get_weather(latitude, longitude)

# ❌ RUIM
class StravaInsights:
    api_client = None
    
    def getWeather(self, lat, lng):
        return self.api_client.getWeather(lat, lng)
```

**Guia de Estilo Python:**
- Siga PEP 8
- Use type hints
- Docstrings para funções públicas
- Máximo 88 caracteres por linha
- Use black formatter

**Testes:**
```python
import pytest

def test_get_weather_returns_dict():
    """Should return weather data as dict."""
    # Arrange
    mock_client = Mock()
    mock_client.get_weather.return_value = {"temp": 25}
    insights = StravaInsights(mock_client)
    
    # Act
    result = insights.get_weather(0, 0)
    
    # Assert
    assert isinstance(result, dict)
    assert result["temp"] == 25
```

### Naming Conventions

```java
// Classes: PascalCase
public class UserService { }

// Variables/Methods: camelCase
private String firstName;
public void getUserById() { }

// Constants: UPPER_SNAKE_CASE
public static final int MAX_USERS = 1000;

// Packages: lowercase.with.dots
com.getavares.strava.service
```

---

## 📝 Convenção de Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/)

### Formato

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Tipos

- **feat**: Nova feature
- **fix**: Bug fix
- **docs**: Documentação
- **style**: Formatação, missing semicolons, etc
- **refactor**: Refatoração de código
- **perf**: Melhoria de performance
- **test**: Adicionando testes
- **chore**: Atualizações de deps, configs, etc

### Exemplos

```bash
# Boa feature
git commit -m "feat(api): add weather enrichment endpoint"

# Boa fix
git commit -m "fix(fastapi): handle missing weather data gracefully"

# Boa documentação
git commit -m "docs: add contribution guidelines"

# Com corpo
git commit -m "feat(insights): implement temperature-based analysis

- Add temperature bucketing algorithm
- Add statistics calculation
- Add test cases"
```

### Scope

Scopes comuns:
- `api`: API endpoints
- `auth`: Authentication
- `db`: Database
- `docs`: Documentação
- `tests`: Testes
- `ci`: CI/CD
- `deps`: Dependencies
- `config`: Configuração

---

## ✅ Checklist antes de Submeter PR

- [ ] Código segue padrões de código
- [ ] Testes adicionados/atualizados
- [ ] Todos os testes passam (`mvn test` ou `pytest`)
- [ ] Documentação atualizada
- [ ] Commits seguem convenção
- [ ] Sem conflitos com main
- [ ] Sem variavelsfora de uso (linting)
- [ ] Performance impactado negativamente? Documentar
- [ ] Segurança? Revisar (sem hardcoded secrets)
- [ ] Dependências? Documentar updates

---

## 🧪 Rodando Testes Localmente

### Java

```bash
cd strava-spring
mvn clean test
```

### Python

```bash
cd python-fastapi
python -m pytest -v
```

### Integração

```bash
# Com Docker
docker-compose up
# Em outro terminal
python python-fastapi/test_api.py
```

---

## 📚 Recursos Úteis

- [GitHub Docs](https://docs.github.com)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)
- [PEP 8](https://pep8.org/)
- [Spring Boot Docs](https://spring.io/projects/spring-boot)
- [FastAPI Docs](https://fastapi.tiangolo.com/)

---

## 🎓 Dúvidas e Suporte

- **Issues:** Para bugs e features
- **Discussions:** Para dúvidas e ideias
- **Email:** seu@email.com

---

## 🙏 Obrigado!

Sua contribuição torna este projeto melhor. Independente do tamanho da contribuição, é valorizada!

**Happy Contributing! 🚀**

---

**Última Atualização:** 20 de novembro de 2025

**Maintainer:** Rogério Tavares (@getavares)

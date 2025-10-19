# 🏃♂️ getavares-strava-api

Integração local com a **API do Strava**, desenvolvida em **Java (IntelliJ IDEA)**, para explorar dados de atleta, atividades e estatísticas via autenticação **OAuth 2.0**.  
Projeto criado por [Rogério Tavares](https://github.com/rogtavares) — *"Simple artist looking for an achievement."* 🎨

---

## 🚀 Objetivo
Este projeto demonstra como conectar uma aplicação Java local à **API do Strava**, realizar a autenticação do usuário e consumir dados reais do perfil de atleta.

Ele serve como base para futuras integrações com análise de performance, monitoramento via Datadog e extensões com AWS.

---

## 🧩 Tecnologias Utilizadas
- **Java 17+**
- **Maven**
- **IntelliJ IDEA**
- **Gson (Google)** — manipulação de JSON  
- **Apache HttpClient 5** — comunicação HTTP  
- **Strava API v3**

---

## ⚙️ Estrutura do Projeto

### Dependências Maven
```xml
<dependencies>
    <dependency>
        <groupId>com.google.code.gson</groupId>
        <artifactId>gson</artifactId>
        <version>2.10.1</version>
    </dependency>
    <dependency>
        <groupId>org.apache.httpcomponents.client5</groupId>
        <artifactId>httpclient5</artifactId>
        <version>5.2.1</version>
    </dependency>
</dependencies>
```

---

## 🔑 Criação da Aplicação no Strava

1. Acesse: [https://www.strava.com/settings/api](https://www.strava.com/settings/api)  
2. Clique em **Create & Manage Your App**
3. Preencha:
   - **Application Name:** `StravaLocalApp`
   - **Website:** `http://localhost`
   - **Authorization Callback Domain:** `localhost`
   - **Category:** `Other`
4. Salve e anote o `Client ID` e `Client Secret`

---

## 🔐 Autenticação OAuth 2.0

A autenticação segue o fluxo padrão do Strava:  
**Autorização → Código → Token de Acesso**

### 1️⃣ Obter o Código de Autorização
Acesse no navegador:

Após autorizar, será redirecionado para:

---

## 📊 Endpoints Utilizados

| Endpoint               | Descrição                                 |
| ---------------------- | ----------------------------------------- |
| `/athlete`             | Retorna informações do atleta autenticado |
| `/athlete/activities`  | Lista as atividades recentes              |
| `/athletes/{id}/stats` | Estatísticas gerais do atleta             |
| `/activities/{id}`     | Detalhes de uma atividade específica      |

---

## 📄 Licença

Este projeto é de uso livre para fins educacionais e demonstrações técnicas.  
© 2025 Rogério Tavares – Todos os direitos reservados.
# Strava Connect - Integração Completa com Análises Inteligentes

## 1. Abertura
- Projeto pessoal de integração com Strava
- Objetivo: estudar APIs, OAuth, Python e Java
- Aplicação real conectada ao dia a dia como atleta

## 2. Motivação
- Consolidar estudos em APIs e OAuth
- Entrega concreta para PDI. nov./2025

## 3. Objetivos do Projeto
- Integrar com API do Strava (OAuth 2.0)
- Consumir dados reais de treinos
- Criar análises automatizadas
  - Ritmo e pace
  - Potência
  - Zonas cardíacas
  - Insights inteligentes
- Preparar para IA futura

## 4. Arquitetura Geral
- Cliente
  - Navegador / Postman
- OAuth 2.0
- OAuth Strava
  - Autorização
  - Tokens
- Backend
  - Java Spring Boot
  - Python FastAPI
- Processamento
  - Análises
  - Enriquecimento com clima ( futuro)
- Dashboard
  - datadog (futuro)

## 5. Tecnologias Utilizadas
- Backend
  - Java 21
  - Spring Boot 3.2
  - Python 3.11+
  - FastAPI
- Autenticação
  - OAuth 2.0
  - Requests-OAuthlib

- Cloud (futuro)
  - AWS Lambda
  - API Gateway
  - Bedrock (IA)
- DevOps
  - Git/GitHub
  - Maven
  - Docker

## 6. Fluxo OAuth 2.0
- Passo 1: Usuário acessa endpoint
- Passo 2: Redirecionamento para Strava
- Passo 3: Usuário autoriza aplicação
- Passo 4: Strava retorna código
- Passo 5: Backend troca código por token
- Passo 6: Chamadas autenticadas à API

## 7. Funcionalidades Implementadas
- Autenticação OAuth completa
- Busca de dados do atleta
- Listagem de atividades
- Enriquecimento com clima
  - OpenWeather API
  - Dados históricos
- Análises inteligentes
  - Performance por condição climática
  - Impacto do vento
  - Melhor temperatura para treino
  - Zonas cardíacas
  - Distribuição de ritmo

## 8. Exemplo de Dados
- Perfil do Atleta
  - ID: 3329857
  - Nome e foto
  - Estatísticas totais
- Atividades
  - Distância
  - Tempo
  - Pace
  - Frequência cardíaca
  - Elevação
- Insights
  - "Você corre melhor em dias com 18°C"
  - "Vento reduz seu pace em 8.5%"
  - "Melhor horário: manhã"

## 9. Análises Inteligentes
- Rule-based (atual)
  - Zonas cardíacas
  - Distribuição de ritmo
  - Comparação de treinos
  - Tendências
- IA (próximo release)
  - Amazon Bedrock
  - Insights personalizados
  - Recomendações automáticas

## 10. Próximos Passos
- Frontend
  - Dashboard HTML + Python E dataDog
  - Interface responsiva
- Cloud
  - Deploy AWS Lambda
  - API Gateway
  - CloudWatch
- Integrações
  - Notificações personalizadas
  - Datadog (logs e métricas)
- IA
  - Amazon Bedrock
  - Análises preditivas

## 11. Resultados Alcançados
- Backend Java funcionando
- API FastAPI rodando
- OAuth 2.0 implementado
- 10 guias de documentação
- Código no GitHub
- Ambiente completo configurado
- Pronto para demonstração

## 12. Conclusão
- Integra tecnologia e performance

- Desenvolvimento em:
  - APIs REST
  - OAuth 2.0
  - AWS
  - Integrações
  - IA (futuro)
- Obrigado!
  - Perguntas?
  - GitHub: rogtavares/strava-connect-java-getavares

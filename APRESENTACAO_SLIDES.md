# 🎤 Apresentação: Strava Connect

## Slide 1:
```
🏃 strava-connect-java-getavares


Rogério Tavares
Atleta ID: 3329857
GitHub: rogtavares/strava-connect-java-getavares
```

---

## Slide 2: PDI
```
POR QUE ESTE PROJETO?

✅ Consolidar estudos em APIs e OAuth
✅ Criar produto real para portfólio
✅ Demonstrar habilidades técnicas
✅ Entrega concreta para PDI
✅ Aplicação prática no dia a dia
```

---

## Slide 3: Objetivos
```
OBJETIVOS DO PROJETO

1. Integrar com API do Strava (OAuth 2.0)
2. Consumir dados reais de treinos
3. Criar análises automatizadas
4. Gerar insights inteligentes
5. Desenvolver API REST com Java

---

## Slide 4: Arquitetura
```
ARQUITETURA GERAL

Cliente → OAuth Strava → Backend → Processamento → Dashboard

Componentes:
• Java Spring Boot (porta 8081)
• Python FastAPI (porta 8000)
• Streamlit Dashboard
• AWS Lambda (futuro)

---

## Slide 5: Tecnologias

Backend:
• Java 21 + Spring Boot 3.2
• Python 3.11+ + FastAPI

Autenticação:
• OAuth 2.0
• Requests-OAuthlib

Análises:
• Pandas, Matplotlib
• OpenWeather API

Cloud (futuro):
• AWS Lambda + API Gateway
• Amazon Bedrock (IA)
---

## Slide 6: OAuth 2.0
```
FLUXO DE AUTENTICAÇÃO

1. vc acessa endpoint local
2. Redirecionamento para Strava
3. vc autoriza aplicação
4. Strava retorna código
5. Backend troca código por token
6. Chamadas autenticadas à API

✅ Implementado e funcionando!
```

---

## Slide 7: Funcionalidades
```
O QUE JÁ FUNCIONA

✅ Autenticação OAuth completa
✅ Busca de dados do atleta
✅ Listagem de atividades
✅ Enriquecimento com clima
✅ Análises inteligentes
✅ API REST documentada (Swagger)
✅ Dashboard interativo ((NAO CONSEGUI TERMINAR))
```

---

## Slide 8: Exemplo de Dados
```
DADOS REAIS DO STRAVA

Perfil:
• ID: 3329857
• Nome, foto, estatísticas

Atividades:
• Distância: 5.000m
• Tempo: 30min
• Pace: 6:00 min/km
• FC média: 145 bpm
• Elevação: 50m
```

---

## Slide 9: Insights Inteligentes
```
ANÁLISES GERADAS

🌡️ "Você corre melhor em dias com 18°C"
💨 "Vento reduz seu pace em 8.5%"
⏰ "Melhor horário: manhã"
❤️ "Zona cardíaca ideal: 140-150 bpm"
📊 "Tendência: melhora de 5% no último mês"

Próximo: Amazon Bedrock para IA
```

---

## Slide 10: Demonstração
```
DEMO AO VIVO

1. API FastAPI rodando
   http://localhost:8000/docs

2. Endpoints testados
   GET /health ✅
   GET /insights ✅

3. Backend Java pronto
   http://localhost:8081/api/auth
```

---

## Slide 11: Próximos Passos
```
ROADMAP

Curto Prazo:
• Frontend responsivo
• Deploy AWS Lambda
• Notificações personalizadas

Médio Prazo:
• Integração Datadog
• Publicação social automática
• Amazon Bedrock (IA)

Longo Prazo:
• App mobile
• Análises preditivas
• Comunidade de atletas
```

---

## Slide 12: Resultados
```
O QUE FOI ENTREGUE

✅ Backend Java funcionando
✅ API FastAPI rodando
✅ OAuth 2.0 implementado
✅ Documentação
✅ Código no GitHub
✅ Ambiente completo configurado
✅ Pronto para demonstração

PRÓXIMOS PASSOS

---

## Slide 13: Conclusão
```
CONCLUSÃO

Este projeto integra:
• Tecnologia moderna
• Performance esportiva
• Dados reais e aplicáveis

Demonstra habilidades em:
• APIs REST
• OAuth 2.0
• AWS
• Integrações
• IA (futuro)

OBRIGADO!
Perguntas?

GitHub: rogtavares/strava-connect-java-getavares
```

---

## Como Usar

### Opção 1: Markmap (Visual)
1. Instale: `npm install -g markmap-cli`
2. Gere: `markmap APRESENTACAO_MARKMAP.md`
3. Abra no navegador

### Opção 2: Marp (Slides)
1. Instale extensão Marp no VS Code
2. Abra `APRESENTACAO_SLIDES.md`
3. Exporte para PDF ou HTML

### Opção 3: Reveal.js
1. Use online: https://revealjs.com/
2. Cole o conteúdo
3. Apresente direto do navegador

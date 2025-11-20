Strava Spring Example

Variáveis de ambiente necessárias:
- STRAVA_CLIENT_ID
- STRAVA_CLIENT_SECRET
- STRAVA_REDIRECT_URI (ex.: http://localhost:8080/callback)

Como rodar (maven):

mvn -f strava-spring/pom.xml spring-boot:run

Endpoints:
- GET /authorize -> link para iniciar OAuth
- GET /callback?code=... -> troca código por token e armazena em memória
- GET /activities/export -> retorna activities (raw JSON)

@echo off
echo ========================================
echo INICIAR BACKEND COM VARIAVEIS DE AMBIENTE
echo ========================================
echo.

REM Configurar variáveis de ambiente
REM IMPORTANTE: Substitua com suas NOVAS credenciais
set STRAVA_CLIENT_ID=seu_novo_client_id
set STRAVA_CLIENT_SECRET=seu_novo_client_secret
set STRAVA_REDIRECT_URI=http://localhost:8081/callback

echo Variáveis configuradas:
echo CLIENT_ID: %STRAVA_CLIENT_ID%
echo REDIRECT_URI: %STRAVA_REDIRECT_URI%
echo.

cd strava-spring

echo Iniciando backend...
echo.
mvn spring-boot:run

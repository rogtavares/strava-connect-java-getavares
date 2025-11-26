@echo off
echo ========================================
echo INICIAR BACKEND COM VARIAVEIS DE AMBIENTE
echo ========================================
echo.

REM Configurar variáveis de ambiente
set STRAVA_CLIENT_ID=181788
set STRAVA_CLIENT_SECRET=9b73316f1bad61de6e0be4822afc55c4278b20f2
set STRAVA_REDIRECT_URI=http://localhost:8081/callback

echo Variáveis configuradas:
echo CLIENT_ID: %STRAVA_CLIENT_ID%
echo REDIRECT_URI: %STRAVA_REDIRECT_URI%
echo.

cd strava-spring

echo Iniciando backend...
echo.
mvn spring-boot:run

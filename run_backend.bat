@echo off
echo ========================================
echo   Configurando ambiente Strava
echo ========================================
set STRAVA_CLIENT_ID=181788
set STRAVA_CLIENT_SECRET=9b73316f1bad61de6e0be4822afc55c4278b20f2
set STRAVA_REDIRECT_URI=http://localhost:8081/api/callback

echo.
echo Variaveis configuradas:
echo CLIENT_ID: %STRAVA_CLIENT_ID%
echo REDIRECT_URI: %STRAVA_REDIRECT_URI%
echo.
echo ========================================
echo   Iniciando Backend Java Spring Boot
echo ========================================
cd strava-spring
mvn spring-boot:run

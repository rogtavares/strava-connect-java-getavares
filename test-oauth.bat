@echo off
echo ========================================
echo TESTE OAUTH 2.0 - STRAVA CONNECT
echo ========================================
echo.

echo [1/3] Verificando backend...
curl -s http://localhost:8081/authorize >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Backend nao esta rodando na porta 8081
    echo Execute: cd strava-spring ^&^& mvn spring-boot:run
    exit /b 1
)
echo OK: Backend rodando

echo.
echo [2/3] Testando endpoint /authorize...
curl -s http://localhost:8081/authorize
echo.

echo.
echo [3/3] Instrucoes:
echo 1. Abra no navegador: http://localhost:8081/authorize
echo 2. Clique no link "Authorize with Strava"
echo 3. Faca login e autorize
echo 4. Apos callback, acesse: http://localhost:8081/activities/export
echo.
echo ========================================

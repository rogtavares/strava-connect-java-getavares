@echo off
echo ========================================
echo REINICIAR BACKEND - STRAVA CONNECT
echo ========================================
echo.

echo [1/4] Parando processos Java na porta 8081...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8081') do (
    taskkill /F /PID %%a >nul 2>&1
)
echo OK: Processos finalizados

echo.
echo [2/4] Aguardando 3 segundos...
timeout /t 3 /nobreak >nul
echo OK: Aguardado

echo.
echo [3/4] Recompilando projeto...
cd strava-spring
call mvn clean compile -q
if %errorlevel% neq 0 (
    echo ERRO: Falha na compilacao
    pause
    exit /b 1
)
echo OK: Projeto compilado

echo.
echo [4/4] Iniciando backend...
echo.
echo ========================================
echo Backend iniciando na porta 8081...
echo Aguarde mensagem: "Started StravaApplication"
echo.
echo Apos iniciar, acesse:
echo http://localhost:8081/authorize
echo ========================================
echo.

call mvn spring-boot:run

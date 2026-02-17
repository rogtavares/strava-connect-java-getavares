@echo off
echo 🚀 Iniciando Ambiente Completo (API + Dashboard)...

start "Strava API" cmd /k "cd ..\api-RT && python run.py"
timeout /t 5

start "Strava Dashboard" cmd /k "cd ..\dashboard && streamlit run app.py"

echo ✅ Ambiente iniciado!
echo 📡 API: http://localhost:8000
echo 📊 Dashboard: http://localhost:8501
pause
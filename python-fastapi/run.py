import uvicorn
import os
import sys

if __name__ == "__main__":
    # Adiciona o diretório atual ao path do Python para garantir que 'app' seja encontrado
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    print("🚀 Iniciando servidor Strava Connect...")
    print("📂 Diretório de trabalho:", os.getcwd())
    
    # Roda o servidor importando a string "app:app"
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

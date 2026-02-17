import uvicorn
from app import app

if __name__ == "__main__":
    print("Iniciando API FastAPI...")
    print("Acesse: http://localhost:8000")
    print("Documentacao: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Servidor Mínimo Funcionando!"}

if __name__ == "__main__":
    print("🚀 Iniciando servidor mínimo na porta 8001...")
    uvicorn.run(app, host="127.0.0.1", port=8001)

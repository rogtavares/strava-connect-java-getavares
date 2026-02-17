import socket
import time
import threading
import uvicorn
import requests
import sys
import os

def check_port(port):
    """Check if port is open"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

def run_server():
    """Run uvicorn server programmatically"""
    print("🚀 Tentando iniciar servidor Uvicorn na porta 8000...")
    try:
        # Import app here to avoid circular imports if app has issues
        sys.path.append(os.getcwd())
        from app import app
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")

def diagnose():
    print("🔍 Iniciando diagnóstico do servidor FastAPI...\n")

    # 1. Check if port is already in use
    if check_port(8000):
        print("⚠️ A porta 8000 JÁ ESTÁ em uso.")
        print("   Isso significa que o servidor já pode estar rodando ou outro programa está usando a porta.")
        print("   Tentando conectar...")
    else:
        print("ℹ️ A porta 8000 está livre. Iniciando servidor de teste...")
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        time.sleep(3) # Wait for server to start

    # 2. Try to connect
    try:
        print("\n📡 Tentando conectar em http://127.0.0.1:8000/ ...")
        response = requests.get("http://127.0.0.1:8000/", timeout=2)
        
        if response.status_code == 200:
            print("✅ SUCESSO! O servidor respondeu corretamente.")
            print(f"   Resposta: {response.json()}")
            print("\n👉 Se o Insomnia não conecta, verifique se ele está usando 'localhost' ou '127.0.0.1'.")
            print("   Tente trocar 'localhost' por '127.0.0.1' no Insomnia.")
        else:
            print(f"⚠️ O servidor respondeu, mas com erro: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ FALHA: Não foi possível conectar ao servidor.")
        print("   Possíveis causas:")
        print("   1. O servidor não iniciou corretamente (verifique erros acima).")
        print("   2. Firewall ou antivírus bloqueando a conexão.")
    except Exception as e:
        print(f"❌ Erro inesperado ao conectar: {e}")

if __name__ == "__main__":
    diagnose()

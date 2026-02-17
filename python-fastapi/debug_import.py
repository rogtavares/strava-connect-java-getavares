import sys
import traceback

print("🔍 Tentando importar 'app'...")

try:
    import app
    print("✅ Importação bem sucedida!")
except Exception as e:
    print("\n❌ ERRO AO IMPORTAR 'app':")
    traceback.print_exc()

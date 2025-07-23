#!/usr/bin/env python3
"""
🚀 RED SOLUCIONES ISP v1.0.0 - SERVIDOR DE PRODUCCIÓN
"""
import sys
import os
from pathlib import Path

# Configurar paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
os.environ['PYTHONPATH'] = str(project_root)

def main():
    print("🚀 Iniciando Red Soluciones ISP v1.0.0")
    print("=" * 50)
    print(f"📁 Directorio: {project_root}")
    print("🌐 Servidor: http://localhost:8004")
    print("📊 Dashboard: http://localhost:8004")
    print("📚 API Docs: http://localhost:8004/docs")
    print("🧪 Verificación: python3 final_verification.py")
    print("=" * 50)
    print("✅ Estado: Producción v1.0.0")
    print()
    
    try:
        import uvicorn
        uvicorn.run(
            "backend.app.main:app",
            host="0.0.0.0",
            port=8004,
            reload=False,
            log_level="info"
        )
    except ImportError:
        print("❌ Error: uvicorn no instalado")
        print("💡 Ejecuta: pip install uvicorn")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

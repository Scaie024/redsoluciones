#!/usr/bin/env python3
"""
Script para iniciar Red Soluciones ISP
"""
import os
import subprocess
import sys
from pathlib import Path

def main():
    print("🚀 Iniciando Red Soluciones ISP...")
    print("=" * 50)
    
    # Cambiar al directorio del proyecto
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Configurar variables de entorno
    os.environ["PYTHONPATH"] = str(project_dir)
    
    print(f"📁 Directorio: {project_dir}")
    print("🌐 Iniciando servidor UNIFICADO en http://localhost:8000")
    print("=" * 50)
    print("✅ Sistema listo!")
    print("📱 Dashboard: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("❤️  Health: http://localhost:8000/health")
    print("🔌 Dashboard API: http://localhost:8000/api/dashboard")
    print("=" * 50)
    
    try:
        # Importar y ejecutar la aplicación UNIFICADA
        import uvicorn
        from app import app  # <-- Usar el app.py unificado
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000, # Puerto estándar unificado
            reload=True,
            log_level="info"
        )
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("📦 Instalando dependencias...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas. Reiniciando...")
        
        import uvicorn
        from app import app
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )

if __name__ == "__main__":
    main()

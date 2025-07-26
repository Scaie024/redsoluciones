#!/usr/bin/env python3
"""
Servidor de desarrollo para Red Soluciones ISP
Punto de entrada simple y unificado para desarrollo local
"""

import uvicorn
import os
import sys
from pathlib import Path

def main():
    print("🚀 Red Soluciones ISP - Servidor de Desarrollo")
    print("=" * 50)
    
    # Configurar path del proyecto
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    # Configurar variables de entorno para desarrollo
    os.environ.setdefault("GOOGLE_SHEET_ID", "1OZKZIpn6U1nCfrDM_yGmC6jKj6iLH_MQz814LjEBRMQ")
    os.environ.setdefault("DEBUG", "True")
    os.environ.setdefault("ENVIRONMENT", "development")
    
    print("✨ Configuración:")
    print("   • Puerto: 8000")
    print("   • Host: 0.0.0.0")
    print("   • Modo: Desarrollo")
    print("   • Hot Reload: Activado")
    print("   • App: backend.app.main:app")
    print("")
    print("🌐 URLs disponibles:")
    print("   • Dashboard: http://localhost:8000/")
    print("   • API Health: http://localhost:8000/health")
    print("   • API Chat: http://localhost:8000/api/chat")
    print("")
    print("Presiona Ctrl+C para detener")
    print("=" * 50)
    
    # Iniciar servidor con la aplicación unificada
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(project_root / "backend"), str(project_root / "frontend")],
        log_level="info"
    )

if __name__ == "__main__":
    main()
    print("🔗 URLs disponibles:")
    print("   • API Principal: http://localhost:8000/")
    print("   • Demo Interactiva: http://localhost:8000/demo")
    print("   • Estado Sistema: http://localhost:8000/health")
    print("   • Documentación: http://localhost:8000/docs")
    print("")
    print("🔥 Iniciando servidor...")
    print("Para detener: Ctrl+C")
    print("=" * 50)
    
    # Configurar variables de entorno para desarrollo
    os.environ["ENVIRONMENT"] = "development"
    os.environ["DEBUG"] = "true"
    
    # Ejecutar servidor con hot reload
    uvicorn.run(
        "app:app",  # Import string para habilitar reload
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        reload_dirs=[str(Path.cwd())]
    )

if __name__ == "__main__":
    main()

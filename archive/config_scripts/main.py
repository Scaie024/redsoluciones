#!/usr/bin/env python3
"""
RED SOLUCIONES ISP - SISTEMA UNIFICADO
=====================================
Versión limpia y funcional del sistema ISP
Con integración completa de Google Sheets e IA
"""

import os
import sys
import uvicorn
from pathlib import Path

# Agregar el directorio backend al path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from backend.app.main_unified import app

def main():
    """Función principal para ejecutar el sistema"""
    print("🚀 RED SOLUCIONES ISP - SISTEMA UNIFICADO v5.0")
    print("=" * 60)
    print("📅 Iniciando sistema...")
    print("🌍 Puerto: 8004")
    print("📱 Dashboard: http://localhost:8004")
    print("📱 Dashboard Limpio: http://localhost:8004/frontend/dashboard.html")
    print("=" * 60)
    
    # Configurar y ejecutar el servidor
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8004,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    main()

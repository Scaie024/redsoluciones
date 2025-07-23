#!/usr/bin/env python3
"""
Servidor simplificado para Red Soluciones ISP
"""
import sys
import os
from pathlib import Path

# Agregar el directorio del proyecto al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
os.environ['PYTHONPATH'] = str(project_root)

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Iniciando Red Soluciones ISP Server...")
    print(f"📁 Directorio del proyecto: {project_root}")
    print("🌐 Servidor disponible en: http://localhost:8004")
    print("📊 Panel principal: http://localhost:8004/index.html")
    
    # Iniciar servidor
    uvicorn.run(
        "backend.app.main:app", 
        host="0.0.0.0", 
        port=8004, 
        reload=False,
        log_level="info"
    )

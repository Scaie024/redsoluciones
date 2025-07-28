"""
Red Soluciones ISP - Entry Point Principal
==========================================
Punto de entrada unificado para desarrollo y producción
Importa la aplicación principal desde backend
"""

import sys
from pathlib import Path

# Configurar path del proyecto
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Importar aplicación principal desde backend
from backend.app.main import app

# Exportar para Vercel y servidores
__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando Red Soluciones ISP...")
    uvicorn.run(
        app,
        host="0.0.0.0", 
        port=8004,
        reload=True
    )

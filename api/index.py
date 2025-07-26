"""
Red Soluciones ISP - API Gateway para Vercel
Punto de entrada unificado que importa la aplicación principal
"""

import sys
from pathlib import Path

# Configurar el path para importar desde backend
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

# Importar la aplicación principal desde backend
from backend.app.main import app

# Exportar para Vercel
__all__ = ["app"]

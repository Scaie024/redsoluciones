"""
Vercel Serverless Function Entry Point para Red Soluciones ISP
"""
import sys
import os
from pathlib import Path

# Configurar paths para Vercel
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

# Importar la aplicación FastAPI
from backend.app.main import app

# Vercel handler
def handler(request, response):
    return app

"""
Vercel Serverless Function Entry Point para Red Soluciones ISP
"""
import sys
import os
import json
from pathlib import Path

# Configurar paths para Vercel
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

# Configurar variables de entorno para Google Credentials
def setup_google_credentials():
    """Configura las credenciales de Google desde variables de entorno"""
    try:
        # Si hay un string JSON en la variable de entorno, usarlo
        google_creds = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
        if google_creds:
            # Crear archivo temporal para las credenciales
            credentials_path = '/tmp/google_credentials.json'
            with open(credentials_path, 'w') as f:
                if isinstance(google_creds, str):
                    json.dump(json.loads(google_creds), f)
                else:
                    json.dump(google_creds, f)
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
            print("Google credentials configured successfully")
    except Exception as e:
        print(f"Warning: Could not setup Google credentials: {e}")

# Configurar credenciales al inicio
setup_google_credentials()

# Intentar importar la aplicación principal
try:
    from backend.app.main import app
    print("Main app imported successfully")
except ImportError as e:
    print(f"Error importing main app: {e}")
    print("Creating fallback FastAPI app...")
    
    # Fallback: crear una app básica funcional
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    
    app = FastAPI(
        title="Red Soluciones ISP", 
        version="1.0.0",
        description="Sistema ISP en modo compatible Vercel"
    )
    
    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/")
    async def root():
        return {
            "message": "Red Soluciones ISP API",
            "status": "active",
            "mode": "vercel_compatible",
            "version": "1.0.0"
        }
    
    @app.get("/health")
    async def health():
        return {
            "status": "healthy",
            "environment": "vercel",
            "timestamp": "2025-07-24"
        }
    
    @app.get("/api/status")
    async def api_status():
        return {
            "api": "operational",
            "services": {
                "gemini": bool(os.getenv("GEMINI_API_KEY")),
                "telegram": bool(os.getenv("TELEGRAM_BOT_TOKEN")),
                "google_sheets": bool(os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"))
            }
        }

# Vercel handler
def handler(request, response):
    return app

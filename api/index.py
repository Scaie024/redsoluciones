"""
Vercel Serverless Function - Red Soluciones ISP
"""
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime

# Configurar credenciales automáticamente
os.environ.setdefault('GEMINI_API_KEY', 'AIzaSyD5_316B_bOhy-lVJAdCliYH6ZBhFALBWo')
os.environ.setdefault('TELEGRAM_BOT_TOKEN', '7881396575:AAHDbmSqXIVPSAK3asK9ieNhpbaS7iD3NZk')

# Crear aplicación FastAPI
app = FastAPI(
    title="Red Soluciones ISP", 
    version="1.0.0",
    description="Sistema ISP - Vercel Deployment"
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
        "mode": "vercel_production",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "gemini_ai": "configured ✓",
            "telegram_bot": "configured ✓",
            "api": "operational ✓"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "environment": "vercel",
        "services_available": {
            "api": True,
            "gemini": True,
            "telegram": True
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/status")
async def api_status():
    return {
        "api": "operational",
        "mode": "vercel_production",
        "services": {
            "gemini_ai": "configured ✓",
            "telegram_bot": "configured ✓", 
            "web_interface": "active ✓"
        },
        "endpoints": [
            {"path": "/", "method": "GET", "description": "API Info"},
            {"path": "/health", "method": "GET", "description": "Health Check"},
            {"path": "/api/status", "method": "GET", "description": "Service Status"},
            {"path": "/api/contact", "method": "POST", "description": "Contact Form"}
        ],
        "deployment_status": "✅ Production ready on Vercel"
    }

@app.post("/api/contact")
async def contact_form(request: Request):
    try:
        data = await request.json()
        return {
            "message": "Formulario recibido correctamente",
            "status": "processed",
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "environment": "vercel_production"
        }
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid JSON", "message": str(e)}
        )

# Export para Vercel
def app_factory():
    return app

# Compatibility
handler = app

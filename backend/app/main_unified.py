"""
RED SOLUCIONES ISP - SISTEMA UNIFICADO v5.0
==========================================
Sistema completo de gestión ISP con IA integrada
Versión limpia y funcional
"""

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel
from pathlib import Path
from typing import Optional, Dict, List, Any
import logging
import os
from datetime import datetime

# Servicios del sistema
from backend.app.services.sheets.service import SheetsServiceV2
from backend.app.services.context_engine import ContextEngine
from backend.app.services.enhanced_agent import HomologatedAIAgent

# === CONFIGURACIÓN ===
PROJECT_NAME = "Red Soluciones ISP"
VERSION = "5.0 Unificado"
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# === APLICACIÓN FASTAPI ===
app = FastAPI(
    title=PROJECT_NAME,
    description="Sistema ISP unificado con IA y Google Sheets",
    version=VERSION,
    debug=DEBUG
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === SERVICIOS GLOBALES ===
sheets_service = None
context_engine = None
ai_agent = None

# === MODELOS PYDANTIC ===
class ChatMessage(BaseModel):
    message: str
    user: Optional[str] = "Eduardo"

class AuthRequest(BaseModel):
    username: str
    password: str

# === INICIALIZACIÓN ===
@app.on_event("startup")
async def startup_event():
    """Inicializar servicios del sistema"""
    global sheets_service, context_engine, ai_agent
    
    logger.info("🚀 Iniciando Red Soluciones ISP v5.0...")
    
    try:
        # Inicializar Google Sheets
        logger.info("📊 Configurando Google Sheets...")
        sheets_service = SheetsServiceV2()
        
        # Inicializar Context Engine
        logger.info("🧠 Inicializando Context Engine...")
        context_engine = ContextEngine(sheets_service)
        await context_engine.initialize_system()
        
        # Inicializar AI Agent
        logger.info("🤖 Configurando AI Agent...")
        ai_agent = HomologatedAIAgent(context_engine, sheets_service)
        
        logger.info("✅ Sistema inicializado correctamente")
        
    except Exception as e:
        logger.error(f"❌ Error en inicialización: {e}")
        raise

# === MANEJADORES DE ERRORES ===
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error no manejado: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": f"Error interno: {str(exc)}"}
    )

# === ARCHIVOS ESTÁTICOS ===
# Frontend
frontend_dir = Path(__file__).parent.parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/frontend", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")

# Assets
assets_dir = frontend_dir / "assets"
if assets_dir.exists():
    app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

# === RUTAS PRINCIPALES ===
@app.get("/")
async def root():
    """Redirección al dashboard"""
    return RedirectResponse(url="/frontend/index.html")

@app.get("/health")
async def health_check():
    """Verificación de salud del sistema"""
    return {
        "status": "healthy",
        "version": VERSION,
        "timestamp": datetime.now().isoformat(),
        "services": {
            "sheets": sheets_service is not None,
            "context_engine": context_engine is not None,
            "ai_agent": ai_agent is not None
        }
    }

# === API DE DATOS ===
@app.get("/api/clients")
async def get_clients():
    """Obtener todos los clientes"""
    if not sheets_service:
        raise HTTPException(status_code=500, detail="Servicio de sheets no disponible")
    
    try:
        clients = sheets_service.get_all_rows()
        logger.info(f"📊 Obtenidos {len(clients)} clientes")
        return {"clients": clients, "total": len(clients)}
    except Exception as e:
        logger.error(f"Error obteniendo clientes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/clients/{user}")
async def get_clients_by_user(user: str):
    """Obtener clientes filtrados por usuario"""
    if not context_engine:
        raise HTTPException(status_code=500, detail="Context engine no disponible")
    
    try:
        user_context = await context_engine.get_full_context(user)
        clients = user_context.get("clientes", [])
        logger.info(f"📊 Obtenidos {len(clients)} clientes para {user}")
        return {"clients": clients, "total": len(clients), "user": user}
    except Exception as e:
        logger.error(f"Error obteniendo clientes para {user}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dashboard/{user}")
async def get_dashboard_data(user: str):
    """Obtener datos del dashboard para un usuario"""
    if not context_engine:
        raise HTTPException(status_code=500, detail="Context engine no disponible")
    
    try:
        user_context = await context_engine.get_full_context(user)
        business_context = await context_engine._calculate_business_context()
        
        return {
            "user": user,
            "user_context": user_context,
            "business_metrics": business_context.__dict__,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error obteniendo dashboard para {user}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# === API DE IA ===
@app.post("/api/chat")
async def chat_with_ai(chat_message: ChatMessage):
    """Chat con el agente de IA"""
    if not ai_agent:
        raise HTTPException(status_code=500, detail="Agente de IA no disponible")
    
    try:
        response = await ai_agent.process_query(
            query=chat_message.message,
            propietario=chat_message.user or "Eduardo"
        )
        
        return {
            "response": response,
            "user": chat_message.user,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error en chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# === API DE AUTENTICACIÓN ===
@app.post("/api/auth/login")
async def login(auth_request: AuthRequest):
    """Autenticación de usuario"""
    valid_users = {
        "eduardo": "admin123",
        "omar": "admin123"
    }
    
    username = auth_request.username.lower()
    if username in valid_users and valid_users[username] == auth_request.password:
        return {
            "success": True,
            "user": username.title(),
            "message": f"Bienvenido {username.title()}"
        }
    else:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

# === INFORMACIÓN DEL SISTEMA ===
@app.get("/api/system/info")
async def get_system_info():
    """Información del sistema"""
    return {
        "name": PROJECT_NAME,
        "version": VERSION,
        "status": "operational",
        "features": [
            "Google Sheets Integration",
            "AI Agent",
            "Context Engine",
            "User Authentication",
            "Real-time Dashboard"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)

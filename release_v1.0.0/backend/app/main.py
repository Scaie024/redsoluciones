"""
Red Soluciones ISP - Sistema Unificado v1.0
Sistema completo de gestión ISP con IA integrada
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel
from pathlib import Path
from typing import Optional, Dict, List, Any
import logging
from datetime import datetime

# Importaciones locales
from .services.sheets.service import SheetsServiceV2 as SheetsService
from .services.smart_agent import SmartISPAgent
from .utils.logger import get_logger
from .core.config import settings

# Configurar logging
logger = get_logger(__name__)

# === INICIALIZACIÓN ===
sheets_service = None
smart_agent = None

try:
    sheets_service = SheetsService()
    smart_agent = SmartISPAgent(sheets_service)
    logger.info("🚀 Red Soluciones ISP v1.0.0 - Servicios inicializados")
except Exception as e:
    logger.error(f"❌ Error inicializando servicios: {e}")

# === CONFIGURACIÓN FASTAPI ===
app = FastAPI(
    title="Red Soluciones ISP",
    description="Sistema completo de gestión ISP con IA integrada v1.0",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === MODELOS PYDANTIC ===
class ClientData(BaseModel):
    nombre: str
    email: Optional[str] = ""
    zona: Optional[str] = ""
    telefono: Optional[str] = ""
    pago_mensual: Optional[float] = 0

class ProspectData(BaseModel):
    nombre: str
    telefono: Optional[str] = ""
    zona: Optional[str] = ""
    email: Optional[str] = ""
    notas: Optional[str] = ""

class IncidentData(BaseModel):
    cliente: str
    descripcion: str
    tipo: Optional[str] = "Técnico"
    prioridad: Optional[str] = "Media"

class ChatMessage(BaseModel):
    message: str

# === EXCEPTION HANDLERS ===
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# === RUTAS PRINCIPALES ===

@app.get("/")
async def root():
    return RedirectResponse(url="/dashboard.html")

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "google_sheets": sheets_service is not None,
            "smart_agent": smart_agent is not None
        }
    }


# === API ENDPOINTS ===

@app.get("/api/clients")
async def get_clients():
    """Obtener todos los clientes"""
    try:
        if not sheets_service:
            raise HTTPException(status_code=503, detail="Servicio no disponible")
            
        clients = sheets_service.get_all_clients()
        return {"clients": clients, "count": len(clients)}
        
    except Exception as e:
        logger.error(f"Error obteniendo clientes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/clients")
async def add_client(client_data: ClientData):
    """Agregar nuevo cliente"""
    try:
        if not sheets_service:
            raise HTTPException(status_code=503, detail="Servicio no disponible")
        
        # Convertir a formato esperado por el servicio
        client_dict = {
            "Nombre": client_data.nombre,
            "Email": client_data.email or "",
            "Zona": client_data.zona or "",
            "Teléfono": str(client_data.telefono) if client_data.telefono else "",
            "Pago": str(client_data.pago_mensual) if client_data.pago_mensual else "0",
            "Activo (SI/NO)": "SI",
            "Fecha Registro": datetime.now().strftime("%Y-%m-%d")
        }
        
        result = sheets_service.add_client(client_dict)
        
        if result:
            return {
                "success": True,
                "message": f"Cliente {client_data.nombre} agregado exitosamente"
            }
        else:
            raise HTTPException(status_code=400, detail="Error agregando cliente")
            
    except Exception as e:
        logger.error(f"Error agregando cliente: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/prospects")
async def add_prospect(prospect_data: ProspectData):
    """Agregar nuevo prospecto"""
    try:
        if not sheets_service:
            raise HTTPException(status_code=503, detail="Servicio no disponible")
        
        # Usar add_client con datos de prospecto
        prospect_dict = {
            "Nombre": f"[PROSPECTO] {prospect_data.nombre}",
            "Email": prospect_data.email or "",
            "Zona": prospect_data.zona or "",
            "Teléfono": str(prospect_data.telefono) if prospect_data.telefono else "",
            "Pago": "0",  # Prospectos no pagan aún
            "Notas": prospect_data.notas or "",
            "Activo (SI/NO)": "PROSPECTO",
            "Fecha Registro": datetime.now().strftime("%Y-%m-%d")
        }
        
        result = sheets_service.add_client(prospect_dict)
        
        if result:
            return {
                "success": True,
                "message": f"Prospecto {prospect_data.nombre} agregado exitosamente"
            }
        else:
            raise HTTPException(status_code=400, detail="Error agregando prospecto")
            
    except Exception as e:
        logger.error(f"Error agregando prospecto: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/incidents")
async def add_incident(incident_data: IncidentData):
    """Agregar nuevo incidente"""
    try:
        if not sheets_service:
            raise HTTPException(status_code=503, detail="Servicio no disponible")
        
        # Usar add_client para simular incidentes como "clientes especiales"
        incident_dict = {
            "Nombre": f"[INCIDENTE] {incident_data.cliente}",
            "Email": f"incidente@{datetime.now().strftime('%Y%m%d%H%M%S')}.com",
            "Zona": "SOPORTE",
            "Teléfono": "INCIDENTE",
            "Pago": "0",
            "Notas": f"{incident_data.tipo}: {incident_data.descripcion} (Prioridad: {incident_data.prioridad})",
            "Activo (SI/NO)": "INCIDENTE",
            "Fecha Registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        result = sheets_service.add_client(incident_dict)
        
        if result:
            return {
                "success": True,
                "message": f"Incidente registrado para {incident_data.cliente}"
            }
        else:
            raise HTTPException(status_code=400, detail="Error registrando incidente")
            
    except Exception as e:
        logger.error(f"Error registrando incidente: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat(message: ChatMessage):
    """Chat con agente inteligente"""
    try:
        if not smart_agent:
            raise HTTPException(status_code=503, detail="Agente no disponible")
            
        response = smart_agent.process_query(message.message)
        return response
        
    except Exception as e:
        logger.error(f"Error en chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# === ARCHIVOS ESTÁTICOS ===
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# === STARTUP EVENT ===
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Red Soluciones ISP v1.0.0 iniciado exitosamente")

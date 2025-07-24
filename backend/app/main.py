"""
Red Soluciones ISP - Sistema Unificado y Funcional
Sistema completo de gestión ISP con IA integrada
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse, HTMLResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel
from pathlib import Path
from typing import Optional, Dict, List, Any
import logging
import traceback
from datetime import datetime

from backend.app.services.sheets.service import SheetsServiceV2 as SheetsService
from backend.app.services.smart_agent import SmartISPAgent, initialize_smart_agent, get_smart_agent
from backend.app.utils.logger import get_logger
from backend.app.core.config import settings

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Sistema completo de gestión ISP con IA integrada - Unificado",
    version=settings.VERSION,
    debug=settings.DEBUG
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": f"Internal server error: {str(exc)}",
            "type": "server_error"
        }
    )

# Mount frontend static files
frontend_dir = settings.FRONTEND_DIR
app.mount(
    "/frontend",
    StaticFiles(directory=str(frontend_dir), html=True),
    name="frontend"
)

# Mount assets directly
assets_dir = settings.FRONTEND_DIR / "assets"
if assets_dir.exists():
    app.mount(
        "/assets",
        StaticFiles(directory=str(assets_dir)),
        name="assets"
    )

# === CONFIGURACIÓN DE SERVICIOS UNIFICADA ===
# Inicializar variables globales
sheets_service = None
smart_agent = None
logger = get_logger(__name__)

try:
    # Instantiate services con configuración centralizada
    sheets_service = SheetsService()
    initialize_smart_agent(sheets_service)
    smart_agent = get_smart_agent()
    
    logger.info(f"🚀 {settings.PROJECT_NAME} v{settings.VERSION} - Servicios inicializados con Smart Agent")
except Exception as e:
    # Fallback a modo mock si hay problemas de configuración
    logger.warning(f"⚠️ Iniciando en modo mock debido a: {e}")
    # Inicializar agente en modo fallback
    initialize_smart_agent(None)  # Sin servicio de sheets
    smart_agent = get_smart_agent()
    logger.info("🤖 Smart Agent inicializado en modo fallback")

# Data models
class ChatMessage(BaseModel):
    message: str

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
    prioridad: Optional[str] = "Media"
    origen: Optional[str] = "Sistema"

class IncidentData(BaseModel):
    cliente: str
    descripcion: str
    tipo: str  # "Técnico", "Facturación", "Soporte", "Comercial"
    prioridad: str  # "Alta", "Media", "Baja"
    zona: Optional[str] = ""
    telefono: Optional[str] = ""

# === RUTAS PRINCIPALES ===

# Root redirect
@app.get("/")
async def root():
    return RedirectResponse(url="/dashboard.html")

# Health check endpoint
@app.get("/health")
async def system_health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "timestamp": datetime.now().isoformat(),
        "services": {
            "google_sheets": sheets_service is not None,
            "smart_agent": smart_agent is not None
        }
    }

# Sheets connection test
@app.get("/api/sheets/test")
async def test_sheets_connection():
    """Probar conexión directa con Google Sheets"""
    try:
        if sheets_service:
            # Verificar estado de la conexión del cliente
            if not sheets_service.gc:
                return {
                    "success": False,
                    "message": "❌ Cliente de Google no inicializado",
                    "solution": "Verificar credenciales de service_account.json"
                }
            
            # Intentar abrir la hoja específicamente
            try:
                spreadsheet = sheets_service.gc.open_by_key(sheets_service.sheet_id)
                worksheet = spreadsheet.sheet1  # Primera hoja
                
                # Intentar leer datos de prueba
                test_data = worksheet.get('A1')
                headers = worksheet.row_values(1) if worksheet.row_count > 0 else []
                
                return {
                    "success": True,
                    "message": "✅ Conexión exitosa con Google Sheets",
                    "spreadsheet_title": spreadsheet.title,
                    "worksheet_title": worksheet.title,
                    "test_data": test_data,
                    "headers": headers,
                    "sheet_id": sheets_service.sheet_id,
                    "rows": worksheet.row_count,
                    "cols": worksheet.col_count
                }
                
            except Exception as sheet_error:
                error_msg = str(sheet_error)
                
                if "PERMISSION_DENIED" in error_msg or "does not have access" in error_msg:
                    return {
                        "success": False,
                        "message": "❌ Sin permisos para acceder a la Google Sheet",
                        "error": error_msg,
                        "solution": f"Comparte la hoja con: {sheets_service.gc.auth.service_account_email if hasattr(sheets_service.gc.auth, 'service_account_email') else 'red-soluciones-fo@dev-spirit-466223-v9.iam.gserviceaccount.com'}",
                        "sheet_url": f"https://docs.google.com/spreadsheets/d/{sheets_service.sheet_id}/edit",
                        "sheet_id": sheets_service.sheet_id
                    }
                elif "INVALID_ARGUMENT" in error_msg or "Unable to parse range" in error_msg:
                    return {
                        "success": False,
                        "message": "❌ ID de Google Sheet inválido",
                        "error": error_msg,
                        "solution": "Verificar que el ID de la hoja sea correcto",
                        "current_id": sheets_service.sheet_id
                    }
                else:
                    return {
                        "success": False,
                        "message": f"❌ Error accediendo a Google Sheets: {error_msg}",
                        "error_type": type(sheet_error).__name__,
                        "sheet_id": sheets_service.sheet_id
                    }
        else:
            return {
                "success": False,
                "message": "❌ Servicio de Google Sheets no disponible"
            }
    except Exception as e:
        logger.error(f"Error testing sheets connection: {e}")
        return {
            "success": False,
            "message": f"❌ Error general: {str(e)}",
            "error_type": type(e).__name__
        }

@app.get("/api/sheets/status")
async def get_sheets_status():
    """Verificar estado de conexión con Google Sheets"""
    try:
        if sheets_service:
            status = sheets_service.test_connection()
            return {
                "success": True,
                "sheets_connected": status.get("status") == "connected",
                "details": status
            }
        else:
            return {
                "success": False,
                "sheets_connected": False,
                "message": "Servicio de Google Sheets no inicializado"
            }
    except Exception as e:
        logger.error(f"Error checking sheets status: {e}")
        return {
            "success": False,
            "sheets_connected": False,
            "error": str(e)
        }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    sheets_status = None
    if sheets_service:
        try:
            sheets_status = sheets_service.test_connection()
        except:
            sheets_status = {"status": "error"}
    
    return {
        "status": "ok",
        "message": "Red Soluciones ISP API funcionando correctamente",
        "version": "2.0.0",
        "port": 8004,
        "services": {
            "google_sheets": sheets_service is not None,
            "google_sheets_connected": sheets_status.get("status") == "connected" if sheets_status else False,
            "smart_agent": smart_agent is not None
        }
    }

# Serve main HTML file
@app.get("/index.html")
async def serve_index():
    """Servir la página principal"""
    try:
        with open(Path(__file__).parents[2] / "frontend" / "index.html", encoding='utf-8') as f:
            content = f.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

@app.get("/dashboard.html")
async def serve_dashboard():
    """Servir el dashboard funcional"""
    try:
        with open(Path(__file__).parents[2] / "frontend" / "dashboard.html", encoding='utf-8') as f:
            content = f.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Dashboard no encontrado")

# === CHAT INTELIGENTE ===

@app.post("/api/chat")
async def chat(msg: ChatMessage):
    """Process chat message with intelligent AI agent"""
    try:
        if smart_agent:
            # Usar el nuevo agente inteligente
            response = smart_agent.process_query(msg.message)
            return {
                "response": response["response"],
                "suggestions": response.get("suggestions", []),
                "confidence": 0.9,  # El nuevo agente es más confiable
                "type": response.get("type", "general"),
                "data": response.get("data", {})
            }
        else:
            return {
                "response": "❌ Agente no disponible temporalmente.",
                "suggestions": ["Reiniciar sistema", "Contactar soporte"],
                "confidence": 0.0
            }
    except Exception as e:
        logger.error(f"Error in intelligent chat: {e}")
        return {
            "response": "❌ Error procesando mensaje. El agente está trabajando para resolverlo.",
            "suggestions": ["Intentar de nuevo", "Ver estadísticas", "Mostrar ayuda"],
            "confidence": 0.0
        }

@app.get("/api/chat/suggestions")
async def get_chat_suggestions(q: str = ""):
    """Get smart suggestions for chat input"""
    try:
        suggestions = [
            "Ver estadísticas del negocio",
            "Buscar cliente por nombre", 
            "Análisis financiero completo",
            "Información de zonas",
            "Mostrar ayuda y comandos"
        ]
        
        if q:
            # Filtrar sugerencias basadas en la query
            suggestions = [s for s in suggestions if q.lower() in s.lower()]
        
        return {"suggestions": suggestions}
    except Exception as e:
        logger.error(f"Error getting suggestions: {e}")
        return {"suggestions": []}

# === DATOS DE NEGOCIO Y GESTIÓN DE CLIENTES ===

@app.get("/api/clients")
async def get_all_clients():
    """Obtener todos los clientes"""
    try:
        if sheets_service:
            clients = sheets_service.get_all_clients(include_inactive=True)
            logger.info(f"📊 Obtenidos {len(clients)} clientes desde Google Sheets")
            return {
                "success": True,
                "data": clients,
                "count": len(clients)
            }
        else:
            return {
                "success": False,
                "message": "Servicio de Google Sheets no disponible",
                "data": []
            }
    except Exception as e:
        logger.error(f"Error getting clients: {e}")
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "data": []
        }

@app.post("/api/clients")
async def add_client(client_data: ClientData):
    """Agregar nuevo cliente"""
    try:
        if sheets_service:
            # Convertir a diccionario
            client_dict = {
                "Nombre": client_data.nombre,
                "Email": client_data.email,
                "Zona": client_data.zona,
                "Teléfono": client_data.telefono,
                "Pago": client_data.pago_mensual,
                "Notas": "",
                "Activo (SI/NO)": "SI",
                "Fecha Registro": datetime.now().strftime("%Y-%m-%d")
            }
            
            result = sheets_service.add_client(client_dict)
            if result:
                logger.info(f"✅ Cliente agregado: {client_data.nombre}")
                return {
                    "success": True,
                    "message": f"Cliente {client_data.nombre} agregado exitosamente",
                    "data": client_dict
                }
            else:
                return {
                    "success": False,
                    "message": "Error al agregar cliente"
                }
        else:
            return {
                "success": False,
                "message": "Servicio de Google Sheets no disponible"
            }
    except Exception as e:
        logger.error(f"Error adding client: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/clients/search/{query}")
async def search_clients(query: str):
    """Buscar clientes por nombre, email, zona, etc."""
    try:
        if sheets_service:
            results = sheets_service.find_client_by_name(query)
            return {
                "success": True,
                "data": results,
                "count": len(results),
                "query": query
            }
        else:
            return {
                "success": False,
                "message": "Servicio de Google Sheets no disponible",
                "data": []
            }
    except Exception as e:
        logger.error(f"Error searching clients: {e}")
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "data": []
        }

# === ENDPOINTS DE PROSPECTOS ===

@app.post("/api/prospects")
async def add_prospect(prospect_data: ProspectData):
    """Agregar nuevo prospecto"""
    try:
        if sheets_service:
            # Convertir a diccionario
            prospect_dict = {
                "Nombre": prospect_data.nombre,
                "Teléfono": prospect_data.telefono,
                "Zona": prospect_data.zona,
                "Email": prospect_data.email,
                "Notas": prospect_data.notas,
                "Prioridad": prospect_data.prioridad,
                "Origen": prospect_data.origen
            }
            
            result = sheets_service.add_prospect(prospect_dict)
            if result:
                logger.info(f"✅ Prospecto agregado: {prospect_data.nombre}")
                return {
                    "success": True,
                    "message": f"Prospecto {prospect_data.nombre} agregado exitosamente",
                    "data": prospect_dict
                }
            else:
                return {
                    "success": False,
                    "message": "Error al agregar prospecto"
                }
        else:
            return {
                "success": False,
                "message": "Servicio de Google Sheets no disponible"
            }
    except Exception as e:
        logger.error(f"Error adding prospect: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/prospects")
async def get_prospects():
    """Obtener lista de prospectos"""
    try:
        if sheets_service:
            prospects = sheets_service.get_prospects()
            return {
                "success": True,
                "data": prospects,
                "count": len(prospects)
            }
        else:
            return {
                "success": False,
                "message": "Servicio de Google Sheets no disponible",
                "data": []
            }
    except Exception as e:
        logger.error(f"Error getting prospects: {e}")
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "data": []
        }

# === ENDPOINTS DE INCIDENTES ===

@app.post("/api/incidents")
async def add_incident(incident_data: IncidentData):
    """Agregar nuevo incidente"""
    try:
        if sheets_service:
            # Crear diccionario para el incidente
            incident_dict = {
                "Cliente": incident_data.cliente,
                "Tipo": incident_data.tipo,
                "Descripción": incident_data.descripcion,
                "Prioridad": incident_data.prioridad,
                "Estado": "Nuevo",
                "Fecha Creación": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "Técnico Asignado": "Sin asignar"
            }
            
            # Usar método genérico para crear hoja de incidentes
            result = sheets_service.add_incident(incident_dict)
            if result:
                logger.info(f"✅ Incidente agregado para cliente: {incident_data.cliente}")
                return {
                    "success": True,
                    "message": f"Incidente registrado para {incident_data.cliente}",
                    "data": incident_dict
                }
            else:
                return {
                    "success": False,
                    "message": "Error al registrar incidente"
                }
        else:
            return {
                "success": False,
                "message": "Servicio de Google Sheets no disponible"
            }
    except Exception as e:
        logger.error(f"Error adding incident: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/incidents")
async def get_incidents():
    """Obtener lista de incidentes"""
    try:
        if sheets_service:
            incidents = sheets_service.get_incidents()
            return {
                "success": True,
                "data": incidents,
                "count": len(incidents)
            }
        else:
            return {
                "success": False,
                "message": "Servicio de Google Sheets no disponible",
                "data": []
            }
    except Exception as e:
        logger.error(f"Error getting incidents: {e}")
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "data": []
        }

@app.get("/api/dashboard/kpis")
async def get_dashboard_kpis():
    """Get main KPIs for dashboard"""
    try:
        if sheets_service:
            # Obtener datos reales desde Google Sheets
            clients = sheets_service.get_all_clients(include_inactive=True)
            active_clients = [c for c in clients if str(c.get('Activo (SI/NO)', '')).strip().lower() in ['si', 'sí', 'yes', '1', 'true', 'activo']]
            
            # Calcular ingresos
            total_revenue = 0
            premium_count = 0
            zones = set()
            
            for client in active_clients:
                pago_str = str(client.get('Pago', '0')).replace('$', '').replace(',', '').strip()
                try:
                    pago = float(pago_str) if pago_str else 0
                    total_revenue += pago
                    if pago >= 400:  # Umbral premium
                        premium_count += 1
                except:
                    pass
                
                zona = client.get('Zona', '').strip()
                if zona:
                    zones.add(zona)
            
            premium_percentage = (premium_count / max(len(active_clients), 1)) * 100
            
            return {
                "total_clients": len(active_clients),
                "monthly_revenue": total_revenue,
                "active_zones": len(zones),
                "premium_percentage": premium_percentage,
                "total_registered": len(clients)
            }
        
        # Si no hay servicio de sheets, usar agente
        if smart_agent:
            stats_response = smart_agent.process_query("estadísticas")
            if stats_response.get("data"):
                data = stats_response["data"]
                return {
                    "total_clients": data.get("total_clients", 0),
                    "monthly_revenue": data.get("monthly_revenue", 0),
                    "active_zones": data.get("active_zones", 0),
                    "premium_percentage": data.get("premium_percentage", 0)
                }
        
        # Fallback con datos básicos
        return {
            "total_clients": 0,
            "monthly_revenue": 0,
            "active_zones": 0,
            "premium_percentage": 0
        }
        
    except Exception as e:
        logger.error(f"Error getting dashboard KPIs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics")
async def get_analytics():
    """Get advanced analytics data"""
    try:
        if smart_agent:
            # Usar el agente para análisis
            analysis_response = smart_agent.process_query("análisis financiero")
            
            if analysis_response.get("data"):
                return analysis_response["data"]
        
        # Fallback básico
        return {
            "revenue": {"total": 1650, "monthly_avg": 412.5},
            "packages": {"premium": 2, "standard": 2},
            "zones": {"Norte": {"clients": 2, "revenue": 800}},
            "total_clients": 4
        }
        
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# === TELEGRAM BOT WEBHOOK ===

@app.post("/api/telegram/webhook")
async def telegram_webhook(request: Request):
    """Webhook para el bot de Telegram"""
    try:
        # Importar el handler del webhook
        import sys
        from pathlib import Path
        api_dir = Path(__file__).parents[2] / "api"
        sys.path.insert(0, str(api_dir))
        
        from telegram_webhook import handle_telegram_webhook
        
        # Obtener los datos del update
        update_data = await request.json()
        logger.info(f"📱 Telegram webhook recibido: {update_data}")
        
        # Procesar el update
        response = handle_telegram_webhook(update_data)
        
        if response.get("method") == "sendMessage":
            # Enviar respuesta directamente a Telegram
            import requests
            
            telegram_api_url = f"https://api.telegram.org/bot7881396575:AAHDbmSqXIVPSAK3asK9ieNhpbaS7iD3NZk/sendMessage"
            
            requests.post(telegram_api_url, json={
                "chat_id": response["chat_id"],
                "text": response["text"],
                "parse_mode": response.get("parse_mode", "Markdown")
            })
            
            return {"status": "message_sent"}
        
        return response
        
    except Exception as e:
        logger.error(f"Error en webhook de Telegram: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/api/telegram/setup")
async def setup_telegram_webhook():
    """Configurar webhook de Telegram"""
    try:
        import requests
        
        # URL del webhook (será la URL de Vercel + /api/telegram/webhook)
        webhook_url = "https://tu-proyecto.vercel.app/api/telegram/webhook"
        
        # Configurar webhook en Telegram
        telegram_api_url = f"https://api.telegram.org/bot7881396575:AAHDbmSqXIVPSAK3asK9ieNhpbaS7iD3NZk/setWebhook"
        
        response = requests.post(telegram_api_url, json={
            "url": webhook_url
        })
        
        if response.status_code == 200:
            result = response.json()
            return {
                "success": True,
                "message": "Webhook configurado exitosamente",
                "webhook_url": webhook_url,
                "telegram_response": result
            }
        else:
            return {
                "success": False,
                "message": "Error configurando webhook",
                "status_code": response.status_code,
                "response": response.text
            }
            
    except Exception as e:
        logger.error(f"Error configurando webhook: {e}")
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)

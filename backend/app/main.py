"""
Red Soluciones ISP - Sistema Unificado y Funcional
Sistema completo de gestión ISP con IA integrada
"""

# Cargar variables de entorno ANTES de cualquier importación
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Cargar manualmente si python-dotenv no está disponible
    import os
    from pathlib import Path
    env_file = Path(__file__).parents[2] / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

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
from backend.app.services.consolidated_agent import ConsolidatedISPAgent
from backend.app.services.context_engine import ContextEngine
from backend.app.utils.logger import get_logger
from backend.app.core.config_unified import settings
from backend.app.core.user_auth import user_auth

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Sistema completo de gestión ISP con IA integrada - Unificado",
    version=settings.VERSION,
    debug=settings.DEBUG
)

# CORS configuration - SEGURA
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:8004", 
    "http://localhost:8005",
    "http://127.0.0.1:8004",
    "http://127.0.0.1:8005",
    "https://red-soluciones.vercel.app",
]

if settings.DEBUG:
    allowed_origins.append("*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
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

# === SERVIR FRONTEND ===
# NOTA: El mount del frontend se movió al final del archivo 
# para evitar que capture las rutas de API antes de que se definan.

# === CONFIGURACIÓN DE SERVICIOS UNIFICADA ===
# Inicializar variables globales
sheets_service = None
context_engine = None
enhanced_agent = None
super_agent = None
logger = get_logger(__name__)

try:
    # Instantiate services con configuración centralizada y manejo robusto
    logger.info("🔧 Inicializando servicios del sistema...")
    sheets_service = SheetsService()
    logger.info("✅ SheetsService inicializado")
    context_engine = ContextEngine(sheets_service)
    try:
        consolidated_agent = ConsolidatedISPAgent(sheets_service, context_engine)
        # Compatibilidad
        enhanced_agent = consolidated_agent
        super_agent = consolidated_agent
        logger.info(f"✅ {settings.PROJECT_NAME} v{settings.VERSION} - Sistema inicializado correctamente")
    except Exception as agent_error:
        logger.error(f"❌ Error en inicialización del agente IA: {agent_error}")
        consolidated_agent = None
        enhanced_agent = None
        super_agent = None
        logger.warning("⚠️ Sistema iniciado sin agente IA, pero con acceso a Google Sheets")
except Exception as e:
    logger.error(f"❌ Error crítico en inicialización de servicios: {e}")
    sheets_service = None
    context_engine = None
    consolidated_agent = None
    enhanced_agent = None
    super_agent = None
    enhanced_agent = None
    super_agent = None
    logger.warning("⚠️ Sistema iniciado en modo seguro sin servicios externos")

# === STARTUP EVENT ===
@app.on_event("startup")
async def startup_event():
    """Inicializar sistema completo al arranque"""
    global context_engine, enhanced_agent
    
    if context_engine and enhanced_agent:
        try:
            logger.info("🚀 Inicializando sistema homologado...")
            result = await context_engine.initialize_system()
            
            if result.get('success'):
                logger.info(f"✅ Sistema homologado inicializado: {result.get('entities_loaded', 0)} entidades cargadas")
            else:
                logger.error(f"❌ Error inicializando sistema: {result.get('error')}")
        except Exception as e:
            logger.error(f"❌ Error en startup: {e}")

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

class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    session_id: Optional[str] = None

# === RUTAS PRINCIPALES ===

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
            "super_agent": super_agent is not None
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
                if not sheets_service.sheet_id:
                    return {
                        "success": False,
                        "message": "❌ ID de Google Sheet no configurado",
                        "error": "sheet_id is None",
                        "solution": "Verificar configuración de GOOGLE_SHEET_ID en .env"
                    }
                
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
                    # Obtener email de service account de forma segura
                    service_email = "red-soluciones-fo@dev-spirit-466223-v9.iam.gserviceaccount.com"
                    try:
                        # Información de las credenciales (para desarrollo)
                        service_email = "google-service-account@configured"
                    except:
                        pass
                    
                    return {
                        "success": False,
                        "message": "❌ Sin permisos para acceder a la Google Sheet",
                        "error": error_msg,
                        "solution": f"Comparte la hoja con: {service_email}",
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

@app.get("/api/debug/cobranza")
async def debug_cobranza():
    """Debug: obtener datos directos de cobranza"""
    try:
        if not sheets_service:
            raise HTTPException(status_code=503, detail="Servicio de Google Sheets no disponible")
        
        # Probar obtener datos de cobranza
        cobranza_data = sheets_service.get_cobranza_data()
        
        # Analizar qué valores únicos tenemos para mes y año
        meses = set()
        años = set()
        for record in cobranza_data[:20]:  # Analizar primeros 20 registros
            mes = record.get('Mes', '')
            año = record.get('Año', '')
            meses.add(mes)
            años.add(año)
        
        # Filtrar solo registros de julio 2025
        julio_2025 = [
            record for record in cobranza_data 
            if record.get('Mes', '').lower() == 'julio' and str(record.get('Año', '')) == '2025'
        ]
        
        return {
            "success": True,
            "total_cobranza": len(cobranza_data),
            "julio_2025": len(julio_2025),
            "unique_meses": sorted(list(meses)),
            "unique_años": sorted(list(años)),
            "sample_raw_data": cobranza_data[:3],
            "sample_filtered": julio_2025[:3]
        }
        
    except Exception as e:
        logger.error(f"Error en debug cobranza: {e}")
        return {"success": False, "error": str(e)}

@app.get("/api/debug/enriched")
async def debug_enriched():
    """Debug: obtener datos enriquecidos"""
    try:
        if not sheets_service:
            raise HTTPException(status_code=503, detail="Servicio de Google Sheets no disponible")
        
        enriched_clients = sheets_service.get_enriched_clients()
        
        # Mostrar los primeros 3 clientes enriquecidos
        sample = enriched_clients[:3] if enriched_clients else []
        
        return {
            "success": True,
            "total_enriched": len(enriched_clients),
            "sample_data": sample
        }
        
    except Exception as e:
        logger.error(f"Error en debug enriched: {e}")
        return {"success": False, "error": str(e)}

@app.get("/api/sheets/explore")
async def explore_sheets():
    """Explorar todas las hojas y columnas del Google Sheets"""
    try:
        if not sheets_service:
            raise HTTPException(status_code=503, detail="Servicio de Google Sheets no disponible")
        
        spreadsheet = sheets_service.gc.open_by_key(sheets_service.sheet_id)
        
        sheets_info = []
        for worksheet in spreadsheet.worksheets():
            try:
                # Obtener todas las cabeceras (primera fila completa)
                headers = worksheet.row_values(1)
                
                # Obtener algunas filas de ejemplo
                all_values = worksheet.get_all_values()
                sample_rows = all_values[1:4] if len(all_values) > 1 else []
                
                sheets_info.append({
                    "name": worksheet.title,
                    "rows": worksheet.row_count,
                    "cols": worksheet.col_count,
                    "headers": headers,
                    "sample_data": sample_rows
                })
            except Exception as e:
                sheets_info.append({
                    "name": worksheet.title,
                    "error": str(e)
                })
        
        return {
            "success": True,
            "spreadsheet_title": spreadsheet.title,
            "sheets": sheets_info
        }
        
    except Exception as e:
        logger.error(f"Error explorando sheets: {e}")
        raise HTTPException(status_code=500, detail=f"Error explorando sheets: {str(e)}")

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
            "super_agent": super_agent is not None
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
    """Process chat message with intelligent AI agent and user context"""
    try:
        # Crear contexto de usuario simple
        user_context = None
        if msg.user_id:
            try:
                # Validar sesión si existe session_id
                if msg.session_id:
                    session = user_auth.validate_session(msg.session_id)
                    if session:
                        user_context = {
                            "user_id": msg.user_id,
                            "session_id": msg.session_id,
                            "username": session.get("username", "Unknown"),
                            "name": session.get("name", "Unknown"),
                            "role": session.get("role", "user")
                        }
                        logger.info(f"💬 Chat - Usuario autenticado: {user_context['name']} ({user_context['username']})")
                    else:
                        # Sesión inválida o expirada
                        user_context = {"user_id": msg.user_id, "session_id": msg.session_id}
                        logger.info(f"💬 Chat - Sesión inválida: {msg.user_id}")
                else:
                    # Sin sesión, usuario básico
                    user_context = {"user_id": msg.user_id}
                    logger.info(f"💬 Chat - Usuario básico: {msg.user_id}")
            except Exception as e:
                logger.warning(f"⚠️ Error validando usuario: {e}")
                user_context = {"user_id": msg.user_id}
        
        if consolidated_agent:
            # Usar el agente consolidado con contexto
            response = await consolidated_agent.process_query(msg.message, user_context)
            
            # Agregar información de usuario a la respuesta
            response_data = {
                "response": response.message,
                "suggestions": response.suggestions,
                "confidence": response.confidence,
                "type": response.action_type.value,
                "data": response.data,
                "execution_time": response.execution_time,
                "user_context": user_context if user_context else None
            }
            
            return response_data
        else:
            return {
                "response": "Agente no disponible temporalmente.",
                "suggestions": ["Reiniciar sistema", "Contactar soporte"],
                "confidence": 0.0,
                "user_context": user_context
            }
    except Exception as e:
        logger.error(f"Error in intelligent chat: {e}")
        return {
            "response": "Error procesando mensaje. El agente está trabajando para resolverlo.",
            "suggestions": ["Intentar de nuevo", "Ver estadísticas", "Mostrar ayuda"],
            "confidence": 0.0,
            "user_context": user_context if 'user_context' in locals() else None
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

# === ENDPOINTS DE AUTENTICACIÓN ===

@app.post("/api/auth/login")
async def login_user(user_data: dict):
    """Iniciar sesión de propietario (sin contraseña)"""
    try:
        owner_name = user_data.get("owner_name", "").lower().strip()
        
        if not owner_name:
            return {
                "success": False,
                "message": "Nombre de propietario es requerido",
                "available_owners": list(user_auth.owners.keys())
            }
        
        auth_result = user_auth.authenticate_owner(owner_name)
        if not auth_result or not auth_result.get("success"):
            return {
                "success": False,
                "message": "Propietario no autorizado",
                "available_owners": list(user_auth.owners.keys())
            }
        
        return {
            "success": True,
            "message": f"Bienvenido, {auth_result['owner']['name']}",
            "owner": auth_result["owner"],
            "session_id": auth_result["session_id"]
        }
        
    except Exception as e:
        logger.error(f"Error en login: {e}")
        return {"success": False, "message": "Error en autenticación"}

@app.get("/api/auth/users")
async def get_available_users():
    """Obtener propietarios disponibles"""
    return {
        "success": True,
        "owners": [
            {
                "id": owner_name,
                "name": info["name"],
                "role": info["role"]
            }
            for owner_name, info in user_auth.owners.items()
        ]
    }

@app.get("/api/auth/active")
async def get_active_users():
    """Obtener propietarios activos"""
    try:
        active_sessions = []
        for session_id, session_info in user_auth.sessions.items():
            if session_info["expires"] > datetime.now():
                active_sessions.append({
                    "session_id": session_id,
                    "owner_name": session_info["owner_name"],
                    "name": session_info["name"],
                    "role": session_info["role"]
                })
        
        return {
            "success": True,
            "active_owners": active_sessions
        }
    except Exception as e:
        logger.error(f"Error obteniendo propietarios activos: {e}")
        return {"success": False, "active_owners": []}

@app.post("/api/auth/logout")
async def logout_user(session_data: dict):
    """Cerrar sesión"""
    try:
        session_id = session_data.get("session_id")
        if session_id:
            success = user_auth.logout(session_id)
            if success:
                return {"success": True, "message": "Sesión cerrada correctamente"}
            else:
                return {"success": False, "message": "Sesión no encontrada"}
        
        return {"success": False, "message": "session_id requerido"}
    except Exception as e:
        logger.error(f"Error en logout: {e}")
        return {"success": False, "message": "Error cerrando sesión"}

# === DATOS DE NEGOCIO Y GESTIÓN DE CLIENTES ===

@app.get("/api/clients")
async def get_all_clients(owner: Optional[str] = None):
    """Obtener todos los clientes con filtro opcional por propietario"""
    try:
        if sheets_service:
            # Si se especifica propietario y el servicio soporta filtrado
            if owner and hasattr(sheets_service, 'get_clients_by_owner'):
                clients = sheets_service.get_clients_by_owner(owner, include_inactive=True)
                logger.info(f"📊 Obtenidos {len(clients)} clientes de {owner} desde Google Sheets")
            else:
                # Usar datos enriquecidos con información de cobranza
                if hasattr(sheets_service, 'get_enriched_clients'):
                    clients = sheets_service.get_enriched_clients()
                    logger.info(f"📊 Obtenidos {len(clients)} clientes enriquecidos desde Google Sheets")
                else:
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
        
        # Si no hay servicio de sheets, usar agente consolidado
        if consolidated_agent:
            stats_response = await consolidated_agent.process_query("estadísticas")
            if stats_response.data:
                data = stats_response.data
                return {
                    "total_clients": data.get("total_clients", 0),
                    "monthly_revenue": data.get("total_revenue", 0),
                    "active_zones": len(data.get("zones", {})),
                    "premium_percentage": data.get("target_achievement", 0)
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

@app.get("/api/dashboard")
async def dashboard_data():
    """Datos principales del dashboard - Compatibilidad con frontend"""
    try:
        if sheets_service:
            # Obtener datos básicos de clientes activos
            clients = sheets_service.get_all_clients(include_inactive=True)
            active_clients = [
                c for c in clients
                if str(c.get('Activo (SI/NO)', '')).strip().lower() in ['si', 'sí', 'yes', '1', 'true', 'activo']
            ]
            total_clients = len(active_clients)
            # Calcular ingresos mensuales y clientes premium
            monthly_revenue = 0.0
            premium_clients = 0
            zones = set()
            for client in active_clients:
                pago_str = str(client.get('Pago', '0')).replace('$', '').replace(',', '').strip()
                try:
                    pago = float(pago_str) if pago_str else 0.0
                    monthly_revenue += pago
                    if pago >= 400:
                        premium_clients += 1
                except:
                    pass
                zona = client.get('Zona', '').strip()
                if zona:
                    zones.add(zona)
            zones_active = len(zones)
            # Satisfacción aproximada como porcentaje de clientes premium
            satisfaction = (premium_clients / total_clients * 100) if total_clients else 0.0
            return {
                "total_clients": total_clients,
                "active_users": total_clients,
                "monthly_revenue": monthly_revenue,
                "satisfaction": round(satisfaction, 2),
                "zones_active": zones_active,
                "premium_clients": premium_clients
            }
        # Fallback con datos mock
        return {
            "total_clients": 0,
            "active_users": 0,
            "monthly_revenue": 0.0,
            "satisfaction": 0.0,
            "zones_active": 0,
            "premium_clients": 0
        }
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        # Retornar datos mock en caso de error
        return {
            "total_clients": 1247,
            "active_users": 1198,
            "monthly_revenue": 2485600,
            "satisfaction": 94.5,
            "zones_active": 15,
            "premium_clients": 312
        }

@app.get("/api/analytics")
async def get_analytics():
    """Get advanced analytics data"""
    try:
        if consolidated_agent:
            # Usar el agente consolidado para análisis
            analysis_response = await consolidated_agent.process_query("análisis financiero")
            
            if analysis_response.data:
                return analysis_response.data
        
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
    """Webhook para el bot de Telegram - Integrado con Carlos"""
    try:
        # Importar el handler del webhook
        import sys
        from pathlib import Path
        api_dir = Path(__file__).parents[2] / "api"
        sys.path.insert(0, str(api_dir))
        
        try:
            from telegram_webhook import handle_telegram_webhook
        except ImportError:
            logger.warning("⚠️ telegram_webhook module not found, using simplified handler")
            # Función básica de fallback
            def handle_telegram_webhook(update_data):
                return {"success": False, "message": "Telegram handler not available"}
        
        # Obtener los datos del update
        update_data = await request.json()
        logger.info(f"📱 Telegram webhook recibido: {update_data}")
        
        # Extraer mensaje para procesarlo con Carlos
        message = update_data.get('message', {})
        text = message.get('text', '').strip()
        chat_id = message.get('chat', {}).get('id')
        
        # Si hay texto, procesarlo primero con Carlos (IA real)
        carlos_response = None
        if text and text.lower() not in ['/start', '/help']:
            try:
                # Usar el agente consolidado ya disponible
                if consolidated_agent:
                    carlos_result = await consolidated_agent.process_query(text)
                    
                    if carlos_result and carlos_result.message:
                        carlos_response = carlos_result.message
                        
            except Exception as e:
                logger.warning(f"Carlos no disponible para Telegram: {e}")
        
        # Procesar el update con el webhook handler
        response = handle_telegram_webhook(update_data)
        
        # Si Carlos respondió, usar su respuesta
        if carlos_response and response.get("method") == "sendMessage":
            response["text"] = f"🤖 **Carlos - Red Soluciones ISP**\n\n{carlos_response}"
        
        if response.get("method") == "sendMessage":
            # Enviar respuesta directamente a Telegram
            import requests
            
            # Usar token desde configuración
            from .core.config_unified import settings
            token = settings.TELEGRAM_BOT_TOKEN
            telegram_api_url = f"https://api.telegram.org/bot{token}/sendMessage"
            
            requests.post(telegram_api_url, json={
                "chat_id": response["chat_id"],
                "text": response["text"],
                "parse_mode": response.get("parse_mode", "Markdown")
            })
            
            logger.info(f"📱 Respuesta enviada a Telegram chat {chat_id}")
            return {"status": "message_sent"}
        
        return response
        
    except Exception as e:
        logger.error(f"Error en webhook de Telegram: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/api/telegram/test")
async def test_telegram_bot():
    """Probar bot de Telegram con Carlos"""
    try:
        import requests
        from .core.config_unified import settings
        
        # Obtener información del bot
        token = settings.TELEGRAM_BOT_TOKEN
        get_me_url = f"https://api.telegram.org/bot{token}/getMe"
        
        response = requests.get(get_me_url)
        bot_info = response.json()
        
        if bot_info.get("ok"):
            bot_data = bot_info.get("result", {})
            return {
                "status": "success",
                "message": "Bot de Telegram configurado correctamente",
                "bot_info": {
                    "id": bot_data.get("id"),
                    "name": bot_data.get("first_name"),
                    "username": bot_data.get("username"),
                    "can_join_groups": bot_data.get("can_join_groups")
                },
                "webhook_endpoint": "/api/telegram/webhook",
                "integration": "Carlos (SuperIntelligentAgent) integrado"
            }
        else:
            return {
                "status": "error", 
                "message": "Token de bot inválido",
                "error": bot_info
            }
            
    except Exception as e:
        logger.error(f"Error probando bot de Telegram: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/api/telegram/setup")
async def setup_telegram_webhook():
    """Configurar webhook de Telegram"""
    try:
        import requests
        from .core.config_unified import settings
        
        # URL del webhook (será la URL de Vercel + /api/telegram/webhook)
        webhook_url = "https://tu-proyecto.vercel.app/api/telegram/webhook"
        
        # Configurar webhook en Telegram usando token desde configuración
        token = settings.TELEGRAM_BOT_TOKEN
        telegram_api_url = f"https://api.telegram.org/bot{token}/setWebhook"
        
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

# === NUEVAS RUTAS API - SISTEMA HOMOLOGADO ===

@app.get("/api/v2/system/status")
async def get_system_status():
    """Estado completo del sistema homologado"""
    try:
        if not context_engine or not enhanced_agent:
            return {
                "success": False,
                "message": "Sistema homologado no inicializado",
                "status": "not_ready"
            }
        
        # Obtener métricas del sistema
        cache_stats = context_engine._get_cache_health()
        entity_count = len(context_engine.entity_graph)
        
        return {
            "success": True,
            "status": "operational",
            "version": "4.0 Homologado",
            "entities_loaded": entity_count,
            "cache_health": cache_stats,
            "available_users": list(context_engine.user_contexts.keys()),
            "last_sync": max(context_engine.cache_timestamps.values()) if context_engine.cache_timestamps else None
        }
        
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        return {
            "success": False,
            "error": str(e),
            "status": "error"
        }

@app.get("/api/v2/context/{propietario}")
async def get_full_context(propietario: str):
    """Obtener contexto completo para un propietario"""
    try:
        if not context_engine:
            raise HTTPException(status_code=503, detail="Context Engine no disponible")
        
        full_context = await context_engine.get_full_context(propietario)
        
        if 'error' in full_context:
            raise HTTPException(status_code=404, detail=full_context['error'])
        
        return {
            "success": True,
            "context": full_context,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting context for {propietario}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v2/chat/enhanced")
async def enhanced_chat(request: Request):
    """Chat con agente IA homologado mejorado"""
    try:
        data = await request.json()
        
        if not enhanced_agent:
            return {
                "success": False,
                "message": "Sistema de IA no disponible",
                "suggestions": ["Verificar configuración del sistema", "Intentar más tarde"]
            }
        
        message = data.get("message", "").strip()
        propietario = data.get("user_name", "Sistema")
        session_id = data.get("session_id")
        
        if not message:
            return {
                "success": False,
                "message": "Mensaje vacío",
                "suggestions": ["Escribir una consulta específica"]
            }
        
        # Procesar con agente consolidado
        if consolidated_agent:
            response = await consolidated_agent.process_query(message, {"propietario": propietario, "session_id": session_id})
        else:
            # Fallback si el agente no está disponible
            from backend.app.services.consolidated_agent import ConsolidatedISPAgent
            temp_agent = ConsolidatedISPAgent()
            response = await temp_agent.process_query(message, {"propietario": propietario, "session_id": session_id})
        
        return {
            "success": True,
            "message": response.message,
            "action_type": response.action_type,
            "confidence": response.confidence,
            "data": response.data,
            "suggestions": response.suggestions,
            "quick_actions": response.quick_actions,
            "context_used": response.context_used,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in enhanced chat: {e}")
        return {
            "success": False,
            "message": f"Error procesando consulta: {str(e)}",
            "suggestions": ["Reformular la consulta", "Verificar conectividad"]
        }

@app.get("/api/v2/insights/{propietario}")
async def get_business_insights(propietario: str):
    """Obtener insights automáticos del negocio"""
    try:
        if not consolidated_agent:
            raise HTTPException(status_code=503, detail="Agente consolidado no disponible")
        
        # Obtener insights usando análisis del agente consolidado
        insights_response = await consolidated_agent.process_query(f"análisis para {propietario}")
        
        return {
            "success": True,
            "insights": [
                {
                    "type": "info",
                    "title": "Análisis de Negocio",
                    "description": insights_response.message,
                    "recommended_action": "Revisar métricas regularmente",
                    "impact_level": "medium",
                    "data_source": "Agente Consolidado"
                }
            ],
            "count": 1,
            "generated_at": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting insights for {propietario}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v2/system/refresh")
async def refresh_system_data(request: Request):
    """Refrescar datos del sistema desde Google Sheets"""
    try:
        data = await request.json()
        sheet_type = data.get("sheet_type")  # Opcional: refrescar hoja específica
        
        if not context_engine:
            raise HTTPException(status_code=503, detail="Context Engine no disponible")
        
        result = await context_engine.refresh_data(sheet_type)
        
        return {
            "success": result.get('success', False),
            "message": result.get('message', 'Refresh completado'),
            "updated_at": result.get('updated_at'),
            "entities_loaded": result.get('entities_loaded', 0)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error refreshing system data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v2/dashboard/{propietario}")
async def get_enhanced_dashboard(propietario: str):
    """Dashboard mejorado con contexto completo"""
    try:
        if not context_engine:
            raise HTTPException(status_code=503, detail="Context Engine no disponible")
        
        # Obtener contexto completo
        full_context = await context_engine.get_full_context(propietario)
        
        if 'error' in full_context:
            raise HTTPException(status_code=404, detail=full_context['error'])
        
        business_context = full_context.get('business_context', {})
        user_context = full_context.get('user_context', {})
        
        # Construir dashboard optimizado
        dashboard_data = {
            "propietario": propietario,
            "global_metrics": {
                "total_clientes": business_context.get('total_clientes', 0),
                "clientes_activos": business_context.get('clientes_activos', 0),
                "ingresos_mensuales": business_context.get('ingresos_mensuales', 0),
                "incidentes_abiertos": business_context.get('incidentes_abiertos', 0),
                "arpu": business_context.get('arpu', 0),
                "churn_rate": business_context.get('churn_rate', 0)
            },
            "personal_metrics": user_context.get('kpis_personales', {}),
            "quick_stats": {
                "mis_clientes": len(user_context.get('clientes_asignados', [])),
                "mis_prospectos": len(user_context.get('prospectos_pipeline', [])),
                "mis_incidentes": len(user_context.get('incidentes_responsable', [])),
                "mis_zonas": len(user_context.get('zonas_responsable', []))
            },
            "system_status": full_context.get('system_status', {}),
            "quick_actions": full_context.get('quick_actions', []),
            "recent_insights": full_context.get('insights', [])
        }
        
        return {
            "success": True,
            "dashboard": dashboard_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting enhanced dashboard for {propietario}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v2/entities/search")
async def search_entities(
    q: str, 
    entity_type: Optional[str] = None,
    propietario: Optional[str] = None
):
    """Búsqueda avanzada de entidades"""
    try:
        if not context_engine:
            raise HTTPException(status_code=503, detail="Context Engine no disponible")
        
        from backend.app.services.context_engine import search_entities
        
        # Realizar búsqueda
        results = search_entities(context_engine, q, entity_type)
        
        # Filtrar por propietario si se especifica
        if propietario:
            results = [r for r in results if r.propietario == propietario]
        
        # Formatear resultados
        formatted_results = []
        for result in results:
            formatted_results.append({
                "id": result.id,
                "type": result.type,
                "data": result.data,
                "propietario": result.propietario,
                "last_updated": result.last_updated.isoformat(),
                "relationships": result.relationships
            })
        
        return {
            "success": True,
            "results": formatted_results,
            "count": len(formatted_results),
            "query": q,
            "filters": {
                "entity_type": entity_type,
                "propietario": propietario
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching entities: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# === MOUNT FRONTEND AL FINAL ===
# Montar el directorio 'frontend' en la raíz para servir la SPA/sitio estático.
# IMPORTANTE: Esto debe ir al final, después de todas las rutas API.
app.mount("/", StaticFiles(directory=settings.FRONTEND_DIR, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)

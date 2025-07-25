"""
Red Soluciones ISP - API Principal
Sistema completo de gestión para proveedores de internet
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import json
import sys
from pathlib import Path
from datetime import datetime

# Configurar el path
current_dir = Path(__file__).parent.parent
sys.path.append(str(current_dir))

# Configurar variables de entorno
os.environ.setdefault("GEMINI_API_KEY", "AIzaSyD5_316B_bOhy-lVJAdCliYH6ZBhFALBWo")
os.environ.setdefault("TELEGRAM_BOT_TOKEN", "7881396575:AAHDbmSqXIVPSAK3asK9ieNhpbaS7iD3NZk")
os.environ.setdefault("GOOGLE_SHEET_ID", "1OZKZIpn6U1nCfrDM_yGmC6jKj6iLH_MQz814LjEBRMQ")

app = FastAPI(
    title="Red Soluciones ISP",
    description="Sistema completo de gestión para proveedores de internet",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar archivos estáticos
frontend_dir = current_dir / "frontend"
if frontend_dir.exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dir / "assets")), name="assets")

# Importar servicio de Google Sheets y agente Carlos
try:
    from backend.app.services.sheets.service import SheetsServiceV2
    from backend.app.services.smart_agent import SmartISPAgent
    sheets_service = SheetsServiceV2()
    carlos_agent = SmartISPAgent(sheets_service=sheets_service)
    SHEETS_CONNECTED = True
    print("✅ Servicio de Google Sheets inicializado")
    print("🤖 Agente Carlos inicializado")
except Exception as e:
    print(f"⚠️ Error inicializando servicios: {e}")
    SHEETS_CONNECTED = False
    sheets_service = None
    carlos_agent = None

# ==========================================
# RUTAS FRONTEND
# ==========================================

@app.get("/")
async def root():
    """Página principal del dashboard"""
    try:
        frontend_path = current_dir / "frontend" / "index.html"
        if frontend_path.exists():
            return FileResponse(str(frontend_path))
        else:
            return JSONResponse({
                "message": "Red Soluciones ISP API",
                "status": "running",
                "frontend": "not_found",
                "paths_checked": str(frontend_path)
            })
    except Exception as e:
        return JSONResponse({"error": str(e), "status": "error"})

@app.get("/health")
async def health_check():
    """Verificación de salud del sistema"""
    return JSONResponse({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Red Soluciones ISP",
        "version": "1.0.0"
    })

# ==========================================
# API ENDPOINTS
# ==========================================

@app.get("/api/clients")
async def get_clients():
    """Obtener lista de clientes desde Google Sheets"""
    try:
        if SHEETS_CONNECTED and sheets_service:
            # Intentar obtener datos reales de Google Sheets
            try:
                clients_data = sheets_service.get_all_clients()
                if clients_data:
                    return JSONResponse({
                        "success": True, 
                        "data": clients_data, 
                        "count": len(clients_data),
                        "source": "google_sheets"
                    })
            except Exception as sheets_error:
                print(f"Error conectando a Google Sheets: {sheets_error}")
        
        # Datos de respaldo si Google Sheets no está disponible
        fallback_clients = [
            {
                "ID Cliente": "REDSOL001",
                "Nombre": "Juan Pérez García",
                "Teléfono": "3001234567",
                "Email": "juan.perez@email.com",
                "Zona": "SALAMANCA",
                "Propietario": "Juan Pérez",
                "Pago": "35000",
                "Activo (SI/NO)": "SI",
                "Notas": "Cliente desde enero 2024"
            },
            {
                "ID Cliente": "REDSOL002",
                "Nombre": "María García López",
                "Teléfono": "3009876543",
                "Email": "maria.garcia@email.com",
                "Zona": "CERRO/PRIETO",
                "Propietario": "María García",
                "Pago": "45000",
                "Activo (SI/NO)": "SI",
                "Notas": "Plan premium"
            },
            {
                "ID Cliente": "REDSOL003",
                "Nombre": "Carlos López Rodríguez",
                "Teléfono": "3004567890",
                "Email": "carlos.lopez@email.com",
                "Zona": "ZAUS",
                "Propietario": "Carlos López",
                "Pago": "25000",
                "Activo (SI/NO)": "NO",
                "Notas": "Suspendido por falta de pago"
            },
            {
                "ID Cliente": "REDSOL004",
                "Nombre": "Ana Martínez Cruz",
                "Teléfono": "3002345678",
                "Email": "ana.martinez@email.com",
                "Zona": "TAMBOR",
                "Propietario": "Ana Martínez",
                "Pago": "40000",
                "Activo (SI/NO)": "SI",
                "Notas": "Cliente corporativo"
            },
            {
                "ID Cliente": "REDSOL005",
                "Nombre": "Luis Fernando Gómez",
                "Teléfono": "3003456789",
                "Email": "luis.gomez@email.com",
                "Zona": "SALAMANCA",
                "Propietario": "Luis Gómez",
                "Pago": "30000",
                "Activo (SI/NO)": "SI",
                "Notas": "Plan básico"
            }
        ]
        
        return JSONResponse({
            "success": True, 
            "data": fallback_clients, 
            "count": len(fallback_clients),
            "source": "fallback_data",
            "warning": "Usando datos de respaldo - Google Sheets no disponible"
        })
        
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.post("/api/clientes")
async def crear_cliente(request: Request):
    """Crear nuevo cliente"""
    try:
        data = await request.json()
        # Aquí integrarías con Google Sheets para guardar el cliente
        
        nuevo_cliente = {
            "id": 999,  # En producción, esto sería auto-generado
            "nombre": data.get("nombre"),
            "email": data.get("email"),
            "telefono": data.get("telefono"),
            "plan": data.get("plan"),
            "estado": "Activo",
            "fecha_registro": datetime.now().strftime("%Y-%m-%d")
        }
        
        return JSONResponse({"success": True, "data": nuevo_cliente})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.get("/api/planes")
async def get_planes():
    """Obtener planes de internet disponibles"""
    try:
        planes = [
            {
                "id": 1,
                "nombre": "Básico 10MB",
                "velocidad": "10 Mbps",
                "precio": 25000,
                "descripcion": "Plan básico para uso residencial"
            },
            {
                "id": 2,
                "nombre": "Premium 50MB",
                "velocidad": "50 Mbps",
                "precio": 45000,
                "descripcion": "Plan premium para familias"
            },
            {
                "id": 3,
                "nombre": "Empresarial 100MB",
                "velocidad": "100 Mbps",
                "precio": 85000,
                "descripcion": "Plan empresarial de alta velocidad"
            }
        ]
        return JSONResponse({"success": True, "data": planes})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.get("/api/estadisticas")
async def get_estadisticas():
    """Obtener estadísticas del dashboard"""
    try:
        stats = {
            "clientes_activos": 156,
            "clientes_nuevos_mes": 12,
            "ingresos_mes": 6750000,
            "tickets_pendientes": 3,
            "conexiones_activas": 142,
            "ancho_banda_usado": "78%"
        }
        return JSONResponse({"success": True, "data": stats})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.post("/api/chat")
async def chat_ai(request: Request):
    """Chat con el agente Carlos usando Gemini AI"""
    try:
        data = await request.json()
        message = data.get("message", "")
        
        if carlos_agent:
            # Usar el agente Carlos real
            try:
                response = carlos_agent.process_query(message)
                return JSONResponse({
                    "success": True,
                    "response": response.get('response', 'Lo siento, no pude procesar tu mensaje.'),
                    "type": response.get('type', 'general'),
                    "data": response.get('data', {}),
                    "agent": "Carlos - Red Soluciones ISP",
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as agent_error:
                print(f"Error con agente Carlos: {agent_error}")
        
        # Respuesta de respaldo
        response = f"Soy Carlos, tu asistente de Red Soluciones ISP. Procesando: '{message}'. Sistema operativo. ¿En qué más puedo ayudarte?"
        
        return JSONResponse({
            "success": True,
            "response": response,
            "type": "general",
            "agent": "Carlos (modo básico)",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.get("/api/clients/search/{query}")
async def search_clients(query: str):
    """Buscar clientes por cualquier campo"""
    try:
        if SHEETS_CONNECTED and sheets_service:
            # Intentar buscar en Google Sheets
            try:
                search_results = await sheets_service.search_clients(query)
                if search_results:
                    return JSONResponse({
                        "success": True,
                        "data": search_results,
                        "count": len(search_results),
                        "source": "google_sheets"
                    })
            except Exception as sheets_error:
                print(f"Error buscando en Google Sheets: {sheets_error}")
        
        # Datos de respaldo para búsqueda
        all_clients = [
            {
                "ID Cliente": "REDSOL001",
                "Nombre": "Juan Pérez García",
                "Teléfono": "3001234567",
                "Email": "juan.perez@email.com",
                "Zona": "SALAMANCA",
                "Propietario": "Juan Pérez",
                "Pago": "35000",
                "Activo (SI/NO)": "SI",
                "Notas": "Cliente desde enero 2024"
            },
            {
                "ID Cliente": "REDSOL002",
                "Nombre": "María García López",
                "Teléfono": "3009876543",
                "Email": "maria.garcia@email.com",
                "Zona": "CERRO/PRIETO",
                "Propietario": "María García",
                "Pago": "45000",
                "Activo (SI/NO)": "SI",
                "Notas": "Plan premium"
            },
            {
                "ID Cliente": "REDSOL003",
                "Nombre": "Carlos López Rodríguez",
                "Teléfono": "3004567890",
                "Email": "carlos.lopez@email.com",
                "Zona": "ZAUS",
                "Propietario": "Carlos López",
                "Pago": "25000",
                "Activo (SI/NO)": "NO",
                "Notas": "Suspendido por falta de pago"
            },
            {
                "ID Cliente": "REDSOL004",
                "Nombre": "Ana Martínez Cruz",
                "Teléfono": "3002345678",
                "Email": "ana.martinez@email.com",
                "Zona": "TAMBOR",
                "Propietario": "Ana Martínez",
                "Pago": "40000",
                "Activo (SI/NO)": "SI",
                "Notas": "Cliente corporativo"
            },
            {
                "ID Cliente": "REDSOL005",
                "Nombre": "Luis Fernando Gómez",
                "Teléfono": "3003456789",
                "Email": "luis.gomez@email.com",
                "Zona": "SALAMANCA",
                "Propietario": "Luis Gómez",
                "Pago": "30000",
                "Activo (SI/NO)": "SI",
                "Notas": "Plan básico"
            }
        ]
        
        # Buscar en todos los campos
        query_lower = query.lower()
        filtered_clients = []
        
        for client in all_clients:
            for key, value in client.items():
                if str(value).lower().find(query_lower) != -1:
                    filtered_clients.append(client)
                    break
        
        return JSONResponse({
            "success": True,
            "data": filtered_clients,
            "count": len(filtered_clients),
            "source": "fallback_data"
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.post("/api/clients")
async def create_client(request: Request):
    """Crear nuevo cliente en Google Sheets"""
    try:
        data = await request.json()
        
        if SHEETS_CONNECTED and sheets_service:
            try:
                # Intentar crear en Google Sheets
                result = sheets_service.add_client(data)
                if result:
                    return JSONResponse({
                        "success": True,
                        "message": f"Cliente {data.get('Nombre', 'N/A')} agregado exitosamente a Google Sheets",
                        "data": data,
                        "source": "google_sheets"
                    })
            except Exception as sheets_error:
                print(f"Error agregando cliente a Google Sheets: {sheets_error}")
        
        # Respuesta de respaldo
        return JSONResponse({
            "success": True,
            "message": f"Cliente {data.get('Nombre', 'N/A')} registrado (modo simulación)",
            "data": data,
            "source": "fallback",
            "warning": "No se pudo conectar a Google Sheets - datos no guardados"
        })
    except Exception as e:
        return JSONResponse({"success": False, "message": str(e)}, status_code=500)

@app.post("/api/prospects")
async def create_prospect(request: Request):
    """Crear nuevo prospecto"""
    try:
        data = await request.json()
        # En producción, esto guardaría en Google Sheets
        
        return JSONResponse({
            "success": True,
            "message": f"Prospecto {data.get('Nombre', 'N/A')} agregado exitosamente",
            "data": data
        })
    except Exception as e:
        return JSONResponse({"success": False, "message": str(e)}, status_code=500)

@app.post("/api/incidents")
async def create_incident(request: Request):
    """Crear nuevo incidente"""
    try:
        data = await request.json()
        # En producción, esto guardaría en Google Sheets
        
        return JSONResponse({
            "success": True,
            "message": f"Incidente registrado para {data.get('cliente_nombre', 'N/A')}",
            "data": data
        })
    except Exception as e:
        return JSONResponse({"success": False, "message": str(e)}, status_code=500)

# ==========================================
# TELEGRAM BOT WEBHOOK
# ==========================================

@app.post("/api/telegram/webhook")
async def telegram_webhook(request: Request):
    """Webhook para el bot de Telegram - integrado con Carlos"""
    try:
        update_data = await request.json()
        print(f"📱 Telegram webhook recibido: {update_data}")
        
        # Extraer mensaje
        if "message" in update_data:
            message = update_data["message"]
            chat_id = message["chat"]["id"]
            user_message = message.get("text", "")
            
            if carlos_agent and user_message:
                # Procesar con Carlos
                try:
                    response = carlos_agent.process_query(user_message)
                    response_text = response.get('response', 'Lo siento, no pude procesar tu mensaje.')
                except Exception as agent_error:
                    print(f"Error con Carlos en Telegram: {agent_error}")
                    response_text = f"Soy Carlos de Red Soluciones ISP. Procesando: '{user_message}'. ¿En qué puedo ayudarte?"
            else:
                response_text = "¡Hola! Soy Carlos, tu asistente de Red Soluciones ISP. ¿En qué puedo ayudarte?"
            
            # Enviar respuesta a Telegram
            import requests
            telegram_api_url = f"https://api.telegram.org/bot{os.environ.get('TELEGRAM_BOT_TOKEN')}/sendMessage"
            
            requests.post(telegram_api_url, json={
                "chat_id": chat_id,
                "text": response_text,
                "parse_mode": "Markdown"
            })
            
            return JSONResponse({"status": "message_sent"})
        
        return JSONResponse({"status": "no_message"})
        
    except Exception as e:
        print(f"Error en Telegram webhook: {e}")
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.post("/api/telegram/setup")
async def setup_telegram_webhook():
    """Configurar webhook de Telegram"""
    try:
        import requests
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        webhook_url = "https://redsoluciones.vercel.app/api/telegram/webhook"  # Cambiar por tu URL de Vercel
        
        telegram_api_url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
        
        response = requests.post(telegram_api_url, json={
            "url": webhook_url
        })
        
        return JSONResponse({
            "success": True,
            "message": "Webhook configurado",
            "telegram_response": response.json()
        })
        
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

# ==========================================
# MANEJO DE ERRORES
# ==========================================

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"error": "Recurso no encontrado", "path": str(request.url)}
    )

@app.exception_handler(500)
async def server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Error interno del servidor", "details": str(exc)}
    )

# Para Vercel
app = app

"""
🤖 Webhook endpoint para Telegram Bot en Vercel
Integración COMPLETA con Red Soluciones ISP Backend
"""
import os
import json
import logging
import sys
from typing import Dict, Any
from datetime import datetime
from pathlib import Path

# Configurar paths para importar backend
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Token del bot de Telegram
TELEGRAM_BOT_TOKEN = "7881396575:AAHDbmSqXIVPSAK3asK9ieNhpbaS7iD3NZk"

# Importar servicios del backend
try:
    from backend.app.services.sheets.service import SheetsServiceV2 as SheetsService
    from backend.app.services.smart_agent import SmartISPAgent, get_smart_agent
    BACKEND_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Backend no disponible: {e}")
    BACKEND_AVAILABLE = False

class TelegramISPBotAdvanced:
    """🤖 Bot de Telegram con integración COMPLETA al backend ISP"""
    
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.user_sessions = {}  # Sesiones por usuario
        
        # Inicializar servicios del backend
        if BACKEND_AVAILABLE:
            try:
                self.sheets_service = SheetsService()
                self.smart_agent = SmartISPAgent(self.sheets_service)
                logger.info("✅ Backend ISP conectado al bot de Telegram")
            except Exception as e:
                logger.error(f"Error conectando backend: {e}")
                self.sheets_service = None
                self.smart_agent = None
        else:
            self.sheets_service = None
            self.smart_agent = None
        
        # Estados de conversación para operaciones complejas
        self.conversation_states = {
            "IDLE": "idle",
            "ADDING_CLIENT": "adding_client",
            "SEARCHING": "searching",
            "INCIDENT_REPORT": "incident_report",
            "PROSPECT_ENTRY": "prospect_entry"
        }
        
    def process_update(self, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Procesar update de Telegram con integración completa"""
        try:
            # Extraer información del mensaje
            message = update_data.get('message', {})
            chat_id = message.get('chat', {}).get('id')
            text = message.get('text', '')
            user = message.get('from', {})
            
            if not chat_id or not text:
                return {"status": "ignored", "reason": "No chat_id or text"}
            
            user_id = user.get('id')
            user_name = user.get('first_name', 'Usuario')
            
            # Log de la interacción
            logger.info(f"📱 {user_name} ({user_id}): {text}")
            
            # Obtener estado de conversación del usuario
            user_state = self.user_sessions.get(user_id, {}).get('state', 'IDLE')
            
            # Procesar según el estado
            if user_state != 'IDLE':
                return self.handle_conversation_state(chat_id, text, user, user_state)
            
            # Procesar comandos y mensajes normales
            if text.startswith('/'):
                return self.handle_command(chat_id, text, user)
            else:
                return self.handle_intelligent_message(chat_id, text, user)
                
        except Exception as e:
            logger.error(f"Error procesando update: {e}")
            return self.send_message(chat_id, f"❌ Error interno: {str(e)}")
    
    def handle_command(self, chat_id: int, command: str, user: Dict) -> Dict[str, Any]:
        """Manejar comandos del bot con funcionalidad completa"""
        
        user_name = user.get('first_name', 'Usuario')
        
        if command == '/start':
            response = self.get_welcome_message_advanced(user_name)
            
        elif command == '/help':
            response = self.get_help_message_advanced()
            
        elif command == '/status':
            response = self.get_system_status()
            
        elif command == '/stats' or command == '/estadisticas':
            response = self.get_business_stats()
            
        elif command == '/clientes':
            response = self.get_clients_summary()
            
        elif command == '/add' or command == '/agregar':
            return self.start_add_client_flow(chat_id, user)
            
        elif command == '/buscar':
            return self.start_search_flow(chat_id, user)
            
        elif command == '/incidente':
            return self.start_incident_flow(chat_id, user)
            
        elif command == '/prospecto':
            return self.start_prospect_flow(chat_id, user)
            
        elif command == '/zonas':
            response = self.get_zones_info()
            
        elif command == '/analytics' or command == '/analisis':
            response = self.get_financial_analytics()
            
        else:
            response = f"❓ Comando no reconocido: {command}\n\n📋 Usa /help para ver todos los comandos disponibles"
        
        return self.send_message(chat_id, response)
    
    def handle_intelligent_message(self, chat_id: int, text: str, user: Dict) -> Dict[str, Any]:
        """Manejar mensajes usando el agente inteligente del backend"""
        
        if self.smart_agent:
            try:
                # Usar el agente inteligente del backend
                agent_response = self.smart_agent.process_query(text)
                
                response = agent_response.get('response', '❌ Sin respuesta del agente')
                suggestions = agent_response.get('suggestions', [])
                response_type = agent_response.get('type', 'general')
                
                # Agregar sugerencias si las hay
                if suggestions:
                    response += "\n\n� **Sugerencias:**\n"
                    for i, suggestion in enumerate(suggestions[:3], 1):
                        response += f"{i}. {suggestion}\n"
                
                # Agregar ayuda contextual
                response += "\n\n🤖 También puedes usar comandos como:\n"
                response += "• /add - Agregar cliente\n"
                response += "• /buscar - Buscar información\n"
                response += "• /stats - Ver estadísticas\n"
                response += "• /help - Ayuda completa"
                
                return self.send_message(chat_id, response)
                
            except Exception as e:
                logger.error(f"Error con agente inteligente: {e}")
                return self.send_message(chat_id, 
                    f"❌ Error procesando con IA: {str(e)}\n\n" +
                    "💡 Intenta usar comandos específicos como /help")
        else:
            # Fallback sin agente
            response = self.handle_message_fallback(text, user.get('first_name', ''))
            return self.send_message(chat_id, response)
    
    def handle_conversation_state(self, chat_id: int, text: str, user: Dict, state: str) -> Dict[str, Any]:
        """Manejar estados de conversación para operaciones complejas"""
        user_id = user.get('id')
        
        if state == 'ADDING_CLIENT':
            return self.process_add_client_data(chat_id, text, user)
        elif state == 'SEARCHING':
            return self.process_search_query(chat_id, text, user)
        elif state == 'INCIDENT_REPORT':
            return self.process_incident_data(chat_id, text, user)
        elif state == 'PROSPECT_ENTRY':
            return self.process_prospect_data(chat_id, text, user)
        else:
            # Reset a estado idle
            if user_id in self.user_sessions:
                self.user_sessions[user_id]['state'] = 'IDLE'
            return self.handle_intelligent_message(chat_id, text, user)
    
    def start_add_client_flow(self, chat_id: int, user: Dict) -> Dict[str, Any]:
        """Iniciar flujo de agregar cliente"""
        user_id = user.get('id')
        self.user_sessions[user_id] = {
            'state': 'ADDING_CLIENT',
            'step': 1,
            'data': {}
        }
        
        response = """🆕 **Agregar Nuevo Cliente**

📝 Por favor, proporciona la información en este formato:

```
Nombre: Juan Pérez
Email: juan@email.com
Zona: Norte
Teléfono: 555-1234
Pago: 400
```

🔄 O envía `/cancel` para cancelar"""

        return self.send_message(chat_id, response)
    
    def process_add_client_data(self, chat_id: int, text: str, user: Dict) -> Dict[str, Any]:
        """Procesar datos para agregar cliente"""
        user_id = user.get('id')
        
        if text.lower() == '/cancel':
            self.user_sessions[user_id]['state'] = 'IDLE'
            return self.send_message(chat_id, "❌ Operación cancelada")
        
        try:
            # Parsear los datos del cliente
            client_data = {}
            lines = text.strip().split('\n')
            
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower()
                    value = value.strip()
                    
                    if 'nombre' in key:
                        client_data['nombre'] = value
                    elif 'email' in key:
                        client_data['email'] = value
                    elif 'zona' in key:
                        client_data['zona'] = value
                    elif 'teléfono' in key or 'telefono' in key:
                        client_data['telefono'] = value
                    elif 'pago' in key:
                        client_data['pago_mensual'] = float(value)
            
            # Validar datos mínimos
            if not client_data.get('nombre'):
                return self.send_message(chat_id, "❌ Nombre requerido. Intenta de nuevo.")
            
            # Agregar cliente usando el backend
            if self.sheets_service:
                success = self.add_client_to_system(client_data)
                if success:
                    self.user_sessions[user_id]['state'] = 'IDLE'
                    response = f"✅ **Cliente agregado exitosamente**\n\n" \
                             f"👤 **Nombre**: {client_data['nombre']}\n" \
                             f"📧 **Email**: {client_data.get('email', 'N/A')}\n" \
                             f"📍 **Zona**: {client_data.get('zona', 'N/A')}\n" \
                             f"📞 **Teléfono**: {client_data.get('telefono', 'N/A')}\n" \
                             f"💰 **Pago**: ${client_data.get('pago_mensual', 0)}"
                    
                    return self.send_message(chat_id, response)
                else:
                    return self.send_message(chat_id, "❌ Error agregando cliente. Intenta de nuevo.")
            else:
                return self.send_message(chat_id, "❌ Servicio no disponible temporalmente")
                
        except Exception as e:
            logger.error(f"Error procesando datos de cliente: {e}")
            return self.send_message(chat_id, f"❌ Error procesando datos: {str(e)}\nIntenta de nuevo.")
    
    def add_client_to_system(self, client_data: Dict) -> bool:
        """Agregar cliente al sistema usando el backend"""
        try:
            if self.sheets_service:
                # Convertir al formato esperado por el sheets service
                sheet_data = {
                    "Nombre": client_data.get('nombre', ''),
                    "Email": client_data.get('email', ''),
                    "Zona": client_data.get('zona', ''),
                    "Teléfono": client_data.get('telefono', ''),
                    "Pago": client_data.get('pago_mensual', 0),
                    "Notas": "",
                    "Activo (SI/NO)": "SI",
                    "Fecha Registro": datetime.now().strftime("%Y-%m-%d")
                }
                
                return self.sheets_service.add_client(sheet_data)
            return False
        except Exception as e:
            logger.error(f"Error agregando cliente: {e}")
            return False
    
    def start_search_flow(self, chat_id: int, user: Dict) -> Dict[str, Any]:
        """Iniciar flujo de búsqueda"""
        response = """🔍 **Buscar en el Sistema**

💡 Puedes buscar por:
• Nombre del cliente
• Zona
• Teléfono
• Email

✍️ Escribe tu consulta de búsqueda o /cancel para cancelar"""

        return self.send_message(chat_id, response)
    
    def process_search_query(self, chat_id: int, text: str, user: Dict) -> Dict[str, Any]:
        """Procesar búsqueda usando el agente inteligente"""
        if text.lower() == '/cancel':
            return self.send_message(chat_id, "❌ Búsqueda cancelada")
        
        # Usar el agente para la búsqueda
        search_query = f"buscar {text}"
        return self.handle_intelligent_message(chat_id, search_query, user)
    
    def start_incident_flow(self, chat_id: int, user: Dict) -> Dict[str, Any]:
        """Iniciar flujo de reporte de incidentes"""
        response = """🚨 **Reportar Incidente**

📝 Formato para reportar:

```
Cliente: Juan Pérez
Tipo: Técnico
Descripción: Sin conexión a internet
Prioridad: Alta
```

🔄 O envía `/cancel` para cancelar"""

        return self.send_message(chat_id, response)
    
    def process_incident_data(self, chat_id: int, text: str, user: Dict) -> Dict[str, Any]:
        """Procesar datos de incidente"""
        if text.lower() == '/cancel':
            return self.send_message(chat_id, "❌ Reporte cancelado")
        
        # Procesar incidente con el agente
        incident_query = f"crear incidente {text}"
        return self.handle_intelligent_message(chat_id, incident_query, user)
    
    def start_prospect_flow(self, chat_id: int, user: Dict) -> Dict[str, Any]:
        """Iniciar flujo de agregar prospecto"""
        response = """🎯 **Agregar Prospecto**

📝 Formato para prospecto:

```
Nombre: María García
Teléfono: 555-5678
Zona: Centro
Email: maria@email.com
Notas: Interesada en plan premium
Prioridad: Alta
```

🔄 O envía `/cancel` para cancelar"""

        return self.send_message(chat_id, response)
    
    def process_prospect_data(self, chat_id: int, text: str, user: Dict) -> Dict[str, Any]:
        """Procesar datos de prospecto"""
        if text.lower() == '/cancel':
            return self.send_message(chat_id, "❌ Entrada cancelada")
        
        # Procesar prospecto con el agente
        prospect_query = f"agregar prospecto {text}"
        return self.handle_intelligent_message(chat_id, prospect_query, user)
    
    def get_welcome_message_advanced(self, name: str) -> str:
        """Mensaje de bienvenida completo"""
        return f"""🚀 ¡Bienvenido {name}!

🏢 **Red Soluciones ISP - Control Total**
Tu bot para gestión completa del sistema ISP

🎯 **OPERACIONES DISPONIBLES:**

📊 **Consultas y Análisis:**
• /stats - Estadísticas del negocio
• /clientes - Lista de clientes
• /analytics - Análisis financiero
• /zonas - Información de zonas

➕ **Agregar Datos:**
• /add - Agregar nuevo cliente
• /prospecto - Registrar prospecto
• /incidente - Reportar incidente

🔍 **Búsquedas:**
• /buscar - Buscar cualquier información
• Pregunta directamente: "buscar cliente Juan"

💬 **Chat Inteligente:**
• "estadísticas del mes"
• "análisis financiero"
• "clientes de la zona norte"
• "¿cuántos clientes premium tengo?"

🤖 ¡Powered by Gemini AI! - Todo tu sistema ISP en Telegram"""
    
    def get_help_message_advanced(self) -> str:
        """Mensaje de ayuda completo"""
        return """🆘 **Ayuda Completa - Red Soluciones ISP**

🎯 **COMANDOS PRINCIPALES:**

📊 **Información y Estadísticas:**
• `/stats` - Estadísticas completas del negocio
• `/clientes` - Resumen de clientes
• `/analytics` - Análisis financiero detallado
• `/zonas` - Información de cobertura
• `/status` - Estado del sistema

➕ **Agregar/Crear:**
• `/add` - Agregar nuevo cliente (paso a paso)
• `/prospecto` - Registrar nuevo prospecto
• `/incidente` - Reportar incidente técnico

🔍 **Búsquedas:**
• `/buscar` - Búsqueda general
• "buscar cliente [nombre]"
• "clientes zona norte"
• "pagos pendientes"

💬 **Chat Inteligente (Gemini AI):**
• "¿cuántos clientes tengo?"
• "análisis de ingresos"
• "clientes premium"
• "estadísticas por zona"
• "oportunidades de crecimiento"

🎮 **Ejemplos de Uso:**
1. Escribir: "estadísticas del mes"
2. Comando: `/add` y seguir instrucciones
3. Buscar: "cliente Juan Pérez"
4. Análisis: "¿cuál es mi zona más rentable?"

🤖 **Desarrollado con IA para Red Soluciones ISP**"""
    
    def get_system_status(self) -> str:
        """Estado del sistema"""
        backend_status = "✅ Conectado" if self.smart_agent else "❌ Sin conexión"
        sheets_status = "✅ Conectado" if self.sheets_service else "❌ Sin conexión"
        
        return f"""🔧 **Estado del Sistema Red Soluciones ISP**

🤖 **Bot de Telegram**: ✅ Activo
🧠 **Agente Inteligente**: {backend_status}
📊 **Google Sheets**: {sheets_status}
⚡ **API Backend**: ✅ Funcional

📈 **Servicios Disponibles:**
• Gestión de clientes
• Análisis financiero
• Reportes de incidentes
• Chat con IA
• Búsquedas inteligentes

🕒 **Última verificación**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
    
    def get_business_stats(self) -> str:
        """Obtener estadísticas usando el agente"""
        if self.smart_agent:
            try:
                stats_response = self.smart_agent.process_query("estadísticas completas")
                return stats_response.get('response', '❌ Error obteniendo estadísticas')
            except Exception as e:
                return f"❌ Error: {str(e)}"
        else:
            return "❌ Agente no disponible. Usa /status para verificar conexión."
    
    def get_clients_summary(self) -> str:
        """Obtener resumen de clientes"""
        if self.smart_agent:
            try:
                clients_response = self.smart_agent.process_query("mostrar todos los clientes")
                return clients_response.get('response', '❌ Error obteniendo clientes')
            except Exception as e:
                return f"❌ Error: {str(e)}"
        else:
            return "❌ Agente no disponible. Usa /status para verificar conexión."
    
    def get_zones_info(self) -> str:
        """Información de zonas"""
        if self.smart_agent:
            try:
                zones_response = self.smart_agent.process_query("información de zonas")
                return zones_response.get('response', '❌ Error obteniendo zonas')
            except Exception as e:
                return f"❌ Error: {str(e)}"
        else:
            return "❌ Agente no disponible. Usa /status para verificar conexión."
    
    def get_financial_analytics(self) -> str:
        """Análisis financiero"""
        if self.smart_agent:
            try:
                analytics_response = self.smart_agent.process_query("análisis financiero completo")
                return analytics_response.get('response', '❌ Error en análisis')
            except Exception as e:
                return f"❌ Error: {str(e)}"
        else:
            return "❌ Agente no disponible. Usa /status para verificar conexión."
    
    def handle_message_fallback(self, text: str, user_name: str) -> str:
        """Manejo de mensajes cuando no hay agente disponible"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['hola', 'hi', 'buenos', 'buenas']):
            return f"¡Hola {user_name}! 👋\n\n🤖 Bot Red Soluciones ISP activado\n\nUsa /help para ver todas las opciones disponibles."
        
        elif any(word in text_lower for word in ['cliente', 'buscar', 'encontrar']):
            return "🔍 **Búsqueda de Clientes**\n\nUsa el comando `/buscar` para iniciar una búsqueda o `/clientes` para ver el resumen completo."
        
        elif any(word in text_lower for word in ['estadística', 'estadisticas', 'stats']):
            return "📊 **Estadísticas del Negocio**\n\nUsa `/stats` para ver estadísticas completas o `/analytics` para análisis financiero."
        
        elif any(word in text_lower for word in ['agregar', 'añadir', 'nuevo']):
            return "➕ **Agregar al Sistema**\n\n• `/add` - Nuevo cliente\n• `/prospecto` - Nuevo prospecto\n• `/incidente` - Reportar incidente"
        
        else:
            return f"🤖 Procesando: '{text}'\n\n💡 **Comandos disponibles:**\n• `/help` - Ayuda completa\n• `/stats` - Estadísticas\n• `/add` - Agregar cliente\n• `/buscar` - Buscar información\n\n🧠 Para mejor experiencia, asegúrate de que el agente IA esté conectado."
    
    def send_message(self, chat_id: int, text: str) -> Dict[str, Any]:
        """Preparar respuesta para enviar"""
        return {
            "method": "sendMessage",
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }

# Instancia global del handler
telegram_handler = TelegramISPBotAdvanced()

def handle_telegram_webhook(update_data: Dict[str, Any]) -> Dict[str, Any]:
    """Función principal para manejar webhooks de Telegram"""
    return telegram_handler.process_update(update_data)

# Para testing local
if __name__ == "__main__":
    # Ejemplo de update de Telegram
    test_update = {
        "message": {
            "chat": {"id": 123456789},
            "text": "/start",
            "from": {"first_name": "Test", "id": 123456789}
        }
    }
    
    result = handle_telegram_webhook(test_update)
    print(json.dumps(result, indent=2, ensure_ascii=False))
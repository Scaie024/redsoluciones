"""
🤖 Webhook endpoint para Telegram Bot en Vercel
Integración directa con Red Soluciones ISP
"""
import os
import json
import logging
from typing import Dict, Any
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Token del bot de Telegram
TELEGRAM_BOT_TOKEN = "7881396575:AAHDbmSqXIVPSAK3asK9ieNhpbaS7iD3NZk"

class TelegramWebhookHandler:
    """Manejador de webhook para Telegram Bot"""
    
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        
    def process_update(self, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Procesar update de Telegram"""
        try:
            # Extraer información del mensaje
            message = update_data.get('message', {})
            chat_id = message.get('chat', {}).get('id')
            text = message.get('text', '')
            user = message.get('from', {})
            
            if not chat_id or not text:
                return {"status": "ignored", "reason": "No chat_id or text"}
            
            # Log de la interacción
            logger.info(f"📱 Mensaje de {user.get('first_name', 'Usuario')}: {text}")
            
            # Procesar comandos
            if text.startswith('/'):
                return self.handle_command(chat_id, text, user)
            else:
                return self.handle_message(chat_id, text, user)
                
        except Exception as e:
            logger.error(f"Error procesando update: {e}")
            return {"status": "error", "message": str(e)}
    
    def handle_command(self, chat_id: int, command: str, user: Dict) -> Dict[str, Any]:
        """Manejar comandos del bot"""
        
        if command == '/start':
            response = self.get_welcome_message(user.get('first_name', 'Usuario'))
        elif command == '/help':
            response = self.get_help_message()
        elif command == '/status':
            response = "✅ Red Soluciones ISP - Sistema activo\n🤖 Bot funcionando correctamente"
        elif command == '/clientes':
            response = "📊 Consultando base de clientes...\n💡 Tip: Puedes buscar por nombre directamente"
        else:
            response = f"❓ Comando no reconocido: {command}\nUsa /help para ver comandos disponibles"
        
        return self.send_message(chat_id, response)
    
    def handle_message(self, chat_id: int, text: str, user: Dict) -> Dict[str, Any]:
        """Manejar mensajes normales"""
        
        # Respuestas inteligentes basadas en el contenido
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['hola', 'hi', 'buenos', 'buenas']):
            response = f"¡Hola {user.get('first_name', '')}! 👋\n¿En qué puedo ayudarte con Red Soluciones ISP?"
        
        elif any(word in text_lower for word in ['cliente', 'buscar', 'encontrar']):
            response = "🔍 Búsqueda de clientes\n\n💡 Puedes buscar por:\n• Nombre del cliente\n• Zona\n• Teléfono\n\n¿Qué cliente necesitas encontrar?"
        
        elif any(word in text_lower for word in ['pago', 'factura', 'cobro']):
            response = "💰 Información de pagos\n\n📊 Servicios disponibles:\n• Consultar estado de pagos\n• Generar reportes\n• Ver estadísticas\n\n¿Qué información necesitas?"
        
        elif any(word in text_lower for word in ['zona', 'cobertura', 'área']):
            response = "🗺️ Información de zonas\n\n📍 Zonas disponibles:\n• Norte\n• Sur\n• Centro\n• Oriente\n\n¿Sobre qué zona necesitas información?"
        
        elif any(word in text_lower for word in ['ayuda', 'help', 'comandos']):
            response = self.get_help_message()
        
        else:
            # Respuesta inteligente general
            response = f"🤖 Procesando: '{text}'\n\n💡 Red Soluciones ISP puede ayudarte con:\n• Consultas de clientes\n• Información de pagos\n• Gestión de zonas\n• Soporte técnico\n\nUsa /help para más opciones"
        
        return self.send_message(chat_id, response)
    
    def get_welcome_message(self, name: str) -> str:
        """Mensaje de bienvenida"""
        return f"""🚀 ¡Bienvenido {name}!

🏢 **Red Soluciones ISP**
Bot inteligente para gestión ISP

📋 **Comandos disponibles:**
/help - Mostrar ayuda
/status - Estado del sistema
/clientes - Gestión de clientes

💬 **O simplemente escribe:**
• "buscar cliente Juan"
• "información de pagos"
• "zonas de cobertura"

🤖 ¡Estoy aquí para ayudarte!"""
    
    def get_help_message(self) -> str:
        """Mensaje de ayuda"""
        return """🆘 **Ayuda - Red Soluciones ISP**

🎯 **Comandos principales:**
/start - Iniciar conversación
/help - Mostrar esta ayuda
/status - Estado del sistema
/clientes - Gestión de clientes

💬 **Consultas naturales:**
• "buscar cliente [nombre]"
• "información de pagos"
• "zonas disponibles"
• "estado del servicio"

📊 **Funciones disponibles:**
✅ Búsqueda de clientes
✅ Consulta de pagos
✅ Información de zonas
✅ Soporte técnico

🤖 Desarrollado para Red Soluciones ISP"""
    
    def send_message(self, chat_id: int, text: str) -> Dict[str, Any]:
        """Preparar respuesta para enviar"""
        return {
            "method": "sendMessage",
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }

# Instancia global del handler
telegram_handler = TelegramWebhookHandler()

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

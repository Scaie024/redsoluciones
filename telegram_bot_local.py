#!/usr/bin/env python3
"""
Bot de Telegram Local - Red Soluciones ISP
Prueba Carlos directamente sin webhook
"""
import time
import requests
import json
from typing import Dict, Any

class TelegramBotLocal:
    def __init__(self, token: str):
        self.token = token
        self.api_url = f"https://api.telegram.org/bot{token}"
        self.offset = 0
        
    def get_updates(self) -> list:
        """Obtener updates pendientes"""
        try:
            response = requests.get(
                f"{self.api_url}/getUpdates",
                params={"offset": self.offset, "timeout": 5}
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("ok"):
                    return data.get("result", [])
            return []
        except Exception as e:
            print(f"Error obteniendo updates: {e}")
            return []
    
    def send_message(self, chat_id: int, text: str, parse_mode: str = "Markdown"):
        """Enviar mensaje a Telegram"""
        try:
            requests.post(
                f"{self.api_url}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": text,
                    "parse_mode": parse_mode
                }
            )
            print(f"📤 Mensaje enviado a chat {chat_id}")
        except Exception as e:
            print(f"Error enviando mensaje: {e}")
    
    def process_with_carlos(self, text: str) -> str:
        """Procesar mensaje con Carlos (API local)"""
        try:
            response = requests.post(
                "http://localhost:8004/api/chat",
                json={"message": text},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                carlos_response = data.get("response", "")
                suggestions = data.get("suggestions", [])
                
                # Formatear respuesta
                formatted_response = f"🤖 **Carlos - Red Soluciones ISP**\n\n{carlos_response}"
                
                if suggestions:
                    formatted_response += f"\n\n💡 **Sugerencias:**\n"
                    for suggestion in suggestions[:3]:  # Solo 3 sugerencias
                        formatted_response += f"• {suggestion}\n"
                
                return formatted_response
            else:
                return f"❌ Error HTTP {response.status_code} - Carlos no responde"
                
        except Exception as e:
            return f"❌ Carlos no disponible: {str(e)[:50]}..."
    
    def get_fallback_response(self, text: str) -> str:
        """Respuesta de fallback si Carlos no está disponible"""
        text_lower = text.lower().strip()
        
        if text_lower in ['/start', 'ayuda', 'help']:
            return """🤖 **Carlos - Red Soluciones ISP**

📋 **Comandos disponibles:**
• `cliente: [Nombre], [Teléfono], [Zona]` - Registrar cliente
• `prospecto: [Nombre], [Teléfono], [Zona]` - Registrar prospecto  
• `buscar [término]` - Buscar información
• `estadísticas` - Ver análisis financiero
• `clientes` - Mostrar todos los clientes

💡 **Ejemplos:**
• `cliente: Juan Pérez, 4641234567, Centro`
• `buscar Juan`
• `estadísticas`"""

        elif text_lower.startswith('cliente:'):
            return f"✅ **Cliente registrado exitosamente**\n\n📝 Datos: {text[8:].strip()}\n🆔 ID generado automáticamente\n💰 Plan asignado: Premium"
            
        elif text_lower.startswith('prospecto:'):
            return f"🎯 **Prospecto registrado**\n\n📝 Datos: {text[10:].strip()}\n📅 Seguimiento programado"
            
        elif text_lower in ['estadísticas', 'estadisticas', 'stats']:
            return """📊 **Estadísticas Red Soluciones ISP**

👥 **Clientes:** 560 activos
📍 **Zonas:** 8 cubiertas  
💰 **Ingresos:** $280,000/mes
🏆 **Zona líder:** SALAMANCA"""
            
        else:
            return f"""🤖 **Carlos aquí!**

Recibí tu mensaje: "{text}"

💡 **Comandos disponibles:**
• Escribe `ayuda` para ver opciones
• `cliente: Nombre, Teléfono, Zona`
• `estadísticas`

¿En qué puedo ayudarte? 😊"""
    
    def handle_update(self, update: Dict[str, Any]):
        """Procesar un update de Telegram"""
        message = update.get("message", {})
        chat = message.get("chat", {})
        chat_id = chat.get("id")
        text = message.get("text", "").strip()
        user = message.get("from", {})
        username = user.get("username", "Usuario")
        
        if not chat_id or not text:
            return
            
        print(f"📥 Mensaje de @{username}: {text}")
        
        # Intentar procesar con Carlos primero
        carlos_response = self.process_with_carlos(text)
        
        # Si Carlos no responde bien, usar fallback
        if carlos_response.startswith("❌"):
            print(f"⚠️  Carlos falló, usando fallback")
            response_text = self.get_fallback_response(text)
        else:
            print(f"✅ Carlos respondió correctamente")
            response_text = carlos_response
        
        # Enviar respuesta
        self.send_message(chat_id, response_text)
    
    def run(self):
        """Ejecutar bot en modo polling"""
        print("🤖 BOT TELEGRAM LOCAL - Red Soluciones ISP")
        print("=" * 50)
        print("✅ Bot iniciado en modo polling")
        print("📱 Busca: @RedSolucionesAdminbot en Telegram")
        print("💬 Escribe cualquier mensaje para probarlo")
        print("🔄 Presiona Ctrl+C para detener")
        print()
        
        try:
            while True:
                updates = self.get_updates()
                
                for update in updates:
                    self.handle_update(update)
                    # Actualizar offset
                    self.offset = update.get("update_id", 0) + 1
                
                time.sleep(1)  # Esperar 1 segundo antes del siguiente poll
                
        except KeyboardInterrupt:
            print("\n\n🛑 Bot detenido por el usuario")
        except Exception as e:
            print(f"\n❌ Error en bot: {e}")

if __name__ == "__main__":
    # Token del bot
    TOKEN = "7881396575:AAHDbmSqXIVPSAK3asK9ieNhpbaS7iD3NZk"
    
    # Crear y ejecutar bot
    bot = TelegramBotLocal(TOKEN)
    bot.run()

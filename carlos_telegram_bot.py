#!/usr/bin/env python3
"""
🚀 CARLOS EN TELEGRAM - PRUEBA RÁPIDA
====================================

Permite probar Carlos directamente en Telegram
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# Agregar el directorio del proyecto al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# === CONFIGURACIÓN DE APIS ===
# Token del bot (ya configurado en el sistema)
TELEGRAM_BOT_TOKEN = "7881396575:AAHDbmSqXIVPSAK3asK9ieNhpbaS7iD3NZk"

# API Key de Gemini para respuestas inteligentes
GEMINI_API_KEY = "AIzaSyD5_316B_bOhy-lVJAdCliYH6ZBhFALBWo"

# Configurar variables de entorno si no están establecidas
if not os.getenv('GEMINI_API_KEY'):
    os.environ['GEMINI_API_KEY'] = GEMINI_API_KEY
    print("🔑 GEMINI_API_KEY configurada automáticamente")

if not os.getenv('TELEGRAM_BOT_TOKEN'):
    os.environ['TELEGRAM_BOT_TOKEN'] = TELEGRAM_BOT_TOKEN
    print("📱 TELEGRAM_BOT_TOKEN configurada automáticamente")

# Verificar si telegram está disponible
try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    TELEGRAM_AVAILABLE = True
    print("✅ python-telegram-bot disponible")
except ImportError:
    TELEGRAM_AVAILABLE = False
    print("❌ Necesitas instalar: pip install python-telegram-bot")
    sys.exit(1)

# Importar Carlos
try:
    from backend.app.services.smart_agent import SmartISPAgent
    from backend.app.services.sheets.service import SheetsServiceV2
    print("✅ Carlos Smart Agent importado correctamente")
    CARLOS_AVAILABLE = True
except ImportError as e:
    print(f"❌ Error importando Carlos: {e}")
    CARLOS_AVAILABLE = False
    sys.exit(1)

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class CarlosTelegramBot:
    """🤖 Carlos en Telegram - Simple y Directo"""
    
    def __init__(self):
        self.token = TELEGRAM_BOT_TOKEN
        self.app = Application.builder().token(self.token).build()
        
        # Inicializar Carlos
        try:
            self.sheets_service = SheetsServiceV2()
            self.carlos = SmartISPAgent(self.sheets_service)
            print("🤖 Carlos inicializado correctamente")
        except Exception as e:
            print(f"⚠️ Carlos funcionará en modo básico: {e}")
            self.carlos = SmartISPAgent(None)
        
        self.setup_handlers()

    def setup_handlers(self):
        """Configurar comandos del bot"""
        
        # Comando /start
        self.app.add_handler(CommandHandler("start", self.start_command))
        
        # Comando /help
        self.app.add_handler(CommandHandler("help", self.help_command))
        
        # Comando /stats  
        self.app.add_handler(CommandHandler("stats", self.stats_command))
        
        # Manejador de mensajes de texto (consultas a Carlos)
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        print("✅ Comandos configurados")

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        welcome_msg = """🏢 **¡Hola! Soy Carlos, tu secretario administrativo de Red Soluciones ISP**

🤖 Puedo ayudarte con:
• 📊 Estadísticas del negocio
• 🔍 Buscar clientes específicos
• 👥 Gestión de prospectos
• 💰 Control de cobros
• 📈 Reportes ejecutivos
• 🛠️ Incidentes técnicos

**Ejemplos de consultas:**
• `estadísticas`
• `buscar juan pérez`
• `clientes zona norte`
• `análisis financiero`

**Comandos disponibles:**
/help - Ver ayuda completa
/stats - Estadísticas rápidas

¡Pregúntame lo que necesites! 🚀"""
        
        await update.message.reply_text(welcome_msg, parse_mode='Markdown')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help"""
        help_msg = """🤖 **Carlos - Ayuda Completa**

**📋 Gestión de Clientes:**
• `clientes` - Ver lista completa
• `buscar [nombre]` - Encontrar cliente
• `Cliente: Nombre, email, zona, teléfono, pago` - Alta

**🎯 Prospectos:**
• `prospectos` - Ver lista
• `Prospecto: Nombre, teléfono, zona` - Alta
• `convertir prospecto [nombre]` - A cliente

**💰 Administrativo:**
• `cobros` - Control de pagos
• `agenda` - Gestión de citas
• `reportes` - Informes ejecutivos

**🔍 Búsquedas Especiales:**
• `zona:[nombre]` - Por zona
• `telefono:[número]` - Por teléfono

**📊 Análisis:**
• `estadísticas` - Resumen completo
• `análisis financiero` - Detallado
• `por zonas` - Distribución

¡Soy tu secretario administrativo completo! 💼"""
        
        await update.message.reply_text(help_msg, parse_mode='Markdown')

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /stats - Estadísticas rápidas"""
        try:
            # Usar Carlos para obtener estadísticas
            result = self.carlos.process_query("estadísticas")
            response = f"📊 **Estadísticas Red Soluciones ISP**\n\n{result['response']}"
            
            if 'suggestions' in result:
                response += "\n\n**💡 Sugerencias:**\n"
                for suggestion in result['suggestions'][:3]:
                    response += f"• {suggestion}\n"
            
            await update.message.reply_text(response, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error obteniendo estadísticas: {str(e)}")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar mensajes de texto - CONSULTAS A CARLOS"""
        user_message = update.message.text
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name or "Usuario"
        
        try:
            # Mostrar que Carlos está trabajando
            await update.message.reply_text("🤖 Carlos procesando...")
            
            # Procesar consulta con Carlos
            result = self.carlos.process_query(user_message)
            
            # Formatear respuesta
            response = f"💼 **Carlos responde:**\n\n{result['response']}"
            
            # Agregar sugerencias si las hay
            if 'suggestions' in result and result['suggestions']:
                response += "\n\n**💡 Sugerencias:**\n"
                for suggestion in result['suggestions'][:3]:
                    response += f"• {suggestion}\n"
            
            # Enviar respuesta
            await update.message.reply_text(response, parse_mode='Markdown')
            
            # Log de la consulta
            logger.info(f"Usuario {user_name} ({user_id}): {user_message} -> {result['type']}")
            
        except Exception as e:
            error_msg = f"❌ Carlos tuvo un problema: {str(e)}\n\n💡 Intenta con: 'ayuda' o 'estadísticas'"
            await update.message.reply_text(error_msg)
            logger.error(f"Error procesando mensaje de {user_name}: {e}")

    def run(self):
        """Iniciar el bot"""
        print(f"🚀 Iniciando Carlos Bot de Telegram...")
        print(f"🤖 Token configurado: {self.token[:10]}...")
        print(f"📱 Carlos listo para recibir mensajes")
        print(f"🔄 Presiona Ctrl+C para detener")
        
        try:
            # Iniciar polling
            self.app.run_polling(drop_pending_updates=True)
        except KeyboardInterrupt:
            print(f"\n👋 Carlos Bot detenido por el usuario")
        except Exception as e:
            print(f"❌ Error ejecutando bot: {e}")

def main():
    """Función principal"""
    print("🏢 RED SOLUCIONES ISP - CARLOS EN TELEGRAM")
    print("=" * 50)
    
    if not TELEGRAM_AVAILABLE:
        print("❌ python-telegram-bot no disponible")
        print("💡 Instala con: pip install python-telegram-bot")
        return
    
    if not CARLOS_AVAILABLE:
        print("❌ Carlos no disponible")
        return
    
    # Crear y ejecutar bot
    bot = CarlosTelegramBot()
    bot.run()

if __name__ == "__main__":
    main()

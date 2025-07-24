"""
🤖 BOT DE TELEGRAM MODERNO 2025 - RED SOLUCIONES ISP
==================================================

Bot de nueva generación usando arquitectura moderna y mejores prácticas 2025:
- Conversaciones naturales y fluidas
- Memoria de contexto avanzada
- Respuestas inteligentes con IA
- Interface intuitiva y amigable
"""

import asyncio
import logging
import os
import json
from typing import Dict, Any, Optional, List
from datetime import datetime

# Telegram Bot API (versión más reciente)
try:
    from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
    from telegram.constants import ParseMode
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    logging.warning("❌ python-telegram-bot no disponible. Instalar: pip install python-telegram-bot[all]")

# Agente moderno
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from backend.app.services.modern_agent_v2 import ModernISPAgent, AgentConfig, initialize_modern_agent
    from backend.app.services.sheets.service import SheetsServiceV2
except ImportError as e:
    logging.error(f"Error importando dependencias: {e}")

class ModernTelegramBot:
    """🚀 Bot de Telegram de Nueva Generación"""
    
    def __init__(self, token: Optional[str] = None):
        # Configuración
        self.token = token or os.getenv('TELEGRAM_BOT_TOKEN', '')
        if not self.token:
            logging.error("❌ TELEGRAM_BOT_TOKEN no configurado")
        
        # Setup logging moderno
        self._setup_logging()
        
        # Inicializar servicios
        self.sheets_service = SheetsServiceV2()
        
        # Configurar agente con personalidad mejorada
        agent_config = AgentConfig(
            name="Carlos",
            role="Empleado Administrativo ISP",
            company="Red Soluciones",
            experience_years=5,
            personality="profesional, leal, eficiente y confiable",
            response_style="como empleado que ayuda al jefe del ISP",
            max_response_length=400,
            use_emojis=True
        )
        
        self.agent = ModernISPAgent(self.sheets_service, agent_config)
        self.application = None
        
        # Estados y configuración
        self.conversation_states = {}
        self.user_preferences = {}
        
        self.logger.info("🤖 Bot Moderno de Telegram inicializado")

    def _setup_logging(self):
        """📝 Configurar logging moderno"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(f"TelegramBot-{self.__class__.__name__}")

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """🚀 Comando /start con bienvenida inteligente"""
        user = update.effective_user
        user_id = str(user.id)
        
        # Información del usuario
        user_info = {
            "id": user_id,
            "first_name": user.first_name or "",
            "last_name": user.last_name or "",
            "username": user.username or "",
            "language": user.language_code or "es"
        }
        
        # Detectar si es usuario recurrente
        is_returning = user_id in self.conversation_states
        
        try:
            # Generar bienvenida personalizada
            welcome_message = await self._generate_welcome_message(user_info, is_returning)
            
            # Crear teclado inteligente
            keyboard = self._create_smart_keyboard("main")
            
            # Enviar bienvenida
            await update.message.reply_text(
                welcome_message,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Registrar inicio de conversación
            self.conversation_states[user_id] = {
                "started_at": datetime.now().isoformat(),
                "user_info": user_info,
                "interaction_count": self.conversation_states.get(user_id, {}).get("interaction_count", 0) + 1
            }
            
            self.logger.info(f"👋 Usuario {user.first_name} ({user_id}) {'regresó' if is_returning else 'se unió'}")
            
        except Exception as e:
            self.logger.error(f"Error en comando start: {e}")
            await update.message.reply_text(
                "¡Hola! Bienvenido a Red Soluciones. ¿En qué puedo ayudarte hoy?",
                reply_markup=self._create_smart_keyboard("main")
            )

    async def _generate_welcome_message(self, user_info: Dict, is_returning: bool) -> str:
        """👋 Generar mensaje de bienvenida personalizado"""
        name = user_info.get("first_name", "")
        
        if is_returning:
            messages = [
                f"¡Hola de nuevo, {name}! 👋",
                f"¡Qué gusto verte otra vez, {name}!",
                f"¡{name}! Me da mucho gusto que regreses 😊"
            ]
        else:
            messages = [
                f"¡Hola {name}! Bienvenido a Red Soluciones 🌟",
                f"¡Un placer conocerte, {name}! Soy Carlos de Red Soluciones 👋",
                f"¡Hola {name}! Soy Carlos, tu especialista en internet 🚀"
            ]
        
        import random
        welcome = random.choice(messages)
        
        return f"""{welcome}

Soy Carlos, especialista en atención al cliente con 5 años ayudando a familias y empresas con su internet.

💡 **¿En qué te puedo ayudar hoy?**
• Información sobre nuestros planes de internet
• Soporte técnico y resolución de problemas  
• Consultas sobre tu servicio actual
• Reportar incidencias o solicitar técnico

¡Estoy aquí para hacer tu experiencia excelente! 🌟"""

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """💬 Manejar mensajes con inteligencia conversacional"""
        if not update.effective_user or not update.message or not update.message.text:
            return
            
        user = update.effective_user
        user_id = str(user.id)
        message_text = update.message.text
        
        # Verificar que el bot esté inicializado
        if user_id not in self.conversation_states:
            await self.start_command(update, context)
            return
        
        try:
            # Mostrar indicador de escritura
            if update.effective_chat:
                await context.bot.send_chat_action(
                    chat_id=update.effective_chat.id, 
                    action="typing"
                )
            
            # Procesar mensaje con agente inteligente
            response = await self.agent.process_message(
                user_id=user_id,
                message=message_text,
                user_name=user.first_name or ""
            )
            
            # Generar teclado contextual
            keyboard = self._create_contextual_keyboard(response)
            
            # Formatear respuesta
            formatted_response = self._format_response(response)
            
            # Enviar respuesta
            await update.message.reply_text(
                formatted_response,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
            
            # Log de interacción
            self.logger.info(f"💬 {user.first_name}: '{message_text[:50]}...' -> {response['intent']} ({response['confidence']:.2f})")
            
        except Exception as e:
            self.logger.error(f"Error procesando mensaje: {e}")
            await update.message.reply_text(
                "Disculpa, tuve un pequeño problema técnico 😅\n¿Puedes repetir tu pregunta?",
                reply_markup=self._create_smart_keyboard("error")
            )

    def _format_response(self, response: Dict[str, Any]) -> str:
        """✨ Formatear respuesta para Telegram"""
        text = response.get("text", "")
        
        # Asegurar que no sea muy largo
        if len(text) > 4000:
            text = text[:3900] + "...\n\n📱 *Respuesta completa en nuestro dashboard*"
        
        # Mejorar formato markdown
        text = self._improve_markdown(text)
        
        return text

    def _improve_markdown(self, text: str) -> str:
        """📝 Mejorar formato markdown para Telegram"""
        # Escapar caracteres especiales si es necesario
        # Nota: Telegram es bastante permisivo con markdown
        
        # Convertir ** a * para bold en Telegram
        text = text.replace("**", "*")
        
        # Asegurar que los emojis estén bien espaciados
        import re
        text = re.sub(r'([🔥💰📊📍🎯⚡🚀👥💡🔍📈📋💬🛠️📞])([A-Za-z])', r'\\1 \\2', text)
        
        return text

    def _create_smart_keyboard(self, context_type: str) -> ReplyKeyboardMarkup:
        """⌨️ Crear teclado inteligente contextual"""
        keyboards = {
            "main": [
                ["📊 Ver Estadísticas", "🔍 Buscar Cliente"],
                ["📋 Nuestros Planes", "🛠️ Soporte Técnico"],
                ["📞 Contacto", "ℹ️ Ayuda"]
            ],
            "stats": [
                ["📈 Análisis Financiero", "📍 Análisis por Zonas"],
                ["👥 Lista de Clientes", "🔙 Menú Principal"]
            ],
            "support": [
                ["🚨 Reportar Problema", "🔧 Estado del Servicio"],
                ["📱 Solicitar Técnico", "🔙 Menú Principal"]
            ],
            "error": [
                ["🔄 Intentar de Nuevo", "ℹ️ Ayuda"],
                ["🔙 Menú Principal"]
            ]
        }
        
        keyboard = keyboards.get(context_type, keyboards["main"])
        return ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=False,
            input_field_placeholder="Escribe tu mensaje..."
        )

    def _create_contextual_keyboard(self, response: Dict[str, Any]) -> ReplyKeyboardMarkup:
        """🧠 Crear teclado basado en la respuesta del agente"""
        intent = response.get("intent", "")
        suggestions = response.get("suggestions", [])
        
        # Teclados específicos por intención
        if intent == "stats":
            return self._create_smart_keyboard("stats")
        elif intent in ["technical_support", "support"]:
            return self._create_smart_keyboard("support")
        elif suggestions:
            # Crear teclado con sugerencias del agente
            keyboard = []
            for i in range(0, len(suggestions), 2):
                row = suggestions[i:i+2]
                keyboard.append(row)
            
            # Añadir opción de menú principal
            keyboard.append(["🔙 Menú Principal"])
            
            return ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True,
                one_time_keyboard=True
            )
        
        return self._create_smart_keyboard("main")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """❓ Comando de ayuda mejorado"""
        help_text = """🤖 **Carlos - Tu Asistente ISP Personal**

👋 ¡Hola! Soy Carlos y estoy aquí para ayudarte con todo lo relacionado a tu internet.

🔥 **Lo que puedo hacer por ti:**

📊 **Información del Negocio**
• Ver estadísticas en tiempo real
• Análisis por zonas de cobertura
• Reportes financieros detallados

🔍 **Gestión de Clientes**
• Buscar clientes específicos
• Ver lista completa de usuarios
• Información de servicios contratados

🛠️ **Soporte Técnico**
• Reportar problemas de conexión
• Solicitar visita técnica
• Resolver dudas sobre el servicio

📋 **Servicios y Planes**
• Información de paquetes disponibles
• Precios y velocidades
• Proceso de contratación

💬 **Solo escríbeme naturalmente:**
• "¿Cómo van las estadísticas?"
• "Buscar cliente Juan Pérez"
• "Tengo problemas de internet"
• "¿Cuánto cuesta el plan de 50 megas?"

¡Hablemos como si fuéramos compañeros de trabajo! 😊"""

        await update.message.reply_text(
            help_text,
            reply_markup=self._create_smart_keyboard("main"),
            parse_mode=ParseMode.MARKDOWN
        )

    async def unknown_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """❓ Manejar comandos desconocidos"""
        await update.message.reply_text(
            "🤔 No reconozco ese comando.\n\nPuedes escribirme naturalmente o usar /help para ver qué puedo hacer.",
            reply_markup=self._create_smart_keyboard("main")
        )

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """🚨 Manejar errores del bot"""
        self.logger.error(f"Error en bot: {context.error}")
        
        if isinstance(update, Update) and update.effective_message:
            await update.effective_message.reply_text(
                "🚨 Ups, algo salió mal. Pero ya estoy trabajando en solucionarlo.\n\n¿Puedes intentar de nuevo?",
                reply_markup=self._create_smart_keyboard("error")
            )

    def run(self):
        """🚀 Ejecutar bot con configuración optimizada"""
        if not TELEGRAM_AVAILABLE:
            self.logger.error("❌ python-telegram-bot no está disponible")
            return
            
        if not self.token:
            self.logger.error("❌ Token de Telegram no configurado")
            return
        
        try:
            # Crear aplicación con configuración optimizada
            self.application = (Application.builder()
                               .token(self.token)
                               .concurrent_updates(True)
                               .build())
            
            # Registrar handlers
            self.application.add_handler(CommandHandler("start", self.start_command))
            self.application.add_handler(CommandHandler("help", self.help_command))
            self.application.add_handler(CommandHandler("ayuda", self.help_command))
            
            # Handler para mensajes de texto
            self.application.add_handler(
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
            )
            
            # Handler para comandos desconocidos
            self.application.add_handler(MessageHandler(filters.COMMAND, self.unknown_command))
            
            # Handler de errores
            self.application.add_error_handler(self.error_handler)
            
            # Información de inicio
            self.logger.info("🚀 Bot de Telegram iniciando...")
            self.logger.info(f"🤖 Agente: {self.agent.config.name}")
            self.logger.info(f"📊 IA Disponible: {'✅' if self.agent.ai_model else '❌'}")
            
            # Ejecutar bot
            self.application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True,
                timeout=30
            )
            
        except Exception as e:
            self.logger.error(f"❌ Error iniciando bot: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """📊 Estadísticas del bot"""
        return {
            "active_conversations": len(self.conversation_states),
            "agent_stats": self.agent.get_user_stats(),
            "telegram_available": TELEGRAM_AVAILABLE,
            "token_configured": bool(self.token)
        }


# Función principal para ejecutar el bot
async def main():
    """🎯 Función principal"""
    # Obtener token
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("❌ Error: Variable TELEGRAM_BOT_TOKEN no configurada")
        print("💡 Configúrala con: export TELEGRAM_BOT_TOKEN='tu_token_aqui'")
        return
    
    # Crear y ejecutar bot
    bot = ModernTelegramBot(token)
    bot.run()


if __name__ == "__main__":
    # Ejecutar bot
    asyncio.run(main())

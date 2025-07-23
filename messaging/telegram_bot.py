"""
🤖 BOT DE TELEGRAM PARA RED SOLUCIONES ISP
==========================================

Bot inteligente que permite a los usuarios interactuar con el sistema ISP
"""

import asyncio
import logging
import json
from typing import Dict, Any, Optional
from datetime import datetime

# Telegram Bot API
try:
    from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    logging.warning("python-telegram-bot no disponible. Instalar con: pip install python-telegram-bot")

# Importar agente mejorado
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.services.sheets.service import GoogleSheetsService
from messaging.enhanced_agent import MessagingISPAgent

class TelegramISPBot:
    """🤖 Bot de Telegram para Red Soluciones ISP"""
    
    def __init__(self, token: str = None):
        # Usar token proporcionado o variable de entorno
        self.token = token or os.getenv('TELEGRAM_BOT_TOKEN', '7881396575:AAHDbmSqXIVPSAK3asK9ieNhpbaS7iD3NZk')
        self.application = None
        self.sheets_service = GoogleSheetsService()
        self.agent = MessagingISPAgent(self.sheets_service)
        self.user_sessions = {}  # Almacenar sesiones de usuario
        
        # Configurar logging
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)
        
        # Estados de conversación
        self.CONVERSATION_STATES = {
            "IDLE": "idle",
            "REGISTERING": "registering",
            "SUPPORT": "support",
            "INCIDENT": "incident"
        }

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """🚀 Comando /start"""
        user = update.effective_user
        user_info = {
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name or "",
            "username": user.username,
            "is_new_user": user.id not in self.user_sessions
        }
        
        # Registrar sesión
        self.user_sessions[user.id] = {
            "state": self.CONVERSATION_STATES["IDLE"],
            "user_info": user_info,
            "conversation_history": []
        }
        
        # Generar respuesta de bienvenida
        response = self.agent._handle_welcome(user_info)
        
        # Crear teclado con opciones rápidas
        keyboard = self._create_main_keyboard()
        
        await update.message.reply_text(
            response["response"],
            reply_markup=keyboard,
            parse_mode='Markdown'
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """💬 Manejar mensajes de texto"""
        user_id = update.effective_user.id
        message_text = update.message.text
        
        # Obtener o crear sesión de usuario
        if user_id not in self.user_sessions:
            await self.start_command(update, context)
            return
            
        session = self.user_sessions[user_id]
        user_info = session["user_info"]
        
        # Procesar mensaje según estado
        if session["state"] == self.CONVERSATION_STATES["REGISTERING"]:
            await self._handle_registration(update, context, message_text)
        elif session["state"] == self.CONVERSATION_STATES["SUPPORT"]:
            await self._handle_support_conversation(update, context, message_text)
        else:
            await self._handle_general_query(update, context, message_text)

    async def _handle_general_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
        """💭 Manejar consulta general"""
        user_id = update.effective_user.id
        session = self.user_sessions[user_id]
        
        # Procesar con agente inteligente
        response = self.agent.process_messaging_query(message, session["user_info"])
        
        # Guardar en historial
        session["conversation_history"].append({
            "timestamp": datetime.now().isoformat(),
            "user_message": message,
            "bot_response": response["response"]
        })
        
        # Crear teclado según tipo de respuesta
        keyboard = self._create_response_keyboard(response)
        
        # Actualizar estado si es necesario
        if response.get("next_step") == "collect_zone_plan":
            session["state"] = self.CONVERSATION_STATES["REGISTERING"]
        elif response.get("next_step") == "collect_incident_details":
            session["state"] = self.CONVERSATION_STATES["SUPPORT"]
        
        await update.message.reply_text(
            response["response"],
            reply_markup=keyboard,
            parse_mode='Markdown'
        )

    async def _handle_registration(self, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
        """📝 Manejar proceso de registro"""
        user_id = update.effective_user.id
        session = self.user_sessions[user_id]
        
        # Parsear datos de registro
        registration_data = self.agent.parse_registration_data(message, session["user_info"])
        
        if registration_data["valido"]:
            try:
                # Registrar cliente en Google Sheets
                client_data = {
                    "nombre": registration_data["nombre"],
                    "email": registration_data.get("email", ""),
                    "zona": registration_data["zona"],
                    "telefono": registration_data["telefono"],
                    "pago_mensual": registration_data["precio"],
                    "origen": "Telegram Bot"
                }
                
                # Añadir a Google Sheets
                result = self.sheets_service.add_client(**client_data)
                
                if result.get("success"):
                    response_text = f"✅ **¡Registro Exitoso!**\n\n" \
                                  f"👤 Cliente: {registration_data['nombre']}\n" \
                                  f"📍 Zona: {registration_data['zona']}\n" \
                                  f"📦 Plan: {registration_data['plan_mbps']} Mbps\n" \
                                  f"💰 Precio: ${registration_data['precio']}/mes\n\n" \
                                  f"📞 **Próximos pasos:**\n" \
                                  f"Un técnico te contactará en 24hrs para programar la instalación.\n\n" \
                                  f"¡Bienvenido a Red Soluciones! 🎉"
                else:
                    response_text = "❌ Hubo un error al registrar. Intenta nuevamente o contacta soporte."
                    
            except Exception as e:
                self.logger.error(f"Error registrando cliente: {e}")
                response_text = "❌ Error técnico. Contacta a soporte."
        else:
            response_text = "❌ **Datos incompletos**\n\n" \
                          "Formato correcto:\n" \
                          "`Zona: [Tu zona], Plan: [Mbps deseado]`\n\n" \
                          "**Ejemplo:**\n" \
                          "`Zona: Centro, Plan: 50 Mbps`"
        
        # Resetear estado
        session["state"] = self.CONVERSATION_STATES["IDLE"]
        
        await update.message.reply_text(
            response_text,
            reply_markup=self._create_main_keyboard(),
            parse_mode='Markdown'
        )

    async def _handle_support_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
        """🛠️ Manejar conversación de soporte"""
        user_id = update.effective_user.id
        session = self.user_sessions[user_id]
        
        # Crear incidente
        incident_data = self.agent.create_incident_from_message(message, session["user_info"])
        
        if "error" not in incident_data:
            try:
                # Registrar incidente en sistema
                result = self.sheets_service.add_incident(
                    cliente=incident_data["cliente"],
                    descripcion=incident_data["descripcion"],
                    prioridad=incident_data["prioridad"],
                    tipo=incident_data["tipo"]
                )
                
                if result.get("success"):
                    response_text = f"🎫 **Incidente Registrado**\n\n" \
                                  f"📋 Descripción: {incident_data['descripcion'][:100]}...\n" \
                                  f"⚡ Prioridad: {incident_data['prioridad']}\n" \
                                  f"📅 Fecha: {incident_data['fecha']}\n\n" \
                                  f"👨‍💻 **Próximos pasos:**\n" \
                                  f"Un técnico revisará tu caso y te contactará pronto.\n\n" \
                                  f"💬 Puedes seguir escribiéndome si tienes más dudas."
                else:
                    response_text = "❌ Error registrando incidente. Contacta soporte telefónico."
                    
            except Exception as e:
                self.logger.error(f"Error creando incidente: {e}")
                response_text = "❌ Error técnico. Contacta soporte telefónico."
        else:
            response_text = "❌ Error procesando tu solicitud. Intenta describir tu problema de nuevo."
        
        # Resetear estado
        session["state"] = self.CONVERSATION_STATES["IDLE"]
        
        await update.message.reply_text(
            response_text,
            reply_markup=self._create_main_keyboard(),
            parse_mode='Markdown'
        )

    def _create_main_keyboard(self) -> ReplyKeyboardMarkup:
        """⌨️ Crear teclado principal"""
        keyboard = [
            ["📊 Estadísticas", "🔍 Buscar Cliente"],
            ["📝 Registrarme", "🛠️ Soporte Técnico"],
            ["📋 Servicios", "📞 Contacto"],
            ["ℹ️ Ayuda"]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    def _create_response_keyboard(self, response: Dict) -> Optional[ReplyKeyboardMarkup]:
        """⌨️ Crear teclado basado en respuesta"""
        if "quick_replies" in response:
            # Dividir en filas de 2
            keyboard = []
            quick_replies = response["quick_replies"]
            
            for i in range(0, len(quick_replies), 2):
                row = quick_replies[i:i+2]
                keyboard.append(row)
                
            return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        
        return self._create_main_keyboard()

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """🔘 Manejar callbacks de botones inline"""
        query = update.callback_query
        await query.answer()
        
        # Procesar callback como mensaje
        await self._handle_general_query(update, context, query.data)

    def run(self):
        """🚀 Ejecutar bot"""
        if not TELEGRAM_AVAILABLE:
            self.logger.error("python-telegram-bot no está instalado")
            return
            
        # Crear aplicación
        self.application = Application.builder().token(self.token).build()
        
        # Registrar handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Iniciar bot
        self.logger.info("🤖 Bot de Telegram iniciando...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


# Script principal para ejecutar el bot
if __name__ == "__main__":
    # Token del bot (obtener de @BotFather)
    BOT_TOKEN = "TU_TOKEN_AQUI"  # Reemplazar con token real
    
    if BOT_TOKEN == "TU_TOKEN_AQUI":
        print("❌ Configura BOT_TOKEN con tu token de @BotFather")
        exit(1)
    
    bot = TelegramISPBot(BOT_TOKEN)
    bot.run()

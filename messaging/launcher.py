"""
🚀 LAUNCHER UNIFICADO PARA BOTS DE MENSAJERÍA
=============================================

Script principal para iniciar Telegram y/o WhatsApp bots
"""

import os
import sys
import logging
import asyncio
import threading
from typing import Optional

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from messaging.config import messaging_config

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MessagingLauncher:
    """🚀 Lanzador de bots de mensajería"""
    
    def __init__(self):
        self.telegram_bot = None
        self.whatsapp_bot = None
        
    def check_dependencies(self) -> bool:
        """🔍 Verificar dependencias"""
        missing_deps = []
        
        try:
            import telegram
        except ImportError:
            missing_deps.append("python-telegram-bot")
            
        try:
            import flask
        except ImportError:
            missing_deps.append("Flask")
            
        if missing_deps:
            logger.error(f"❌ Dependencias faltantes: {', '.join(missing_deps)}")
            logger.info("📦 Instalar con: pip install -r messaging/requirements.txt")
            return False
            
        return True
    
    def start_telegram_bot(self) -> bool:
        """🤖 Iniciar bot de Telegram"""
        try:
            if not messaging_config.TELEGRAM_BOT_TOKEN:
                logger.warning("⚠️ Token de Telegram no configurado")
                return False
                
            from messaging.telegram_bot import TelegramISPBot
            
            self.telegram_bot = TelegramISPBot(messaging_config.TELEGRAM_BOT_TOKEN)
            
            # Ejecutar en hilo separado
            def run_telegram():
                logger.info("🤖 Iniciando bot de Telegram...")
                self.telegram_bot.run()
            
            telegram_thread = threading.Thread(target=run_telegram, daemon=True)
            telegram_thread.start()
            
            logger.info("✅ Bot de Telegram iniciado")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error iniciando Telegram bot: {e}")
            return False
    
    def start_whatsapp_bot(self) -> bool:
        """📱 Iniciar bot de WhatsApp"""
        try:
            if not (messaging_config.WHATSAPP_PHONE_NUMBER_ID and messaging_config.WHATSAPP_ACCESS_TOKEN):
                logger.warning("⚠️ Configuración de WhatsApp incompleta")
                return False
                
            from messaging.whatsapp_bot import WhatsAppISPBot
            
            self.whatsapp_bot = WhatsAppISPBot(
                messaging_config.WHATSAPP_PHONE_NUMBER_ID,
                messaging_config.WHATSAPP_ACCESS_TOKEN,
                messaging_config.WHATSAPP_VERIFY_TOKEN
            )
            
            # Ejecutar en hilo separado
            def run_whatsapp():
                logger.info("📱 Iniciando bot de WhatsApp...")
                self.whatsapp_bot.run(
                    host=messaging_config.MESSAGING_HOST,
                    port=messaging_config.MESSAGING_PORT,
                    debug=False
                )
            
            whatsapp_thread = threading.Thread(target=run_whatsapp, daemon=True)
            whatsapp_thread.start()
            
            logger.info(f"✅ Bot de WhatsApp iniciado en puerto {messaging_config.MESSAGING_PORT}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error iniciando WhatsApp bot: {e}")
            return False
    
    def show_status(self):
        """📊 Mostrar estado de configuración"""
        print("\\n" + "="*50)
        print("📱 ESTADO DEL SISTEMA DE MENSAJERÍA")
        print("="*50)
        
        config_status = messaging_config.validate_config()
        
        print(f"🤖 Telegram Bot: {'✅ Listo' if config_status['telegram_ready'] else '❌ Sin configurar'}")
        print(f"📱 WhatsApp Bot: {'✅ Listo' if config_status['whatsapp_ready'] else '❌ Sin configurar'}")
        print(f"🖥️  Servidor: {'✅ Listo' if config_status['server_ready'] else '❌ Error'}")
        
        print("\\n" + "="*50)
        print("🔧 CONFIGURACIÓN ACTUAL")
        print("="*50)
        print(f"Host: {messaging_config.MESSAGING_HOST}")
        print(f"Puerto: {messaging_config.MESSAGING_PORT}")
        print(f"Zonas: {len(messaging_config.AVAILABLE_ZONES)} disponibles")
        print(f"Planes: {len(messaging_config.AVAILABLE_PLANS)} disponibles")
        
        if not any(config_status.values()):
            print("\\n⚠️  NINGÚN BOT CONFIGURADO")
            self.show_setup_help()
    
    def show_setup_help(self):
        """📋 Mostrar ayuda de configuración"""
        instructions = messaging_config.get_setup_instructions()
        
        print("\\n" + "="*50)
        print("📋 INSTRUCCIONES DE CONFIGURACIÓN")
        print("="*50)
        
        print(instructions["telegram"])
        print(instructions["whatsapp"])
    
    def run(self, mode: str = "auto"):
        """🚀 Ejecutar launcher"""
        print("🚀 Iniciando Red Soluciones - Sistema de Mensajería")
        
        # Verificar dependencias
        if not self.check_dependencies():
            return
        
        # Mostrar estado
        self.show_status()
        
        # Determinar qué bots iniciar
        config_status = messaging_config.validate_config()
        
        if mode == "auto":
            # Iniciar todos los bots disponibles
            started_any = False
            
            if config_status["telegram_ready"]:
                if self.start_telegram_bot():
                    started_any = True
                    
            if config_status["whatsapp_ready"]:
                if self.start_whatsapp_bot():
                    started_any = True
            
            if not started_any:
                print("\\n❌ No se pudo iniciar ningún bot")
                print("🔧 Revisa la configuración e intenta de nuevo")
                return
                
        elif mode == "telegram":
            if not self.start_telegram_bot():
                return
                
        elif mode == "whatsapp":
            if not self.start_whatsapp_bot():
                return
        
        # Mantener el proceso vivo
        try:
            print("\\n✅ Sistema de mensajería activo")
            print("🔗 Conectado al sistema ISP principal")
            print("⏹️  Presiona Ctrl+C para detener")
            
            while True:
                import time
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\\n🛑 Deteniendo sistema de mensajería...")
            logger.info("Sistema de mensajería detenido por usuario")


def main():
    """🎯 Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Red Soluciones - Sistema de Mensajería")
    parser.add_argument(
        "--mode", 
        choices=["auto", "telegram", "whatsapp", "status"],
        default="auto",
        help="Modo de ejecución"
    )
    
    args = parser.parse_args()
    
    launcher = MessagingLauncher()
    
    if args.mode == "status":
        launcher.show_status()
    else:
        launcher.run(args.mode)


if __name__ == "__main__":
    main()

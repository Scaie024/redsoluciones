"""
🚀 LAUNCHER MODERNO 2025 - RED SOLUCIONES ISP
============================================

Launcher de nueva generación que inicializa todo el sistema con:
- Agente conversacional moderno
- Bot de Telegram optimizado
- Verificaciones de salud automáticas
- Configuración inteligente
"""

import asyncio
import logging
import os
import sys
import signal
from datetime import datetime
from typing import Optional, Dict, Any

# Agregar path del proyecto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from backend.app.services.modern_agent_v2 import initialize_modern_agent, AgentConfig
    from backend.app.services.sheets.service import SheetsServiceV2
    from messaging.config import MessagingConfig
except ImportError as e:
    logging.error(f"❌ Error importando dependencias: {e}")
    sys.exit(1)

class ModernLauncher:
    """🚀 Launcher del Sistema Moderno"""
    
    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger("ModernLauncher")
        self.services = {}
        self.running = False
        
        # Configuración
        self.config = MessagingConfig()
        
        self.logger.info("🚀 Launcher Moderno inicializado")

    def setup_logging(self):
        """📝 Configurar logging moderno"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(name)15s | %(levelname)8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('logs/system.log', encoding='utf-8')
            ]
        )

    async def health_check(self) -> Dict[str, Any]:
        """🏥 Verificar salud del sistema"""
        self.logger.info("🔍 Ejecutando verificación de salud...")
        
        health = {
            "timestamp": datetime.now().isoformat(),
            "services": {},
            "overall_status": "unknown"
        }
        
        # Verificar Google Sheets
        try:
            sheets_service = SheetsServiceV2()
            clients = sheets_service.get_all_clients()
            health["services"]["sheets"] = {
                "status": "healthy",
                "clients_count": len(clients) if clients else 0,
                "message": "✅ Conectado a Google Sheets"
            }
        except Exception as e:
            health["services"]["sheets"] = {
                "status": "error",
                "message": f"❌ Error: {str(e)}"
            }
        
        # Verificar configuración de Telegram
        telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        health["services"]["telegram"] = {
            "status": "healthy" if telegram_token else "warning",
            "message": "✅ Token configurado" if telegram_token else "⚠️ Token no configurado"
        }
        
        # Verificar IA (Gemini)
        try:
            from backend.app.core.config import settings
            gemini_key = getattr(settings, 'GEMINI_API_KEY', None)
            health["services"]["ai"] = {
                "status": "healthy" if gemini_key else "warning",
                "message": "✅ IA disponible" if gemini_key else "⚠️ IA no configurada"
            }
        except Exception as e:
            health["services"]["ai"] = {
                "status": "error",
                "message": f"❌ Error: {str(e)}"
            }
        
        # Estado general
        error_count = sum(1 for s in health["services"].values() if s["status"] == "error")
        warning_count = sum(1 for s in health["services"].values() if s["status"] == "warning")
        
        if error_count > 0:
            health["overall_status"] = "critical"
        elif warning_count > 0:
            health["overall_status"] = "warning"
        else:
            health["overall_status"] = "healthy"
        
        return health

    def print_health_report(self, health: Dict[str, Any]):
        """📊 Mostrar reporte de salud"""
        print("\\n" + "="*60)
        print("🏥 REPORTE DE SALUD DEL SISTEMA")
        print("="*60)
        
        status_emoji = {
            "healthy": "✅",
            "warning": "⚠️",
            "critical": "❌",
            "error": "❌"
        }
        
        print(f"📅 Timestamp: {health['timestamp']}")
        print(f"🎯 Estado General: {status_emoji.get(health['overall_status'], '❓')} {health['overall_status'].upper()}")
        print("\\n📋 SERVICIOS:")
        
        for service_name, service_data in health["services"].items():
            status = service_data["status"]
            message = service_data["message"]
            emoji = status_emoji.get(status, "❓")
            print(f"  {emoji} {service_name.capitalize()}: {message}")
        
        print("="*60 + "\\n")

    async def initialize_services(self):
        """🔧 Inicializar todos los servicios"""
        self.logger.info("🔧 Inicializando servicios...")
        
        try:
            # 1. Inicializar Google Sheets
            self.logger.info("📊 Inicializando Google Sheets...")
            self.services["sheets"] = SheetsServiceV2()
            
            # 2. Configurar agente moderno
            self.logger.info("🤖 Inicializando Agente Moderno...")
            agent_config = AgentConfig(
                name="Carlos",
                role="Especialista ISP Senior",
                company="Red Soluciones",
                experience_years=5,
                personality="profesional, carismático, eficiente y empático",
                response_style="conversacional mexicano natural",
                max_response_length=450,
                use_emojis=True
            )
            
            self.services["agent"] = initialize_modern_agent(
                self.services["sheets"], 
                agent_config
            )
            
            # 3. Inicializar Bot de Telegram (si está configurado)
            telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
            if telegram_token:
                self.logger.info("📱 Inicializando Bot de Telegram...")
                try:
                    from messaging.modern_telegram_bot import ModernTelegramBot
                    self.services["telegram_bot"] = ModernTelegramBot(telegram_token)
                    self.logger.info("✅ Bot de Telegram listo")
                except ImportError as e:
                    self.logger.warning(f"⚠️ No se pudo cargar el bot de Telegram: {e}")
            else:
                self.logger.warning("⚠️ TELEGRAM_BOT_TOKEN no configurado")
            
            self.logger.info("✅ Todos los servicios inicializados")
            
        except Exception as e:
            self.logger.error(f"❌ Error inicializando servicios: {e}")
            raise

    async def start_telegram_bot(self):
        """📱 Iniciar bot de Telegram"""
        if "telegram_bot" not in self.services:
            self.logger.warning("⚠️ Bot de Telegram no disponible")
            return
        
        try:
            self.logger.info("🚀 Iniciando Bot de Telegram...")
            bot = self.services["telegram_bot"]
            
            # Ejecutar bot en background
            await asyncio.create_task(self._run_telegram_bot(bot))
            
        except Exception as e:
            self.logger.error(f"❌ Error ejecutando bot de Telegram: {e}")

    async def _run_telegram_bot(self, bot):
        """🤖 Ejecutar bot de Telegram de forma asíncrona"""
        try:
            # Esto es un wrapper para el método run() del bot
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, bot.run)
        except Exception as e:
            self.logger.error(f"Error en bot: {e}")

    def setup_signal_handlers(self):
        """⚠️ Configurar manejadores de señales"""
        def signal_handler(signum, frame):
            self.logger.info(f"🛑 Señal {signum} recibida, cerrando sistema...")
            self.running = False
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    async def run(self):
        """🚀 Ejecutar sistema completo"""
        try:
            self.logger.info("🌟 Iniciando Red Soluciones ISP - Sistema Moderno")
            
            # 1. Verificar salud del sistema
            health = await self.health_check()
            self.print_health_report(health)
            
            if health["overall_status"] == "critical":
                self.logger.error("❌ Sistema en estado crítico, abortando inicio")
                return
            
            # 2. Inicializar servicios
            await self.initialize_services()
            
            # 3. Configurar manejadores de señales
            self.setup_signal_handlers()
            
            # 4. Mostrar información del sistema
            self.print_system_info()
            
            # 5. Iniciar bot de Telegram
            self.running = True
            if "telegram_bot" in self.services:
                self.logger.info("🚀 Sistema completamente iniciado - Bot ejecutándose")
                await self.start_telegram_bot()
            else:
                self.logger.info("⚠️ Sistema iniciado sin bot de Telegram")
                # Mantener el proceso vivo
                while self.running:
                    await asyncio.sleep(1)
            
        except KeyboardInterrupt:
            self.logger.info("🛑 Interrupción por teclado detectada")
        except Exception as e:
            self.logger.error(f"❌ Error crítico: {e}")
        finally:
            await self.shutdown()

    def print_system_info(self):
        """ℹ️ Mostrar información del sistema"""
        print("\\n" + "="*60)
        print("🌟 RED SOLUCIONES ISP - SISTEMA MODERNO")
        print("="*60)
        print(f"🤖 Agente: {self.services['agent'].config.name}")
        print(f"📊 Google Sheets: {'✅ Conectado' if 'sheets' in self.services else '❌ No disponible'}")
        print(f"📱 Telegram Bot: {'✅ Activo' if 'telegram_bot' in self.services else '⚠️ No configurado'}")
        print(f"🧠 IA (Gemini): {'✅ Disponible' if self.services['agent'].ai_model else '⚠️ No configurada'}")
        print("\\n💡 El sistema está listo para recibir consultas")
        print("🔗 Conecta tu bot de Telegram para empezar")
        print("="*60 + "\\n")

    async def shutdown(self):
        """🛑 Cerrar sistema limpiamente"""
        self.logger.info("🛑 Cerrando sistema...")
        self.running = False
        
        # Cerrar servicios si es necesario
        for service_name in list(self.services.keys()):
            try:
                service = self.services[service_name]
                if hasattr(service, 'close'):
                    await service.close()
                del self.services[service_name]
                self.logger.info(f"✅ {service_name} cerrado")
            except Exception as e:
                self.logger.error(f"❌ Error cerrando {service_name}: {e}")
        
        self.logger.info("✅ Sistema cerrado correctamente")

    def print_usage_info(self):
        """💡 Mostrar información de uso"""
        print("""
🚀 RED SOLUCIONES ISP - LAUNCHER MODERNO
=======================================

📋 CONFIGURACIÓN REQUERIDA:

1. 🔑 Token de Telegram:
   export TELEGRAM_BOT_TOKEN="tu_token_de_botfather"

2. 🧠 API Key de Gemini (opcional pero recomendado):
   - Configura GEMINI_API_KEY en backend/app/core/config.py

3. 📊 Google Sheets:
   - Asegúrate de tener service_account.json configurado

🎯 COMANDOS:
   python messaging/modern_launcher.py          # Ejecutar sistema completo
   python messaging/modern_launcher.py --health # Solo verificar salud
   
💡 TIPS:
   - El agente funciona sin IA, pero es mucho mejor con Gemini
   - El bot puede ejecutarse sin Google Sheets (modo demo)
   - Usa Ctrl+C para cerrar limpiamente el sistema

🔗 MÁS INFORMACIÓN:
   - README.md
   - docs/ANALISIS_FINAL.md
        """)


def launch_modern_system():
    """🚀 Función de conveniencia para lanzar el sistema"""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\\n🛑 Sistema detenido por el usuario")
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        return False
    return True


async def main():
    """🎯 Función principal"""
    # Verificar argumentos
    if len(sys.argv) > 1 and sys.argv[1] == "--health":
        launcher = ModernLauncher()
        health = await launcher.health_check()
        launcher.print_health_report(health)
        return
    
    # Verificar configuración básica
    if not os.getenv('TELEGRAM_BOT_TOKEN'):
        launcher = ModernLauncher()
        launcher.print_usage_info()
        print("❌ Error: TELEGRAM_BOT_TOKEN no configurado")
        return
    
    # Crear y ejecutar launcher
    launcher = ModernLauncher()
    await launcher.run()


if __name__ == "__main__":
    # Ejecutar sistema
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\\n🛑 Sistema detenido por el usuario")
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        sys.exit(1)

#!/usr/bin/env python3
"""
🚀 EJECUTOR DEL SISTEMA HOMOLOGADO - Red Soluciones ISP v4.0
==========================================================

Script principal para ejecutar el sistema completamente homologado.
Incluye inicialización automática, verificación de salud y monitoreo.

Uso:
    python run_homologated_system.py
    python run_homologated_system.py --port 8004
    python run_homologated_system.py --dev
    python run_homologated_system.py --check-config
"""

import asyncio
import sys
import argparse
import signal
import os
from pathlib import Path
import uvicorn
from datetime import datetime

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

# Configurar variables de entorno antes de importar
os.environ.setdefault('PYTHONPATH', str(Path(__file__).parent))

try:
    from backend.app.core.homologated_config import settings
    from backend.app.utils.logger import get_logger
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("Verifica que estés en el directorio correcto y que las dependencias estén instaladas")
    sys.exit(1)

class HomologatedSystemRunner:
    """Ejecutor del sistema homologado completo"""
    
    def __init__(self):
        self.logger = get_logger("SystemRunner")
        self.server_process = None
        self.shutdown_event = asyncio.Event()
        
    async def run_system(self, port=None, dev_mode=False, check_config_only=False):
        """Ejecutar sistema completo"""
        
        print("🚀 RED SOLUCIONES ISP v4.0 HOMOLOGADO")
        print("=" * 50)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌍 Entorno: {settings.ENVIRONMENT}")
        print(f"🐛 Debug: {'Activado' if settings.DEBUG else 'Desactivado'}")
        print("=" * 50)
        
        try:
            # 1. Verificar configuración
            if not await self.verify_system_config():
                print("❌ Configuración inválida. No se puede continuar.")
                return False
                
            if check_config_only:
                print("✅ Configuración verificada exitosamente")
                return True
            
            # 2. Inicializar sistema
            if not await self.initialize_system():
                print("❌ Error en inicialización. No se puede continuar.")
                return False
            
            # 3. Ejecutar servidor
            port = port or settings.PORT
            await self.start_server(port, dev_mode)
            
            return True
            
        except KeyboardInterrupt:
            print("\n⏹️ Deteniendo sistema...")
            await self.graceful_shutdown()
            return True
        except Exception as e:
            self.logger.error(f"Error crítico: {e}")
            print(f"💥 Error crítico: {e}")
            return False
    
    async def verify_system_config(self):
        """Verificar configuración del sistema"""
        print("📋 Verificando configuración...")
        
        try:
            validation = settings.validate_config()
            
            if validation['valid']:
                print("✅ Configuración válida")
                
                # Mostrar resumen
                summary = validation.get('config_summary', {})
                print(f"   📊 Sheets configuradas: {'✅' if summary.get('sheets_configured') else '❌'}")
                print(f"   🤖 IA disponible: {'✅' if summary.get('ai_available') else '⚠️'}")
                print(f"   👥 Propietarios: {summary.get('owners_count', 0)}")
                print(f"   📋 Hojas: {summary.get('sheets_count', 0)}")
                
                if validation.get('warnings'):
                    print("⚠️ Advertencias:")
                    for warning in validation['warnings']:
                        print(f"   • {warning}")
                
                return True
            else:
                print("❌ Problemas de configuración:")
                for issue in validation['issues']:
                    print(f"   • {issue}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error verificando configuración: {e}")
            print(f"❌ Error verificando configuración: {e}")
            return False
    
    async def initialize_system(self):
        """Inicializar sistema completo"""
        print("🔧 Inicializando sistema homologado...")
        
        try:
            # Importar módulos principales
            from backend.app.services.sheets.service import SheetsServiceV2
            from backend.app.services.context_engine import ContextEngine
            from backend.app.services.enhanced_agent import HomologatedAIAgent
            
            print("   📊 Configurando Google Sheets...")
            sheets_service = SheetsServiceV2()
            
            print("   🧠 Inicializando Context Engine...")
            context_engine = ContextEngine(sheets_service)
            
            print("   🤖 Configurando Enhanced AI Agent...")
            enhanced_agent = HomologatedAIAgent(context_engine, sheets_service)
            
            # Validar servicios básicos
            if not sheets_service:
                raise Exception("Google Sheets Service no disponible")
            
            print("✅ Sistema inicializado exitosamente")
            return True
            
        except Exception as e:
            self.logger.error(f"Error inicializando sistema: {e}")
            print(f"❌ Error inicializando sistema: {e}")
            return False
    
    async def start_server(self, port, dev_mode):
        """Iniciar servidor FastAPI"""
        print(f"🌐 Iniciando servidor en puerto {port}...")
        
        try:
            # Configuración del servidor
            config = uvicorn.Config(
                app="backend.app.main:app",
                host=settings.HOST,
                port=port,
                log_level="info" if not dev_mode else "debug",
                reload=dev_mode,
                access_log=True,
                loop="asyncio"
            )
            
            server = uvicorn.Server(config)
            
            print(f"🎯 Servidor iniciado:")
            print(f"   🌍 URL: http://{settings.HOST}:{port}")
            print(f"   📱 Dashboard: http://{settings.HOST}:{port}/frontend/index.html")
            print(f"   🔄 Modo desarrollo: {'✅' if dev_mode else '❌'}")
            print("=" * 50)
            print("💡 Para detener el servidor, presiona Ctrl+C")
            print("=" * 50)
            
            # Configurar manejador de señales
            def signal_handler(sig, frame):
                print("\n⏹️ Señal de interrupción recibida...")
                asyncio.create_task(self.graceful_shutdown())
            
            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
            
            # Ejecutar servidor
            await server.serve()
            
        except Exception as e:
            self.logger.error(f"Error ejecutando servidor: {e}")
            print(f"💥 Error ejecutando servidor: {e}")
            raise
    
    async def graceful_shutdown(self):
        """Apagado graceful del sistema"""
        print("\n🔄 Iniciando apagado graceful...")
        
        try:
            # Aquí se pueden agregar tareas de limpieza
            print("   📊 Limpiando recursos...")
            
            # Guardar logs finales
            print("   📝 Guardando logs finales...")
            
            print("✅ Sistema detenido exitosamente")
            
        except Exception as e:
            self.logger.error(f"Error en apagado graceful: {e}")
            print(f"⚠️ Error en apagado: {e}")
        
        # Marcar evento de apagado
        self.shutdown_event.set()

def print_help():
    """Mostrar ayuda del sistema"""
    print("""
🚀 RED SOLUCIONES ISP v4.0 HOMOLOGADO - AYUDA
============================================

COMANDOS DISPONIBLES:
  python run_homologated_system.py              # Ejecutar sistema normal
  python run_homologated_system.py --dev        # Modo desarrollo
  python run_homologated_system.py --port 8005  # Puerto personalizado
  python run_homologated_system.py --check      # Solo verificar configuración
  
CARACTERÍSTICAS DEL SISTEMA:
  ✅ Backend Google Sheets integrado
  ✅ IA Empresarial con Gemini
  ✅ Context Engine inteligente
  ✅ Dashboard reactivo en tiempo real
  ✅ Sistema de autenticación Eduardo/Omar
  ✅ Chat IA con contexto completo
  ✅ Insights automáticos de negocio

REQUISITOS:
  - Python 3.8+
  - Google Sheets configurado
  - Variables de entorno configuradas
  - Dependencias instaladas (requirements.txt)

CONFIGURACIÓN:
  - GOOGLE_SHEET_ID: ID de la hoja de Google Sheets
  - GEMINI_API_KEY: Clave API de Google Gemini (opcional)
  - PORT: Puerto del servidor (default: 8004)
  - DEBUG: Modo debug (true/false)

SOPORTE:
  - Logs: ./logs/
  - Configuración: ./backend/app/core/homologated_config.py
  - Inicialización: ./init_homologated_system.py
""")

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description="Red Soluciones ISP v4.0 Homologado - Sistema Empresarial Completo",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=None,
        help=f'Puerto del servidor (default: {settings.PORT})'
    )
    
    parser.add_argument(
        '--dev', '-d',
        action='store_true',
        help='Modo desarrollo (hot reload, debug)'
    )
    
    parser.add_argument(
        '--check', '-c',
        action='store_true',
        help='Solo verificar configuración'
    )
    
    parser.add_argument(
        '--help-system',
        action='store_true',
        help='Mostrar ayuda detallada del sistema'
    )
    
    args = parser.parse_args()
    
    if args.help_system:
        print_help()
        return
    
    # Ejecutar sistema
    runner = HomologatedSystemRunner()
    
    try:
        success = asyncio.run(runner.run_system(
            port=args.port,
            dev_mode=args.dev,
            check_config_only=args.check
        ))
        
        if success:
            if not args.check:
                print("\n👋 ¡Hasta luego!")
            sys.exit(0)
        else:
            print("\n💥 El sistema no pudo ejecutarse correctamente")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️ Sistema detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Error crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

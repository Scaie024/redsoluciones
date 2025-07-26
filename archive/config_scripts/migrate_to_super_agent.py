#!/usr/bin/env python3
"""
🔄 MIGRACIÓN AL SUPER AGENTE INTELIGENTE
======================================

Script para migrar del agente anterior al nuevo agente unificado
"""

import os
import shutil
import logging
from pathlib import Path
from datetime import datetime

def setup_logging():
    """Configurar logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('migration.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def backup_old_agents(logger):
    """Hacer backup de agentes anteriores"""
    
    logger.info("📦 Haciendo backup de agentes anteriores...")
    
    backup_dir = Path("backup_agents_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
    backup_dir.mkdir(exist_ok=True)
    
    old_agents = [
        "backend/app/services/smart_agent.py",
        "backend/app/services/smart_agent_new.py", 
        "backend/app/services/smart_agent_old.py",
        "backend/app/services/modern_agent_v2.py"
    ]
    
    for agent_file in old_agents:
        agent_path = Path(agent_file)
        if agent_path.exists():
            backup_path = backup_dir / agent_path.name
            shutil.copy2(agent_path, backup_path)
            logger.info(f"✅ Backup: {agent_file} → {backup_path}")
        else:
            logger.warning(f"⚠️ No encontrado: {agent_file}")
    
    logger.info(f"📦 Backup completado en: {backup_dir}")
    return backup_dir

def verify_new_agent(logger):
    """Verificar que el nuevo agente esté configurado"""
    
    logger.info("🔍 Verificando nuevo agente...")
    
    new_agent_path = Path("backend/app/services/super_agent_final.py")
    
    if not new_agent_path.exists():
        logger.error("❌ Super agente no encontrado!")
        return False
    
    # Verificar que el main.py esté actualizado
    main_path = Path("backend/app/main.py")
    if main_path.exists():
        with open(main_path, 'r') as f:
            content = f.read()
            
        if "super_agent_final" in content:
            logger.info("✅ main.py actualizado para usar super agente")
        else:
            logger.warning("⚠️ main.py puede necesitar actualización")
    
    logger.info("✅ Verificación del nuevo agente completada")
    return True

def verify_environment(logger):
    """Verificar configuración del entorno"""
    
    logger.info("🔧 Verificando configuración del entorno...")
    
    required_vars = {
        "GOOGLE_SHEET_ID": "ID de Google Sheets",
        "GEMINI_API_KEY": "API Key de Gemini"
    }
    
    missing_vars = []
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            masked_value = f"{'*' * (len(value) - 6)}{value[-6:]}" if len(value) > 6 else "***"
            logger.info(f"✅ {var}: {masked_value}")
        else:
            logger.warning(f"❌ {var}: NO CONFIGURADA ({description})")
            missing_vars.append(var)
    
    # Verificar service_account.json
    service_account = Path("service_account.json")
    if service_account.exists():
        logger.info("✅ service_account.json: ENCONTRADO")
    else:
        logger.warning("❌ service_account.json: NO ENCONTRADO")
        missing_vars.append("service_account.json")
    
    if missing_vars:
        logger.warning(f"⚠️ Variables faltantes: {', '.join(missing_vars)}")
        return False
    
    logger.info("✅ Configuración del entorno verificada")
    return True

def test_super_agent(logger):
    """Probar el super agente"""
    
    logger.info("🧪 Probando super agente...")
    
    try:
        from backend.app.services.super_agent_final import SuperIntelligentAgent
        from backend.app.services.sheets.service import SheetsServiceV2
        
        # Inicializar servicios
        sheets_service = SheetsServiceV2()
        agent = SuperIntelligentAgent(sheets_service)
        
        # Test básico
        test_query = "ayuda"
        response = agent.process_query(test_query)
        
        if response and response.get("response"):
            logger.info("✅ Super agente funcionando correctamente")
            logger.info(f"   Respuesta de prueba: {response['response'][:100]}...")
            return True
        else:
            logger.error("❌ Super agente no responde correctamente")
            return False
            
    except ImportError as e:
        logger.error(f"❌ Error de importación: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Error probando super agente: {e}")
        return False

def generate_migration_report(logger, backup_dir, success):
    """Generar reporte de migración"""
    
    logger.info("📋 Generando reporte de migración...")
    
    report_path = Path("MIGRATION_REPORT.md")
    
    with open(report_path, 'w') as f:
        f.write(f"""# 🔄 REPORTE DE MIGRACIÓN - SUPER AGENTE INTELIGENTE

## 📊 Resumen
- **Fecha**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Estado**: {'✅ EXITOSA' if success else '❌ FALLÓ'}
- **Backup**: {backup_dir.name}

## 📦 Archivos Respaldados
""")
        
        if backup_dir.exists():
            for backup_file in backup_dir.iterdir():
                f.write(f"- `{backup_file.name}`\n")
        
        f.write(f"""
## 🔧 Configuración
- GOOGLE_SHEET_ID: {'✅ Configurada' if os.getenv('GOOGLE_SHEET_ID') else '❌ Faltante'}
- GEMINI_API_KEY: {'✅ Configurada' if os.getenv('GEMINI_API_KEY') else '❌ Faltante'}
- service_account.json: {'✅ Presente' if Path('service_account.json').exists() else '❌ Faltante'}

## 🚀 Nuevo Agente
- Archivo: `backend/app/services/super_agent_final.py`
- Estado: {'✅ Funcionando' if success else '❌ Necesita corrección'}

## 📝 Próximos Pasos
""")
        
        if success:
            f.write("""
1. ✅ El super agente está funcionando correctamente
2. 🧪 Ejecutar tests completos: `python test_super_agent.py`
3. 🚀 Iniciar servidor: `python backend/app/main.py`
4. 💬 Probar chat en: http://localhost:8004
""")
        else:
            f.write("""
1. ❌ Revisar configuración de variables de entorno
2. 🔧 Verificar credenciales de Google Sheets y Gemini
3. 📞 Contactar soporte si el problema persiste
""")
    
    logger.info(f"📋 Reporte generado: {report_path}")

def main():
    """Función principal de migración"""
    
    logger = setup_logging()
    
    logger.info("🚀 INICIANDO MIGRACIÓN AL SUPER AGENTE INTELIGENTE")
    logger.info("🏢 Red Soluciones ISP - Sistema Unificado")
    logger.info("=" * 60)
    
    try:
        # 1. Backup de agentes anteriores
        backup_dir = backup_old_agents(logger)
        
        # 2. Verificar nuevo agente
        agent_ok = verify_new_agent(logger)
        
        # 3. Verificar entorno
        env_ok = verify_environment(logger)
        
        # 4. Probar super agente
        test_ok = test_super_agent(logger) if agent_ok and env_ok else False
        
        success = agent_ok and env_ok and test_ok
        
        # 5. Generar reporte
        generate_migration_report(logger, backup_dir, success)
        
        # 6. Resultado final
        if success:
            logger.info("🎉 ¡MIGRACIÓN COMPLETADA EXITOSAMENTE!")
            logger.info("💡 El super agente inteligente está listo para usar")
            logger.info("🔗 Ejecuta 'python test_super_agent.py' para probar")
        else:
            logger.error("❌ MIGRACIÓN INCOMPLETA")
            logger.error("💡 Revisa el reporte y corrige los problemas")
        
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"💥 Error crítico en migración: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

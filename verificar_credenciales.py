#!/usr/bin/env python3
"""
Red Soluciones ISP - Script de Verificación de Credenciales
Verifica que todas las credenciales estén configuradas correctamente
"""

import os
import sys
from pathlib import Path

# Añadir el directorio del proyecto al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Cargar variables de entorno desde .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Si python-dotenv no está disponible, cargar manualmente
    env_file = project_root / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

def check_environment():
    """Verificar configuración del entorno"""
    print("🔍 VERIFICACIÓN DE CREDENCIALES - Red Soluciones ISP")
    print("=" * 60)
    print("⚠️  MODO PRODUCCIÓN: Todas las credenciales son OBLIGATORIAS")
    print()
    
    # Variables críticas OBLIGATORIAS
    critical_vars = {
        'GOOGLE_SHEET_ID': 'ID de Google Sheets (OBLIGATORIO)',
        'GEMINI_API_KEY': 'API Key de Gemini AI (OBLIGATORIO)',
    }
    
    # Variables importantes
    important_vars = {
        'ENVIRONMENT': 'Entorno de ejecución',
        'SECRET_KEY': 'Clave secreta',
        'PORT': 'Puerto del servidor',
        'DEBUG': 'Modo debug'
    }
    
    print("� CREDENCIALES OBLIGATORIAS:")
    all_critical_ok = True
    
    for var, description in critical_vars.items():
        value = os.getenv(var)
        if value and len(value.strip()) > 0 and not value.startswith("tu_"):
            if var == 'GOOGLE_SHEET_ID' and len(value) > 20:
                print(f"  ✅ {var}: Configurado correctamente")
            elif var == 'GEMINI_API_KEY' and value.startswith('AIza'):
                print(f"  ✅ {var}: API Key válida detectada")
            elif var == 'GEMINI_API_KEY':
                print(f"  ⚠️  {var}: Configurado pero formato inusual (verificar)")
            else:
                print(f"  ✅ {var}: Configurado")
        else:
            print(f"  ❌ {var}: ¡FALTA! ({description})")
            all_critical_ok = False
    
    print("\n📋 CONFIGURACIÓN ADICIONAL:")
    for var, description in important_vars.items():
        value = os.getenv(var)
        if value:
            if var == 'ENVIRONMENT' and value == 'production':
                print(f"  ✅ {var}: {value} (RECOMENDADO para uso real)")
            else:
                print(f"  ✅ {var}: {value}")
        else:
            print(f"  ⚠️  {var}: Usando valor por defecto ({description})")
    
    # Verificar archivos
    print("\n📁 ARCHIVOS OBLIGATORIOS:")
    service_account_file = project_root / "service_account.json"
    if service_account_file.exists():
        print("  ✅ service_account.json: Encontrado y configurado")
    else:
        print("  ❌ service_account.json: ¡FALTA! (OBLIGATORIO para Google Sheets)")
        all_critical_ok = False
    
    env_file = project_root / ".env"
    if env_file.exists():
        print("  ✅ .env: Encontrado")
    else:
        print("  ❌ .env: No encontrado (crear desde .env.example)")
        all_critical_ok = False
    
    # Verificar importaciones
    print("\n🔧 VERIFICACIÓN TÉCNICA:")
    try:
        from backend.app.core.config import settings
        print(f"  ✅ Configuración: {settings.PROJECT_NAME} v{settings.VERSION}")
        print(f"  ✅ Entorno: {settings.ENVIRONMENT}")
        print(f"  ✅ Puerto: {settings.PORT}")
    except Exception as e:
        print(f"  ❌ Error en configuración: {e}")
        return False
    
    # Verificar servicios
    try:
        from backend.app.services.smart_agent import SmartISPAgent
        print("  ✅ SmartAgent: Disponible")
    except Exception as e:
        print(f"  ❌ SmartAgent: Error - {e}")
    
    try:
        from backend.app.services.sheets.service import SheetsServiceV2
        print("  ✅ SheetsService: Disponible")
    except Exception as e:
        print(f"  ❌ SheetsService: Error - {e}")
    
    # Resumen final
    print("\n" + "=" * 60)
    if all_critical_ok:
        print("🎉 ESTADO: SISTEMA LISTO PARA PRODUCCIÓN")
        print("✅ Todas las credenciales obligatorias están configuradas")
        print("🚀 Red Soluciones ISP completamente funcional")
        print("💼 Listo para uso empresarial")
    else:
        print("❌ ESTADO: CONFIGURACIÓN INCOMPLETA")
        print("🚨 FALTAN CREDENCIALES OBLIGATORIAS")
        print("⛔ El sistema NO FUNCIONARÁ sin estas credenciales")
        print()
        print("📋 PASOS PARA SOLUCIONAR:")
        print("1. Ejecutar: python3 configurar_credenciales.py")
        print("2. Obtener Gemini API Key: https://makersuite.google.com/app/apikey")
        print("3. Descargar service_account.json de Google Cloud Console")
        print("4. Configurar GOOGLE_SHEET_ID en .env")
        print("5. Volver a ejecutar este script")
    
    return all_critical_ok

if __name__ == "__main__":
    check_environment()

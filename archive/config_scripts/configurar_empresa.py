#!/usr/bin/env python3
"""
Red Soluciones ISP - Configuración Empresarial
Script para configurar el sistema para uso real de la empresa
"""

import os
import sys
import secrets
from pathlib import Path

def setup_production():
    """Configurar sistema para uso empresarial"""
    print("🏢 RED SOLUCIONES ISP - CONFIGURACIÓN EMPRESARIAL")
    print("=" * 60)
    print("Este script configura el sistema para uso REAL de la empresa")
    print("⚠️  TODAS LAS CREDENCIALES SON OBLIGATORIAS")
    print()
    
    # Verificar si ya existe configuración
    env_file = Path(".env")
    if env_file.exists():
        response = input("⚠️  Ya existe un archivo .env. ¿Sobrescribir? (s/N): ")
        if response.lower() != 's':
            print("❌ Operación cancelada")
            return False
    
    print("📋 CONFIGURACIÓN DE CREDENCIALES EMPRESARIALES")
    print("=" * 40)
    
    # Google Sheets ID
    print("\n1️⃣  GOOGLE SHEETS ID:")
    print("   • Abra su Google Sheet de Red Soluciones")
    print("   • Copie el ID de la URL: docs.google.com/spreadsheets/d/[ESTE_ID]/edit")
    print("   • Ejemplo: 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms")
    
    while True:
        sheet_id = input("\n📊 Ingrese el Google Sheet ID: ").strip()
        if len(sheet_id) > 20 and not sheet_id.startswith("tu_"):
            break
        print("❌ ID inválido. Debe ser el ID completo de Google Sheets (40+ caracteres)")
    
    # Gemini API Key
    print("\n2️⃣  GEMINI AI API KEY:")
    print("   • Vaya a: https://makersuite.google.com/app/apikey")
    print("   • Cree un nuevo proyecto o use uno existente")
    print("   • Genere una API Key")
    print("   • Formato: AIzaSyC...")
    
    while True:
        gemini_key = input("\n🤖 Ingrese la Gemini API Key: ").strip()
        if gemini_key.startswith("AIza") and len(gemini_key) > 30:
            break
        print("❌ API Key inválida. Debe comenzar con 'AIza' y tener más de 30 caracteres")
    
    # Service Account
    print("\n3️⃣  SERVICE ACCOUNT:")
    service_account_file = Path("service_account.json")
    if not service_account_file.exists():
        print("   ❌ service_account.json NO ENCONTRADO")
        print("   📥 INSTRUCCIONES:")
        print("   • Vaya a: https://console.cloud.google.com/")
        print("   • IAM & Admin > Service Accounts")
        print("   • Crear cuenta de servicio")
        print("   • Descargar JSON y guardarlo como 'service_account.json'")
        print("   • Colocar en la raíz del proyecto")
        
        input("\n⏸️  Presione Enter cuando haya colocado service_account.json...")
        
        if not service_account_file.exists():
            print("❌ service_account.json aún no encontrado. Configure manualmente.")
            return False
    
    print("   ✅ service_account.json encontrado")
    
    # Configuración adicional
    print("\n4️⃣  CONFIGURACIÓN DEL SISTEMA:")
    
    # Environment
    env_choice = input("🌍 Entorno [production/development] (recomendado: production): ").strip()
    environment = env_choice if env_choice in ['production', 'development'] else 'production'
    
    # Debug
    debug = 'false' if environment == 'production' else 'true'
    
    # Puerto
    port_input = input("🔌 Puerto del servidor (default: 8004): ").strip()
    port = port_input if port_input.isdigit() else '8004'
    
    # Secret Key
    secret_key = secrets.token_urlsafe(32)
    
    # Crear archivo .env
    print("\n💾 GUARDANDO CONFIGURACIÓN...")
    
    env_content = f"""# Red Soluciones ISP - Configuración Empresarial
# Configurado automáticamente para uso real
# Fecha: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# ================================
# CREDENCIALES EMPRESARIALES
# ================================

# Google Sheets ID (Base de datos principal)
GOOGLE_SHEET_ID={sheet_id}

# Gemini AI API Key (Chat inteligente)
GEMINI_API_KEY={gemini_key}

# ================================
# CONFIGURACIÓN DE PRODUCCIÓN
# ================================

# Entorno empresarial
ENVIRONMENT={environment}
DEBUG={debug}

# Servidor
PORT={port}
HOST=0.0.0.0

# Seguridad
SECRET_KEY={secret_key}

# Logging
LOG_LEVEL=INFO

# ================================
# NOTAS IMPORTANTES
# ================================
# - Mantener este archivo seguro y privado
# - NO subir a repositorios públicos
# - Hacer backup de las credenciales
# - Renovar API keys periódicamente
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Archivo .env creado exitosamente")
    
    # Verificar configuración
    print("\n🔍 VERIFICANDO CONFIGURACIÓN...")
    
    # Importar y verificar
    try:
        os.environ.clear()  # Limpiar variables anteriores
        # Cargar nuevas variables
        for line in env_content.split('\n'):
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
        
        # Verificar sistema
        sys.path.insert(0, '.')
        from backend.app.core.config import settings
        
        print(f"✅ Proyecto: {settings.PROJECT_NAME}")
        print(f"✅ Entorno: {settings.ENVIRONMENT}")
        print(f"✅ Puerto: {settings.PORT}")
        print(f"✅ Google Sheets: Configurado")
        print(f"✅ Gemini AI: Configurado")
        
    except Exception as e:
        print(f"⚠️  Error en verificación: {e}")
        print("🔧 El archivo .env se creó pero hay que revisar la configuración")
    
    # Configuración de permisos Google Sheets
    print("\n📋 CONFIGURACIÓN FINAL DE GOOGLE SHEETS:")
    print("1. Abra su Google Sheet")
    print("2. Clic en 'Compartir'")
    print("3. Agregar el email del service account como editor")
    print("4. El email está en service_account.json (campo 'client_email')")
    
    print("\n🎉 ¡CONFIGURACIÓN EMPRESARIAL COMPLETADA!")
    print("=" * 60)
    print("✅ Sistema configurado para uso real")
    print("🏢 Listo para Red Soluciones ISP")
    print("🚀 Ejecutar: python3 app.py")
    print("🌐 Acceder: http://localhost:8004")
    
    return True

if __name__ == "__main__":
    if setup_production():
        print("\n🔍 Ejecutando verificación final...")
        os.system("python3 verificar_credenciales.py")

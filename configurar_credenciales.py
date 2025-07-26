#!/usr/bin/env python3
"""
Red Soluciones ISP - Configuración Rápida de Credenciales
Script interactivo para configurar las credenciales principales
"""

import os
import sys
from pathlib import Path

def configure_credentials():
    """Configuración interactiva de credenciales"""
    print("🔧 CONFIGURACIÓN RÁPIDA - Red Soluciones ISP")
    print("=" * 60)
    print("Este script te ayudará a configurar las credenciales principales")
    print()
    
    # Leer archivo .env existente
    env_file = Path(".env")
    env_vars = {}
    
    if env_file.exists():
        print("📄 Archivo .env existente encontrado")
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
    else:
        print("📄 Creando nuevo archivo .env")
    
    print("\n🔑 CONFIGURACIÓN DE CREDENCIALES:")
    print("(Presiona Enter para mantener el valor actual)")
    print()
    
    # Google Sheets ID
    current_sheet = env_vars.get('GOOGLE_SHEET_ID', '')
    if current_sheet and not current_sheet.startswith('tu_'):
        prompt = f"Google Sheets ID (actual: {current_sheet[:15]}...): "
    else:
        prompt = "Google Sheets ID (ejemplo: 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms): "
    
    sheet_id = input(prompt).strip()
    if sheet_id:
        env_vars['GOOGLE_SHEET_ID'] = sheet_id
    elif 'GOOGLE_SHEET_ID' not in env_vars:
        env_vars['GOOGLE_SHEET_ID'] = '1OZKZIpn6U1nCfrDM_yGmC6jKj6iLH_MQz814LjEBRMQ'  # Demo sheet
    
    # Gemini API Key
    current_gemini = env_vars.get('GEMINI_API_KEY', '')
    if current_gemini and not current_gemini.startswith('tu_'):
        prompt = f"Gemini API Key (actual: {current_gemini[:15]}...): "
    else:
        prompt = "Gemini API Key (ejemplo: AIzaSyC-...): "
    
    gemini_key = input(prompt).strip()
    if gemini_key:
        env_vars['GEMINI_API_KEY'] = gemini_key
    elif 'GEMINI_API_KEY' not in env_vars:
        env_vars['GEMINI_API_KEY'] = 'demo_key_for_testing'
    
    # Environment
    current_env = env_vars.get('ENVIRONMENT', 'development')
    env_choice = input(f"Entorno (actual: {current_env}) [development/production]: ").strip()
    if env_choice in ['development', 'production']:
        env_vars['ENVIRONMENT'] = env_choice
    elif 'ENVIRONMENT' not in env_vars:
        env_vars['ENVIRONMENT'] = 'development'
    
    # Debug
    current_debug = env_vars.get('DEBUG', 'true')
    debug_choice = input(f"Modo Debug (actual: {current_debug}) [true/false]: ").strip()
    if debug_choice in ['true', 'false']:
        env_vars['DEBUG'] = debug_choice
    elif 'DEBUG' not in env_vars:
        env_vars['DEBUG'] = 'true'
    
    # Port
    current_port = env_vars.get('PORT', '8004')
    port_choice = input(f"Puerto (actual: {current_port}): ").strip()
    if port_choice and port_choice.isdigit():
        env_vars['PORT'] = port_choice
    elif 'PORT' not in env_vars:
        env_vars['PORT'] = '8004'
    
    # Secret Key
    if 'SECRET_KEY' not in env_vars:
        import secrets
        env_vars['SECRET_KEY'] = secrets.token_urlsafe(32)
    
    # Escribir archivo .env
    print("\n💾 Guardando configuración...")
    
    with open('.env', 'w') as f:
        f.write("# Red Soluciones ISP - Configuración de Entorno\n")
        f.write("# Generado automáticamente\n\n")
        
        f.write("# === CONFIGURACIÓN PRINCIPAL ===\n")
        f.write(f"ENVIRONMENT={env_vars['ENVIRONMENT']}\n")
        f.write(f"DEBUG={env_vars['DEBUG']}\n")
        f.write(f"PORT={env_vars['PORT']}\n")
        f.write(f"SECRET_KEY={env_vars['SECRET_KEY']}\n\n")
        
        f.write("# === SERVICIOS EXTERNOS ===\n")
        f.write(f"GOOGLE_SHEET_ID={env_vars['GOOGLE_SHEET_ID']}\n")
        f.write(f"GEMINI_API_KEY={env_vars['GEMINI_API_KEY']}\n\n")
        
        f.write("# === CONFIGURACIÓN ADICIONAL ===\n")
        f.write("HOST=0.0.0.0\n")
        f.write("LOG_LEVEL=INFO\n")
    
    print("✅ Archivo .env creado exitosamente")
    
    # Verificar configuración
    print("\n🔍 Verificando configuración...")
    os.system(f"{sys.executable} verificar_credenciales.py")
    
    print("\n🎉 ¡Configuración completada!")
    print("\n📖 PRÓXIMOS PASOS:")
    print("1. Si usas Google Sheets, asegúrate de compartir la hoja con el service account")
    print("2. Para obtener Gemini API Key: https://makersuite.google.com/app/apikey") 
    print("3. Ejecutar: python app.py")
    print("4. Abrir: http://localhost:8004")

if __name__ == "__main__":
    configure_credentials()

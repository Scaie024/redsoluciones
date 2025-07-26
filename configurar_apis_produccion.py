#!/usr/bin/env python3
"""
Configurador de APIs Productivas - Red Soluciones ISP
Configura las APIs reales para modo productivo
"""
import os
import re
from pathlib import Path

def configurar_apis_produccion():
    """Configura las APIs necesarias para producción"""
    print("🚀 CONFIGURADOR DE APIs PRODUCTIVAS - Red Soluciones ISP")
    print("=" * 60)
    
    # Ruta del archivo .env
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ Archivo .env no encontrado")
        return False
    
    print("\n🔧 CONFIGURACIÓN DE APIs OBLIGATORIAS:")
    print("-" * 40)
    
    # Pedir Gemini API Key
    print("\n1️⃣ GEMINI API KEY")
    print("   📍 Obtener en: https://makersuite.google.com/app/apikey")
    gemini_key = input("   🔑 Ingrese su Gemini API Key: ").strip()
    
    if not gemini_key:
        print("   ❌ API Key requerida")
        return False
    
    # Pedir Google Sheets ID
    print("\n2️⃣ GOOGLE SHEETS ID")
    print("   📍 Obtener de la URL de su hoja de Google Sheets")
    print("   📄 Formato: docs.google.com/spreadsheets/d/[ESTE_ID]/edit")
    sheets_id = input("   📊 Ingrese el ID de su Google Sheet: ").strip()
    
    if not sheets_id:
        print("   ❌ Google Sheets ID requerido")
        return False
    
    # Leer contenido actual
    content = env_file.read_text()
    
    # Actualizar Gemini API Key
    content = re.sub(
        r'GEMINI_API_KEY=.*',
        f'GEMINI_API_KEY={gemini_key}',
        content
    )
    
    # Actualizar Google Sheets ID
    content = re.sub(
        r'GOOGLE_SHEET_ID=.*',
        f'GOOGLE_SHEET_ID={sheets_id}',
        content
    )
    
    # Guardar cambios
    env_file.write_text(content)
    
    print("\n✅ CONFIGURACIÓN COMPLETADA")
    print("=" * 60)
    print("🔥 APIs configuradas para modo PRODUCTIVO")
    print("🚀 Sistema listo para funcionar con APIs reales")
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Ejecutar: python3 verificar_credenciales.py")
    print("2. Reiniciar el servidor")
    print("3. Probar los comandos del agente")
    
    return True

if __name__ == "__main__":
    try:
        configurar_apis_produccion()
    except KeyboardInterrupt:
        print("\n\n❌ Configuración cancelada")
    except Exception as e:
        print(f"\n❌ Error: {e}")

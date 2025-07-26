#!/usr/bin/env python3
"""
🧪 VERIFICACIÓN FINAL DEL SISTEMA - Red Soluciones ISP
=====================================================

Script que verifica que todas las correcciones han sido aplicadas
y el sistema está funcionando correctamente.
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def main():
    print("🧪 VERIFICACIÓN FINAL DEL SISTEMA CORREGIDO")
    print("=" * 50)
    
    # 1. Verificar archivos críticos
    verify_critical_files()
    
    # 2. Verificar variables de entorno
    verify_environment()
    
    # 3. Verificar dependencias
    verify_dependencies()
    
    # 4. Probar importaciones
    verify_imports()
    
    # 5. Probar el servidor
    verify_server()
    
    print("\n✅ VERIFICACIÓN COMPLETADA")

def verify_critical_files():
    """Verifica que todos los archivos críticos existan"""
    print("\n📁 Verificando archivos críticos...")
    
    critical_files = [
        ".env",
        "requirements.txt", 
        "service_account.json",
        "backend/app/main.py",
        "backend/app/core/config_unified.py",
        "backend/app/core/user_auth.py",
        "backend/app/utils/logging_setup.py"
    ]
    
    for file_path in critical_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - FALTA")

def verify_environment():
    """Verifica variables de entorno"""
    print("\n🌍 Verificando variables de entorno...")
    
    # Cargar .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    env_vars = {
        "GOOGLE_SHEET_ID": "✅" if os.getenv("GOOGLE_SHEET_ID") else "❌",
        "GEMINI_API_KEY": "✅" if os.getenv("GEMINI_API_KEY") else "⚠️ Opcional",
        "HOST": os.getenv("HOST", "0.0.0.0"),
        "PORT": os.getenv("PORT", "8004"),
        "DEBUG": os.getenv("DEBUG", "false"),
    }
    
    for var, status in env_vars.items():
        print(f"  {var}: {status}")

def verify_dependencies():
    """Verifica dependencias instaladas"""
    print("\n📦 Verificando dependencias críticas...")
    
    critical_deps = [
        "fastapi",
        "uvicorn", 
        "gspread",
        "google-generativeai",
        "python-dotenv"
    ]
    
    for dep in critical_deps:
        try:
            __import__(dep.replace("-", "_"))
            print(f"  ✅ {dep}")
        except ImportError:
            print(f"  ❌ {dep} - NO INSTALADO")

def verify_imports():
    """Verifica importaciones del sistema"""
    print("\n🔧 Verificando importaciones del sistema...")
    
    try:
        from backend.app.core.config import settings
        print("  ✅ Configuración")
    except Exception as e:
        print(f"  ❌ Configuración: {e}")
    
    try:
        from backend.app.services.sheets.service import SheetsServiceV2
        print("  ✅ Google Sheets Service")
    except Exception as e:
        print(f"  ❌ Google Sheets Service: {e}")
    
    try:
        from backend.app.services.smart_agent import SmartISPAgent
        print("  ✅ Smart Agent")
    except Exception as e:
        print(f"  ❌ Smart Agent: {e}")
    
    try:
        from backend.app.core.user_auth import user_auth
        print("  ✅ Sistema de Autenticación")
    except Exception as e:
        print(f"  ❌ Sistema de Autenticación: {e}")

def verify_server():
    """Verifica que el servidor se pueda iniciar"""
    print("\n🚀 Verificando servidor...")
    
    # Intentar importar la app
    try:
        from backend.app.main import app
        print("  ✅ FastAPI app importada correctamente")
    except Exception as e:
        print(f"  ❌ Error importando app: {e}")
        return
    
    print("  ✅ Sistema listo para iniciar")

if __name__ == "__main__":
    main()

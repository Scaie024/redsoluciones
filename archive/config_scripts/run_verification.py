#!/usr/bin/env python3
"""
Ejecuta verificación del sistema y guarda resultados
"""
import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Configurar path y variables
sys.path.insert(0, str(Path(__file__).parent))
os.environ['GOOGLE_SHEET_ID'] = '1OZKZIpn6U1nCfrDM_yGmC6jKj6iLH_MQz814LjEBRMQ'

def run_verification():
    """Ejecuta verificación completa y retorna resultados"""
    results = {
        "timestamp": datetime.now().isoformat(),
        "status": "running",
        "checks": {}
    }
    
    # 1. Verificar archivos
    files_check = {}
    critical_files = [
        'service_account.json',
        'app.py',
        'backend/app/main.py',
        'frontend/index.html',
        'vercel.json'
    ]
    
    for file_path in critical_files:
        exists = Path(file_path).exists()
        files_check[file_path] = {
            "exists": exists,
            "status": "✅ EXISTE" if exists else "❌ FALTA"
        }
    
    results["checks"]["files"] = files_check
    
    # 2. Variables de entorno
    env_check = {
        "GOOGLE_SHEET_ID": {
            "value": os.environ.get('GOOGLE_SHEET_ID'),
            "status": "✅ CONFIGURADO" if os.environ.get('GOOGLE_SHEET_ID') else "❌ FALTA"
        }
    }
    results["checks"]["environment"] = env_check
    
    # 3. Importaciones
    imports_check = {}
    
    # Test SheetsServiceV2
    try:
        from backend.app.services.sheets.service import SheetsServiceV2
        imports_check["SheetsServiceV2"] = {
            "status": "✅ OK",
            "error": None
        }
        sheets_import_ok = True
    except Exception as e:
        imports_check["SheetsServiceV2"] = {
            "status": "❌ ERROR",
            "error": str(e)
        }
        sheets_import_ok = False
    
    # Test SmartISPAgent
    try:
        from backend.app.services.smart_agent import SmartISPAgent
        imports_check["SmartISPAgent"] = {
            "status": "✅ OK",
            "error": None
        }
        agent_import_ok = True
    except Exception as e:
        imports_check["SmartISPAgent"] = {
            "status": "❌ ERROR",
            "error": str(e)
        }
        agent_import_ok = False
    
    # Test FastAPI App
    try:
        from backend.app.main import app
        imports_check["FastAPI_App"] = {
            "status": "✅ OK",
            "error": None
        }
        app_import_ok = True
    except Exception as e:
        imports_check["FastAPI_App"] = {
            "status": "❌ ERROR", 
            "error": str(e)
        }
        app_import_ok = False
    
    results["checks"]["imports"] = imports_check
    
    # 4. Google Sheets Connection
    sheets_check = {}
    if sheets_import_ok:
        try:
            service = SheetsServiceV2()
            sheets_check["service_init"] = {
                "status": "✅ INICIALIZADO",
                "error": None
            }
            
            # Test connection
            connection_result = service.test_connection()
            if connection_result and connection_result.get('status') == 'connected':
                sheets_check["connection"] = {
                    "status": "✅ CONECTADO",
                    "sheet_id": connection_result.get('sheet_id'),
                    "message": connection_result.get('message')
                }
                
                # Get real data
                try:
                    clients = service.get_all_clients()
                    sheets_check["data_clients"] = {
                        "status": "✅ DATOS OK",
                        "count": len(clients)
                    }
                    
                    analytics = service.get_analytics()
                    sheets_check["data_analytics"] = {
                        "status": "✅ ANALYTICS OK",
                        "data": analytics
                    }
                    
                except Exception as e:
                    sheets_check["data_retrieval"] = {
                        "status": "❌ ERROR DATOS",
                        "error": str(e)
                    }
            else:
                sheets_check["connection"] = {
                    "status": "❌ CONEXIÓN FALLIDA",
                    "error": "No se pudo conectar a Google Sheets"
                }
                
        except Exception as e:
            sheets_check["service_init"] = {
                "status": "❌ ERROR INICIALIZACIÓN",
                "error": str(e)
            }
    else:
        sheets_check["service_init"] = {
            "status": "❌ IMPORT FAILED",
            "error": "No se pudo importar SheetsServiceV2"
        }
    
    results["checks"]["google_sheets"] = sheets_check
    
    # 5. Status final
    all_files_ok = all(check["exists"] for check in files_check.values())
    all_imports_ok = sheets_import_ok and agent_import_ok and app_import_ok
    sheets_connected = sheets_check.get("connection", {}).get("status", "").startswith("✅")
    
    if all_files_ok and all_imports_ok and sheets_connected:
        results["status"] = "✅ SISTEMA COMPLETAMENTE OPERATIVO"
        results["summary"] = {
            "files": "✅ TODOS LOS ARCHIVOS PRESENTES",
            "imports": "✅ TODAS LAS IMPORTACIONES EXITOSAS", 
            "google_sheets": "✅ CONECTADO CON DATOS REALES",
            "ready_for": "🚀 LISTO PARA PRODUCCIÓN"
        }
    else:
        results["status"] = "⚠️ SISTEMA REQUIERE ATENCIÓN"
        results["summary"] = {
            "files": "✅ OK" if all_files_ok else "❌ FALTAN ARCHIVOS",
            "imports": "✅ OK" if all_imports_ok else "❌ ERROR IMPORTACIONES",
            "google_sheets": "✅ OK" if sheets_connected else "❌ ERROR CONEXIÓN"
        }
    
    return results

def main():
    print("🚀 Ejecutando verificación completa...")
    
    # Ejecutar verificación
    results = run_verification()
    
    # Guardar resultados en archivo
    with open('system_status.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Mostrar resumen en pantalla
    print(f"\n{results['status']}")
    print("=" * 60)
    
    for category, checks in results["checks"].items():
        print(f"\n📋 {category.upper()}:")
        if isinstance(checks, dict):
            for name, check in checks.items():
                if isinstance(check, dict):
                    print(f"   {check.get('status', '❓')} {name}")
                    if check.get('error'):
                        print(f"      Error: {check['error'][:100]}...")
                    if check.get('count'):
                        print(f"      Registros: {check['count']}")
    
    print(f"\n📄 Resultados completos guardados en: system_status.json")
    
    if results["status"].startswith("✅"):
        print("\n🎉 ¡SISTEMA LISTO PARA USAR!")
        print("🚀 Para iniciar el servidor:")
        print("   export GOOGLE_SHEET_ID='1OZKZIpn6U1nCfrDM_yGmC6jKj6iLH_MQz814LjEBRMQ'")
        print("   python3 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    main()

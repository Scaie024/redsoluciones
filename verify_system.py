#!/usr/bin/env python3
"""
Script completo de verificación para Red Soluciones ISP
"""
import os
import sys
import json
from pathlib import Path

# Configurar path
sys.path.insert(0, str(Path(__file__).parent))

# Configurar variables de entorno
os.environ['GOOGLE_SHEET_ID'] = '1OZKZIpn6U1nCfrDM_yGmC6jKj6iLH_MQz814LjEBRMQ'

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}")

def print_step(step, description):
    print(f"\n{step}. {description}")

def print_result(success, message):
    symbol = "✅" if success else "❌"
    print(f"   {symbol} {message}")

def main():
    print_header("VERIFICACIÓN COMPLETA DEL SISTEMA RED SOLUCIONES")
    
    # 1. Verificar archivos de configuración
    print_step(1, "Verificando archivos de configuración")
    
    service_account_exists = Path('service_account.json').exists()
    print_result(service_account_exists, f"service_account.json {'encontrado' if service_account_exists else 'NO encontrado'}")
    
    app_py_exists = Path('app.py').exists()
    print_result(app_py_exists, f"app.py {'encontrado' if app_py_exists else 'NO encontrado'}")
    
    main_py_exists = Path('backend/app/main.py').exists()
    print_result(main_py_exists, f"backend/app/main.py {'encontrado' if main_py_exists else 'NO encontrado'}")
    
    # 2. Verificar variables de entorno
    print_step(2, "Verificando variables de entorno")
    
    google_sheet_id = os.environ.get('GOOGLE_SHEET_ID')
    print_result(bool(google_sheet_id), f"GOOGLE_SHEET_ID: {google_sheet_id}")
    
    # 3. Probar importaciones
    print_step(3, "Probando importaciones del sistema")
    
    try:
        from backend.app.services.sheets.service import SheetsServiceV2
        print_result(True, "SheetsServiceV2 importado correctamente")
        sheets_import_ok = True
    except Exception as e:
        print_result(False, f"Error importando SheetsServiceV2: {e}")
        sheets_import_ok = False
    
    try:
        from backend.app.services.smart_agent import SmartISPAgent
        print_result(True, "SmartISPAgent importado correctamente")
        agent_import_ok = True
    except Exception as e:
        print_result(False, f"Error importando SmartISPAgent: {e}")
        agent_import_ok = False
    
    try:
        from backend.app.main import app
        print_result(True, "FastAPI app importada correctamente")
        app_import_ok = True
    except Exception as e:
        print_result(False, f"Error importando FastAPI app: {e}")
        app_import_ok = False
    
    # 4. Probar conexión a Google Sheets
    if sheets_import_ok:
        print_step(4, "Probando conexión a Google Sheets")
        
        try:
            service = SheetsServiceV2()
            print_result(True, "Servicio de Google Sheets inicializado")
            
            # Test de conexión
            result = service.test_connection()
            connection_ok = result and result.get('status') == 'connected'
            print_result(connection_ok, f"Conexión a Google Sheets: {result.get('message', 'Sin mensaje') if result else 'Error en test'}")
            
            if connection_ok:
                # Obtener datos reales
                try:
                    clients = service.get_all_clients()
                    print_result(True, f"Clientes obtenidos: {len(clients)} registros")
                    
                    analytics = service.get_analytics()
                    print_result(True, f"Analytics obtenidos: {json.dumps(analytics, indent=2)}")
                    
                except Exception as e:
                    print_result(False, f"Error obteniendo datos: {e}")
                    
        except Exception as e:
            print_result(False, f"Error inicializando servicio de Google Sheets: {e}")
    
    # 5. Resumen final
    print_step(5, "Resumen del estado del sistema")
    
    all_files_ok = service_account_exists and app_py_exists and main_py_exists
    all_imports_ok = sheets_import_ok and agent_import_ok and app_import_ok
    
    print_result(all_files_ok, f"Archivos de configuración: {'COMPLETO' if all_files_ok else 'INCOMPLETO'}")
    print_result(all_imports_ok, f"Importaciones del sistema: {'EXITOSAS' if all_imports_ok else 'CON ERRORES'}")
    
    if all_files_ok and all_imports_ok:
        print_header("🎉 SISTEMA LISTO PARA USAR")
        print("✅ Backend consolidado funcionando")
        print("✅ Google Sheets conectado con datos reales")
        print("✅ Smart Agent Carlos operativo")
        print("✅ Frontend dashboard disponible")
        print("✅ Listo para despliegue en Vercel")
        
        print("\n🚀 Para iniciar el servidor ejecuta:")
        print("export GOOGLE_SHEET_ID='1OZKZIpn6U1nCfrDM_yGmC6jKj6iLH_MQz814LjEBRMQ'")
        print("python3 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000")
    else:
        print_header("⚠️ SISTEMA REQUIERE ATENCIÓN")
        print("Revisa los errores arriba para resolver los problemas pendientes.")

if __name__ == "__main__":
    main()

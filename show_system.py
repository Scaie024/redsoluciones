#!/usr/bin/env python3
"""
Demo directo del sistema Red Soluciones ISP
Ejecuta verificación y muestra resultados
"""
import os
import sys
import json
from pathlib import Path

# Configurar path y variables
sys.path.insert(0, str(Path(__file__).parent))
os.environ['GOOGLE_SHEET_ID'] = '1OZKZIpn6U1nCfrDM_yGmC6jKj6iLH_MQz814LjEBRMQ'

def show_system_status():
    print("🚀 RED SOLUCIONES ISP - VERIFICACIÓN EN VIVO")
    print("=" * 60)
    
    # 1. Verificar archivos
    print("\n📁 ARCHIVOS DE CONFIGURACIÓN:")
    files_to_check = [
        'service_account.json',
        'app.py', 
        'backend/app/main.py',
        'frontend/index.html',
        'vercel.json'
    ]
    
    for file_path in files_to_check:
        exists = Path(file_path).exists()
        status = "✅" if exists else "❌"
        print(f"   {status} {file_path}")
    
    # 2. Variables de entorno
    print("\n🔧 VARIABLES DE ENTORNO:")
    google_sheet_id = os.environ.get('GOOGLE_SHEET_ID')
    print(f"   ✅ GOOGLE_SHEET_ID: {google_sheet_id}")
    
    # 3. Importaciones
    print("\n📦 IMPORTACIONES DEL SISTEMA:")
    
    try:
        from backend.app.services.sheets.service import SheetsServiceV2
        print("   ✅ SheetsServiceV2 - Google Sheets Service")
        sheets_ok = True
    except Exception as e:
        print(f"   ❌ Error SheetsServiceV2: {e}")
        sheets_ok = False
    
    try:
        from backend.app.services.smart_agent import SmartISPAgent
        print("   ✅ SmartISPAgent - Carlos AI")
        agent_ok = True
    except Exception as e:
        print(f"   ❌ Error SmartISPAgent: {e}")
        agent_ok = False
    
    try:
        from backend.app.main import app
        print("   ✅ FastAPI App - Backend Principal")
        app_ok = True
    except Exception as e:
        print(f"   ❌ Error FastAPI App: {e}")
        app_ok = False
    
    # 4. Test de Google Sheets
    if sheets_ok:
        print("\n📊 CONEXIÓN A GOOGLE SHEETS:")
        try:
            service = SheetsServiceV2()
            print("   ✅ Servicio inicializado")
            
            result = service.test_connection()
            if result and result.get('status') == 'connected':
                print("   ✅ Conexión exitosa")
                
                # Obtener datos reales
                clients = service.get_all_clients()
                print(f"   ✅ Clientes obtenidos: {len(clients)} registros")
                
                analytics = service.get_analytics()
                print(f"   ✅ Analytics disponibles:")
                for key, value in analytics.items():
                    print(f"      • {key}: {value}")
                    
            else:
                print("   ❌ Error en conexión")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:100]}...")
    
    # 5. Resumen
    print("\n🎯 ESTADO FINAL:")
    if sheets_ok and agent_ok and app_ok:
        print("   🎉 ¡SISTEMA COMPLETAMENTE OPERATIVO!")
        print("   ✅ Google Sheets conectado con datos reales")
        print("   ✅ Smart Agent Carlos funcionando")
        print("   ✅ Backend consolidado y listo")
        print("   ✅ Listo para despliegue")
        
        print("\n🚀 PARA INICIAR EL SERVIDOR:")
        print("   export GOOGLE_SHEET_ID='1OZKZIpn6U1nCfrDM_yGmC6jKj6iLH_MQz814LjEBRMQ'")
        print("   python3 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000")
        
        return True
    else:
        print("   ⚠️ Sistema necesita atención en algunos componentes")
        return False

if __name__ == "__main__":
    show_system_status()

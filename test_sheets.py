#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, '.')

# Configurar variables de entorno
os.environ['GOOGLE_SHEET_ID'] = '1OZKZIpn6U1nCfrDM_yGmC6jKj6iLH_MQz814LjEBRMQ'

print("🚀 PROBANDO CONEXIÓN REAL A GOOGLE SHEETS")
print("=" * 50)
print(f"📂 Directorio: {os.getcwd()}")
print(f"📁 service_account.json: {'✅ EXISTE' if os.path.exists('service_account.json') else '❌ NO EXISTE'}")
print(f"📊 GOOGLE_SHEET_ID: {os.environ.get('GOOGLE_SHEET_ID', 'NO CONFIGURADO')}")
print()

try:
    print("📦 Importando SheetsServiceV2...")
    from backend.app.services.sheets.service import SheetsServiceV2
    print("✅ Importación exitosa")
    
    print("🔧 Inicializando servicio...")
    service = SheetsServiceV2()
    print("✅ Servicio inicializado")
    
    print("🧪 Probando conexión...")
    result = service.test_connection()
    print(f"📊 Resultado: {result}")
    
    if result and result.get('success'):
        print("🎉 ¡CONEXIÓN EXITOSA!")
        print("📋 Datos disponibles:")
        for key, value in result.items():
            print(f"   {key}: {value}")
    else:
        print("⚠️ Conexión con problemas")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

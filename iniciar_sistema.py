#!/usr/bin/env python3
"""
Inicializador simple para Red Soluciones ISP
"""
import os
import sys
from pathlib import Path

# Configurar path y variables
sys.path.insert(0, str(Path(__file__).parent))
os.environ['GOOGLE_SHEET_ID'] = '1OZKZIpn6U1nCfrDM_yGmC6jKj6iLH_MQz814LjEBRMQ'

def main():
    try:
        print("🚀 RED SOLUCIONES ISP - INICIANDO SISTEMA")
        print("=" * 50)
        
        # Verificar archivos críticos
        print("📁 Verificando archivos...")
        if not Path('service_account.json').exists():
            print("❌ Error: service_account.json no encontrado")
            return
        print("✅ service_account.json encontrado")
        
        if not Path('backend/app/main.py').exists():
            print("❌ Error: backend/app/main.py no encontrado")
            return
        print("✅ Backend principal encontrado")
        
        # Importar y verificar servicios
        print("\n📦 Importando servicios...")
        
        from backend.app.main import app
        print("✅ FastAPI app importada")
        
        from backend.app.services.sheets.service import SheetsServiceV2
        print("✅ Google Sheets service importado")
        
        # Test rápido de Google Sheets
        print("\n🧪 Probando conexión a Google Sheets...")
        service = SheetsServiceV2()
        result = service.test_connection()
        
        if result and result.get('status') == 'connected':
            print("✅ Google Sheets conectado exitosamente")
            clients = service.get_all_clients()
            print(f"✅ {len(clients)} clientes disponibles")
        else:
            print("⚠️ Problema con Google Sheets, continuando en modo mock")
        
        print("\n🌐 Iniciando servidor web...")
        print("📊 Dashboard disponible en: http://localhost:8000/")
        print("📚 API Docs en: http://localhost:8000/docs")
        print("❤️ Health Check en: http://localhost:8000/health")
        print("🤖 Chat Carlos en: http://localhost:8000/api/chat")
        print("\n✅ SISTEMA COMPLETAMENTE OPERATIVO")
        print("⚠️ Presiona Ctrl+C para detener")
        print("=" * 50)
        
        # Iniciar servidor
        import uvicorn
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            access_log=True
        )
        
    except KeyboardInterrupt:
        print("\n👋 Sistema detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

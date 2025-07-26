#!/usr/bin/env python3
"""
Servidor de prueba para Red Soluciones ISP
"""
import os
import sys
from pathlib import Path

# Configurar path y variables
sys.path.insert(0, str(Path(__file__).parent))
os.environ['GOOGLE_SHEET_ID'] = '1OZKZIpn6U1nCfrDM_yGmC6jKj6iLH_MQz814LjEBRMQ'

print("🚀 INICIANDO SERVIDOR RED SOLUCIONES ISP")
print("=" * 50)

try:
    print("📦 Importando aplicación...")
    from backend.app.main import app
    print("✅ Aplicación importada correctamente")
    
    print("🔧 Configurando servidor...")
    import uvicorn
    
    print("🌐 Iniciando servidor en http://localhost:8000")
    print("📊 Dashboard disponible en: http://localhost:8000/")
    print("🤖 Chat con Carlos en: http://localhost:8000/api/chat")
    print("📈 API Dashboard en: http://localhost:8000/api/dashboard")
    print("❤️ Health Check en: http://localhost:8000/health")
    print("=" * 50)
    print("✅ SERVIDOR LISTO CON DATOS REALES DE GOOGLE SHEETS")
    print("Presiona Ctrl+C para detener")
    
    # Iniciar servidor
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info",
        reload=False
    )
    
except KeyboardInterrupt:
    print("\n👋 Servidor detenido por el usuario")
except Exception as e:
    print(f"❌ Error iniciando servidor: {e}")
    import traceback
    traceback.print_exc()

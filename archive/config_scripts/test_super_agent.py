#!/usr/bin/env python3
"""
🧪 TEST DEL SUPER AGENTE INTELIGENTE
===================================

Script para probar las capacidades del nuevo agente unificado
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Cargar variables de entorno
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ python-dotenv no disponible, usando variables del sistema")

def test_super_agent():
    """Probar el super agente inteligente"""
    
    print("🧠 PROBANDO SUPER AGENTE INTELIGENTE")
    print("=" * 50)
    
    try:
        # Importar servicios
        from backend.app.services.sheets.service import SheetsServiceV2
        from backend.app.services.super_agent_final import SuperIntelligentAgent
        
        # Inicializar servicios
        print("📊 Inicializando servicio de Sheets...")
        sheets_service = SheetsServiceV2()
        
        print("🧠 Inicializando Super Agente...")
        agent = SuperIntelligentAgent(sheets_service)
        
        print("✅ Servicios inicializados correctamente\n")
        
        # Tests específicos
        test_queries = [
            "cliente: Juan Pérez, 5551234567, Centro",
            "prospecto: María García, 5559876543, Norte", 
            "buscar Juan",
            "estadísticas del negocio",
            "análisis financiero",
            "listar todos los clientes",
            "problema con internet en zona sur",
            "ayuda"
        ]
        
        print("🔬 EJECUTANDO TESTS:")
        print("-" * 30)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🔹 Test {i}: '{query}'")
            
            try:
                response = agent.process_query(query)
                
                print(f"   📤 Respuesta: {response['response']}")
                print(f"   🎯 Tipo: {response['action_type']}")
                print(f"   ✨ Confianza: {response['confidence']:.2f}")
                
                if response['data']:
                    print(f"   📊 Datos: {list(response['data'].keys())}")
                
                print(f"   💡 Sugerencias: {response['suggestions']}")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print("\n" + "=" * 50)
        print("✅ TESTS COMPLETADOS")
        
        # Test interactivo
        print("\n🎮 MODO INTERACTIVO (escribe 'salir' para terminar)")
        print("-" * 40)
        
        while True:
            try:
                user_input = input("\n💬 Tú: ").strip()
                
                if user_input.lower() in ['salir', 'exit', 'quit']:
                    break
                
                if not user_input:
                    continue
                
                response = agent.process_query(user_input)
                print(f"🤖 Agente: {response['response']}")
                
                if response['suggestions']:
                    print(f"💡 Sugerencias: {', '.join(response['suggestions'])}")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print("\n👋 ¡Hasta luego!")
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Asegúrate de estar en el directorio correcto")
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()

def check_environment():
    """Verificar configuración del entorno"""
    
    print("🔍 VERIFICANDO CONFIGURACIÓN")
    print("=" * 30)
    
    # Verificar variables de entorno
    required_vars = ["GOOGLE_SHEET_ID", "GEMINI_API_KEY"]
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {'*' * (len(value) - 10)}{value[-10:]}")
        else:
            print(f"❌ {var}: NO CONFIGURADA")
    
    # Verificar archivos
    service_account = Path("service_account.json")
    if service_account.exists():
        print("✅ service_account.json: ENCONTRADO")
    else:
        print("❌ service_account.json: NO ENCONTRADO")
    
    print()

if __name__ == "__main__":
    print("🚀 INICIANDO TESTS DEL SUPER AGENTE")
    print("🏢 Red Soluciones ISP - Sistema Unificado")
    print("=" * 50)
    
    check_environment()
    test_super_agent()

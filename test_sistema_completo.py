#!/usr/bin/env python3
"""
🧪 PRUEBA COMPLETA DEL SISTEMA MODERNO
====================================

Script para verificar que todo el sistema funciona correctamente.
"""

import asyncio
import os
import sys
from datetime import datetime

# Agregar path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def print_result(test_name, success, details=""):
    status = "✅" if success else "❌"
    print(f"{status} {test_name}")
    if details:
        print(f"   💡 {details}")

async def test_complete_system():
    """🧪 Prueba completa del sistema"""
    
    print("🚀 INICIANDO PRUEBAS DEL SISTEMA MODERNO")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # Test 1: Importaciones
    print_header("VERIFICANDO IMPORTACIONES")
    try:
        from backend.app.services.modern_agent_v2 import ModernISPAgent, AgentConfig
        from messaging.modern_telegram_bot import ModernTelegramBot  
        from messaging.modern_launcher import launch_modern_system
        print_result("Importaciones", True, "Todos los módulos disponibles")
        results.append(("Importaciones", True))
    except Exception as e:
        print_result("Importaciones", False, str(e))
        results.append(("Importaciones", False))
        return results
    
    # Test 2: Configuración del agente
    print_header("CONFIGURACIÓN DEL AGENTE")
    try:
        config = AgentConfig(
            name="Carlos",
            role="Empleado Administrativo ISP",
            company="Red Soluciones",
            personality="profesional, leal, eficiente y confiable",
            response_style="como empleado que ayuda al jefe del ISP"
        )
        
        agent = ModernISPAgent(config=config)
        
        print_result("Agente creado", True, f"Nombre: {config.name}, Rol: {config.role}")
        results.append(("Configuración", True))
    except Exception as e:
        print_result("Agente creado", False, str(e))
        results.append(("Configuración", False))
        return results
    
    # Test 3: Procesamiento de mensajes
    print_header("PROCESAMIENTO DE MENSAJES")
    test_messages = [
        ("Saludo", "Hola Carlos", "greeting"),
        ("Estadísticas", "Dame las estadísticas del negocio", "stats"),
        ("Búsqueda", "Busca el cliente María García", "search_client"),
        ("Información", "¿Qué servicios ofrecemos?", "service_info")
    ]
    
    message_results = []
    for test_name, message, expected_intent in test_messages:
        try:
            response = await agent.process_message("test_user", message, "Jefe")
            intent_correct = response["intent"] == expected_intent
            
            print(f"  🔸 {test_name}:")
            print(f"     👤 Entrada: '{message}'")
            print(f"     🤖 Respuesta: '{response['text'][:50]}...'")
            print(f"     🎯 Intención: {response['intent']} (esperada: {expected_intent})")
            print(f"     📊 Confianza: {response['confidence']:.2f}")
            
            status = "✅" if intent_correct else "⚠️"
            print(f"     {status} {'Correcto' if intent_correct else 'Intención diferente'}")
            
            message_results.append(intent_correct)
            
        except Exception as e:
            print(f"  ❌ {test_name}: Error - {e}")
            message_results.append(False)
    
    messages_success = all(message_results)
    print_result("Procesamiento de mensajes", messages_success, 
                f"{sum(message_results)}/{len(message_results)} mensajes procesados correctamente")
    results.append(("Mensajes", messages_success))
    
    # Test 4: Estadísticas del agente
    print_header("ESTADÍSTICAS DEL AGENTE")
    try:
        stats = agent.get_user_stats()
        print(f"  📊 Contextos totales: {stats['total_contexts']}")
        print(f"  🟢 Usuarios activos (24h): {stats['active_24h']}")
        print(f"  🧠 IA disponible: {stats['ai_available']}")
        
        print_result("Estadísticas", True, "Métricas obtenidas correctamente")
        results.append(("Estadísticas", True))
    except Exception as e:
        print_result("Estadísticas", False, str(e))
        results.append(("Estadísticas", False))
    
    # Test 5: Verificar archivos del sistema
    print_header("ARCHIVOS DEL SISTEMA")
    required_files = [
        "backend/app/services/modern_agent_v2.py",
        "messaging/modern_telegram_bot.py", 
        "messaging/modern_launcher.py",
        "demo_agente_moderno.py",
        "README_AGENTE_MODERNO.md"
    ]
    
    files_ok = 0
    for file_path in required_files:
        if os.path.exists(file_path):
            print_result(f"Archivo {file_path}", True)
            files_ok += 1
        else:
            print_result(f"Archivo {file_path}", False, "No encontrado")
    
    files_success = files_ok == len(required_files)
    results.append(("Archivos", files_success))
    
    # Resumen final
    print_header("RESUMEN DE PRUEBAS")
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} {test_name}")
    
    print(f"\n🎯 RESULTADO FINAL: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("✨ Carlos está listo para ayudarte como empleado administrativo")
    else:
        print("⚠️ Algunas pruebas fallaron - revisar detalles arriba")
    
    return results

async def main():
    """🎯 Función principal"""
    try:
        results = await test_complete_system()
        
        # Código de salida
        passed = sum(1 for _, success in results if success)
        total = len(results)
        
        if passed == total:
            print("\n🚀 Sistema listo para producción!")
            return 0
        else:
            print(f"\n⚠️ {total - passed} problemas encontrados")
            return 1
            
    except Exception as e:
        print(f"\n❌ Error crítico en las pruebas: {e}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

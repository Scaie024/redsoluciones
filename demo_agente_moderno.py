#!/usr/bin/env python3
"""
🚀 DEMO DEL AGENTE MODERNO 2025
==============================

Demostración interactiva del nuevo agente conversacional
"""

import asyncio
import sys
import os

# Agregar path del proyecto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from backend.app.services.modern_agent_v2 import ModernISPAgent, AgentConfig
    from backend.app.services.sheets.service import SheetsServiceV2
except ImportError as e:
    print(f"❌ Error importando: {e}")
    print("💡 Ejecuta desde el directorio raíz del proyecto")
    sys.exit(1)

class AgentDemo:
    """🎭 Demo interactivo del agente"""
    
    def __init__(self):
        print("🚀 Inicializando demo del agente moderno...")
        
        # Configurar el agente
        config = AgentConfig(
            name="Carlos",
            role="Empleado Administrativo ISP",  
            company="Red Soluciones",
            experience_years=5,
            personality="profesional, leal, eficiente y confiable",
            response_style="como empleado que ayuda al jefe del ISP",
            max_response_length=300,
            use_emojis=True
        )
        
        # Inicializar servicios
        try:
            sheets_service = SheetsServiceV2()
            print("✅ Google Sheets conectado")
        except Exception as e:
            print(f"⚠️ Google Sheets no disponible: {e}")
            sheets_service = None
            
        self.agent = ModernISPAgent(sheets_service, config)
        
        print(f"✅ Agente {self.agent.config.name} listo")
        print(f"🧠 IA: {'✅ Gemini activo' if self.agent.ai_model else '⚠️ Sin IA (respuestas básicas)'}")
        print()

    async def demo_conversation(self):
        """💬 Demo de conversación"""
        print("="*60)
        print("🎭 DEMO DE CONVERSACIÓN INTERACTIVA")
        print("="*60)
        print()
        print("💡 Ejemplos de lo que puedes preguntar:")
        print("   • 'Hola'")
        print("   • '¿Cómo van las estadísticas?'")
        print("   • 'Buscar cliente Juan'")
        print("   • 'Problemas de internet'")
        print("   • 'Información de planes'")
        print()
        print("🔥 ¡Habla naturalmente como si fuera un empleado real!")
        print("   (Escribe 'salir' para terminar)")
        print()
        
        user_id = "demo_user"
        
        while True:
            try:
                # Obtener input del usuario
                user_input = input("👤 Tú: ").strip()
                
                if user_input.lower() in ['salir', 'exit', 'quit']:
                    print("👋 ¡Hasta luego!")
                    break
                
                if not user_input:
                    continue
                
                # Procesar con el agente
                print("🤖 Carlos: ", end="", flush=True)
                
                response = await self.agent.process_message(
                    user_id=user_id,
                    message=user_input,
                    user_name="Demo User"
                )
                
                # Mostrar respuesta
                print(response['text'])
                
                # Mostrar info técnica si es útil
                if response['confidence'] < 0.5:
                    print(f"   📊 (Confianza: {response['confidence']:.2f}, Tipo: {response['intent']})")
                
                print()
                
            except KeyboardInterrupt:
                print("\\n👋 Demo terminado")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    async def demo_scenarios(self):
        """🎬 Demo de escenarios específicos"""
        print("="*60)
        print("🎬 DEMO DE ESCENARIOS ESPECÍFICOS")
        print("="*60)
        print()
        
        scenarios = [
            {
                "title": "👋 Saludo inicial",
                "message": "Hola, ¿cómo estás?"
            },
            {
                "title": "📊 Consulta de estadísticas",
                "message": "¿Cómo van las estadísticas del negocio?"
            },
            {
                "title": "🔍 Búsqueda de cliente",
                "message": "buscar cliente María García"
            },
            {
                "title": "🛠️ Soporte técnico",
                "message": "Mi internet está muy lento, ¿me pueden ayudar?"
            },
            {
                "title": "📋 Información de servicios",
                "message": "¿Cuáles son sus planes de internet?"
            },
            {
                "title": "❓ Pregunta ambigua",
                "message": "¿Qué tal todo?"
            }
        ]
        
        user_id = "scenario_user"
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"🎬 **Escenario {i}: {scenario['title']}**")
            print(f"👤 Usuario: \"{scenario['message']}\"")
            print("🤖 Carlos: ", end="", flush=True)
            
            try:
                response = await self.agent.process_message(
                    user_id=user_id,
                    message=scenario['message'],
                    user_name="Test User"
                )
                
                print(response['text'])
                print(f"   📊 Intención: {response['intent']} (Confianza: {response['confidence']:.2f})")
                
                if response.get('suggestions'):
                    print(f"   💡 Sugerencias: {', '.join(response['suggestions'][:3])}")
                
            except Exception as e:
                print(f"❌ Error: {e}")
            
            print()
            print("-" * 60)
            print()

    async def run(self):
        """🚀 Ejecutar demo completo"""
        print("🌟 BIENVENIDO AL DEMO DEL AGENTE MODERNO 2025")
        print()
        
        while True:
            print("¿Qué quieres probar?")
            print("1. 💬 Conversación interactiva")
            print("2. 🎬 Escenarios de prueba")
            print("3. 📊 Estadísticas del agente")
            print("4. 🚪 Salir")
            print()
            
            choice = input("Elige una opción (1-4): ").strip()
            
            if choice == "1":
                await self.demo_conversation()
            elif choice == "2":
                await self.demo_scenarios()
            elif choice == "3":
                self.show_agent_stats()
            elif choice == "4":
                print("👋 ¡Gracias por probar el agente!")
                break
            else:
                print("❌ Opción inválida")
            
            print()

    def show_agent_stats(self):
        """📊 Mostrar estadísticas del agente"""
        print("="*60)
        print("📊 ESTADÍSTICAS DEL AGENTE")
        print("="*60)
        
        stats = self.agent.get_user_stats()
        
        print(f"👥 Contextos de usuario: {stats['total_contexts']}")
        print(f"🔥 Usuarios activos (24h): {stats['active_24h']}")
        print(f"🧠 IA disponible: {'✅ Sí' if stats['ai_available'] else '❌ No'}")
        print(f"🤖 Nombre del agente: {self.agent.config.name}")
        print(f"🎭 Personalidad: {self.agent.config.personality}")
        print(f"💬 Estilo: {self.agent.config.response_style}")
        print(f"📏 Máximo caracteres: {self.agent.config.max_response_length}")
        
        print()


async def main():
    """🎯 Función principal"""
    try:
        demo = AgentDemo()
        await demo.run()
    except KeyboardInterrupt:
        print("\\n👋 Demo terminado por el usuario")
    except Exception as e:
        print(f"❌ Error en demo: {e}")

if __name__ == "__main__":
    asyncio.run(main())

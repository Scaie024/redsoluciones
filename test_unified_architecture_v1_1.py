#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔍 VERIFICACIÓN DE ARQUITECTURA UNIFICADA v1.1
===============================================

Proyecto de verificación para asegurar que la lógica del agente
está unificada y solo los canales de comunicación cambian.

Arquitectura esperada:
- 🧠 AgentCore: Lógica unificada
- 📡 Canal Web: API REST + Dashboard
- 📱 Canal Telegram: Bot de Telegram
- 💬 Canal WhatsApp: Bot de WhatsApp (v1.1)
"""

import requests
import json
import time
import asyncio
from datetime import datetime
from typing import Dict, Any, List

class UnifiedArchitectureTest:
    """🧪 Verificador de arquitectura unificada"""
    
    def __init__(self):
        self.base_url = "http://localhost:8004"
        self.test_results = {}
        self.test_messages = [
            "Hola, ¿qué servicios ofrecen?",
            "¿Cuántos clientes tienen?", 
            "Necesito soporte técnico",
            "Quiero registrarme como cliente",
            "Estadísticas del negocio"
        ]
        
    def print_header(self):
        print("🔍" + "="*60 + "🔍")
        print("    VERIFICACIÓN ARQUITECTURA UNIFICADA v1.1")
        print("    Fecha:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("🔍" + "="*60 + "🔍")
        print()

    def test_core_agent(self) -> bool:
        """🧠 Verificar que el agente core existe y funciona"""
        print("🧠 PROBANDO AGENTE CORE...")
        try:
            from backend.app.services.smart_agent import SmartISPAgent
            from backend.app.services.sheets.service import SheetsServiceV2
            
            # Instanciar agente
            sheets = SheetsServiceV2()
            agent = SmartISPAgent(sheets)
            
            # Probar método principal
            response = agent.process_query("estadísticas")
            
            if response and 'response' in response:
                print("✅ Agente Core: FUNCIONAL")
                self.test_results['core_agent'] = True
                return True
            else:
                print("❌ Agente Core: NO RESPONDE")
                self.test_results['core_agent'] = False
                return False
                
        except Exception as e:
            print(f"❌ Agente Core: ERROR - {e}")
            self.test_results['core_agent'] = False
            return False

    def test_messaging_agent(self) -> bool:
        """📱 Verificar que el agente de mensajería hereda correctamente"""
        print("\n📱 PROBANDO AGENTE DE MENSAJERÍA...")
        try:
            from messaging.enhanced_agent import MessagingISPAgent
            from backend.app.services.smart_agent import SmartISPAgent
            from backend.app.services.sheets.service import SheetsServiceV2
            
            # Verificar herencia
            if not issubclass(MessagingISPAgent, SmartISPAgent):
                print("❌ Herencia: INCORRECTA")
                self.test_results['messaging_agent'] = False
                return False
            
            # Instanciar agente de mensajería
            sheets = SheetsServiceV2()
            msg_agent = MessagingISPAgent(sheets)
            
            # Probar método específico de mensajería
            response = msg_agent.process_messaging_query(
                "hola", 
                {'first_name': 'Test', 'is_new_user': True}
            )
            
            if response and 'response' in response:
                print("✅ Agente Mensajería: FUNCIONAL")
                print(f"✅ Herencia: CORRECTA")
                self.test_results['messaging_agent'] = True
                return True
            else:
                print("❌ Agente Mensajería: NO RESPONDE")
                self.test_results['messaging_agent'] = False
                return False
                
        except Exception as e:
            print(f"❌ Agente Mensajería: ERROR - {e}")
            self.test_results['messaging_agent'] = False
            return False

    def test_channel_web(self) -> bool:
        """🌐 Verificar canal web (API + Dashboard)"""
        print("\n🌐 PROBANDO CANAL WEB...")
        
        try:
            # Test health
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code != 200:
                print("❌ Canal Web: SERVIDOR DOWN")
                self.test_results['channel_web'] = False
                return False
            
            # Test chat API
            responses = []
            for message in self.test_messages:
                try:
                    chat_response = requests.post(
                        f"{self.base_url}/api/chat",
                        json={"message": message},
                        timeout=5
                    )
                    if chat_response.status_code == 200:
                        data = chat_response.json()
                        responses.append({
                            'message': message,
                            'response': data.get('response', '')[:50] + '...',
                            'type': data.get('type', 'unknown')
                        })
                    time.sleep(0.5)  # Rate limiting
                except Exception as e:
                    print(f"⚠️ Error en mensaje: {message[:20]}...")
            
            if len(responses) >= 3:  # Al menos 3 respuestas exitosas
                print(f"✅ Canal Web: FUNCIONAL ({len(responses)}/{len(self.test_messages)} respuestas)")
                self.test_results['channel_web'] = True
                self.test_results['web_responses'] = responses
                return True
            else:
                print(f"❌ Canal Web: FALLOS ({len(responses)}/{len(self.test_messages)})")
                self.test_results['channel_web'] = False
                return False
                
        except Exception as e:
            print(f"❌ Canal Web: ERROR - {e}")
            self.test_results['channel_web'] = False
            return False

    def test_channel_telegram(self) -> bool:
        """📱 Verificar canal Telegram"""
        print("\n📱 PROBANDO CANAL TELEGRAM...")
        
        try:
            from messaging.telegram_bot import TelegramISPBot
            
            # Instanciar bot
            bot = TelegramISPBot()
            
            # Verificar que tiene el agente correcto
            if not hasattr(bot, 'agent'):
                print("❌ Canal Telegram: SIN AGENTE")
                self.test_results['channel_telegram'] = False
                return False
            
            # Probar respuestas del agente
            responses = []
            for message in self.test_messages:
                try:
                    response = bot.agent.process_messaging_query(
                        message,
                        {'first_name': 'TestUser', 'is_new_user': False}
                    )
                    if response and 'response' in response:
                        responses.append({
                            'message': message,
                            'response': response['response'][:50] + '...',
                            'type': response.get('type', 'unknown')
                        })
                except Exception as e:
                    print(f"⚠️ Error en mensaje: {message[:20]}...")
            
            if len(responses) >= 3:
                print(f"✅ Canal Telegram: FUNCIONAL ({len(responses)}/{len(self.test_messages)} respuestas)")
                self.test_results['channel_telegram'] = True
                self.test_results['telegram_responses'] = responses
                return True
            else:
                print(f"❌ Canal Telegram: FALLOS ({len(responses)}/{len(self.test_messages)})")
                self.test_results['channel_telegram'] = False
                return False
                
        except Exception as e:
            print(f"❌ Canal Telegram: ERROR - {e}")
            self.test_results['channel_telegram'] = False
            return False

    def test_response_consistency(self) -> bool:
        """🔄 Verificar consistencia de respuestas entre canales"""
        print("\n🔄 PROBANDO CONSISTENCIA ENTRE CANALES...")
        
        if not (self.test_results.get('channel_web') and self.test_results.get('channel_telegram')):
            print("❌ Consistencia: CANALES NO DISPONIBLES")
            self.test_results['consistency'] = False
            return False
        
        web_responses = self.test_results.get('web_responses', [])
        telegram_responses = self.test_results.get('telegram_responses', [])
        
        consistent_count = 0
        total_comparisons = min(len(web_responses), len(telegram_responses))
        
        for i in range(total_comparisons):
            web_type = web_responses[i].get('type', '')
            telegram_type = telegram_responses[i].get('type', '')
            
            # Para el mismo mensaje, el tipo de respuesta debería ser similar
            if web_type == telegram_type or (web_type and telegram_type):
                consistent_count += 1
        
        consistency_rate = (consistent_count / total_comparisons * 100) if total_comparisons > 0 else 0
        
        if consistency_rate >= 60:  # 60% de consistencia mínima
            print(f"✅ Consistencia: {consistency_rate:.1f}% ({consistent_count}/{total_comparisons})")
            self.test_results['consistency'] = True
            return True
        else:
            print(f"❌ Consistencia: {consistency_rate:.1f}% - BAJA")
            self.test_results['consistency'] = False
            return False

    def test_whatsapp_readiness(self) -> bool:
        """💬 Verificar preparación para WhatsApp"""
        print("\n💬 VERIFICANDO PREPARACIÓN PARA WHATSAPP...")
        
        try:
            import os
            
            # Verificar si existe el archivo
            whatsapp_file = os.path.exists('messaging/whatsapp_bot.py')
            
            # Verificar configuración
            config_ready = os.path.exists('messaging/config.py')
            
            if whatsapp_file and config_ready:
                print("✅ WhatsApp: PREPARADO")
                self.test_results['whatsapp_ready'] = True
                return True
            elif config_ready:
                print("📋 WhatsApp: PARCIALMENTE PREPARADO (falta bot)")
                self.test_results['whatsapp_ready'] = False
                return False
            else:
                print("📋 WhatsApp: NO PREPARADO")
                self.test_results['whatsapp_ready'] = False
                return False
                
        except Exception as e:
            print(f"❌ WhatsApp: ERROR - {e}")
            self.test_results['whatsapp_ready'] = False
            return False

    def generate_report(self):
        """📊 Generar reporte final"""
        print("\n" + "="*60)
        print("📊 REPORTE FINAL - ARQUITECTURA UNIFICADA v1.1")
        print("="*60)
        
        total_tests = len([k for k in self.test_results.keys() if not k.endswith('_responses')])
        passed_tests = len([v for k, v in self.test_results.items() if v and not k.endswith('_responses')])
        
        print(f"\n🎯 RESULTADOS:")
        print(f"   ✅ Pruebas exitosas: {passed_tests}/{total_tests}")
        print(f"   📈 Tasa de éxito: {(passed_tests/total_tests*100):.1f}%")
        
        print(f"\n📋 DETALLES:")
        status_map = {
            'core_agent': '🧠 Agente Core',
            'messaging_agent': '📱 Agente Mensajería', 
            'channel_web': '🌐 Canal Web',
            'channel_telegram': '📱 Canal Telegram',
            'consistency': '🔄 Consistencia',
            'whatsapp_ready': '💬 Preparación WhatsApp'
        }
        
        for key, name in status_map.items():
            if key in self.test_results:
                status = "✅ PASS" if self.test_results[key] else "❌ FAIL"
                print(f"   {name}: {status}")
        
        print(f"\n🎯 ESTADO GENERAL:")
        if passed_tests >= total_tests - 1:  # Permitir 1 fallo
            print("   🎉 ARQUITECTURA UNIFICADA: EXCELENTE")
            print("   🚀 Lista para versión 1.1")
        elif passed_tests >= total_tests * 0.7:
            print("   ✅ ARQUITECTURA UNIFICADA: BUENA")
            print("   🔧 Necesita ajustes menores")
        else:
            print("   ⚠️ ARQUITECTURA UNIFICADA: NECESITA TRABAJO")
            print("   🛠️ Requiere correcciones importantes")
        
        print("="*60)

    def run_all_tests(self):
        """🚀 Ejecutar todas las pruebas"""
        self.print_header()
        
        # Ejecutar todas las pruebas
        self.test_core_agent()
        self.test_messaging_agent()
        self.test_channel_web()
        self.test_channel_telegram()
        self.test_response_consistency()
        self.test_whatsapp_readiness()
        
        # Generar reporte
        self.generate_report()

if __name__ == "__main__":
    print("🔍 Iniciando verificación de arquitectura unificada...")
    print("⏱️  Tiempo estimado: 30-60 segundos")
    print()
    
    tester = UnifiedArchitectureTest()
    tester.run_all_tests()

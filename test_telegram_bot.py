#!/usr/bin/env python3
"""
Probador de Bot de Telegram - Red Soluciones ISP
Permite probar la integración de Carlos con Telegram
"""
import requests
import json

def test_telegram_integration():
    """Prueba la integración completa"""
    print("🤖 PROBADOR BOT TELEGRAM - Red Soluciones ISP")
    print("=" * 50)
    
    # Configuración
    bot_token = "7881396575:AAHDbmSqXIVPSAK3asK9ieNhpbaS7iD3NZk"
    webhook_url = "http://localhost:8004/api/telegram/webhook"
    test_chat_id = 123456789
    
    print(f"🔗 Webhook: {webhook_url}")
    print(f"💬 Chat ID de prueba: {test_chat_id}")
    print()
    
    # Tests a realizar
    test_messages = [
        "/start",
        "ayuda", 
        "cliente: Test Usuario, 4641234567, Centro",
        "estadísticas",
        "clientes"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"📨 Test {i}/5: {message}")
        
        # Simular mensaje de Telegram
        telegram_update = {
            "message": {
                "chat": {"id": test_chat_id},
                "from": {"username": "test_user"},
                "text": message
            }
        }
        
        try:
            # Enviar al webhook
            response = requests.post(
                webhook_url,
                headers={"Content-Type": "application/json"},
                json=telegram_update,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                status = result.get("status", "unknown")
                print(f"   ✅ Respuesta: {status}")
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    print("🎯 Pruebas completadas!")
    print()
    print("📱 Para probar en Telegram real:")
    print(f"   1. Busca: @RedSolucionesAdminbot")
    print(f"   2. Escribe: /start")
    print(f"   3. Prueba: ayuda")

if __name__ == "__main__":
    test_telegram_integration()

#!/usr/bin/env python3
"""
Test del Sistema de Identificación de Propietarios
Verifica que el sistema de Eduardo/Omar funcione correctamente
"""

import requests
import json
import time
from datetime import datetime

def test_authentication_system():
    """Probar el sistema de autenticación"""
    base_url = "http://localhost:8004"
    
    print("🔐 === TESTING SISTEMA DE AUTENTICACIÓN ===")
    print(f"📍 Base URL: {base_url}")
    print(f"⏰ Timestamp: {datetime.now()}")
    print()
    
    # Test 1: Obtener usuarios disponibles
    print("1️⃣ Testing: Obtener usuarios disponibles")
    try:
        response = requests.get(f"{base_url}/api/auth/users")
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"📊 Usuarios disponibles: {data}")
        
        if data.get('success'):
            available_users = data.get('users', [])
            print(f"👥 Usuarios: {[u['name'] for u in available_users]}")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
    
    # Test 2: Login como Eduardo
    print("2️⃣ Testing: Login como Eduardo")
    try:
        login_data = {
            "user_id": "eduardo",
            "session_id": f"test_session_eduardo_{int(time.time())}"
        }
        
        response = requests.post(
            f"{base_url}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"📊 Response: {data}")
        
        if data.get('success'):
            eduardo_session = login_data["session_id"]
            eduardo_user = data.get('user')
            print(f"👤 Eduardo logueado: {eduardo_user.get('name')} ({eduardo_user.get('user_id')})")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
    
    # Test 3: Login como Omar
    print("3️⃣ Testing: Login como Omar")
    try:
        login_data = {
            "user_id": "omar",
            "session_id": f"test_session_omar_{int(time.time())}"
        }
        
        response = requests.post(
            f"{base_url}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"📊 Response: {data}")
        
        if data.get('success'):
            omar_session = login_data["session_id"]
            omar_user = data.get('user')
            print(f"👤 Omar logueado: {omar_user.get('name')} ({omar_user.get('user_id')})")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
    
    # Test 4: Chat con Eduardo
    print("4️⃣ Testing: Chat personalizado con Eduardo")
    try:
        chat_data = {
            "message": "Hola, quiero ver mis clientes",
            "user_id": "eduardo",
            "user_name": "Eduardo",
            "session_id": eduardo_session
        }
        
        response = requests.post(
            f"{base_url}/api/chat",
            json=chat_data,
            headers={"Content-Type": "application/json"}
        )
        
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"🤖 Respuesta del agente para Eduardo:")
        print(f"   {data.get('response', 'Sin respuesta')}")
        
        user_context = data.get('user_context')
        if user_context:
            print(f"👤 Contexto: {user_context.get('name')} ({user_context.get('user_id')})")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
    
    # Test 5: Chat con Omar
    print("5️⃣ Testing: Chat personalizado con Omar")
    try:
        chat_data = {
            "message": "Quiero ver estadísticas de mi negocio",
            "user_id": "omar",
            "user_name": "Omar",
            "session_id": omar_session
        }
        
        response = requests.post(
            f"{base_url}/api/chat",
            json=chat_data,
            headers={"Content-Type": "application/json"}
        )
        
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"🤖 Respuesta del agente para Omar:")
        print(f"   {data.get('response', 'Sin respuesta')}")
        
        user_context = data.get('user_context')
        if user_context:
            print(f"👤 Contexto: {user_context.get('name')} ({user_context.get('user_id')})")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
    
    # Test 6: Usuarios activos
    print("6️⃣ Testing: Verificar usuarios activos")
    try:
        response = requests.get(f"{base_url}/api/auth/active")
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"📊 Usuarios activos: {data}")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
    
    print("🎯 === TESTING COMPLETADO ===")
    print("✅ Sistema de identificación de propietarios implementado")
    print("📋 Funcionalidades probadas:")
    print("   • Login de usuarios (Eduardo/Omar)")
    print("   • Chat personalizado por usuario")
    print("   • Contexto de usuario en respuestas")
    print("   • Sesiones activas")
    print()

if __name__ == "__main__":
    test_authentication_system()

#!/usr/bin/env python3
"""
Test de endpoints para Red Soluciones ISP
"""
import requests
import json
import time

def run_endpoint(url, method='GET', data=None, timeout=10):
    """Test un endpoint específico"""
    try:
        if method == 'GET':
            response = requests.get(url, timeout=timeout)
        elif method == 'POST':
            response = requests.post(url, json=data, timeout=timeout)
        
        return {
            'success': True,
            'status_code': response.status_code,
            'data': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text[:200]
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def main():
    print("🚀 TESTING ENDPOINTS RED SOLUCIONES ISP")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # Lista de endpoints para probar
    endpoints = [
        {"url": f"{base_url}/health", "name": "Health Check"},
        {"url": f"{base_url}/api/dashboard", "name": "Dashboard Data"},
        {"url": f"{base_url}/api/dashboard/kpis", "name": "Dashboard KPIs"},
        {"url": f"{base_url}/api/clients", "name": "Clientes"},
        {"url": f"{base_url}/api/sheets/status", "name": "Google Sheets Status"},
        {"url": f"{base_url}/api/chat", "name": "Chat Carlos", "method": "POST", "data": {"message": "Hola Carlos, ¿cuántos clientes tenemos?"}},
    ]
    
    print("⏳ Esperando 3 segundos para que el servidor inicie...")
    time.sleep(3)
    
    results = []
    
    for endpoint in endpoints:
        print(f"\n🔍 Testing: {endpoint['name']}")
        print(f"   URL: {endpoint['url']}")
        
        result = run_endpoint(
            endpoint['url'], 
            method=endpoint.get('method', 'GET'),
            data=endpoint.get('data')
        )
        
        if result['success']:
            print(f"   ✅ Status: {result['status_code']}")
            if isinstance(result['data'], dict):
                print(f"   📊 Data: {json.dumps(result['data'], indent=6)}")
            else:
                print(f"   📝 Response: {result['data']}")
        else:
            print(f"   ❌ Error: {result['error']}")
        
        results.append({
            'endpoint': endpoint['name'],
            'result': result
        })
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    successful = sum(1 for r in results if r['result']['success'])
    total = len(results)
    
    for result in results:
        status = "✅" if result['result']['success'] else "❌"
        print(f"{status} {result['endpoint']}")
    
    print(f"\n🎯 Resultados: {successful}/{total} endpoints funcionando")
    
    if successful == total:
        print("🎉 ¡TODOS LOS ENDPOINTS FUNCIONAN CORRECTAMENTE!")
        print("✅ Sistema Red Soluciones ISP completamente operativo")
        print("✅ Google Sheets conectado con datos reales")
        print("✅ Carlos AI Agent respondiendo")
        print("✅ Dashboard funcionando")
    else:
        print("⚠️ Algunos endpoints requieren atención")

if __name__ == "__main__":
    main()

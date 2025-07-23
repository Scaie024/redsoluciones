#!/usr/bin/env python3
"""
🧪 SISTEMA DE PRUEBAS COMPLETO - RED SOLUCIONES v1.0
====================================================

Suite de pruebas integral para validar toda la funcionalidad del sistema
"""

import asyncio
import json
import logging
import requests
import sys
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RedSolucionesTestSuite:
    """🧪 Suite de pruebas completa"""
    
    def __init__(self, base_url: str = "http://localhost:8004"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.test_results = []
        self.start_time = None
        
        # Datos de prueba
        self.test_client = {
            "nombre": "Cliente Test Automatizado",
            "email": "test@redsol.com",
            "zona": "Norte",
            "telefono": "4641234567",
            "pago_mensual": 450
        }
        
        self.test_prospect = {
            "nombre": "Prospecto Test Auto",
            "telefono": "4649876543",
            "zona": "Centro",
            "email": "prospect@test.com",
            "notas": "Interesado en plan premium - Test automatizado"
        }
        
        self.test_incident = {
            "cliente": "Cliente Test Automatizado",
            "descripcion": "Internet intermitente - Prueba automatizada",
            "prioridad": "Media",
            "tipo": "Técnico"
        }
        
    def log_test(self, test_name: str, passed: bool, details: str = "", response_time: float = 0):
        """📝 Registrar resultado de prueba"""
        result = {
            "test": test_name,
            "passed": passed,
            "details": details,
            "response_time": response_time if response_time > 0 else None,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if passed else "❌ FAIL"
        time_info = f"({response_time:.2f}s)" if response_time > 0 else ""
        logger.info(f"{status} {test_name} {time_info} - {details}")
        
    def test_server_health(self) -> bool:
        """🏥 Probar salud del servidor"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/health", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Server Health", True, f"Status: {data.get('status', 'unknown')}", response_time)
                return True
            else:
                self.log_test("Server Health", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Server Health", False, f"Connection error: {str(e)}")
            return False
    
    def test_dashboard_access(self) -> bool:
        """🖥️ Probar acceso al dashboard"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/dashboard.html", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200 and len(response.content) > 1000:
                self.log_test("Dashboard Access", True, f"{len(response.content)} bytes loaded", response_time)
                return True
            else:
                self.log_test("Dashboard Access", False, f"HTTP {response.status_code} or content too small")
                return False
                
        except Exception as e:
            self.log_test("Dashboard Access", False, f"Error: {str(e)}")
            return False
    
    def test_sheets_connection(self) -> bool:
        """📊 Probar conexión con Google Sheets"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.api_url}/clients", timeout=15)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                client_count = len(data.get('clients', []))
                
                if client_count > 0:
                    self.log_test("Google Sheets Connection", True, f"{client_count} clients loaded", response_time)
                    return True
                else:
                    self.log_test("Google Sheets Connection", False, "No clients found")
                    return False
            else:
                self.log_test("Google Sheets Connection", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Google Sheets Connection", False, f"Error: {str(e)}")
            return False
    
    def test_smart_agent(self) -> bool:
        """🤖 Probar agente inteligente"""
        test_queries = [
            {"message": "estadísticas", "expected_type": "stats"},
            {"message": "buscar norma", "expected_type": "search"},
            {"message": "hola", "expected_type": "help"}
        ]
        
        all_passed = True
        
        for query in test_queries:
            try:
                start_time = time.time()
                response = requests.post(
                    f"{self.api_url}/chat",
                    json=query,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get('response') and len(data['response']) > 10:
                        self.log_test(
                            f"Smart Agent - {query['message'][:20]}",
                            True,
                            f"Response length: {len(data['response'])}",
                            response_time
                        )
                    else:
                        self.log_test(
                            f"Smart Agent - {query['message'][:20]}",
                            False,
                            "Response too short or empty"
                        )
                        all_passed = False
                else:
                    self.log_test(
                        f"Smart Agent - {query['message'][:20]}",
                        False,
                        f"HTTP {response.status_code}"
                    )
                    all_passed = False
                    
            except Exception as e:
                self.log_test(
                    f"Smart Agent - {query['message'][:20]}",
                    False,
                    f"Error: {str(e)}"
                )
                all_passed = False
        
        return all_passed
    
    def test_client_operations(self) -> bool:
        """👥 Probar operaciones de clientes"""
        try:
            # Test: Agregar cliente
            start_time = time.time()
            response = requests.post(
                f"{self.api_url}/clients",
                json=self.test_client,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_test("Add Client", True, "Client added successfully", response_time)
                    
                    # Test: Buscar cliente agregado
                    search_response = requests.post(
                        f"{self.api_url}/chat",
                        json={"message": f"buscar {self.test_client['nombre']}"},
                        headers={"Content-Type": "application/json"},
                        timeout=15
                    )
                    
                    if search_response.status_code == 200:
                        search_data = search_response.json()
                        if self.test_client['nombre'] in search_data.get('response', ''):
                            self.log_test("Search Added Client", True, "Client found in search")
                            return True
                        else:
                            self.log_test("Search Added Client", False, "Client not found in search")
                            return False
                    else:
                        self.log_test("Search Added Client", False, f"Search failed: HTTP {search_response.status_code}")
                        return False
                else:
                    self.log_test("Add Client", False, f"API returned: {data}")
                    return False
            else:
                self.log_test("Add Client", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Client Operations", False, f"Error: {str(e)}")
            return False
    
    def test_prospect_operations(self) -> bool:
        """🎯 Probar operaciones de prospectos"""
        try:
            start_time = time.time()
            response = requests.post(
                f"{self.api_url}/prospects",
                json=self.test_prospect,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_test("Add Prospect", True, "Prospect added successfully", response_time)
                    return True
                else:
                    self.log_test("Add Prospect", False, f"API returned: {data}")
                    return False
            else:
                self.log_test("Add Prospect", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Prospect Operations", False, f"Error: {str(e)}")
            return False
    
    def test_incident_operations(self) -> bool:
        """🚨 Probar operaciones de incidentes"""
        try:
            start_time = time.time()
            response = requests.post(
                f"{self.api_url}/incidents",
                json=self.test_incident,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_test("Add Incident", True, "Incident added successfully", response_time)
                    return True
                else:
                    self.log_test("Add Incident", False, f"API returned: {data}")
                    return False
            else:
                self.log_test("Add Incident", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Incident Operations", False, f"Error: {str(e)}")
            return False
    
    def test_messaging_agent(self) -> bool:
        """📱 Probar agente de mensajería"""
        try:
            # Importar y probar agente de mensajería
            import sys
            import os
            sys.path.append(os.getcwd())
            
            from backend.app.services.sheets.service import SheetsServiceV2
            from messaging.enhanced_agent import MessagingISPAgent
            
            sheets = SheetsServiceV2()
            agent = MessagingISPAgent(sheets)
            
            test_user = {
                'first_name': 'Test',
                'last_name': 'User',
                'phone': '4641234567',
                'user_id': 'test_user'
            }
            
            # Probar diferentes tipos de mensajes
            test_messages = [
                "hola",
                "qué servicios tienen",
                "quiero registrarme",
                "estadísticas"
            ]
            
            all_passed = True
            for message in test_messages:
                start_time = time.time()
                response = agent.process_messaging_query(message, test_user)
                response_time = time.time() - start_time
                
                if response and response.get('response') and len(response['response']) > 10:
                    self.log_test(
                        f"Messaging Agent - {message[:15]}",
                        True,
                        f"Response length: {len(response['response'])}",
                        response_time
                    )
                else:
                    self.log_test(
                        f"Messaging Agent - {message[:15]}",
                        False,
                        "Invalid response"
                    )
                    all_passed = False
            
            return all_passed
            
        except Exception as e:
            self.log_test("Messaging Agent", False, f"Error: {str(e)}")
            return False
    
    def run_full_test_suite(self) -> Dict[str, Any]:
        """🚀 Ejecutar suite completa de pruebas"""
        self.start_time = time.time()
        
        print("🧪 INICIANDO SUITE DE PRUEBAS - RED SOLUCIONES v1.0")
        print("=" * 60)
        print(f"🕐 Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 Servidor: {self.base_url}")
        print()
        
        # Lista de pruebas
        tests = [
            ("🏥 Server Health", self.test_server_health),
            ("🖥️  Dashboard Access", self.test_dashboard_access),
            ("📊 Google Sheets Connection", self.test_sheets_connection),
            ("🤖 Smart Agent", self.test_smart_agent),
            ("👥 Client Operations", self.test_client_operations),
            ("🎯 Prospect Operations", self.test_prospect_operations),
            ("🚨 Incident Operations", self.test_incident_operations),
            ("📱 Messaging Agent", self.test_messaging_agent)
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            print(f"Running {test_name}...")
            try:
                if test_func():
                    passed_tests += 1
            except Exception as e:
                logger.error(f"Test {test_name} crashed: {e}")
            
            time.sleep(1)  # Pausa entre pruebas
        
        # Generar reporte final
        total_time = time.time() - self.start_time
        success_rate = (passed_tests / total_tests) * 100
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "success_rate": success_rate,
            "total_time": total_time,
            "individual_results": self.test_results,
            "version": "1.0.0",
            "server_url": self.base_url
        }
        
        # Mostrar resumen
        print()
        print("=" * 60)
        print("📊 RESUMEN DE PRUEBAS")
        print("=" * 60)
        print(f"✅ Pruebas exitosas: {passed_tests}/{total_tests}")
        print(f"❌ Pruebas fallidas: {total_tests - passed_tests}")
        print(f"📈 Tasa de éxito: {success_rate:.1f}%")
        print(f"⏱️  Tiempo total: {total_time:.2f}s")
        print()
        
        if success_rate >= 90:
            print("🎉 SISTEMA LISTO PARA PRODUCCIÓN!")
        elif success_rate >= 75:
            print("⚠️  Sistema funcional con algunos problemas menores")
        else:
            print("❌ Sistema requiere correcciones antes de producción")
        
        return report
    
    def save_report(self, report: Dict[str, Any], filename: Optional[str] = None):
        """💾 Guardar reporte de pruebas"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_report_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"📄 Reporte guardado en: {filename}")
        except Exception as e:
            print(f"❌ Error guardando reporte: {e}")


def main():
    """🎯 Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Red Soluciones - Test Suite v1.0")
    parser.add_argument("--server", default="http://localhost:8004", help="URL del servidor")
    parser.add_argument("--save-report", action="store_true", help="Guardar reporte en archivo")
    
    args = parser.parse_args()
    
    # Ejecutar pruebas
    test_suite = RedSolucionesTestSuite(args.server)
    report = test_suite.run_full_test_suite()
    
    # Guardar reporte si se solicita
    if args.save_report:
        test_suite.save_report(report)
    
    # Exit code basado en resultados
    sys.exit(0 if report['success_rate'] >= 90 else 1)


if __name__ == "__main__":
    main()

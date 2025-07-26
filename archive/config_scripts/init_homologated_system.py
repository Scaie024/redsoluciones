#!/usr/bin/env python3
"""
🚀 SCRIPT DE INICIALIZACIÓN - Red Soluciones ISP v4.0 Homologado
================================================================

Script para inicializar completamente el sistema homologado:
- Verificar configuración
- Inicializar servicios
- Cargar contexto completo
- Validar conexiones
- Ejecutar pruebas de sistema

Uso:
    python init_homologated_system.py
    python init_homologated_system.py --check-only
    python init_homologated_system.py --reset-cache
"""

import asyncio
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime
import traceback

# Agregar el directorio padre al path para importaciones
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.app.core.homologated_config import settings
from backend.app.services.sheets.service import SheetsServiceV2
from backend.app.services.context_engine import ContextEngine
from backend.app.services.enhanced_agent import HomologatedAIAgent
from backend.app.utils.logger import get_logger

class SystemInitializer:
    """Inicializador completo del sistema homologado"""
    
    def __init__(self):
        self.logger = get_logger("SystemInitializer")
        self.sheets_service = None
        self.context_engine = None
        self.enhanced_agent = None
        self.initialization_results = {}
        
    async def run_full_initialization(self, check_only=False, reset_cache=False):
        """Ejecutar inicialización completa del sistema"""
        
        print("🚀 INICIALIZANDO RED SOLUCIONES ISP v4.0 HOMOLOGADO")
        print("=" * 60)
        
        try:
            # 1. Verificar configuración
            config_result = await self.verify_configuration()
            self.initialization_results['configuration'] = config_result
            
            if not config_result['valid']:
                print("❌ Configuración inválida. No se puede continuar.")
                return False
            
            if check_only:
                print("✅ Verificación de configuración completada exitosamente")
                return True
            
            # 2. Inicializar servicios base
            services_result = await self.initialize_services()
            self.initialization_results['services'] = services_result
            
            if not services_result['success']:
                print("❌ Error inicializando servicios base")
                return False
            
            # 3. Cargar contexto completo
            context_result = await self.load_system_context(reset_cache)
            self.initialization_results['context'] = context_result
            
            # 4. Validar sistema completo
            validation_result = await self.validate_system()
            self.initialization_results['validation'] = validation_result
            
            # 5. Ejecutar pruebas básicas
            tests_result = await self.run_system_tests()
            self.initialization_results['tests'] = tests_result
            
            # 6. Generar reporte final
            await self.generate_initialization_report()
            
            print("\n🎉 SISTEMA HOMOLOGADO INICIALIZADO EXITOSAMENTE")
            return True
            
        except Exception as e:
            self.logger.error(f"Error crítico en inicialización: {e}")
            print(f"❌ Error crítico: {e}")
            traceback.print_exc()
            return False
    
    async def verify_configuration(self):
        """Verificar configuración completa"""
        print("\n📋 Verificando configuración...")
        
        try:
            # Usar validación integrada
            config_validation = settings.validate_config()
            
            # Verificaciones adicionales
            additional_checks = {
                'google_sheets_accessible': await self.check_google_sheets_access(),
                'ai_service_available': self.check_ai_service(),
                'required_directories': self.check_directories(),
                'environment_variables': self.check_environment_variables()
            }
            
            config_validation.update(additional_checks)
            
            # Mostrar resultados
            if config_validation['valid']:
                print("✅ Configuración válida")
                
                if config_validation['warnings']:
                    print("⚠️ Advertencias encontradas:")
                    for warning in config_validation['warnings']:
                        print(f"   • {warning}")
            else:
                print("❌ Problemas de configuración:")
                for issue in config_validation['issues']:
                    print(f"   • {issue}")
            
            return config_validation
            
        except Exception as e:
            self.logger.error(f"Error verificando configuración: {e}")
            return {
                'valid': False,
                'issues': [f"Error verificando configuración: {str(e)}"],
                'warnings': []
            }
    
    async def check_google_sheets_access(self):
        """Verificar acceso a Google Sheets"""
        try:
            # Intentar crear servicio y conectar
            test_service = SheetsServiceV2()
            if hasattr(test_service, 'gc') and test_service.gc:
                # Intentar acceder a la hoja
                if test_service.sheet_id:
                    test_service.gc.open_by_key(test_service.sheet_id)
                    return True
            return False
        except Exception as e:
            self.logger.warning(f"No se pudo acceder a Google Sheets: {e}")
            return False
    
    def check_ai_service(self):
        """Verificar disponibilidad del servicio de IA"""
        try:
            import google.generativeai as genai
            return bool(settings.GEMINI_API_KEY)
        except ImportError:
            return False
    
    def check_directories(self):
        """Verificar directorios requeridos"""
        required_dirs = [
            settings.LOGS_DIR,
            settings.TEMP_DIR,
            settings.FRONTEND_DIR
        ]
        
        all_exist = True
        for dir_path in required_dirs:
            if not dir_path.exists():
                try:
                    dir_path.mkdir(parents=True, exist_ok=True)
                    print(f"📁 Directorio creado: {dir_path}")
                except Exception as e:
                    print(f"❌ No se pudo crear directorio {dir_path}: {e}")
                    all_exist = False
        
        return all_exist
    
    def check_environment_variables(self):
        """Verificar variables de entorno críticas"""
        required_vars = ['GOOGLE_SHEET_ID']
        optional_vars = ['GEMINI_API_KEY', 'TELEGRAM_BOT_TOKEN']
        
        missing_required = []
        missing_optional = []
        
        for var in required_vars:
            if not getattr(settings, var, None):
                missing_required.append(var)
        
        for var in optional_vars:
            if not getattr(settings, var, None):
                missing_optional.append(var)
        
        return {
            'valid': len(missing_required) == 0,
            'missing_required': missing_required,
            'missing_optional': missing_optional
        }
    
    async def initialize_services(self):
        """Inicializar servicios principales"""
        print("\n🔧 Inicializando servicios...")
        
        try:
            # 1. Sheets Service
            print("   📊 Inicializando Google Sheets Service...")
            self.sheets_service = SheetsServiceV2()
            
            # 2. Context Engine
            print("   🧠 Inicializando Context Engine...")
            self.context_engine = ContextEngine(self.sheets_service)
            
            # 3. Enhanced Agent
            print("   🤖 Inicializando Enhanced AI Agent...")
            self.enhanced_agent = HomologatedAIAgent(self.context_engine, self.sheets_service)
            
            print("✅ Servicios inicializados exitosamente")
            
            return {
                'success': True,
                'services': {
                    'sheets_service': bool(self.sheets_service),
                    'context_engine': bool(self.context_engine),
                    'enhanced_agent': bool(self.enhanced_agent)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error inicializando servicios: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def load_system_context(self, reset_cache=False):
        """Cargar contexto completo del sistema"""
        print("\n🔄 Cargando contexto del sistema...")
        
        try:
            if reset_cache:
                print("   🗑️ Limpiando cache...")
                self.context_engine.clear_cache()
            
            # Inicializar sistema completo
            print("   📈 Cargando todas las entidades...")
            result = await self.context_engine.initialize_system()
            
            if result.get('success'):
                entities_loaded = result.get('entities_loaded', 0)
                load_time = result.get('load_time', 0)
                
                print(f"✅ Contexto cargado: {entities_loaded} entidades en {load_time}s")
                
                return {
                    'success': True,
                    'entities_loaded': entities_loaded,
                    'load_time': load_time,
                    'business_context': result.get('business_context', {}),
                    'available_users': result.get('available_users', [])
                }
            else:
                raise Exception(result.get('error', 'Error desconocido'))
                
        except Exception as e:
            self.logger.error(f"Error cargando contexto: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def validate_system(self):
        """Validar funcionamiento completo del sistema"""
        print("\n🔍 Validando sistema...")
        
        validations = {}
        
        try:
            # 1. Validar Context Engine
            if self.context_engine:
                context_health = self.context_engine._get_cache_health()
                validations['context_engine'] = {
                    'healthy': len(context_health.get('cached_sheets', [])) > 0,
                    'details': context_health
                }
            
            # 2. Validar Enhanced Agent
            if self.enhanced_agent:
                # Probar procesamiento básico
                test_response = await self.enhanced_agent.process_query(
                    "Estado del sistema", 
                    "Eduardo"
                )
                validations['enhanced_agent'] = {
                    'healthy': test_response.confidence > 0,
                    'test_confidence': test_response.confidence
                }
            
            # 3. Validar datos de negocio
            if self.context_engine and len(self.context_engine.entity_graph) > 0:
                sample_entities = list(self.context_engine.entity_graph.keys())[:5]
                validations['business_data'] = {
                    'healthy': True,
                    'sample_entities': sample_entities,
                    'total_entities': len(self.context_engine.entity_graph)
                }
            
            all_healthy = all(
                validation.get('healthy', False) 
                for validation in validations.values()
            )
            
            if all_healthy:
                print("✅ Validación del sistema exitosa")
            else:
                print("⚠️ Se encontraron problemas en la validación")
            
            return {
                'overall_health': all_healthy,
                'validations': validations
            }
            
        except Exception as e:
            self.logger.error(f"Error en validación: {e}")
            return {
                'overall_health': False,
                'error': str(e)
            }
    
    async def run_system_tests(self):
        """Ejecutar pruebas básicas del sistema"""
        print("\n🧪 Ejecutando pruebas del sistema...")
        
        tests = {}
        
        try:
            # Test 1: Consulta básica del agente
            print("   🤖 Probando agente IA...")
            if self.enhanced_agent:
                response = await self.enhanced_agent.process_query(
                    "¿Cuántos clientes tenemos?",
                    "Eduardo"
                )
                tests['ai_query'] = {
                    'passed': response.confidence > 0.5,
                    'confidence': response.confidence,
                    'response_type': response.action_type
                }
            
            # Test 2: Contexto de usuario
            print("   👤 Probando contexto de usuario...")
            if self.context_engine:
                context = await self.context_engine.get_full_context("Eduardo")
                tests['user_context'] = {
                    'passed': 'error' not in context,
                    'has_business_context': 'business_context' in context,
                    'has_user_context': 'user_context' in context
                }
            
            # Test 3: Búsqueda de entidades
            print("   🔍 Probando búsqueda...")
            if self.context_engine and len(self.context_engine.entity_graph) > 0:
                from backend.app.services.context_engine import search_entities
                results = search_entities(self.context_engine, "cliente", "clientes")
                tests['entity_search'] = {
                    'passed': len(results) >= 0,
                    'results_count': len(results)
                }
            
            passed_tests = sum(1 for test in tests.values() if test.get('passed', False))
            total_tests = len(tests)
            
            print(f"✅ Pruebas completadas: {passed_tests}/{total_tests} exitosas")
            
            return {
                'passed': passed_tests,
                'total': total_tests,
                'success_rate': passed_tests / total_tests if total_tests > 0 else 0,
                'tests': tests
            }
            
        except Exception as e:
            self.logger.error(f"Error ejecutando pruebas: {e}")
            return {
                'passed': 0,
                'total': 0,
                'success_rate': 0,
                'error': str(e)
            }
    
    async def generate_initialization_report(self):
        """Generar reporte de inicialización"""
        print("\n📄 Generando reporte de inicialización...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'system_info': settings.get_environment_info(),
            'initialization_results': self.initialization_results,
            'summary': {
                'configuration_valid': self.initialization_results.get('configuration', {}).get('valid', False),
                'services_initialized': self.initialization_results.get('services', {}).get('success', False),
                'context_loaded': self.initialization_results.get('context', {}).get('success', False),
                'system_healthy': self.initialization_results.get('validation', {}).get('overall_health', False),
                'tests_passed': self.initialization_results.get('tests', {}).get('success_rate', 0)
            }
        }
        
        # Guardar reporte
        report_file = settings.LOGS_DIR / f"initialization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"📝 Reporte guardado en: {report_file}")
            
        except Exception as e:
            self.logger.error(f"Error guardando reporte: {e}")
        
        return report

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description="Inicializador del sistema Red Soluciones ISP v4.0 Homologado"
    )
    parser.add_argument(
        '--check-only', 
        action='store_true',
        help='Solo verificar configuración sin inicializar'
    )
    parser.add_argument(
        '--reset-cache',
        action='store_true', 
        help='Limpiar cache antes de inicializar'
    )
    
    args = parser.parse_args()
    
    # Ejecutar inicialización
    initializer = SystemInitializer()
    
    try:
        success = asyncio.run(initializer.run_full_initialization(
            check_only=args.check_only,
            reset_cache=args.reset_cache
        ))
        
        if success:
            print("\n🎯 Sistema listo para producción")
            sys.exit(0)
        else:
            print("\n💥 Inicialización falló")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️ Inicialización cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

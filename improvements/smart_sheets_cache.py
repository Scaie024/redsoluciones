"""
🚀 MEJORA 1: SISTEMA DE CACHÉ INTELIGENTE PARA GOOGLE SHEETS
===========================================================

Optimización del rendimiento manteniendo Google Sheets como fuente única de verdad
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import hashlib
import json

class SmartSheetsCache:
    """
    Sistema de caché inteligente que optimiza las consultas a Google Sheets
    manteniendo la sincronización en tiempo real
    """
    
    def __init__(self, sheets_service):
        self.sheets_service = sheets_service
        self.cache = {}
        self.cache_metadata = {}
        self.last_sync = {}
        
        # Configuración de TTL por tipo de dato
        self.ttl_config = {
            'clientes': 300,      # 5 minutos - datos que cambian poco
            'cobranza': 120,      # 2 minutos - datos financieros críticos  
            'prospectos': 180,    # 3 minutos - datos de ventas
            'incidentes': 60,     # 1 minuto - datos operativos urgentes
            'dashboard_kpis': 30, # 30 segundos - métricas en tiempo real
        }
        
        # Hash para detectar cambios
        self.data_hashes = {}
    
    def _generate_cache_key(self, sheet_type: str, filters: Dict = None) -> str:
        """Generar clave única para el caché"""
        base_key = f"{sheet_type}_{datetime.now().strftime('%Y%m%d_%H')}"
        if filters:
            filter_str = json.dumps(filters, sort_keys=True)
            filter_hash = hashlib.md5(filter_str.encode()).hexdigest()[:8]
            base_key += f"_{filter_hash}"
        return base_key
    
    def _calculate_data_hash(self, data: List[Dict]) -> str:
        """Calcular hash de los datos para detectar cambios"""
        if not data:
            return ""
        
        # Crear string representativo de los datos
        data_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    async def get_enriched_clients_cached(self, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """
        Obtener clientes enriquecidos con caché inteligente
        """
        cache_key = self._generate_cache_key('clientes_enriched')
        current_time = time.time()
        
        # Verificar si tenemos datos en caché y son válidos
        if not force_refresh and cache_key in self.cache:
            cache_data = self.cache[cache_key]
            cache_time = self.cache_metadata.get(cache_key, {}).get('timestamp', 0)
            ttl = self.ttl_config['clientes']
            
            if current_time - cache_time < ttl:
                # Datos en caché válidos
                return cache_data['data']
        
        # Obtener datos frescos
        try:
            enriched_clients = self.sheets_service.get_enriched_clients()
            
            # Calcular hash para detectar cambios futuros
            data_hash = self._calculate_data_hash(enriched_clients)
            
            # Guardar en caché
            self.cache[cache_key] = {
                'data': enriched_clients,
                'hash': data_hash
            }
            
            self.cache_metadata[cache_key] = {
                'timestamp': current_time,
                'records_count': len(enriched_clients),
                'last_updated': datetime.now().isoformat()
            }
            
            self.data_hashes['clientes'] = data_hash
            
            return enriched_clients
            
        except Exception as e:
            # Si hay error y tenemos datos en caché, usar esos
            if cache_key in self.cache:
                return self.cache[cache_key]['data']
            raise e
    
    async def get_real_time_kpis(self) -> Dict[str, Any]:
        """
        KPIs en tiempo real con caché ultra-rápido
        """
        cache_key = self._generate_cache_key('dashboard_kpis')
        current_time = time.time()
        
        if cache_key in self.cache:
            cache_time = self.cache_metadata.get(cache_key, {}).get('timestamp', 0)
            if current_time - cache_time < self.ttl_config['dashboard_kpis']:
                return self.cache[cache_key]['data']
        
        # Calcular KPIs frescos
        clients = await self.get_enriched_clients_cached()
        
        kpis = self._calculate_kpis(clients)
        
        # Guardar en caché
        self.cache[cache_key] = {'data': kpis}
        self.cache_metadata[cache_key] = {
            'timestamp': current_time,
            'calculation_time': time.time() - current_time
        }
        
        return kpis
    
    def _calculate_kpis(self, clients: List[Dict]) -> Dict[str, Any]:
        """Calcular KPIs optimizados"""
        if not clients:
            return {
                'total_clients': 0, 'active_clients': 0, 'total_revenue': 0,
                'avg_payment': 0, 'zones_count': 0, 'growth_rate': 0
            }
        
        active_clients = [
            c for c in clients 
            if str(c.get('Activo (SI/NO)', '')).lower() in ['si', 'sí', 'yes', '1', 'true']
        ]
        
        # Cálculos optimizados
        total_revenue = sum(
            float(str(c.get('Pago', 0)).replace('$', '').replace(',', '') or 0) 
            for c in active_clients
        )
        
        zones = set(c.get('Zona', '').strip() for c in active_clients if c.get('Zona', '').strip())
        
        return {
            'total_clients': len(clients),
            'active_clients': len(active_clients),
            'total_revenue': total_revenue,
            'avg_payment': total_revenue / max(len(active_clients), 1),
            'zones_count': len(zones),
            'last_calculated': datetime.now().isoformat(),
            'calculation_source': 'google_sheets_cached'
        }
    
    def invalidate_cache(self, cache_type: str = None):
        """Invalidar caché específico o todo el caché"""
        if cache_type:
            keys_to_remove = [k for k in self.cache.keys() if cache_type in k]
            for key in keys_to_remove:
                self.cache.pop(key, None)
                self.cache_metadata.pop(key, None)
        else:
            self.cache.clear()
            self.cache_metadata.clear()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Estadísticas del caché para monitoreo"""
        return {
            'total_cached_items': len(self.cache),
            'cache_types': list(set(k.split('_')[0] for k in self.cache.keys())),
            'cache_metadata': self.cache_metadata,
            'memory_usage_items': len(self.cache),
            'last_sync_times': self.last_sync
        }


# Extensión del servicio actual
class EnhancedSheetsService:
    """
    Extensión del SheetsServiceV2 con capacidades mejoradas
    """
    
    def __init__(self, base_service):
        self.base_service = base_service
        self.smart_cache = SmartSheetsCache(base_service)
        
        # Sistema de notificaciones en tiempo real
        self.webhooks = []
        self.change_listeners = []
    
    async def get_enriched_clients_fast(self) -> List[Dict[str, Any]]:
        """Versión ultra-rápida de clientes enriquecidos"""
        return await self.smart_cache.get_enriched_clients_cached()
    
    async def get_dashboard_kpis_realtime(self) -> Dict[str, Any]:
        """KPIs del dashboard en tiempo real"""
        return await self.smart_cache.get_real_time_kpis()
    
    async def sync_and_notify(self, sheet_type: str):
        """Sincronizar datos y notificar cambios"""
        try:
            # Obtener datos frescos
            if sheet_type == 'clientes':
                new_data = await self.smart_cache.get_enriched_clients_cached(force_refresh=True)
            
            # Verificar si hay cambios
            new_hash = self.smart_cache._calculate_data_hash(new_data)
            old_hash = self.smart_cache.data_hashes.get(sheet_type, '')
            
            if new_hash != old_hash:
                # Hay cambios, notificar a los listeners
                for listener in self.change_listeners:
                    await listener(sheet_type, new_data)
                
                return {
                    'changed': True,
                    'records_count': len(new_data),
                    'change_detected_at': datetime.now().isoformat()
                }
            
            return {'changed': False}
            
        except Exception as e:
            return {'error': str(e)}
    
    def add_change_listener(self, callback):
        """Agregar listener para cambios en tiempo real"""
        self.change_listeners.append(callback)
    
    async def health_check_enhanced(self) -> Dict[str, Any]:
        """Health check mejorado con métricas de rendimiento"""
        try:
            start_time = time.time()
            
            # Test básico de conexión
            basic_test = self.base_service.test_connection()
            
            # Test de rendimiento
            clients = await self.smart_cache.get_enriched_clients_cached()
            performance_time = time.time() - start_time
            
            # Métricas de caché
            cache_stats = self.smart_cache.get_cache_stats()
            
            return {
                'status': 'healthy' if basic_test.get('status') == 'connected' else 'degraded',
                'connection': basic_test,
                'performance': {
                    'response_time_ms': round(performance_time * 1000, 2),
                    'clients_loaded': len(clients),
                    'cache_efficiency': len(cache_stats['cache_types'])
                },
                'cache_stats': cache_stats,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

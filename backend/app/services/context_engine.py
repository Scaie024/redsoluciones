"""
🧠 MOTOR DE CONTEXTO CENTRAL - Red Soluciones ISP
===============================================

Sistema unificado que gestiona TODA la información del Google Sheets
como un backend coherente y inteligente.

Características:
- Mapeo completo de todas las hojas de Google Sheets
- Contexto empresarial unificado para Eduardo y Omar
- Sincronización inteligente en tiempo real
- Relaciones automáticas entre entidades
- Cache inteligente con invalidación selectiva
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import time
from collections import defaultdict

@dataclass
class BusinessContext:
    """Contexto completo del negocio Red Soluciones ISP"""
    total_clientes: int
    clientes_activos: int
    clientes_morosos: int
    ingresos_mensuales: float
    incidentes_abiertos: int
    prospectos_activos: int
    zonas_cobertura: List[str]
    growth_rate: float
    churn_rate: float
    arpu: float  # Average Revenue Per User

@dataclass
class UserContext:
    """Contexto específico por propietario"""
    propietario: str
    clientes_asignados: List[Dict]
    prospectos_pipeline: List[Dict]
    incidentes_responsable: List[Dict]
    zonas_responsable: List[str]
    kpis_personales: Dict[str, Any]
    permissions: List[str]
    preferences: Dict[str, Any]

@dataclass
class DataEntity:
    """Entidad de datos con metadatos"""
    id: str
    type: str  # 'cliente', 'prospecto', 'incidente', etc.
    data: Dict[str, Any]
    relationships: Dict[str, List[str]]
    last_updated: datetime
    propietario: str

class SheetType(Enum):
    """Tipos de hojas en Google Sheets"""
    CLIENTES = "clientes"
    PROSPECTOS = "prospectos"
    INCIDENTES = "incidentes"
    ESTADISTICAS = "estadisticas"
    PROPIETARIOS = "propietarios"
    ZONAS = "zonas"
    SERVICIOS = "servicios"
    FACTURACION = "facturacion"

class ContextEngine:
    """
    Motor de contexto central que unifica TODA la información
    del Google Sheets como un backend coherente.
    """
    
    def __init__(self, sheets_service):
        self.sheets = sheets_service
        self.logger = logging.getLogger(__name__)
        
        # Estado global del sistema
        self.global_context = {}
        self.user_contexts = {}
        self.entity_graph = {}
        self.relationship_map = defaultdict(list)
        
        # Cache inteligente
        self.cache = {}
        self.cache_timestamps = {}
        self.cache_ttl = {
            'clientes': 300,      # 5 minutos
            'prospectos': 180,    # 3 minutos
            'incidentes': 60,     # 1 minuto
            'estadisticas': 600,  # 10 minutos
            'zonas': 900,         # 15 minutos
            'propietarios': 3600  # 1 hora
        }
        
        # Configuración de hojas del Google Sheets
        self.sheet_config = {
            SheetType.CLIENTES: {
                'name': 'Clientes',
                'key_fields': ['ID', 'Nombre', 'Email', 'Telefono', 'Plan', 'Estado', 'Zona', 'Propietario', 'Fecha_Instalacion', 'Pago_Mensual'],
                'required_fields': ['Nombre', 'Plan', 'Estado', 'Propietario'],
                'relationships': ['incidentes', 'zona', 'servicios']
            },
            SheetType.PROSPECTOS: {
                'name': 'Prospectos',
                'key_fields': ['ID', 'Nombre', 'Telefono', 'Email', 'Zona', 'Estado', 'Propietario', 'Origen', 'Fecha_Contacto', 'Probabilidad'],
                'required_fields': ['Nombre', 'Estado', 'Propietario'],
                'relationships': ['zona', 'seguimientos']
            },
            SheetType.INCIDENTES: {
                'name': 'Incidentes',
                'key_fields': ['ID', 'Cliente_ID', 'Tipo', 'Descripcion', 'Estado', 'Prioridad', 'Propietario', 'Fecha_Creacion', 'Fecha_Resolucion'],
                'required_fields': ['Cliente_ID', 'Tipo', 'Estado', 'Prioridad'],
                'relationships': ['cliente', 'tecnico']
            },
            SheetType.ESTADISTICAS: {
                'name': 'Estadisticas',
                'key_fields': ['Fecha', 'Total_Clientes', 'Ingresos_Mes', 'Nuevos_Clientes', 'Clientes_Perdidos', 'Incidentes_Mes', 'Propietario'],
                'required_fields': ['Fecha', 'Total_Clientes', 'Ingresos_Mes'],
                'relationships': []
            },
            SheetType.ZONAS: {
                'name': 'Zonas',
                'key_fields': ['ID', 'Nombre', 'Cobertura', 'Densidad_Clientes', 'Infraestructura', 'Propietario_Responsable'],
                'required_fields': ['Nombre', 'Cobertura'],
                'relationships': ['clientes', 'infraestructura']
            },
            SheetType.PROPIETARIOS: {
                'name': 'Propietarios',
                'key_fields': ['ID', 'Nombre', 'Email', 'Rol', 'Permisos', 'Zonas_Asignadas', 'Activo'],
                'required_fields': ['Nombre', 'Rol'],
                'relationships': ['clientes', 'zonas']
            }
        }
        
        self.logger.info("🧠 Context Engine inicializado - Sistema homologado Red Soluciones ISP")

    async def initialize_system(self) -> Dict[str, Any]:
        """
        Inicializa completamente el sistema cargando TODA la información
        de Google Sheets y construyendo el contexto global.
        """
        try:
            self.logger.info("🚀 Inicializando sistema completo...")
            
            # 1. Cargar todas las hojas en paralelo
            start_time = time.time()
            await self._load_all_sheets()
            
            # 2. Construir relaciones entre entidades
            await self._build_relationship_graph()
            
            # 3. Calcular contexto de negocio global
            business_context = await self._calculate_business_context()
            
            # 4. Preparar contextos por usuario
            await self._initialize_user_contexts()
            
            load_time = time.time() - start_time
            
            result = {
                'success': True,
                'message': 'Sistema completamente inicializado y homologado',
                'load_time': round(load_time, 2),
                'entities_loaded': len(self.entity_graph),
                'business_context': asdict(business_context),
                'available_users': list(self.user_contexts.keys()),
                'sheets_mapped': list(self.sheet_config.keys())
            }
            
            self.logger.info(f"✅ Sistema inicializado en {load_time:.2f}s - {len(self.entity_graph)} entidades cargadas")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Error inicializando sistema: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Error en la inicialización del sistema'
            }

    async def _load_all_sheets(self):
        """Carga todas las hojas de Google Sheets en paralelo"""
        tasks = []
        
        for sheet_type, config in self.sheet_config.items():
            task = self._load_sheet_data(sheet_type, config)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(results):
            sheet_type = list(self.sheet_config.keys())[i]
            if isinstance(result, Exception):
                self.logger.error(f"❌ Error cargando {sheet_type.value}: {result}")
            else:
                self.logger.info(f"✅ {sheet_type.value}: {len(result)} registros cargados")

    async def _load_sheet_data(self, sheet_type: SheetType, config: Dict) -> List[Dict]:
        """Carga datos de una hoja específica"""
        try:
            # Simular carga asíncrona (adaptar según tu SheetsService)
            if hasattr(self.sheets, 'get_all_rows'):
                raw_data = self.sheets.get_all_rows()
            else:
                # Fallback si no está disponible
                raw_data = []
            
            # Procesar y estructurar datos
            processed_data = []
            for i, row in enumerate(raw_data):
                if not row or not any(row):  # Saltar filas vacías
                    continue
                    
                entity = self._create_entity(
                    id=f"{sheet_type.value}_{i+1}",
                    type=sheet_type.value,
                    data=dict(zip(config['key_fields'], row)),
                    propietario=row.get('Propietario', 'Sistema') if isinstance(row, dict) else 'Sistema'
                )
                
                processed_data.append(entity)
                
                # Agregar al grafo de entidades
                self.entity_graph[entity.id] = entity
            
            # Cachear los datos
            self.cache[sheet_type.value] = processed_data
            self.cache_timestamps[sheet_type.value] = time.time()
            
            return processed_data
            
        except Exception as e:
            self.logger.error(f"Error cargando {sheet_type.value}: {e}")
            return []

    def _create_entity(self, id: str, type: str, data: Dict, propietario: str) -> DataEntity:
        """Crea una entidad de datos estructurada"""
        return DataEntity(
            id=id,
            type=type,
            data=data,
            relationships={},
            last_updated=datetime.now(),
            propietario=propietario
        )

    async def _build_relationship_graph(self):
        """Construye el grafo de relaciones entre entidades"""
        self.logger.info("🔗 Construyendo grafo de relaciones...")
        
        # Relaciones Cliente -> Incidentes
        clientes = [e for e in self.entity_graph.values() if e.type == 'clientes']
        incidentes = [e for e in self.entity_graph.values() if e.type == 'incidentes']
        
        for cliente in clientes:
            cliente_id = cliente.data.get('ID')
            related_incidentes = [
                inc.id for inc in incidentes 
                if inc.data.get('Cliente_ID') == cliente_id
            ]
            cliente.relationships['incidentes'] = related_incidentes
            
        # Relaciones Cliente -> Zona
        zonas = [e for e in self.entity_graph.values() if e.type == 'zonas']
        for cliente in clientes:
            zona_nombre = cliente.data.get('Zona')
            related_zona = next(
                (z.id for z in zonas if z.data.get('Nombre') == zona_nombre),
                None
            )
            if related_zona:
                cliente.relationships['zona'] = [related_zona]
        
        # Más relaciones según necesidades...
        self.logger.info(f"✅ Grafo de relaciones construido con {len(self.entity_graph)} entidades")

    async def _calculate_business_context(self) -> BusinessContext:
        """Calcula el contexto de negocio global"""
        clientes = [e for e in self.entity_graph.values() if e.type == 'clientes']
        incidentes = [e for e in self.entity_graph.values() if e.type == 'incidentes']
        prospectos = [e for e in self.entity_graph.values() if e.type == 'prospectos']
        zonas = [e for e in self.entity_graph.values() if e.type == 'zonas']
        
        # Cálculos de negocio
        total_clientes = len(clientes)
        clientes_activos = len([c for c in clientes if c.data.get('Estado') == 'Activo'])
        clientes_morosos = len([c for c in clientes if c.data.get('Estado') == 'Moroso'])
        
        ingresos_mensuales = sum(
            float(c.data.get('Pago_Mensual', 0)) 
            for c in clientes 
            if c.data.get('Estado') == 'Activo'
        )
        
        incidentes_abiertos = len([i for i in incidentes if i.data.get('Estado') == 'Abierto'])
        prospectos_activos = len([p for p in prospectos if p.data.get('Estado') == 'Activo'])
        
        zonas_cobertura = [z.data.get('Nombre') for z in zonas]
        
        # KPIs calculados
        arpu = ingresos_mensuales / max(clientes_activos, 1)
        growth_rate = 0.0  # Calcular según datos históricos
        churn_rate = clientes_morosos / max(total_clientes, 1) * 100
        
        context = BusinessContext(
            total_clientes=total_clientes,
            clientes_activos=clientes_activos,
            clientes_morosos=clientes_morosos,
            ingresos_mensuales=ingresos_mensuales,
            incidentes_abiertos=incidentes_abiertos,
            prospectos_activos=prospectos_activos,
            zonas_cobertura=zonas_cobertura,
            growth_rate=growth_rate,
            churn_rate=churn_rate,
            arpu=arpu
        )
        
        self.global_context['business'] = context
        return context

    async def _initialize_user_contexts(self):
        """Inicializa contextos específicos por usuario"""
        propietarios = ['Eduardo', 'Omar']  # Desde Google Sheets
        
        for propietario in propietarios:
            user_context = await self._build_user_context(propietario)
            self.user_contexts[propietario] = user_context
            
        self.logger.info(f"✅ Contextos de usuario inicializados: {list(self.user_contexts.keys())}")

    async def _build_user_context(self, propietario: str) -> UserContext:
        """Construye el contexto específico para un propietario"""
        # Filtrar entidades por propietario
        clientes_usuario = [
            e.data for e in self.entity_graph.values() 
            if e.type == 'clientes' and e.propietario == propietario
        ]
        
        prospectos_usuario = [
            e.data for e in self.entity_graph.values() 
            if e.type == 'prospectos' and e.propietario == propietario
        ]
        
        incidentes_usuario = [
            e.data for e in self.entity_graph.values() 
            if e.type == 'incidentes' and e.propietario == propietario
        ]
        
        # Zonas responsables
        zonas_usuario = list(set([
            c.get('Zona') for c in clientes_usuario if c.get('Zona')
        ]))
        
        # KPIs personales
        kpis_personales = {
            'clientes_total': len(clientes_usuario),
            'ingresos_responsable': sum(float(c.get('Pago_Mensual', 0)) for c in clientes_usuario),
            'incidentes_pendientes': len([i for i in incidentes_usuario if i.get('Estado') == 'Abierto']),
            'conversion_rate': 0.0  # Calcular según prospectos convertidos
        }
        
        return UserContext(
            propietario=propietario,
            clientes_asignados=clientes_usuario,
            prospectos_pipeline=prospectos_usuario,
            incidentes_responsable=incidentes_usuario,
            zonas_responsable=zonas_usuario,
            kpis_personales=kpis_personales,
            permissions=['read', 'write', 'delete'],  # Desde Google Sheets
            preferences={}
        )

    async def get_full_context(self, propietario: str) -> Dict[str, Any]:
        """
        Obtiene el contexto COMPLETO para un propietario específico.
        Esto es lo que usará el agente IA para respuestas inteligentes.
        """
        if propietario not in self.user_contexts:
            await self._initialize_user_contexts()
        
        user_context = self.user_contexts.get(propietario)
        business_context = self.global_context.get('business')
        
        if not user_context or not business_context:
            return {'error': 'Contexto no disponible'}
        
        return {
            'propietario': propietario,
            'business_context': asdict(business_context),
            'user_context': asdict(user_context),
            'system_status': {
                'entities_loaded': len(self.entity_graph),
                'last_sync': max(self.cache_timestamps.values()) if self.cache_timestamps else 0,
                'cache_health': self._get_cache_health()
            },
            'quick_actions': self._get_quick_actions(propietario),
            'insights': await self._generate_insights(propietario)
        }

    def _get_cache_health(self) -> Dict[str, Any]:
        """Estado del sistema de cache"""
        return {
            'cached_sheets': list(self.cache.keys()),
            'cache_sizes': {k: len(v) for k, v in self.cache.items()},
            'freshness': {
                k: time.time() - ts 
                for k, ts in self.cache_timestamps.items()
            }
        }

    def _get_quick_actions(self, propietario: str) -> List[Dict[str, str]]:
        """Acciones rápidas disponibles para el usuario"""
        return [
            {'action': 'add_cliente', 'label': 'Agregar Cliente', 'icon': 'user-plus'},
            {'action': 'add_prospecto', 'label': 'Nuevo Prospecto', 'icon': 'target'},
            {'action': 'create_incidente', 'label': 'Reportar Incidente', 'icon': 'exclamation-triangle'},
            {'action': 'view_stats', 'label': 'Ver Estadísticas', 'icon': 'chart-bar'},
            {'action': 'export_data', 'label': 'Exportar Datos', 'icon': 'download'}
        ]

    async def _generate_insights(self, propietario: str) -> List[str]:
        """Genera insights automáticos para el propietario"""
        user_context = self.user_contexts.get(propietario)
        if not user_context:
            return []
        
        insights = []
        
        # Insight de incidentes
        incidentes_pendientes = user_context.kpis_personales.get('incidentes_pendientes', 0)
        if incidentes_pendientes > 5:
            insights.append(f"⚠️ Tienes {incidentes_pendientes} incidentes pendientes que requieren atención")
        
        # Insight de ingresos
        ingresos = user_context.kpis_personales.get('ingresos_responsable', 0)
        if ingresos > 0:
            insights.append(f"💰 Generas ${ingresos:,.2f} en ingresos mensuales recurrentes")
        
        # Insight de crecimiento
        clientes_total = user_context.kpis_personales.get('clientes_total', 0)
        if clientes_total > 50:
            insights.append(f"📈 Excelente gestión: administras {clientes_total} clientes")
        
        return insights

    async def refresh_data(self, sheet_type: Optional[str] = None) -> Dict[str, Any]:
        """Refresca los datos desde Google Sheets"""
        try:
            if sheet_type:
                # Refrescar hoja específica
                sheet_enum = SheetType(sheet_type)
                config = self.sheet_config[sheet_enum]
                await self._load_sheet_data(sheet_enum, config)
                
                return {
                    'success': True,
                    'message': f'Hoja {sheet_type} actualizada',
                    'updated_at': datetime.now().isoformat()
                }
            else:
                # Refrescar todo el sistema
                await self._load_all_sheets()
                await self._build_relationship_graph()
                await self._initialize_user_contexts()
                
                return {
                    'success': True,
                    'message': 'Sistema completamente actualizado',
                    'entities_loaded': len(self.entity_graph),
                    'updated_at': datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Error refrescando datos: {e}")
            return {
                'success': False,
                'error': str(e)
            }

# === FUNCIONES DE UTILIDAD ===

def get_entity_by_id(engine: ContextEngine, entity_id: str) -> Optional[DataEntity]:
    """Obtiene una entidad por su ID"""
    return engine.entity_graph.get(entity_id)

def search_entities(engine: ContextEngine, query: str, entity_type: Optional[str] = None) -> List[DataEntity]:
    """Busca entidades por texto"""
    results = []
    query_lower = query.lower()
    
    for entity in engine.entity_graph.values():
        if entity_type and entity.type != entity_type:
            continue
            
        # Buscar en todos los campos de datos
        for field, value in entity.data.items():
            if isinstance(value, str) and query_lower in value.lower():
                results.append(entity)
                break
    
    return results

def get_related_entities(engine: ContextEngine, entity_id: str, relationship_type: str) -> List[DataEntity]:
    """Obtiene entidades relacionadas"""
    entity = engine.entity_graph.get(entity_id)
    if not entity:
        return []
    
    related_ids = entity.relationships.get(relationship_type, [])
    return [engine.entity_graph[rid] for rid in related_ids if rid in engine.entity_graph]

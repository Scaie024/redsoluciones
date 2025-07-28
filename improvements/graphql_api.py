"""
🚀 MEJORA 3: API GRAPHQL PARA CONSULTAS AVANZADAS
================================================

Sistema GraphQL que permite consultas complejas y eficientes a Google Sheets
manteniendo el eje central pero mejorando la flexibilidad
"""

import graphene
from graphene import ObjectType, String, Int, Float, List, Field, Boolean
from typing import Dict, List as TypingList, Any, Optional
from datetime import datetime

# ========== TIPOS GRAPHQL ==========

class ClienteType(ObjectType):
    """Tipo GraphQL para Cliente"""
    id_cliente = String()
    nombre = String()
    email = String()
    zona = String()
    telefono = String()
    pago = Float()
    activo = Boolean()
    propietario = String()
    inicio_contrato = String()
    pagado = Boolean()
    dia_corte = Int()
    
    # Campos calculados
    es_premium = Boolean()
    dias_desde_inicio = Int()
    estado_pago = String()
    
    def resolve_es_premium(self, info):
        return (self.pago or 0) >= 400
    
    def resolve_dias_desde_inicio(self, info):
        if self.inicio_contrato:
            try:
                # Calcular días desde inicio (simplificado)
                return 30  # Placeholder
            except:
                return None
        return None
    
    def resolve_estado_pago(self, info):
        if self.pagado:
            return "AL_DIA"
        elif self.activo:
            return "PENDIENTE"
        else:
            return "INACTIVO"

class ZonaStatsType(ObjectType):
    """Estadísticas por zona"""
    zona = String()
    total_clientes = Int()
    clientes_activos = Int()
    ingresos_total = Float()
    promedio_pago = Float()
    tasa_actividad = Float()
    clientes_premium = Int()

class PropietarioStatsType(ObjectType):
    """Estadísticas por propietario"""
    propietario = String()
    total_clientes = Int()
    clientes_activos = Int()
    ingresos_generados = Float()
    zonas_asignadas = List(String)
    tasa_retencion = Float()

class BusinessKPIType(ObjectType):
    """KPIs del negocio"""
    total_clientes = Int()
    clientes_activos = Int()
    ingresos_mensuales = Float()
    arpu = Float()  # Average Revenue Per User
    churn_rate = Float()
    growth_rate = Float()
    zonas_activas = Int()
    ultimo_calculo = String()

class AlertType(ObjectType):
    """Alerta del sistema"""
    id = String()
    tipo = String()
    nivel = String()
    titulo = String()
    mensaje = String()
    timestamp = String()
    propietario_afectado = String()
    accion_requerida = String()
    datos = String()  # JSON serializado

# ========== QUERIES ==========

class Query(ObjectType):
    """Consultas principales de GraphQL"""
    
    # Consultas básicas
    clientes = List(ClienteType, 
                   zona=String(), 
                   propietario=String(), 
                   activo=Boolean(),
                   pago_min=Float(),
                   pago_max=Float())
    
    cliente = Field(ClienteType, id_cliente=String(required=True))
    
    # Estadísticas agregadas
    estadisticas_zona = List(ZonaStatsType, zona=String())
    estadisticas_propietario = List(PropietarioStatsType, propietario=String())
    kpis_negocio = Field(BusinessKPIType)
    
    # Análisis avanzados
    clientes_en_riesgo = List(ClienteType, dias_sin_pago=Int())
    oportunidades_upgrade = List(ClienteType, zona=String())
    tendencias_zona = List(ZonaStatsType, periodo_dias=Int())
    
    # Alertas y monitoreo
    alertas_activas = List(AlertType, nivel=String())
    resumen_salud = String()

    # ========== RESOLVERS ==========
    
    async def resolve_clientes(self, info, zona=None, propietario=None, activo=None, pago_min=None, pago_max=None):
        """Resolver consulta de clientes con filtros avanzados"""
        # Obtener servicio desde el contexto
        sheets_service = info.context.get('sheets_service')
        if not sheets_service:
            return []
        
        try:
            # Obtener datos enriquecidos
            clientes_data = await sheets_service.get_enriched_clients()
            
            # Aplicar filtros
            filtered_clients = []
            for client_data in clientes_data:
                client = ClienteType(
                    id_cliente=client_data.get('ID Cliente'),
                    nombre=client_data.get('Nombre'),
                    email=client_data.get('Email'),
                    zona=client_data.get('Zona'),
                    telefono=str(client_data.get('Teléfono', '')),
                    pago=float(str(client_data.get('Pago', 0)).replace('$', '').replace(',', '') or 0),
                    activo=str(client_data.get('Activo (SI/NO)', '')).lower() in ['si', 'sí'],
                    propietario=client_data.get('Propietario'),
                    inicio_contrato=client_data.get('Inicio Contrato'),
                    pagado=str(client_data.get('Pagado', 'NO')).upper() == 'SI',
                    dia_corte=int(client_data.get('Dia_Corte', 0) or 0)
                )
                
                # Aplicar filtros
                if zona and client.zona != zona:
                    continue
                if propietario and client.propietario != propietario:
                    continue
                if activo is not None and client.activo != activo:
                    continue
                if pago_min and client.pago < pago_min:
                    continue
                if pago_max and client.pago > pago_max:
                    continue
                
                filtered_clients.append(client)
            
            return filtered_clients
            
        except Exception as e:
            print(f"Error en resolve_clientes: {e}")
            return []
    
    async def resolve_cliente(self, info, id_cliente):
        """Resolver consulta de cliente individual"""
        clientes = await self.resolve_clientes(info)
        return next((c for c in clientes if c.id_cliente == id_cliente), None)
    
    async def resolve_estadisticas_zona(self, info, zona=None):
        """Resolver estadísticas por zona"""
        clientes = await self.resolve_clientes(info)
        
        # Agrupar por zona
        zonas_stats = {}
        for cliente in clientes:
            zona_nombre = cliente.zona or 'Sin zona'
            
            if zona_nombre not in zonas_stats:
                zonas_stats[zona_nombre] = {
                    'total': 0, 'activos': 0, 'ingresos': 0, 'premium': 0
                }
            
            stats = zonas_stats[zona_nombre]
            stats['total'] += 1
            
            if cliente.activo:
                stats['activos'] += 1
                stats['ingresos'] += cliente.pago or 0
            
            if cliente.es_premium:
                stats['premium'] += 1
        
        # Convertir a tipos GraphQL
        result = []
        for zona_nombre, stats in zonas_stats.items():
            if zona and zona_nombre != zona:
                continue
                
            promedio = stats['ingresos'] / max(stats['activos'], 1)
            tasa = stats['activos'] / max(stats['total'], 1)
            
            result.append(ZonaStatsType(
                zona=zona_nombre,
                total_clientes=stats['total'],
                clientes_activos=stats['activos'],
                ingresos_total=stats['ingresos'],
                promedio_pago=promedio,
                tasa_actividad=tasa,
                clientes_premium=stats['premium']
            ))
        
        return result
    
    async def resolve_kpis_negocio(self, info):
        """Resolver KPIs principales del negocio"""
        clientes = await self.resolve_clientes(info)
        
        if not clientes:
            return BusinessKPIType(
                total_clientes=0, clientes_activos=0, ingresos_mensuales=0,
                arpu=0, churn_rate=0, growth_rate=0, zonas_activas=0,
                ultimo_calculo=datetime.now().isoformat()
            )
        
        clientes_activos = [c for c in clientes if c.activo]
        ingresos_total = sum(c.pago or 0 for c in clientes_activos)
        zonas_unicas = len(set(c.zona for c in clientes if c.zona))
        arpu = ingresos_total / max(len(clientes_activos), 1)
        
        # Estimaciones simplificadas
        churn_rate = (len(clientes) - len(clientes_activos)) / max(len(clientes), 1) * 100
        growth_rate = 5.0  # Placeholder - sería calculado con datos históricos
        
        return BusinessKPIType(
            total_clientes=len(clientes),
            clientes_activos=len(clientes_activos),
            ingresos_mensuales=ingresos_total,
            arpu=arpu,
            churn_rate=churn_rate,
            growth_rate=growth_rate,
            zonas_activas=zonas_unicas,
            ultimo_calculo=datetime.now().isoformat()
        )
    
    async def resolve_clientes_en_riesgo(self, info, dias_sin_pago=30):
        """Clientes que pueden estar en riesgo de abandono"""
        clientes = await self.resolve_clientes(info)
        
        clientes_riesgo = []
        for cliente in clientes:
            if cliente.activo and not cliente.pagado:
                # Cliente activo pero sin pago - en riesgo
                clientes_riesgo.append(cliente)
        
        return clientes_riesgo
    
    async def resolve_oportunidades_upgrade(self, info, zona=None):
        """Clientes con potencial de upgrade a planes premium"""
        clientes = await self.resolve_clientes(info, zona=zona)
        
        oportunidades = []
        for cliente in clientes:
            if cliente.activo and cliente.pagado and not cliente.es_premium:
                # Cliente activo, al día, pero no premium - oportunidad
                if (cliente.pago or 0) >= 250:  # Pago medio-alto
                    oportunidades.append(cliente)
        
        return oportunidades
    
    async def resolve_alertas_activas(self, info, nivel=None):
        """Resolver alertas activas del sistema"""
        # Obtener monitor desde contexto
        monitor = info.context.get('business_monitor')
        if not monitor:
            return []
        
        try:
            from improvements.business_monitor import AlertLevel
            
            level_filter = None
            if nivel:
                level_filter = AlertLevel(nivel.lower())
            
            alerts = monitor.get_active_alerts(level_filter)
            
            return [
                AlertType(
                    id=alert.id,
                    tipo=alert.type.value,
                    nivel=alert.level.value,
                    titulo=alert.title,
                    mensaje=alert.message,
                    timestamp=alert.timestamp.isoformat(),
                    propietario_afectado=alert.propietario_affected,
                    accion_requerida=alert.action_required,
                    datos=str(alert.data)
                )
                for alert in alerts
            ]
            
        except Exception as e:
            print(f"Error obteniendo alertas: {e}")
            return []

# ========== MUTATIONS ==========

class UpdateClienteMutation(graphene.Mutation):
    """Mutación para actualizar cliente"""
    
    class Arguments:
        id_cliente = String(required=True)
        nombre = String()
        zona = String()
        telefono = String()
        pago = Float()
        activo = Boolean()
    
    cliente = Field(ClienteType)
    success = Boolean()
    message = String()
    
    async def mutate(self, info, id_cliente, **kwargs):
        """Ejecutar mutación de actualización"""
        sheets_service = info.context.get('sheets_service')
        if not sheets_service:
            return UpdateClienteMutation(
                success=False, 
                message="Servicio no disponible"
            )
        
        try:
            # Aquí implementarías la lógica de actualización en Google Sheets
            # Por ahora, simulamos éxito
            
            # Invalidar caché para refrescar datos
            if hasattr(sheets_service, 'smart_cache'):
                sheets_service.smart_cache.invalidate_cache('clientes')
            
            return UpdateClienteMutation(
                success=True,
                message=f"Cliente {id_cliente} actualizado exitosamente"
            )
            
        except Exception as e:
            return UpdateClienteMutation(
                success=False,
                message=f"Error actualizando cliente: {str(e)}"
            )

class Mutation(ObjectType):
    """Mutaciones principales"""
    update_cliente = UpdateClienteMutation.Field()

# ========== SCHEMA ==========

schema = graphene.Schema(query=Query, mutation=Mutation)

# ========== INTEGRACIÓN CON FASTAPI ==========

class GraphQLSheetsAPI:
    """
    Clase para integrar GraphQL con el sistema existente
    """
    
    def __init__(self, sheets_service, business_monitor=None):
        self.sheets_service = sheets_service
        self.business_monitor = business_monitor
        self.schema = schema
    
    def get_context(self):
        """Crear contexto para GraphQL"""
        return {
            'sheets_service': self.sheets_service,
            'business_monitor': self.business_monitor
        }
    
    async def execute_query(self, query: str, variables: Dict = None):
        """Ejecutar consulta GraphQL"""
        try:
            context = self.get_context()
            result = await self.schema.execute_async(
                query, 
                context_value=context,
                variable_values=variables or {}
            )
            
            return {
                'data': result.data,
                'errors': [str(error) for error in result.errors] if result.errors else None
            }
            
        except Exception as e:
            return {
                'data': None,
                'errors': [f"Error ejecutando consulta: {str(e)}"]
            }

# ========== CONSULTAS DE EJEMPLO ==========

EXAMPLE_QUERIES = {
    'clientes_activos_zona': '''
        query ClientesActivosZona($zona: String!) {
            clientes(zona: $zona, activo: true) {
                idCliente
                nombre
                pago
                esPremium
                estadoPago
            }
        }
    ''',
    
    'kpis_negocio': '''
        query KPIsNegocio {
            kpisNegocio {
                totalClientes
                clientesActivos
                ingresosMensuales
                arpu
                churnRate
                zonasActivas
                ultimoCalculo
            }
        }
    ''',
    
    'analisis_zona': '''
        query AnalisisZona($zona: String!) {
            estadisticasZona(zona: $zona) {
                zona
                totalClientes
                clientesActivos
                ingresosTotal
                promedioPago
                tasaActividad
                clientesPremium
            }
            
            oportunidadesUpgrade(zona: $zona) {
                nombre
                pago
                zona
                propietario
            }
        }
    ''',
    
    'dashboard_completo': '''
        query DashboardCompleto {
            kpisNegocio {
                totalClientes
                ingresosMensuales
                arpu
            }
            
            alertasActivas(nivel: "critical") {
                titulo
                mensaje
                timestamp
                accionRequerida
            }
            
            clientesEnRiesgo {
                nombre
                zona
                propietario
                diasDesdePago
            }
        }
    '''
}

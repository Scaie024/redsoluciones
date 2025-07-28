"""
🚀 MEJORA 2: SISTEMA DE MONITOREO Y ALERTAS EN TIEMPO REAL
==========================================================

Sistema avanzado de monitoreo que detecta cambios críticos en Google Sheets
y genera alertas automáticas para el negocio
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import logging

class AlertLevel(Enum):
    INFO = "info"
    WARNING = "warning" 
    CRITICAL = "critical"
    EMERGENCY = "emergency"

class AlertType(Enum):
    REVENUE_DROP = "revenue_drop"
    CLIENT_CHURNED = "client_churned"  
    PAYMENT_OVERDUE = "payment_overdue"
    SYSTEM_ERROR = "system_error"
    GROWTH_OPPORTUNITY = "growth_opportunity"
    ZONE_PERFORMANCE = "zone_performance"

@dataclass
class BusinessAlert:
    id: str
    type: AlertType
    level: AlertLevel
    title: str
    message: str
    data: Dict[str, Any]
    timestamp: datetime
    propietario_affected: Optional[str] = None
    auto_resolve: bool = False
    action_required: Optional[str] = None

class BusinessMonitor:
    """
    Monitor inteligente que detecta patrones y genera alertas basadas en Google Sheets
    """
    
    def __init__(self, sheets_service):
        self.sheets_service = sheets_service
        self.alerts = []
        self.alert_callbacks = []
        self.thresholds = {
            'revenue_drop_percent': 15,  # 15% caída en ingresos
            'client_inactive_days': 30,   # Cliente inactivo por 30 días
            'payment_overdue_days': 5,    # Pago atrasado 5 días
            'zone_performance_min': 0.8,  # 80% rendimiento mínimo por zona
        }
        
        # Histórico para comparaciones
        self.historical_data = {}
        self.last_check = {}
        
        self.logger = logging.getLogger(__name__)
    
    async def run_continuous_monitoring(self):
        """
        Ejecutar monitoreo continuo de Google Sheets
        """
        while True:
            try:
                await self.check_all_metrics()
                await asyncio.sleep(60)  # Verificar cada minuto
            except Exception as e:
                self.logger.error(f"Error en monitoreo continuo: {e}")
                await asyncio.sleep(300)  # Esperar 5 minutos si hay error
    
    async def check_all_metrics(self):
        """Verificar todas las métricas críticas"""
        
        # 1. Verificar ingresos
        await self._check_revenue_trends()
        
        # 2. Verificar estado de clientes  
        await self._check_client_status()
        
        # 3. Verificar pagos atrasados
        await self._check_overdue_payments()
        
        # 4. Verificar rendimiento por zonas
        await self._check_zone_performance()
        
        # 5. Detectar oportunidades de crecimiento
        await self._detect_growth_opportunities()
    
    async def _check_revenue_trends(self):
        """Detectar caídas significativas en ingresos"""
        try:
            current_data = await self.sheets_service.get_enriched_clients()
            
            # Calcular ingresos actuales
            current_revenue = sum(
                float(str(c.get('Pago', 0)).replace('$', '').replace(',', '') or 0)
                for c in current_data
                if str(c.get('Activo (SI/NO)', '')).lower() in ['si', 'sí']
            )
            
            # Comparar con histórico
            yesterday_revenue = self.historical_data.get('revenue_yesterday', current_revenue)
            
            if yesterday_revenue > 0:
                drop_percent = ((yesterday_revenue - current_revenue) / yesterday_revenue) * 100
                
                if drop_percent > self.thresholds['revenue_drop_percent']:
                    alert = BusinessAlert(
                        id=f"revenue_drop_{datetime.now().strftime('%Y%m%d_%H%M')}",
                        type=AlertType.REVENUE_DROP,
                        level=AlertLevel.CRITICAL,
                        title="🚨 CAÍDA CRÍTICA EN INGRESOS",
                        message=f"Los ingresos han caído {drop_percent:.1f}% en las últimas 24h. "
                               f"Anterior: ${yesterday_revenue:,.2f} → Actual: ${current_revenue:,.2f}",
                        data={
                            'current_revenue': current_revenue,
                            'previous_revenue': yesterday_revenue,
                            'drop_percent': drop_percent,
                            'affected_clients': len(current_data)
                        },
                        timestamp=datetime.now(),
                        action_required="Revisar clientes inactivos y pagos pendientes"
                    )
                    await self._trigger_alert(alert)
            
            # Actualizar histórico
            self.historical_data['revenue_yesterday'] = current_revenue
            
        except Exception as e:
            self.logger.error(f"Error verificando tendencias de ingresos: {e}")
    
    async def _check_client_status(self):
        """Detectar clientes que se han vuelto inactivos"""
        try:
            clients = await self.sheets_service.get_enriched_clients()
            
            inactive_clients = []
            for client in clients:
                if str(client.get('Activo (SI/NO)', '')).lower() not in ['si', 'sí']:
                    # Cliente inactivo detectado
                    inactive_clients.append(client)
            
            if len(inactive_clients) > 0:
                # Agrupar por propietario
                by_owner = {}
                for client in inactive_clients:
                    owner = client.get('Propietario', 'Sin asignar')
                    if owner not in by_owner:
                        by_owner[owner] = []
                    by_owner[owner].append(client)
                
                for owner, clients_list in by_owner.items():
                    if len(clients_list) >= 3:  # 3 o más clientes inactivos
                        alert = BusinessAlert(
                            id=f"clients_inactive_{owner}_{datetime.now().strftime('%Y%m%d')}",
                            type=AlertType.CLIENT_CHURNED,
                            level=AlertLevel.WARNING,
                            title=f"⚠️ CLIENTES INACTIVOS - {owner}",
                            message=f"{len(clients_list)} clientes inactivos detectados para {owner}. "
                                   f"Requiere atención inmediata.",
                            data={
                                'propietario': owner,
                                'inactive_count': len(clients_list),
                                'client_names': [c.get('Nombre', 'Sin nombre') for c in clients_list]
                            },
                            timestamp=datetime.now(),
                            propietario_affected=owner,
                            action_required="Contactar clientes y reactivar servicios"
                        )
                        await self._trigger_alert(alert)
        
        except Exception as e:
            self.logger.error(f"Error verificando estado de clientes: {e}")
    
    async def _check_overdue_payments(self):
        """Detectar pagos atrasados críticos"""
        try:
            clients = await self.sheets_service.get_enriched_clients()
            current_date = datetime.now()
            
            overdue_clients = []
            for client in clients:
                pagado = str(client.get('Pagado', 'NO')).upper()
                if pagado != 'SI':
                    # Cliente con pago pendiente
                    dia_corte = client.get('Dia_Corte', 1)
                    try:
                        dia_corte = int(dia_corte)
                        days_overdue = current_date.day - dia_corte
                        
                        if days_overdue > self.thresholds['payment_overdue_days']:
                            overdue_clients.append({
                                'client': client,
                                'days_overdue': days_overdue
                            })
                    except:
                        pass
            
            if overdue_clients:
                total_overdue_amount = sum(
                    float(str(oc['client'].get('Pago', 0)).replace('$', '').replace(',', '') or 0)
                    for oc in overdue_clients
                )
                
                alert = BusinessAlert(
                    id=f"payments_overdue_{datetime.now().strftime('%Y%m%d')}",
                    type=AlertType.PAYMENT_OVERDUE,
                    level=AlertLevel.CRITICAL,
                    title="💰 PAGOS ATRASADOS CRÍTICOS",
                    message=f"{len(overdue_clients)} clientes con pagos atrasados. "
                           f"Monto total: ${total_overdue_amount:,.2f}",
                    data={
                        'overdue_count': len(overdue_clients),
                        'total_amount': total_overdue_amount,
                        'avg_days_overdue': sum(oc['days_overdue'] for oc in overdue_clients) / len(overdue_clients),
                        'clients': [oc['client'].get('Nombre', 'Sin nombre') for oc in overdue_clients[:5]]
                    },
                    timestamp=datetime.now(),
                    action_required="Contactar clientes para gestión de cobranza"
                )
                await self._trigger_alert(alert)
        
        except Exception as e:
            self.logger.error(f"Error verificando pagos atrasados: {e}")
    
    async def _check_zone_performance(self):
        """Analizar rendimiento por zonas"""
        try:
            clients = await self.sheets_service.get_enriched_clients()
            
            # Agrupar por zona
            zones = {}
            for client in clients:
                zona = client.get('Zona', 'Sin zona')
                if zona not in zones:
                    zones[zona] = {'total': 0, 'active': 0, 'revenue': 0}
                
                zones[zona]['total'] += 1
                
                if str(client.get('Activo (SI/NO)', '')).lower() in ['si', 'sí']:
                    zones[zona]['active'] += 1
                    pago = float(str(client.get('Pago', 0)).replace('$', '').replace(',', '') or 0)
                    zones[zona]['revenue'] += pago
            
            # Detectar zonas con bajo rendimiento
            underperforming_zones = []
            for zone, stats in zones.items():
                if stats['total'] > 5:  # Solo zonas con más de 5 clientes
                    active_rate = stats['active'] / stats['total']
                    if active_rate < self.thresholds['zone_performance_min']:
                        underperforming_zones.append({
                            'zone': zone,
                            'active_rate': active_rate,
                            'stats': stats
                        })
            
            if underperforming_zones:
                alert = BusinessAlert(
                    id=f"zone_performance_{datetime.now().strftime('%Y%m%d')}",
                    type=AlertType.ZONE_PERFORMANCE,
                    level=AlertLevel.WARNING,
                    title="📍 ZONAS CON BAJO RENDIMIENTO",
                    message=f"{len(underperforming_zones)} zonas requieren atención especial",
                    data={
                        'underperforming_zones': underperforming_zones,
                        'total_zones_analyzed': len(zones)
                    },
                    timestamp=datetime.now(),
                    action_required="Revisar estrategia comercial en zonas afectadas"
                )
                await self._trigger_alert(alert)
        
        except Exception as e:
            self.logger.error(f"Error verificando rendimiento por zonas: {e}")
    
    async def _detect_growth_opportunities(self):
        """Detectar oportunidades de crecimiento"""
        try:
            clients = await self.sheets_service.get_enriched_clients()
            
            # Detectar zonas con alta concentración de clientes premium
            zones_premium = {}
            for client in clients:
                zona = client.get('Zona', 'Sin zona')
                pago = float(str(client.get('Pago', 0)).replace('$', '').replace(',', '') or 0)
                
                if zona not in zones_premium:
                    zones_premium[zona] = {'total': 0, 'premium': 0}
                
                zones_premium[zona]['total'] += 1
                if pago >= 400:  # Cliente premium
                    zones_premium[zona]['premium'] += 1
            
            # Encontrar zonas con potencial de upgrade
            opportunity_zones = []
            for zone, stats in zones_premium.items():
                if stats['total'] >= 10:  # Zonas con suficientes clientes
                    premium_rate = stats['premium'] / stats['total']
                    if 0.3 <= premium_rate <= 0.7:  # Entre 30% y 70% premium
                        opportunity_zones.append({
                            'zone': zone,
                            'premium_rate': premium_rate,
                            'potential_upgrades': stats['total'] - stats['premium']
                        })
            
            if opportunity_zones:
                alert = BusinessAlert(
                    id=f"growth_opportunity_{datetime.now().strftime('%Y%m%d')}",
                    type=AlertType.GROWTH_OPPORTUNITY,
                    level=AlertLevel.INFO,
                    title="🚀 OPORTUNIDADES DE CRECIMIENTO",
                    message=f"Detectadas {len(opportunity_zones)} zonas con potencial de upgrade",
                    data={
                        'opportunity_zones': opportunity_zones,
                        'total_potential_revenue': sum(
                            oz['potential_upgrades'] * 100 for oz in opportunity_zones
                        )
                    },
                    timestamp=datetime.now(),
                    action_required="Implementar campaña de upgrade en zonas identificadas"
                )
                await self._trigger_alert(alert)
        
        except Exception as e:
            self.logger.error(f"Error detectando oportunidades: {e}")
    
    async def _trigger_alert(self, alert: BusinessAlert):
        """Disparar alerta y notificar a todos los callbacks"""
        # Evitar alertas duplicadas
        existing_alert = next(
            (a for a in self.alerts if a.id == alert.id), None
        )
        
        if not existing_alert:
            self.alerts.append(alert)
            
            # Notificar a todos los callbacks registrados
            for callback in self.alert_callbacks:
                try:
                    await callback(alert)
                except Exception as e:
                    self.logger.error(f"Error en callback de alerta: {e}")
            
            self.logger.info(f"🚨 Alerta generada: {alert.title}")
    
    def add_alert_callback(self, callback: Callable[[BusinessAlert], None]):
        """Registrar callback para recibir alertas"""
        self.alert_callbacks.append(callback)
    
    def get_active_alerts(self, level: AlertLevel = None) -> List[BusinessAlert]:
        """Obtener alertas activas filtradas por nivel"""
        alerts = [a for a in self.alerts if not a.auto_resolve]
        
        if level:
            alerts = [a for a in alerts if a.level == level]
        
        return sorted(alerts, key=lambda x: x.timestamp, reverse=True)
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Marcar alerta como resuelta"""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.auto_resolve = True
                return True
        return False
    
    def get_monitoring_dashboard(self) -> Dict[str, Any]:
        """Dashboard de monitoreo con estadísticas"""
        current_alerts = self.get_active_alerts()
        
        alert_stats = {
            'total': len(current_alerts),
            'critical': len([a for a in current_alerts if a.level == AlertLevel.CRITICAL]),
            'warning': len([a for a in current_alerts if a.level == AlertLevel.WARNING]),
            'info': len([a for a in current_alerts if a.level == AlertLevel.INFO])
        }
        
        return {
            'status': 'healthy' if alert_stats['critical'] == 0 else 'attention_required',
            'alert_stats': alert_stats,
            'recent_alerts': [
                {
                    'id': a.id,
                    'type': a.type.value,
                    'level': a.level.value,
                    'title': a.title,
                    'timestamp': a.timestamp.isoformat()
                }
                for a in current_alerts[:10]
            ],
            'thresholds': self.thresholds,
            'monitoring_since': min(a.timestamp for a in self.alerts) if self.alerts else datetime.now(),
            'last_check': self.last_check
        }

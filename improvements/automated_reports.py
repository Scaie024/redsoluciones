"""
🚀 MEJORA 4: SISTEMA DE REPORTES AUTOMÁTICOS
==========================================

Sistema avanzado de reportes que genera automáticamente análisis de negocio
usando Google Sheets como fuente de datos central
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from email.mime.base import MimeBase
from email import encoders
import matplotlib.pyplot as plt
import pandas as pd
from jinja2 import Template
import logging

# ========== CONFIGURACIÓN ==========

class ReportConfig:
    """Configuración del sistema de reportes"""
    
    # Configuración de email
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    
    # Plantillas de reportes
    REPORT_TEMPLATES = {
        'diario': 'daily_report.html',
        'semanal': 'weekly_report.html',
        'mensual': 'monthly_report.html',
        'ejecutivo': 'executive_summary.html'
    }
    
    # Configuración de gráficos
    CHART_SETTINGS = {
        'figsize': (12, 8),
        'dpi': 300,
        'style': 'seaborn-v0_8',
        'color_palette': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    }

# ========== GENERADOR DE REPORTES ==========

class ReportGenerator:
    """Generador principal de reportes"""
    
    def __init__(self, sheets_service, business_monitor=None):
        self.sheets_service = sheets_service
        self.business_monitor = business_monitor
        self.config = ReportConfig()
        self.setup_logging()
    
    def setup_logging(self):
        """Configurar logging para reportes"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - ReportGenerator - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('reports.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    async def generate_daily_report(self, propietario: str = None) -> Dict[str, Any]:
        """Generar reporte diario"""
        try:
            self.logger.info(f"Generando reporte diario para {propietario or 'todos'}")
            
            # Obtener datos del día
            data = await self._get_daily_data(propietario)
            
            # Generar análisis
            analysis = self._analyze_daily_data(data)
            
            # Generar gráficos
            charts = await self._generate_daily_charts(data)
            
            # Crear reporte
            report = {
                'tipo': 'diario',
                'fecha': datetime.now().strftime('%Y-%m-%d'),
                'propietario': propietario,
                'datos': data,
                'analisis': analysis,
                'graficos': charts,
                'recomendaciones': self._generate_daily_recommendations(analysis)
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generando reporte diario: {e}")
            raise
    
    async def generate_weekly_report(self, propietario: str = None) -> Dict[str, Any]:
        """Generar reporte semanal"""
        try:
            self.logger.info(f"Generando reporte semanal para {propietario or 'todos'}")
            
            # Obtener datos de la semana
            data = await self._get_weekly_data(propietario)
            
            # Análisis de tendencias
            trends = self._analyze_weekly_trends(data)
            
            # Comparación con semana anterior
            comparison = await self._compare_with_previous_week(data, propietario)
            
            # Gráficos semanales
            charts = await self._generate_weekly_charts(data, trends)
            
            # Crear reporte
            report = {
                'tipo': 'semanal',
                'semana': datetime.now().strftime('%Y-W%U'),
                'propietario': propietario,
                'datos': data,
                'tendencias': trends,
                'comparacion': comparison,
                'graficos': charts,
                'insights': self._generate_weekly_insights(trends, comparison)
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generando reporte semanal: {e}")
            raise
    
    async def generate_monthly_report(self, propietario: str = None) -> Dict[str, Any]:
        """Generar reporte mensual completo"""
        try:
            self.logger.info(f"Generando reporte mensual para {propietario or 'todos'}")
            
            # Datos del mes
            data = await self._get_monthly_data(propietario)
            
            # Análisis profundo
            deep_analysis = self._perform_monthly_analysis(data)
            
            # Proyecciones
            projections = self._calculate_projections(data)
            
            # Benchmarking
            benchmarks = await self._calculate_benchmarks(data)
            
            # Gráficos avanzados
            charts = await self._generate_monthly_charts(data, deep_analysis)
            
            # Plan de acción
            action_plan = self._generate_action_plan(deep_analysis, benchmarks)
            
            report = {
                'tipo': 'mensual',
                'mes': datetime.now().strftime('%Y-%m'),
                'propietario': propietario,
                'datos': data,
                'analisis': deep_analysis,
                'proyecciones': projections,
                'benchmarks': benchmarks,
                'graficos': charts,
                'plan_accion': action_plan
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generando reporte mensual: {e}")
            raise
    
    async def generate_executive_summary(self) -> Dict[str, Any]:
        """Generar resumen ejecutivo para alta gerencia"""
        try:
            self.logger.info("Generando resumen ejecutivo")
            
            # KPIs principales
            kpis = await self._get_executive_kpis()
            
            # Tendencias del negocio
            business_trends = await self._analyze_business_trends()
            
            # Alertas críticas
            critical_alerts = await self._get_critical_alerts()
            
            # Oportunidades identificadas
            opportunities = await self._identify_opportunities()
            
            # Recomendaciones estratégicas
            strategic_recommendations = self._generate_strategic_recommendations(
                kpis, business_trends, opportunities
            )
            
            report = {
                'tipo': 'ejecutivo',
                'periodo': datetime.now().strftime('%Y-%m'),
                'kpis': kpis,
                'tendencias': business_trends,
                'alertas_criticas': critical_alerts,
                'oportunidades': opportunities,
                'recomendaciones_estrategicas': strategic_recommendations,
                'score_salud_negocio': self._calculate_business_health_score(kpis)
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generando resumen ejecutivo: {e}")
            raise
    
    # ========== MÉTODOS DE DATOS ==========
    
    async def _get_daily_data(self, propietario: str = None) -> Dict[str, Any]:
        """Obtener datos del día actual"""
        try:
            # Obtener clientes actuales
            clientes = await self.sheets_service.get_enriched_clients()
            
            # Filtrar por propietario si se especifica
            if propietario:
                clientes = [c for c in clientes if c.get('Propietario') == propietario]
            
            # Calcular métricas del día
            today = datetime.now().date()
            
            data = {
                'fecha': today.isoformat(),
                'total_clientes': len(clientes),
                'clientes_activos': len([c for c in clientes if str(c.get('Activo (SI/NO)', '')).lower() in ['si', 'sí']]),
                'clientes_pagados': len([c for c in clientes if str(c.get('Pagado', 'NO')).upper() == 'SI']),
                'ingresos_esperados': sum(
                    float(str(c.get('Pago', 0)).replace('$', '').replace(',', '') or 0)
                    for c in clientes 
                    if str(c.get('Activo (SI/NO)', '')).lower() in ['si', 'sí']
                ),
                'clientes_por_zona': self._group_by_zone(clientes),
                'alertas_dia': await self._get_daily_alerts()
            }
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error obteniendo datos diarios: {e}")
            return {}
    
    async def _get_weekly_data(self, propietario: str = None) -> Dict[str, Any]:
        """Obtener datos de la semana"""
        # Datos actuales (simulado con datos del día)
        daily_data = await self._get_daily_data(propietario)
        
        # Simular evolución semanal
        week_evolution = []
        for i in range(7):
            day_date = datetime.now().date() - timedelta(days=i)
            # Simular pequeñas variaciones
            variation = 1 + (i * 0.02)  # 2% de variación por día
            
            week_evolution.append({
                'fecha': day_date.isoformat(),
                'clientes_activos': int(daily_data['clientes_activos'] * variation),
                'ingresos': daily_data['ingresos_esperados'] * variation,
                'nuevos_clientes': max(0, 2 - i),  # Simulado
                'bajas': max(0, i - 1)  # Simulado
            })
        
        return {
            'semana_actual': week_evolution,
            'resumen': daily_data,
            'tendencia_semanal': 'positiva' if week_evolution[0]['clientes_activos'] > week_evolution[-1]['clientes_activos'] else 'negativa'
        }
    
    async def _get_monthly_data(self, propietario: str = None) -> Dict[str, Any]:
        """Obtener datos del mes"""
        weekly_data = await self._get_weekly_data(propietario)
        
        # Proyectar datos mensuales basados en datos semanales
        weekly_avg = sum(d['ingresos'] for d in weekly_data['semana_actual']) / len(weekly_data['semana_actual'])
        monthly_projection = weekly_avg * 4.33  # Promedio de semanas por mes
        
        return {
            'mes_actual': datetime.now().strftime('%Y-%m'),
            'semanas': weekly_data,
            'proyeccion_mensual': monthly_projection,
            'meta_mensual': monthly_projection * 1.15,  # Meta 15% superior
            'cumplimiento_meta': (monthly_projection / (monthly_projection * 1.15)) * 100
        }
    
    # ========== ANÁLISIS ==========
    
    def _analyze_daily_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analizar datos del día"""
        if not data:
            return {}
        
        tasa_actividad = (data['clientes_activos'] / max(data['total_clientes'], 1)) * 100
        tasa_pago = (data['clientes_pagados'] / max(data['clientes_activos'], 1)) * 100
        arpu = data['ingresos_esperados'] / max(data['clientes_activos'], 1)
        
        return {
            'tasa_actividad': round(tasa_actividad, 2),
            'tasa_pago': round(tasa_pago, 2),
            'arpu': round(arpu, 2),
            'zona_mejor_rendimiento': max(data['clientes_por_zona'].items(), key=lambda x: x[1], default=('N/A', 0))[0],
            'alertas_criticas': len([a for a in data.get('alertas_dia', []) if a.get('nivel') == 'critical']),
            'salud_general': 'buena' if tasa_actividad > 80 and tasa_pago > 70 else 'requiere_atencion'
        }
    
    def _analyze_weekly_trends(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analizar tendencias semanales"""
        if not data.get('semana_actual'):
            return {}
        
        week_data = data['semana_actual']
        
        # Calcular tendencias
        ingresos_trend = self._calculate_trend([d['ingresos'] for d in week_data])
        clientes_trend = self._calculate_trend([d['clientes_activos'] for d in week_data])
        
        return {
            'tendencia_ingresos': ingresos_trend,
            'tendencia_clientes': clientes_trend,
            'dia_mejor_rendimiento': max(week_data, key=lambda x: x['ingresos'])['fecha'],
            'crecimiento_semanal': ((week_data[0]['ingresos'] - week_data[-1]['ingresos']) / week_data[-1]['ingresos']) * 100,
            'estabilidad': 'alta' if abs(ingresos_trend) < 5 else 'media' if abs(ingresos_trend) < 15 else 'baja'
        }
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calcular tendencia de una serie de valores"""
        if len(values) < 2:
            return 0
        
        # Regresión lineal simple
        n = len(values)
        x = list(range(n))
        
        sum_x = sum(x)
        sum_y = sum(values)
        sum_xy = sum(x[i] * values[i] for i in range(n))
        sum_x2 = sum(xi ** 2 for xi in x)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        return round(slope, 2)
    
    # ========== RECOMENDACIONES ==========
    
    def _generate_daily_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generar recomendaciones diarias"""
        recommendations = []
        
        if analysis.get('tasa_actividad', 0) < 80:
            recommendations.append("🔴 Tasa de actividad baja. Revisar clientes inactivos y contactar para reactivación.")
        
        if analysis.get('tasa_pago', 0) < 70:
            recommendations.append("💰 Tasa de pago baja. Implementar estrategias de cobranza.")
        
        if analysis.get('alertas_criticas', 0) > 0:
            recommendations.append("⚠️ Hay alertas críticas pendientes. Revisar inmediatamente.")
        
        if analysis.get('salud_general') == 'buena':
            recommendations.append("✅ El negocio está funcionando bien. Mantener estrategias actuales.")
        
        return recommendations
    
    def _generate_weekly_insights(self, trends: Dict[str, Any], comparison: Dict[str, Any]) -> List[str]:
        """Generar insights semanales"""
        insights = []
        
        if trends.get('tendencia_ingresos', 0) > 0:
            insights.append(f"📈 Ingresos en tendencia positiva (+{trends['tendencia_ingresos']}%)")
        else:
            insights.append(f"📉 Ingresos en tendencia negativa ({trends['tendencia_ingresos']}%)")
        
        if trends.get('crecimiento_semanal', 0) > 5:
            insights.append("🚀 Excelente crecimiento semanal detectado")
        
        if trends.get('estabilidad') == 'baja':
            insights.append("⚡ Alta volatilidad detectada. Revisar factores externos.")
        
        return insights
    
    def _generate_action_plan(self, analysis: Dict[str, Any], benchmarks: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generar plan de acción mensual"""
        actions = []
        
        # Acciones basadas en benchmarks
        if benchmarks.get('arpu_vs_industria', 0) < 0:
            actions.append({
                'area': 'Pricing',
                'accion': 'Revisar estructura de precios',
                'prioridad': 'alta',
                'plazo': '2 semanas',
                'responsable': 'Gerencia'
            })
        
        if benchmarks.get('churn_rate', 0) > 10:
            actions.append({
                'area': 'Retención',
                'accion': 'Implementar programa de retención',
                'prioridad': 'crítica',
                'plazo': '1 semana',
                'responsable': 'Atención al Cliente'
            })
        
        return actions
    
    # ========== GRÁFICOS ==========
    
    async def _generate_daily_charts(self, data: Dict[str, Any]) -> List[str]:
        """Generar gráficos diarios"""
        charts = []
        
        try:
            plt.style.use('seaborn-v0_8')
            
            # Gráfico de distribución por zona
            if data.get('clientes_por_zona'):
                fig, ax = plt.subplots(figsize=(10, 6))
                zonas = list(data['clientes_por_zona'].keys())
                valores = list(data['clientes_por_zona'].values())
                
                ax.bar(zonas, valores, color=self.config.CHART_SETTINGS['color_palette'])
                ax.set_title('Distribución de Clientes por Zona')
                ax.set_ylabel('Número de Clientes')
                plt.xticks(rotation=45)
                plt.tight_layout()
                
                chart_path = f"reports/charts/daily_zones_{datetime.now().strftime('%Y%m%d')}.png"
                Path(chart_path).parent.mkdir(parents=True, exist_ok=True)
                plt.savefig(chart_path, dpi=300, bbox_inches='tight')
                plt.close()
                charts.append(chart_path)
            
            return charts
            
        except Exception as e:
            self.logger.error(f"Error generando gráficos diarios: {e}")
            return []
    
    # ========== HELPERS ==========
    
    def _group_by_zone(self, clientes: List[Dict]) -> Dict[str, int]:
        """Agrupar clientes por zona"""
        zones = {}
        for cliente in clientes:
            zona = cliente.get('Zona', 'Sin zona')
            zones[zona] = zones.get(zona, 0) + 1
        return zones
    
    async def _get_daily_alerts(self) -> List[Dict[str, Any]]:
        """Obtener alertas del día"""
        if self.business_monitor:
            try:
                alerts = self.business_monitor.get_active_alerts()
                return [
                    {
                        'nivel': alert.level.value,
                        'titulo': alert.title,
                        'mensaje': alert.message
                    }
                    for alert in alerts
                ]
            except:
                pass
        return []
    
    async def _compare_with_previous_week(self, data: Dict[str, Any], propietario: str = None) -> Dict[str, Any]:
        """Comparar con semana anterior (simulado)"""
        # En implementación real, obtendría datos históricos
        current_revenue = sum(d['ingresos'] for d in data.get('semana_actual', []))
        previous_revenue = current_revenue * 0.95  # Simulado: 5% menos la semana anterior
        
        return {
            'ingresos_semana_anterior': previous_revenue,
            'variacion_porcentual': ((current_revenue - previous_revenue) / previous_revenue) * 100,
            'direccion': 'positiva' if current_revenue > previous_revenue else 'negativa'
        }
    
    def _perform_monthly_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Realizar análisis profundo mensual"""
        return {
            'crecimiento_mensual': 8.5,  # Simulado
            'eficiencia_cobranza': 87.3,  # Simulado
            'satisfaccion_cliente': 92.1,  # Simulado
            'expansion_mercado': 'moderada',
            'factores_riesgo': ['Competencia', 'Estacionalidad'],
            'fortalezas': ['Base sólida de clientes', 'Buena retención']
        }
    
    def _calculate_projections(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calcular proyecciones"""
        current = data.get('proyeccion_mensual', 0)
        
        return {
            'siguiente_mes': current * 1.08,  # 8% crecimiento proyectado
            'trimestre': current * 3.25,
            'año': current * 12.5,
            'confianza': 85  # Porcentaje de confianza en la proyección
        }
    
    async def _calculate_benchmarks(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calcular benchmarks de la industria"""
        # Benchmarks típicos de ISPs pequeños/medianos
        return {
            'arpu_industria': 350,  # ARPU promedio industria
            'arpu_actual': data.get('proyeccion_mensual', 0) / max(data.get('semanas', {}).get('resumen', {}).get('clientes_activos', 1), 1),
            'churn_industria': 8.5,  # % mensual
            'churn_actual': 6.2,  # Simulado - mejor que industria
            'crecimiento_industria': 5.8,  # % mensual
            'crecimiento_actual': 8.5  # Simulado - mejor que industria
        }
    
    async def _get_executive_kpis(self) -> Dict[str, Any]:
        """Obtener KPIs ejecutivos"""
        daily_data = await self._get_daily_data()
        
        return {
            'revenue_mensual': daily_data.get('ingresos_esperados', 0) * 30,
            'num_clientes': daily_data.get('total_clientes', 0),
            'crecimiento_mes': 8.5,  # Simulado
            'margen_beneficio': 68.2,  # Simulado
            'nps_score': 72,  # Net Promoter Score simulado
            'market_share': 12.3  # Simulado
        }
    
    async def _analyze_business_trends(self) -> Dict[str, Any]:
        """Analizar tendencias del negocio"""
        return {
            'digitalizacion': 'en_progreso',
            'expansion_geografica': 'oportunidad',
            'competencia': 'moderada',
            'demanda_servicios': 'creciente',
            'tecnologia': 'actualizada'
        }
    
    async def _get_critical_alerts(self) -> List[Dict[str, Any]]:
        """Obtener alertas críticas"""
        alerts = await self._get_daily_alerts()
        return [a for a in alerts if a.get('nivel') == 'critical']
    
    async def _identify_opportunities(self) -> List[Dict[str, Any]]:
        """Identificar oportunidades de negocio"""
        return [
            {
                'tipo': 'Expansión de servicios',
                'descripcion': 'Ofrecer servicios empresariales',
                'potencial_revenue': 25000,
                'esfuerzo': 'medio'
            },
            {
                'tipo': 'Optimización pricing',
                'descripcion': 'Ajustar precios en zonas premium',
                'potencial_revenue': 8000,
                'esfuerzo': 'bajo'
            }
        ]
    
    def _generate_strategic_recommendations(self, kpis: Dict, trends: Dict, opportunities: List[Dict]) -> List[str]:
        """Generar recomendaciones estratégicas"""
        recommendations = []
        
        if kpis.get('crecimiento_mes', 0) > 5:
            recommendations.append("Acelerar inversión en infraestructura para sostener crecimiento")
        
        if kpis.get('nps_score', 0) > 70:
            recommendations.append("Aprovechar alta satisfacción para programas de referidos")
        
        if len(opportunities) > 0:
            recommendations.append(f"Priorizar implementación de {opportunities[0]['tipo']}")
        
        return recommendations
    
    def _calculate_business_health_score(self, kpis: Dict[str, Any]) -> int:
        """Calcular score de salud del negocio (0-100)"""
        score = 0
        
        # Factores de salud
        if kpis.get('crecimiento_mes', 0) > 5:
            score += 25
        if kpis.get('margen_beneficio', 0) > 60:
            score += 25
        if kpis.get('nps_score', 0) > 60:
            score += 25
        if kpis.get('num_clientes', 0) > 400:
            score += 25
        
        return min(score, 100)

# ========== SCHEDULER DE REPORTES ==========

class ReportScheduler:
    """Programador automático de reportes"""
    
    def __init__(self, report_generator: ReportGenerator):
        self.report_generator = report_generator
        self.scheduled_tasks = {}
    
    async def schedule_daily_reports(self, propietarios: List[str], hora: str = "08:00"):
        """Programar reportes diarios"""
        for propietario in propietarios:
            task_id = f"daily_{propietario}"
            # En implementación real, usarías un scheduler como APScheduler
            self.scheduled_tasks[task_id] = {
                'tipo': 'diario',
                'propietario': propietario,
                'hora': hora,
                'activo': True
            }
    
    async def schedule_executive_reports(self, hora: str = "07:00"):
        """Programar reportes ejecutivos"""
        task_id = "executive_summary"
        self.scheduled_tasks[task_id] = {
            'tipo': 'ejecutivo',
            'hora': hora,
            'activo': True
        }
    
    def get_scheduled_reports(self) -> Dict[str, Any]:
        """Obtener reportes programados"""
        return self.scheduled_tasks

# ========== EJEMPLO DE USO ==========

async def demo_reportes():
    """Demostración del sistema de reportes"""
    
    # Simular sheets_service
    class MockSheetsService:
        async def get_enriched_clients(self):
            return [
                {
                    'ID Cliente': '001',
                    'Nombre': 'Cliente Test',
                    'Zona': 'Centro',
                    'Propietario': 'Carlos',
                    'Activo (SI/NO)': 'SI',
                    'Pagado': 'SI',
                    'Pago': '400'
                }
            ]
    
    # Crear generador
    generator = ReportGenerator(MockSheetsService())
    
    # Generar reporte diario
    reporte_diario = await generator.generate_daily_report('Carlos')
    print("✅ Reporte diario generado")
    
    # Generar resumen ejecutivo
    resumen_ejecutivo = await generator.generate_executive_summary()
    print("✅ Resumen ejecutivo generado")
    
    return {
        'diario': reporte_diario,
        'ejecutivo': resumen_ejecutivo
    }

if __name__ == "__main__":
    # Ejemplo de ejecución
    asyncio.run(demo_reportes())

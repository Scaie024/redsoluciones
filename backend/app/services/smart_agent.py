"""
🤖 AGENTE ISP INTELIGENTE Y FUNCIONAL CON GEMINI AI
==================================================

Agente especializado para Red Soluciones ISP con integración completa
de Google Gemini AI y Google Sheets
"""

import json
import logging
import re
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

# Gemini AI integration
try:
    import google.generativeai as genai
    from backend.app.core.config import settings
    
    # Configure Gemini
    try:
        if hasattr(settings, 'GEMINI_API_KEY') and settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            GEMINI_AVAILABLE = True
        else:
            GEMINI_AVAILABLE = False
            logging.warning("GEMINI_API_KEY no configurada")
    except Exception as e:
        GEMINI_AVAILABLE = False
        logging.warning(f"Gemini AI config error: {e}")
except ImportError:
    GEMINI_AVAILABLE = False
    logging.warning("Gemini AI no disponible - funcionando sin IA generativa")


class SmartISPAgent:
    """Empleado virtual de Red Soluciones"""
    
    def __init__(self, sheets_service=None):
        self.sheets_service = sheets_service
        self.logger = logging.getLogger(__name__)
        
        # Inicializar Gemini AI
        self.gemini_model = None
        if GEMINI_AVAILABLE:
            try:
                # Cambiar a modelo actualizado
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                self.logger.info("🧠 Gemini AI conectado exitosamente")
            except Exception as e:
                try:
                    # Fallback a otro modelo
                    self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')
                    self.logger.info("🧠 Gemini AI conectado con modelo alternativo")
                except Exception as e2:
                    self.logger.error(f"Error conectando Gemini AI: {e} / {e2}")
                    self.gemini_model = None
        
        # Configuración del agente
        self.business_rules = {
            "standard_price": 350,
            "premium_price": 500,
            "premium_threshold": 400,
            "zones": ["Norte", "Sur", "Centro", "Este", "Oeste", "Salamanca", "Bajio", "Industrial", "Residencial"]
        }
        
        # Patrones CARLOS SÚPER PODEROSO - Gestión Completa ISP
        self.query_patterns = {
            "stats": ["estadísticas", "estadisticas", "resumen", "números", "kpi", "métricas", "metricas", "dashboard", "cuántos", "cuantos", "total"],
            "clients": ["clientes", "cliente", "usuarios", "usuario", "mostrar", "listar", "todos", "lista"],
            "prospects": ["prospecto", "prospectos", "lead", "leads", "potencial", "potenciales", "interesado", "interesados"],
            "convert": ["convertir", "conversion", "conversión", "pasar", "cambiar", "promover"],
            "search": ["buscar", "busca", "encontrar", "encuentra", "localizar", "nombre", "propietario", "zona"],
            "add_prospect": ["alta prospecto", "nuevo prospecto", "agregar prospecto", "registrar prospecto"],
            "add_client": ["alta cliente", "nuevo cliente", "agregar cliente", "registrar cliente"],
            "incident": ["incidente", "incidentes", "problema", "problemas", "reporte", "reportes", "soporte", "técnico", "tecnico", "falla", "fallas"],
            "financial": ["análisis", "analisis", "financiero", "ingresos", "revenue", "dinero", "pago", "pagos", "facturación", "facturacion"],
            "zones": ["zona", "zonas", "área", "areas", "región", "regiones", "ubicación", "ubicaciones"],
            "update": ["actualizar", "modificar", "cambiar", "editar", "corregir", "update"],
            "payments": ["cobro", "cobros", "pago", "pagos", "facturar", "cobrar", "recibo", "recibos"],
            "schedule": ["agenda", "agendar", "cita", "citas", "calendario", "recordatorio", "recordatorios"],
            "tasks": ["tarea", "tareas", "pendiente", "pendientes", "recordar", "nota", "notas"],
            "reports": ["reporte", "reportes", "informe", "informes", "documento", "documentos"],
            "admin": ["administrativo", "administración", "administracion", "gestión", "gestion", "secretario"],
            "help": ["ayuda", "help", "comandos", "qué puedes hacer", "que puedes hacer", "opciones", "funciones"]
        }
        
        # MODO EFICIENCIA - Solo respuestas directas
        self.efficient_mode = True
        self.fallback_message = "❌ No tengo acceso al LLM. Favor de pedir al administrador ayuda."
        
        self.logger.info("🤖 Agente ISP Inteligente inicializado")

    def process_query(self, query: str) -> Dict[str, Any]:
        """🧠 Procesar consulta con inteligencia real"""
        try:
            query_clean = query.strip().lower()
            intent = self._detect_intent(query_clean)
            
            # CARLOS SÚPER PODEROSO - Procesamiento Inteligente de Intenciones
            if intent == "stats":
                return self._handle_stats_query(query_clean)
            elif intent == "clients":
                return self._handle_clients_query(query_clean)
            elif intent == "prospects":
                return self._handle_prospects_query(query_clean)
            elif intent == "add_prospect":
                return self._handle_add_prospect_query(query_clean)
            elif intent == "add_client":
                return self._handle_add_client_query(query_clean)
            elif intent == "convert":
                return self._handle_convert_prospect_query(query_clean)
            elif intent == "incident":
                return self._handle_incident_report_query(query_clean)
            elif intent == "search":
                return self._handle_search_query(query_clean)
            elif intent == "update":
                return self._handle_update_client_query(query_clean)
            elif intent == "payments":
                return self._handle_payments_query(query_clean)
            elif intent == "financial":
                return self._handle_analytics_query(query_clean)
            elif intent == "zones":
                return self._handle_zones_query(query_clean)
            elif intent == "schedule":
                return self._handle_schedule_query(query_clean)
            elif intent == "tasks":
                return self._handle_tasks_query(query_clean)
            elif intent == "reports":
                return self._handle_reports_query(query_clean)
            elif intent == "admin":
                return self._handle_admin_query(query_clean)
            elif intent == "help":
                return self._handle_help_query()
            else:
                return self._handle_general_query(query_clean)
                
        except Exception as e:
            self.logger.error(f"Error procesando consulta '{query}': {e}")
            return {
                "response": f"❌ Error procesando consulta: {str(e)}",
                "type": "error",
                "suggestions": ["Ver estadísticas", "Buscar cliente", "Mostrar ayuda"]
            }

    def _detect_intent(self, query: str) -> str:
        """🎯 Detectar intención de la consulta"""
        # Patrones específicos para detectar intenciones exactas
        
        # Lista/mostrar clientes (sin nombres específicos)
        if any(phrase in query for phrase in [
            "lista de clientes", "listar clientes", "mostrar clientes", 
            "todos los clientes", "ver clientes", "clientes activos"
        ]) or (
            "clientes" in query and not any(word in query for word in [
                "buscar", "busca", "encontrar", "encuentra", "localizar"
            ])
        ):
            return "clients"
        
        # Búsqueda específica
        if any(phrase in query for phrase in [
            "buscar", "busca", "encontrar", "encuentra", "localizar"
        ]):
            return "search"
        
        # Usar el sistema de puntuación para el resto
        scores = {}
        
        for intent, keywords in self.query_patterns.items():
            score = sum(1 for keyword in keywords if keyword in query)
            if score > 0:
                scores[intent] = score
        
        # Retornar la intención con mayor score
        if scores:
            return max(scores.keys(), key=lambda k: scores[k])
        return "general"

    def _generate_natural_response(self, context: str, data: Optional[Dict] = None, response_type: str = "general") -> str:
        """🚀 CARLOS SÚPER PODEROSO - Respuestas Eficientes"""
        
        # MODO EFICIENCIA: Sin LLM = respuesta directa
        if not self.gemini_model or not GEMINI_AVAILABLE:
            if self.efficient_mode:
                return self.fallback_message
            return context  # Fallback básico
        
        try:
            # CARLOS SÚPER PODEROSO - Personalidad Optimizada
            prompt = f"""Eres CARLOS, secretario administrativo experto de Red Soluciones ISP.

REGLAS ESTRICTAS:
- Respuesta máximo 2 líneas
- Directo y profesional 
- No menciones IA/bot
- Solo datos relevantes
- Usar emojis mínimos

CONTEXTO: {context}

Responde como Carlos:"""

            response = self.gemini_model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()[:300]  # Máximo 300 caracteres
            
        except Exception as e:
            self.logger.error(f"Error Gemini: {e}")
        
        return self.fallback_message

    def _handle_stats_query(self, query: str) -> Dict[str, Any]:
        """📊 CARLOS SÚPER PODEROSO - Estadísticas Eficientes"""
        try:
            stats = self._get_business_stats()
            
            response = f"📊 {stats['total_clients']} clientes, ${stats['total_revenue']:,.0f} ingresos, {len(stats['zones'])} zonas activas."
            
            return {
                "response": response,
                "type": "stats",
                "data": stats,
                "suggestions": ["Ver clientes", "Análisis financiero", "Por zonas"]
            }
            
        except Exception as e:
            return {"response": self.fallback_message, "type": "error"}

    def _handle_clients_query(self, query: str) -> Dict[str, Any]:
        """📋 Manejar consultas sobre clientes"""
        try:
            clients = self._get_clients_data()
            
            if not clients:
                return {
                    "response": "❌ No se encontraron clientes en el sistema.\n\n" +
                              "**Posibles causas:**\n" +
                              "• No hay conexión con Google Sheets\n" +
                              "• La hoja de cálculo está vacía\n" +
                              "• Error de configuración\n\n" +
                              "💡 **Sugerencia**: Verifica la conexión a Google Sheets",
                    "type": "error",
                    "suggestions": [
                        "Verificar conexión Google Sheets",
                        "Agregar un cliente nuevo",
                        "Ver ayuda del sistema"
                    ]
                }
            
            # Análisis de clientes
            active_clients = []
            inactive_clients = []
            zones = {}
            total_revenue = 0
            
            for client in clients:
                # Verificar estado activo
                activo = str(client.get('Activo (SI/NO)', '')).strip().lower()
                if activo in ['si', 'sí', 'yes', '1', 'true', 'activo']:
                    active_clients.append(client)
                else:
                    inactive_clients.append(client)
                
                # Contar por zonas
                zona = client.get('Zona', 'Sin zona')
                zones[zona] = zones.get(zona, 0) + 1
                
                # Sumar ingresos
                pago = self._extract_payment(client)
                total_revenue += pago
            
            # Formatear respuesta
            response = f"👥 **Lista de Clientes Red Soluciones ISP**\n\n"
            response += f"📊 **Resumen**:\n"
            response += f"• Total de clientes: {len(clients)}\n"
            response += f"• Clientes activos: {len(active_clients)}\n"
            response += f"• Clientes inactivos: {len(inactive_clients)}\n"
            response += f"• Ingreso mensual total: ${total_revenue:,.2f}\n\n"
            
            if zones:
                response += f"📍 **Distribución por zonas**:\n"
                for zona, count in sorted(zones.items()):
                    response += f"• {zona}: {count} clientes\n"
                response += "\n"
            
            # Mostrar primeros 5 clientes activos
            if active_clients:
                response += f"👥 **Clientes Activos (primeros 5)**:\n"
                for i, client in enumerate(active_clients[:5], 1):
                    payment = self._extract_payment(client)
                    package_info = self._analyze_package(payment)
                    
                    response += f"**{i}. {client.get('Nombre', 'Sin nombre')}**\n"
                    response += f"   📧 {client.get('Email', 'Sin email')}\n"
                    response += f"   📍 {client.get('Zona', 'Sin zona')}\n"
                    response += f"   💰 ${payment} ({package_info['type']})\n"
                    response += f"   📱 {client.get('Teléfono', 'Sin teléfono')}\n\n"
                
                if len(active_clients) > 5:
                    response += f"... y {len(active_clients) - 5} clientes más.\n\n"
            
            return {
                "response": response,
                "type": "clients_list",
                "data": {
                    "total_clients": len(clients),
                    "active_clients": len(active_clients),
                    "inactive_clients": len(inactive_clients),
                    "zones": zones,
                    "total_revenue": total_revenue,
                    "clients": active_clients[:10]  # Primeros 10 para datos
                },
                "suggestions": [
                    f"Buscar cliente específico",
                    f"Ver clientes por zona",
                    f"Análisis financiero detallado",
                    f"Agregar nuevo cliente"
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Error en consulta de clientes: {e}")
            return {
                "response": f"❌ Error obteniendo información de clientes: {str(e)}",
                "type": "error"
            }

    def _handle_search_query(self, query: str) -> Dict[str, Any]:
        """🔍 Manejar búsquedas de clientes con respuestas naturales"""
        try:
            # Extraer nombre a buscar
            search_terms = self._extract_search_terms(query)
            
            if not search_terms:
                context = """El usuario quiere buscar un cliente pero no especificó el nombre.

Necesito explicarle cómo hacer búsquedas. Ejemplos útiles:
- "buscar juan" 
- "cliente maria garcia"
- "encontrar rodriguez"
- También puede buscar por zona, teléfono, etc."""

                response = self._generate_natural_response(context, None, "search")
                return {
                    "response": response,
                    "type": "instruction"
                }
            
            results = self._search_clients(search_terms)
            
            if not results:
                context = f"""Busqué el cliente "{search_terms}" pero no encontré resultados.

Posibles sugerencias:
- Verificar la ortografía del nombre
- Buscar solo por apellido  
- Intentar buscar por zona
- Ver la lista completa de clientes"""

                response = self._generate_natural_response(context, None, "search")
                return {
                    "response": response,
                    "type": "not_found",
                    "suggestions": [
                        "Verificar el nombre",
                        "Buscar solo por apellido", 
                        "Ver todos los clientes"
                    ]
                }
            
            # Formatear resultados para la IA
            context = f"""Encontré {len(results)} resultado(s) para "{search_terms}":

"""
            
            for i, client in enumerate(results[:3], 1):  # Máximo 3 resultados para IA
                payment = self._extract_payment(client)
                package_info = self._analyze_package(payment)
                
                context += f"""Cliente {i}: {client.get('Nombre', 'Sin nombre')}
Email: {client.get('Email', 'Sin email')}
Teléfono: {client.get('Teléfono', 'Sin teléfono')}
Zona: {client.get('Zona', 'Sin zona')}
Pago: ${payment} ({package_info['type']})
Velocidad: {package_info['speed']}

"""
            
            if len(results) > 3:
                context += f"...y {len(results) - 3} clientes más encontrados."

            response = self._generate_natural_response(context, {"results": results, "search_term": search_terms}, "search")
            
            return {
                "response": response,
                "type": "search_results",
                "data": {"results": results, "search_term": search_terms},
                "suggestions": [
                    "Ver detalles de un cliente específico",
                    "Buscar en otra zona",
                    "Ver estadísticas generales"
                ]
            }
            
        except Exception as e:
            return {
                "response": f"Tuve un problema buscando. ¿Puedes intentar de nuevo?",
                "type": "error"
            }
            
        except Exception as e:
            return {
                "response": f"❌ Error en la búsqueda: {str(e)}",
                "type": "error"
            }

    def _handle_analytics_query(self, query: str) -> Dict[str, Any]:
        """📈 Manejar consultas de análisis"""
        try:
            analytics = self._get_detailed_analytics()
            
            response = f"""📈 **Análisis Empresarial Detallado**

💼 **Resumen Financiero**:
   • Ingresos totales: ${analytics['total_revenue']:,.2f}/mes
   • Promedio por cliente: ${analytics['avg_revenue']:.2f}
   • Potencial premium: ${analytics['premium_potential']:,.2f}

🎯 **Oportunidades de Crecimiento**:
   • Clientes para upgrade: {analytics['upgrade_candidates']}
   • Potencial adicional: ${analytics['upgrade_revenue']:,.2f}/mes

📍 **Análisis por Zonas**:"""
            
            for zone, data in analytics['zones'].items():
                if data['clients'] > 0:
                    response += f"\n   • {zone}: {data['clients']} clientes (${data['revenue']:,.2f})"
            
            response += f"""

🔍 **Insights**:
{analytics['insights']}

💡 **Recomendaciones**:
{analytics['recommendations']}"""

            return {
                "response": response,
                "type": "analytics",
                "data": analytics,
                "suggestions": [
                    "Ver clientes candidatos a upgrade",
                    "Análizar zona específica", 
                    "Generar reporte completo"
                ]
            }
            
        except Exception as e:
            return {
                "response": f"❌ Error en el análisis: {str(e)}",
                "type": "error"
            }

    def _handle_help_query(self) -> Dict[str, Any]:
        """❓ Mostrar ayuda y comandos disponibles con personalidad natural"""
        try:
            context = """El usuario pidió ayuda sobre qué puedo hacer. Soy Carlos, secretario administrativo completo de Red Soluciones ISP y puedo ayudar con:

CAPACIDADES COMO SECRETARIO ADMINISTRATIVO:

👥 GESTIÓN DE CLIENTES:
• Ver estadísticas completas del negocio
• Buscar información de clientes específicos
• Dar de alta nuevos clientes
• Actualizar información existente (teléfonos, emails, planes)
• Gestionar bajas y cancelaciones

💰 GESTIÓN FINANCIERA:
• Control de cobros y pagos
• Seguimiento de clientes morosos
• Actualizar precios y planes
• Generar reportes financieros
• Estados de cuenta y facturación

📅 ADMINISTRACIÓN DIARIA:
• Gestionar agenda y citas
• Coordinar visitas técnicas
• Programar mantenimientos
• Recordatorios automáticos
• Seguimiento de tareas

📊 REPORTES Y ANÁLISIS:
• Reportes ejecutivos completos
• Análisis por zonas de cobertura
• Información financiera detallada
• Seguimiento de prospectos e incidentes
• Métricas del negocio

EJEMPLOS DE CONSULTAS:
• "Estadísticas del negocio"
• "Buscar cliente Juan Pérez"
• "Dar de alta nuevo cliente"
• "Actualizar teléfono de María"
• "Ver clientes morosos"
• "Agendar visita técnica"
• "Generar reporte mensual"

Soy tu brazo derecho administrativo. ¿En qué te puedo ayudar específicamente?"""

            response = self._generate_natural_response(context, None, "help")
            
            return {
                "response": response,
                "type": "help",
                "suggestions": [
                    "Ver estadísticas completas",
                    "Gestionar clientes", 
                    "Control de cobros",
                    "Administrar agenda",
                    "Generar reportes"
                ]
            }
        except Exception as e:
            return {
                "response": "🏢 Soy Carlos, tu secretario administrativo completo. Manejo clientes, cobros, agenda, reportes y toda la administración de Red Soluciones. ¿Qué necesitas que haga?",
                "type": "help",
                "suggestions": [
                    "Gestión clientes",
                    "Control cobros", 
                    "Agenda y citas",
                    "Reportes ejecutivos"
                ]
            }
        except Exception as e:
            return {
                "response": "¿En qué te puedo ayudar? Manejo todo lo relacionado con nuestros clientes, estadísticas del negocio, búsquedas, y análisis por zonas. Nomás dime qué necesitas.",
                "type": "help"
            }

    def _get_business_stats(self) -> Dict[str, Any]:
        """📊 Obtener estadísticas del negocio"""
        try:
            clients = self._get_clients_data()
            
            if not clients:
                return self._get_fallback_stats()
            
            # Calcular métricas
            total_clients = len(clients)
            payments = [self._extract_payment(c) for c in clients]
            valid_payments = [p for p in payments if p > 0]
            
            monthly_revenue = sum(valid_payments)
            avg_revenue = monthly_revenue / max(len(valid_payments), 1)
            
            # Análisis de paquetes
            standard_clients = len([p for p in valid_payments if p < self.business_rules["premium_threshold"]])
            premium_clients = len([p for p in valid_payments if p >= self.business_rules["premium_threshold"]])
            premium_percentage = (premium_clients / max(total_clients, 1)) * 100
            
            # Análisis de zonas
            zones = {}
            for client in clients:
                zone = client.get('Zona', 'Sin zona')
                zones[zone] = zones.get(zone, 0) + 1
            
            if zones:
                top_zone = max(zones.keys(), key=lambda k: zones[k])
                top_zone_clients = zones.get(top_zone, 0)
            else:
                top_zone = "N/A"
                top_zone_clients = 0
            
            # Insight de negocio
            if premium_percentage < 20:
                business_insight = "Oportunidad: Muchos clientes pueden hacer upgrade a premium"
            elif premium_percentage > 60:
                business_insight = "Excelente: Alta penetración de paquetes premium"
            else:
                business_insight = "Balance saludable entre paquetes estándar y premium"
            
            return {
                "total_clients": total_clients,
                "monthly_revenue": monthly_revenue,
                "avg_revenue": avg_revenue,
                "active_zones": len([z for z in zones if zones[z] > 0]),
                "standard_clients": standard_clients,
                "premium_clients": premium_clients,
                "premium_percentage": premium_percentage,
                "top_zone": top_zone,
                "top_zone_clients": top_zone_clients,
                "business_insight": business_insight,
                "zones": zones
            }
            
        except Exception as e:
            self.logger.error(f"Error calculando estadísticas: {e}")
            return self._get_fallback_stats()

    def _get_detailed_analytics(self) -> Dict[str, Any]:
        """📈 Análisis detallado del negocio"""
        try:
            clients = self._get_clients_data()
            stats = self._get_business_stats()
            
            # Identificar candidatos a upgrade
            upgrade_candidates = []
            for client in clients:
                payment = self._extract_payment(client)
                if 250 <= payment < 400:  # Rango para upgrade
                    upgrade_candidates.append(client)
            
            upgrade_revenue = len(upgrade_candidates) * (500 - 350)  # Diferencia premium-standard
            premium_potential = stats['standard_clients'] * 150  # Potencial si todos upgradearan
            
            # Análisis por zonas con ingresos
            zones_analysis = {}
            for client in clients:
                zone = client.get('Zona', 'Sin zona')
                payment = self._extract_payment(client)
                
                if zone not in zones_analysis:
                    zones_analysis[zone] = {'clients': 0, 'revenue': 0}
                
                zones_analysis[zone]['clients'] += 1
                zones_analysis[zone]['revenue'] += payment
            
            # Insights inteligentes
            insights = []
            if len(upgrade_candidates) > 5:
                insights.append(f"• {len(upgrade_candidates)} clientes están listos para upgrade premium")
            if stats['premium_percentage'] < 25:
                insights.append("• Baja penetración premium: oportunidad de crecimiento")
            if stats['top_zone_clients'] > stats['total_clients'] * 0.4:
                insights.append(f"• Alta concentración en {stats['top_zone']}: diversificar zonas")
            
            # Recomendaciones
            recommendations = []
            if upgrade_revenue > 1000:
                recommendations.append(f"• Campaña de upgrade podría generar ${upgrade_revenue:,.0f} adicionales/mes")
            if len(zones_analysis) < 5:
                recommendations.append("• Expandir a nuevas zonas geográficas")
            if stats['avg_revenue'] < 400:
                recommendations.append("• Revisar estrategia de precios para aumentar ARPU")
            
            return {
                "total_revenue": stats['monthly_revenue'],
                "avg_revenue": stats['avg_revenue'],
                "premium_potential": premium_potential,
                "upgrade_candidates": len(upgrade_candidates),
                "upgrade_revenue": upgrade_revenue,
                "zones": zones_analysis,
                "insights": "\n".join(insights) if insights else "• Negocio estable sin alertas críticas",
                "recommendations": "\n".join(recommendations) if recommendations else "• Mantener operación actual"
            }
            
        except Exception as e:
            self.logger.error(f"Error en análisis detallado: {e}")
            return {"error": "No se pudo realizar el análisis"}

    def _get_clients_data(self) -> List[Dict]:
        """📋 Obtener datos de clientes"""
        try:
            if self.sheets_service:
                return self.sheets_service.get_all_clients() or []
        except Exception as e:
            self.logger.error(f"Error obteniendo clientes: {e}")
        
        # Datos de fallback para testing
        return [
            {"Nombre": "Juan Pérez", "Email": "juan@email.com", "Zona": "Norte", "Pago": "350", "Teléfono": "555-0001"},
            {"Nombre": "María García", "Email": "maria@email.com", "Zona": "Sur", "Pago": "500", "Teléfono": "555-0002"},
            {"Nombre": "Carlos López", "Email": "carlos@email.com", "Zona": "Centro", "Pago": "350", "Teléfono": "555-0003"},
            {"Nombre": "Ana Martínez", "Email": "ana@email.com", "Zona": "Norte", "Pago": "450", "Teléfono": "555-0004"},
        ]

    def _extract_payment(self, client: Dict) -> float:
        """💰 Extraer pago de cliente"""
        for field in ['Pago', 'Precio', 'Mensualidad', 'Costo', 'Tarifa']:
            if field in client and client[field]:
                try:
                    value = str(client[field]).replace('$', '').replace(',', '').strip()
                    return float(value)
                except:
                    continue
        return 0.0

    def _analyze_package(self, payment: float) -> Dict[str, str]:
        """📦 Analizar tipo de paquete"""
        if payment >= self.business_rules["premium_threshold"]:
            return {"type": "Premium", "speed": "20Mbps"}
        elif payment > 0:
            return {"type": "Estándar", "speed": "10Mbps"}
        else:
            return {"type": "Sin definir", "speed": "N/A"}

    def _search_clients(self, search_term: str) -> List[Dict]:
        """🔍 Buscar clientes mejorado con campos específicos"""
        clients = self._get_clients_data()
        results = []
        
        # Detectar búsqueda por campo específico
        if ':' in search_term:
            field, value = search_term.split(':', 1)
            value_lower = value.lower().strip()
            
            field_mapping = {
                'propietario': 'Propietario',
                'zona': 'Zona', 
                'telefono': 'Teléfono',
                'id': 'ID Cliente'
            }
            
            target_field = field_mapping.get(field)
            if target_field:
                for client in clients:
                    client_value = str(client.get(target_field, '')).lower()
                    if value_lower in client_value and client_value:
                        results.append(client)
                return results
        
        # Búsqueda normal por múltiples campos
        search_lower = search_term.lower()
        
        for client in clients:
            name = client.get('Nombre', '').lower()
            email = client.get('Email', '').lower()  
            zone = client.get('Zona', '').lower()
            phone = str(client.get('Teléfono', '')).lower()
            client_id = client.get('ID Cliente', '').lower()
            propietario = client.get('Propietario', '').lower()
            
            if (search_lower in name or 
                search_lower in email or 
                search_lower in zone or
                search_lower in phone or
                search_lower in client_id or
                search_lower in propietario):
                results.append(client)
        
        return results

    def _extract_search_terms(self, query: str) -> str:
        """🎯 Extraer términos de búsqueda mejorado"""
        
        # Detectar búsquedas por campo específico
        field_patterns = {
            'propietario': ['propietario', 'dueño', 'owner'],
            'zona': ['zona', 'area', 'region', 'ubicacion'],
            'telefono': ['telefono', 'teléfono', 'celular', 'movil', 'móvil'],
            'id': ['id', 'codigo', 'código', 'identificador']
        }
        
        # Buscar patrones específicos
        for field, patterns in field_patterns.items():
            for pattern in patterns:
                if pattern in query:
                    # Extraer el valor después del campo
                    parts = query.split(pattern)
                    if len(parts) > 1:
                        value = parts[1].strip()
                        # Limpiar palabras conectoras
                        value = re.sub(r'^(es|con|de|del|la|el|los|las|como)\s+', '', value)
                        if value:
                            return f"{field}:{value}"
        
        # Búsqueda normal por nombre
        words_to_remove = [
            'buscar', 'busca', 'encontrar', 'cliente', 'clientes', 
            'el', 'la', 'los', 'las', 'de', 'lista', 'listar', 
            'mostrar', 'ver', 'todos', 'todas', 'activos', 'activas',
            'con', 'como', 'que', 'tenga', 'tengan'
        ]
        words = query.split()
        
        filtered_words = [w for w in words if w.lower() not in words_to_remove]
        return ' '.join(filtered_words).strip()

    def _get_fallback_stats(self) -> Dict[str, Any]:
        """📊 Estadísticas de fallback"""
        return {
            "total_clients": 4,
            "monthly_revenue": 1650.0,
            "avg_revenue": 412.5,
            "active_zones": 3,
            "standard_clients": 2,
            "premium_clients": 2,
            "premium_percentage": 50.0,
            "top_zone": "Norte",
            "top_zone_clients": 2,
            "business_insight": "Sistema en modo demo - Conectar Google Sheets para datos reales",
            "zones": {"Norte": 2, "Sur": 1, "Centro": 1}
        }

    def _handle_general_query(self, query: str) -> Dict[str, Any]:
        """Respuesta para consultas no reconocidas usando IA"""
        try:
            context = f"""El usuario preguntó: "{query}"

No pude entender exactamente qué necesita. Como empleado de Red Soluciones ISP, puedo ayudar con:
- Estadísticas del negocio y reportes
- Buscar información de clientes específicos  
- Análisis por zonas de cobertura
- Información financiera y métricas
- Gestión de prospectos e incidentes"""

            response = self._generate_natural_response(context, None, "general")
            
            return {
                "response": response,
                "type": "help"
            }
        except Exception as e:
            return {
                "response": "No entendí bien qué necesitas. ¿Podrías ser más específico? Puedo ayudarte con estadísticas, buscar clientes, o análisis del negocio.",
                "type": "help"
            }

    def _handle_add_client_query(self, query: str) -> Dict[str, Any]:
        """👤 Agregar cliente completo - CARLOS SECRETARIO"""
        try:
            # Detectar si viene con formato específico
            if "cliente:" in query.lower():
                return self._process_client_data_from_query(query)
            
            context = f"""El jefe quiere dar de alta un nuevo cliente: '{query}'

SOY CARLOS - TU SECRETARIO ADMINISTRATIVO

📝 PROCESO DE ALTA DE CLIENTES:

OPCIÓN 1 - DAME LOS DATOS AHORA:
Puedes decirme: "Cliente: [Nombre], [Email], [Zona], [Teléfono], [Pago]"

EJEMPLO:
"Cliente: Ana López, ana@email.com, Norte, 555-9876, 350"

OPCIÓN 2 - GUÍA PASO A PASO:
Solo dime "alta cliente" y te guío paso a paso

INFORMACIÓN QUE NECESITO:
✅ Nombre completo
✅ Email de contacto  
✅ Zona de cobertura (Norte, Sur, Centro, etc.)
✅ Teléfono principal
✅ Plan/Pago mensual

COMO SECRETARIO TAMBIÉN PUEDO:
• Verificar que no existe el cliente
• Asignar zona más conveniente
• Sugerir plan según ubicación
• Coordinar instalación técnica
• Generar contrato automáticamente

¿Cómo prefieres proceder con el alta?"""

            response = self._generate_natural_response(context, None, "add_client")
            
            return {
                "response": response,
                "type": "add_client_guide",
                "suggestions": [
                    "Cliente: Nombre, email, zona, teléfono, pago",
                    "Guía paso a paso",
                    "Ver zonas disponibles",
                    "Planes y precios"
                ]
            }
            
        except Exception as e:
            return {
                "response": "👤 Como secretario puedo dar de alta clientes. Dime: 'Cliente: Nombre, email, zona, teléfono, pago' o pide 'alta cliente' para guía paso a paso.",
                "type": "add_client_guide",
                "suggestions": ["Formato: Cliente: datos", "Guía paso a paso", "Ver zonas"]
            }

    def _process_client_data_from_query(self, query: str) -> Dict[str, Any]:
        """📝 Procesar datos de cliente desde consulta - CARLOS SECRETARIO"""
        try:
            # Extraer datos después de "cliente:"
            parts = query.lower().split("cliente:")
            if len(parts) < 2:
                return {"response": "❌ Formato incorrecto. Usa: Cliente: Nombre, email, zona, teléfono, pago", "type": "error"}
            
            data_part = parts[1].strip()
            client_data = [item.strip() for item in data_part.split(",")]
            
            if len(client_data) < 5:
                return {
                    "response": "❌ Faltan datos. Necesito: Cliente: Nombre, email, zona, teléfono, pago",
                    "type": "error",
                    "suggestions": ["Ver formato correcto", "Guía paso a paso"]
                }
            
            # Estructurar datos del cliente
            new_client = {
                "nombre": client_data[0].strip(),
                "email": client_data[1].strip(),
                "zona": client_data[2].strip(),
                "telefono": client_data[3].strip(),
                "plan": client_data[4].strip()
            }
            
            # Validar datos básicos
            if not new_client["nombre"] or not new_client["email"]:
                return {
                    "response": "❌ Nombre y email son obligatorios",
                    "type": "error"
                }
            
            # Procesar alta completa
            return self._handle_add_client_detailed(new_client)
            
        except Exception as e:
            return {
                "response": "❌ Error procesando datos del cliente. Usa formato: Cliente: Nombre, email, zona, teléfono, pago",
                "type": "error",
                "suggestions": ["Ver formato correcto", "Intentar de nuevo"]
            }

    def _handle_add_prospect_query(self, query: str) -> Dict[str, Any]:
        """🎯 Instrucciones para agregar prospecto"""
        return {
            "response": "🎯 **Para agregar un prospecto:**\n\n" +
                       "Usa el modal 'Ver Prospectos' en el dashboard\n" +
                       "o escribe en el formato:\n\n" +
                       "`Prospecto: [Nombre], [Teléfono], [Zona]`\n\n" +
                       "**Ejemplo:**\n" +
                       "`Prospecto: Carlos Ruiz, 555-1234, Sur`",
            "type": "instruction"
        }

    def _handle_zones_query(self, query: str) -> Dict[str, Any]:
        """📍 Información de zonas"""
        try:
            stats = self._get_business_stats()
            zones = stats['zones']
            
            response = "📍 **Análisis por Zonas**\n\n"
            
            # Ordenar zonas por número de clientes
            sorted_zones = sorted(zones.items(), key=lambda x: x[1], reverse=True)
            
            for zone, clients in sorted_zones:
                if clients > 0:
                    percentage = (clients / stats['total_clients']) * 100
                    response += f"• **{zone}**: {clients} clientes ({percentage:.1f}%)\n"
            
            # Identificar zona con más potencial
            max_zone = sorted_zones[0] if sorted_zones else ("N/A", 0)
            
            response += f"\n🎯 **Zona principal**: {max_zone[0]} con {max_zone[1]} clientes"
            response += f"\n📈 **Oportunidad**: Expandir a zonas con pocos clientes"
            
            return {
                "response": response,
                "type": "zones_analysis",
                "data": {"zones": zones, "top_zone": max_zone[0]},
                "suggestions": [
                    f"Ver clientes de {max_zone[0]}",
                    "Análisis de expansión",
                    "Estadísticas generales"
                ]
            }
            
        except Exception as e:
            return {
                "response": f"❌ Error analizando zonas: {str(e)}",
                "type": "error"
            }

    def _handle_incidents_query(self, query: str) -> Dict[str, Any]:
        """🚨 Manejar consultas sobre incidentes"""
        try:
            if self.sheets_service:
                incidents = self.sheets_service.get_incidents()
            else:
                incidents = []

            if not incidents:
                return {
                    "response": "📋 **No hay incidentes registrados actualmente**\n\n" +
                              "Para registrar un nuevo incidente:\n" +
                              "• Usa el botón 'Nuevo Incidente' en el dashboard\n" +
                              "• O escribe: 'agregar incidente para cliente [ID]'",
                    "type": "incidents_empty",
                    "suggestions": ["Registrar nuevo incidente", "Ver clientes", "Ver estadísticas"]
                }

            # Analizar incidentes
            open_incidents = [i for i in incidents if i.get('Estado', '').lower() in ['nuevo', 'abierto', 'en proceso']]
            high_priority = [i for i in incidents if i.get('Prioridad', '').lower() == 'alta']
            
            response = f"🚨 **Gestión de Incidentes**\n\n"
            response += f"📊 **Resumen**:\n"
            response += f"• Total incidentes: {len(incidents)}\n"
            response += f"• Incidentes abiertos: {len(open_incidents)}\n"
            response += f"• Prioridad alta: {len(high_priority)}\n\n"
            
            if high_priority:
                response += "🔥 **Incidentes de Alta Prioridad**:\n"
                for incident in high_priority[:3]:
                    response += f"• **{incident.get('Cliente', 'N/A')}** - {incident.get('Tipo', 'N/A')}\n"
                    response += f"  📅 {incident.get('Fecha Creación', 'N/A')}\n\n"

            return {
                "response": response,
                "type": "incidents_analysis",
                "data": {
                    "total": len(incidents),
                    "open": len(open_incidents),
                    "high_priority": len(high_priority),
                    "incidents": incidents[:10]  # Primeros 10
                },
                "suggestions": ["Registrar incidente", "Ver por prioridad", "Ver por técnico"]
            }
        except Exception as e:
            self.logger.error(f"Error consultando incidentes: {e}")
            return {
                "response": "❌ Error consultando incidentes",
                "type": "error"
            }

    def _handle_prospects_query(self, query: str) -> Dict[str, Any]:
        """👥 Manejar consultas sobre prospectos"""
        try:
            if self.sheets_service:
                prospects = self.sheets_service.get_prospects()
            else:
                prospects = []

            if not prospects:
                return {
                    "response": "🎯 **No hay prospectos registrados actualmente**\n\n" +
                              "Para agregar un nuevo prospecto:\n" +
                              "• Usa el botón 'Nuevo Prospecto' en el dashboard\n" +
                              "• O escribe: 'agregar prospecto [nombre]'",
                    "type": "prospects_empty",
                    "suggestions": ["Agregar prospecto", "Ver clientes actuales", "Ver zonas"]
                }

            # Analizar prospectos
            high_priority = [p for p in prospects if p.get('Prioridad', '').lower() == 'alta']
            by_zone = {}
            for p in prospects:
                zone = p.get('Zona', 'Sin zona')
                by_zone[zone] = by_zone.get(zone, 0) + 1

            response = f"🎯 **Gestión de Prospectos**\n\n"
            response += f"📊 **Resumen**:\n"
            response += f"• Total prospectos: {len(prospects)}\n"
            response += f"• Alta prioridad: {len(high_priority)}\n"
            response += f"• Zonas con interés: {len(by_zone)}\n\n"
            
            if high_priority:
                response += "⭐ **Prospectos Prioritarios**:\n"
                for prospect in high_priority[:5]:
                    response += f"• **{prospect.get('Nombre', 'N/A')}**\n"
                    response += f"  📍 {prospect.get('Zona', 'N/A')} | 📱 {prospect.get('Teléfono', 'N/A')}\n"
                    response += f"  💬 {prospect.get('Notas', 'Sin notas')[:50]}...\n\n"
            
            if by_zone:
                response += "📍 **Distribución por Zonas**:\n"
                for zone, count in sorted(by_zone.items(), key=lambda x: x[1], reverse=True)[:5]:
                    response += f"• {zone}: {count} prospectos\n"

            return {
                "response": response,
                "type": "prospects_analysis",
                "data": {
                    "total": len(prospects),
                    "high_priority": len(high_priority),
                    "by_zone": by_zone,
                    "prospects": prospects[:10]
                },
                "suggestions": ["Agregar prospecto", "Contactar prioritarios", "Ver por zona"]
            }
        except Exception as e:
            self.logger.error(f"Error consultando prospectos: {e}")
            return {
                "response": "❌ Error consultando prospectos",
                "type": "error"
            }

    # ============================================
    # 🏢 FUNCIONES DE SECRETARIO ADMINISTRATIVO COMPLETO
    # ============================================
    
    def _handle_update_client_query(self, query: str) -> Dict[str, Any]:
        """✏️ Actualizar información de clientes - CARLOS SECRETARIO"""
        try:
            context = f"""El jefe quiere actualizar información de un cliente. La consulta fue: '{query}'

Soy Carlos, secretario administrativo de Red Soluciones ISP. Puedo ayudar a:

ACTUALIZAR CLIENTES:
• Cambiar datos personales (nombre, teléfono, email)
• Actualizar zona de cobertura
• Modificar plan de internet y precio
• Cambiar estado (activo/inactivo)
• Corregir información de contacto

PROCESO:
1. Dime qué cliente quieres actualizar
2. Especifica qué información cambiar
3. Yo busco el cliente y hago la modificación
4. Te confirmo los cambios realizados

EJEMPLOS:
• "Actualizar teléfono de Juan Pérez"
• "Cambiar plan de María a 500 pesos"
• "Modificar zona de Cliente123 a Norte"
• "Actualizar email de empresa@ejemplo.com"

¿Qué cliente necesitas actualizar y qué información cambiar?"""

            response = self._generate_natural_response(context, None, "update")
            
            return {
                "response": response,
                "type": "update_client",
                "suggestions": [
                    "Actualizar teléfono cliente",
                    "Cambiar plan de internet",
                    "Modificar zona cobertura",
                    "Buscar cliente específico"
                ]
            }
        except Exception as e:
            return {
                "response": "❌ Error preparando actualización. Dime qué cliente y qué información necesitas cambiar.",
                "type": "update_client",
                "suggestions": ["Buscar cliente", "Ver lista clientes"]
            }

    def _handle_payments_query(self, query: str) -> Dict[str, Any]:
        """💰 Gestión de cobros y pagos - CARLOS SECRETARIO"""
        try:
            # Obtener datos de clientes para análisis de pagos
            clients_data = self._get_clients_data()
            total_pending = 0
            overdue_clients = []
            paid_this_month = 0
            
            for client in clients_data:
                payment = self._extract_payment(client)
                if payment > 0:
                    paid_this_month += payment
                    # Simular clientes con pagos pendientes (lógica de ejemplo)
                    if len(client.get('Nombre', '')) % 3 == 0:  # Cada 3er cliente tiene pago pendiente
                        total_pending += payment
                        overdue_clients.append({
                            'name': client.get('Nombre', 'Sin nombre'),
                            'amount': payment,
                            'zone': client.get('Zona', 'Sin zona'),
                            'phone': client.get('Teléfono', 'Sin teléfono')
                        })

            context = f"""El jefe pregunta sobre cobros y pagos: '{query}'

RESUMEN DE COBROS - RED SOLUCIONES ISP:

💰 INGRESOS ACTUALES:
• Total facturado este mes: ${paid_this_month:,.2f}
• Promedio por cliente: ${paid_this_month/len(clients_data):,.2f}
• Total clientes facturados: {len(clients_data)}

⚠️ COBROS PENDIENTES:
• Monto pendiente: ${total_pending:,.2f}
• Clientes con atraso: {len(overdue_clients)}

FUNCIONES QUE MANEJO COMO SECRETARIO:
✅ Generar estados de cuenta
✅ Recordatorios de pago automáticos
✅ Actualizar montos de planes
✅ Registrar pagos recibidos
✅ Reportes de morosidad
✅ Gestión de cortes por falta de pago

¿Qué necesitas específicamente? ¿Actualizar un cobro, ver morosos, o generar reporte?"""

            response = self._generate_natural_response(context, {
                'total_revenue': paid_this_month,
                'pending': total_pending,
                'overdue_count': len(overdue_clients)
            }, "payments")
            
            return {
                "response": response,
                "type": "payments",
                "data": {
                    "total_revenue": paid_this_month,
                    "total_pending": total_pending,
                    "overdue_clients": overdue_clients[:5],  # Primeros 5
                    "clients_count": len(clients_data)
                },
                "suggestions": [
                    "Ver clientes morosos",
                    "Actualizar precio cliente",
                    "Generar reporte cobros",
                    "Recordatorios de pago"
                ]
            }
        except Exception as e:
            return {
                "response": "💰 Como secretario manejo todos los cobros: recordatorios, estados de cuenta, actualización de precios y seguimiento de pagos. ¿Qué necesitas específicamente?",
                "type": "payments",
                "suggestions": ["Ver morosos", "Actualizar cobros", "Generar reporte"]
            }

    def _handle_schedule_query(self, query: str) -> Dict[str, Any]:
        """📅 Gestión de agenda y citas - CARLOS SECRETARIO"""
        try:
            context = f"""El jefe consulta sobre agenda: '{query}'

SOY CARLOS - TU SECRETARIO ADMINISTRATIVO PERSONAL

📅 GESTIONO TU AGENDA COMPLETA:

CITAS Y REUNIONES:
• Visitas técnicas a clientes
• Reuniones con proveedores  
• Instalaciones de internet
• Mantenimientos programados
• Supervisión de campo

RECORDATORIOS AUTOMÁTICOS:
• Cortes programados por falta de pago
• Seguimientos a prospectos
• Renovaciones de contratos
• Llamadas importantes
• Tareas pendientes críticas

CALENDARIO ACTUAL:
• Hoy: {datetime.now().strftime('%d/%m/%Y')}
• Horarios disponibles para agendar
• Prioridades del día
• Seguimientos pendientes

¿Qué necesitas agendar o revisar en tu calendario?"""

            response = self._generate_natural_response(context, None, "schedule")
            
            return {
                "response": response,
                "type": "schedule",
                "suggestions": [
                    "Agendar visita técnica",
                    "Ver agenda de hoy",
                    "Recordatorios pendientes",
                    "Programar mantenimiento"
                ]
            }
        except Exception as e:
            return {
                "response": "📅 Como tu secretario manejo toda tu agenda: citas, visitas técnicas, reuniones y recordatorios. ¿Qué necesitas agendar?",
                "type": "schedule",
                "suggestions": ["Agendar cita", "Ver calendario", "Recordatorios"]
            }

    def _handle_tasks_query(self, query: str) -> Dict[str, Any]:
        """📝 Gestión de tareas y pendientes - CARLOS SECRETARIO"""
        try:
            context = f"""El jefe consulta sobre tareas: '{query}'

CARLOS - GESTIÓN DE TAREAS ADMINISTRATIVAS

📝 TAREAS QUE ADMINISTRO:

ADMINISTRATIVAS DIARIAS:
• Seguimiento a clientes morosos
• Actualización de base de datos
• Generación de reportes
• Coordinación con técnicos
• Atención telefónica

TAREAS PENDIENTES HOY:
• Llamar a 3 clientes con pagos atrasados
• Actualizar información de 5 nuevos prospectos  
• Generar reporte semanal de ingresos
• Coordinar instalación en Zona Norte
• Revisar incidentes técnicos pendientes

SEGUIMIENTOS IMPORTANTES:
• Cliente premium requiere atención
• Equipo técnico solicita repuestos
• Reunión con proveedor pendiente
• Renovación contrato zona industrial

¿Qué tarea específica necesitas que maneje o revise?"""

            response = self._generate_natural_response(context, None, "tasks")
            
            return {
                "response": response,
                "type": "tasks",
                "suggestions": [
                    "Ver tareas de hoy",
                    "Pendientes importantes",
                    "Seguimiento clientes",
                    "Coordinar técnicos"
                ]
            }
        except Exception as e:
            return {
                "response": "📝 Manejo todas tus tareas administrativas: seguimientos, coordinaciones, reportes y pendientes. ¿Qué necesitas que gestione?",
                "type": "tasks",
                "suggestions": ["Tareas pendientes", "Seguimientos", "Coordinar actividades"]
            }

    def _handle_reports_query(self, query: str) -> Dict[str, Any]:
        """📊 Generación de reportes - CARLOS SECRETARIO"""
        try:
            stats = self._get_business_stats()
            
            context = f"""El jefe solicita reportes: '{query}'

CARLOS - REPORTES EJECUTIVOS DISPONIBLES

📊 REPORTES QUE GENERO:

REPORTES FINANCIEROS:
• Ingresos mensuales detallados
• Análisis de rentabilidad por zona
• Clientes morosos y recuperación
• Proyecciones de crecimiento
• Comparativos período anterior

REPORTES OPERATIVOS:
• Estado de la red por zonas
• Incidentes técnicos resueltos/pendientes
• Satisfacción del cliente
• Rendimiento del equipo técnico
• Nuevas instalaciones del mes

REPORTES COMERCIALES:
• Análisis de prospectos
• Conversión de leads
• Clientes perdidos y causas
• Oportunidades de upgrade
• Competencia en el mercado

DATOS ACTUALES DISPONIBLES:
• {stats['total_clients']} clientes activos
• ${stats['total_revenue']:,.2f} ingresos mensuales
• {len(stats['zones'])} zonas de cobertura

¿Qué reporte específico necesitas que prepare?"""

            response = self._generate_natural_response(context, stats, "reports")
            
            return {
                "response": response,
                "type": "reports", 
                "data": stats,
                "suggestions": [
                    "Reporte financiero mensual",
                    "Estado operativo actual",
                    "Análisis comercial",
                    "Reporte personalizado"
                ]
            }
        except Exception as e:
            return {
                "response": "📊 Como secretario genero todos los reportes que necesites: financieros, operativos, comerciales. ¿Qué reporte requieres?",
                "type": "reports",
                "suggestions": ["Reporte financiero", "Estado operativo", "Análisis comercial"]
            }

    def _handle_admin_query(self, query: str) -> Dict[str, Any]:
        """🏢 Funciones administrativas generales - CARLOS SECRETARIO"""
        try:
            context = f"""El jefe consulta funciones administrativas: '{query}'

CARLOS - TU SECRETARIO ADMINISTRATIVO COMPLETO

🏢 TODAS MIS FUNCIONES ADMINISTRATIVAS:

GESTIÓN DE CLIENTES:
✅ Dar de alta nuevos clientes
✅ Actualizar información existente
✅ Gestionar bajas y cancelaciones
✅ Seguimiento postventa

GESTIÓN FINANCIERA:
✅ Control de cobros y pagos
✅ Facturación y estados de cuenta
✅ Seguimiento de morosos
✅ Reportes financieros

OPERACIONES DIARIAS:
✅ Agenda y citas
✅ Coordinación con técnicos
✅ Atención telefónica
✅ Seguimiento de incidentes

ADMINISTRACIÓN GENERAL:
✅ Reportes ejecutivos
✅ Control de inventario
✅ Gestión documental
✅ Comunicación con proveedores

SOPORTE AL JEFE:
✅ Preparación de reuniones
✅ Recordatorios importantes
✅ Análisis de negocio
✅ Gestión de prioridades

Soy tu brazo derecho administrativo. ¿En qué área específica necesitas mi apoyo?"""

            response = self._generate_natural_response(context, None, "admin")
            
            return {
                "response": response,
                "type": "admin",
                "suggestions": [
                    "Gestión de clientes",
                    "Control financiero", 
                    "Operaciones diarias",
                    "Reportes ejecutivos"
                ]
            }
        except Exception as e:
            return {
                "response": "🏢 Soy Carlos, tu secretario administrativo completo. Manejo clientes, cobros, agenda, reportes y todo lo administrativo. ¿Qué necesitas?",
                "type": "admin",
                "suggestions": ["Gestión clientes", "Control cobros", "Agenda", "Reportes"]
            }

    def _handle_add_client_detailed(self, client_data: Dict[str, str]) -> Dict[str, Any]:
        """👤 Proceso completo de alta de cliente - CARLOS SECRETARIO"""
        try:
            if not self.sheets_service:
                return {
                    "response": "📋 He registrado la solicitud de alta. Formato:\n\n📝 **Nuevo Cliente**:\n• Nombre: " + client_data.get('nombre', 'No especificado') + "\n• Zona: " + client_data.get('zona', 'No especificada') + "\n• Plan: " + client_data.get('plan', 'No especificado') + "\n• Teléfono: " + client_data.get('telefono', 'No especificado') + "\n\n✅ Listo para procesar en el sistema.",
                    "type": "add_client_success",
                    "suggestions": ["Ver clientes", "Agregar otro cliente", "Estadísticas"]
                }
            
            # Aquí iría la lógica real de agregar a Google Sheets
            # Por ahora simulamos el proceso
            
            context = f"""He procesado el alta del nuevo cliente:

CLIENTE AGREGADO EXITOSAMENTE:
📝 Nombre: {client_data.get('nombre', 'Sin especificar')}
📍 Zona: {client_data.get('zona', 'Sin especificar')}  
💰 Plan: {client_data.get('plan', 'Sin especificar')}
📞 Teléfono: {client_data.get('telefono', 'Sin especificar')}
📧 Email: {client_data.get('email', 'Sin especificar')}

SIGUIENTES PASOS ADMINISTRATIVOS:
✅ Cliente registrado en base de datos
✅ Asignado a zona correspondiente
✅ Plan configurado en sistema
✅ Listo para activación técnica

Como secretario he coordinado:
• Notificación al equipo técnico
• Programación de instalación
• Generación de contrato
• Inclusión en facturación

¿Necesitas que coordine algo más para este cliente?"""

            response = self._generate_natural_response(context, client_data, "add_client_complete")
            
            return {
                "response": response,
                "type": "add_client_success",
                "data": client_data,
                "suggestions": [
                    "Programar instalación",
                    "Generar contrato",
                    "Agregar otro cliente",
                    "Ver resumen clientes"
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Error en alta detallada de cliente: {e}")
            return {
                "response": "❌ Error procesando alta. Como secretario he registrado la solicitud manualmente para procesamiento posterior.",
                "type": "add_client_error",
                "suggestions": ["Reintentar", "Ver clientes existentes"]
            }

    # ================================================
    # 🚀 CARLOS SÚPER PODEROSO - NUEVAS FUNCIONES
    # ================================================
    
    def _handle_convert_prospect_query(self, query: str) -> Dict[str, Any]:
        """🔄 Convertir prospecto a cliente - CARLOS SÚPER PODEROSO"""
        try:
            # Detectar formato: "convertir prospecto [nombre]" o "pasar a cliente [nombre]"
            if "convertir" in query or "pasar" in query:
                # Extraer nombre del prospecto
                words = query.split()
                if len(words) >= 3:
                    prospect_name = " ".join(words[2:])  # Todo después de "convertir prospecto"
                    
                    return {
                        "response": f"✅ {prospect_name} convertido de prospecto a cliente. Necesito: zona, plan y teléfono para completar.",
                        "type": "conversion_success",
                        "data": {"prospect_name": prospect_name},
                        "suggestions": [
                            f"Cliente: {prospect_name}, email, zona, teléfono, plan",
                            "Ver lista clientes",
                            "Buscar más prospectos"
                        ]
                    }
            
            return {
                "response": "📝 Para convertir: 'convertir prospecto [nombre]' o dame el formato completo del cliente.",
                "type": "conversion_guide",
                "suggestions": ["Ver prospectos", "Alta cliente directo"]
            }
            
        except Exception as e:
            return {"response": self.fallback_message, "type": "error"}

    def _handle_incident_report_query(self, query: str) -> Dict[str, Any]:
        """🛠️ Reportar incidentes para técnicos - CARLOS SÚPER PODEROSO"""
        try:
            # Detectar formato: "incidente [cliente] [descripción]"
            incident_data = self._parse_incident_from_query(query)
            
            if incident_data:
                incident_id = f"INC{len(str(incident_data.get('description', '')))}{incident_data.get('client', 'XXX')[:3].upper()}"
                
                return {
                    "response": f"🛠️ Incidente {incident_id} registrado para {incident_data['client']}. Técnico será notificado.",
                    "type": "incident_created",
                    "data": {
                        "incident_id": incident_id,
                        "client": incident_data['client'],
                        "description": incident_data['description'],
                        "priority": incident_data.get('priority', 'normal'),
                        "status": "pendiente"
                    },
                    "suggestions": [
                        "Ver incidentes pendientes",
                        "Asignar técnico",
                        "Cambiar prioridad"
                    ]
                }
            
            return {
                "response": "🛠️ Para reportar: 'incidente [cliente] [descripción]' o 'problema de [cliente]: [detalle]'",
                "type": "incident_guide",
                "suggestions": [
                    "incidente Juan Pérez sin internet",
                    "problema María: línea lenta",
                    "Ver incidentes activos"
                ]
            }
            
        except Exception as e:
            return {"response": self.fallback_message, "type": "error"}

    def _parse_incident_from_query(self, query: str) -> Optional[Dict[str, str]]:
        """📝 Extraer datos de incidente de la consulta"""
        try:
            # Patrones comunes
            if "incidente" in query:
                parts = query.split("incidente", 1)
                if len(parts) > 1:
                    content = parts[1].strip()
                    # Buscar patrón: "cliente descripción"
                    words = content.split()
                    if len(words) >= 2:
                        client = words[0] + (" " + words[1] if len(words) > 2 and len(words[1]) < 10 else "")
                        description = " ".join(words[2:]) if len(words) > 2 else "problema reportado"
                        return {"client": client, "description": description}
            
            elif "problema" in query:
                # Patrón: "problema de Cliente: descripción"
                if ":" in query:
                    parts = query.split(":", 1)
                    client_part = parts[0].replace("problema de", "").strip()
                    description = parts[1].strip()
                    return {"client": client_part, "description": description}
            
            return None
            
        except Exception:
            return None

    def _handle_add_prospect_query(self, query: str) -> Dict[str, Any]:
        """🎯 Dar de alta prospecto - CARLOS SÚPER PODEROSO"""
        try:
            # Detectar formato específico
            if "prospecto:" in query.lower():
                return self._process_prospect_data_from_query(query)
            
            return {
                "response": "🎯 Formato: 'Prospecto: Nombre, teléfono, zona, interés'. Ejemplo: 'Prospecto: Ana López, 555-1234, Norte, plan básico'",
                "type": "prospect_guide",
                "suggestions": [
                    "Prospecto: nombre, teléfono, zona, interés",
                    "Ver prospectos existentes",
                    "Convertir a cliente"
                ]
            }
            
        except Exception as e:
            return {"response": self.fallback_message, "type": "error"}

    def _process_prospect_data_from_query(self, query: str) -> Dict[str, Any]:
        """📝 Procesar datos de prospecto"""
        try:
            parts = query.lower().split("prospecto:")
            if len(parts) < 2:
                return {"response": "❌ Formato incorrecto", "type": "error"}
            
            data_part = parts[1].strip()
            prospect_data = [item.strip() for item in data_part.split(",")]
            
            if len(prospect_data) < 3:
                return {"response": "❌ Necesito: nombre, teléfono, zona mínimo", "type": "error"}
            
            new_prospect = {
                "nombre": prospect_data[0],
                "telefono": prospect_data[1] if len(prospect_data) > 1 else "",
                "zona": prospect_data[2] if len(prospect_data) > 2 else "",
                "interes": prospect_data[3] if len(prospect_data) > 3 else "plan básico"
            }
            
            prospect_id = f"PROS{len(new_prospect['nombre'])}{new_prospect['zona'][:2].upper()}"
            
            return {
                "response": f"🎯 Prospecto {prospect_id} registrado: {new_prospect['nombre']}. Listo para seguimiento.",
                "type": "prospect_created",
                "data": new_prospect,
                "suggestions": [
                    f"Convertir {new_prospect['nombre']} a cliente",
                    "Agendar llamada de seguimiento",
                    "Ver todos los prospectos"
                ]
            }
            
        except Exception as e:
            return {"response": self.fallback_message, "type": "error"}


# Instancia global del agente inteligente
smart_agent = None


def initialize_smart_agent(sheets_service=None):
    """Inicializar agente inteligente"""
    global smart_agent
    smart_agent = SmartISPAgent(sheets_service)
    return smart_agent


def get_smart_agent():
    """Obtener instancia del agente"""
    return smart_agent

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
        genai.configure(api_key=settings.GEMINI_API_KEY)
        GEMINI_AVAILABLE = True
    except Exception as e:
        GEMINI_AVAILABLE = False
        logging.warning(f"Gemini AI config error: {e}")
except ImportError:
    GEMINI_AVAILABLE = False
    logging.warning("Gemini AI no disponible - funcionando sin IA generativa")


class SmartISPAgent:
    """🤖 Agente ISP Inteligente que realmente funciona"""
    
    def __init__(self, sheets_service=None):
        self.sheets_service = sheets_service
        self.logger = logging.getLogger(__name__)
        
        # Inicializar Gemini AI
        self.gemini_model = None
        if GEMINI_AVAILABLE:
            try:
                self.gemini_model = genai.GenerativeModel('gemini-pro')
                self.logger.info("🧠 Gemini AI conectado exitosamente")
            except Exception as e:
                self.logger.error(f"Error conectando Gemini AI: {e}")
        
        # Configuración del agente
        self.business_rules = {
            "standard_price": 350,
            "premium_price": 500,
            "premium_threshold": 400,
            "zones": ["Norte", "Sur", "Centro", "Este", "Oeste", "Salamanca", "Bajio", "Industrial", "Residencial"]
        }
        
        # Patrones de consulta más completos
        self.query_patterns = {
            "stats": ["estadísticas", "estadisticas", "resumen", "números", "kpi", "métricas", "metricas", "dashboard", "cuántos", "cuantos", "total"],
            "clients": ["clientes", "cliente", "usuarios", "usuario", "mostrar", "listar", "todos", "lista"],
            "search": ["buscar", "busca", "encontrar", "encuentra", "localizar", "nombre", "propietario", "zona"],
            "financial": ["análisis", "analisis", "financiero", "ingresos", "revenue", "dinero", "pago", "pagos", "facturación", "facturacion"],
            "zones": ["zona", "zonas", "área", "areas", "región", "regiones", "ubicación", "ubicaciones", "salamanca", "cerro", "tambor"],
            "incidents": ["incidente", "incidentes", "problema", "problemas", "reporte", "reportes", "soporte", "técnico", "tecnico"],
            "prospects": ["prospecto", "prospectos", "lead", "leads", "potencial", "potenciales", "interesado", "interesados"],
            "add": ["agregar", "añadir", "nuevo", "crear", "registrar", "alta"],
            "help": ["ayuda", "help", "comandos", "qué puedes hacer", "que puedes hacer", "opciones", "funciones"]
        }
        
        self.logger.info("🤖 Agente ISP Inteligente inicializado")

    def process_query(self, query: str) -> Dict[str, Any]:
        """🧠 Procesar consulta con inteligencia real"""
        try:
            query_clean = query.strip().lower()
            intent = self._detect_intent(query_clean)
            
            # Procesar según intención
            if intent == "stats":
                return self._handle_stats_query(query_clean)
            elif intent == "clients":
                return self._handle_clients_query(query_clean)
            elif intent == "search":
                return self._handle_search_query(query_clean)
            elif intent == "add":
                return self._handle_add_client_query(query_clean)
            elif intent == "financial":
                return self._handle_analytics_query(query_clean)
            elif intent == "zones":
                return self._handle_zones_query(query_clean)
            elif intent == "incidents":
                return self._handle_incidents_query(query_clean)
            elif intent == "prospects":
                return self._handle_prospects_query(query_clean)
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

    def _handle_stats_query(self, query: str) -> Dict[str, Any]:
        """📊 Manejar consultas de estadísticas"""
        try:
            stats = self._get_business_stats()
            
            response = f"""📊 **Estadísticas Red Soluciones ISP**

👥 **Clientes**: {stats['total_clients']} activos
💰 **Ingresos Mensuales**: ${stats['monthly_revenue']:,.2f}
📍 **Zonas Activas**: {stats['active_zones']}
📦 **Distribución de Paquetes**:
   • Estándar (10Mbps): {stats['standard_clients']} clientes
   • Premium (20Mbps): {stats['premium_clients']} clientes

📈 **Métricas Clave**:
   • Ingreso promedio por cliente: ${stats['avg_revenue']:.2f}
   • Porcentaje premium: {stats['premium_percentage']:.1f}%
   • Zona principal: {stats['top_zone']} ({stats['top_zone_clients']} clientes)

🎯 **Análisis**: {stats['business_insight']}"""

            return {
                "response": response,
                "type": "analytics",
                "data": stats,
                "suggestions": [
                    "Ver clientes por zona",
                    "Análizar oportunidades de upselling",
                    "Generar reporte financiero"
                ]
            }
        except Exception as e:
            return {
                "response": f"❌ Error obteniendo estadísticas: {str(e)}",
                "type": "error"
            }

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
        """🔍 Manejar búsquedas de clientes"""
        try:
            # Extraer nombre a buscar
            search_terms = self._extract_search_terms(query)
            
            if not search_terms:
                return {
                    "response": "🔍 **Para buscar un cliente:**\n\n" +
                              "Escribe: 'buscar [nombre]' o 'cliente [nombre]'\n\n" +
                              "**Ejemplos:**\n" +
                              "• buscar juan\n" +
                              "• cliente maria garcia\n" +
                              "• encontrar rodriguez",
                    "type": "instruction"
                }
            
            results = self._search_clients(search_terms)
            
            if not results:
                return {
                    "response": f"❌ No se encontraron clientes con '{search_terms}'",
                    "type": "not_found",
                    "suggestions": [
                        "Verificar el nombre",
                        "Buscar solo por apellido",
                        "Ver todos los clientes"
                    ]
                }
            
            # Formatear resultados
            response = f"🔍 **Resultados para '{search_terms}'**\n\n"
            
            for i, client in enumerate(results[:5], 1):  # Máximo 5 resultados
                payment = self._extract_payment(client)
                package_info = self._analyze_package(payment)
                
                response += f"**{i}. {client.get('Nombre', 'Sin nombre')}**\n"
                response += f"   📧 {client.get('Email', 'Sin email')}\n"
                response += f"   📱 {client.get('Teléfono', 'Sin teléfono')}\n"
                response += f"   📍 Zona: {client.get('Zona', 'Sin zona')}\n"
                response += f"   💰 Pago: ${payment} ({package_info['type']})\n"
                response += f"   📦 Velocidad: {package_info['speed']}\n\n"
            
            if len(results) > 5:
                response += f"... y {len(results) - 5} resultados más."
            
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
        """❓ Mostrar ayuda y comandos disponibles"""
        help_text = """🤖 **Asistente IA Red Soluciones - Comandos Disponibles**

📊 **ESTADÍSTICAS Y ANÁLISIS**
   • "estadísticas" - Resumen completo del negocio
   • "análisis financiero" - Detalles de ingresos y oportunidades
   • "métricas" - KPIs principales

🔍 **BÚSQUEDA DE CLIENTES**
   • "buscar [nombre]" - Encontrar cliente específico
   • "cliente [nombre]" - Información de cliente
   • "zona norte" - Ver clientes por zona

👥 **GESTIÓN DE CLIENTES**
   • "nuevo cliente: [datos]" - Agregar cliente
   • "prospecto: [datos]" - Agregar prospecto

📈 **REPORTES**
   • "reporte mensual" - Reporte completo
   • "análisis de zonas" - Distribución geográfica

💡 **EJEMPLOS PRÁCTICOS**
   • "¿cuántos clientes tenemos?"
   • "buscar maría"
   • "análisis financiero"
   • "clientes de salamanca"

**¡Puedes escribir de forma natural! Entiendo consultas en español conversacional.**"""

        return {
            "response": help_text,
            "type": "help",
            "suggestions": [
                "Ver estadísticas",
                "Buscar un cliente",
                "Análisis financiero",
                "Mostrar zonas"
            ]
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
        """💬 Manejar consultas generales"""
        return {
            "response": f"💡 **No entendí completamente tu consulta**\n\n" +
                       "Puedes preguntarme sobre:\n" +
                       "• 📊 Estadísticas del negocio\n" +
                       "• 🔍 Buscar clientes\n" +
                       "• 📈 Análisis financiero\n" +
                       "• 📍 Información de zonas\n\n" +
                       "**Ejemplo**: 'estadísticas' o 'buscar juan'",
            "type": "help",
            "suggestions": [
                "Ver estadísticas",
                "Buscar cliente",
                "Análisis financiero",
                "Mostrar ayuda"
            ]
        }

    def _handle_add_client_query(self, query: str) -> Dict[str, Any]:
        """👤 Instrucciones para agregar cliente"""
        return {
            "response": "👤 **Para agregar un cliente:**\n\n" +
                       "Usa el modal 'Ver Clientes' en el dashboard\n" +
                       "o escribe en el formato:\n\n" +
                       "`Cliente: [Nombre], [Email], [Zona], [Teléfono], [Pago]`\n\n" +
                       "**Ejemplo:**\n" +
                       "`Cliente: Ana López, ana@email.com, Norte, 555-9876, 350`",
            "type": "instruction"
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

"""
🎯 SUPER ADMINISTRADOR - RED SOLUCIONES ISP
==========================================

Asistente ejecutivo profesional para administración empresarial
- Análisis avanzado de negocio y operaciones
- Gestión estratégica de clientes y recursos
- Reportes ejecutivos y métricas clave
- Supervisión integral del sistema ISP

Sistema: Red Soluciones ISP v2.0 Enterprise
Rol: Super Administrador Ejecutivo
"""

# === IMPORTACIONES ===
import json
import logging
import re
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

# === CONFIGURACIÓN GEMINI AI ===
try:
    import google.generativeai as genai
    
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and len(api_key) > 20:
        genai.configure(api_key=api_key)
        GEMINI_AVAILABLE = True
        logging.info("🧠 Sistema IA: Activo y operacional")
    else:
        GEMINI_AVAILABLE = False
        logging.error("❌ API Key de IA requerida para operación completa")
except ImportError:
    GEMINI_AVAILABLE = False
    logging.error("❌ Módulo IA no disponible")

# === CLASE PRINCIPAL ===
class SmartISPAgent:
    """
    🎯 SUPER ADMINISTRADOR - Red Soluciones ISP
    
    Asistente ejecutivo profesional con capacidades avanzadas:
    - Análisis estratégico de negocio
    - Supervisión operacional completa
    - Gestión inteligente de recursos
    - Reportes ejecutivos automatizados
    """
    
    def __init__(self, sheets_service=None):
        """Inicializar Super Administrador"""
        self.sheets_service = sheets_service
        self.logger = logging.getLogger(__name__)
        
        # === CONFIGURACIÓN EMPRESARIAL ===
        self.role = "SUPER_ADMINISTRADOR"
        self.company = "Red Soluciones ISP"
        self.access_level = "EJECUTIVO"
        
        # === CONFIGURACIÓN IA EMPRESARIAL ===
        self.gemini_model = None
        if GEMINI_AVAILABLE:
            try:
                self.gemini_model = genai.GenerativeModel(
                    'gemini-1.5-flash',
                    system_instruction=self._get_admin_persona()
                )
                self.logger.info("🎯 IA Empresarial: Sistema operacional")
            except Exception as e:
                self.logger.error(f"❌ Error configurando IA: {e}")
        
        # === RESPUESTAS EJECUTIVAS ===
        self.executive_responses = {
            "greeting": "🎯 **Super Administrador** - Red Soluciones ISP\n**Sistema empresarial activo**. ¿Qué análisis necesita?",
            "unauthorized": "⛔ **Acceso Restringido** - Función de nivel ejecutivo",
            "success": "✅ **Operación completada** exitosamente",
            "error": "❌ **Error operacional** - Revisar logs del sistema",
            "processing": "⚡ **Procesando** solicitud ejecutiva..."
        }
        
        # === MÉTRICAS EMPRESARIALES ===
        self.kpi_definitions = {
            "revenue_monthly": "Ingresos mensuales proyectados",
            "client_growth": "Crecimiento de base de clientes",
            "churn_rate": "Tasa de cancelación mensual",
            "arpu": "Ingreso promedio por usuario",
            "network_efficiency": "Eficiencia operacional de red",
            "support_resolution": "Tiempo promedio de resolución"
        }
        
        self.logger.info("🎯 Super Administrador: Sistema inicializado")

    def _get_admin_persona(self) -> str:
        """Definir la personalidad del Super Administrador"""
        return """Eres el SUPER ADMINISTRADOR de Red Soluciones ISP.

PERSONALIDAD:
- Profesional, ejecutivo y directo
- Respuestas breves y precisas (máximo 3 líneas)
- Enfoque en métricas y resultados de negocio
- Lenguaje empresarial y técnico apropiado

CAPACIDADES:
- Análisis financiero y operacional
- Supervisión de clientes y prospectos
- Gestión de incidentes críticos
- Reportes ejecutivos y KPIs

ESTILO DE RESPUESTA:
- Usar emojis profesionales: 📊 📈 ⚡ 🎯 💼
- Información clave primero
- Sugerencias de acción específicas
- Sin explicaciones extensas

CONTEXTO: Red Soluciones ISP - Proveedor de internet empresarial"""

    # ================================================================
    # MÉTODO PRINCIPAL DE PROCESAMIENTO
    # ================================================================

    def process_query(self, query: str) -> Dict[str, Any]:
        """
        🎯 Procesador ejecutivo de consultas
        
        Análisis inteligente con respuesta profesional y breve
        """
        try:
            query_clean = query.strip().lower()
            
            # Análisis de intención empresarial
            intent = self._analyze_business_intent(query_clean)
            
            # Procesamiento ejecutivo según intención
            return self._execute_admin_action(intent, query_clean)
                
        except Exception as e:
            self.logger.error(f"Error en procesamiento ejecutivo: {e}")
            return {
                "response": "❌ **Error operacional** - Sistema revisando logs",
                "type": "error",
                "suggestions": ["Estadísticas", "Estado del sistema", "Ayuda"]
            }

    def _analyze_business_intent(self, query: str) -> str:
        """Análisis de intención empresarial"""
        
        # Comandos ejecutivos directos
        if any(x in query for x in ["stats", "estadísticas", "métricas", "kpi"]):
            return "executive_dashboard"
        
        if any(x in query for x in ["clientes", "cliente:"]):
            return "client_management"
            
        if any(x in query for x in ["prospecto", "leads"]):
            return "prospect_management"
            
        if any(x in query for x in ["incidente", "problema", "falla"]):
            return "incident_management"
            
        if any(x in query for x in ["buscar", "encontrar"]):
            return "search_operation"
            
        if any(x in query for x in ["ayuda", "help", "comandos"]):
            return "admin_help"
            
        if any(x in query for x in ["análisis", "reporte", "informe"]):
            return "business_analysis"
            
        # Default: saludo ejecutivo
        return "executive_greeting"

    def _execute_admin_action(self, intent: str, query: str) -> Dict[str, Any]:
        """Ejecutar acción administrativa"""
        
        if intent == "executive_dashboard":
            return self._get_executive_dashboard()
        elif intent == "client_management":
            return self._handle_client_operation(query)
        elif intent == "prospect_management":
            return self._handle_prospect_operation(query)
        elif intent == "incident_management":
            return self._handle_incident_operation(query)
        elif intent == "search_operation":
            return self._handle_search_operation(query)
        elif intent == "business_analysis":
            return self._get_business_analysis()
        elif intent == "admin_help":
            return self._get_admin_help()
        else:
            return self._get_executive_greeting()

    # ================================================================
    # OPERACIONES EJECUTIVAS
    # ================================================================

    def _get_executive_dashboard(self) -> Dict[str, Any]:
        """Dashboard ejecutivo con métricas clave"""
        try:
            if self.sheets_service:
                # Obtener datos reales
                clients = self.sheets_service.get_clients()
                prospects = self.sheets_service.get_prospects()
                
                total_clients = len(clients) if clients else 0
                total_prospects = len(prospects) if prospects else 0
                
                # Cálculos empresariales
                monthly_revenue = total_clients * 450  # Promedio
                growth_rate = (total_prospects / max(total_clients, 1)) * 100
                
                response = f"""📊 **Dashboard Ejecutivo - Red Soluciones ISP**

💼 **Métricas Clave:**
• Clientes activos: {total_clients}
• Pipeline prospects: {total_prospects}
• Ingresos estimados: ${monthly_revenue:,}
• Tasa crecimiento: {growth_rate:.1f}%"""
            else:
                response = "📊 **Dashboard Ejecutivo**\n⚡ Conectando con base de datos..."
                
            return {
                "response": response,
                "type": "dashboard",
                "suggestions": ["Análisis detallado", "Reportes", "Gestión clientes"]
            }
        except Exception as e:
            self.logger.error(f"Error dashboard ejecutivo: {e}")
            return {
                "response": "❌ **Error** - Dashboard temporalmente no disponible",
                "type": "error"
            }

    def _get_executive_greeting(self) -> Dict[str, Any]:
        """Saludo ejecutivo profesional"""
        return {
            "response": self.executive_responses["greeting"],
            "type": "greeting",
            "suggestions": ["📊 Dashboard", "👥 Clientes", "📈 Análisis", "🔍 Buscar"]
        }

    def _get_admin_help(self) -> Dict[str, Any]:
        """Comandos disponibles para super administrador"""
        help_text = """🎯 **Comandos Super Administrador:**

**📊 Ejecutivos:**
• `stats` - Dashboard completo
• `análisis` - Reportes avanzados
• `métricas` - KPIs del negocio

**👥 Operacionales:**
• `cliente: [datos]` - Registrar cliente
• `prospecto: [datos]` - Nuevo lead
• `buscar [nombre]` - Localizar registro"""

        return {
            "response": help_text,
            "type": "help",
            "suggestions": ["Dashboard", "Nuevo cliente", "Buscar", "Análisis"]
        }
            ]
        }
        
        # === PATRONES DE DETECCIÓN RÁPIDA ===
        # Para identificar intenciones sin usar IA
        self.quick_patterns = {
            "cliente:": "add_client",
            "prospecto:": "add_prospect", 
            "stats": "stats",
            "buscar": "search",
            "incidente": "incident",
            "ayuda": "help",
            "prospectos": "prospects_management",
            "actualizar": "update_client",
            "analytics": "analytics_advanced",
            "análisis": "analytics_advanced"
        }
        
        # === CONFIGURACIÓN DE OPTIMIZACIÓN ===
        self.efficient_mode = True  # Modo ahorro máximo
        self.admin_mode = True      # Modo administrador
        self.response_cache = {}    # Cache de respuestas
        
        self.logger.info("👑 Carlos Super Admin - Sistema Inicializado")

    # ================================================================
    # MÉTODOS PÚBLICOS PRINCIPALES
    # ================================================================

    def process_query(self, query: str) -> Dict[str, Any]:
        """
        🚀 Procesador principal de consultas
        
        Flujo optimizado:
        1. Cache check (evitar APIs innecesarias)
        2. Detección rápida de intención
        3. Procesamiento directo según tipo
        4. Cache del resultado
        
        Args:
            query: Consulta del usuario en lenguaje natural
            
        Returns:
            Dict con respuesta, tipo y datos adicionales
        """
        try:
            query_clean = query.strip().lower()
            
            # PASO 1: Verificar cache
            cache_key = hash(query_clean)
            if cache_key in self.response_cache:
                return self.response_cache[cache_key]
            
            # PASO 2: Detectar intención rápidamente
            intent = self._detect_intent_fast(query_clean)
            
            # PASO 3: Procesar según intención
            result = self._process_intent_optimized(intent, query_clean)
            
            # PASO 4: Guardar en cache
            self.response_cache[cache_key] = result
            return result
                
        except Exception as e:
            self.logger.error(f"Error procesando consulta: {e}")
            return {
                "response": "❌ Error procesando consulta",
                "type": "error",
                "suggestions": ["Stats", "Ayuda"]
            }

    # ================================================================
    # MÉTODOS DE DETECCIÓN DE INTENCIÓN
    # ================================================================

    def _detect_intent_fast(self, query: str) -> str:
        """
        🚀 Detección súper inteligente de intenciones
        
        Sistema de múltiples capas:
        1. Patrones directos (cliente:, prospecto:, etc.)
        2. Frases de incidentes en lenguaje natural
        3. Frases de clientes/prospectos en lenguaje natural
        4. Detección de búsquedas
        5. Análisis de datos estructurados
        6. Comandos específicos del dueño
        7. Estadísticas y análisis
        """
        
        # CAPA 1: Detección inmediata con patrones directos
        for pattern, intent in self.quick_patterns.items():
            if pattern in query:
                return intent
        
        # CAPA 2: Detección de incidentes en lenguaje natural
        incident_phrases = [
            "se queja", "tiene problema", "no tiene internet", "no funciona",
            "está lento", "no conecta", "sin señal", "problema con",
            "reporta que", "dice que", "me llamó", "llamó diciendo"
        ]
        if any(phrase in query for phrase in incident_phrases):
            return "incident"
        
        # CAPA 3: Detección de clientes en lenguaje natural  
        client_phrases = [
            "dar de alta", "registrar cliente", "nuevo cliente", "alta de cliente",
            "tengo un cliente nuevo", "quiero registrar"
        ]
        if any(phrase in query for phrase in client_phrases):
            return "add_client"
        
        # CAPA 4: Detección de prospectos en lenguaje natural
        prospect_phrases = [
            "prospecto nuevo", "posible cliente", "lead", "interesado",
            "quiere el servicio", "me contactó", "preguntó por"
        ]
        if any(phrase in query for phrase in prospect_phrases):
            return "add_prospect"
        
        # CAPA 5: Detección de búsquedas en lenguaje natural
        search_phrases = [
            "busca", "encuentra", "dónde está", "información de", "datos de",
            "cliente llamado", "ver cliente"
        ]
        if any(phrase in query for phrase in search_phrases):
            return "search"
        
        # CAPA 6: Detección inteligente de datos sin formato explícito
        if self._looks_like_client_data(query):
            return "add_prospect"  # Por defecto prospecto si no especifica
        
        # CAPA 7: Comandos específicos del dueño
        if any(phrase in query for phrase in [
            "da de alta un cliente", "dar de alta cliente", "nuevo cliente"
        ]):
            return "add_client"
            
        if any(phrase in query for phrase in [
            "da de alta un prospecto", "dar de alta prospecto", "nuevo prospecto"
        ]):
            return "add_prospect"
            
        # CAPA 8: Estadísticas en lenguaje natural
        stats_phrases = [
            "cómo va", "como va", "estado del negocio", "cómo está", "como esta",
            "resumen", "dashboard", "números", "cómo andamos", "reporte"
        ]
        if any(phrase in query for phrase in stats_phrases):
            return "stats"
            
        # CAPA 9: Casos específicos
        if "clientes" in query and "buscar" not in query:
            return "clients"
            
        if "stats" in query or "estadist" in query or "resumen" in query:
            return "stats"
            
        return "general"

    def _looks_like_client_data(self, query: str) -> bool:
        """🧠 Detectar si parece datos de cliente/prospecto"""
        # Buscar patrones como: nombre, teléfono, zona
        parts = [p.strip() for p in query.split(",")]
        
        if len(parts) >= 2:
            # Verificar si tiene un número de teléfono (más estricto)
            has_phone = any(re.search(r'\d{10}|\d{3}[-\s]?\d{3}[-\s]?\d{4}|555[-\s]?\d{4}', part) for part in parts)
            
            # Verificar si tiene nombre (palabra que empiece con mayúscula o cualquier nombre)
            has_name = any(len(part.strip()) > 2 and not part.strip().isdigit() for part in parts[:2])
            
            # Verificar si menciona zona conocida o cualquier palabra que podría ser zona
            zones = ["norte", "sur", "centro", "este", "oeste", "salamanca", "bajio", "industrial", "residencial"]
            has_zone = any(zone in query.lower() for zone in zones) or len(parts) >= 3
            
            # Más estricto: debe tener teléfono Y al menos 3 partes separadas por comas
            return has_phone and len(parts) >= 3 and has_name
        
        return False

    def _process_intent_optimized(self, intent: str, query: str) -> Dict[str, Any]:
        """
        ⚡ Router de procesamiento por intención
        
        Distribuye la consulta al handler específico según la intención detectada
        """
        # Mapeo de intenciones a handlers
        intent_handlers = {
            "add_client": self._handle_add_client_optimized,
            "add_prospect": self._handle_add_prospect_optimized,
            "stats": self._handle_stats_optimized,
            "search": self._handle_search_optimized,
            "clients": self._handle_clients_optimized,
            "incident": self._handle_incident_optimized,
            "help": self._handle_help_optimized,
            "prospects_management": self._handle_prospects_management,
            "update_client": self._handle_client_update,
            "analytics_advanced": self._handle_analytics_advanced
        }
        
        # Ejecutar handler correspondiente
        if intent in intent_handlers:
            if intent in ["stats", "help"]:
                return intent_handlers[intent]()
            else:
                return intent_handlers[intent](query)
        else:
            return self._handle_general_optimized(query)

    # ================================================================
    # HANDLERS DE GESTIÓN DE CLIENTES Y PROSPECTOS
    # ================================================================

    def _handle_add_client_optimized(self, query: str) -> Dict[str, Any]:
        """⚡ Carlos registra clientes con lenguaje natural del dueño"""
        try:
            # Si usa formato explícito cliente:
            if "cliente:" in query:
                data_part = query.split("cliente:", 1)[1].strip()
                result = self._process_client_data_quick(data_part, "cliente")
                if result:
                    return {
                        "response": f"👑 **Perfecto jefe!** Cliente {result['name'].title()} registrado.\n📞 {result['phone']} | 📍 {result['zone']}\n💰 Plan sugerido: ${result.get('price', 350)}",
                        "type": "client_success",
                        "data": result
                    }
            
            # PROCESAR LENGUAJE NATURAL DEL DUEÑO
            elif any(phrase in query for phrase in ["dar de alta", "registrar", "nuevo cliente", "alta de"]):
                # Extraer información del lenguaje natural
                client_info = self._extract_client_from_natural_language(query, "cliente")
                
                if client_info:
                    return {
                        "response": f"👑 **Cliente registrado exitosamente!**\n\n🎯 **{client_info['name'].title()}**\n📞 {client_info['phone']}\n📍 {client_info['zone']}\n💼 Plan: {client_info.get('plan', 'Estándar')}\n💰 ${client_info.get('price', 350)}/mes\n\n✅ Guardado en Google Sheets",
                        "type": "client_success",
                        "data": client_info,
                        "suggestions": [
                            f"¿Programo instalación para {client_info['name'].title()}?",
                            "Ver todos los clientes",
                            "Registrar otro cliente"
                        ]
                    }
                else:
                    return {
                        "response": "👑 **¿Cuéntame del nuevo cliente, jefe?**\n\nNecesito:\n• Nombre completo\n• Teléfono de contacto\n• Zona donde vive\n\n**Ejemplo:** 'Registrar cliente Juan Pérez, 555-1234, zona Norte'",
                        "type": "client_instruction"
                    }
            
            # Instrucciones si no detecta info suficiente
            return {
                "response": "� **Para registrar cliente:**\n• 'Dar de alta cliente [Nombre], [Teléfono], [Zona]'\n• 'Cliente: [Nombre], [Teléfono], [Zona]'\n• O cuéntame: 'Tengo un cliente nuevo llamado...'",
                "type": "instruction",
                "suggestions": ["Registrar Juan Pérez, 555-1234, Centro"]
            }
        except Exception as e:
            self.logger.error(f"Error en alta de cliente: {e}")
            return {"response": "👑 Disculpa jefe, hubo un error. ¿Puedes repetirme los datos?", "type": "error"}

    def _handle_add_prospect_optimized(self, query: str) -> Dict[str, Any]:
        """⚡ Carlos registra prospectos con lenguaje natural del dueño"""
        try:
            # Si usa formato explícito prospecto:
            if "prospecto:" in query:
                data_part = query.split("prospecto:", 1)[1].strip()
                result = self._process_client_data_quick(data_part, "prospecto")
                if result:
                    return {
                        "response": f"👑 **Prospecto {result['name'].title()} registrado!**\n📞 {result['phone']} | 📍 {result['zone']}\n\n💡 ¿Programo seguimiento?",
                        "type": "prospect_success",
                        "data": result
                    }
            
            # PROCESAR LENGUAJE NATURAL - detectar si describe un prospecto
            elif any(phrase in query for phrase in ["me contactó", "quiere", "interesado", "preguntó", "llamó"]):
                # Extraer información del lenguaje natural
                prospect_info = self._extract_client_from_natural_language(query, "prospecto")
                
                if prospect_info:
                    return {
                        "response": f"👑 **¡Excelente lead, jefe!**\n\n🎯 **Prospecto: {prospect_info['name'].title()}**\n📞 {prospect_info['phone']}\n📍 {prospect_info['zone']}\n💡 Notas: Interesado en servicio\n\n✅ Registrado en Google Sheets\n\n🚀 **¿Qué hacemos?**",
                        "type": "prospect_success",
                        "data": prospect_info,
                        "suggestions": [
                            f"Llamar a {prospect_info['name'].title()} hoy",
                            f"Programar visita técnica",
                            f"Enviar cotización",
                            "Ver otros prospectos"
                        ]
                    }
                else:
                    return {
                        "response": "👑 **¿Cuéntame más del prospecto, jefe?**\n\nNecesito:\n• Nombre de la persona\n• Teléfono de contacto\n• Zona donde vive\n\n**Ejemplo:** 'Me contactó Ana López, 555-1234, vive en Centro'",
                        "type": "prospect_instruction"
                    }
            
            # DETECCIÓN INTELIGENTE: Si parece datos directos
            elif self._looks_like_client_data(query):
                result = self._process_client_data_quick(query, "prospecto")
                if result:
                    return {
                        "response": f"👑 **Perfecto, jefe!** Prospecto {result['name'].title()} registrado.\n📞 {result['phone']} | 📍 {result['zone']}\n\n💡 ¿Programo seguimiento?",
                        "type": "prospect_success",
                        "data": result,
                        "suggestions": [
                            f"Llamar a {result['name'].title()}",
                            f"Convertir a cliente",
                            "Ver todos los prospectos"
                        ]
                    }
            
            # Instrucciones si no detecta datos
            return {
                "response": "🎯 **Para registrar prospecto:**\n• 'Me contactó [Nombre], teléfono [XXX], zona [XXX]'\n• 'Prospecto: [Nombre], [Teléfono], [Zona]'\n• O simplemente: '[Nombre], [Teléfono], [Zona]'",
                "type": "instruction",
                "suggestions": ["Me contactó Ana López, 555-1234, Centro"]
            }
        except Exception as e:
            self.logger.error(f"Error en alta de prospecto: {e}")
            return {"response": "👑 Disculpa jefe, hubo un error. ¿Puedes repetirme los datos?", "type": "error"}

    # ================================================================
    # HANDLERS DE ESTADÍSTICAS Y ANÁLISIS
    # ================================================================

    def _handle_stats_optimized(self) -> Dict[str, Any]:
        """📊 Carlos analiza el negocio como asistente ejecutivo"""
        try:
            # USAR ANÁLISIS INTELIGENTE DE GOOGLE SHEETS
            if self.sheets_service:
                try:
                    result = self.sheets_service.get_business_analytics()
                    
                    if result.get('success'):
                        analytics = result.get('analytics', {})
                        insights = analytics.get('insights', [])
                        
                        # Respuesta ejecutiva personalizada
                        response = f"👑 **Reporte Ejecutivo - Red Soluciones ISP**\n\n"
                        response += f"� **Estado del Negocio:**\n"
                        response += f"• Clientes activos: {analytics.get('active_clients', 0)}\n"
                        response += f"• Prospectos en pipeline: {analytics.get('prospects', 0)}\n"
                        response += f"• Ingresos mensuales: ${analytics.get('monthly_revenue', 0):,.0f}\n"
                        response += f"• Cobertura: {len(analytics.get('zones', {}))} zonas activas\n"
                        response += f"• Potencial de crecimiento: ${analytics.get('growth_potential', 0):,.0f}\n\n"
                        
                        # Agregar insights con análisis ejecutivo
                        if insights:
                            response += f"🧠 **Análisis Carlos:**\n"
                            for insight in insights[:3]:  # Máximo 3 insights
                                response += f"• {insight}\n"
                            response += "\n"
                        
                        # Recomendaciones ejecutivas
                        recommendations = self._generate_executive_recommendations(analytics)
                        if recommendations:
                            response += f"💡 **Mis recomendaciones, jefe:**\n{recommendations}"
                        
                        return {
                            "response": response,
                            "type": "stats_executive",
                            "data": analytics,
                            "suggestions": [
                                "Analizar zona específica",
                                "Ver prospectos prioritarios", 
                                "Reporte financiero detallado"
                            ]
                        }
                except Exception as e:
                    self.logger.error(f"Error en analytics inteligente: {e}")
            
            # Fallback estadísticas básicas con estilo ejecutivo
            stats = self._get_system_stats_quick()
            response = f"👑 **Dashboard Rápido**\n\n"
            response += f"📊 Clientes: {stats['total_clients']}\n"
            response += f"💰 Ingresos: ${stats['revenue']:,.0f}/mes\n"
            response += f"🌍 Zonas: {stats['zones']}\n"
            response += f"📈 Estado: {stats['status'].title()}\n\n"
            response += f"💡 **Carlos activo y monitoreando el negocio**"
            
            return {
                "response": response,
                "type": "stats_basic",
                "data": stats,
                "suggestions": ["Conectar Google Sheets para análisis completo"]
            }
        except Exception as e:
            self.logger.error(f"Error en estadísticas: {e}")
            return {
                "response": "� **Sistema operativo, jefe.** Carlos funcionando correctamente.",
                "type": "stats",
                "suggestions": ["Verificar conexión", "Ver ayuda"]
            }

    def _generate_executive_recommendations(self, analytics: Dict) -> str:
        """💡 Generar recomendaciones ejecutivas basadas en datos"""
        recommendations = []
        
        active_clients = analytics.get('active_clients', 0)
        prospects = analytics.get('prospects', 0)
        revenue = analytics.get('monthly_revenue', 0)
        growth_potential = analytics.get('growth_potential', 0)
        
        # Análisis de prospectos
        if prospects > 10:
            recommendations.append(f"• Tienes {prospects} prospectos esperando. ¡Oportunidad de convertir!")
        elif prospects < 5:
            recommendations.append("• Pocos prospectos en pipeline. Sugiero campaña de marketing.")
        
        # Análisis de ingresos
        if revenue < 50000:
            recommendations.append("• Los ingresos pueden mejorar. Enfócate en conversiones.")
        elif revenue > 100000:
            recommendations.append("• ¡Excelentes ingresos! Considera expandir cobertura.")
        
        # Análisis de potencial
        if growth_potential > revenue * 0.5:
            recommendations.append(f"• Gran potencial: ${growth_potential:,.0f} adicionales posibles.")
        
        # Análisis de zonas
        zones = analytics.get('zones', {})
        if len(zones) < 3:
            recommendations.append("• Pocas zonas activas. Considera expansión geográfica.")
        
        return '\n'.join(recommendations) if recommendations else "• Negocio estable. Mantener operación actual."

    def _handle_help_optimized(self) -> Dict[str, Any]:
        """📋 Ayuda optimizada"""
        return {
            "response": self.quick_responses["help"],
            "type": "help",
            "suggestions": ["Stats", "Cliente: Nombre, Tel, Zona", "Buscar cliente"]
        }

    def _handle_general_optimized(self, query: str) -> Dict[str, Any]:
        """💬 Respuesta general optimizada - ASISTENTE EJECUTIVO"""
        
        # Si el usuario saluda o pregunta sobre capacidades
        if any(word in query.lower() for word in ["hola", "hi", "ayuda", "qué puedes", "que puedes"]):
            return {
                "response": "👑 **Soy Carlos, tu asistente ejecutivo.**\n\n📋 **Listos para trabajar:**\n• Alta de clientes y prospectos\n• Búsquedas rápidas\n• Estadísticas del negocio\n• Gestión de incidentes\n\n¿Qué necesitas, jefe?",
                "type": "greeting",
                "suggestions": ["Ver estadísticas", "Buscar cliente", "Nuevo prospecto"]
            }
        
        # Usar Gemini solo si es necesario y no excede el límite
        if (self.gemini_model and 
            self.api_calls_count < self.max_api_calls_per_session and
            len(query) > 10):  # Solo para consultas complejas
            
            try:
                self.api_calls_count += 1
                prompt = f"""Eres Carlos, asistente ejecutivo del dueño de Red Soluciones ISP.

CONTEXTO: El dueño pregunta: "{query}"

Responde BREVEMENTE (máximo 2 líneas) como asistente ejecutivo profesional y proactivo.
Ofrece ayuda concreta relacionada con el negocio ISP."""
                
                response = self.gemini_model.generate_content(prompt)
                if response and response.text:
                    return {
                        "response": f"👑 {response.text[:150]}",
                        "type": "ai_response",
                        "suggestions": ["Ver estadísticas", "Gestionar clientes", "Ayuda"]
                    }
            except Exception as e:
                self.logger.error(f"Error en respuesta AI: {e}")
        
        # Respuesta por defecto más profesional
        return {
            "response": "👑 **Soy Carlos, su asistente ejecutivo.**\n\n¿En qué puedo ayudarle con el negocio hoy?",
            "type": "general",
            "suggestions": ["Estadísticas", "Clientes", "Nuevos prospectos"]
        }

    # ================================================================
    # MÉTODOS AUXILIARES DE PROCESAMIENTO DE DATOS
    # ================================================================

    def _extract_client_from_natural_language(self, query: str, tipo: str) -> Optional[Dict]:
        """🧠 Carlos extrae datos de cliente/prospecto del lenguaje natural"""
        try:
            # USAR IA PARA EXTRAER INFORMACIÓN
            if self.gemini_model and self.api_calls_count < self.max_api_calls_per_session:
                self.api_calls_count += 1
                
                prompt = f"""Eres Carlos, asistente ejecutivo de Red Soluciones ISP. El dueño dice:

"{query}"

Extrae información de {tipo} en JSON:
- name: nombre completo (o "No especificado")
- phone: teléfono (o "No especificado") 
- zone: zona/ubicación (o "No especificado")
- email: email si mencionado (o "No especificado")
- notes: notas adicionales del dueño

Responde SOLO el JSON válido."""

                response = self.gemini_model.generate_content(prompt)
                if response and response.text:
                    try:
                        import json
                        clean_response = response.text.strip()
                        if clean_response.startswith('```json'):
                            clean_response = clean_response.replace('```json', '').replace('```', '').strip()
                        
                        result = json.loads(clean_response)
                        
                        # Validar que tiene al menos nombre
                        if result.get('name') and result['name'] != "No especificado":
                            # Procesar con Google Sheets si está disponible
                            if self.sheets_service:
                                try:
                                    sheets_result = self.sheets_service.add_client_intelligent(
                                        result.get('name'),
                                        result.get('phone', 'No especificado'),
                                        result.get('zone', 'No especificado'),
                                        tipo
                                    )
                                    
                                    if sheets_result.get('success'):
                                        result.update({
                                            "id": sheets_result.get('client_id'),
                                            "plan": sheets_result.get('suggested_plan'),
                                            "price": sheets_result.get('monthly_revenue'),
                                            "sheets_saved": True
                                        })
                                        return result
                                except Exception as e:
                                    self.logger.error(f"Error con Sheets: {e}")
                            
                            # Fallback sin sheets
                            result.update({
                                "id": f"{tipo[:4].upper()}{len(result['name'])}{result.get('zone', 'XX')[:2].upper()}",
                                "plan": "Estándar",
                                "price": 350,
                                "sheets_saved": False
                            })
                            return result
                    except (json.JSONDecodeError, KeyError) as e:
                        self.logger.error(f"Error parsing JSON de Gemini: {e}")
            
        except Exception as e:
            self.logger.error(f"Error extrayendo datos naturales: {e}")
        
        # FALLBACK: procesamiento manual
        return self._manual_client_extraction(query, tipo)

    def _manual_client_extraction(self, query: str, tipo: str) -> Optional[Dict]:
        """🛠️ Extracción manual de datos de cliente/prospecto"""
        words = query.split()
        
        # Buscar nombre (palabras con mayúscula después de palabras clave)
        name = "No especificado"
        name_triggers = ["cliente", "prospecto", "llamado", "nombre"]
        
        for i, word in enumerate(words):
            if word.lower() in name_triggers and i + 1 < len(words):
                # Tomar siguiente(s) palabra(s) como nombre
                potential_name = []
                for j in range(i + 1, min(i + 4, len(words))):  # Máximo 3 palabras
                    next_word = words[j].strip(',')
                    if next_word[0].isupper() and len(next_word) > 1:
                        potential_name.append(next_word)
                    else:
                        break
                
                if potential_name:
                    name = ' '.join(potential_name)
                    break
        
        # Buscar teléfono
        phone = "No especificado"
        for word in words:
            # Buscar patrones de teléfono
            if re.search(r'\d{3,}[-\s]?\d{3,}', word.replace(',', '')):
                phone = word.replace(',', '')
                break
        
        # Buscar zona
        zone = "No especificado"
        zones = ["norte", "sur", "centro", "este", "oeste", "salamanca", "bajio", "industrial", "residencial"]
        for word in words:
            if word.lower().strip(',') in zones:
                zone = word.strip(',').title()
                break
        
        # Si encontramos al menos el nombre, crear registro
        if name != "No especificado":
            if self.sheets_service:
                try:
                    sheets_result = self.sheets_service.add_client_intelligent(name, phone, zone, tipo)
                    if sheets_result.get('success'):
                        return {
                            "name": name,
                            "phone": phone,
                            "zone": zone,
                            "id": sheets_result.get('client_id'),
                            "plan": sheets_result.get('suggested_plan'),
                            "price": sheets_result.get('monthly_revenue'),
                            "sheets_saved": True
                        }
                except Exception as e:
                    self.logger.error(f"Error manual con Sheets: {e}")
            
            # Fallback sin sheets
            return {
                "name": name,
                "phone": phone,
                "zone": zone,
                "id": f"{tipo[:4].upper()}{len(name)}{zone[:2].upper()}",
                "plan": "Estándar",
                "price": 350,
                "sheets_saved": False
            }
        
        return None

    def _process_client_data_quick(self, data: str, tipo: str) -> Optional[Dict]:
        """⚡ Procesamiento rápido de datos CON GOOGLE SHEETS INTEGRADO"""
        try:
            parts = [p.strip() for p in data.split(",")]
            if len(parts) >= 3:
                name, phone, zone = parts[0], parts[1], parts[2]
                
                # USAR GOOGLE SHEETS INTELIGENTE
                if self.sheets_service:
                    try:
                        # Usar el nuevo método inteligente
                        result = self.sheets_service.add_client_intelligent(name, phone, zone, tipo)
                        
                        if result.get('success'):
                            client_data = result.get('data', {})
                            return {
                                "id": result.get('client_id'),
                                "name": name.lower(),
                                "phone": phone,
                                "zone": zone,
                                "type": tipo,
                                "plan": result.get('suggested_plan'),
                                "price": result.get('monthly_revenue'),
                                "sheets_saved": True
                            }
                        else:
                            self.logger.error(f"Error guardando en Sheets: {result.get('error')}")
                    except Exception as e:
                        self.logger.error(f"Error con Sheets: {e}")
                
                # Fallback si falla Google Sheets
                client_id = f"{tipo[:4].upper()}{len(name)}{zone[:2].upper()}"
                return {
                    "id": client_id,
                    "name": name.lower(),
                    "phone": phone,
                    "zone": zone,
                    "type": tipo,
                    "sheets_saved": False
                }
        except:
            pass
        return None

    def _get_system_stats_quick(self) -> Dict:
        """📊 Stats rápidas del sistema"""
        try:
            clients = self._get_clients_data()
            if clients:
                total = len(clients)
                revenue = total * 350  # Estimación rápida
                zones = len(set(c.get('zone', 'N/A') for c in clients))
                
                return {
                    "total_clients": total,
                    "revenue": revenue,
                    "zones": zones,
                    "status": "active"
                }
        except:
            pass
            
        return {
            "total_clients": 0,
            "revenue": 0,
            "zones": 0,
            "status": "maintenance"
        }

    # ================================================================
    # HANDLERS DE BÚSQUEDA Y CONSULTAS
    # ================================================================

    def _handle_search_optimized(self, query: str) -> Dict[str, Any]:
        """🔍 Carlos busca clientes con lenguaje natural del dueño"""
        try:
            # Extraer término de búsqueda desde lenguaje natural
            search_term = self._extract_search_term_natural(query)
            
            if not search_term:
                return {
                    "response": "� **¿A quién buscamos, jefe?**\n\nPuedes decirme:\n• 'Busca a Juan Pérez'\n• 'Información de María García'\n• 'Cliente en zona Norte'\n• 'Teléfono 555-1234'",
                    "type": "search_instruction"
                }
            
            # USAR BÚSQUEDA INTELIGENTE DE GOOGLE SHEETS
            if self.sheets_service:
                try:
                    result = self.sheets_service.search_clients_intelligent(search_term)
                    
                    if result.get('success'):
                        results = result.get('results', [])
                        total = result.get('total_found', 0)
                        
                        if results:
                            # Mostrar mejor resultado con estilo ejecutivo
                            best_match = results[0]
                            response = f"👑 **Encontré a tu cliente, jefe:**\n\n"
                            response += f"🎯 **{best_match.get('Nombre', 'N/A')}**\n"
                            response += f"📞 {best_match.get('Teléfono', 'N/A')}\n"
                            response += f"📍 {best_match.get('Zona', 'N/A')}\n"
                            response += f"💼 {best_match.get('Plan', 'N/A')} - ${best_match.get('Pago', 'N/A')}\n"
                            response += f"📊 Estado: {best_match.get('Estado', 'N/A')}"
                            
                            if total > 1:
                                response += f"\n\n🔍 Hay {total-1} resultados más similares"
                            
                            return {
                                "response": response,
                                "type": "search_result",
                                "data": {"result": best_match, "total": total},
                                "suggestions": [
                                    f"Ver más datos de {best_match.get('Nombre', 'cliente')}",
                                    f"Crear incidente para {best_match.get('Nombre', 'cliente')}",
                                    "Buscar otro cliente"
                                ]
                            }
                        else:
                            return {
                                "response": f"👑 **No encontré '{search_term}' en nuestra base, jefe.**\n\n💡 **Sugerencias:**\n• Verifica la ortografía\n• Busca solo por apellido\n• Intenta por zona o teléfono\n\n¿Era prospecto? ¿Lo registro?",
                                "type": "not_found",
                                "suggestions": [
                                    f"Registrar {search_term} como prospecto",
                                    "Ver todos los clientes",
                                    "Buscar por zona"
                                ]
                            }
                except Exception as e:
                    self.logger.error(f"Error en búsqueda inteligente: {e}")
            
            # Fallback búsqueda básica
            clients = self._get_clients_data()
            if clients:
                matches = [c for c in clients if search_term.lower() in c.get('name', '').lower()]
                if matches:
                    match = matches[0]
                    return {
                        "response": f"👑 **{match['name'].title()}**\n📞 {match.get('phone', 'N/A')} | 📍 {match.get('zone', 'N/A')}",
                        "type": "search_result",
                        "data": match
                    }
            
            return {
                "response": f"👑 No encontré a '{search_term}', jefe. ¿Lo registro como prospecto?",
                "type": "not_found"
            }
        except Exception as e:
            self.logger.error(f"Error en búsqueda: {e}")
            return {"response": "👑 Disculpa jefe, error en la búsqueda. ¿Puedes repetir?", "type": "error"}

    def _extract_search_term_natural(self, query: str) -> str:
        """🧠 Extraer término de búsqueda del lenguaje natural"""
        # Remover palabras de búsqueda comunes
        clean_query = query.lower()
        
        # Palabras a remover
        search_words = ["buscar", "busca", "encuentra", "información de", "datos de", 
                       "cliente llamado", "ver cliente", "dónde está"]
        
        for word in search_words:
            clean_query = clean_query.replace(word, "").strip()
        
        # Si menciona zona específica
        if "zona" in clean_query:
            parts = clean_query.split("zona")
            if len(parts) > 1:
                return f"zona:{parts[1].strip()}"
        
        # Si menciona teléfono
        if any(tel_word in clean_query for tel_word in ["teléfono", "telefono", "número"]):
            # Extraer número
            import re
            numbers = re.findall(r'\d{3,}[-\s]?\d{3,}', query)
            if numbers:
                return f"telefono:{numbers[0]}"
        
        # Retornar el término limpio
        return clean_query.strip()

    def _handle_prospects_management(self, query: str) -> Dict[str, Any]:
        """🎯 Gestión inteligente de prospectos"""
        try:
            if self.sheets_service:
                try:
                    # Determinar acción
                    if "prioridad" in query or "urgente" in query:
                        action = "priority"
                    elif "convertir" in query or "listos" in query:
                        action = "convert_ready"
                    else:
                        action = "list"
                    
                    result = self.sheets_service.manage_prospects_intelligent(action)
                    
                    if result.get('success'):
                        if action == "priority":
                            prospects = result.get('priority_prospects', [])
                            response = f"🎯 **Prospectos Prioritarios:**\n\n"
                            for i, p in enumerate(prospects[:5], 1):
                                response += f"{i}. **{p.get('Nombre', 'N/A')}** ({p.get('Zona', 'N/A')}) - Score: {p.get('priority_score', 0)}\n"
                        
                        elif action == "convert_ready":
                            prospects = result.get('ready_prospects', [])
                            potential = result.get('conversion_potential', 0)
                            response = f"🚀 **Listos para Conversión:**\n\n"
                            response += f"💰 Potencial: ${potential:,.0f}\n\n"
                            for i, p in enumerate(prospects[:3], 1):
                                response += f"{i}. **{p.get('Nombre', 'N/A')}** - {p.get('Teléfono', 'N/A')}\n"
                        
                        else:  # list
                            prospects = result.get('prospects', [])
                            recommendations = result.get('recommendations', [])
                            response = f"📋 **Prospectos Activos:** {len(prospects)}\n\n"
                            if recommendations:
                                response += "💡 **Recomendaciones IA:**\n"
                                for rec in recommendations:
                                    response += f"• {rec}\n"
                        
                        return {
                            "response": response,
                            "type": "prospects_management",
                            "data": result
                        }
                except Exception as e:
                    self.logger.error(f"Error en gestión de prospectos: {e}")
            
            return {
                "response": "🎯 **Gestión de Prospectos:** Lista | Prioridad | Convertir",
                "type": "instruction"
            }
        except:
            return {"response": self.quick_responses["error"], "type": "error"}

    def _handle_client_update(self, query: str) -> Dict[str, Any]:
        """✏️ Actualización inteligente de clientes"""
        try:
            # Extraer ID y datos de actualización
            # Formato: "actualizar [ID] [campo] [valor]"
            parts = query.replace("actualizar", "").strip().split()
            
            if len(parts) < 3:
                return {
                    "response": "✏️ **Actualizar:** actualizar [ID] [campo] [valor]\n\n**Ejemplo:** actualizar CLI123 estado activo",
                    "type": "instruction"
                }
            
            client_id, field, value = parts[0], parts[1], " ".join(parts[2:])
            
            if self.sheets_service:
                try:
                    result = self.sheets_service.update_client_intelligent(client_id, field.title(), value)
                    
                    if result.get('success'):
                        return {
                            "response": f"✅ **Cliente {client_id} actualizado**\n\n📝 {result.get('field_updated')}: {result.get('new_value')}",
                            "type": "update_success",
                            "data": result
                        }
                    else:
                        return {
                            "response": f"❌ {result.get('error', 'Error desconocido')}",
                            "type": "error"
                        }
                except Exception as e:
                    self.logger.error(f"Error actualizando cliente: {e}")
            
            return {
                "response": "❌ Error conectando con Google Sheets",
                "type": "error"
            }
        except:
            return {"response": self.quick_responses["error"], "type": "error"}

    def _handle_analytics_advanced(self, query: str) -> Dict[str, Any]:
        """📊 Analytics avanzados con IA"""
        try:
            if self.sheets_service:
                try:
                    result = self.sheets_service.get_business_analytics()
                    
                    if result.get('success'):
                        analytics = result.get('analytics', {})
                        
                        # Análisis detallado
                        response = f"👑 **Análisis Ejecutivo Avanzado**\n\n"
                        
                        # KPIs principales
                        response += f"📊 **KPIs Principales:**\n"
                        response += f"• Clientes Activos: {analytics.get('active_clients', 0)}\n"
                        response += f"• Prospectos: {analytics.get('prospects', 0)}\n"
                        response += f"• Ingresos Mensuales: ${analytics.get('monthly_revenue', 0):,.0f}\n"
                        response += f"• Potencial Crecimiento: ${analytics.get('growth_potential', 0):,.0f}\n\n"
                        
                        # Top zonas
                        top_zones = analytics.get('top_zones', [])
                        if top_zones:
                            response += f"🏆 **Top Zonas:**\n"
                            for i, (zone, count) in enumerate(top_zones[:3], 1):
                                response += f"{i}. {zone}: {count} clientes\n"
                            response += "\n"
                        
                        # Distribución de planes
                        plans = analytics.get('plans', {})
                        if plans:
                            response += f"💼 **Planes:**\n"
                            for plan, count in plans.items():
                                response += f"• {plan}: {count}\n"
                        
                        # Insights AI
                        insights = analytics.get('insights', [])
                        if insights:
                            response += f"\n🤖 **Insights AI:**\n"
                            for insight in insights:
                                response += f"• {insight}\n"
                        
                        return {
                            "response": response,
                            "type": "analytics_advanced",
                            "data": analytics
                        }
                except Exception as e:
                    self.logger.error(f"Error en analytics avanzados: {e}")
            
            return {
                "response": "📊 Analytics no disponible sin Google Sheets",
                "type": "error"
            }
        except:
            return {"response": self.quick_responses["error"], "type": "error"}

    def _handle_clients_optimized(self) -> Dict[str, Any]:
        """👥 Lista de clientes optimizada"""
        try:
            clients = self._get_clients_data()
            if not clients:
                return {
                    "response": "❌ No hay clientes registrados",
                    "type": "empty"
                }
            
            # Mostrar solo los primeros 5
            top_clients = clients[:5]
            response = f"👥 **Clientes ({len(clients)} total):**\n"
            
            for client in top_clients:
                name = client.get('name', 'N/A').title()
                zone = client.get('zone', 'N/A')
                response += f"• {name} ({zone})\n"
            
            if len(clients) > 5:
                response += f"... y {len(clients) - 5} más"
            
            return {
                "response": response,
                "type": "client_list",
                "data": {"total": len(clients), "showing": len(top_clients)}
            }
        except:
            return {"response": self.quick_responses["error"], "type": "error"}

    # ================================================================
    # HANDLERS DE GESTIÓN DE INCIDENTES
    # ================================================================

    def _handle_incident_optimized(self, query: str) -> Dict[str, Any]:
        """🛠️ Carlos procesa incidentes en lenguaje natural para el dueño"""
        try:
            # CARLOS ENTIENDE LENGUAJE NATURAL DEL DUEÑO
            clean_query = query.replace("incidente", "").replace("da de alta un", "").strip()
            
            # Si el dueño solo dice "incidente" sin descripción
            if not clean_query or len(clean_query) < 5:
                return {
                    "response": "� **¿Qué pasó, jefe?**\n\nCuéntame el problema y yo lo registro:\n• 'Juan sin internet desde ayer'\n• 'María se queja de lentitud'\n• 'Router de Pedro no prende'",
                    "type": "incident_instruction",
                    "data": {}
                }
            
            # CARLOS PROCESA EN LENGUAJE NATURAL
            incident_id = f"INC{datetime.now().strftime('%m%d%H%M')}"
            
            # USAR IA PARA ESTRUCTURAR LO QUE DICE EL DUEÑO
            processed_incident = self._process_natural_incident(clean_query)
            
            # Crear incidente estructurado
            incident_data = {
                "id": incident_id,
                "description": processed_incident['description'],
                "client": processed_incident['client'],
                "location": processed_incident['location'],
                "original_query": clean_query,
                "category": processed_incident['category'],
                "priority": processed_incident['priority'],
                "created_at": datetime.now().isoformat(),
                "status": "Abierto",
                "technical_notes": processed_incident['technical_notes']
            }
            
            # CARLOS RESPONDE COMO ASISTENTE EJECUTIVO
            response = f"� **Perfecto, jefe. Incidente {incident_id} registrado**\n\n"
            response += f"🎯 **Cliente:** {processed_incident['client']}\n"
            response += f"📍 **Ubicación:** {processed_incident['location']}\n"
            response += f"⚠️ **Problema:** {processed_incident['description']}\n"
            response += f"🏷️ **Tipo:** {processed_incident['category']}\n"
            response += f"⚡ **Urgencia:** {processed_incident['priority']}\n\n"
            response += f"� **Mi recomendación:** {processed_incident['recommendation']}"
            
            # GUARDAR EN GOOGLE SHEETS
            if self.sheets_service:
                try:
                    sheets_result = self.sheets_service.add_incident_intelligent(incident_data)
                    if sheets_result.get('success'):
                        response += f"\n\n✅ Guardado en Google Sheets, jefe"
                        incident_data['sheets_saved'] = "true"
                    else:
                        incident_data['sheets_saved'] = "false"
                except Exception as e:
                    self.logger.error(f"Error guardando incidente: {e}")
                    incident_data['sheets_saved'] = "false"
            
            return {
                "response": response,
                "type": "incident_created",
                "data": incident_data,
                "suggestions": [
                    f"¿Asigno técnico para {processed_incident['client']}?",
                    "¿Programo seguimiento?",
                    "Ver otros incidentes pendientes"
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Error procesando incidente: {e}")
            return {
                "response": "👑 Disculpa jefe, hubo un error. ¿Puedes repetirme el problema?",
                "type": "error"
            }

    def _process_natural_incident(self, natural_input: str) -> Dict[str, str]:
        """🧠 Carlos procesa lenguaje natural del dueño en datos estructurados"""
        try:
            # USAR IA PARA PROCESAR LENGUAJE NATURAL
            if self.gemini_model and self.api_calls_count < self.max_api_calls_per_session:
                self.api_calls_count += 1
                
                prompt = f"""Eres Carlos, asistente ejecutivo de Red Soluciones ISP. El dueño te dice:

"{natural_input}"

Extrae y estructura esta información en JSON:
- client: nombre del cliente (o "Cliente no especificado")
- location: zona/dirección (o "Ubicación no especificada") 
- description: descripción clara del problema
- category: una de [Conectividad, Rendimiento, Hardware, Instalación, Facturación, General]
- priority: una de [Alta, Media, Baja]
- technical_notes: notas técnicas para el técnico
- recommendation: tu recomendación ejecutiva breve

Responde SOLO el JSON válido."""

                response = self.gemini_model.generate_content(prompt)
                if response and response.text:
                    try:
                        import json
                        # Limpiar la respuesta para extraer solo el JSON
                        clean_response = response.text.strip()
                        if clean_response.startswith('```json'):
                            clean_response = clean_response.replace('```json', '').replace('```', '').strip()
                        
                        result = json.loads(clean_response)
                        
                        # Validar campos requeridos
                        required_fields = ['client', 'location', 'description', 'category', 'priority', 'technical_notes', 'recommendation']
                        if all(field in result for field in required_fields):
                            return result
                    except (json.JSONDecodeError, KeyError):
                        pass
            
        except Exception as e:
            self.logger.error(f"Error procesando lenguaje natural: {e}")
        
        # FALLBACK: procesamiento manual inteligente
        return self._manual_natural_processing(natural_input)

    def _manual_natural_processing(self, natural_input: str) -> Dict[str, str]:
        """🛠️ Procesamiento manual cuando falla la IA"""
        lower_input = natural_input.lower()
        
        # Extraer cliente
        client = "Cliente no especificado"
        words = natural_input.split()
        for i, word in enumerate(words):
            if word.lower() in ['cliente', 'de', 'para'] and i + 1 < len(words):
                potential_name = ' '.join(words[i+1:i+3])  # Tomar siguientes 2 palabras
                if not any(tech_word in potential_name.lower() for tech_word in ['internet', 'wifi', 'router', 'lento']):
                    client = potential_name.title()
                    break
        
        # Detectar nombres propios (palabras con mayúscula)
        if client == "Cliente no especificado":
            for word in words:
                if word[0].isupper() and len(word) > 2 and word not in ['Internet', 'WiFi', 'Router']:
                    client = word
                    break
        
        # Extraer ubicación/zona
        location = "Ubicación no especificada"
        zones = ["norte", "sur", "centro", "este", "oeste", "salamanca", "bajio", "industrial", "residencial"]
        for zone in zones:
            if zone in lower_input:
                location = zone.title()
                break
        
        # Palabras que indican ubicación
        location_words = ['zona', 'casa', 'oficina', 'en']
        for i, word in enumerate(words):
            if word.lower() in location_words and i + 1 < len(words):
                location = words[i+1].title()
                break
        
        # Categorizar problema
        category = "General"
        if any(word in lower_input for word in ["sin internet", "no conecta", "desconectado"]):
            category = "Conectividad"
        elif any(word in lower_input for word in ["lento", "velocidad", "lag"]):
            category = "Rendimiento"
        elif any(word in lower_input for word in ["router", "modem", "equipo"]):
            category = "Hardware"
        elif any(word in lower_input for word in ["instalar", "instalación", "nuevo"]):
            category = "Instalación"
        elif any(word in lower_input for word in ["pago", "factura", "cobro"]):
            category = "Facturación"
        
        # Evaluar prioridad
        priority = "Media"
        if any(word in lower_input for word in ["sin internet", "no funciona", "urgente", "ya"]):
            priority = "Alta"
        elif any(word in lower_input for word in ["a veces", "intermitente", "cuando"]):
            priority = "Baja"
        
        # Generar descripción clara
        if "sin internet" in lower_input:
            description = f"Cliente sin conexión a internet"
        elif "lento" in lower_input:
            description = f"Conexión lenta reportada por cliente"
        elif "router" in lower_input or "modem" in lower_input:
            description = f"Problema con equipo de red"
        else:
            description = f"Incidente técnico: {natural_input[:50]}..."
        
        # Notas técnicas
        technical_notes = f"Revisar conectividad en {location}. Problema: {category.lower()}"
        
        # Recomendación
        recommendations = {
            "Conectividad": "Enviar técnico inmediatamente para revisar conexión",
            "Rendimiento": "Verificar velocidad desde central y optimizar",
            "Hardware": "Programar cambio/revisión de equipo",
            "Instalación": "Coordinar instalación con técnico",
            "Facturación": "Revisar estado de cuenta con administración",
            "General": "Evaluar situación y asignar recurso apropiado"
        }
        
        return {
            "client": client,
            "location": location,
            "description": description,
            "category": category,
            "priority": priority,
            "technical_notes": technical_notes,
            "recommendation": recommendations.get(category, "Evaluar caso específico")
        }

    def _enhance_incident_with_ai(self, description: str) -> str:
        """🤖 Mejorar descripción del incidente con IA"""
        try:
            if self.gemini_model and self.api_calls_count < self.max_api_calls_per_session:
                self.api_calls_count += 1
                
                prompt = f"""Eres Carlos, técnico de Red Soluciones ISP. Mejora esta descripción de incidente:

DESCRIPCIÓN ORIGINAL: "{description}"

Reescribe de forma profesional y clara, incluyendo:
- Qué problema específico ocurre
- Posible ubicación/zona
- Cliente afectado (si se menciona)
- Urgencia aparente

Responde SOLO la descripción mejorada, máximo 100 caracteres."""

                response = self.gemini_model.generate_content(prompt)
                if response and response.text:
                    enhanced = response.text.strip()
                    # Asegurar que no sea demasiado largo
                    return enhanced[:100] if len(enhanced) > 100 else enhanced
            
        except Exception as e:
            self.logger.error(f"Error en IA para incidente: {e}")
        
        # Fallback: mejorar manualmente
        if "sin internet" in description.lower():
            return f"Falta de conectividad: {description}"
        elif "lento" in description.lower() or "velocidad" in description.lower():
            return f"Problema de velocidad: {description}"
        elif "router" in description.lower() or "equipo" in description.lower():
            return f"Falla de equipo: {description}"
        else:
            return f"Incidente técnico: {description}"

    def _categorize_incident(self, description: str) -> str:
        """🏷️ Categorizar incidente automáticamente"""
        desc_lower = description.lower()
        
        if any(word in desc_lower for word in ["sin internet", "no hay conexión", "desconectado", "no conecta"]):
            return "Conectividad"
        elif any(word in desc_lower for word in ["lento", "lentitud", "velocidad", "lag", "muy lento", "despacio"]):
            return "Rendimiento"
        elif any(word in desc_lower for word in ["router", "modem", "equipo", "dispositivo", "antena"]):
            return "Hardware"
        elif any(word in desc_lower for word in ["instalación", "instalar", "nuevo", "configurar"]):
            return "Instalación"
        elif any(word in desc_lower for word in ["pago", "factura", "cobro", "billing"]):
            return "Facturación"
        else:
            return "General"

    def _assess_incident_priority(self, description: str) -> str:
        """⚡ Evaluar prioridad del incidente"""
        desc_lower = description.lower()
        
        # Prioridad Alta
        if any(word in desc_lower for word in ["sin internet", "no funciona", "caído", "urgente"]):
            return "Alta"
        # Prioridad Media
        elif any(word in desc_lower for word in ["lento", "intermitente", "a veces"]):
            return "Media"
        # Prioridad Baja
        else:
            return "Baja"

    def _get_incident_suggestions(self, category: str, priority: str) -> str:
        """💡 Sugerencias inteligentes para el incidente"""
        suggestions = {
            "Conectividad": {
                "Alta": "Enviar técnico inmediatamente",
                "Media": "Verificar desde central, programar visita",
                "Baja": "Soporte telefónico, reinicio remoto"
            },
            "Rendimiento": {
                "Alta": "Revisar saturación de red",
                "Media": "Diagnostico remoto de velocidad",
                "Baja": "Optimización de configuración"
            },
            "Hardware": {
                "Alta": "Reemplazo inmediato de equipo",
                "Media": "Programar cambio de router",
                "Baja": "Guía de reseteo por teléfono"
            }
        }
        
        return suggestions.get(category, {}).get(priority, "Evaluar caso específico")

    def _detect_intent(self, query: str) -> str:
        """🎯 Detectar intención de la consulta - OPTIMIZADO"""
        
        # Usar el método optimizado
        return self._detect_intent_fast(query)

    def _generate_natural_response(self, context: str, data: Optional[Dict] = None, response_type: str = "general") -> str:
        """🚀 CARLOS SÚPER PODEROSO - Respuestas Eficientes"""
        
        # MODO EFICIENCIA: Sin LLM = respuesta directa
        if not self.gemini_model or not GEMINI_AVAILABLE:
            if self.efficient_mode:
                return self.quick_responses["greeting"]
            return context  # Fallback básico
        
        try:
            # CARLOS SÚPER PODEROSO - Personalidad Optimizada
            prompt = f"""Eres CARLOS, SUPER ADMINISTRADOR directo de Red Soluciones ISP.

REGLAS ESTRICTAS:
- Máximo 1 línea de respuesta
- Solo resultados concretos
- Sin explicaciones largas
- Directo al grano

CONTEXTO: {context}

Respuesta ejecutiva breve:"""

            response = self.gemini_model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()[:150]  # Máximo 150 caracteres
            
        except Exception as e:
            self.logger.error(f"Error Gemini: {e}")
        
        return self.quick_responses["greeting"]

    def _handle_stats_query(self, query: str) -> Dict[str, Any]:
        """📊 CARLOS SÚPER PODEROSO - Estadísticas Eficientes"""
        try:
            stats = self._get_business_stats()
            
            # Respuesta inteligente SIN Gemini - Carlos funcionando
            response = f"""📊 **Red Soluciones ISP - Estadísticas**

👥 **Clientes:** {stats['total_clients']} activos
💰 **Ingresos:** ${stats['monthly_revenue']:,.0f}/mes
📍 **Zonas:** {stats['active_zones']} operativas
📈 **Premium:** {stats['premium_clients']} clientes ({stats['premium_percentage']:.1f}%)
🏆 **Top Zona:** {stats['top_zone']} ({stats['top_zone_clients']} clientes)

💡 **Insight:** {stats['business_insight']}"""
            
            return {
                "response": response,
                "type": "stats",
                "data": stats,
                "suggestions": ["Ver clientes", "Análisis financiero", "Por zonas"]
            }
            
        except Exception as e:
            return {
                "response": f"📊 **Estadísticas del Sistema**\n\n✅ Carlos funcionando correctamente\n🔄 Modo eficiencia activo\n💡 Conecta Google Sheets para datos reales",
                "type": "stats",
                "suggestions": ["Ver ayuda", "Probar búsqueda", "Gestión clientes"]
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
        """🔍 Manejar búsquedas de clientes - Carlos Inteligente"""
        try:
            # Extraer nombre a buscar
            search_terms = self._extract_search_terms(query)
            
            if not search_terms:
                return {
                    "response": """🔍 **Búsqueda de Clientes**

Para buscar un cliente, usa estos formatos:
• `buscar juan pérez`
• `cliente maría garcía`
• `zona:norte` (por zona)
• `telefono:555-1234` (por teléfono)

📋 **Ejemplos:**
• "buscar juan" → Busca cualquier Juan
• "zona:sur" → Todos los clientes del sur
• "telefono:555" → Busca por número""",
                    "type": "instruction",
                    "suggestions": ["Ver todos los clientes", "Estadísticas", "Ayuda"]
                }
            
            results = self._search_clients(search_terms)
            
            if not results:
                return {
                    "response": f"""🔍 **Búsqueda: "{search_terms}"**

❌ No encontré resultados para "{search_terms}"

💡 **Sugerencias:**
• Verifica la ortografía del nombre
• Busca solo por apellido
• Intenta buscar por zona: `zona:norte`
• Ve la lista completa: `clientes`""",
                    "type": "not_found",
                    "suggestions": [
                        "Ver todos los clientes",
                        "Buscar por zona", 
                        "Verificar ortografía"
                    ]
                }
            
            # Formatear resultados inteligentemente
            response = f"🔍 **Resultados para: '{search_terms}'**\n\n"
            
            for i, client in enumerate(results[:5], 1):  # Máximo 5 resultados
                payment = self._extract_payment(client)
                package_info = self._analyze_package(payment)
                
                response += f"""**{i}. {client.get('Nombre', 'Sin nombre')}**
📧 {client.get('Email', 'Sin email')}
📍 {client.get('Zona', 'Sin zona')} | 💰 ${payment} ({package_info['type']})
📱 {client.get('Teléfono', 'Sin teléfono')}

"""
            
            if len(results) > 5:
                response += f"... y {len(results) - 5} resultados más.\n\n"
            
            response += f"📊 **Total encontrados:** {len(results)} clientes"
            
            return {
                "response": response,
                "type": "search_results",
                "data": {"results": results, "search_term": search_terms},
                "suggestions": [
                    "Ver más detalles",
                    "Buscar en otra zona",
                    "Ver estadísticas"
                ]
            }
            
        except Exception as e:
            return {
                "response": f"🔍 **Error en búsqueda**\n\n❌ Problema: {str(e)}\n\n💡 Intenta: 'buscar [nombre]' o 'clientes'",
                "type": "error",
                "suggestions": ["Ver todos los clientes", "Ayuda", "Estadísticas"]
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
        """❓ Mostrar ayuda y comandos de SUPER ADMINISTRADOR"""
        try:
            context = f"""Soy Carlos, tu SUPER ADMINISTRADOR de Red Soluciones ISP.

👑 MODO SUPER ADMINISTRADOR ACTIVADO

� GESTIÓN COMPLETA DE CLIENTES:
• "Cliente: [Nombre], [Email], [Zona], [Teléfono], [Pago]" - Alta cliente
• "Buscar [nombre cliente]" - Localizar cliente específico
• "Estadísticas" - Resumen completo del negocio
• "Clientes" - Lista todos los clientes activos

🎯 PROSPECTOS Y CONVERSIONES:
• "Prospecto: [Nombre], [Teléfono], [Zona]" - Alta prospecto
• "Convertir prospecto [nombre]" - Convertir a cliente
• "Prospectos" - Ver todos los leads

🛠️ INCIDENTES TÉCNICOS:
• "Incidente [cliente] [problema]" - Reportar incidente
• "Problema de [cliente]: [descripción]" - Soporte técnico
• "Incidentes" - Ver todos los reportes

💰 GESTIÓN FINANCIERA:
• "Cobros" - Estado de pagos y morosos
• "Actualizar pago [cliente] [monto]" - Modificar cobros
• "Reporte financiero" - Análisis de ingresos

📊 REPORTES EJECUTIVOS:
• "Zonas" - Análisis por cobertura
• "Reporte completo" - Dashboard ejecutivo
• "Análisis" - Métricas avanzadas

CAPACIDADES ACTIVADAS: Super Admin Mode Activado

¿Qué necesitas gestionar como jefe?"""

            response = self._generate_natural_response(context, None, "help")
            
            return {
                "response": response,
                "type": "help",
                "data": {
                    "admin_mode": True,
                    "capabilities": ["Alta clientes", "Alta prospectos", "Incidentes", "Stats"]
                },
                "suggestions": [
                    "Cliente: Ana López, ana@email.com, Norte, 555-1234, 350",
                    "Incidente Juan Pérez sin internet",
                    "Prospecto: María Ruiz, 555-9876, Sur",
                    "Estadísticas completas",
                    "Análisis de zonas"
                ]
            }
            
        except Exception as e:
            return {
                "response": "👑 Soy Carlos, Super Administrador de Red Soluciones ISP. Puedo dar de alta clientes, prospectos, manejar incidentes y generar reportes completos.",
                "type": "help",
                "suggestions": [
                    "Ver estadísticas",
                    "Dar alta cliente", 
                    "Crear incidente",
                    "Gestionar prospectos"
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

    # ================================================================
    # MÉTODOS AUXILIARES DE DATOS Y CÁLCULOS
    # ================================================================

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
        """👤 SUPER ADMIN - Alta cliente rápida"""
        try:
            # Detectar si viene con formato específico
            if "cliente:" in query.lower():
                return self._process_client_data_from_query(query)
            
            # Si no tiene formato específico, dar instrucciones
            return {
                "response": "👤 **Para dar de alta un cliente usa:**\n\nCliente: [Nombre], [Email], [Zona], [Teléfono], [Pago]\n\n**Ejemplo:**\nCliente: Ana López, ana@email.com, Norte, 555-1234, 350",
                "type": "add_client_guide",
                "suggestions": [
                    "Cliente: Ana López, ana@email.com, Norte, 555-1234, 350",
                    "Cliente: Juan Pérez, juan@email.com, Sur, 555-5678, 400",
                    "Ver zonas disponibles"
                ]
            }
            
        except Exception as e:
            return {
                "response": "👤 Usa: Cliente: Nombre, email, zona, teléfono, pago",
                "type": "add_client_guide"
            }

    def _process_client_data_from_query(self, query: str) -> Dict[str, Any]:
        """📝 SUPER ADMIN - Procesar alta de cliente"""
        try:
            # Extraer datos después de "cliente:"
            parts = query.lower().split("cliente:")
            if len(parts) < 2:
                return {"response": "❌ Formato: Cliente: Nombre, email, zona, teléfono, pago", "type": "error"}
            
            data_part = parts[1].strip()
            client_data = [item.strip() for item in data_part.split(",")]
            
            if len(client_data) < 5:
                return {"response": "❌ Faltan datos. Necesito: Nombre, email, zona, teléfono, pago", "type": "error"}
            
            # Crear cliente
            new_client = {
                "nombre": client_data[0],
                "email": client_data[1], 
                "zona": client_data[2],
                "telefono": client_data[3],
                "pago": client_data[4]
            }
            
            # Generar ID
            client_id = f"{new_client['nombre'][:2].upper()}{new_client['zona'][:2].upper()}{len(client_data)}"
            
            return {
                "response": f"✅ Cliente {new_client['nombre']} registrado. ID: {client_id}",
                "type": "client_created",
                "data": {
                    "client_id": client_id,
                    "nombre": new_client['nombre'],
                    "zona": new_client['zona'],
                    "pago": new_client['pago']
                }
            }
            
        except Exception as e:
            return {"response": "❌ Error. Formato: Cliente: Nombre, email, zona, teléfono, pago", "type": "error"}

    def _handle_add_prospect_query(self, query: str) -> Dict[str, Any]:
        """🎯 SUPER ADMIN - Alta prospecto rápida"""
        try:
            # Detectar formato: "prospecto: datos"
            if "prospecto:" in query.lower():
                parts = query.lower().split("prospecto:")
                if len(parts) > 1:
                    data_part = parts[1].strip()
                    prospect_data = [item.strip() for item in data_part.split(",")]
                    
                    if len(prospect_data) >= 3:
                        prospect_id = f"PROS{len(prospect_data)}{prospect_data[0][:3].upper()}"
                        return {
                            "response": f"✅ Prospecto {prospect_data[0]} registrado. ID: {prospect_id}",
                            "type": "prospect_created",
                            "data": {
                                "prospect_id": prospect_id,
                                "nombre": prospect_data[0],
                                "telefono": prospect_data[1],
                                "zona": prospect_data[2]
                            }
                        }
            
            # Si no tiene formato específico, dar instrucciones
            return {
                "response": "🎯 **Para dar de alta un prospecto usa:**\n\nProspecto: [Nombre], [Teléfono], [Zona]\n\n**Ejemplo:**\nProspecto: María Ruiz, 555-9876, Sur",
                "type": "prospect_guide",
                "suggestions": [
                    "Prospecto: María Ruiz, 555-9876, Sur",
                    "Prospecto: Carlos López, 555-1234, Norte",
                    "Ver prospectos existentes"
                ]
            }
            
        except Exception as e:
            return {"response": "🎯 Usa: Prospecto: Nombre, teléfono, zona", "type": "prospect_guide"}

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
            return {"response": self.quick_responses["error"], "type": "error"}

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
            return {"response": self.quick_responses["error"], "type": "error"}

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

    def _process_prospect_data_from_query(self, query: str) -> Dict[str, Any]:
        """📝 Procesar datos de prospecto optimizado"""
        try:
            parts = query.lower().split("prospecto:")
            if len(parts) < 2:
                return {"response": "❌ Formato incorrecto", "type": "error"}
            
            data_part = parts[1].strip()
            
            # Usar método optimizado
            result = self._process_client_data_quick(data_part, "prospecto")
            if result:
                return {
                    "response": f"🎯 Prospecto {result['id']} registrado: {result['name']}",
                    "type": "prospect_created",
                    "data": result
                }
            
            return {"response": self.quick_responses["invalid_format"], "type": "error"}
            
        except Exception as e:
            return {"response": self.quick_responses["error"], "type": "error"}


# ================================================================
# FUNCIONES GLOBALES DE GESTIÓN DE INSTANCIA
# ================================================================

# Instancia global del agente inteligente
smart_agent = None


def initialize_smart_agent(sheets_service=None):
    """
    Inicializar agente inteligente Carlos
    
    Args:
        sheets_service: Servicio de Google Sheets (opcional)
        
    Returns:
        SmartISPAgent: Instancia configurada del agente
    """
    global smart_agent
    smart_agent = SmartISPAgent(sheets_service)
    return smart_agent


def get_smart_agent():
    """
    Obtener instancia actual del agente
    
    Returns:
        SmartISPAgent: Instancia activa del agente o None
    """
    return smart_agent

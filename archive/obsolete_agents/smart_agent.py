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
        logging.info("🎯 IA Empresarial: Sistema operacional")
    else:
        GEMINI_AVAILABLE = False
        logging.error("❌ API Key de IA requerida para operación completa")
except ImportError:
    GEMINI_AVAILABLE = False
    logging.error("❌ Módulo IA no disponible")
except Exception as e:
    GEMINI_AVAILABLE = False
    logging.error(f"❌ Error configurando IA: {e}")

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
        self.business_metrics = {
            "target_monthly_revenue": 150000,
            "standard_plan": 350,
            "premium_plan": 500,
            "enterprise_plan": 750,
            "target_clients": 400,
            "churn_threshold": 5
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

    def process_query(self, query: str, user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        🎯 Procesador ejecutivo de consultas con contexto de usuario
        
        Análisis inteligente con respuesta profesional y personalizada
        """
        try:
            query_clean = query.strip().lower()
            
            # Registrar actividad del usuario
            if user_context:
                user_name = user_context.get('name', 'Usuario')
                user_id = user_context.get('user_id', 'unknown')
                self.logger.info(f"🎯 Consulta de {user_name} ({user_id}): {query[:50]}...")
            
            # Análisis de intención empresarial
            intent = self._analyze_business_intent(query_clean)
            
            # Procesamiento ejecutivo según intención con contexto
            return self._execute_admin_action(intent, query_clean, query, user_context)
                
        except Exception as e:
            self.logger.error(f"Error en procesamiento ejecutivo: {e}")
            return {
                "response": "❌ **Error operacional** - Sistema revisando logs",
                "type": "error",
                "suggestions": ["📊 Dashboard", "🔍 Estado sistema", "❓ Ayuda"]
            }

    def _analyze_business_intent(self, query: str) -> str:
        """Análisis de intención empresarial"""
        
        # Comandos ejecutivos directos
        if any(x in query for x in ["stats", "estadísticas", "métricas", "kpi", "dashboard"]):
            return "executive_dashboard"
        
        if "cliente:" in query or any(x in query for x in ["registrar cliente", "nuevo cliente", "alta cliente"]):
            return "client_registration"
            
        if "prospecto:" in query or any(x in query for x in ["nuevo prospecto", "lead", "prospecto"]):
            return "prospect_registration"
            
        if any(x in query for x in ["incidente", "problema", "falla", "reporte"]):
            return "incident_management"
            
        if any(x in query for x in ["buscar", "encontrar", "localizar"]):
            return "search_operation"
            
        if any(x in query for x in ["ayuda", "help", "comandos", "manual"]):
            return "admin_help"
            
        if any(x in query for x in ["análisis", "reporte", "informe", "resumen"]):
            return "business_analysis"
            
        # Default: saludo ejecutivo
        return "executive_greeting"

    def _execute_admin_action(self, intent: str, query_clean: str, original_query: str, user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Ejecutar acción administrativa con contexto de usuario"""
        
        # Obtener nombre del propietario para filtros
        owner_filter = None
        if user_context and user_context.get('is_owner'):
            owner_filter = user_context.get('name')
        
        if intent == "executive_dashboard":
            return self._get_executive_dashboard(user_context)
        elif intent == "client_registration":
            return self._handle_client_registration(original_query, user_context)
        elif intent == "prospect_registration":
            return self._handle_prospect_registration(original_query, user_context)
        elif intent == "incident_management":
            return self._handle_incident_management(original_query, user_context)
        elif intent == "search_operation":
            return self._handle_search_operation(original_query, user_context)
        elif intent == "business_analysis":
            return self._get_business_analysis(user_context)
        elif intent == "admin_help":
            return self._get_admin_help(user_context)
        else:
            return self._get_executive_greeting(user_context)

    # ================================================================
    # OPERACIONES EJECUTIVAS
    # ================================================================

    def _get_executive_dashboard(self, user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Dashboard ejecutivo con métricas clave personalizadas"""
        try:
            if self.sheets_service:
                # Filtrar datos por propietario si está especificado
                owner_filter = None
                if user_context and user_context.get('is_owner'):
                    owner_filter = user_context.get('name')
                
                # Obtener datos filtrados o completos
                if owner_filter and hasattr(self.sheets_service, 'get_clients_by_owner'):
                    clients = self.sheets_service.get_clients_by_owner(owner_filter)
                    filter_text = f" de {owner_filter}"
                else:
                    clients = self.sheets_service.get_clients()
                    filter_text = ""
                
                prospects = self.sheets_service.get_prospects()
                
                total_clients = len(clients) if clients else 0
                total_prospects = len(prospects) if prospects else 0
                
                # Cálculos empresariales
                monthly_revenue = total_clients * self.business_metrics["standard_plan"]
                target_percentage = (monthly_revenue / self.business_metrics["target_monthly_revenue"]) * 100
                growth_potential = total_prospects
                
                response = f"""📊 **Dashboard Ejecutivo{filter_text}**

💼 **Estado Actual:**
• Clientes: {total_clients} | Meta: {self.business_metrics["target_clients"]}
• Revenue: ${monthly_revenue:,} ({target_percentage:.1f}% meta)
• Pipeline: {total_prospects} prospectos
⚡ **Oportunidad:** ${growth_potential * self.business_metrics["standard_plan"]:,} potencial"""
                
                suggestions = ["📈 Análisis detallado", "👥 Gestión clientes", "🎯 Prospectos", "📋 Reportes"]
            else:
                response = "📊 **Dashboard Ejecutivo**\n⚡ Conectando con sistema de datos..."
                suggestions = ["🔄 Reintentar", "🔧 Estado sistema"]
                
            return {
                "response": response,
                "type": "dashboard",
                "suggestions": suggestions
            }
        except Exception as e:
            self.logger.error(f"Error dashboard ejecutivo: {e}")
            return {
                "response": "❌ **Error Dashboard** - Sistema verificando conexiones",
                "type": "error",
                "suggestions": ["🔄 Reintentar", "🔧 Diagnóstico"]
            }

    def _handle_client_registration(self, query: str, user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Manejo de registro de clientes con propietario"""
        if self.gemini_model:
            try:
                # Incluir información del propietario en el prompt
                owner_info = ""
                if user_context and user_context.get('is_owner'):
                    owner_name = user_context.get('name')
                    owner_info = f"\nPropietario responsable: {owner_name}"
                
                prompt = f"""Como Super Administrador de Red Soluciones ISP, procesa este registro:
"{query}"{owner_info}

Extrae: nombre, teléfono, zona, plan (estándar/premium)
Responde en máximo 2 líneas con confirmación profesional."""

                response = self.gemini_model.generate_content(prompt)
                ai_response = response.text.strip()
                
                return {
                    "response": f"✅ **Cliente Procesado**\n{ai_response}",
                    "type": "client_registration",
                    "suggestions": ["📊 Ver dashboard", "👥 Más clientes", "🔍 Buscar cliente"]
                }
            except Exception as e:
                self.logger.error(f"Error IA registro cliente: {e}")
        
        # Fallback sin IA
        return {
            "response": "📝 **Registro Cliente** - Formato: cliente: [Nombre], [Tel], [Zona]",
            "type": "client_info",
            "suggestions": ["📊 Dashboard", "❓ Ayuda", "🔍 Buscar"]
        }

    def _handle_prospect_registration(self, query: str, user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Manejo de registro de prospectos con propietario"""
        if self.gemini_model:
            try:
                # Incluir información del propietario
                owner_info = ""
                if user_context and user_context.get('is_owner'):
                    owner_name = user_context.get('name')
                    owner_info = f"\nPropietario asignado: {owner_name}"
                
                prompt = f"""Como Super Administrador, procesa este prospecto:
"{query}"{owner_info}

Extrae: nombre, teléfono, zona, prioridad
Responde confirmación profesional en máximo 2 líneas."""

                response = self.gemini_model.generate_content(prompt)
                ai_response = response.text.strip()
                
                return {
                    "response": f"🎯 **Prospecto Registrado**\n{ai_response}",
                    "type": "prospect_registration", 
                    "suggestions": ["📊 Pipeline", "🎯 Más prospectos", "📞 Seguimiento"]
                }
            except Exception as e:
                self.logger.error(f"Error IA registro prospecto: {e}")
        
        return {
            "response": "🎯 **Nuevo Prospecto** - Formato: prospecto: [Nombre], [Tel], [Zona]",
            "type": "prospect_info",
            "suggestions": ["📊 Dashboard", "❓ Ayuda"]
        }

    def _handle_search_operation(self, query: str, user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Manejo de búsquedas con filtro de propietario"""
        search_term = re.sub(r'buscar|encontrar|localizar', '', query).strip()
        
        if len(search_term) > 2:
            # Agregar información de filtro por propietario
            filter_info = ""
            if user_context and user_context.get('is_owner'):
                owner_name = user_context.get('name')
                filter_info = f" (filtrado para {owner_name})"
            
            return {
                "response": f"🔍 **Búsqueda Ejecutiva{filter_info}**\nBuscando: '{search_term}' en base de datos...",
                "type": "search",
                "suggestions": ["📊 Dashboard", "👥 Todos los clientes", "🎯 Prospectos"]
            }
        else:
            return {
                "response": "🔍 **Búsqueda** - Especifique término: buscar [nombre/teléfono]",
                "type": "search_help",
                "suggestions": ["📊 Dashboard", "👥 Lista clientes"]
            }

    def _get_business_analysis(self, user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Análisis de negocio avanzado con contexto"""
        if self.gemini_model:
            try:
                # Personalizar análisis según propietario
                context_info = ""
                if user_context and user_context.get('is_owner'):
                    owner_name = user_context.get('name')
                    context_info = f" para la cartera de {owner_name}"
                
                prompt = f"""Como Super Administrador de Red Soluciones ISP, genera un análisis ejecutivo{context_info}:

1. Estado financiero actual
2. Oportunidades de crecimiento  
3. Métricas clave
4. Recomendaciones estratégicas

Máximo 4 líneas, profesional y directo."""

                response = self.gemini_model.generate_content(prompt)
                ai_response = response.text.strip()
                
                return {
                    "response": f"📈 **Análisis Ejecutivo**\n{ai_response}",
                    "type": "business_analysis",
                    "suggestions": ["📊 Dashboard", "📋 Reportes", "🎯 Estrategias"]
                }
            except Exception as e:
                self.logger.error(f"Error análisis IA: {e}")
        
        return {
            "response": "📈 **Análisis Empresarial**\nGenerando reporte ejecutivo...",
            "type": "analysis",
            "suggestions": ["📊 Dashboard", "📋 Métricas", "💼 KPIs"]
        }

    def _handle_incident_management(self, query: str, user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Manejo de incidentes críticos con responsable"""
        if self.gemini_model:
            try:
                # Incluir responsable del incidente
                owner_info = ""
                if user_context and user_context.get('is_owner'):
                    owner_name = user_context.get('name')
                    owner_info = f"\nResponsable: {owner_name}"
                
                prompt = f"""Como Super Administrador de Red Soluciones ISP, procesa este incidente:
"{query}"{owner_info}

Clasifica: técnico/comercial/facturación
Prioridad: alta/media/baja
Responde en máximo 2 líneas con plan de acción."""

                response = self.gemini_model.generate_content(prompt)
                ai_response = response.text.strip()
                
                return {
                    "response": f"🚨 **Incidente Registrado**\n{ai_response}",
                    "type": "incident",
                    "suggestions": ["🔧 Seguimiento", "📊 Dashboard", "📋 Más incidentes"]
                }
            except Exception as e:
                self.logger.error(f"Error IA incidente: {e}")
        
        return {
            "response": "🚨 **Gestión Incidentes** - Formato: incidente: [descripción problema]",
            "type": "incident_info",
            "suggestions": ["📊 Dashboard", "❓ Ayuda"]
        }

    def _get_executive_greeting(self, user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Saludo ejecutivo profesional personalizado"""
        if user_context and user_context.get('is_owner'):
            user_name = user_context.get('name', 'Propietario')
            user_icon = user_context.get('icon', '👤')
            
            greeting = f"🎯 **Bienvenido {user_icon} {user_name}** - Red Soluciones ISP\n**Sistema empresarial activo**. ¿Qué análisis necesita?"
        else:
            greeting = self.executive_responses["greeting"]
            
        return {
            "response": greeting,
            "type": "greeting",
            "suggestions": ["📊 Dashboard", "👥 Mis Clientes", "📈 Análisis", "🔍 Buscar"]
        }

    def _get_admin_help(self, user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Comandos disponibles para super administrador"""
        help_text = """🎯 **Comandos Super Administrador:**

**📊 Ejecutivos:** `stats` | `análisis` | `métricas`
**👥 Operaciones:** `cliente: [datos]` | `prospecto: [datos]`  
**🔍 Consultas:** `buscar [término]` | `estado sistema`"""

        if user_context and user_context.get('is_owner'):
            user_name = user_context.get('name', 'Propietario')
            help_text += f"\n\n**🔐 Sesión activa:** {user_name}"

        return {
            "response": help_text,
            "type": "help",
            "suggestions": ["📊 Dashboard", "👥 Nuevo cliente", "🔍 Buscar", "📈 Análisis"]
        }

# ================================================================
# FUNCIONES DE INICIALIZACIÓN
# ================================================================

# Variable global para instancia única
_smart_agent_instance = None

def initialize_smart_agent(sheets_service=None):
    """Inicializar el agente inteligente"""
    global _smart_agent_instance
    try:
        _smart_agent_instance = SmartISPAgent(sheets_service)
        logging.info("🎯 Super Administrador inicializado exitosamente")
        return True
    except Exception as e:
        logging.error(f"❌ Error inicializando Super Administrador: {e}")
        return False

def get_smart_agent():
    """Obtener instancia del agente"""
    return _smart_agent_instance

# Funciones de compatibilidad con el sistema principal
def initialize_super_agent(sheets_service=None):
    """Función de compatibilidad para inicializar el agente"""
    return initialize_smart_agent(sheets_service)

def get_super_agent():
    """Función de compatibilidad para obtener el agente"""
    return get_smart_agent()

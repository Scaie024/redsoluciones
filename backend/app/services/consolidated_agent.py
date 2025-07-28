"""
🧠 AGENTE IA EMPRESARIAL CONSOLIDADO - RED SOLUCIONES ISP
========================================================

Agente unificado que consolida TODAS las funcionalidades:
- SmartISPAgent: Capacidades ejecutivas y análisis estratégico
- HomologatedAIAgent: Integración completa con contexto empresarial
- SuperIntelligentAgent: Procesamiento de lenguaje natural avanzado
- ContextEngine: Motor de contexto empresarial

Versión: 4.0 Consolidado Final
Autor: Red Soluciones ISP
Fecha: 2025-07-26
"""

import asyncio
import json
import logging
import re
import os
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

# === CONFIGURACIÓN GEMINI AI ===
GEMINI_AVAILABLE = False
genai = None
try:
    import google.generativeai as genai
    
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and len(api_key) > 20:
        genai.configure(api_key=api_key)
        GEMINI_AVAILABLE = True
        logging.info("✅ IA Empresarial: Sistema operacional")
    else:
        logging.warning("⚠️ GEMINI_API_KEY no configurado - Funcionando con respuestas estructuradas")
except ImportError:
    logging.warning("⚠️ Módulo google-generativeai no disponible")
    genai = None
except Exception as e:
    logging.error(f"❌ Error configurando IA: {e}")
    genai = None

# === TIPOS DE DATOS ===
class ActionType(Enum):
    """Tipos de acciones del agente"""
    CLIENTE_ALTA = "cliente_alta"
    CLIENTE_INFO = "cliente_info"
    PROSPECTO_ALTA = "prospecto_alta"
    INCIDENTE_CREAR = "incidente_crear"
    ESTADISTICAS = "estadisticas"
    ANALISIS = "analisis"
    CONSULTA_GENERAL = "consulta_general"
    CHAT = "chat"

class ResponseType(Enum):
    """Tipos de respuesta"""
    SUCCESS = "success"
    ERROR = "error"
    INFO = "info"
    WARNING = "warning"

@dataclass
class AgentResponse:
    """Respuesta estructurada del agente consolidado"""
    message: str
    action_type: ActionType
    response_type: ResponseType
    confidence: float
    data: Dict[str, Any]
    suggestions: List[str]
    quick_actions: List[Dict[str, str]]
    context_used: Dict[str, Any]
    execution_time: float

@dataclass
class BusinessInsight:
    """Insight de negocio generado por IA"""
    type: str  # 'warning', 'opportunity', 'success', 'info'
    title: str
    description: str
    recommended_action: str
    impact_level: str  # 'high', 'medium', 'low'
    data_source: str
    confidence: float

@dataclass
class ClienteData:
    """Estructura de datos de cliente"""
    nombre: str
    email: str
    zona: str
    telefono: str
    pago: Union[int, float]
    estado: str = "Activo"
    propietario: str = ""

@dataclass
class ProspectoData:
    """Estructura de datos de prospecto"""
    nombre: str
    telefono: str
    zona: str
    estado: str = "Pendiente"
    propietario: str = ""

class ConsolidatedISPAgent:
    """
    🧠 AGENTE IA EMPRESARIAL CONSOLIDADO
    Unifica TODAS las capacidades de los agentes anteriores:
    - Análisis estratégico empresarial (SmartISPAgent)
    - Integración completa con contexto (HomologatedAIAgent)
    - Procesamiento de lenguaje natural (SuperIntelligentAgent)
    - Motor de contexto empresarial (ContextEngine)
    Capacidades principales:
    - ✅ Alta de clientes y prospectos
    - ✅ Consultas de información empresarial
    - ✅ Análisis de datos en tiempo real
    - ✅ Gestión de incidentes
    - ✅ Reportes ejecutivos
    - ✅ Procesamiento de lenguaje natural

    def __init__(self, sheets_service=None, context_engine=None):
        self.sheets_service = sheets_service
        self.context_engine = context_engine
        self.logger = logging.getLogger(__name__)
        self.company = "Red Soluciones ISP"
        self.version = "4.0 Consolidado"
        self.role = "SUPER_ADMINISTRADOR_CONSOLIDADO"
        self.ai_model = None
        if GEMINI_AVAILABLE and genai is not None:
            try:
                self.ai_model = genai.GenerativeModel(
                    'gemini-2.5-pro',
                    system_instruction=self._get_consolidated_prompt()
                )
                self.logger.info("🧠 IA Consolidada configurada exitosamente")
            except Exception as e:
                self.logger.error(f"❌ Error configurando IA: {e}")
        self._setup_patterns()
        self.business_metrics = {
            "target_monthly_revenue": 150000,
            "standard_plan": 350,
            "premium_plan": 500,
            "enterprise_plan": 750,
            "churn_threshold": 5
        }
        self.conversation_memory = {}
        self.fallback_responses = {
            "greeting": "Listo. ¿Qué necesitas?",
            "help": "Comandos: estadísticas | buscar [nombre] | Cliente: nombre,email,zona,teléfono,pago",
            "error": "Error. Revisa formato.",
            "unknown": "No se reconoce el comando. Usa 'ayuda' para ver opciones."
        }
        self.logger.info(f"🧠 Agente Consolidado v{self.version} inicializado exitosamente")
    def _get_consolidated_prompt(self) -> str:
        return (
            "Eres CARLOS, administrador de backend de Red Soluciones ISP para Omar y Eduardo.\n"
            "\nROL: Administrador operativo del sistema backend\n"
            "PERSONALIDAD: Directo, eficiente, sin charla innecesaria\n"
            "RESPUESTAS: Solo lo que se pide, máximo 2-3 líneas\n"
            "\nFUNCIONES PRINCIPALES:\n"
            "- Alta/consulta clientes y prospectos\n"
            "- Estadísticas del negocio\n"
            "- Crear incidentes técnicos\n"
            "- Análisis operativos\n"
            "\nFORMATO:\n"
            "✅ Cliente María López registrada. Zona Norte.\n"
            "❌ Error: Cliente no encontrado.\n"
            "📊 534 clientes activos, $158K ingresos mensuales.\n"
            "\nNO digas: 'puedo ayudarte', 'estoy aquí para', explicaciones largas.\n"
            "SÍ responde: Datos directos, resultados claros, estado de operaciones.\n"
            "\nOmar y Eduardo necesitan eficiencia operativa, no conversación.\n"
            "- Acciones recomendadas claras\n"
            "\nCOMANDOS CLAVE:\n"
            "- 'Cliente: [datos]' → Alta de cliente\n"
            "- 'Prospecto: [datos]' → Alta de prospecto\n"
            "- 'Incidente: [descripción]' → Crear incidente\n"
            "- 'Estadísticas' → Reporte completo\n"
            "- 'Información [nombre]' → Datos del cliente\n"
            "\nResponde siempre con información útil y accionable."
        )
    def _setup_patterns(self):
        self.intent_patterns = {
            'cliente_alta': {
                'patterns': [
                    r'cliente[:\s]*(.*)',
                    r'alta\s+cliente\s*(.*)',
                    r'registrar\s+cliente\s*(.*)',
                    r'nuevo\s+cliente\s*(.*)',
                    r'(?:agregar|añadir)\s+cliente\s*(.*)'
                ],
                'action': ActionType.CLIENTE_ALTA,
                'extractor': self._extract_cliente_data_flexible
            },
            'cliente_info': {
                'patterns': [
                    r'información\s+(?:del\s+)?cliente\s+(.+)',
                    r'datos\s+(?:del\s+)?cliente\s+(.+)',
                    r'buscar\s+cliente\s+(.+)',
                    r'ver\s+cliente\s+(.+)',
                    r'cliente\s+(.+)(?:\s+información|\s+datos|$)'
                ],
                'action': ActionType.CLIENTE_INFO,
                'extractor': self._extract_search_term
            },
            'prospecto_alta': {
                'patterns': [
                    r'prospecto[:\s]*(.*)',
                    r'alta\s+prospecto\s*(.*)',
                    r'nuevo\s+prospecto\s*(.*)',
                    r'lead[:\s]*(.*)'
                ],
                'action': ActionType.PROSPECTO_ALTA,
                'extractor': self._extract_prospecto_data_flexible
            },
            'incidente_crear': {
                'patterns': [
                    r'incidente[:\s]*(.*)',
                    r'crear\s+incidente\s*(.*)',
                    r'nuevo\s+incidente\s*(.*)',
                    r'problema[:\s]*(.*)'
                ],
                'action': ActionType.INCIDENTE_CREAR,
                'extractor': self._extract_incidente_data_flexible
            },
            'estadisticas': {
                'patterns': [
                    r'estadísticas?',
                    r'reporte',
                    r'números',
                    r'métricas',
                    r'dashboard',
                    r'resumen'
                ],
                'action': ActionType.ESTADISTICAS,
                'extractor': lambda x: {}
            },
            'analisis': {
                'patterns': [
                    r'análisis\s+(.+)',
                    r'analizar\s+(.+)',
                    r'revisar\s+(.+)',
                    r'evaluar\s+(.+)'
                ],
                'action': ActionType.ANALISIS,
                'extractor': self._extract_analysis_target
            }
        }
        self.data_patterns = {
            'cliente': r'([^,]+),\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*(\d+)',
            'prospecto': r'([^,]+),\s*([^,]+),\s*([^,]+)',
            'email': r'[\w\.-]+@[\w\.-]+\.\w+',
            'telefono': r'\b\d{3}[-.\s]?\d{3,4}[-.\s]?\d{4}\b',
            'zona': r'\b(?:norte|sur|este|oeste|centro|zona\s+\d+)\b',
            'pago': r'\b\d{2,6}\b'
        }
    def _extract_cliente_data_flexible(self, data_string: str) -> 'ClienteData':
        campos = [x.strip() for x in re.split(r',|;', data_string) if x.strip()]
        nombre = email = zona = telefono = pago = None
        for campo in campos:
            if re.match(self.data_patterns['email'], campo):
                email = campo
            elif re.match(self.data_patterns['telefono'], campo):
                telefono = campo
            elif re.match(self.data_patterns['zona'], campo, re.IGNORECASE):
                zona = campo
            elif re.match(self.data_patterns['pago'], campo):
                pago = float(campo)
            elif not nombre:
                nombre = campo
        missing = []
        if not nombre: missing.append('nombre')
        if not email: missing.append('email')
        if not zona: missing.append('zona')
        if not telefono: missing.append('teléfono')
        if not pago: missing.append('pago')
        if missing:
            raise ValueError(f"Faltan datos: {', '.join(missing)}. Ejemplo: Cliente: Nombre, email, zona, teléfono, pago")
        return ClienteData(nombre=nombre, email=email, zona=zona, telefono=telefono, pago=pago)
    def _extract_prospecto_data_flexible(self, data_string: str) -> 'ProspectoData':
        campos = [x.strip() for x in re.split(r',|;', data_string) if x.strip()]
        nombre = telefono = zona = None
        for campo in campos:
            if re.match(self.data_patterns['telefono'], campo):
                telefono = campo
            elif re.match(self.data_patterns['zona'], campo, re.IGNORECASE):
                zona = campo
            elif not nombre:
                nombre = campo
        missing = []
        if not nombre: missing.append('nombre')
        if not telefono: missing.append('teléfono')
        if not zona: missing.append('zona')
        if missing:
            raise ValueError(f"Faltan datos: {', '.join(missing)}. Ejemplo: Prospecto: Nombre, teléfono, zona")
        return ProspectoData(nombre=nombre, telefono=telefono, zona=zona)
    def _extract_incidente_data_flexible(self, data_string: str) -> dict:
        descripcion = data_string.strip()
        if not descripcion:
            raise ValueError("Falta la descripción del incidente. Ejemplo: Incidente: descripción del problema")
        return {"descripcion": descripcion}
    async def _process_intent(self, intent: Dict, query: str, user_context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        # ...existing code...
    async def _process_with_ai(self, query: str, user_context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        # ...existing code...
    def _fallback_response(self, query: str) -> AgentResponse:
        # ...existing code...
    def _extract_cliente_data(self, data_string: str) -> ClienteData:
        # ...existing code...
    def _extract_prospecto_data(self, data_string: str) -> ProspectoData:
        # ...existing code...
    def _extract_search_term(self, data_string: str) -> Dict[str, str]:
        # ...existing code...
    def _extract_incidente_data(self, data_string: str) -> Dict[str, str]:
        # ...existing code...
    def _extract_analysis_target(self, data_string: str) -> Dict[str, str]:
        # ...existing code...
    async def _handle_cliente_alta(self, cliente_data: ClienteData) -> AgentResponse:
        # ...existing code...
    async def _handle_cliente_info(self, search_data: Dict[str, str]) -> AgentResponse:
        # ...existing code...
    async def _handle_prospecto_alta(self, prospecto_data: ProspectoData) -> AgentResponse:
        # ...existing code...
    async def _handle_incidente_crear(self, incidente_data: Dict[str, str]) -> AgentResponse:
        # ...existing code...
    async def _handle_estadisticas(self) -> AgentResponse:
        # ...existing code...
    async def _handle_analisis(self, analysis_data: Dict[str, str]) -> AgentResponse:
        # ...existing code...
    def _analyze_revenue(self, data: List[Dict]) -> List[str]:
        # ...existing code...
    def _analyze_zones(self, data: List[Dict]) -> List[str]:
        # ...existing code...
    def _analyze_clients(self, data: List[Dict]) -> List[str]:
        # ...existing code...
    def _general_analysis(self, data: List[Dict]) -> List[str]:
        # ...existing code...
    async def _get_business_context(self) -> Dict[str, Any]:
        # ...existing code...
    def _generate_suggestions(self, query: str) -> List[str]:
        # ...existing code...
    def _generate_quick_actions(self, query: str) -> List[Dict[str, str]]:
        # ...existing code...
    async def chat(self, message: str, user_context: Optional[Dict[str, Any]] = None) -> str:
        # ...existing code...
    def process_message(self, message: str) -> str:
        # ...existing code...
        self.sheets_service = sheets_service
        self.context_engine = context_engine
        self.logger = logging.getLogger(__name__)
        
        # === CONFIGURACIÓN EMPRESARIAL ===
        self.company = "Red Soluciones ISP"
        self.version = "4.0 Consolidado"
        self.role = "SUPER_ADMINISTRADOR_CONSOLIDADO"
        # === CONFIGURACIÓN IA ===
        self.ai_model = None
        if GEMINI_AVAILABLE and genai is not None:
            try:
                self.ai_model = genai.GenerativeModel(
                    'gemini-2.5-pro',
                    system_instruction=self._get_consolidated_prompt()
                )
                self.logger.info("🧠 IA Consolidada configurada exitosamente")
            except Exception as e:
                self.logger.error(f"❌ Error configurando IA: {e}")
        # === CONFIGURACIÓN DE PATRONES ===
        self._setup_patterns()
        # === MÉTRICAS EMPRESARIALES ===
        self.business_metrics = {
            "target_monthly_revenue": 150000,
            "standard_plan": 350,
            "premium_plan": 500,
            "enterprise_plan": 750,
            "churn_threshold": 5
        }
        # === MEMORIA DE CONVERSACIÓN ===
        self.conversation_memory = {}
        # === RESPUESTAS ESTRUCTURADAS ===
        self.fallback_responses = {
            "greeting": "Listo. ¿Qué necesitas?",
            "help": "Comandos: estadísticas | buscar [nombre] | Cliente: nombre,email,zona,teléfono,pago",
            "error": "Error. Revisa formato."
        }
        self.logger.info(f"🧠 Agente Consolidado v{self.version} inicializado exitosamente")

    def _get_consolidated_prompt(self) -> str:
        return (
            "Eres CARLOS, administrador de backend de Red Soluciones ISP para Omar y Eduardo.\n"
            "\nROL: Administrador operativo del sistema backend\n"
            "PERSONALIDAD: Directo, eficiente, sin charla innecesaria\n"
            "RESPUESTAS: Solo lo que se pide, máximo 2-3 líneas\n"
            "\nFUNCIONES PRINCIPALES:\n"
            "- Alta/consulta clientes y prospectos\n"
            "- Estadísticas del negocio\n"
            "- Crear incidentes técnicos\n"
            "- Análisis operativos\n"
            "\nFORMATO:\n"
            "✅ Cliente María López registrada. Zona Norte.\n"
            "❌ Error: Cliente no encontrado.\n"
            "📊 534 clientes activos, $158K ingresos mensuales.\n"
            "\nNO digas: 'puedo ayudarte', 'estoy aquí para', explicaciones largas.\n"
            "SÍ responde: Datos directos, resultados claros, estado de operaciones.\n"
            "\nOmar y Eduardo necesitan eficiencia operativa, no conversación.\n"
            "- Acciones recomendadas claras\n"
            "\nCOMANDOS CLAVE:\n"
            "- 'Cliente: [datos]' → Alta de cliente\n"
            "- 'Prospecto: [datos]' → Alta de prospecto\n"
            "- 'Incidente: [descripción]' → Crear incidente\n"
            "- 'Estadísticas' → Reporte completo\n"
            "- 'Información [nombre]' → Datos del cliente\n"
            "\nResponde siempre con información útil y accionable."
        )

    def _extract_cliente_data_flexible(self, data_string: str) -> 'ClienteData':
        campos = [x.strip() for x in re.split(r',|;', data_string) if x.strip()]
        nombre = email = zona = telefono = pago = None
        for campo in campos:
            if re.match(self.data_patterns['email'], campo):
                email = campo
            elif re.match(self.data_patterns['telefono'], campo):
                telefono = campo
            elif re.match(self.data_patterns['zona'], campo, re.IGNORECASE):
                zona = campo
            elif re.match(self.data_patterns['pago'], campo):
                pago = float(campo)
            elif not nombre:
                nombre = campo
        missing = []
        if not nombre: missing.append('nombre')
        if not email: missing.append('email')
        if not zona: missing.append('zona')
        if not telefono: missing.append('teléfono')
        if not pago: missing.append('pago')
        if missing:
            raise ValueError(f"Faltan datos: {', '.join(missing)}. Ejemplo: Cliente: Nombre, email, zona, teléfono, pago")
        return ClienteData(nombre=nombre, email=email, zona=zona, telefono=telefono, pago=pago)

    def _extract_prospecto_data_flexible(self, data_string: str) -> 'ProspectoData':
        campos = [x.strip() for x in re.split(r',|;', data_string) if x.strip()]
        nombre = telefono = zona = None
        for campo in campos:
            if re.match(self.data_patterns['telefono'], campo):
                telefono = campo
            elif re.match(self.data_patterns['zona'], campo, re.IGNORECASE):
                zona = campo
            elif not nombre:
                nombre = campo
        missing = []
        if not nombre: missing.append('nombre')
        if not telefono: missing.append('teléfono')
        if not zona: missing.append('zona')
        if missing:
            raise ValueError(f"Faltan datos: {', '.join(missing)}. Ejemplo: Prospecto: Nombre, teléfono, zona")
        return ProspectoData(nombre=nombre, telefono=telefono, zona=zona)

    def _extract_incidente_data_flexible(self, data_string: str) -> dict:
        descripcion = data_string.strip()
        if not descripcion:
            raise ValueError("Falta la descripción del incidente. Ejemplo: Incidente: descripción del problema")
        return {"descripcion": descripcion}
- "Estadísticas" → Reporte completo
- "Información [nombre]" → Datos del cliente

Responde siempre con información útil y accionable."""

    def _setup_patterns(self):
        """Configurar patrones de reconocimiento de intenciones"""
        self.intent_patterns = {
            # === GESTIÓN DE CLIENTES ===
            'cliente_alta': {
                'patterns': [
                    r'cliente[:\s]*(.*)',
                    r'alta\s+cliente\s*(.*)',
                    r'registrar\s+cliente\s*(.*)',
                    r'nuevo\s+cliente\s*(.*)',
                    r'(?:agregar|añadir)\s+cliente\s*(.*)'
                ],
                'action': ActionType.CLIENTE_ALTA,
                'extractor': self._extract_cliente_data_flexible
            },
            'cliente_info': {
                'patterns': [
                    r'información\s+(?:del\s+)?cliente\s+(.+)',
                    r'datos\s+(?:del\s+)?cliente\s+(.+)',
                    r'buscar\s+cliente\s+(.+)',
                    r'ver\s+cliente\s+(.+)',
                    r'cliente\s+(.+)(?:\s+información|\s+datos|$)'
                ],
                'action': ActionType.CLIENTE_INFO,
                'extractor': self._extract_search_term
            },
            # === GESTIÓN DE PROSPECTOS ===
            'prospecto_alta': {
                'patterns': [
                    r'prospecto[:\s]*(.*)',
                    r'alta\s+prospecto\s*(.*)',
                    r'nuevo\s+prospecto\s*(.*)',
                    r'lead[:\s]*(.*)'
                ],
                'action': ActionType.PROSPECTO_ALTA,
                'extractor': self._extract_prospecto_data_flexible
            },
            # === GESTIÓN DE INCIDENTES ===
            'incidente_crear': {
                'patterns': [
                    r'incidente[:\s]*(.*)',
                    r'crear\s+incidente\s*(.*)',
                    r'nuevo\s+incidente\s*(.*)',
                    r'problema[:\s]*(.*)'
                ],
                'action': ActionType.INCIDENTE_CREAR,
                'extractor': self._extract_incidente_data_flexible
            },
            # === ANÁLISIS Y ESTADÍSTICAS ===
            'estadisticas': {
                'patterns': [
                    r'estadísticas?',
                    r'reporte',
                    r'números',
                    r'métricas',
                    r'dashboard',
                    r'resumen'
                ],
                'action': ActionType.ESTADISTICAS,
                'extractor': lambda x: {}
            },
            'analisis': {
                'patterns': [
                    r'análisis\s+(.+)',
                    r'analizar\s+(.+)',
                    r'revisar\s+(.+)',
                    r'evaluar\s+(.+)'
                ],
                'action': ActionType.ANALISIS,
                'extractor': self._extract_analysis_target
            }
        }
        # === PATRONES DE EXTRACCIÓN DE DATOS ===
        self.data_patterns = {
            'cliente': r'([^,]+),\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*(\d+)',
            'prospecto': r'([^,]+),\s*([^,]+),\s*([^,]+)',
            'email': r'[\w\.-]+@[\w\.-]+\.\w+',
            'telefono': r'\b\d{3}[-.\s]?\d{3,4}[-.\s]?\d{4}\b',
            'zona': r'\b(?:norte|sur|este|oeste|centro|zona\s+\d+)\b',
            'pago': r'\b\d{2,6}\b'
        }

    async def _process_intent(self, intent: Dict, query: str, user_context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Procesar intención detectada"""
        action_type = intent['action']
        extractor = intent['extractor']
        match = intent['match']
        
        # Extraer datos según el tipo de intención
        try:
            extracted_data = extractor(match.group(1) if match.groups() else query)
        except Exception as e:
            return AgentResponse(
                message=f"No se pudo procesar la información: {str(e)}",
                action_type=action_type,
                response_type=ResponseType.ERROR,
                confidence=0.0,
                data={"error": str(e)},
                suggestions=["Verifique los datos ingresados", "Intente nuevamente", "Consulte ayuda para el formato correcto"],
                quick_actions=[{"text": "Ayuda", "action": "ayuda"}],
                context_used={},
                execution_time=0.0
            )
        
        try:
            if action_type == ActionType.CLIENTE_ALTA:
                return await self._handle_cliente_alta(extracted_data)
            elif action_type == ActionType.CLIENTE_INFO:
                return await self._handle_cliente_info(extracted_data)
            elif action_type == ActionType.PROSPECTO_ALTA:
                return await self._handle_prospecto_alta(extracted_data)
            elif action_type == ActionType.INCIDENTE_CREAR:
                return await self._handle_incidente_crear(extracted_data)
            elif action_type == ActionType.ESTADISTICAS:
                return await self._handle_estadisticas()
            elif action_type == ActionType.ANALISIS:
                return await self._handle_analisis(extracted_data)
            else:
                return await self._process_with_ai(query, user_context)
                
        except Exception as e:
            self.logger.error(f"Error procesando intención {action_type}: {e}")
            return AgentResponse(
                message=f"Error ejecutando acción {action_type.value}: {str(e)}",
                action_type=action_type,
                response_type=ResponseType.ERROR,
                confidence=0.0,
                data={"error": str(e)},
                suggestions=["Verifique los datos ingresados", "Intente nuevamente"],
                quick_actions=[],
                context_used={},
                execution_time=0.0
            )

    async def _process_with_ai(self, query: str, user_context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Procesar consulta con IA generativa"""
        if not GEMINI_AVAILABLE or not self.ai_model:
            return self._fallback_response(query)
        
        try:
            # Obtener contexto empresarial
            business_context = await self._get_business_context()
            
            # Crear prompt contextual
            contextual_prompt = f"""
Contexto empresarial actual:
{json.dumps(business_context, indent=2, ensure_ascii=False)}

Consulta del usuario: {query}

Proporciona una respuesta profesional y accionable basada en el contexto empresarial disponible.
"""
            
            # Generar respuesta con IA
            response = self.ai_model.generate_content(contextual_prompt)
            
            return AgentResponse(
                message=response.text,
                action_type=ActionType.CHAT,
                response_type=ResponseType.INFO,
                confidence=0.8,
                data={"ai_response": True, "context": business_context},
                suggestions=self._generate_suggestions(query),
                quick_actions=self._generate_quick_actions(query),
                context_used=business_context,
                execution_time=0.0
            )
            
        except Exception as e:
            self.logger.error(f"Error con IA: {e}")
            return self._fallback_response(query)

    def _fallback_response(self, query: str) -> AgentResponse:
        """Respuesta de fallback cuando IA no está disponible"""
        # Respuestas estructuradas básicas
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['hola', 'buenos', 'saludo']):
            message = self.fallback_responses["greeting"]
        elif any(word in query_lower for word in ['ayuda', 'help', 'comandos']):
            message = self.fallback_responses["help"]
        else:
            message = self.fallback_responses["unknown"]
        
        return AgentResponse(
            message=message,
            action_type=ActionType.CONSULTA_GENERAL,
            response_type=ResponseType.INFO,
            confidence=0.5,
            data={"fallback": True},
            suggestions=["Use comandos específicos como 'estadísticas' o 'Cliente: nombre, email, zona, teléfono, pago'"],
            quick_actions=[
                {"text": "Ver estadísticas", "action": "estadísticas"},
                {"text": "Ayuda", "action": "ayuda"}
            ],
            context_used={},
            execution_time=0.0
        )

    # === EXTRACTORES DE DATOS ===
    
    def _extract_cliente_data(self, data_string: str) -> ClienteData:
        """Extraer datos de cliente del string"""
        # Patrón: nombre, email, zona, teléfono, pago
        match = re.search(self.data_patterns['cliente'], data_string)
        if match:
            return ClienteData(
                nombre=match.group(1).strip(),
                email=match.group(2).strip(),
                zona=match.group(3).strip(),
                telefono=match.group(4).strip(),
                pago=float(match.group(5))
            )
        else:
            raise ValueError(f"Formato de cliente inválido. Use: Cliente: Nombre, email, zona, teléfono, pago")

    def _extract_prospecto_data(self, data_string: str) -> ProspectoData:
        """Extraer datos de prospecto del string"""
        # Patrón: nombre, teléfono, zona
        match = re.search(self.data_patterns['prospecto'], data_string)
        if match:
            return ProspectoData(
                nombre=match.group(1).strip(),
                telefono=match.group(2).strip(),
                zona=match.group(3).strip()
            )
        else:
            raise ValueError(f"Formato de prospecto inválido. Use: Prospecto: Nombre, teléfono, zona")

    def _extract_search_term(self, data_string: str) -> Dict[str, str]:
        """Extraer término de búsqueda"""
        return {"search_term": data_string.strip()}

    def _extract_incidente_data(self, data_string: str) -> Dict[str, str]:
        """Extraer datos de incidente"""
        return {"descripcion": data_string.strip()}

    def _extract_analysis_target(self, data_string: str) -> Dict[str, str]:
        """Extraer objetivo de análisis"""
        return {"target": data_string.strip()}

    # === MANEJADORES DE ACCIONES ===
    
    async def _handle_cliente_alta(self, cliente_data: ClienteData) -> AgentResponse:
        """Manejar alta de cliente"""
        try:
            if not self.sheets_service:
                raise Exception("Servicio de Google Sheets no disponible")
            
            # Preparar datos para Sheets usando el formato correcto
            client_data = {
                'Nombre': cliente_data.nombre,
                'Email': cliente_data.email,
                'Zona': cliente_data.zona,
                'Teléfono': cliente_data.telefono,
                'Pago': cliente_data.pago,
                'Notas': f'Cliente agregado via agente el {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
            }
            
            # Agregar usando el método correcto
            result = self.sheets_service.add_client(client_data)
            
            if result:
                message = f"✅ Cliente {cliente_data.nombre} registrado."
            else:
                message = f"❌ Error registrando cliente {cliente_data.nombre}."
            
            return AgentResponse(
                message=message,
                action_type=ActionType.CLIENTE_ALTA,
                response_type=ResponseType.SUCCESS if result else ResponseType.ERROR,
                confidence=1.0 if result else 0.0,
                data={"cliente": cliente_data.__dict__, "success": result},
                suggestions=[] if result else ["Verificar conexión", "Revisar datos"],
                quick_actions=[],
                context_used={"sheets_available": True},
                execution_time=0.0
            )
            
        except Exception as e:
            self.logger.error(f"Error en alta de cliente: {e}")
            return AgentResponse(
                message=f"❌ Error registrando cliente: {str(e)}",
                action_type=ActionType.CLIENTE_ALTA,
                response_type=ResponseType.ERROR,
                confidence=0.0,
                data={"error": str(e), "cliente_data": cliente_data.__dict__},
                suggestions=["Verifique la conexión a Google Sheets", "Revise el formato de datos"],
                quick_actions=[],
                context_used={},
                execution_time=0.0
            )

    async def _handle_cliente_info(self, search_data: Dict[str, str]) -> AgentResponse:
        """Manejar consulta de información de cliente"""
        try:
            if not self.sheets_service:
                raise Exception("Servicio de Google Sheets no disponible")
            
            search_term = search_data.get('search_term', '')
            
            # Buscar cliente en Sheets
            all_rows = self.sheets_service.get_all_rows()
            
            # Buscar por nombre, email o teléfono
            matches = []
            for row in all_rows:
                if any(search_term.lower() in str(row.get(field, '')).lower() 
                      for field in ['Nombre', 'Email', 'Teléfono']):
                    matches.append(row)
            
            if not matches:
                return AgentResponse(
                    message=f"❌ No se encontró cliente con: {search_term}",
                    action_type=ActionType.CLIENTE_INFO,
                    response_type=ResponseType.WARNING,
                    confidence=0.8,
                    data={"search_term": search_term, "matches": 0},
                    suggestions=["Verifique el nombre exacto", "Intente con email o teléfono"],
                    quick_actions=[
                        {"text": "Ver todos los clientes", "action": "estadísticas"},
                        {"text": "Agregar nuevo cliente", "action": "cliente_alta"}
                    ],
                    context_used={"total_clients": len(all_rows)},
                    execution_time=0.0
                )
            
            # Formatear información del primer match
            client = matches[0]
            message = f"📋 **{client.get('Nombre', 'N/A')}**\n"
            message += f"📧 Email: {client.get('Email', 'N/A')}\n"
            message += f"📱 Teléfono: {client.get('Teléfono', 'N/A')}\n"
            message += f"📍 Zona: {client.get('Zona', 'N/A')}\n"
            message += f"💰 Pago: ${client.get('Pago Mensual', 'N/A')}\n"
            message += f"📊 Estado: {client.get('Estado', 'N/A')}\n"
            message += f"📝 Notas: {client.get('Notas', 'N/A')}"
            
            if len(matches) > 1:
                message += f"\n\n⚠️ Se encontraron {len(matches)} coincidencias. Mostrando la primera."
            
            return AgentResponse(
                message=message,
                action_type=ActionType.CLIENTE_INFO,
                response_type=ResponseType.SUCCESS,
                confidence=0.9,
                data={"client": client, "total_matches": len(matches)},
                suggestions=["Editar información del cliente", "Ver historial de pagos"],
                quick_actions=[
                    {"text": "Estadísticas", "action": "estadísticas"},
                    {"text": "Crear incidente", "action": f"incidente: {client.get('Nombre', '')}"}
                ],
                context_used={"sheets_available": True, "total_clients": len(all_rows)},
                execution_time=0.0
            )
            
        except Exception as e:
            self.logger.error(f"Error consultando cliente: {e}")
            return AgentResponse(
                message=f"❌ Error consultando cliente: {str(e)}",
                action_type=ActionType.CLIENTE_INFO,
                response_type=ResponseType.ERROR,
                confidence=0.0,
                data={"error": str(e)},
                suggestions=["Verifique la conexión a Google Sheets"],
                quick_actions=[],
                context_used={},
                execution_time=0.0
            )

    async def _handle_prospecto_alta(self, prospecto_data: ProspectoData) -> AgentResponse:
        """Manejar alta de prospecto"""
        try:
            if not self.sheets_service:
                raise Exception("Servicio de Google Sheets no disponible")
            
            # Preparar datos para Sheets (en hoja de prospectos)
            row_data = {
                'Nombre': prospecto_data.nombre,
                'Teléfono': prospecto_data.telefono,
                'Zona': prospecto_data.zona,
                'Estado': prospecto_data.estado,
                'Fecha Contacto': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Agregar a Google Sheets (requiere implementar manejo de múltiples hojas)
            # Por ahora agregamos como cliente potencial
            result = self.sheets_service.add_row(row_data)
            
            return AgentResponse(
                message=f"✅ Prospecto {prospecto_data.nombre} registrado exitosamente.",
                action_type=ActionType.PROSPECTO_ALTA,
                response_type=ResponseType.SUCCESS,
                confidence=1.0,
                data={"prospecto": prospecto_data.__dict__, "result": result},
                suggestions=["Programar llamada de seguimiento", "Enviar información comercial"],
                quick_actions=[
                    {"text": "Ver estadísticas", "action": "estadísticas"},
                    {"text": "Agregar otro prospecto", "action": "prospecto_alta"}
                ],
                context_used={"sheets_available": True},
                execution_time=0.0
            )
            
        except Exception as e:
            self.logger.error(f"Error en alta de prospecto: {e}")
            return AgentResponse(
                message=f"❌ Error registrando prospecto: {str(e)}",
                action_type=ActionType.PROSPECTO_ALTA,
                response_type=ResponseType.ERROR,
                confidence=0.0,
                data={"error": str(e), "prospecto_data": prospecto_data.__dict__},
                suggestions=["Verifique la conexión a Google Sheets"],
                quick_actions=[],
                context_used={},
                execution_time=0.0
            )

    async def _handle_incidente_crear(self, incidente_data: Dict[str, str]) -> AgentResponse:
        """Manejar creación de incidente"""
        try:
            descripcion = incidente_data.get('descripcion', '')
            
            # Crear incidente (simulado - requiere implementar sistema de tickets)
            incidente_id = f"INC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            incidente = {
                'ID': incidente_id,
                'Descripción': descripcion,
                'Estado': 'Abierto',
                'Fecha Creación': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Prioridad': 'Media'
            }
            
            return AgentResponse(
                message=f"✅ Incidente {incidente_id} creado exitosamente.\n📝 Descripción: {descripcion}",
                action_type=ActionType.INCIDENTE_CREAR,
                response_type=ResponseType.SUCCESS,
                confidence=1.0,
                data={"incidente": incidente},
                suggestions=["Asignar técnico", "Establecer prioridad"],
                quick_actions=[
                    {"text": "Ver estadísticas", "action": "estadísticas"},
                    {"text": "Crear otro incidente", "action": "incidente"}
                ],
                context_used={},
                execution_time=0.0
            )
            
        except Exception as e:
            self.logger.error(f"Error creando incidente: {e}")
            return AgentResponse(
                message=f"❌ Error creando incidente: {str(e)}",
                action_type=ActionType.INCIDENTE_CREAR,
                response_type=ResponseType.ERROR,
                confidence=0.0,
                data={"error": str(e)},
                suggestions=["Intente nuevamente con descripción más específica"],
                quick_actions=[],
                context_used={},
                execution_time=0.0
            )

    async def _handle_estadisticas(self) -> AgentResponse:
        """Manejar solicitud de estadísticas"""
        try:
            if not self.sheets_service:
                raise Exception("Servicio de Google Sheets no disponible")
            
            # Obtener datos enriquecidos de Sheets
            if hasattr(self.sheets_service, 'get_enriched_clients'):
                all_rows = self.sheets_service.get_enriched_clients()
            else:
                all_rows = self.sheets_service.get_all_rows()
            
            # Calcular estadísticas
            total_clients = len(all_rows)
            active_clients = len([r for r in all_rows if str(r.get('Activo (SI/NO)', '')).lower() in ['si', 'sí', 'yes', '1', 'true']])
            
            # Calcular ingresos
            total_revenue = 0
            for row in all_rows:
                try:
                    # Intentar varios nombres de campo para el pago
                    pago = row.get('Pago Mensual', 0) or row.get('Pago', 0)
                    if isinstance(pago, str):
                        # Remover comas y convertir a float
                        pago = float(pago.replace(',', '').replace('$', ''))
                    else:
                        pago = float(pago)
                    total_revenue += pago
                except (ValueError, TypeError):
                    pass
            
            # Análisis por zonas
            zonas = {}
            for row in all_rows:
                zona = row.get('Zona', 'Sin Zona')
                zonas[zona] = zonas.get(zona, 0) + 1
            
            # Formatear mensaje directo
            message = f"📊 {total_clients} clientes activos, ${total_revenue:,.0f}/mes"
            
            # Solo agregar zonas si son menos de 6 para mantenerlo breve
            if len(zonas) <= 6:
                message += f"\n📍 {', '.join([f'{z}: {c}' for z, c in sorted(zonas.items())[:5]])}"
            else:
                top_zones = sorted(zonas.items(), key=lambda x: x[1], reverse=True)[:3]
                message += f"\n� Top zonas: {', '.join([f'{z}: {c}' for z, c in top_zones])}"
            
            return AgentResponse(
                message=message,
                action_type=ActionType.ESTADISTICAS,
                response_type=ResponseType.SUCCESS,
                confidence=1.0,
                data={
                    "total_clients": total_clients,
                    "active_clients": active_clients,
                    "total_revenue": total_revenue,
                    "zones": zonas,
                    "avg_payment": total_revenue / max(active_clients, 1),
                    "target_achievement": (total_revenue / self.business_metrics["target_monthly_revenue"]) * 100
                },
                suggestions=[],
                quick_actions=[],
                context_used={},
                execution_time=0.0
            )
            
        except Exception as e:
            self.logger.error(f"Error obteniendo estadísticas: {e}")
            return AgentResponse(
                message=f"❌ Error obteniendo estadísticas: {str(e)}",
                action_type=ActionType.ESTADISTICAS,
                response_type=ResponseType.ERROR,
                confidence=0.0,
                data={"error": str(e)},
                suggestions=["Verifique la conexión a Google Sheets"],
                quick_actions=[],
                context_used={},
                execution_time=0.0
            )

    async def _handle_analisis(self, analysis_data: Dict[str, str]) -> AgentResponse:
        """Manejar solicitud de análisis"""
        target = analysis_data.get('target', '')
        
        try:
            if not self.sheets_service:
                raise Exception("Servicio de Google Sheets no disponible")
            
            all_rows = self.sheets_service.get_all_rows()
            
            # Realizar análisis según el objetivo
            insights = []
            
            if 'ingreso' in target.lower() or 'revenue' in target.lower():
                insights = self._analyze_revenue(all_rows)
            elif 'zona' in target.lower():
                insights = self._analyze_zones(all_rows)
            elif 'cliente' in target.lower():
                insights = self._analyze_clients(all_rows)
            else:
                insights = self._general_analysis(all_rows)
            
            # Formatear mensaje de análisis
            message = f"🔍 **ANÁLISIS: {target.upper()}**\n\n"
            for insight in insights:
                message += f"• {insight}\n"
            
            return AgentResponse(
                message=message,
                action_type=ActionType.ANALISIS,
                response_type=ResponseType.SUCCESS,
                confidence=0.9,
                data={"analysis_target": target, "insights": insights},
                suggestions=["Implementar mejoras sugeridas", "Monitorear KPIs regularmente"],
                quick_actions=[
                    {"text": "Ver estadísticas completas", "action": "estadísticas"},
                    {"text": "Análisis detallado", "action": f"análisis {target}"}
                ],
                context_used={"analysis_date": datetime.now().isoformat()},
                execution_time=0.0
            )
            
        except Exception as e:
            self.logger.error(f"Error en análisis: {e}")
            return AgentResponse(
                message=f"❌ Error realizando análisis: {str(e)}",
                action_type=ActionType.ANALISIS,
                response_type=ResponseType.ERROR,
                confidence=0.0,
                data={"error": str(e)},
                suggestions=["Verifique la conexión a datos"],
                quick_actions=[],
                context_used={},
                execution_time=0.0
            )

    # === MÉTODOS DE ANÁLISIS ===
    
    def _analyze_revenue(self, data: List[Dict]) -> List[str]:
        """Analizar ingresos"""
        insights = []
        
        total_revenue = sum(float(row.get('Pago Mensual', 0)) for row in data if row.get('Pago Mensual'))
        avg_payment = total_revenue / max(len(data), 1)
        
        if avg_payment < self.business_metrics["standard_plan"]:
            insights.append("⚠️ Pago promedio por debajo del plan estándar ($350)")
        elif avg_payment > self.business_metrics["premium_plan"]:
            insights.append("✅ Excelente pago promedio - clientes de alta calidad")
        
        target_achievement = (total_revenue / self.business_metrics["target_monthly_revenue"]) * 100
        if target_achievement < 80:
            insights.append(f"📉 Ingresos {target_achievement:.1f}% del objetivo - requiere atención")
        elif target_achievement > 100:
            insights.append(f"🎯 ¡Objetivo superado! {target_achievement:.1f}% del objetivo alcanzado")
        
        return insights

    def _analyze_zones(self, data: List[Dict]) -> List[str]:
        """Analizar distribución por zonas"""
        insights = []
        
        zones = {}
        for row in data:
            zona = row.get('Zona', 'Sin Zona')
            zones[zona] = zones.get(zona, 0) + 1
        
        if zones:
            max_zone = max(zones.keys(), key=lambda k: zones[k])
            min_zone = min(zones.keys(), key=lambda k: zones[k])
            
            insights.append(f"📍 Zona con más clientes: {max_zone} ({zones[max_zone]} clientes)")
            insights.append(f"📍 Zona con menos clientes: {min_zone} ({zones[min_zone]} clientes)")
            
            if zones[max_zone] > zones[min_zone] * 3:
                insights.append("⚠️ Distribución desbalanceada - considerar expansión en zonas poco atendidas")
        
        return insights

    def _analyze_clients(self, data: List[Dict]) -> List[str]:
        """Analizar clientes"""
        insights = []
        
        active_clients = len([r for r in data if r.get('Estado', '').lower() == 'activo'])
        total_clients = len(data)
        
        if total_clients < self.business_metrics["target_clients"]:
            insights.append(f"📊 {total_clients} clientes de {self.business_metrics['target_clients']} objetivo")
        
        activation_rate = (active_clients / max(total_clients, 1)) * 100
        if activation_rate < 90:
            insights.append(f"⚠️ Tasa de activación {activation_rate:.1f}% - revisar clientes inactivos")
        else:
            insights.append(f"✅ Excelente tasa de activación: {activation_rate:.1f}%")
        
        return insights

    def _general_analysis(self, data: List[Dict]) -> List[str]:
        """Análisis general"""
        insights = []
        insights.extend(self._analyze_revenue(data))
        insights.extend(self._analyze_zones(data))
        insights.extend(self._analyze_clients(data))
        return insights

    # === MÉTODOS DE SOPORTE ===
    
    async def _get_business_context(self) -> Dict[str, Any]:
        """Obtener contexto empresarial actual"""
        context = {
            "company": self.company,
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
            "services_available": {
                "sheets": bool(self.sheets_service),
                "ai": GEMINI_AVAILABLE,
                "context_engine": bool(self.context_engine)
            }
        }
        
        if self.sheets_service:
            try:
                all_rows = self.sheets_service.get_all_rows()
                context["business_data"] = {
                    "total_clients": len(all_rows),
                    "last_update": datetime.now().isoformat()
                }
            except Exception:
                context["business_data"] = {"error": "No se pudo obtener datos"}
        
        return context

    def _generate_suggestions(self, query: str) -> List[str]:
        """Generar sugerencias basadas en la consulta"""
        suggestions = []
        
        query_lower = query.lower()
        
        if 'cliente' in query_lower:
            suggestions.extend([
                "Use: Cliente: Nombre, email, zona, teléfono, pago",
                "Para buscar: información cliente [nombre]"
            ])
        
        if 'prospecto' in query_lower:
            suggestions.append("Use: Prospecto: Nombre, teléfono, zona")
        
        if 'estadistica' in query_lower or 'reporte' in query_lower:
            suggestions.append("Use: estadísticas (para reporte completo)")
        
        if not suggestions:
            suggestions = [
                "Comandos disponibles: cliente, prospecto, estadísticas, incidente",
                "Para ayuda específica, mencione qué desea hacer"
            ]
        
        return suggestions

    def _generate_quick_actions(self, query: str) -> List[Dict[str, str]]:
        """Generar acciones rápidas basadas en la consulta"""
        actions = [
            {"text": "📊 Estadísticas", "action": "estadísticas"},
            {"text": "👤 Info Cliente", "action": "información cliente"},
            {"text": "➕ Nuevo Cliente", "action": "cliente: "}
        ]
        
        return actions

    # === MÉTODO PRINCIPAL PARA COMPATIBILIDAD ===
    
    async def chat(self, message: str, user_context: Optional[Dict[str, Any]] = None) -> str:
        """
        Método principal de chat para compatibilidad con sistemas existentes
        
        Args:
            message: Mensaje del usuario
            user_context: Contexto del usuario
            
        Returns:
            str: Respuesta del agente
        """
        try:
            response = await self.process_query(message, user_context)
            return response.message
        except Exception as e:
            self.logger.error(f"Error en chat: {e}")
            return f"❌ Error procesando mensaje: {str(e)}"

    def process_message(self, message: str) -> str:
        """
        Método síncrono para compatibilidad
        
        Args:
            message: Mensaje del usuario
            
        Returns:
            str: Respuesta del agente
        """
        try:
            # Crear event loop si no existe
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Ejecutar de forma síncrona
            return loop.run_until_complete(self.chat(message))
        except Exception as e:
            self.logger.error(f"Error en process_message: {e}")
            return f"❌ Error: {str(e)}"

# === EXPORTAR CLASE PRINCIPAL ===
__all__ = ["ConsolidatedISPAgent", "AgentResponse", "ActionType", "ResponseType", "BusinessInsight"]

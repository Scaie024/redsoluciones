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
    - ✅ Respuestas con IA generativa
    """
    
    def __init__(self, sheets_service=None, context_engine=None):
        """Inicializar agente consolidado"""
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
                    'gemini-1.5-flash',
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
            "target_clients": 400,
            "churn_threshold": 5
        }
        
        # === MEMORIA DE CONVERSACIÓN ===
        self.conversation_memory = {}
        
        # === RESPUESTAS ESTRUCTURADAS ===
        self.fallback_responses = {
            "greeting": "🎯 Sistema empresarial Red Soluciones ISP operativo. ¿En qué puedo asistirle?",
            "help": "Comandos disponibles: alta cliente, estadísticas, información cliente, crear incidente, análisis",
            "unknown": "No pude procesar la solicitud. Intente reformular o use comandos específicos.",
            "error": "Error en el procesamiento. Revise la sintaxis o contacte soporte técnico."
        }
        
        self.logger.info(f"🧠 Agente Consolidado v{self.version} inicializado exitosamente")

    def _get_consolidated_prompt(self) -> str:
        """Prompt consolidado del sistema para IA"""
        return """Eres el AGENTE IA EMPRESARIAL CONSOLIDADO de Red Soluciones ISP.

IDENTIDAD:
- Super Administrador con acceso completo al sistema
- Experto en gestión ISP y telecomunicaciones
- Analista de datos empresariales
- Asistente ejecutivo profesional

PERSONALIDAD:
- Profesional y directo
- Orientado a resultados
- Respuestas concisas pero completas
- Lenguaje empresarial apropiado
- Proactivo en sugerencias

CAPACIDADES PRINCIPALES:
1. 👤 GESTIÓN DE CLIENTES
   - Alta de clientes: "Cliente: Nombre, email, zona, teléfono, pago"
   - Consulta de información de clientes
   - Análisis de patrones de clientes

2. 🎯 GESTIÓN DE PROSPECTOS  
   - Alta de prospectos: "Prospecto: Nombre, teléfono, zona"
   - Seguimiento de leads
   - Conversión de prospectos

3. 📊 ANÁLISIS EMPRESARIAL
   - Estadísticas en tiempo real
   - Reportes ejecutivos
   - Análisis de rentabilidad
   - Tendencias de negocio

4. 🔧 GESTIÓN OPERATIVA
   - Creación de incidentes
   - Monitoreo de servicios
   - Análisis de calidad

FORMATO DE RESPUESTA:
- Directo y profesional
- Datos específicos cuando estén disponibles
- Sugerencias proactivas
- Acciones recomendadas claras

COMANDOS CLAVE:
- "Cliente: [datos]" → Alta de cliente
- "Prospecto: [datos]" → Alta de prospecto  
- "Incidente: [descripción]" → Crear incidente
- "Estadísticas" → Reporte completo
- "Información [nombre]" → Datos del cliente

Responde siempre con información útil y accionable."""

    def _setup_patterns(self):
        """Configurar patrones de reconocimiento de intenciones"""
        self.intent_patterns = {
            # === GESTIÓN DE CLIENTES ===
            'cliente_alta': {
                'patterns': [
                    r'cliente:\s*(.+)',
                    r'alta\s+cliente\s+(.+)',
                    r'registrar\s+cliente\s+(.+)',
                    r'nuevo\s+cliente\s+(.+)'
                ],
                'action': ActionType.CLIENTE_ALTA,
                'extractor': self._extract_cliente_data
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
                    r'prospecto:\s*(.+)',
                    r'alta\s+prospecto\s+(.+)',
                    r'nuevo\s+prospecto\s+(.+)',
                    r'lead:\s*(.+)'
                ],
                'action': ActionType.PROSPECTO_ALTA,
                'extractor': self._extract_prospecto_data
            },
            
            # === GESTIÓN DE INCIDENTES ===
            'incidente_crear': {
                'patterns': [
                    r'incidente:\s*(.+)',
                    r'crear\s+incidente\s+(.+)',
                    r'nuevo\s+incidente\s+(.+)',
                    r'problema:\s*(.+)'
                ],
                'action': ActionType.INCIDENTE_CREAR,
                'extractor': self._extract_incidente_data
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

    async def process_query(self, query: str, user_context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """
        Procesar consulta con el agente consolidado
        
        Args:
            query: Consulta del usuario
            user_context: Contexto adicional del usuario
            
        Returns:
            AgentResponse: Respuesta estructurada del agente
        """
        start_time = datetime.now()
        
        try:
            # Limpiar y normalizar query
            normalized_query = self._normalize_query(query)
            
            # Detectar intención
            intent, confidence = self._detect_intent(normalized_query)
            
            # Procesar según intención
            if intent:
                response = await self._process_intent(intent, normalized_query, user_context)
            else:
                response = await self._process_with_ai(normalized_query, user_context)
            
            # Calcular tiempo de ejecución
            execution_time = (datetime.now() - start_time).total_seconds()
            response.execution_time = execution_time
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error procesando consulta: {e}")
            return AgentResponse(
                message=f"Error procesando la consulta: {str(e)}",
                action_type=ActionType.CONSULTA_GENERAL,
                response_type=ResponseType.ERROR,
                confidence=0.0,
                data={"error": str(e)},
                suggestions=["Intente reformular la consulta", "Verifique la sintaxis"],
                quick_actions=[],
                context_used={},
                execution_time=(datetime.now() - start_time).total_seconds()
            )

    def _normalize_query(self, query: str) -> str:
        """Normalizar consulta para procesamiento"""
        # Convertir a minúsculas
        normalized = query.lower().strip()
        
        # Eliminar caracteres especiales innecesarios
        normalized = re.sub(r'[^\w\s,:.@-]', '', normalized)
        
        # Normalizar espacios
        normalized = re.sub(r'\s+', ' ', normalized)
        
        return normalized

    def _detect_intent(self, query: str) -> Tuple[Optional[Dict], float]:
        """Detectar intención de la consulta"""
        best_match = None
        best_confidence = 0.0
        
        for intent_name, intent_config in self.intent_patterns.items():
            for pattern in intent_config['patterns']:
                match = re.search(pattern, query, re.IGNORECASE)
                if match:
                    confidence = len(match.group(0)) / len(query)
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_match = {
                            'name': intent_name,
                            'match': match,
                            'action': intent_config['action'],
                            'extractor': intent_config['extractor']
                        }
        
        return best_match, best_confidence

    async def _process_intent(self, intent: Dict, query: str, user_context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Procesar intención detectada"""
        action_type = intent['action']
        extractor = intent['extractor']
        match = intent['match']
        
        # Extraer datos según el tipo de intención
        extracted_data = extractor(match.group(1) if match.groups() else query)
        
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
            
            # Preparar datos para Sheets
            row_data = {
                'Nombre': cliente_data.nombre,
                'Email': cliente_data.email,
                'Zona': cliente_data.zona,
                'Teléfono': cliente_data.telefono,
                'Pago Mensual': cliente_data.pago,
                'Estado': cliente_data.estado,
                'Fecha Registro': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Agregar a Google Sheets
            result = self.sheets_service.add_row(row_data)
            
            message = f"✅ Cliente {cliente_data.nombre} registrado exitosamente."
            if 'ID' in result:
                message += f" ID: {result['ID']}"
            
            return AgentResponse(
                message=message,
                action_type=ActionType.CLIENTE_ALTA,
                response_type=ResponseType.SUCCESS,
                confidence=1.0,
                data={"cliente": cliente_data.__dict__, "result": result},
                suggestions=["Configurar servicios del cliente", "Programar instalación"],
                quick_actions=[
                    {"text": "Ver estadísticas", "action": "estadísticas"},
                    {"text": "Agregar otro cliente", "action": "cliente_alta"}
                ],
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
            message += f"📊 Estado: {client.get('Estado', 'N/A')}"
            
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
            
            # Obtener datos de Sheets
            all_rows = self.sheets_service.get_all_rows()
            
            # Calcular estadísticas
            total_clients = len(all_rows)
            active_clients = len([r for r in all_rows if r.get('Estado', '').lower() == 'activo'])
            
            # Calcular ingresos
            total_revenue = 0
            for row in all_rows:
                try:
                    pago = float(row.get('Pago Mensual', 0))
                    total_revenue += pago
                except (ValueError, TypeError):
                    pass
            
            # Análisis por zonas
            zonas = {}
            for row in all_rows:
                zona = row.get('Zona', 'Sin Zona')
                zonas[zona] = zonas.get(zona, 0) + 1
            
            # Formatear mensaje
            message = f"📊 **ESTADÍSTICAS RED SOLUCIONES ISP**\n\n"
            message += f"👥 **Clientes:**\n"
            message += f"  • Total: {total_clients}\n"
            message += f"  • Activos: {active_clients}\n\n"
            message += f"💰 **Ingresos Mensuales:** ${total_revenue:,.2f}\n\n"
            message += f"📍 **Distribución por Zonas:**\n"
            for zona, count in sorted(zonas.items()):
                message += f"  • {zona}: {count} clientes\n"
            
            # Calcular KPIs
            avg_payment = total_revenue / max(active_clients, 1)
            target_achievement = (total_revenue / self.business_metrics["target_monthly_revenue"]) * 100
            
            message += f"\n📈 **KPIs:**\n"
            message += f"  • Pago promedio: ${avg_payment:.2f}\n"
            message += f"  • Cumplimiento objetivo: {target_achievement:.1f}%"
            
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
                    "avg_payment": avg_payment,
                    "target_achievement": target_achievement
                },
                suggestions=["Revisar clientes inactivos", "Analizar oportunidades de crecimiento"],
                quick_actions=[
                    {"text": "Agregar cliente", "action": "cliente_alta"},
                    {"text": "Ver cliente específico", "action": "cliente_info"}
                ],
                context_used={"sheets_available": True, "data_date": datetime.now().isoformat()},
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

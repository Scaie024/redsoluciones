"""
🤖 AGENTE CONVERSACIONAL MODERNO 2025 - RED SOLUCIONES ISP
=========================================================

Agente de IA conversacional usando las mejores prácticas de 2025:
- Modelos de lenguaje avanzados (GPT-4, Gemini Pro)
- Arquitectura modular y escalable
- Memoria conversacional
- Personalidad humana consistente
- Respuestas contextuales inteligentes
"""

import json
import logging
import re
import os
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum

# IA Models
try:
    import google.generativeai as genai
    from backend.app.core.config import settings
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logging.warning("Google Gemini AI no disponible")

# Configuración del agente
@dataclass
class AgentConfig:
    """Configuración del agente"""
    name: str = "Carlos"
    role: str = "Empleado Back Office & Administrador ISP"
    company: str = "Red Soluciones ISP"
    experience_years: int = 5
    personality: str = "experto técnico, proactivo, detallista y eficiente"
    response_style: str = "como empleado especializado que domina todo el back office"
    max_response_length: int = 600
    use_emojis: bool = True
    language: str = "es-MX"

class ConversationState(Enum):
    """Estados de conversación"""
    GREETING = "greeting"
    NORMAL = "normal"
    COLLECTING_INFO = "collecting_info" 
    PROCESSING_REQUEST = "processing_request"
    SUPPORT_MODE = "support_mode"
    CLARIFYING = "clarifying"

class IntentType(Enum):
    """Tipos de intención - Carlos Back Office"""
    GREETING = "greeting"
    STATS = "stats"
    SEARCH_CLIENT = "search_client"
    LIST_CLIENTS = "list_clients"
    ADD_CLIENT = "add_client"
    UPDATE_CLIENT = "update_client"
    DELETE_CLIENT = "delete_client"
    FINANCIAL_ANALYSIS = "financial_analysis"
    ZONE_ANALYSIS = "zone_analysis"
    PAYMENT_MANAGEMENT = "payment_management"
    TECHNICAL_SUPPORT = "technical_support"
    INCIDENT_REPORT = "incident_report"
    SERVICE_INFO = "service_info"
    CONTACT_INFO = "contact_info"
    BACKUP_DATA = "backup_data"
    GENERATE_REPORT = "generate_report"
    BULK_OPERATIONS = "bulk_operations"
    DATA_EXPORT = "data_export"
    SYSTEM_STATUS = "system_status"
    HELP = "help"
    CHITCHAT = "chitchat"
    UNKNOWN = "unknown"

@dataclass
class ConversationContext:
    """Contexto de conversación"""
    user_id: str
    user_name: str = ""
    conversation_history: Optional[List[Dict]] = None
    current_state: ConversationState = ConversationState.NORMAL
    pending_action: Optional[str] = None
    user_preferences: Optional[Dict] = None
    last_interaction: Optional[datetime] = None
    
    def __post_init__(self):
        if self.conversation_history is None:
            self.conversation_history = []
        if self.user_preferences is None:
            self.user_preferences = {}
        if self.last_interaction is None:
            self.last_interaction = datetime.now()

class ModernISPAgent:
    """🤖 Agente ISP Moderno con IA Avanzada"""
    
    def __init__(self, sheets_service=None, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig()
        self.sheets_service = sheets_service
        self.logger = logging.getLogger(__name__)
        
        # Contexts de usuarios activos
        self.user_contexts: Dict[str, ConversationContext] = {}
        
        # Inicializar IA
        self._initialize_ai()
        
        # Patrones de intención modernos
        self._setup_intent_patterns()
        
        # Base de conocimiento
        self._setup_knowledge_base()
        
        self.logger.info(f"🤖 {self.config.name} (Agente ISP Moderno) inicializado")

    def _initialize_ai(self):
        """🧠 Inicializar modelos de IA"""
        self.ai_model = None
        
        if GEMINI_AVAILABLE:
            try:
                # Verificar si tenemos configuración de settings
                try:
                    from backend.app.core.config import settings
                    api_key = getattr(settings, 'GEMINI_API_KEY', None)
                except ImportError:
                    # Fallback a variable de entorno
                    import os
                    api_key = os.getenv('GEMINI_API_KEY')
                
                if api_key:
                    import google.generativeai as genai
                    genai.configure(api_key=api_key)
                    
                    # Usar el modelo más reciente
                    self.ai_model = genai.GenerativeModel('gemini-1.5-pro')
                    self.logger.info("🧠 Gemini 1.5 Pro conectado exitosamente")
                else:
                    self.logger.warning("🔍 GEMINI_API_KEY no configurada")
                    
            except Exception as e:
                self.logger.error(f"Error conectando Gemini: {e}")
                self.ai_model = None
        else:
            self.logger.warning("🔍 Funcionando sin IA generativa - usando respuestas predefinidas")

    def _setup_intent_patterns(self):
        """🎯 Configurar patrones de detección de intenciones - Carlos Back Office Expert"""
        self.intent_patterns = {
            IntentType.GREETING: {
                "patterns": [
                    r"\b(hola|buenos días|buenas tardes|buenas noches|hey|saludos)\b",
                    r"\b(que tal|como estas|como está)\b",
                    r"^/start$"
                ],
                "keywords": ["hola", "buenos", "hey", "saludos", "que tal"]
            },
            IntentType.STATS: {
                "patterns": [
                    r"\b(estadísticas|estadisticas|números|kpis?|métricas|metricas)\b",
                    r"\b(resumen|dashboard|reporte|cuántos|cuantos clientes)\b",
                    r"\b(¿?cómo vamos|como vamos|situación|estado del negocio)\b",
                    r"\b(facturación|ingresos|revenue|ventas)\b"
                ],
                "keywords": ["estadísticas", "números", "resumen", "clientes", "negocio", "kpis", "métricas"]
            },
            IntentType.SEARCH_CLIENT: {
                "patterns": [
                    r"\b(buscar|busca|encontrar|encuentra|localizar)\b.*\b(cliente|usuario)\b",
                    r"\b(cliente|usuario)\b.*\b(buscar|busca|encontrar)\b",
                    r"\b(información de|datos de|ver)\b.*\b(cliente|usuario)\b",
                    r"\b(consultar|revisar)\b.*\b(cliente|usuario)\b"
                ],
                "keywords": ["buscar", "encontrar", "cliente", "información", "consultar", "revisar"]
            },
            IntentType.ADD_CLIENT: {
                "patterns": [
                    r"\b(agregar|añadir|crear|dar de alta|registrar)\b.*\b(cliente|usuario)\b",
                    r"\b(nuevo cliente|nueva cuenta|alta de)\b",
                    r"\b(ingresar|capturar)\b.*\b(cliente|datos)\b"
                ],
                "keywords": ["agregar", "añadir", "crear", "alta", "nuevo", "registrar", "cliente"]
            },
            IntentType.UPDATE_CLIENT: {
                "patterns": [
                    r"\b(actualizar|modificar|cambiar|editar)\b.*\b(cliente|datos)\b",
                    r"\b(cambio de|modificación de)\b.*\b(dirección|teléfono|plan|datos)\b",
                    r"\b(corregir|ajustar)\b.*\b(información|datos)\b"
                ],
                "keywords": ["actualizar", "modificar", "cambiar", "editar", "corregir", "ajustar"]
            },
            IntentType.DELETE_CLIENT: {
                "patterns": [
                    r"\b(eliminar|borrar|dar de baja|cancelar)\b.*\b(cliente|cuenta|servicio)\b",
                    r"\b(baja de|cancelación de)\b.*\b(cliente|servicio)\b",
                    r"\b(desactivar|suspender)\b.*\b(cuenta|cliente)\b"
                ],
                "keywords": ["eliminar", "borrar", "baja", "cancelar", "desactivar", "suspender"]
            },
            IntentType.PAYMENT_MANAGEMENT: {
                "patterns": [
                    r"\b(pagos|pago|facturación|cobro|cobranza)\b",
                    r"\b(morosos|adeudos|debe|pendiente de pago)\b",
                    r"\b(recibo|factura|comprobante)\b",
                    r"\b(aplicar pago|registrar pago)\b"
                ],
                "keywords": ["pagos", "pago", "morosos", "adeudos", "facturación", "cobro", "recibo"]
            },
            IntentType.ZONE_ANALYSIS: {
                "patterns": [
                    r"\b(zona|zonas|área|sector)\b.*\b(norte|sur|este|oeste|centro|salamanca)\b",
                    r"\b(cobertura|coverage|alcance)\b.*\b(zona|área)\b",
                    r"\b(análisis por zona|reporte de zona)\b"
                ],
                "keywords": ["zona", "zonas", "norte", "sur", "este", "oeste", "centro", "salamanca", "cobertura"]
            },
            IntentType.FINANCIAL_ANALYSIS: {
                "patterns": [
                    r"\b(análisis financiero|finanzas|rentabilidad)\b",
                    r"\b(ingresos|gastos|utilidades|ganancia)\b",
                    r"\b(proyección|forecast|presupuesto)\b",
                    r"\b(flujo de efectivo|cash flow)\b"
                ],
                "keywords": ["financiero", "finanzas", "ingresos", "gastos", "utilidades", "proyección"]
            },
            IntentType.INCIDENT_REPORT: {
                "patterns": [
                    r"\b(incidente|incidencia|reporte|reportar)\b.*\b(falla|problema|caída)\b",
                    r"\b(crear ticket|abrir ticket|nuevo reporte)\b",
                    r"\b(emergencia|urgente|crítico)\b.*\b(problema|falla)\b"
                ],
                "keywords": ["incidente", "reporte", "ticket", "emergencia", "crítico", "falla"]
            },
            IntentType.BACKUP_DATA: {
                "patterns": [
                    r"\b(respaldo|backup|respaldar|guardar)\b.*\b(datos|información)\b",
                    r"\b(exportar|descargar)\b.*\b(base de datos|información)\b",
                    r"\b(copia de seguridad|backup completo)\b"
                ],
                "keywords": ["respaldo", "backup", "exportar", "guardar", "seguridad", "datos"]
            },
            IntentType.GENERATE_REPORT: {
                "patterns": [
                    r"\b(generar|crear|hacer)\b.*\b(reporte|informe)\b",
                    r"\b(reporte de|informe de)\b.*\b(clientes|ventas|pagos|zona)\b",
                    r"\b(exportar reporte|descargar reporte)\b"
                ],
                "keywords": ["generar", "reporte", "informe", "exportar", "descargar"]
            },
            IntentType.BULK_OPERATIONS: {
                "patterns": [
                    r"\b(operación masiva|proceso masivo|lote|bulk)\b",
                    r"\b(actualización masiva|cambio masivo)\b",
                    r"\b(importar|cargar)\b.*\b(archivo|excel|csv)\b"
                ],
                "keywords": ["masiva", "masivo", "lote", "bulk", "importar", "cargar", "archivo"]
            },
            IntentType.SYSTEM_STATUS: {
                "patterns": [
                    r"\b(estado del sistema|status|funcionamiento)\b",
                    r"\b(conectividad|conexión)\b.*\b(google sheets|base de datos)\b",
                    r"\b(salud del sistema|health check)\b"
                ],
                "keywords": ["sistema", "status", "funcionamiento", "conectividad", "salud"]
            },
            IntentType.LIST_CLIENTS: {
                "patterns": [
                    r"\b(listar|mostrar|ver)\b.*\b(clientes|usuarios)\b",
                    r"\b(todos los|lista de)\b.*\b(clientes|usuarios)\b",
                    r"\b(clientes activos|usuarios activos|base completa)\b"
                ],
                "keywords": ["listar", "mostrar", "todos", "clientes", "activos", "lista"]
            },
            IntentType.TECHNICAL_SUPPORT: {
                "patterns": [
                    r"\b(problema|falla|error|no funciona|lento|caído)\b",
                    r"\b(soporte|ayuda técnica|técnico)\b",
                    r"\b(internet no|sin internet|conexión|servicio)\b"
                ],
                "keywords": ["problema", "falla", "soporte", "técnico", "internet", "servicio"]
            },
            IntentType.SERVICE_INFO: {
                "patterns": [
                    r"\b(planes|paquetes|servicios|precios|costos|tarifas)\b",
                    r"\b(cuánto cuesta|precio de|velocidades|mbps)\b",
                    r"\b(catálogo|ofertas|promociones)\b"
                ],
                "keywords": ["planes", "precios", "servicios", "velocidades", "tarifas", "catálogo"]
            }
        }

    def _setup_knowledge_base(self):
        """📚 Base de conocimiento del negocio - Carlos Back Office Expert"""
        self.knowledge_base = {
            "company_info": {
                "name": "Red Soluciones ISP",
                "services": ["Internet residencial", "Internet empresarial", "Soporte técnico", "Instalaciones", "Mantenimiento"],
                "coverage_zones": ["Norte", "Sur", "Centro", "Este", "Oeste", "Salamanca"],
                "business_hours": "Lunes a Viernes 8:00 AM - 6:00 PM",
                "emergency_hours": "24/7 para emergencias críticas",
                "founded": "2019",
                "total_capacity": "1000+ clientes"
            },
            "google_sheets_structure": {
                "main_sheet": "Clientes Red Soluciones",
                "columns": {
                    "A": "ID Cliente",
                    "B": "Nombre Completo", 
                    "C": "Teléfono",
                    "D": "Dirección",
                    "E": "Zona",
                    "F": "Plan",
                    "G": "Velocidad",
                    "H": "Precio/Pago",
                    "I": "Fecha Alta",
                    "J": "Estado/Activo",
                    "K": "Último Pago",
                    "L": "Adeudo",
                    "M": "Notas",
                    "N": "Técnico Asignado",
                    "O": "Fecha Instalación",
                    "P": "Equipo/Router",
                    "Q": "IP Asignada",
                    "R": "Estado Técnico"
                },
                "data_validation": {
                    "Zona": ["Norte", "Sur", "Centro", "Este", "Oeste", "Salamanca"],
                    "Plan": ["Básico", "Estándar", "Premium", "Empresarial"],
                    "Activo": ["Si", "No", "Suspendido", "Moroso"],
                    "Estado Técnico": ["Activo", "Con problemas", "Mantenimiento", "Instalación pendiente"]
                }
            },
            "service_plans": {
                "basico": {
                    "speed": "20 Mbps", 
                    "price": 350, 
                    "type": "Residencial",
                    "description": "Plan ideal para navegación básica y redes sociales",
                    "installation": 500
                },
                "estandar": {
                    "speed": "50 Mbps", 
                    "price": 450, 
                    "type": "Residencial",
                    "description": "Perfecto para streaming y trabajo desde casa",
                    "installation": 500
                },
                "premium": {
                    "speed": "100 Mbps", 
                    "price": 600, 
                    "type": "Residencial/Empresarial",
                    "description": "Alta velocidad para múltiples dispositivos",
                    "installation": 700
                },
                "empresarial": {
                    "speed": "200 Mbps", 
                    "price": 1200, 
                    "type": "Empresarial",
                    "description": "Servicio dedicado con IP fija y soporte prioritario",
                    "installation": 1500
                }
            },
            "back_office_procedures": {
                "alta_cliente": [
                    "1. Verificar disponibilidad en zona",
                    "2. Capturar datos completos en Google Sheets",
                    "3. Asignar ID único de cliente",
                    "4. Programar instalación con técnico",
                    "5. Generar orden de trabajo",
                    "6. Enviar contrato y datos de pago"
                ],
                "baja_cliente": [
                    "1. Verificar motivo de baja",
                    "2. Calcular adeudos pendientes",
                    "3. Programar recuperación de equipo",
                    "4. Actualizar estado en Google Sheets",
                    "5. Liberar IP asignada",
                    "6. Archivar expediente"
                ],
                "cambio_plan": [
                    "1. Verificar plan actual y facturación",
                    "2. Calcular diferencia prorrateada",
                    "3. Actualizar velocidad en sistema",
                    "4. Modificar datos en Google Sheets",
                    "5. Notificar al cliente",
                    "6. Generar nueva facturación"
                ]
            },
            "technical_procedures": {
                "reporte_falla": [
                    "1. Documentar síntomas detallados",
                    "2. Verificar estado del servicio remotamente",
                    "3. Crear ticket en sistema",
                    "4. Asignar técnico según zona",
                    "5. Establecer prioridad y tiempo estimado",
                    "6. Notificar al cliente sobre el proceso"
                ],
                "mantenimiento_preventivo": [
                    "1. Revisar equipos con más de 6 meses",
                    "2. Programar visitas por zona",
                    "3. Verificar calidad de señal",
                    "4. Actualizar firmware si es necesario",
                    "5. Documentar hallazgos",
                    "6. Generar reporte mensual"
                ]
            },
            "financial_kpis": {
                "ingresos_objetivo": 450000,  # Meta mensual
                "clientes_objetivo": 1000,
                "precio_promedio": 480,
                "tasa_conversion": 0.85,
                "churn_rate_max": 0.05,  # 5% máximo mensual
                "dias_promedio_pago": 30,
                "zona_mas_rentable": "Centro",
                "plan_mas_vendido": "Estándar"
            },
            "common_issues": {
                "slow_internet": {
                    "diagnosis": "Verificar conexiones, reiniciar módem, medir velocidad",
                    "solution": "Optimizar configuración, cambiar canal WiFi",
                    "escalation": "Técnico en sitio si persiste"
                },
                "no_connection": {
                    "diagnosis": "Verificar cables, luces del módem, ping a gateway",
                    "solution": "Reinicio completo, verificar configuración",
                    "escalation": "Revisión de infraestructura externa"
                },
                "wifi_problems": {
                    "diagnosis": "Verificar contraseña, alcance de señal, interferencias",
                    "solution": "Reposicionar router, cambiar canal, actualizar drivers",
                    "escalation": "Instalación de repetidor o router adicional"
                },
                "payment_issues": {
                    "diagnosis": "Verificar método de pago, fechas de corte",
                    "solution": "Reactivar servicio tras pago, ajustar fecha de corte",
                    "escalation": "Plan de pagos especial o migración de plan"
                }
            },
            "zone_management": {
                "Norte": {"tecnico": "Juan Pérez", "clientes": 180, "torre": "Torre Norte", "cobertura": "95%"},
                "Sur": {"tecnico": "María González", "clientes": 220, "torre": "Torre Sur", "cobertura": "98%"},
                "Centro": {"tecnico": "Carlos Ruiz", "clientes": 250, "torre": "Torre Centro", "cobertura": "99%"},
                "Este": {"tecnico": "Ana López", "clientes": 160, "torre": "Torre Este", "cobertura": "92%"},
                "Oeste": {"tecnico": "Luis Martín", "clientes": 140, "torre": "Torre Oeste", "cobertura": "90%"},
                "Salamanca": {"tecnico": "Pedro Sánchez", "clientes": 90, "torre": "Torre Salamanca", "cobertura": "88%"}
            }
        }

    async def process_message(self, user_id: str, message: str, user_name: str = "") -> Dict[str, Any]:
        """🧠 Procesar mensaje del usuario"""
        try:
            # Obtener o crear contexto
            context = self._get_or_create_context(user_id, user_name)
            
            # Actualizar historial
            if context.conversation_history is not None:
                context.conversation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "role": "user",
                    "content": message
                })
            
            # Detectar intención
            intent, confidence = self._detect_intent(message, context)
            
            # Generar respuesta
            response = await self._generate_response(message, intent, context, confidence)
            
            # Actualizar contexto
            if context.conversation_history is not None:
                context.conversation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "role": "assistant", 
                    "content": response["text"]
                })
            context.last_interaction = datetime.now()
            
            # Mantener historial limitado (últimos 20 mensajes)
            if context.conversation_history is not None and len(context.conversation_history) > 20:
                context.conversation_history = context.conversation_history[-20:]
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error procesando mensaje: {e}")
            return {
                "text": "Disculpa, tuve un pequeño problema técnico. ¿Puedes repetir tu pregunta?",
                "type": "error",
                "intent": "unknown",
                "confidence": 0.0
            }

    def _get_or_create_context(self, user_id: str, user_name: str = "") -> ConversationContext:
        """👤 Obtener o crear contexto de usuario"""
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = ConversationContext(
                user_id=user_id,
                user_name=user_name
            )
        elif user_name and not self.user_contexts[user_id].user_name:
            self.user_contexts[user_id].user_name = user_name
            
        return self.user_contexts[user_id]

    def _detect_intent(self, message: str, context: ConversationContext) -> Tuple[IntentType, float]:
        """🎯 Detectar intención del mensaje"""
        message_lower = message.lower().strip()
        
        # Verificar contexto de conversación
        if context.current_state == ConversationState.GREETING:
            return IntentType.GREETING, 1.0
            
        # Búsqueda por patrones regex y keywords
        intent_scores = {}
        
        for intent_type, config in self.intent_patterns.items():
            score = 0.0
            
            # Verificar patrones regex
            for pattern in config["patterns"]:
                if re.search(pattern, message_lower):
                    score += 0.7
            
            # Verificar keywords
            for keyword in config["keywords"]:
                if keyword in message_lower:
                    score += 0.3
            
            if score > 0:
                intent_scores[intent_type] = min(score, 1.0)
        
        # Retornar intención con mayor score
        if intent_scores:
            best_intent = max(intent_scores.keys(), key=lambda k: intent_scores[k])
            confidence = intent_scores[best_intent]
            return best_intent, confidence
        
        return IntentType.UNKNOWN, 0.0

    async def _generate_response(self, message: str, intent: IntentType, context: ConversationContext, confidence: float) -> Dict[str, Any]:
        """💬 Generar respuesta inteligente"""
        
        # Preparar contexto para IA
        conversation_context = self._build_conversation_context(context)
        business_context = await self._get_business_context(intent)
        
        # Generar respuesta usando IA
        if self.ai_model and confidence > 0.3:
            response_text = await self._generate_ai_response(
                message, intent, conversation_context, business_context
            )
        else:
            response_text = self._generate_fallback_response(intent, message)
        
        # Generar sugerencias inteligentes
        suggestions = self._generate_suggestions(intent, context)
        
        return {
            "text": response_text,
            "type": intent.value,
            "intent": intent.value,
            "confidence": confidence,
            "suggestions": suggestions,
            "quick_actions": self._get_quick_actions(intent)
        }

    def _build_conversation_context(self, context: ConversationContext) -> str:
        """📝 Construir contexto de conversación"""
        if context.conversation_history is None:
            return f"Usuario: {context.user_name or 'Cliente'}\nConversación nueva\n"
            
        recent_messages = context.conversation_history[-6:]  # Últimos 6 mensajes
        
        context_text = f"Usuario: {context.user_name or 'Cliente'}\n"
        context_text += "Conversación reciente:\n"
        
        for msg in recent_messages:
            role = "👤 Usuario" if msg["role"] == "user" else f"🤖 {self.config.name}"
            context_text += f"{role}: {msg['content']}\n"
        
        return context_text

    async def _get_business_context(self, intent: IntentType) -> str:
        """💼 Obtener contexto del negocio"""
        context = f"Empresa: {self.knowledge_base['company_info']['name']}\n"
        
        if intent in [IntentType.STATS, IntentType.LIST_CLIENTS, IntentType.SEARCH_CLIENT]:
            # Obtener datos reales del negocio
            try:
                if self.sheets_service:
                    clients = self.sheets_service.get_all_clients() or []
                    context += f"Total clientes: {len(clients)}\n"
                    
                    # Calcular métricas básicas
                    if clients:
                        active_clients = [c for c in clients if str(c.get('Activo', '')).lower() in ['si', 'sí', 'yes', '1']]
                        total_revenue = sum(self._extract_payment(c) for c in active_clients)
                        context += f"Clientes activos: {len(active_clients)}\n"
                        context += f"Ingresos mensuales: ${total_revenue:,.0f}\n"
            except Exception as e:
                self.logger.error(f"Error obteniendo contexto de negocio: {e}")
                
        elif intent == IntentType.SERVICE_INFO:
            context += "Planes disponibles:\n"
            for plan_name, plan_info in self.knowledge_base['service_plans'].items():
                context += f"- {plan_info['speed']}: ${plan_info['price']}/mes\n"
                
        return context

    async def _generate_ai_response(self, message: str, intent: IntentType, conversation_context: str, business_context: str) -> str:
        """🤖 Generar respuesta usando IA"""
        try:
            if self.ai_model is None:
                return self._generate_fallback_response(intent, message)
                
            # Construir prompt optimizado para Back Office Expert
            system_prompt = f"""
Eres {self.config.name}, {self.config.role} de {self.config.company} con {self.config.experience_years} años de experiencia.

ERES EL EMPLEADO BACK OFFICE EXPERTO del dueño de Red Soluciones ISP.

CONOCES GOOGLE SHEETS DE MEMORIA:
- Estructura completa: ID Cliente (A), Nombre (B), Teléfono (C), Dirección (D), Zona (E), Plan (F), Velocidad (G), Precio (H), Fecha Alta (I), Activo (J), Último Pago (K), Adeudo (L), Notas (M), Técnico (N), Instalación (O), Equipo (P), IP (Q), Estado Técnico (R)
- Zonas: Norte, Sur, Centro, Este, Oeste, Salamanca
- Planes: Básico (20 Mbps, $350), Estándar (50 Mbps, $450), Premium (100 Mbps, $600), Empresarial (200 Mbps, $1200)
- Técnicos por zona: Norte (Juan Pérez), Sur (María González), Centro (Carlos Ruiz), Este (Ana López), Oeste (Luis Martín), Salamanca (Pedro Sánchez)

PUEDES HACER TODO EN EL BACK OFFICE:
- Dar de alta/baja clientes
- Modificar datos en Google Sheets
- Generar reportes financieros
- Gestionar incidentes técnicos
- Análisis por zonas
- Control de pagos y adeudos
- Respaldos y exportaciones
- Operaciones masivas

PERSONALIDAD EXPERTA:
- {self.config.personality}
- Dominas completamente el sistema
- Conoces cada procedimiento de memoria
- Siempre proactivo y eficiente
- Tratas al usuario como "jefe" con profesionalismo
- Das soluciones específicas y detalladas

CONTEXTO DEL NEGOCIO:
{business_context}

CONVERSACIÓN:
{conversation_context}

TU JEFE TE DICE: "{message}"

INSTRUCCIONES:
- Responde como EXPERTO EN BACK OFFICE que conoce todo el sistema
- Si te piden dar de alta un cliente, explica el proceso específico
- Si necesitan reportes, especifica qué datos puedes extraer
- Menciona campos específicos de Google Sheets cuando sea relevante
- Sé proactivo sugiriendo mejoras o validaciones
- Máximo {self.config.max_response_length} caracteres
- Incluye emojis técnicos apropiados

RESPUESTA:"""

            response = self.ai_model.generate_content(system_prompt)
            return response.text.strip()
            
        except Exception as e:
            self.logger.error(f"Error generando respuesta IA: {e}")
            return self._generate_fallback_response(intent, message)

    def _generate_fallback_response(self, intent: IntentType, message: str) -> str:
        """🔄 Generar respuesta de fallback - Back Office Expert"""
        responses = {
            IntentType.GREETING: f"¡Buenos días, jefe! Soy {self.config.name}, su especialista en back office. Listo para gestionar clientes, reportes, Google Sheets y todo el sistema. ¿Qué necesita?",
            IntentType.STATS: "Perfecto, jefe. Le traigo las métricas completas: total de clientes, ingresos mensuales, análisis por zonas, morosos y KPIs. ¿Algo específico?",
            IntentType.SEARCH_CLIENT: "Claro, jefe. Puedo buscar por nombre, teléfono, dirección, zona o cualquier campo de Google Sheets. ¿Qué criterio prefiere?",
            IntentType.ADD_CLIENT: "Excelente, jefe. Para dar de alta necesito: Nombre completo, teléfono, dirección, zona, plan deseado. Asigno ID automático y programo instalación. ¿Empezamos?",
            IntentType.UPDATE_CLIENT: "Perfecto, jefe. Puedo modificar cualquier campo: cambio de plan, actualizar dirección, teléfono, estado de pago. ¿Qué cliente y qué datos modificamos?",
            IntentType.LIST_CLIENTS: "Enseguida, jefe. ¿Quiere todos los clientes, solo activos, por zona específica, o con filtro especial? Puedo generar el reporte completo.",
            IntentType.PAYMENT_MANAGEMENT: "Entendido, jefe. Puedo revisar pagos, generar lista de morosos, aplicar pagos, ajustar fechas de corte. ¿Qué gestión de cobranza necesita?",
            IntentType.ZONE_ANALYSIS: "Perfecto, jefe. Analizo zona específica: clientes totales, ingresos, técnico asignado, cobertura, problemas frecuentes. ¿Qué zona revisamos?",
            IntentType.TECHNICAL_SUPPORT: "Entendido, jefe. Creo ticket, asigno técnico por zona, establezco prioridad, actualizo estado en sistema. ¿Detalles del problema?",
            IntentType.INCIDENT_REPORT: "De inmediato, jefe. Documento incidente, asigno técnico responsable, creo plan de solución, notificación a clientes afectados. ¿Qué tipo de incidente?",
            IntentType.GENERATE_REPORT: "Claro, jefe. Puedo generar: reporte financiero, clientes por zona, análisis de pagos, KPIs, exportación completa. ¿Qué reporte necesita?",
            IntentType.BACKUP_DATA: "Perfecto, jefe. Ejecuto respaldo completo de Google Sheets, exporto en múltiples formatos, verifico integridad. ¿Respaldo completo o específico?",
            IntentType.BULK_OPERATIONS: "Entendido, jefe. Manejo actualizaciones masivas, importación de archivos, cambios de plan múltiples, operaciones por lotes. ¿Qué operación masiva?",
            IntentType.SYSTEM_STATUS: "Checking sistema, jefe. Estado Google Sheets: conectado ✅ Base de datos: actualizada ✅ Servicios: operando ✅ ¿Algo específico que revisar?",
            IntentType.FINANCIAL_ANALYSIS: "Análisis financiero listo, jefe. Ingresos actuales, proyecciones, rentabilidad por zona, planes más vendidos, flujo de efectivo. ¿Qué métrica priorizar?",
            IntentType.SERVICE_INFO: "Claro, jefe. Planes disponibles: Básico 20 Mbps ($350), Estándar 50 Mbps ($450), Premium 100 Mbps ($600), Empresarial 200 Mbps ($1200). ¿Detalles específicos?",
            IntentType.HELP: f"Estoy aquí para todo el back office, jefe. Manejo: altas/bajas, modificaciones, reportes, análisis financiero, gestión técnica, respaldos, Google Sheets completo. ¿En qué empezamos?",
            IntentType.UNKNOWN: "Disculpe, jefe, no captué bien. Puedo ayudarle con: gestión de clientes, reportes financieros, análisis por zonas, incidentes técnicos, operaciones masivas. ¿Podría especificar?"
        }
        
        return responses.get(intent, responses[IntentType.UNKNOWN])

    def _generate_suggestions(self, intent: IntentType, context: ConversationContext) -> List[str]:
        """💡 Generar sugerencias inteligentes - Back Office Expert"""
        base_suggestions = {
            IntentType.GREETING: [
                "📊 Ver dashboard completo", 
                "👥 Gestionar clientes", 
                "💰 Análisis financiero",
                "🔧 Revisar incidentes técnicos",
                "📋 Generar reportes"
            ],
            IntentType.STATS: [
                "📍 Análisis por zonas",
                "💸 Reporte financiero detallado", 
                "👥 Lista de morosos",
                "📈 Proyecciones de ingresos",
                "🎯 KPIs del mes"
            ],
            IntentType.SEARCH_CLIENT: [
                "📋 Listar todos los clientes",
                "🌍 Buscar por zona específica",
                "💰 Verificar estado de pagos",
                "✏️ Modificar datos cliente",
                "📊 Historial del cliente"
            ],
            IntentType.ADD_CLIENT: [
                "🔍 Verificar disponibilidad zona",
                "📋 Programar instalación",
                "💳 Configurar método de pago",
                "📄 Generar contrato",
                "📧 Enviar datos de acceso"
            ],
            IntentType.UPDATE_CLIENT: [
                "📊 Ver historial de cambios",
                "💰 Ajustar facturación",
                "📞 Notificar al cliente",
                "🔧 Actualizar configuración técnica"
            ],
            IntentType.PAYMENT_MANAGEMENT: [
                "💸 Generar reporte de morosos",
                "📅 Ajustar fechas de corte",
                "💳 Aplicar pagos pendientes",
                "📋 Crear plan de pagos"
            ],
            IntentType.ZONE_ANALYSIS: [
                "👥 Ver clientes por zona",
                "🔧 Contactar técnico asignado",
                "📊 Análisis de cobertura",
                "💰 Rentabilidad de zona"
            ],
            IntentType.TECHNICAL_SUPPORT: [
                "🎫 Crear nuevo ticket",
                "👨‍🔧 Asignar técnico por zona",
                "📱 Notificar al cliente",
                "📋 Ver historial de problemas"
            ],
            IntentType.INCIDENT_REPORT: [
                "🚨 Clasificar prioridad",
                "👥 Identificar clientes afectados",
                "📞 Plan de comunicación",
                "⏱️ Tiempo estimado solución"
            ],
            IntentType.BACKUP_DATA: [
                "💾 Programar respaldo automático",
                "📤 Exportar a Excel",
                "☁️ Subir a drive de respaldo",
                "✅ Verificar integridad"
            ],
            IntentType.GENERATE_REPORT: [
                "📊 Exportar a Excel",
                "📧 Enviar por email",
                "📅 Programar reporte recurrente",
                "📈 Incluir gráficos"
            ]
        }
        
        return base_suggestions.get(intent, [
            "📊 Ver estadísticas completas",
            "👥 Gestionar clientes", 
            "💰 Análisis financiero",
            "🔧 Soporte técnico",
            "📋 Generar reportes"
        ])

    def _get_quick_actions(self, intent: IntentType) -> List[Dict[str, str]]:
        """⚡ Obtener acciones rápidas"""
        actions = {
            IntentType.GREETING: [
                {"text": "📊 Estadísticas", "action": "stats"},
                {"text": "🔍 Buscar", "action": "search"},
                {"text": "📋 Servicios", "action": "services"}
            ],
            IntentType.STATS: [
                {"text": "📍 Por zonas", "action": "zones"},
                {"text": "💰 Financiero", "action": "financial"},
                {"text": "👥 Clientes", "action": "clients"}
            ]
        }
        
        return actions.get(intent, [])

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

    def get_user_stats(self) -> Dict[str, Any]:
        """📊 Estadísticas de usuarios activos"""
        active_users = len([
            ctx for ctx in self.user_contexts.values()
            if ctx.last_interaction is not None and ctx.last_interaction > datetime.now() - timedelta(hours=24)
        ])
        
        return {
            "total_contexts": len(self.user_contexts),
            "active_24h": active_users,
            "ai_available": self.ai_model is not None
        }

# Instancia global del agente moderno
modern_agent = None

def initialize_modern_agent(sheets_service=None, config: Optional[AgentConfig] = None):
    """🚀 Inicializar agente moderno"""
    global modern_agent
    modern_agent = ModernISPAgent(sheets_service, config)
    return modern_agent

def get_modern_agent():
    """🤖 Obtener instancia del agente moderno"""
    return modern_agent

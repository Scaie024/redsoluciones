"""
🤖 AGENTE IA EMPRESARIAL HOMOLOGADO - Red Soluciones ISP
=====================================================

Agente IA completamente integrado con el contexto completo del negocio.
Utiliza el ContextEngine para respuestas precisas y acciones ejecutables.

Características:
- Comprensión completa del negocio ISP
- Contexto por propietario (Eduardo/Omar)
- Respuestas con datos reales del Google Sheets
- Acciones ejecutables automáticamente
- Análisis inteligente de patrones de negocio
"""

import asyncio
import json
import logging
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import os

# === CONFIGURACIÓN GEMINI AI ===
GEMINI_AVAILABLE = False
try:
    import google.generativeai as genai
    
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and len(api_key) > 20:
        genai.configure(api_key=api_key)
        GEMINI_AVAILABLE = True
        logging.info("✅ IA Empresarial: Sistema operacional")
    else:
        logging.warning("⚠️ API Key de IA requerida para funcionalidad completa")
except ImportError:
    logging.warning("⚠️ Módulo google-generativeai no disponible")
except Exception as e:
    logging.error(f"❌ Error configurando IA: {e}")

@dataclass
class AgentResponse:
    """Respuesta estructurada del agente IA"""
    message: str
    action_type: str
    confidence: float
    data: Dict[str, Any]
    suggestions: List[str]
    quick_actions: List[Dict[str, str]]
    context_used: Dict[str, Any]

@dataclass
class BusinessInsight:
    """Insight de negocio generado por IA"""
    type: str  # 'warning', 'opportunity', 'success', 'info'
    title: str
    description: str
    recommended_action: str
    impact_level: str  # 'high', 'medium', 'low'
    data_source: str

class HomologatedAIAgent:
    """
    Agente IA empresarial completamente homologado que comprende
    TODO el contexto del negocio Red Soluciones ISP.
    """
    
    def __init__(self, context_engine, sheets_service):
        self.context = context_engine
        self.sheets = sheets_service
        self.logger = logging.getLogger(__name__)
        
        # Configuración del agente
        self.company = "Red Soluciones ISP"
        self.version = "4.0 Homologado"
        
        # Configuración IA
        self.ai_model = None
        if GEMINI_AVAILABLE:
            try:
                self.ai_model = genai.GenerativeModel(
                    'gemini-1.5-flash',
                    system_instruction=self._get_system_prompt()
                )
                self.logger.info("🧠 IA configurada exitosamente - Modo empresarial homologado")
            except Exception as e:
                self.logger.error(f"❌ Error configurando IA: {e}")
        
        # Patrones de intención empresarial
        self.intent_patterns = {
            'cliente_info': {
                'patterns': [
                    r'(?:información|datos|detalles).*(?:cliente|usuario)',
                    r'(?:estado|situación).*cliente',
                    r'cliente.*(?:llamado|llamada|nombre)',
                    r'buscar cliente',
                    r'ver cliente'
                ],
                'action': 'get_cliente_info',
                'confidence_base': 0.8
            },
            'crear_incidente': {
                'patterns': [
                    r'(?:crear|abrir|reportar).*(?:incidente|ticket|problema)',
                    r'cliente.*(?:problema|falla|incidencia)',
                    r'reportar.*(?:técnico|servicio|conexión)',
                    r'incidente.*(?:nuevo|crear)'
                ],
                'action': 'create_incidente',
                'confidence_base': 0.9
            },
            'add_cliente': {
                'patterns': [
                    r'(?:agregar|añadir|registrar).*cliente',
                    r'nuevo cliente',
                    r'cliente.*nuevo',
                    r'alta.*cliente'
                ],
                'action': 'add_cliente',
                'confidence_base': 0.85
            },
            'add_prospecto': {
                'patterns': [
                    r'(?:agregar|añadir|registrar).*prospecto',
                    r'nuevo.*(?:prospecto|lead)',
                    r'prospecto.*nuevo',
                    r'potencial cliente'
                ],
                'action': 'add_prospecto',
                'confidence_base': 0.85
            },
            'estadisticas_negocio': {
                'patterns': [
                    r'(?:estadísticas|métricas|números|datos).*(?:negocio|empresa)',
                    r'dashboard',
                    r'kpis?',
                    r'rendimiento.*negocio',
                    r'estado.*empresa'
                ],
                'action': 'get_business_stats',
                'confidence_base': 0.8
            },
            'ingresos_analisis': {
                'patterns': [
                    r'(?:ingresos|dinero|ganancias|facturación)',
                    r'cuánto.*(?:genero|gano|ingreso)',
                    r'dinero.*mes',
                    r'ingresos.*mes'
                ],
                'action': 'analyze_revenue',
                'confidence_base': 0.8
            },
            'incidentes_pendientes': {
                'patterns': [
                    r'incidentes.*(?:pendientes|abiertos|sin resolver)',
                    r'problemas.*pendientes',
                    r'tickets.*abiertos',
                    r'qué.*problemas'
                ],
                'action': 'get_pending_incidents',
                'confidence_base': 0.9
            }
        }
        
        # Memoria de conversación
        self.conversation_memory = {}
        
        self.logger.info(f"🤖 Agente IA Homologado v{self.version} inicializado")

    def _get_system_prompt(self) -> str:
        """Prompt optimizado para el sistema empresarial"""
        return """Eres el AGENTE IA EMPRESARIAL HOMOLOGADO de Red Soluciones ISP.

IDENTIDAD:
- Asistente empresarial profesional para Eduardo y Omar (propietarios)
- Especialista en gestión de ISP y telecomunicaciones
- Conocimiento completo del negocio y sus operaciones

PERSONALIDAD:
- Profesional y eficiente
- Respuestas concisas y orientadas a acción
- Uso de datos reales del sistema
- Sugerencias proactivas para mejorar el negocio

CAPACIDADES PRINCIPALES:
- Consulta completa de clientes, prospectos e incidentes
- Análisis de métricas de negocio en tiempo real
- Generación de insights automáticos
- Ejecución de acciones empresariales
- Filtrado automático por propietario (Eduardo/Omar)

CONTEXTO DE NEGOCIO:
- Red Soluciones ISP: Proveedor de internet residencial
- Dos propietarios: Eduardo y Omar
- Google Sheets como backend centralizado
- Gestión de clientes, prospectos, incidentes y zonas

REGLAS DE RESPUESTA:
1. Siempre usar datos reales del sistema
2. Filtrar información según el propietario solicitante
3. Proporcionar insights accionables
4. Sugerir próximos pasos concretos
5. Mantener contexto de la conversación

FORMATO DE RESPUESTA:
- Respuesta directa a la consulta
- Datos específicos cuando estén disponibles
- Sugerencias de acciones relevantes
- Máximo 3-4 líneas por respuesta

Responde siempre en español y mantén el enfoque empresarial."""

    async def process_query(
        self, 
        query: str, 
        propietario: str,
        session_id: Optional[str] = None
    ) -> AgentResponse:
        """
        Procesa una consulta del usuario con contexto completo del negocio.
        
        Args:
            query: Consulta del usuario
            propietario: Eduardo o Omar
            session_id: ID de sesión para memoria
            
        Returns:
            AgentResponse con respuesta completa y acciones
        """
        try:
            start_time = datetime.now()
            
            # 1. Obtener contexto completo del propietario
            full_context = await self.context.get_full_context(propietario)
            
            if 'error' in full_context:
                return AgentResponse(
                    message="Error accediendo al contexto del sistema. Intenta de nuevo.",
                    action_type="error",
                    confidence=0.0,
                    data={},
                    suggestions=[],
                    quick_actions=[],
                    context_used={}
                )
            
            # 2. Analizar intención del usuario
            intent_result = await self._analyze_intent(query)
            
            # 3. Ejecutar acción según la intención
            if intent_result['action'] and hasattr(self, f"_execute_{intent_result['action']}"):
                action_method = getattr(self, f"_execute_{intent_result['action']}")
                result = await action_method(query, full_context, intent_result)
            else:
                # Fallback: respuesta con IA generativa
                result = await self._generate_ai_response(query, full_context, intent_result)
            
            # 4. Agregar contexto y sugerencias
            result.context_used = {
                'propietario': propietario,
                'entities_consulted': len(full_context.get('user_context', {}).get('clientes_asignados', [])),
                'processing_time': (datetime.now() - start_time).total_seconds(),
                'intent_detected': intent_result['action']
            }
            
            # 5. Guardar en memoria de conversación
            if session_id:
                self._update_conversation_memory(session_id, query, result)
            
            self.logger.info(f"✅ Query procesado: {intent_result['action']} - {result.confidence:.2f}")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Error procesando query: {e}")
            return AgentResponse(
                message=f"Error procesando solicitud: {str(e)}",
                action_type="error",
                confidence=0.0,
                data={'error': str(e)},
                suggestions=["Intenta reformular tu consulta", "Verifica la conexión del sistema"],
                quick_actions=[],
                context_used={}
            )

    async def _analyze_intent(self, query: str) -> Dict[str, Any]:
        """Analiza la intención del usuario usando patrones"""
        query_lower = query.lower()
        best_match = {
            'action': None,
            'confidence': 0.0,
            'pattern_matched': None
        }
        
        for intent_name, intent_config in self.intent_patterns.items():
            for pattern in intent_config['patterns']:
                if re.search(pattern, query_lower):
                    confidence = intent_config['confidence_base']
                    
                    # Ajustar confianza según contexto adicional
                    if len(query.split()) > 3:  # Consultas más específicas
                        confidence += 0.1
                    if any(word in query_lower for word in ['urgente', 'problema', 'error']):
                        confidence += 0.05
                    
                    if confidence > best_match['confidence']:
                        best_match = {
                            'action': intent_config['action'],
                            'confidence': min(confidence, 1.0),
                            'pattern_matched': pattern
                        }
                        break
        
        return best_match

    # === EJECUTORES DE ACCIONES ESPECÍFICAS ===

    async def _execute_get_cliente_info(
        self, 
        query: str, 
        context: Dict[str, Any], 
        intent: Dict[str, Any]
    ) -> AgentResponse:
        """Busca información específica de un cliente"""
        
        # Extraer nombre del cliente de la consulta
        cliente_name = self._extract_client_name(query)
        user_context = context.get('user_context', {})
        clientes = user_context.get('clientes_asignados', [])
        
        if cliente_name:
            # Buscar cliente específico
            cliente_encontrado = None
            for cliente in clientes:
                if cliente_name.lower() in cliente.get('Nombre', '').lower():
                    cliente_encontrado = cliente
                    break
            
            if cliente_encontrado:
                # Obtener información relacionada
                incidentes_cliente = self._get_client_incidents(cliente_encontrado.get('ID'), context)
                
                response_message = f"""Cliente: {cliente_encontrado.get('Nombre')}
• Plan: {cliente_encontrado.get('Plan')} - ${cliente_encontrado.get('Pago_Mensual', 0)}/mes
• Estado: {cliente_encontrado.get('Estado')} - Zona: {cliente_encontrado.get('Zona')}
• Incidentes abiertos: {len(incidentes_cliente)}"""

                return AgentResponse(
                    message=response_message,
                    action_type="cliente_info",
                    confidence=intent['confidence'],
                    data={
                        'cliente': cliente_encontrado,
                        'incidentes': incidentes_cliente
                    },
                    suggestions=[
                        "Ver historial completo",
                        "Crear nuevo incidente",
                        "Actualizar información"
                    ],
                    quick_actions=[
                        {'action': 'view_client_history', 'label': 'Ver Historial'},
                        {'action': 'create_incident', 'label': 'Nuevo Incidente'},
                        {'action': 'edit_client', 'label': 'Editar Info'}
                    ],
                    context_used={}
                )
            else:
                return AgentResponse(
                    message=f"No encontré cliente '{cliente_name}' en tu cartera. ¿Quizás sea un prospecto?",
                    action_type="cliente_not_found",
                    confidence=0.7,
                    data={'search_term': cliente_name},
                    suggestions=[
                        "Buscar en prospectos",
                        "Agregar como nuevo cliente",
                        "Revisar ortografía del nombre"
                    ],
                    quick_actions=[
                        {'action': 'search_prospects', 'label': 'Buscar Prospectos'},
                        {'action': 'add_client', 'label': 'Agregar Cliente'}
                    ],
                    context_used={}
                )
        else:
            # Mostrar resumen de clientes
            total_clientes = len(clientes)
            clientes_activos = len([c for c in clientes if c.get('Estado') == 'Activo'])
            
            return AgentResponse(
                message=f"Tienes {total_clientes} clientes asignados, {clientes_activos} activos. ¿De cuál necesitas información específica?",
                action_type="clientes_summary",
                confidence=0.8,
                data={
                    'total_clientes': total_clientes,
                    'clientes_activos': clientes_activos,
                    'clientes_sample': clientes[:5]  # Primeros 5 para referencia
                },
                suggestions=[
                    "Especificar nombre del cliente",
                    "Ver lista completa",
                    "Filtrar por zona o estado"
                ],
                quick_actions=[
                    {'action': 'list_all_clients', 'label': 'Lista Completa'},
                    {'action': 'filter_clients', 'label': 'Filtrar Clientes'}
                ],
                context_used={}
            )

    async def _execute_get_business_stats(
        self, 
        query: str, 
        context: Dict[str, Any], 
        intent: Dict[str, Any]
    ) -> AgentResponse:
        """Proporciona estadísticas del negocio"""
        
        business_context = context.get('business_context', {})
        user_context = context.get('user_context', {})
        
        # Stats globales vs personales
        if 'mi' in query.lower() or 'mis' in query.lower():
            # Stats personales
            kpis = user_context.get('kpis_personales', {})
            propietario = user_context.get('propietario', 'Usuario')
            
            response_message = f"""📊 Tus métricas, {propietario}:
• Clientes: {kpis.get('clientes_total', 0)} - Ingresos: ${kpis.get('ingresos_responsable', 0):,.2f}/mes
• Incidentes pendientes: {kpis.get('incidentes_pendientes', 0)}
• Zonas responsables: {len(user_context.get('zonas_responsable', []))}"""
        else:
            # Stats globales del negocio
            response_message = f"""📈 Estado del negocio Red Soluciones ISP:
• Total clientes: {business_context.get('total_clientes', 0)} ({business_context.get('clientes_activos', 0)} activos)
• Ingresos mensuales: ${business_context.get('ingresos_mensuales', 0):,.2f}
• ARPU: ${business_context.get('arpu', 0):.2f} - Churn: {business_context.get('churn_rate', 0):.1f}%"""

        return AgentResponse(
            message=response_message,
            action_type="business_stats",
            confidence=intent['confidence'],
            data={
                'business_context': business_context,
                'user_kpis': user_context.get('kpis_personales', {})
            },
            suggestions=[
                "Ver tendencias mensuales",
                "Analizar por zona",
                "Comparar con competencia"
            ],
            quick_actions=[
                {'action': 'detailed_analytics', 'label': 'Análisis Detallado'},
                {'action': 'export_report', 'label': 'Exportar Reporte'}
            ],
            context_used={}
        )

    async def _execute_get_pending_incidents(
        self, 
        query: str, 
        context: Dict[str, Any], 
        intent: Dict[str, Any]
    ) -> AgentResponse:
        """Muestra incidentes pendientes"""
        
        user_context = context.get('user_context', {})
        incidentes = user_context.get('incidentes_responsable', [])
        incidentes_abiertos = [i for i in incidentes if i.get('Estado') == 'Abierto']
        
        if incidentes_abiertos:
            # Mostrar incidentes por prioridad
            alta_prioridad = [i for i in incidentes_abiertos if i.get('Prioridad') == 'Alta']
            
            response_parts = [f"🚨 Tienes {len(incidentes_abiertos)} incidentes pendientes"]
            
            if alta_prioridad:
                response_parts.append(f"⚠️ {len(alta_prioridad)} de alta prioridad:")
                for inc in alta_prioridad[:3]:  # Mostrar máximo 3
                    response_parts.append(f"• {inc.get('Tipo')}: {inc.get('Descripcion', '')[:50]}...")
            
            response_message = '\n'.join(response_parts)
            
            return AgentResponse(
                message=response_message,
                action_type="pending_incidents",
                confidence=intent['confidence'],
                data={
                    'incidentes_abiertos': incidentes_abiertos,
                    'alta_prioridad': alta_prioridad
                },
                suggestions=[
                    "Resolver incidentes de alta prioridad",
                    "Asignar técnicos",
                    "Contactar clientes afectados"
                ],
                quick_actions=[
                    {'action': 'prioritize_incidents', 'label': 'Priorizar'},
                    {'action': 'assign_technician', 'label': 'Asignar Técnico'}
                ],
                context_used={}
            )
        else:
            return AgentResponse(
                message="🎉 ¡Excelente! No tienes incidentes pendientes. Todas las solicitudes están resueltas.",
                action_type="no_pending_incidents",
                confidence=intent['confidence'],
                data={'incidentes_count': 0},
                suggestions=[
                    "Revisar incidentes resueltos",
                    "Preparar reporte de gestión",
                    "Contactar clientes para seguimiento"
                ],
                quick_actions=[
                    {'action': 'review_resolved', 'label': 'Ver Resueltos'},
                    {'action': 'client_followup', 'label': 'Seguimiento'}
                ],
                context_used={}
            )

    async def _generate_ai_response(
        self, 
        query: str, 
        context: Dict[str, Any], 
        intent: Dict[str, Any]
    ) -> AgentResponse:
        """Genera respuesta usando IA cuando no hay acción específica"""
        
        if not self.ai_model:
            return AgentResponse(
                message="Sistema funcionando en modo básico. ¿En qué puedo ayudarte específicamente?",
                action_type="basic_response",
                confidence=0.5,
                data={},
                suggestions=[
                    "Ver estadísticas del negocio",
                    "Consultar cliente específico",
                    "Revisar incidentes pendientes"
                ],
                quick_actions=[],
                context_used={}
            )
        
        try:
            # Construir prompt con contexto completo
            business_context = context.get('business_context', {})
            user_context = context.get('user_context', {})
            
            context_prompt = f"""
            CONTEXTO DEL NEGOCIO:
            - Total clientes: {business_context.get('total_clientes', 0)}
            - Ingresos mensuales: ${business_context.get('ingresos_mensuales', 0):,.2f}
            - Incidentes abiertos: {business_context.get('incidentes_abiertos', 0)}
            
            CONTEXTO DEL USUARIO ({user_context.get('propietario', 'Usuario')}):
            - Clientes asignados: {user_context.get('kpis_personales', {}).get('clientes_total', 0)}
            - Ingresos responsable: ${user_context.get('kpis_personales', {}).get('ingresos_responsable', 0):,.2f}
            - Incidentes pendientes: {user_context.get('kpis_personales', {}).get('incidentes_pendientes', 0)}
            
            CONSULTA DEL USUARIO: {query}
            
            Responde de manera profesional y específica usando estos datos reales.
            Máximo 3 líneas.
            """
            
            response = await self.ai_model.generate_content_async(context_prompt)
            ai_message = response.text if response else "No pude procesar tu consulta en este momento."
            
            return AgentResponse(
                message=ai_message,
                action_type="ai_response",
                confidence=0.7,
                data={'ai_generated': True},
                suggestions=[
                    "¿Necesitas información más específica?",
                    "Ver datos detallados",
                    "Ejecutar alguna acción"
                ],
                quick_actions=[
                    {'action': 'get_details', 'label': 'Más Detalles'},
                    {'action': 'take_action', 'label': 'Tomar Acción'}
                ],
                context_used={}
            )
            
        except Exception as e:
            self.logger.error(f"Error generando respuesta IA: {e}")
            return AgentResponse(
                message="Error procesando con IA. ¿Puedes ser más específico en tu consulta?",
                action_type="ai_error",
                confidence=0.3,
                data={'error': str(e)},
                suggestions=[
                    "Reformular la consulta",
                    "Usar comandos específicos",
                    "Contactar soporte técnico"
                ],
                quick_actions=[],
                context_used={}
            )

    # === UTILIDADES ===

    def _extract_client_name(self, query: str) -> Optional[str]:
        """Extrae el nombre del cliente de la consulta"""
        patterns = [
            r'cliente\s+(?:llamado\s+)?([A-Za-záéíóúñ\s]+)',
            r'(?:información|datos).*?de\s+([A-Za-záéíóúñ\s]+)',
            r'ver\s+([A-Za-záéíóúñ\s]+)',
            r'buscar\s+([A-Za-záéíóúñ\s]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                # Filtrar palabras comunes que no son nombres
                stop_words = ['cliente', 'información', 'datos', 'estado', 'problema']
                if name.lower() not in stop_words and len(name) > 2:
                    return name
        
        return None

    def _get_client_incidents(self, client_id: str, context: Dict[str, Any]) -> List[Dict]:
        """Obtiene incidentes específicos de un cliente"""
        user_context = context.get('user_context', {})
        all_incidents = user_context.get('incidentes_responsable', [])
        
        return [
            inc for inc in all_incidents 
            if inc.get('Cliente_ID') == client_id
        ]

    def _update_conversation_memory(
        self, 
        session_id: str, 
        query: str, 
        response: AgentResponse
    ):
        """Actualiza la memoria de conversación"""
        if session_id not in self.conversation_memory:
            self.conversation_memory[session_id] = []
        
        self.conversation_memory[session_id].append({
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response_type': response.action_type,
            'confidence': response.confidence
        })
        
        # Mantener solo las últimas 10 interacciones
        if len(self.conversation_memory[session_id]) > 10:
            self.conversation_memory[session_id] = self.conversation_memory[session_id][-10:]

    async def get_business_insights(self, propietario: str) -> List[BusinessInsight]:
        """Genera insights automáticos del negocio"""
        context = await self.context.get_full_context(propietario)
        insights = []
        
        if 'error' in context:
            return insights
        
        business_context = context.get('business_context', {})
        user_context = context.get('user_context', {})
        
        # Insight de crecimiento
        churn_rate = business_context.get('churn_rate', 0)
        if churn_rate > 10:
            insights.append(BusinessInsight(
                type='warning',
                title='Tasa de Churn Elevada',
                description=f'La tasa de churn es del {churn_rate:.1f}%, por encima del objetivo del 5%',
                recommended_action='Implementar programa de retención de clientes',
                impact_level='high',
                data_source='estadisticas'
            ))
        
        # Insight de ingresos
        arpu = business_context.get('arpu', 0)
        if arpu < 25:
            insights.append(BusinessInsight(
                type='opportunity',
                title='Oportunidad de Upselling',
                description=f'ARPU actual de ${arpu:.2f} indica potencial para planes premium',
                recommended_action='Analizar upgrade de clientes a planes superiores',
                impact_level='medium',
                data_source='clientes'
            ))
        
        # Insight de incidentes
        kpis = user_context.get('kpis_personales', {})
        incidentes_pendientes = kpis.get('incidentes_pendientes', 0)
        if incidentes_pendientes > 10:
            insights.append(BusinessInsight(
                type='warning',
                title='Acumulación de Incidentes',
                description=f'Tienes {incidentes_pendientes} incidentes pendientes',
                recommended_action='Priorizar resolución y asignar recursos adicionales',
                impact_level='high',
                data_source='incidentes'
            ))
        
        return insights

# === FUNCIONES DE UTILIDAD ===

def format_currency(amount: float) -> str:
    """Formatea moneda para mostrar"""
    return f"${amount:,.2f}"

def calculate_days_ago(date_str: str) -> int:
    """Calcula días transcurridos desde una fecha"""
    try:
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return (datetime.now() - date_obj).days
    except:
        return 0

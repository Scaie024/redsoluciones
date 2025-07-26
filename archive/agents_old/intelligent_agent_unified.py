"""
🧠 AGENTE INTELIGENTE UNIFICADO - RED SOLUCIONES ISP
=================================================

Agente de IA empresarial con capacidades avanzadas:
- Procesamiento de lenguaje natural con Gemini
- Extracción automática de datos estructurados  
- Ejecución automática de operaciones CRUD
- Análisis inteligente de base de datos
- Memoria conversacional persistente
- Respuestas profesionales sin emojis

Autor: Sistema IA Red Soluciones
Versión: 3.0 Unificado
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
import hashlib

# === CONFIGURACIÓN GEMINI AI ===
try:
    import google.generativeai as genai
    
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and len(api_key) > 20:
        genai.configure(api_key=api_key)
        GEMINI_AVAILABLE = True
        logging.info("IA Empresarial: Sistema operacional")
    else:
        GEMINI_AVAILABLE = False
        logging.error("API Key de IA requerida para operación completa")
except ImportError:
    GEMINI_AVAILABLE = False
    logging.error("Módulo IA no disponible")
except Exception as e:
    GEMINI_AVAILABLE = False
    logging.error(f"Error configurando IA: {e}")

# === ENUMS Y DATACLASSES ===

class ActionType(Enum):
    """Tipos de acciones que puede ejecutar el agente"""
    CREATE_CLIENT = "create_client"
    CREATE_PROSPECT = "create_prospect" 
    CREATE_INCIDENT = "create_incident"
    SEARCH_CLIENT = "search_client"
    UPDATE_CLIENT = "update_client"
    DELETE_CLIENT = "delete_client"
    ANALYTICS_FINANCIAL = "analytics_financial"
    ANALYTICS_ZONES = "analytics_zones"
    ANALYTICS_CLIENTS = "analytics_clients"
    LIST_CLIENTS = "list_clients"
    LIST_PROSPECTS = "list_prospects"
    SYSTEM_STATUS = "system_status"
    HELP = "help"
    GENERAL_QUERY = "general_query"

@dataclass
class ExtractedData:
    """Datos extraídos de conversación natural"""
    action: ActionType
    confidence: float
    data: Dict[str, Any]
    requires_confirmation: bool = False
    missing_fields: Optional[List[str]] = None

    def __post_init__(self):
        if self.missing_fields is None:
            self.missing_fields = []

class IntelligentISPAgent:
    """
    Agente de IA empresarial unificado para Red Soluciones ISP
    
    Capacidades principales:
    - Comprensión de lenguaje natural empresarial
    - Extracción automática de datos estructurados
    - Ejecución automática de operaciones de base de datos
    - Análisis inteligente con IA generativa
    - Memoria conversacional persistente
    """
    
    def __init__(self, sheets_service=None):
        """Inicializar agente inteligente unificado"""
        self.sheets_service = sheets_service
        self.logger = logging.getLogger(__name__)
        
        # === CONFIGURACIÓN EMPRESARIAL ===
        self.role = "AGENTE_EMPRESARIAL_INTELIGENTE"
        self.company = "Red Soluciones ISP"
        self.version = "3.0 Unificado"
        
        # === CONFIGURACIÓN IA ===
        self.gemini_model = None
        if GEMINI_AVAILABLE:
            try:
                self.gemini_model = genai.GenerativeModel(
                    'gemini-1.5-flash',
                    system_instruction=self._get_system_instructions()
                )
                self.logger.info("IA Empresarial: Sistema operacional")
            except Exception as e:
                self.logger.error(f"Error configurando IA: {e}")
                GEMINI_AVAILABLE = False
        
        # === MEMORIA CONVERSACIONAL ===
        self.conversation_memory = {}
        
        # === MÉTRICAS EMPRESARIALES ===
        self.business_metrics = {
            "target_monthly_revenue": 200000,
            "standard_plan": 350,
            "premium_plan": 500,
            "enterprise_plan": 750,
            "target_clients": 500,
            "conversion_rate": 0.25
        }
        
        # === PATRONES DE EXTRACCIÓN ===
        self._setup_extraction_patterns()
        
        self.logger.info(f"Agente Inteligente Unificado v{self.version} inicializado")

    def _get_system_instructions(self) -> str:
        """Instrucciones del sistema para el modelo de IA"""
        return """Eres el AGENTE EMPRESARIAL INTELIGENTE de Red Soluciones ISP.

PERSONALIDAD Y ESTILO:
- Profesional, conciso y eficiente
- Lenguaje empresarial sin emojis
- Respuestas directas de máximo 3 líneas
- Enfoque en datos y resultados
- Tono ejecutivo y competente

CAPACIDADES PRINCIPALES:
- Análisis de conversaciones en lenguaje natural
- Extracción de datos estructurados
- Ejecución automática de operaciones
- Análisis inteligente de métricas de negocio
- Generación de insights empresariales

CONTEXTO EMPRESARIAL:
- Empresa: Red Soluciones ISP
- Servicios: Internet empresarial y residencial
- Zonas: Norte, Sur, Centro, Este, Oeste, Salamanca
- Planes: Básico (350), Estándar (500), Premium (750)

INSTRUCCIONES DE RESPUESTA:
- Siempre identifica la intención principal
- Extrae datos estructurados cuando sea posible
- Proporciona confirmación antes de ejecutar acciones
- Incluye análisis de datos cuando sea relevante
- Mantén contexto de conversaciones anteriores

FORMATO DE RESPUESTA:
- Texto principal: información clave
- Acción propuesta: operación a ejecutar
- Datos extraídos: información estructurada
- Confianza: nivel de certeza (0-1)"""

    def _setup_extraction_patterns(self):
        """Configurar patrones para extracción de datos"""
        
        # Patrones para extraer nombres
        self.name_patterns = [
            r'cliente:?\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]+)',
            r'prospecto:?\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]+)',
            r'nombre:?\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]+)',
            r'registrar\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]+)',
            r'agregar\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]+)',
            r'alta\s+de\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]+)'
        ]
        
        # Patrones para extraer teléfonos
        self.phone_patterns = [
            r'(?:tel|teléfono|celular|móvil)?:?\s*(\d{10})',
            r'(?:tel|teléfono|celular|móvil)?:?\s*(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})',
            r'(\d{3}\s?\d{3}\s?\d{4})',
            r'(\d{10})'
        ]
        
        # Patrones para extraer zonas
        self.zone_patterns = [
            r'zona:?\s*(norte|sur|centro|este|oeste|salamanca)',
            r'sector:?\s*(norte|sur|centro|este|oeste|salamanca)',
            r'área:?\s*(norte|sur|centro|este|oeste|salamanca)',
            r'ubicación:?\s*(norte|sur|centro|este|oeste|salamanca)',
            r'\b(norte|sur|centro|este|oeste|salamanca)\b'
        ]
        
        # Patrones para extraer planes
        self.plan_patterns = [
            r'plan:?\s*(básico|estándar|premium|empresarial)',
            r'paquete:?\s*(básico|estándar|premium|empresarial)',
            r'servicio:?\s*(básico|estándar|premium|empresarial)',
            r'\b(básico|estándar|premium|empresarial)\b'
        ]

    async def process_query(self, query: str, user_id: str = "default") -> Dict[str, Any]:
        """
        Procesador principal de consultas con IA avanzada
        
        Args:
            query: Consulta en lenguaje natural
            user_id: ID del usuario para memoria conversacional
            
        Returns:
            Respuesta estructurada con datos y acciones
        """
        try:
            # Limpiar y normalizar consulta
            query_clean = self._normalize_query(query)
            
            # Obtener contexto conversacional
            context = self._get_conversation_context(user_id)
            
            # Análisis con IA para extraer intención y datos
            extraction_result = await self._extract_with_ai(query_clean, context)
            
            # Ejecutar acción según la extracción
            response = await self._execute_action(extraction_result, context)
            
            # Actualizar memoria conversacional
            self._update_conversation_memory(user_id, query, response)
            
            return response
                
        except Exception as e:
            self.logger.error(f"Error en procesamiento: {e}")
            return {
                "response": "Error interno del sistema. Por favor, intente nuevamente.",
                "type": "error",
                "action": None,
                "confidence": 0.0,
                "data": {}
            }

    def _normalize_query(self, query: str) -> str:
        """Normalizar consulta de entrada"""
        # Convertir a minúsculas y limpiar
        query = query.lower().strip()
        
        # Remover caracteres especiales excepto los necesarios
        query = re.sub(r'[^\w\s:,.-]', '', query)
        
        # Normalizar espacios múltiples
        query = re.sub(r'\s+', ' ', query)
        
        return query

    def _get_conversation_context(self, user_id: str) -> Dict[str, Any]:
        """Obtener contexto conversacional del usuario"""
        if user_id not in self.conversation_memory:
            self.conversation_memory[user_id] = {
                "history": [],
                "pending_action": None,
                "last_extraction": None,
                "created_at": datetime.now()
            }
        
        return self.conversation_memory[user_id]

    async def _extract_with_ai(self, query: str, context: Dict) -> ExtractedData:
        """Extraer datos e intención usando IA"""
        
        if not self.gemini_model:
            # Fallback a extracción por patrones
            return self._extract_with_patterns(query)
        
        try:
            # Crear prompt para extracción
            prompt = self._build_extraction_prompt(query, context)
            
            # Generar respuesta con IA
            response = self.gemini_model.generate_content(prompt)
            ai_response = response.text.strip()
            
            # Parsear respuesta de IA
            return self._parse_ai_extraction(ai_response, query)
            
        except Exception as e:
            self.logger.error(f"Error en extracción IA: {e}")
            return self._extract_with_patterns(query)

    def _build_extraction_prompt(self, query: str, context: Dict) -> str:
        """Construir prompt para extracción de datos"""
        
        recent_history = "\n".join([
            f"- {h.get('query', '')}" for h in context.get('history', [])[-3:]
        ])
        
        return f"""Analiza esta consulta empresarial y extrae datos estructurados:

CONSULTA: "{query}"

HISTORIAL RECIENTE:
{recent_history}

INSTRUCCIONES:
1. Identifica la ACCIÓN principal (crear_cliente, crear_prospecto, buscar_cliente, crear_incidente, análisis_financiero, listar_clientes, ayuda, consulta_general)
2. Extrae DATOS estructurados (nombre, teléfono, zona, plan, descripción, etc.)
3. Calcula CONFIANZA (0.0-1.0) basada en claridad de datos
4. Identifica campos FALTANTES si los hay

RESPONDE EN FORMATO JSON:
{{
    "action": "acción_identificada",
    "confidence": 0.85,
    "data": {{
        "nombre": "extraído_si_existe",
        "telefono": "extraído_si_existe", 
        "zona": "extraído_si_existe",
        "plan": "extraído_si_existe",
        "descripcion": "para_incidentes",
        "termino_busqueda": "para_búsquedas"
    }},
    "missing_fields": ["campos_que_faltan"],
    "requires_confirmation": true_o_false
}}

IMPORTANTE: Solo incluye campos que realmente existen en la consulta."""

    def _parse_ai_extraction(self, ai_response: str, original_query: str) -> ExtractedData:
        """Parsear respuesta de IA en estructura ExtractedData"""
        try:
            # Intentar parsear JSON de la respuesta
            response_json = json.loads(ai_response)
            
            # Mapear acción a enum
            action_mapping = {
                "crear_cliente": ActionType.CREATE_CLIENT,
                "crear_prospecto": ActionType.CREATE_PROSPECT,
                "crear_incidente": ActionType.CREATE_INCIDENT,
                "buscar_cliente": ActionType.SEARCH_CLIENT,
                "actualizar_cliente": ActionType.UPDATE_CLIENT,
                "eliminar_cliente": ActionType.DELETE_CLIENT,
                "análisis_financiero": ActionType.ANALYTICS_FINANCIAL,
                "análisis_zonas": ActionType.ANALYTICS_ZONES,
                "análisis_clientes": ActionType.ANALYTICS_CLIENTS,
                "listar_clientes": ActionType.LIST_CLIENTS,
                "listar_prospectos": ActionType.LIST_PROSPECTS,
                "estado_sistema": ActionType.SYSTEM_STATUS,
                "ayuda": ActionType.HELP,
                "consulta_general": ActionType.GENERAL_QUERY
            }
            
            action = action_mapping.get(
                response_json.get("action", "consulta_general"), 
                ActionType.GENERAL_QUERY
            )
            
            return ExtractedData(
                action=action,
                confidence=float(response_json.get("confidence", 0.5)),
                data=response_json.get("data", {}),
                requires_confirmation=response_json.get("requires_confirmation", False),
                missing_fields=response_json.get("missing_fields", [])
            )
            
        except Exception as e:
            self.logger.error(f"Error parseando respuesta IA: {e}")
            return self._extract_with_patterns(original_query)

    def _extract_with_patterns(self, query: str) -> ExtractedData:
        """Extracción de datos usando patrones de regex (fallback)"""
        
        # Detectar acción por palabras clave
        action = ActionType.GENERAL_QUERY
        confidence = 0.6
        data = {}
        
        if any(word in query for word in ["cliente:", "registrar cliente", "agregar cliente", "nuevo cliente", "alta cliente"]):
            action = ActionType.CREATE_CLIENT
            confidence = 0.8
            
        elif any(word in query for word in ["prospecto:", "registrar prospecto", "agregar prospecto", "nuevo prospecto"]):
            action = ActionType.CREATE_PROSPECT
            confidence = 0.8
            
        elif any(word in query for word in ["incidente:", "problema", "falla", "reportar", "incidencia"]):
            action = ActionType.CREATE_INCIDENT
            confidence = 0.7
            
        elif any(word in query for word in ["buscar", "encontrar", "localizar", "buscar cliente"]):
            action = ActionType.SEARCH_CLIENT
            confidence = 0.8
            
        elif any(word in query for word in ["estadísticas", "métricas", "números", "dashboard", "resumen"]):
            action = ActionType.ANALYTICS_CLIENTS
            confidence = 0.8
            
        elif any(word in query for word in ["análisis financiero", "finanzas", "ingresos", "revenue"]):
            action = ActionType.ANALYTICS_FINANCIAL
            confidence = 0.8
            
        elif any(word in query for word in ["listar clientes", "todos los clientes", "mostrar clientes"]):
            action = ActionType.LIST_CLIENTS
            confidence = 0.8
            
        elif any(word in query for word in ["ayuda", "help", "comandos", "manual"]):
            action = ActionType.HELP
            confidence = 0.9
        
        # Extraer datos usando patrones
        data = self._extract_data_patterns(query)
        
        # Determinar campos faltantes
        missing_fields = []
        if action in [ActionType.CREATE_CLIENT, ActionType.CREATE_PROSPECT]:
            if not data.get("nombre"):
                missing_fields.append("nombre")
            if not data.get("telefono"):
                missing_fields.append("telefono")
            if not data.get("zona"):
                missing_fields.append("zona")
        
        return ExtractedData(
            action=action,
            confidence=confidence,
            data=data,
            requires_confirmation=(len(missing_fields) == 0 and action in [ActionType.CREATE_CLIENT, ActionType.CREATE_PROSPECT]),
            missing_fields=missing_fields
        )

    def _extract_data_patterns(self, query: str) -> Dict[str, str]:
        """Extraer datos específicos usando patrones regex"""
        data = {}
        
        # Extraer nombre
        for pattern in self.name_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                data["nombre"] = match.group(1).strip().title()
                break
        
        # Extraer teléfono
        for pattern in self.phone_patterns:
            match = re.search(pattern, query)
            if match:
                phone = re.sub(r'[^\d]', '', match.group(1))
                if len(phone) == 10:
                    data["telefono"] = phone
                break
        
        # Extraer zona
        for pattern in self.zone_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                data["zona"] = match.group(1).lower().title()
                break
        
        # Extraer plan
        for pattern in self.plan_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                data["plan"] = match.group(1).lower()
                break
        
        # Extraer término de búsqueda
        search_patterns = [
            r'buscar\s+(.+)',
            r'encontrar\s+(.+)',
            r'localizar\s+(.+)'
        ]
        
        for pattern in search_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                data["termino_busqueda"] = match.group(1).strip()
                break
        
        return data

    async def _execute_action(self, extraction: ExtractedData, context: Dict) -> Dict[str, Any]:
        """Ejecutar acción basada en datos extraídos"""
        
        try:
            if extraction.action == ActionType.CREATE_CLIENT:
                return await self._handle_create_client(extraction)
                
            elif extraction.action == ActionType.CREATE_PROSPECT:
                return await self._handle_create_prospect(extraction)
                
            elif extraction.action == ActionType.CREATE_INCIDENT:
                return await self._handle_create_incident(extraction)
                
            elif extraction.action == ActionType.SEARCH_CLIENT:
                return await self._handle_search_client(extraction)
                
            elif extraction.action == ActionType.LIST_CLIENTS:
                return await self._handle_list_clients(extraction)
                
            elif extraction.action == ActionType.ANALYTICS_FINANCIAL:
                return await self._handle_financial_analytics(extraction)
                
            elif extraction.action == ActionType.ANALYTICS_CLIENTS:
                return await self._handle_client_analytics(extraction)
                
            elif extraction.action == ActionType.HELP:
                return await self._handle_help(extraction)
                
            else:
                return await self._handle_general_query(extraction)
                
        except Exception as e:
            self.logger.error(f"Error ejecutando acción {extraction.action}: {e}")
            return {
                "response": "Error ejecutando la operación solicitada.",
                "type": "error",
                "action": extraction.action.value,
                "confidence": 0.0,
                "data": {}
            }

    async def _handle_create_client(self, extraction: ExtractedData) -> Dict[str, Any]:
        """Manejar creación de cliente"""
        
        # Verificar datos requeridos
        if extraction.missing_fields:
            missing_text = ", ".join(extraction.missing_fields)
            return {
                "response": f"Para registrar el cliente necesito: {missing_text}. Por favor proporcione esta información.",
                "type": "missing_data",
                "action": "create_client",
                "confidence": extraction.confidence,
                "data": extraction.data,
                "missing_fields": extraction.missing_fields
            }
        
        # Ejecutar creación si tenemos los datos
        if self.sheets_service and all(k in extraction.data for k in ["nombre", "telefono", "zona"]):
            try:
                # Determinar plan si no se especificó
                plan = extraction.data.get("plan", "estándar")
                price = self.business_metrics.get(f"{plan}_plan", 350)
                
                # Usar método inteligente del servicio de sheets
                result = self.sheets_service.add_client_intelligent(
                    name=extraction.data["nombre"],
                    phone=extraction.data["telefono"],
                    zone=extraction.data["zona"],
                    client_type="cliente"
                )
                
                if result.get("success"):
                    client_id = result.get("client_id", "N/A")
                    suggested_plan = result.get("suggested_plan", plan)
                    
                    return {
                        "response": f"Cliente {extraction.data['nombre']} registrado exitosamente con ID {client_id}. Plan sugerido: {suggested_plan}. Precio mensual: ${price}.",
                        "type": "success",
                        "action": "create_client", 
                        "confidence": extraction.confidence,
                        "data": {
                            **extraction.data,
                            "client_id": client_id,
                            "plan": suggested_plan,
                            "price": price,
                            "status": "Activo"
                        }
                    }
                else:
                    return {
                        "response": f"Error registrando cliente: {result.get('error', 'Error desconocido')}",
                        "type": "error",
                        "action": "create_client",
                        "confidence": extraction.confidence,
                        "data": extraction.data
                    }
                    
            except Exception as e:
                self.logger.error(f"Error creando cliente: {e}")
                return {
                    "response": "Error interno registrando cliente. Verifique la conexión con la base de datos.",
                    "type": "error",
                    "action": "create_client",
                    "confidence": extraction.confidence,
                    "data": extraction.data
                }
        
        # Si no hay servicio de sheets o faltan datos críticos
        return {
            "response": "Confirme los datos del cliente: ¿nombre, teléfono y zona son correctos?",
            "type": "confirmation_needed",
            "action": "create_client",
            "confidence": extraction.confidence,
            "data": extraction.data
        }

    async def _handle_create_prospect(self, extraction: ExtractedData) -> Dict[str, Any]:
        """Manejar creación de prospecto"""
        
        # Verificar datos requeridos
        if extraction.missing_fields:
            missing_text = ", ".join(extraction.missing_fields)
            return {
                "response": f"Para registrar el prospecto necesito: {missing_text}. Por favor proporcione esta información.",
                "type": "missing_data",
                "action": "create_prospect",
                "confidence": extraction.confidence,
                "data": extraction.data,
                "missing_fields": extraction.missing_fields
            }
        
        # Ejecutar creación si tenemos los datos
        if self.sheets_service and all(k in extraction.data for k in ["nombre", "telefono", "zona"]):
            try:
                result = self.sheets_service.add_client_intelligent(
                    name=extraction.data["nombre"],
                    phone=extraction.data["telefono"],
                    zone=extraction.data["zona"],
                    client_type="prospecto"
                )
                
                if result.get("success"):
                    prospect_id = result.get("client_id", "N/A")
                    suggested_plan = result.get("suggested_plan", "estándar")
                    potential_revenue = result.get("monthly_revenue", 350)
                    
                    return {
                        "response": f"Prospecto {extraction.data['nombre']} registrado con ID {prospect_id}. Plan sugerido: {suggested_plan}. Potencial mensual: ${potential_revenue}.",
                        "type": "success",
                        "action": "create_prospect",
                        "confidence": extraction.confidence,
                        "data": {
                            **extraction.data,
                            "prospect_id": prospect_id,
                            "suggested_plan": suggested_plan,
                            "potential_revenue": potential_revenue,
                            "status": "Prospecto"
                        }
                    }
                else:
                    return {
                        "response": f"Error registrando prospecto: {result.get('error', 'Error desconocido')}",
                        "type": "error",
                        "action": "create_prospect",
                        "confidence": extraction.confidence,
                        "data": extraction.data
                    }
                    
            except Exception as e:
                self.logger.error(f"Error creando prospecto: {e}")
                return {
                    "response": "Error interno registrando prospecto. Verifique la conexión con la base de datos.",
                    "type": "error",
                    "action": "create_prospect",
                    "confidence": extraction.confidence,
                    "data": extraction.data
                }
        
        return {
            "response": "Confirme los datos del prospecto: ¿nombre, teléfono y zona son correctos?",
            "type": "confirmation_needed",
            "action": "create_prospect",
            "confidence": extraction.confidence,
            "data": extraction.data
        }

    async def _handle_search_client(self, extraction: ExtractedData) -> Dict[str, Any]:
        """Manejar búsqueda de cliente"""
        
        search_term = extraction.data.get("termino_busqueda", "").strip()
        if not search_term:
            # Buscar por nombre si está en los datos
            search_term = extraction.data.get("nombre", "")
        
        if not search_term:
            return {
                "response": "Especifique el nombre, teléfono o ID del cliente que desea buscar.",
                "type": "missing_data",
                "action": "search_client",
                "confidence": extraction.confidence,
                "data": extraction.data,
                "missing_fields": ["termino_busqueda"]
            }
        
        if self.sheets_service:
            try:
                # Usar búsqueda inteligente del servicio
                result = self.sheets_service.search_clients_intelligent(search_term)
                
                if result.get("success"):
                    clients = result.get("results", [])
                    total_found = result.get("total_found", 0)
                    
                    if total_found == 0:
                        return {
                            "response": f"No se encontraron clientes que coincidan con '{search_term}'.",
                            "type": "no_results",
                            "action": "search_client",
                            "confidence": extraction.confidence,
                            "data": {"search_term": search_term, "results": []}
                        }
                    
                    elif total_found == 1:
                        client = clients[0]
                        response_text = f"Cliente encontrado: {client.get('Nombre', 'N/A')} - Tel: {client.get('Teléfono', 'N/A')} - Zona: {client.get('Zona', 'N/A')} - Plan: {client.get('Plan', 'N/A')} - Estado: {client.get('Estado', 'N/A')}"
                        
                        return {
                            "response": response_text,
                            "type": "single_result",
                            "action": "search_client",
                            "confidence": extraction.confidence,
                            "data": {"search_term": search_term, "client": client, "results": clients}
                        }
                    
                    else:
                        # Múltiples resultados - mostrar los primeros 3
                        results_text = f"Encontrados {total_found} clientes. Primeros resultados:\n"
                        for i, client in enumerate(clients[:3]):
                            results_text += f"{i+1}. {client.get('Nombre', 'N/A')} - {client.get('Teléfono', 'N/A')} - {client.get('Zona', 'N/A')}\n"
                        
                        return {
                            "response": results_text.strip(),
                            "type": "multiple_results",
                            "action": "search_client",
                            "confidence": extraction.confidence,
                            "data": {"search_term": search_term, "results": clients, "total": total_found}
                        }
                
                else:
                    return {
                        "response": f"Error en búsqueda: {result.get('error', 'Error desconocido')}",
                        "type": "error",
                        "action": "search_client",
                        "confidence": extraction.confidence,
                        "data": {"search_term": search_term}
                    }
                    
            except Exception as e:
                self.logger.error(f"Error en búsqueda: {e}")
                return {
                    "response": "Error interno en búsqueda. Verifique la conexión con la base de datos.",
                    "type": "error",
                    "action": "search_client",
                    "confidence": extraction.confidence,
                    "data": {"search_term": search_term}
                }
        
        return {
            "response": "Servicio de base de datos no disponible temporalmente.",
            "type": "service_unavailable",
            "action": "search_client",
            "confidence": extraction.confidence,
            "data": {"search_term": search_term}
        }

    async def _handle_list_clients(self, extraction: ExtractedData) -> Dict[str, Any]:
        """Manejar listado de clientes"""
        
        if self.sheets_service:
            try:
                # Obtener clientes
                clients = self.sheets_service.get_all_clients()
                
                if clients:
                    total_clients = len(clients)
                    active_clients = len([c for c in clients if c.get('Estado', '').lower() == 'activo'])
                    inactive_clients = total_clients - active_clients
                    
                    # Calcular revenue total
                    total_revenue = sum([
                        float(c.get('Precio', 0)) for c in clients 
                        if c.get('Estado', '').lower() == 'activo'
                    ])
                    
                    response_text = f"Base de clientes: {total_clients} registros. Activos: {active_clients}, Inactivos: {inactive_clients}. Revenue mensual: ${total_revenue:,.0f}"
                    
                    # Agregar información por zonas
                    zones_summary = {}
                    for client in clients:
                        zone = client.get('Zona', 'Sin zona')
                        if zone not in zones_summary:
                            zones_summary[zone] = 0
                        zones_summary[zone] += 1
                    
                    if zones_summary:
                        zones_text = ", ".join([f"{zone}: {count}" for zone, count in zones_summary.items()])
                        response_text += f". Por zonas: {zones_text}"
                    
                    return {
                        "response": response_text,
                        "type": "success",
                        "action": "list_clients",
                        "confidence": extraction.confidence,
                        "data": {
                            "total_clients": total_clients,
                            "active_clients": active_clients,
                            "inactive_clients": inactive_clients,
                            "total_revenue": total_revenue,
                            "zones_summary": zones_summary,
                            "clients": clients[:10]  # Primeros 10 para mostrar
                        }
                    }
                
                else:
                    return {
                        "response": "No hay clientes registrados en la base de datos.",
                        "type": "no_data",
                        "action": "list_clients",
                        "confidence": extraction.confidence,
                        "data": {"total_clients": 0}
                    }
                    
            except Exception as e:
                self.logger.error(f"Error listando clientes: {e}")
                return {
                    "response": "Error interno accediendo a la base de datos de clientes.",
                    "type": "error", 
                    "action": "list_clients",
                    "confidence": extraction.confidence,
                    "data": {}
                }
        
        return {
            "response": "Servicio de base de datos no disponible temporalmente.",
            "type": "service_unavailable",
            "action": "list_clients",
            "confidence": extraction.confidence,
            "data": {}
        }

    async def _handle_financial_analytics(self, extraction: ExtractedData) -> Dict[str, Any]:
        """Manejar análisis financiero"""
        
        if self.sheets_service:
            try:
                # Obtener datos financieros
                clients = self.sheets_service.get_all_clients()
                prospects = self.sheets_service.get_prospects()
                
                if clients:
                    # Métricas actuales
                    active_clients = [c for c in clients if c.get('Estado', '').lower() == 'activo']
                    current_revenue = sum([float(c.get('Precio', 0)) for c in active_clients])
                    avg_price = current_revenue / len(active_clients) if active_clients else 0
                    
                    # Métricas de crecimiento
                    total_prospects = len(prospects) if prospects else 0
                    potential_revenue = total_prospects * avg_price if avg_price > 0 else total_prospects * 350
                    
                    # Calcular porcentaje vs objetivo
                    target_revenue = self.business_metrics["target_monthly_revenue"]
                    target_percentage = (current_revenue / target_revenue) * 100 if target_revenue > 0 else 0
                    
                    # Generar análisis inteligente con IA si está disponible
                    ai_analysis = ""
                    if self.gemini_model:
                        try:
                            financial_prompt = f"""Analiza estos datos financieros de Red Soluciones ISP:

Revenue actual: ${current_revenue:,.0f}
Meta mensual: ${target_revenue:,.0f}
Cumplimiento: {target_percentage:.1f}%
Clientes activos: {len(active_clients)}
Prospectos: {total_prospects}
Precio promedio: ${avg_price:.0f}
Potencial adicional: ${potential_revenue:,.0f}

Proporciona un análisis ejecutivo de máximo 2 líneas con insights clave y recomendaciones."""
                            
                            ai_response = self.gemini_model.generate_content(financial_prompt)
                            ai_analysis = ai_response.text.strip()
                            
                        except Exception as e:
                            self.logger.error(f"Error en análisis IA: {e}")
                    
                    # Construir respuesta
                    response_text = f"Análisis financiero: Revenue actual ${current_revenue:,.0f} ({target_percentage:.1f}% de meta). {len(active_clients)} clientes activos, precio promedio ${avg_price:.0f}. Potencial de crecimiento: ${potential_revenue:,.0f} con {total_prospects} prospectos."
                    
                    if ai_analysis:
                        response_text += f" Análisis IA: {ai_analysis}"
                    
                    return {
                        "response": response_text,
                        "type": "success",
                        "action": "analytics_financial",
                        "confidence": extraction.confidence,
                        "data": {
                            "current_revenue": current_revenue,
                            "target_revenue": target_revenue,
                            "target_percentage": target_percentage,
                            "active_clients": len(active_clients),
                            "total_prospects": total_prospects,
                            "avg_price": avg_price,
                            "potential_revenue": potential_revenue,
                            "ai_analysis": ai_analysis
                        }
                    }
                
                else:
                    return {
                        "response": "No hay datos suficientes para realizar análisis financiero.",
                        "type": "no_data",
                        "action": "analytics_financial",
                        "confidence": extraction.confidence,
                        "data": {}
                    }
                    
            except Exception as e:
                self.logger.error(f"Error en análisis financiero: {e}")
                return {
                    "response": "Error interno en análisis financiero. Verifique conexión con base de datos.",
                    "type": "error",
                    "action": "analytics_financial",
                    "confidence": extraction.confidence,
                    "data": {}
                }
        
        return {
            "response": "Servicio de análisis no disponible temporalmente.",
            "type": "service_unavailable",
            "action": "analytics_financial",
            "confidence": extraction.confidence,
            "data": {}
        }

    async def _handle_client_analytics(self, extraction: ExtractedData) -> Dict[str, Any]:
        """Manejar análisis de clientes"""
        
        if self.sheets_service:
            try:
                clients = self.sheets_service.get_all_clients()
                prospects = self.sheets_service.get_prospects()
                
                if clients:
                    # Análisis por estado
                    active_clients = [c for c in clients if c.get('Estado', '').lower() == 'activo']
                    inactive_clients = [c for c in clients if c.get('Estado', '').lower() != 'activo']
                    
                    # Análisis por zona
                    zones = {}
                    for client in active_clients:
                        zone = client.get('Zona', 'Sin zona')
                        if zone not in zones:
                            zones[zone] = {"count": 0, "revenue": 0}
                        zones[zone]["count"] += 1
                        zones[zone]["revenue"] += float(client.get('Precio', 0))
                    
                    # Zona más rentable
                    best_zone = max(zones.items(), key=lambda x: x[1]["revenue"]) if zones else None
                    
                    # Análisis por plan
                    plans = {}
                    for client in active_clients:
                        plan = client.get('Plan', 'Sin plan')
                        plans[plan] = plans.get(plan, 0) + 1
                    
                    # Plan más popular
                    popular_plan = max(plans.items(), key=lambda x: x[1]) if plans else None
                    
                    # Construir respuesta
                    response_text = f"Análisis de clientes: {len(active_clients)} activos, {len(inactive_clients)} inactivos. {len(prospects)} prospectos pendientes."
                    
                    if best_zone:
                        response_text += f" Zona líder: {best_zone[0]} con {best_zone[1]['count']} clientes y ${best_zone[1]['revenue']:,.0f} revenue."
                    
                    if popular_plan:
                        response_text += f" Plan más popular: {popular_plan[0]} con {popular_plan[1]} clientes."
                    
                    return {
                        "response": response_text,
                        "type": "success",
                        "action": "analytics_clients",
                        "confidence": extraction.confidence,
                        "data": {
                            "total_clients": len(clients),
                            "active_clients": len(active_clients),
                            "inactive_clients": len(inactive_clients),
                            "total_prospects": len(prospects),
                            "zones_analysis": zones,
                            "plans_analysis": plans,
                            "best_zone": best_zone,
                            "popular_plan": popular_plan
                        }
                    }
                
                else:
                    return {
                        "response": "No hay datos de clientes para analizar.",
                        "type": "no_data",
                        "action": "analytics_clients",
                        "confidence": extraction.confidence,
                        "data": {}
                    }
                    
            except Exception as e:
                self.logger.error(f"Error en análisis de clientes: {e}")
                return {
                    "response": "Error interno en análisis de clientes.",
                    "type": "error",
                    "action": "analytics_clients",
                    "confidence": extraction.confidence,
                    "data": {}
                }
        
        return {
            "response": "Servicio de análisis no disponible temporalmente.",
            "type": "service_unavailable",
            "action": "analytics_clients",
            "confidence": extraction.confidence,
            "data": {}
        }

    async def _handle_create_incident(self, extraction: ExtractedData) -> Dict[str, Any]:
        """Manejar creación de incidente"""
        
        # Verificar si hay descripción del problema
        if "descripcion" not in extraction.data and "termino_busqueda" not in extraction.data:
            return {
                "response": "Para reportar un incidente necesito la descripción del problema.",
                "type": "missing_data",
                "action": "create_incident",
                "confidence": extraction.confidence,
                "data": extraction.data,
                "missing_fields": ["descripcion"]
            }
        
        description = extraction.data.get("descripcion") or extraction.data.get("termino_busqueda", "")
        
        # Generar análisis del incidente con IA si está disponible
        incident_analysis = {}
        if self.gemini_model:
            try:
                incident_prompt = f"""Analiza este incidente técnico de ISP:

DESCRIPCIÓN: "{description}"

Clasifica en formato JSON:
{{
    "categoria": "técnico|comercial|facturación|soporte",
    "prioridad": "alta|media|baja",
    "área_afectada": "infraestructura|cliente_individual|zona_completa|sistema",
    "tiempo_estimado": "minutos_estimados",
    "acción_inmediata": "primera_acción_recomendada"
}}"""

                ai_response = self.gemini_model.generate_content(incident_prompt)
                incident_analysis = json.loads(ai_response.text.strip())
                
            except Exception as e:
                self.logger.error(f"Error analizando incidente: {e}")
                # Análisis básico sin IA
                incident_analysis = {
                    "categoria": "técnico",
                    "prioridad": "media",
                    "área_afectada": "cliente_individual",
                    "tiempo_estimado": "30",
                    "acción_inmediata": "contactar_cliente"
                }
        
        # Generar ID de incidente
        incident_id = f"INC-{datetime.now().strftime('%Y%m%d')}-{hash(description) % 1000:03d}"
        
        # TODO: Aquí se podría guardar en una hoja de incidentes si existe
        
        response_text = f"Incidente {incident_id} registrado. Categoría: {incident_analysis.get('categoria', 'técnico')}. Prioridad: {incident_analysis.get('prioridad', 'media')}. Tiempo estimado: {incident_analysis.get('tiempo_estimado', '30')} minutos."
        
        if incident_analysis.get('acción_inmediata'):
            response_text += f" Acción recomendada: {incident_analysis.get('acción_inmediata')}"
        
        return {
            "response": response_text,
            "type": "success",
            "action": "create_incident",
            "confidence": extraction.confidence,
            "data": {
                "incident_id": incident_id,
                "description": description,
                "analysis": incident_analysis,
                "created_at": datetime.now().isoformat()
            }
        }

    async def _handle_help(self, extraction: ExtractedData) -> Dict[str, Any]:
        """Manejar solicitud de ayuda"""
        
        help_text = """Comandos disponibles:
• Registrar cliente: 'cliente: Juan Pérez, 5551234567, Centro'
• Registrar prospecto: 'prospecto: María García, 5559876543, Norte'  
• Buscar cliente: 'buscar Juan' o 'encontrar 5551234567'
• Listar clientes: 'mostrar todos los clientes'
• Análisis financiero: 'análisis financiero' o 'revenue'
• Estadísticas: 'estadísticas' o 'números del negocio'
• Reportar incidente: 'problema con internet en zona sur'"""
        
        return {
            "response": help_text,
            "type": "success",
            "action": "help",
            "confidence": 1.0,
            "data": {}
        }

    async def _handle_general_query(self, extraction: ExtractedData) -> Dict[str, Any]:
        """Manejar consulta general"""
        
        # Si tenemos IA, generar respuesta contextual
        if self.gemini_model:
            try:
                general_prompt = f"""Como agente empresarial de Red Soluciones ISP, responde esta consulta:

CONSULTA: "{extraction.data.get('termino_busqueda', '')}"

CONTEXTO: 
- Somos proveedor de internet empresarial
- Manejamos clientes, prospectos e incidentes
- Zonas de cobertura: Norte, Sur, Centro, Este, Oeste, Salamanca
- Planes: Básico ($350), Estándar ($500), Premium ($750)

Responde profesionalmente en máximo 2 líneas."""

                ai_response = self.gemini_model.generate_content(general_prompt)
                response_text = ai_response.text.strip()
                
                return {
                    "response": response_text,
                    "type": "success",
                    "action": "general_query",
                    "confidence": extraction.confidence,
                    "data": extraction.data
                }
                
            except Exception as e:
                self.logger.error(f"Error en consulta general: {e}")
        
        # Respuesta predeterminada
        return {
            "response": "Soy el agente empresarial de Red Soluciones ISP. Puedo ayudarle con gestión de clientes, análisis financiero y reportes. Escriba 'ayuda' para ver comandos disponibles.",
            "type": "success",
            "action": "general_query",
            "confidence": 0.7,
            "data": extraction.data
        }

    def _update_conversation_memory(self, user_id: str, query: str, response: Dict[str, Any]):
        """Actualizar memoria conversacional"""
        try:
            if user_id not in self.conversation_memory:
                self.conversation_memory[user_id] = {
                    "history": [],
                    "pending_action": None,
                    "last_extraction": None,
                    "created_at": datetime.now()
                }
            
            # Agregar al historial
            self.conversation_memory[user_id]["history"].append({
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "response": response["response"],
                "action": response.get("action"),
                "confidence": response.get("confidence", 0.0)
            })
            
            # Mantener solo los últimos 10 intercambios
            if len(self.conversation_memory[user_id]["history"]) > 10:
                self.conversation_memory[user_id]["history"] = self.conversation_memory[user_id]["history"][-10:]
            
            # Limpiar memoria antigua (más de 24 horas)
            cutoff_time = datetime.now() - timedelta(hours=24)
            for uid in list(self.conversation_memory.keys()):
                if self.conversation_memory[uid]["created_at"] < cutoff_time:
                    del self.conversation_memory[uid]
                    
        except Exception as e:
            self.logger.error(f"Error actualizando memoria: {e}")


# === FUNCIONES DE INICIALIZACIÓN ===

# Variable global para instancia única
_intelligent_agent_instance = None

def initialize_intelligent_agent(sheets_service=None):
    """Inicializar el agente inteligente unificado"""
    global _intelligent_agent_instance
    try:
        _intelligent_agent_instance = IntelligentISPAgent(sheets_service)
        logging.info("Agente Inteligente Unificado inicializado exitosamente")
        return True
    except Exception as e:
        logging.error(f"Error inicializando Agente Inteligente: {e}")
        return False

def get_intelligent_agent():
    """Obtener instancia del agente inteligente"""
    return _intelligent_agent_instance

# Función de compatibilidad con API existente
async def process_query_unified(query: str, user_id: str = "default") -> Dict[str, Any]:
    """Función de compatibilidad para procesar consultas"""
    if _intelligent_agent_instance:
        return await _intelligent_agent_instance.process_query(query, user_id)
    else:
        return {
            "response": "Agente inteligente no disponible",
            "type": "error",
            "action": None,
            "confidence": 0.0,
            "data": {}
        }

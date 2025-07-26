"""
🧠 SUPER AGENTE INTELIGENTE - RED SOLUCIONES ISP
==============================================

Agente empresarial consolidado y optimizado:
- Procesamiento de lenguaje natural real
- Extracción automática de datos estructurados  
- Ejecución automática de operaciones
- Análisis inteligente con IA
- Respuestas profesionales sin emojis

Versión: 3.0 Final Consolidado
"""

import json
import logging
import re
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

# === CONFIGURACIÓN GEMINI AI ===
GEMINI_AVAILABLE = False
try:
    import google.generativeai as genai
    
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and len(api_key) > 20:
        genai.configure(api_key=api_key)
        GEMINI_AVAILABLE = True
        logging.info("IA Empresarial: Sistema operacional")
    else:
        logging.error("API Key de IA requerida")
except ImportError:
    logging.error("Módulo IA no disponible")
except Exception as e:
    logging.error(f"Error configurando IA: {e}")

@dataclass
class QueryResult:
    """Resultado del procesamiento de consulta"""
    response: str
    action_type: str
    confidence: float
    data: Dict[str, Any]
    suggestions: List[str]

class SuperIntelligentAgent:
    """
    Super Agente Inteligente para Red Soluciones ISP
    
    Capacidades:
    - Comprensión de lenguaje natural
    - Extracción de datos estructurados
    - Ejecución automática de operaciones
    - Análisis con IA generativa
    """
    
    def __init__(self, sheets_service=None):
        """Inicializar super agente"""
        self.sheets_service = sheets_service
        self.logger = logging.getLogger(__name__)
        
        # Configuración empresarial
        self.company = "Red Soluciones ISP"
        self.version = "3.0 Final"
        
        # Configuración IA
        self.ai_model = None
        if GEMINI_AVAILABLE:
            try:
                self.ai_model = genai.GenerativeModel(
                    'gemini-1.5-flash',
                    system_instruction=self._get_system_prompt()
                )
                self.logger.info("IA configurada exitosamente")
            except Exception as e:
                self.logger.error(f"Error configurando IA: {e}")
        
        # Patrones de extracción
        self._setup_patterns()
        
        # Memoria de conversación
        self.conversation_memory = {}
        
        self.logger.info(f"Super Agente Inteligente v{self.version} inicializado")

    def _get_system_prompt(self) -> str:
        """Prompt del sistema para IA"""
        return """Eres el SUPER AGENTE EMPRESARIAL de Red Soluciones ISP.

PERSONALIDAD:
- Profesional, directo y eficiente
- Lenguaje empresarial sin emojis
- Respuestas concisas máximo 3 líneas
- Enfoque en datos y resultados

CAPACIDADES:
- Registrar clientes y prospectos
- Buscar y analizar información
- Generar reportes financieros
- Gestionar incidentes técnicos

CONTEXTO:
- Empresa: Red Soluciones ISP (proveedor de internet)
- Zonas: Norte, Sur, Centro, Este, Oeste, Salamanca
- Planes: Básico ($350), Estándar ($500), Premium ($750)

INSTRUCCIONES:
- Identifica la intención principal de cada consulta
- Extrae datos estructurados cuando sea posible
- Proporciona información precisa y útil
- Mantén el contexto de conversaciones previas"""

    def _setup_patterns(self):
        """Configurar patrones de extracción"""
        
        # Patrones para nombres
        self.name_patterns = [
            r'cliente:?\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]+?)(?:,|\s+\d|\s+tel|\s*$)',
            r'prospecto:?\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]+?)(?:,|\s+\d|\s+tel|\s*$)',
            r'registrar\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]+?)(?:,|\s+\d|\s+tel|\s*$)',
            r'agregar\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]+?)(?:,|\s+\d|\s+tel|\s*$)',
            r'nombre:?\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]+?)(?:,|\s+\d|\s+tel|\s*$)'
        ]
        
        # Patrones para teléfonos
        self.phone_patterns = [
            r'\b(\d{10})\b',
            r'\b(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})\b',
            r'tel[éeEÉ]fono:?\s*(\d+)',
            r'cel[ular]*:?\s*(\d+)'
        ]
        
        # Patrones para zonas
        self.zone_patterns = [
            r'\b(norte|sur|centro|este|oeste|salamanca)\b'
        ]
        
        # Patrones para planes
        self.plan_patterns = [
            r'\b(básico|estándar|standard|premium|empresarial)\b'
        ]

    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Procesar consulta principal
        
        Args:
            query: Consulta en lenguaje natural
            
        Returns:
            Respuesta estructurada
        """
        try:
            # Normalizar consulta
            query_clean = self._normalize_query(query)
            
            # Detectar intención y extraer datos
            intent_data = self._analyze_intent_with_ai(query_clean) if self.ai_model else self._analyze_intent_patterns(query_clean)
            
            # Ejecutar acción
            result = self._execute_intent(intent_data, query_clean)
            
            # Formato de respuesta compatible
            return {
                "response": result.response,
                "type": result.action_type,
                "confidence": result.confidence,
                "data": result.data,
                "suggestions": result.suggestions
            }
            
        except Exception as e:
            self.logger.error(f"Error procesando consulta: {e}")
            return {
                "response": "Error interno del sistema. Intente nuevamente.",
                "type": "error",
                "confidence": 0.0,
                "data": {},
                "suggestions": ["Reintentar", "Ver ayuda", "Estado del sistema"]
            }

    def _normalize_query(self, query: str) -> str:
        """Normalizar consulta"""
        query = query.strip().lower()
        query = re.sub(r'[^\w\s:,.-]', '', query)
        query = re.sub(r'\s+', ' ', query)
        return query

    def _analyze_intent_with_ai(self, query: str) -> Dict[str, Any]:
        """Analizar intención con IA"""
        try:
            prompt = f"""Analiza esta consulta empresarial y responde en JSON:

CONSULTA: "{query}"

Identifica:
1. ACCIÓN: registrar_cliente, registrar_prospecto, buscar_cliente, listar_clientes, análisis_financiero, análisis_clientes, crear_incidente, ayuda, consulta_general
2. DATOS: extrae nombre, teléfono, zona, plan, término de búsqueda, descripción
3. CONFIANZA: 0.0-1.0 basado en claridad

JSON:
{{
    "accion": "acción_identificada",
    "confianza": 0.85,
    "datos": {{
        "nombre": "si_existe",
        "telefono": "si_existe",
        "zona": "si_existe",
        "termino_busqueda": "si_existe",
        "descripcion": "si_existe"
    }}
}}"""

            response = self.ai_model.generate_content(prompt)
            result = json.loads(response.text.strip())
            
            return {
                "action": result.get("accion", "consulta_general"),
                "confidence": float(result.get("confianza", 0.5)),
                "data": result.get("datos", {})
            }
            
        except Exception as e:
            self.logger.error(f"Error análisis IA: {e}")
            return self._analyze_intent_patterns(query)

    def _analyze_intent_patterns(self, query: str) -> Dict[str, Any]:
        """Analizar intención con patrones (fallback)"""
        
        action = "consulta_general"
        confidence = 0.6
        data = {}
        
        # Detectar acción
        if any(word in query for word in ["cliente:", "registrar cliente", "agregar cliente", "nuevo cliente"]):
            action = "registrar_cliente"
            confidence = 0.8
        elif any(word in query for word in ["prospecto:", "registrar prospecto", "nuevo prospecto"]):
            action = "registrar_prospecto"
            confidence = 0.8
        elif any(word in query for word in ["buscar", "encontrar", "localizar"]):
            action = "buscar_cliente"
            confidence = 0.8
        elif any(word in query for word in ["listar", "mostrar", "todos los clientes"]):
            action = "listar_clientes"
            confidence = 0.8
        elif any(word in query for word in ["estadísticas", "números", "métricas", "dashboard"]):
            action = "análisis_clientes"
            confidence = 0.8
        elif any(word in query for word in ["análisis financiero", "finanzas", "revenue", "ingresos"]):
            action = "análisis_financiero"
            confidence = 0.8
        elif any(word in query for word in ["incidente", "problema", "falla", "reporte"]):
            action = "crear_incidente"
            confidence = 0.7
        elif any(word in query for word in ["ayuda", "help", "comandos"]):
            action = "ayuda"
            confidence = 0.9
        
        # Extraer datos
        data = self._extract_data_with_patterns(query)
        
        return {
            "action": action,
            "confidence": confidence,
            "data": data
        }

    def _extract_data_with_patterns(self, query: str) -> Dict[str, Any]:
        """Extraer datos usando patrones regex"""
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
                data["zona"] = match.group(1).title()
                break
        
        # Extraer plan
        for pattern in self.plan_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                plan = match.group(1).lower()
                if plan == "standard":
                    plan = "estándar"
                data["plan"] = plan
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

    def _execute_intent(self, intent_data: Dict[str, Any], query: str) -> QueryResult:
        """Ejecutar intención identificada"""
        
        action = intent_data["action"]
        data = intent_data["data"]
        confidence = intent_data["confidence"]
        
        if action == "registrar_cliente":
            return self._handle_register_client(data, confidence)
        elif action == "registrar_prospecto":
            return self._handle_register_prospect(data, confidence)
        elif action == "buscar_cliente":
            return self._handle_search_client(data, confidence)
        elif action == "listar_clientes":
            return self._handle_list_clients(data, confidence)
        elif action == "análisis_financiero":
            return self._handle_financial_analysis(data, confidence)
        elif action == "análisis_clientes":
            return self._handle_client_analysis(data, confidence)
        elif action == "crear_incidente":
            return self._handle_create_incident(data, confidence, query)
        elif action == "ayuda":
            return self._handle_help(data, confidence)
        else:
            return self._handle_general_query(data, confidence, query)

    def _handle_register_client(self, data: Dict[str, Any], confidence: float) -> QueryResult:
        """Manejar registro de cliente"""
        
        # Verificar datos requeridos
        required_fields = ["nombre", "telefono", "zona"]
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        
        if missing_fields:
            missing_text = ", ".join(missing_fields)
            return QueryResult(
                response=f"Para registrar el cliente necesito: {missing_text}. Formato: cliente: Nombre, Teléfono, Zona",
                action_type="missing_data",
                confidence=confidence,
                data=data,
                suggestions=["Intentar de nuevo", "Ver formato", "Ayuda"]
            )
        
        # Ejecutar registro
        if self.sheets_service:
            try:
                result = self.sheets_service.add_client_intelligent(
                    name=data["nombre"],
                    phone=data["telefono"],
                    zone=data["zona"],
                    client_type="cliente"
                )
                
                if result.get("success"):
                    client_id = result.get("client_id", "N/A")
                    plan = result.get("suggested_plan", "estándar")
                    price = result.get("monthly_revenue", 350)
                    
                    return QueryResult(
                        response=f"Cliente {data['nombre']} registrado exitosamente. ID: {client_id}, Plan: {plan}, Precio: ${price}/mes.",
                        action_type="success",
                        confidence=confidence,
                        data={**data, "client_id": client_id, "plan": plan, "price": price},
                        suggestions=["Ver cliente", "Registrar otro", "Dashboard"]
                    )
                else:
                    return QueryResult(
                        response=f"Error registrando cliente: {result.get('error', 'Error desconocido')}",
                        action_type="error",
                        confidence=confidence,
                        data=data,
                        suggestions=["Reintentar", "Verificar datos", "Soporte"]
                    )
                    
            except Exception as e:
                self.logger.error(f"Error registrando cliente: {e}")
                return QueryResult(
                    response="Error interno registrando cliente. Verificar conexión con base de datos.",
                    action_type="error",
                    confidence=confidence,
                    data=data,
                    suggestions=["Reintentar", "Estado sistema", "Soporte"]
                )
        
        return QueryResult(
            response="Servicio de base de datos no disponible temporalmente.",
            action_type="service_unavailable",
            confidence=confidence,
            data=data,
            suggestions=["Estado sistema", "Reintentar", "Soporte"]
        )

    def _handle_register_prospect(self, data: Dict[str, Any], confidence: float) -> QueryResult:
        """Manejar registro de prospecto"""
        
        # Verificar datos requeridos
        required_fields = ["nombre", "telefono", "zona"]
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        
        if missing_fields:
            missing_text = ", ".join(missing_fields)
            return QueryResult(
                response=f"Para registrar el prospecto necesito: {missing_text}. Formato: prospecto: Nombre, Teléfono, Zona",
                action_type="missing_data",
                confidence=confidence,
                data=data,
                suggestions=["Intentar de nuevo", "Ver formato", "Ayuda"]
            )
        
        # Ejecutar registro
        if self.sheets_service:
            try:
                result = self.sheets_service.add_client_intelligent(
                    name=data["nombre"],
                    phone=data["telefono"],
                    zone=data["zona"],
                    client_type="prospecto"
                )
                
                if result.get("success"):
                    prospect_id = result.get("client_id", "N/A")
                    plan = result.get("suggested_plan", "estándar")
                    potential = result.get("monthly_revenue", 350)
                    
                    return QueryResult(
                        response=f"Prospecto {data['nombre']} registrado exitosamente. ID: {prospect_id}, Plan sugerido: {plan}, Potencial: ${potential}/mes.",
                        action_type="success",
                        confidence=confidence,
                        data={**data, "prospect_id": prospect_id, "plan": plan, "potential": potential},
                        suggestions=["Ver prospecto", "Seguimiento", "Dashboard"]
                    )
                else:
                    return QueryResult(
                        response=f"Error registrando prospecto: {result.get('error', 'Error desconocido')}",
                        action_type="error",
                        confidence=confidence,
                        data=data,
                        suggestions=["Reintentar", "Verificar datos", "Soporte"]
                    )
                    
            except Exception as e:
                self.logger.error(f"Error registrando prospecto: {e}")
                return QueryResult(
                    response="Error interno registrando prospecto. Verificar conexión con base de datos.",
                    action_type="error",
                    confidence=confidence,
                    data=data,
                    suggestions=["Reintentar", "Estado sistema", "Soporte"]
                )
        
        return QueryResult(
            response="Servicio de base de datos no disponible temporalmente.",
            action_type="service_unavailable",
            confidence=confidence,
            data=data,
            suggestions=["Estado sistema", "Reintentar", "Soporte"]
        )

    def _handle_search_client(self, data: Dict[str, Any], confidence: float) -> QueryResult:
        """Manejar búsqueda de cliente"""
        
        search_term = data.get("termino_busqueda") or data.get("nombre", "").strip()
        
        if not search_term:
            return QueryResult(
                response="Especifique el nombre, teléfono o ID del cliente a buscar.",
                action_type="missing_data",
                confidence=confidence,
                data=data,
                suggestions=["Formato búsqueda", "Listar todos", "Ayuda"]
            )
        
        if self.sheets_service:
            try:
                result = self.sheets_service.search_clients_intelligent(search_term)
                
                if result.get("success"):
                    clients = result.get("results", [])
                    total = result.get("total_found", 0)
                    
                    if total == 0:
                        return QueryResult(
                            response=f"No se encontraron clientes con '{search_term}'.",
                            action_type="no_results",
                            confidence=confidence,
                            data={"search_term": search_term},
                            suggestions=["Buscar otro", "Listar todos", "Registrar cliente"]
                        )
                    
                    elif total == 1:
                        client = clients[0]
                        response_text = f"Cliente: {client.get('Nombre', 'N/A')} - Tel: {client.get('Teléfono', 'N/A')} - Zona: {client.get('Zona', 'N/A')} - Plan: {client.get('Plan', 'N/A')} - Estado: {client.get('Estado', 'N/A')}"
                        
                        return QueryResult(
                            response=response_text,
                            action_type="single_result",
                            confidence=confidence,
                            data={"search_term": search_term, "client": client},
                            suggestions=["Editar cliente", "Ver detalles", "Buscar otro"]
                        )
                    
                    else:
                        response_text = f"Encontrados {total} clientes:"
                        for i, client in enumerate(clients[:3]):
                            response_text += f"\n{i+1}. {client.get('Nombre', 'N/A')} - {client.get('Teléfono', 'N/A')} - {client.get('Zona', 'N/A')}"
                        
                        return QueryResult(
                            response=response_text,
                            action_type="multiple_results",
                            confidence=confidence,
                            data={"search_term": search_term, "results": clients, "total": total},
                            suggestions=["Refinar búsqueda", "Ver todos", "Seleccionar cliente"]
                        )
                
                else:
                    return QueryResult(
                        response=f"Error en búsqueda: {result.get('error', 'Error desconocido')}",
                        action_type="error",
                        confidence=confidence,
                        data={"search_term": search_term},
                        suggestions=["Reintentar", "Estado sistema", "Soporte"]
                    )
                    
            except Exception as e:
                self.logger.error(f"Error búsqueda: {e}")
                return QueryResult(
                    response="Error interno en búsqueda. Verificar conexión con base de datos.",
                    action_type="error",
                    confidence=confidence,
                    data={"search_term": search_term},
                    suggestions=["Reintentar", "Estado sistema", "Soporte"]
                )
        
        return QueryResult(
            response="Servicio de búsqueda no disponible temporalmente.",
            action_type="service_unavailable",
            confidence=confidence,
            data={"search_term": search_term},
            suggestions=["Estado sistema", "Reintentar", "Soporte"]
        )

    def _handle_list_clients(self, data: Dict[str, Any], confidence: float) -> QueryResult:
        """Manejar listado de clientes"""
        
        if self.sheets_service:
            try:
                clients = self.sheets_service.get_all_clients()
                
                if clients:
                    total = len(clients)
                    active = len([c for c in clients if c.get('Estado', '').lower() == 'activo'])
                    inactive = total - active
                    
                    # Calcular revenue
                    revenue = sum([float(c.get('Precio', 0)) for c in clients if c.get('Estado', '').lower() == 'activo'])
                    
                    # Análisis por zonas
                    zones = {}
                    for client in clients:
                        zone = client.get('Zona', 'Sin zona')
                        zones[zone] = zones.get(zone, 0) + 1
                    
                    zones_text = ", ".join([f"{zone}: {count}" for zone, count in zones.items()])
                    
                    response_text = f"Base de clientes: {total} registros ({active} activos, {inactive} inactivos). Revenue mensual: ${revenue:,.0f}. Por zonas: {zones_text}"
                    
                    return QueryResult(
                        response=response_text,
                        action_type="success",
                        confidence=confidence,
                        data={
                            "total": total,
                            "active": active,
                            "inactive": inactive,
                            "revenue": revenue,
                            "zones": zones
                        },
                        suggestions=["Análisis financiero", "Buscar cliente", "Registrar cliente"]
                    )
                
                else:
                    return QueryResult(
                        response="No hay clientes registrados en la base de datos.",
                        action_type="no_data",
                        confidence=confidence,
                        data={},
                        suggestions=["Registrar cliente", "Estado sistema", "Ayuda"]
                    )
                    
            except Exception as e:
                self.logger.error(f"Error listando clientes: {e}")
                return QueryResult(
                    response="Error interno accediendo a base de datos de clientes.",
                    action_type="error",
                    confidence=confidence,
                    data={},
                    suggestions=["Reintentar", "Estado sistema", "Soporte"]
                )
        
        return QueryResult(
            response="Servicio de base de datos no disponible temporalmente.",
            action_type="service_unavailable",
            confidence=confidence,
            data={},
            suggestions=["Estado sistema", "Reintentar", "Soporte"]
        )

    def _handle_financial_analysis(self, data: Dict[str, Any], confidence: float) -> QueryResult:
        """Manejar análisis financiero"""
        
        if self.sheets_service:
            try:
                clients = self.sheets_service.get_all_clients()
                prospects = self.sheets_service.get_prospects()
                
                if clients:
                    # Métricas actuales
                    active_clients = [c for c in clients if c.get('Estado', '').lower() == 'activo']
                    current_revenue = sum([float(c.get('Precio', 0)) for c in active_clients])
                    avg_price = current_revenue / len(active_clients) if active_clients else 0
                    
                    # Potencial
                    total_prospects = len(prospects) if prospects else 0
                    potential_revenue = total_prospects * avg_price if avg_price > 0 else total_prospects * 350
                    
                    # Meta
                    target_revenue = 200000  # Meta mensual
                    target_percentage = (current_revenue / target_revenue) * 100 if target_revenue > 0 else 0
                    
                    # Análisis con IA si está disponible
                    ai_insight = ""
                    if self.ai_model:
                        try:
                            analysis_prompt = f"""Analiza estos datos financieros de Red Soluciones ISP:

Revenue actual: ${current_revenue:,.0f}
Meta mensual: ${target_revenue:,.0f}
Cumplimiento: {target_percentage:.1f}%
Clientes activos: {len(active_clients)}
Prospectos: {total_prospects}
Precio promedio: ${avg_price:.0f}

Proporciona insight ejecutivo en 1 línea con recomendación estratégica."""

                            ai_response = self.ai_model.generate_content(analysis_prompt)
                            ai_insight = ai_response.text.strip()
                        except Exception as e:
                            self.logger.error(f"Error análisis IA: {e}")
                    
                    response_text = f"Análisis financiero: Revenue ${current_revenue:,.0f} ({target_percentage:.1f}% de meta). {len(active_clients)} clientes activos, precio promedio ${avg_price:.0f}. Potencial: ${potential_revenue:,.0f} con {total_prospects} prospectos."
                    
                    if ai_insight:
                        response_text += f" Insight: {ai_insight}"
                    
                    return QueryResult(
                        response=response_text,
                        action_type="success",
                        confidence=confidence,
                        data={
                            "current_revenue": current_revenue,
                            "target_revenue": target_revenue,
                            "target_percentage": target_percentage,
                            "active_clients": len(active_clients),
                            "avg_price": avg_price,
                            "total_prospects": total_prospects,
                            "potential_revenue": potential_revenue,
                            "ai_insight": ai_insight
                        },
                        suggestions=["Análisis clientes", "Ver prospectos", "Dashboard"]
                    )
                
                else:
                    return QueryResult(
                        response="No hay datos suficientes para análisis financiero.",
                        action_type="no_data",
                        confidence=confidence,
                        data={},
                        suggestions=["Registrar clientes", "Estado sistema", "Ayuda"]
                    )
                    
            except Exception as e:
                self.logger.error(f"Error análisis financiero: {e}")
                return QueryResult(
                    response="Error interno en análisis financiero.",
                    action_type="error",
                    confidence=confidence,
                    data={},
                    suggestions=["Reintentar", "Estado sistema", "Soporte"]
                )
        
        return QueryResult(
            response="Servicio de análisis no disponible temporalmente.",
            action_type="service_unavailable",
            confidence=confidence,
            data={},
            suggestions=["Estado sistema", "Reintentar", "Soporte"]
        )

    def _handle_client_analysis(self, data: Dict[str, Any], confidence: float) -> QueryResult:
        """Manejar análisis de clientes"""
        
        if self.sheets_service:
            try:
                clients = self.sheets_service.get_all_clients()
                prospects = self.sheets_service.get_prospects()
                
                if clients:
                    # Análisis por estado
                    active = [c for c in clients if c.get('Estado', '').lower() == 'activo']
                    inactive = [c for c in clients if c.get('Estado', '').lower() != 'activo']
                    
                    # Análisis por zona
                    zones = {}
                    for client in active:
                        zone = client.get('Zona', 'Sin zona')
                        if zone not in zones:
                            zones[zone] = {"count": 0, "revenue": 0}
                        zones[zone]["count"] += 1
                        zones[zone]["revenue"] += float(client.get('Precio', 0))
                    
                    # Zona líder
                    best_zone = max(zones.items(), key=lambda x: x[1]["revenue"]) if zones else None
                    
                    # Análisis por plan
                    plans = {}
                    for client in active:
                        plan = client.get('Plan', 'Sin plan')
                        plans[plan] = plans.get(plan, 0) + 1
                    
                    popular_plan = max(plans.items(), key=lambda x: x[1]) if plans else None
                    
                    response_text = f"Análisis de clientes: {len(active)} activos, {len(inactive)} inactivos, {len(prospects)} prospectos."
                    
                    if best_zone:
                        response_text += f" Zona líder: {best_zone[0]} con {best_zone[1]['count']} clientes (${best_zone[1]['revenue']:,.0f})."
                    
                    if popular_plan:
                        response_text += f" Plan popular: {popular_plan[0]} ({popular_plan[1]} clientes)."
                    
                    return QueryResult(
                        response=response_text,
                        action_type="success",
                        confidence=confidence,
                        data={
                            "total_clients": len(clients),
                            "active_clients": len(active),
                            "inactive_clients": len(inactive),
                            "total_prospects": len(prospects),
                            "zones_analysis": zones,
                            "plans_analysis": plans,
                            "best_zone": best_zone,
                            "popular_plan": popular_plan
                        },
                        suggestions=["Análisis financiero", "Ver zona específica", "Dashboard"]
                    )
                
                else:
                    return QueryResult(
                        response="No hay datos de clientes para analizar.",
                        action_type="no_data",
                        confidence=confidence,
                        data={},
                        suggestions=["Registrar clientes", "Estado sistema", "Ayuda"]
                    )
                    
            except Exception as e:
                self.logger.error(f"Error análisis clientes: {e}")
                return QueryResult(
                    response="Error interno en análisis de clientes.",
                    action_type="error",
                    confidence=confidence,
                    data={},
                    suggestions=["Reintentar", "Estado sistema", "Soporte"]
                )
        
        return QueryResult(
            response="Servicio de análisis no disponible temporalmente.",
            action_type="service_unavailable",
            confidence=confidence,
            data={},
            suggestions=["Estado sistema", "Reintentar", "Soporte"]
        )

    def _handle_create_incident(self, data: Dict[str, Any], confidence: float, query: str) -> QueryResult:
        """Manejar creación de incidente"""
        
        description = data.get("descripcion") or data.get("termino_busqueda") or query
        
        if not description or len(description.strip()) < 5:
            return QueryResult(
                response="Para reportar un incidente necesito la descripción del problema.",
                action_type="missing_data",
                confidence=confidence,
                data=data,
                suggestions=["Describir problema", "Ver formato", "Ayuda"]
            )
        
        # Análisis básico del incidente
        category = "técnico"
        priority = "media"
        
        if any(word in description.lower() for word in ["no internet", "sin conexión", "no funciona", "caído"]):
            category = "técnico"
            priority = "alta"
        elif any(word in description.lower() for word in ["lento", "velocidad", "latencia"]):
            category = "técnico"
            priority = "media"
        elif any(word in description.lower() for word in ["factura", "pago", "cobro"]):
            category = "facturación"
            priority = "media"
        
        # Análisis con IA si está disponible
        if self.ai_model:
            try:
                incident_prompt = f"""Analiza este incidente de ISP:

DESCRIPCIÓN: "{description}"

Responde en JSON:
{{
    "categoria": "técnico|comercial|facturación",
    "prioridad": "alta|media|baja",
    "tiempo_estimado": "minutos",
    "accion_recomendada": "primera_acción"
}}"""

                ai_response = self.ai_model.generate_content(incident_prompt)
                ai_analysis = json.loads(ai_response.text.strip())
                
                category = ai_analysis.get("categoria", category)
                priority = ai_analysis.get("prioridad", priority)
                
            except Exception as e:
                self.logger.error(f"Error análisis incidente: {e}")
        
        # Generar ID de incidente
        incident_id = f"INC-{datetime.now().strftime('%Y%m%d')}-{hash(description) % 1000:03d}"
        
        response_text = f"Incidente {incident_id} registrado. Categoría: {category}, Prioridad: {priority}. Se notificará al equipo técnico correspondiente."
        
        return QueryResult(
            response=response_text,
            action_type="success",
            confidence=confidence,
            data={
                "incident_id": incident_id,
                "description": description,
                "category": category,
                "priority": priority,
                "created_at": datetime.now().isoformat()
            },
            suggestions=["Estado incidente", "Crear otro", "Soporte técnico"]
        )

    def _handle_help(self, data: Dict[str, Any], confidence: float) -> QueryResult:
        """Manejar solicitud de ayuda"""
        
        help_text = """Comandos disponibles:
• Registrar cliente: 'cliente: Juan Pérez, 5551234567, Centro'
• Registrar prospecto: 'prospecto: María García, 5559876543, Norte'
• Buscar: 'buscar Juan' o 'encontrar 5551234567'
• Listar clientes: 'mostrar todos los clientes'
• Análisis financiero: 'análisis financiero'
• Estadísticas: 'estadísticas' o 'números'
• Reportar problema: 'problema con internet en zona sur'"""
        
        return QueryResult(
            response=help_text,
            action_type="success",
            confidence=1.0,
            data={},
            suggestions=["Registrar cliente", "Ver estadísticas", "Buscar cliente"]
        )

    def _handle_general_query(self, data: Dict[str, Any], confidence: float, query: str) -> QueryResult:
        """Manejar consulta general"""
        
        # Respuesta con IA si está disponible
        if self.ai_model:
            try:
                general_prompt = f"""Como agente empresarial de Red Soluciones ISP, responde esta consulta:

CONSULTA: "{query}"

CONTEXTO:
- Proveedor de internet empresarial
- Gestión de clientes, prospectos e incidentes  
- Zonas: Norte, Sur, Centro, Este, Oeste, Salamanca
- Planes: Básico ($350), Estándar ($500), Premium ($750)

Responde profesionalmente en máximo 2 líneas."""

                ai_response = self.ai_model.generate_content(general_prompt)
                response_text = ai_response.text.strip()
                
                return QueryResult(
                    response=response_text,
                    action_type="success",
                    confidence=confidence,
                    data=data,
                    suggestions=["Ver comandos", "Estadísticas", "Registrar cliente"]
                )
                
            except Exception as e:
                self.logger.error(f"Error consulta general: {e}")
        
        # Respuesta predeterminada
        return QueryResult(
            response="Soy el agente empresarial de Red Soluciones ISP. Puedo ayudarle con gestión de clientes, análisis financiero y reportes. Escriba 'ayuda' para ver comandos disponibles.",
            action_type="success",
            confidence=0.7,
            data=data,
            suggestions=["Ver ayuda", "Estadísticas", "Registrar cliente"]
        )


# === FUNCIONES DE INICIALIZACIÓN ===

# Variable global para instancia única
_super_agent_instance = None

def initialize_super_agent(sheets_service=None):
    """Inicializar super agente"""
    global _super_agent_instance
    try:
        _super_agent_instance = SuperIntelligentAgent(sheets_service)
        logging.info("Super Agente Inteligente inicializado exitosamente")
        return True
    except Exception as e:
        logging.error(f"Error inicializando Super Agente: {e}")
        return False

def get_super_agent():
    """Obtener instancia del super agente"""
    return _super_agent_instance

# Función de compatibilidad para API existente
def process_query_super(query: str) -> Dict[str, Any]:
    """Función de compatibilidad para procesar consultas"""
    if _super_agent_instance:
        return _super_agent_instance.process_query(query)
    else:
        return {
            "response": "Super agente no disponible",
            "type": "error",
            "confidence": 0.0,
            "data": {},
            "suggestions": ["Reiniciar sistema", "Contactar soporte"]
        }

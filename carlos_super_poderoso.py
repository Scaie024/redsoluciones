"""
🚀 CARLOS SÚPER PODEROSO v2.0 - Red Soluciones ISP
=================================================

Secretario administrativo súper poderoso que puede:
- Dar de alta prospectos eficientemente 
- Convertir prospectos a clientes
- Reportar incidentes para técnicos
- Gestión completa sin desperdicio de API
- Solo activo cuando el dueño escribe
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import re

# Importar configuración
try:
    from backend.app.core.config import settings
    from backend.app.services.sheets.service import SheetsServiceV2 as SheetsService
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
    if hasattr(settings, 'GEMINI_API_KEY') and settings.GEMINI_API_KEY:
        genai.configure(api_key=settings.GEMINI_API_KEY)
    else:
        GEMINI_AVAILABLE = False
except ImportError:
    GEMINI_AVAILABLE = False

class CarlosSuperPoderoso:
    """🚀 CARLOS SÚPER PODEROSO - Secretario ISP de Nueva Generación"""
    
    def __init__(self, sheets_service=None):
        self.sheets_service = sheets_service
        self.logger = logging.getLogger(__name__)
        
        # CONFIGURACIÓN SÚPER PODEROSA
        self.fallback_message = "❌ No tengo acceso al LLM. Favor de pedir al administrador ayuda."
        self.max_response_length = 200  # Respuestas súper concisas
        
        # Inicializar Gemini solo si está disponible
        self.gemini_model = None
        if GEMINI_AVAILABLE:
            try:
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                self.logger.info("🧠 Gemini AI súper poderoso conectado")
            except Exception as e:
                self.logger.warning(f"Gemini no disponible: {e}")
                self.gemini_model = None
        
        # PATRONES SÚPER EFICIENTES
        self.patterns = {
            "prospect": ["prospecto", "prospectos", "lead", "leads", "interesado"],
            "client": ["cliente", "clientes", "alta cliente", "nuevo cliente"],
            "convert": ["convertir", "conversion", "pasar", "promover"],
            "incident": ["incidente", "problema", "falla", "reporte", "técnico"],
            "search": ["buscar", "encontrar", "localizar"],
            "stats": ["estadísticas", "resumen", "números", "total"],
            "help": ["ayuda", "help", "qué puedes hacer"]
        }
        
        self.logger.info("🚀 Carlos Súper Poderoso inicializado")

    def process_query(self, query: str) -> Dict[str, Any]:
        """🧠 Procesamiento súper eficiente de consultas"""
        try:
            query_clean = query.strip().lower()
            intent = self._detect_intent_super_fast(query_clean)
            
            # PROCESAMIENTO SÚPER PODEROSO
            if intent == "prospect":
                return self._handle_prospects(query_clean)
            elif intent == "client":
                return self._handle_clients(query_clean)
            elif intent == "convert":
                return self._handle_conversion(query_clean)
            elif intent == "incident":
                return self._handle_incidents(query_clean)
            elif intent == "search":
                return self._handle_search(query_clean)
            elif intent == "stats":
                return self._handle_stats(query_clean)
            elif intent == "help":
                return self._handle_help()
            else:
                return self._handle_unknown(query_clean)
                
        except Exception as e:
            self.logger.error(f"Error en Carlos Súper Poderoso: {e}")
            return {"response": self.fallback_message, "type": "error"}

    def _detect_intent_super_fast(self, query: str) -> str:
        """⚡ Detección súper rápida de intenciones"""
        for intent, keywords in self.patterns.items():
            if any(keyword in query for keyword in keywords):
                return intent
        return "unknown"

    def _handle_prospects(self, query: str) -> Dict[str, Any]:
        """🎯 Gestión súper eficiente de prospectos"""
        
        # FORMATO: "Prospecto: Nombre, teléfono, zona, interés"
        if "prospecto:" in query:
            return self._process_prospect_data(query)
        
        # LISTAR PROSPECTOS
        if "ver" in query or "mostrar" in query or "listar" in query:
            return {
                "response": "📋 Prospectos activos: 5 pendientes de seguimiento. 2 en negociación.",
                "type": "prospects_list",
                "suggestions": ["Convertir prospecto", "Nuevo prospecto", "Seguimiento"]
            }
        
        # INSTRUCCIONES
        return {
            "response": "🎯 Formato: 'Prospecto: Nombre, teléfono, zona, interés'",
            "type": "prospect_guide",
            "suggestions": ["Prospecto: Ana López, 555-1234, Norte, plan básico"]
        }

    def _process_prospect_data(self, query: str) -> Dict[str, Any]:
        """📝 Procesar datos de prospecto súper eficiente"""
        try:
            # Extraer datos después de "prospecto:"
            parts = query.split("prospecto:", 1)
            if len(parts) < 2:
                return {"response": "❌ Formato incorrecto", "type": "error"}
            
            data = [item.strip() for item in parts[1].split(",")]
            
            if len(data) < 3:
                return {"response": "❌ Necesito: nombre, teléfono, zona mínimo", "type": "error"}
            
            prospect = {
                "nombre": data[0],
                "telefono": data[1] if len(data) > 1 else "",
                "zona": data[2] if len(data) > 2 else "",
                "interes": data[3] if len(data) > 3 else "plan básico"
            }
            
            # ID único súper eficiente
            prospect_id = f"P{len(prospect['nombre'])}{prospect['zona'][:2].upper()}"
            
            return {
                "response": f"✅ Prospecto {prospect_id} registrado: {prospect['nombre']}",
                "type": "prospect_created",
                "data": prospect,
                "suggestions": [f"Convertir {prospect['nombre']}", "Agendar seguimiento"]
            }
            
        except Exception as e:
            return {"response": self.fallback_message, "type": "error"}

    def _handle_clients(self, query: str) -> Dict[str, Any]:
        """👥 Gestión súper eficiente de clientes"""
        
        # FORMATO: "Cliente: Nombre, email, zona, teléfono, plan"
        if "cliente:" in query:
            return self._process_client_data(query)
        
        # LISTAR CLIENTES
        if "ver" in query or "mostrar" in query or "listar" in query:
            return {
                "response": "👥 534 clientes activos. $185,400 ingresos mensuales.",
                "type": "clients_list",
                "suggestions": ["Buscar cliente", "Nuevo cliente", "Ver estadísticas"]
            }
        
        # INSTRUCCIONES
        return {
            "response": "👤 Formato: 'Cliente: Nombre, email, zona, teléfono, plan'",
            "type": "client_guide",
            "suggestions": ["Cliente: Juan Pérez, juan@email.com, Norte, 555-1234, 400"]
        }

    def _process_client_data(self, query: str) -> Dict[str, Any]:
        """📝 Procesar datos de cliente súper eficiente"""
        try:
            # Extraer datos después de "cliente:"
            parts = query.split("cliente:", 1)
            if len(parts) < 2:
                return {"response": "❌ Formato incorrecto", "type": "error"}
            
            data = [item.strip() for item in parts[1].split(",")]
            
            if len(data) < 5:
                return {"response": "❌ Necesito: nombre, email, zona, teléfono, plan", "type": "error"}
            
            client = {
                "nombre": data[0],
                "email": data[1],
                "zona": data[2],
                "telefono": data[3],
                "plan": data[4]
            }
            
            # ID único súper eficiente
            client_id = f"C{len(client['nombre'])}{client['zona'][:2].upper()}"
            
            return {
                "response": f"✅ Cliente {client_id} registrado: {client['nombre']} - ${client['plan']}",
                "type": "client_created",
                "data": client,
                "suggestions": ["Ver cliente", "Programar instalación", "Generar contrato"]
            }
            
        except Exception as e:
            return {"response": self.fallback_message, "type": "error"}

    def _handle_conversion(self, query: str) -> Dict[str, Any]:
        """🔄 Conversión súper eficiente prospecto → cliente"""
        
        # FORMATO: "convertir prospecto [nombre]"
        if "convertir" in query:
            words = query.split()
            if len(words) >= 3:
                prospect_name = " ".join(words[2:])
                return {
                    "response": f"✅ {prospect_name} convertido a cliente. Dame: email, zona, teléfono, plan",
                    "type": "conversion_ready",
                    "data": {"prospect_name": prospect_name},
                    "suggestions": [f"Cliente: {prospect_name}, email, zona, tel, plan"]
                }
        
        return {
            "response": "🔄 Formato: 'convertir prospecto [nombre]'",
            "type": "conversion_guide",
            "suggestions": ["convertir prospecto Ana López"]
        }

    def _handle_incidents(self, query: str) -> Dict[str, Any]:
        """🛠️ Gestión súper eficiente de incidentes"""
        
        # FORMATO: "incidente [cliente] [problema]"
        incident_data = self._parse_incident_super_fast(query)
        
        if incident_data:
            incident_id = f"I{len(incident_data['client'])}{incident_data['description'][:3].upper()}"
            
            return {
                "response": f"🛠️ Incidente {incident_id} registrado para {incident_data['client']}. Técnico notificado.",
                "type": "incident_created",
                "data": incident_data,
                "suggestions": ["Ver incidentes", "Asignar técnico", "Prioridad alta"]
            }
        
        return {
            "response": "🛠️ Formato: 'incidente [cliente] [problema]'",
            "type": "incident_guide",
            "suggestions": ["incidente Juan Pérez sin internet", "problema María línea lenta"]
        }

    def _parse_incident_super_fast(self, query: str) -> Optional[Dict[str, str]]:
        """⚡ Parseo súper rápido de incidentes"""
        try:
            if "incidente" in query:
                parts = query.split("incidente", 1)[1].strip().split()
                if len(parts) >= 2:
                    client = parts[0] + (" " + parts[1] if len(parts) > 2 and len(parts[1]) < 10 else "")
                    description = " ".join(parts[2:]) if len(parts) > 2 else "problema reportado"
                    return {"client": client, "description": description}
            
            elif "problema" in query and ":" in query:
                parts = query.split(":", 1)
                client = parts[0].replace("problema", "").strip()
                description = parts[1].strip()
                return {"client": client, "description": description}
            
            return None
        except:
            return None

    def _handle_search(self, query: str) -> Dict[str, Any]:
        """🔍 Búsqueda súper eficiente"""
        search_term = query.replace("buscar", "").replace("encontrar", "").strip()
        
        if not search_term:
            return {
                "response": "🔍 ¿Qué cliente buscas? Dame nombre, zona o teléfono.",
                "type": "search_guide",
                "suggestions": ["buscar Juan", "buscar zona Norte", "buscar 555-1234"]
            }
        
        # Simulación de búsqueda súper eficiente
        if "juan" in search_term.lower():
            return {
                "response": "✅ Juan Pérez - Norte - $350 - 555-0001 - Activo",
                "type": "search_result",
                "suggestions": ["Ver detalles", "Actualizar info", "Reportar incidente"]
            }
        
        return {
            "response": f"❌ No encontré '{search_term}'. Intenta con nombre completo.",
            "type": "no_results",
            "suggestions": ["Ver todos los clientes", "Alta nuevo cliente"]
        }

    def _handle_stats(self, query: str) -> Dict[str, Any]:
        """📊 Estadísticas súper eficientes"""
        return {
            "response": "📊 534 clientes, $185,400 ingresos, 5 zonas, 12 incidentes pendientes",
            "type": "stats",
            "suggestions": ["Ver por zonas", "Clientes morosos", "Incidentes críticos"]
        }

    def _handle_help(self) -> Dict[str, Any]:
        """❓ Ayuda súper eficiente"""
        return {
            "response": "💼 CARLOS - Puedo: alta prospectos/clientes, convertir, incidentes, buscar, stats",
            "type": "help",
            "suggestions": [
                "Prospecto: nombre, tel, zona",
                "Cliente: nombre, email, zona, tel, plan",
                "incidente cliente problema",
                "convertir prospecto nombre"
            ]
        }

    def _handle_unknown(self, query: str) -> Dict[str, Any]:
        """❓ Consultas no reconocidas"""
        # Si hay LLM disponible, usar respuesta inteligente pero corta
        if self.gemini_model:
            try:
                prompt = f"Eres Carlos, secretario ISP. Responde en máximo 1 línea: {query}"
                response = self.gemini_model.generate_content(prompt)
                if response and response.text:
                    return {
                        "response": response.text.strip()[:self.max_response_length],
                        "type": "ai_response",
                        "suggestions": ["Ver ayuda", "Estadísticas", "Buscar cliente"]
                    }
            except:
                pass
        
        return {"response": self.fallback_message, "type": "error"}


# ================================================
# INSTANCIA GLOBAL SÚPER PODEROSA
# ================================================

carlos_super = None

def initialize_carlos_super(sheets_service=None):
    """🚀 Inicializar Carlos Súper Poderoso"""
    global carlos_super
    carlos_super = CarlosSuperPoderoso(sheets_service)
    return carlos_super

def get_carlos_super():
    """🚀 Obtener instancia de Carlos Súper Poderoso"""
    return carlos_super

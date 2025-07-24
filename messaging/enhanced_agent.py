"""
💬 SISTEMA DE ATENCIÓN AL CLIENTE - RED SOLUCIONES
================================================

Sistema de atención optimizado p    def _handle_service_info(self) -> Dict[str, Any]:
        """📋 Información interna de servicios"""
        return {
            "response": "Aquí tienes los planes actuales:\n\n" +
                       "📶 **20 Mbps** - $350/mes\n" +
                       "📶 **50 Mbps** - $450/mes\n" +
                       "📶 **100 Mbps** - $600/mes\n\n" +
                       "Todos incluyen instalación e incluye soporte.\n\n" +
                       "¿Necesitas actualizar algún precio o agregar un plan?",
            "type": "service_info",
            "compact": True,
            "quick_replies": ["Ver clientes", "Estadísticas", "Agregar cliente", "Más opciones"]
        }instantánea
Telegram y WhatsApp
"""

import json
import logging
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
from backend.app.services.smart_agent import SmartISPAgent

class MessagingISPAgent(SmartISPAgent):
    """💬 Sistema de Atención Red Soluciones"""
    
    def __init__(self, sheets_service=None):
        super().__init__(sheets_service)
        
        # Configuración para mensajería
        self.messaging_config = {
            "max_response_length": 600,  # Más breve
            "enable_emojis": True,
            "compact_mode": True,
            "human_style": True  # Parecer humano
        }
        
        # Patrones de conversación natural
        self.messaging_patterns = {
            "register": ["registrarme", "registrar", "darme de alta", "suscribirme", "contratar"],
            "greeting": ["hola", "buenos días", "buenas tardes", "hey", "saludos"],
            "service_info": ["servicios", "planes", "precios", "costos", "cuánto cuesta", "ofertas"],
            "support": ["ayuda", "soporte", "problema", "falla", "lento", "no funciona"],
            "contact": ["contacto", "teléfono", "dirección", "horarios", "ubicación"]
        }
        
        self.logger.info("� Sistema de atención inicializado")

    def process_messaging_query(self, query: str, user_info: Optional[Dict] = None) -> Dict[str, Any]:
        """📱 Procesar consulta optimizada para mensajería"""
        try:
            query_clean = query.strip().lower()
            
            # Si es nuevo usuario, dar bienvenida
            if user_info and user_info.get('is_new_user', False):
                return self._handle_welcome(user_info)
            
            # Detectar intención específica para mensajería
            intent = self._detect_messaging_intent(query_clean)
            
            if intent == "register":
                return self._handle_register_request(query_clean, user_info or {})
            elif intent == "greeting":
                return self._handle_greeting(user_info or {})
            elif intent == "service_info":
                return self._handle_service_info()
            elif intent == "support":
                return self._handle_support_request(query_clean, user_info or {})
            elif intent == "contact":
                return self._handle_contact_info()
            else:
                # Usar procesamiento base pero optimizado para móvil
                result = self.process_query(query)
                return self._optimize_for_messaging(result)
                
        except Exception as e:
            self.logger.error(f"Error en mensajería '{query}': {e}")
            return {
                "response": "❌ Disculpa, hubo un error técnico. Intenta de nuevo.",
                "type": "error",
                "compact": True
            }

    def _detect_messaging_intent(self, query: str) -> str:
        """🎯 Detectar intención específica para mensajería"""
        # Verificar patrones de mensajería primero
        for intent, keywords in self.messaging_patterns.items():
            if any(keyword in query for keyword in keywords):
                return intent
        
        # Si no es específico de mensajería, usar detección base
        return self._detect_intent(query)

    def _handle_welcome(self, user_info: Dict) -> Dict[str, Any]:
        """👋 Saludo para el dueño o personal"""
        name = user_info.get('first_name', 'Jefe')
        
        return {
            "response": f"Buenos días {name}.\n\n" +
                       "Estoy aquí para ayudarte con:\n" +
                       "• Revisar estadísticas\n" +
                       "• Buscar clientes\n" +
                       "• Registrar incidentes\n" +
                       "• Cualquier consulta del negocio\n\n" +
                       "¿Qué necesitas?",
            "type": "welcome",
            "compact": True,
            "quick_replies": ["Ver servicios", "Registrarme", "Soporte", "Contacto"]
        }

    def _handle_register_request(self, query: str, user_info: Dict) -> Dict[str, Any]:
        """📝 Manejar solicitud de registro"""
        name = user_info.get('first_name', 'Usuario')
        phone = user_info.get('phone', 'No proporcionado')
        
        return {
            "response": f"📝 **Registro de Cliente Nuevo**\n\n" +
                       f"👤 Nombre: {name}\n" +
                       f"📱 Teléfono: {phone}\n\n" +
                       "Para completar tu registro necesito:\n\n" +
                       "1️⃣ Tu zona/colonia\n" +
                       "2️⃣ Dirección completa\n" +
                       "3️⃣ Plan de interés (20/50/100 Mbps)\n\n" +
                       "Escribe: `Zona: [Tu zona], Plan: [Mbps deseado]`\n\n" +
                       "**Ejemplo:**\n" +
                       "`Zona: Centro, Plan: 50 Mbps`",
            "type": "registration",
            "compact": True,
            "next_step": "collect_zone_plan"
        }

    def _handle_greeting(self, user_info: Dict) -> Dict[str, Any]:
        """👋 Manejar saludos"""
        name = user_info.get('first_name', 'Usuario') if user_info else 'Usuario'
        
        return {
            "response": f"👋 ¡Hola {name}!\n\n" +
                       "Soy el asistente de Red Soluciones ISP\n\n" +
                       "¿En qué puedo ayudarte hoy?\n\n" +
                       "💡 Opciones populares:",
            "type": "greeting",
            "compact": True,
            "quick_replies": ["Ver estadísticas", "Buscar cliente", "Registrar incidente", "Información de contacto"]
        }

    def _handle_service_info(self) -> Dict[str, Any]:
        """📋 Información de servicios"""
        return {
            "response": "Tenemos estos planes:\n\n" +
                       "� **20 Mbps** - $350/mes\n" +
                       "📶 **50 Mbps** - $450/mes\n" +
                       "📶 **100 Mbps** - $600/mes\n\n" +
                       "✅ Instalación gratis\n" +
                       "✅ Soporte incluido\n" +
                       "✅ WiFi de alta velocidad\n\n" +
                       "¿Cuál te interesa?",
            "type": "service_info",
            "compact": True,
            "quick_replies": ["20 Mbps", "50 Mbps", "100 Mbps", "Más info"]
        }

    def _handle_support_request(self, query: str, user_info: Dict) -> Dict[str, Any]:
        """🛠️ Registro de incidentes internos"""
        return {
            "response": "Perfecto, voy a registrar el incidente.\n\n" +
                       "Dame los detalles:\n" +
                       "• ¿De qué cliente es?\n" +
                       "• ¿Cuál es el problema?\n" +
                       "• ¿Qué prioridad le damos?\n\n" +
                       "Con esa información lo registro en el sistema.",
            "type": "support",
            "compact": True,
            "next_step": "collect_incident_details"
        }

    def _handle_contact_info(self) -> Dict[str, Any]:
        """📞 Información de contacto"""
        return {
            "response": "📞 **Contacto Red Soluciones**\n\n" +
                       "🏢 **Oficina Central:**\n" +
                       "📍 Dirección: [Dirección principal]\n" +
                       "📱 WhatsApp: +52 [Número]\n" +
                       "☎️ Teléfono: [Teléfono fijo]\n\n" +
                       "🕒 **Horarios:**\n" +
                       "Lun-Vie: 8:00 AM - 6:00 PM\n" +
                       "Sábados: 9:00 AM - 2:00 PM\n\n" +
                       "🚨 **Emergencias 24/7:**\n" +
                       "Para fallas críticas de internet\n\n" +
                       "¿Necesitas algo más?",
            "type": "contact",
            "compact": True
        }

    def _optimize_for_messaging(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """📱 Optimizar respuesta para mensajería"""
        # Acortar respuesta si es muy larga
        response = result.get("response", "")
        
        if len(response) > self.messaging_config["max_response_length"]:
            # Truncar y añadir indicador
            response = response[:self.messaging_config["max_response_length"]] + "...\n\n📱 Respuesta completa en dashboard"
        
        # Añadir modo compacto
        result["response"] = response
        result["compact"] = True
        
        # Limitar sugerencias para móvil
        if "suggestions" in result:
            result["suggestions"] = result["suggestions"][:3]
        
        return result

    def parse_registration_data(self, message: str, user_info: Dict) -> Dict[str, Any]:
        """📝 Parsear datos de registro desde mensaje"""
        try:
            # Patrones para extraer información
            zona_match = re.search(r'zona:\s*([^,]+)', message.lower())
            plan_match = re.search(r'plan:\s*(\d+)', message.lower())
            
            zona = zona_match.group(1).strip().title() if zona_match else None
            plan_mbps = int(plan_match.group(1)) if plan_match else None
            
            # Determinar precio según plan
            precio = 350  # básico por defecto
            if plan_mbps:
                if plan_mbps >= 100:
                    precio = 600
                elif plan_mbps >= 50:
                    precio = 450
            
            return {
                "nombre": user_info.get('first_name', '') + ' ' + user_info.get('last_name', ''),
                "telefono": user_info.get('phone', ''),
                "zona": zona,
                "plan_mbps": plan_mbps,
                "precio": precio,
                "email": user_info.get('email', ''),
                "valido": zona is not None and plan_mbps is not None
            }
            
        except Exception as e:
            self.logger.error(f"Error parseando registro: {e}")
            return {"valido": False, "error": str(e)}

    def create_incident_from_message(self, message: str, user_info: Dict) -> Dict[str, Any]:
        """🚨 Crear incidente desde mensaje"""
        try:
            # Determinar prioridad basada en palabras clave
            alta_prioridad = any(word in message.lower() for word in [
                "sin internet", "no funciona", "urgente", "crítico", "completamente", "nada"
            ])
            
            return {
                "cliente": user_info.get('first_name', 'Usuario Telegram'),
                "telefono": user_info.get('phone', ''),
                "descripcion": message,
                "prioridad": "Alta" if alta_prioridad else "Media",
                "tipo": "Técnico",
                "origen": "Telegram/WhatsApp",
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            self.logger.error(f"Error creando incidente: {e}")
            return {"error": str(e)}

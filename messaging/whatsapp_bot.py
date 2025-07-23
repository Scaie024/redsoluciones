"""
📱 BOT DE WHATSAPP PARA RED SOLUCIONES ISP
==========================================

Bot inteligente usando WhatsApp Business API
"""

import asyncio
import logging
import json
from typing import Dict, Any, Optional
from datetime import datetime
import requests
from flask import Flask, request, jsonify

# Importar agente mejorado
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from backend.app.services.sheets.service import SheetsServiceV2 as GoogleSheetsService
    from messaging.enhanced_agent import MessagingISPAgent
    SERVICES_AVAILABLE = True
except ImportError:
    SERVICES_AVAILABLE = False
    logging.warning("Servicios no disponibles en este contexto")

class WhatsAppISPBot:
    """📱 Bot de WhatsApp para Red Soluciones ISP"""
    
    def __init__(self, phone_number_id: str, access_token: str, verify_token: str):
        self.phone_number_id = phone_number_id
        self.access_token = access_token
        self.verify_token = verify_token
        self.base_url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
        
        # Servicios
        if SERVICES_AVAILABLE:
            self.sheets_service = GoogleSheetsService()
            self.agent = MessagingISPAgent(self.sheets_service)
        
        self.user_sessions = {}
        
        # Flask app para webhooks
        self.app = Flask(__name__)
        self.setup_routes()
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Estados de conversación
        self.CONVERSATION_STATES = {
            "IDLE": "idle",
            "REGISTERING": "registering", 
            "SUPPORT": "support"
        }

    def setup_routes(self):
        """🛣️ Configurar rutas Flask"""
        
        @self.app.route('/webhook', methods=['GET'])
        def verify_webhook():
            """✅ Verificar webhook"""
            mode = request.args.get('hub.mode')
            token = request.args.get('hub.verify_token')
            challenge = request.args.get('hub.challenge')
            
            if mode == 'subscribe' and token == self.verify_token:
                self.logger.info("Webhook verificado exitosamente")
                return challenge
            else:
                return "Verificación fallida", 403

        @self.app.route('/webhook', methods=['POST'])
        def handle_webhook():
            """📨 Manejar mensajes entrantes"""
            try:
                body = request.get_json()
                
                if (body.get('object') == 'whatsapp_business_account' and 
                    body.get('entry') and 
                    body['entry'][0].get('changes')):
                    
                    changes = body['entry'][0]['changes'][0]
                    
                    if changes.get('field') == 'messages':
                        value = changes.get('value', {})
                        
                        if 'messages' in value:
                            for message in value['messages']:
                                self.process_message(message, value.get('contacts', []))
                
                return jsonify({"status": "success"}), 200
                
            except Exception as e:
                self.logger.error(f"Error procesando webhook: {e}")
                return jsonify({"error": str(e)}), 500

    def process_message(self, message: Dict, contacts: list):
        """💬 Procesar mensaje entrante"""
        try:
            phone_number = message['from']
            message_type = message['type']
            
            # Obtener información del contacto
            contact_info = {}
            for contact in contacts:
                if contact['wa_id'] == phone_number:
                    contact_info = {
                        'phone': phone_number,
                        'first_name': contact['profile']['name'],
                        'last_name': '',
                        'user_id': phone_number
                    }
                    break
            
            # Procesar según tipo de mensaje
            if message_type == 'text':
                text_body = message['text']['body']
                self.handle_text_message(phone_number, text_body, contact_info)
            elif message_type == 'interactive':
                self.handle_interactive_message(phone_number, message['interactive'], contact_info)
                
        except Exception as e:
            self.logger.error(f"Error procesando mensaje: {e}")

    def handle_text_message(self, phone_number: str, text: str, contact_info: Dict):
        """📝 Manejar mensaje de texto"""
        try:
            # Obtener o crear sesión
            if phone_number not in self.user_sessions:
                self.user_sessions[phone_number] = {
                    "state": self.CONVERSATION_STATES["IDLE"],
                    "user_info": contact_info,
                    "conversation_history": []
                }
            
            session = self.user_sessions[phone_number]
            
            # Procesar según estado
            if session["state"] == self.CONVERSATION_STATES["REGISTERING"]:
                self.handle_registration_flow(phone_number, text)
            elif session["state"] == self.CONVERSATION_STATES["SUPPORT"]:
                self.handle_support_flow(phone_number, text)
            else:
                self.handle_general_query(phone_number, text)
                
        except Exception as e:
            self.logger.error(f"Error manejando texto: {e}")
            self.send_message(phone_number, "❌ Error procesando mensaje. Intenta de nuevo.")

    def handle_general_query(self, phone_number: str, text: str):
        """💭 Manejar consulta general"""
        session = self.user_sessions[phone_number]
        
        if not SERVICES_AVAILABLE:
            self.send_message(phone_number, "⚠️ Servicios temporalmente no disponibles")
            return
        
        # Procesar con agente
        response = self.agent.process_messaging_query(text, session["user_info"])
        
        # Guardar en historial
        session["conversation_history"].append({
            "timestamp": datetime.now().isoformat(),
            "user_message": text,
            "bot_response": response["response"]
        })
        
        # Actualizar estado si es necesario
        if response.get("next_step") == "collect_zone_plan":
            session["state"] = self.CONVERSATION_STATES["REGISTERING"]
        elif response.get("next_step") == "collect_incident_details":
            session["state"] = self.CONVERSATION_STATES["SUPPORT"]
        
        # Enviar respuesta
        self.send_message(phone_number, response["response"])
        
        # Enviar botones si están disponibles
        if "quick_replies" in response:
            self.send_quick_replies(phone_number, "¿Qué te interesa?", response["quick_replies"])

    def handle_registration_flow(self, phone_number: str, text: str):
        """📝 Manejar flujo de registro"""
        session = self.user_sessions[phone_number]
        
        if not SERVICES_AVAILABLE:
            self.send_message(phone_number, "⚠️ Servicios temporalmente no disponibles")
            return
        
        # Parsear datos
        registration_data = self.agent.parse_registration_data(text, session["user_info"])
        
        if registration_data["valido"]:
            try:
                # Registrar cliente
                client_data = {
                    "nombre": registration_data["nombre"],
                    "email": registration_data.get("email", ""),
                    "zona": registration_data["zona"],
                    "telefono": registration_data["telefono"],
                    "pago_mensual": registration_data["precio"],
                    "origen": "WhatsApp Bot"
                }
                
                result = self.sheets_service.add_client(**client_data)
                
                if result.get("success"):
                    response_text = f"✅ *¡Registro Exitoso!*\n\n" \
                                  f"👤 Cliente: {registration_data['nombre']}\n" \
                                  f"📍 Zona: {registration_data['zona']}\n" \
                                  f"📦 Plan: {registration_data['plan_mbps']} Mbps\n" \
                                  f"💰 Precio: ${registration_data['precio']}/mes\n\n" \
                                  f"📞 *Próximos pasos:*\n" \
                                  f"Un técnico te contactará en 24hrs para programar la instalación.\n\n" \
                                  f"¡Bienvenido a Red Soluciones! 🎉"
                else:
                    response_text = "❌ Hubo un error al registrar. Intenta nuevamente."
                    
            except Exception as e:
                self.logger.error(f"Error registrando: {e}")
                response_text = "❌ Error técnico. Contacta soporte."
        else:
            response_text = "❌ *Datos incompletos*\n\n" \
                          "Formato correcto:\n" \
                          "`Zona: [Tu zona], Plan: [Mbps deseado]`\n\n" \
                          "*Ejemplo:*\n" \
                          "`Zona: Centro, Plan: 50 Mbps`"
        
        # Resetear estado
        session["state"] = self.CONVERSATION_STATES["IDLE"]
        self.send_message(phone_number, response_text)

    def handle_support_flow(self, phone_number: str, text: str):
        """🛠️ Manejar flujo de soporte"""
        session = self.user_sessions[phone_number]
        
        if not SERVICES_AVAILABLE:
            self.send_message(phone_number, "⚠️ Servicios temporalmente no disponibles")
            return
        
        # Crear incidente
        incident_data = self.agent.create_incident_from_message(text, session["user_info"])
        
        if "error" not in incident_data:
            try:
                result = self.sheets_service.add_incident(
                    cliente=incident_data["cliente"],
                    descripcion=incident_data["descripcion"],
                    prioridad=incident_data["prioridad"],
                    tipo=incident_data["tipo"]
                )
                
                if result.get("success"):
                    response_text = f"🎫 *Incidente Registrado*\n\n" \
                                  f"📋 Descripción: {incident_data['descripcion'][:100]}...\n" \
                                  f"⚡ Prioridad: {incident_data['prioridad']}\n\n" \
                                  f"👨‍💻 Un técnico revisará tu caso pronto."
                else:
                    response_text = "❌ Error registrando incidente."
                    
            except Exception as e:
                self.logger.error(f"Error creando incidente: {e}")
                response_text = "❌ Error técnico."
        else:
            response_text = "❌ Error procesando solicitud. Intenta de nuevo."
        
        # Resetear estado
        session["state"] = self.CONVERSATION_STATES["IDLE"]
        self.send_message(phone_number, response_text)

    def send_message(self, phone_number: str, message: str):
        """📤 Enviar mensaje de texto"""
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "type": "text",
                "text": {"body": message}
            }
            
            response = requests.post(self.base_url, headers=headers, json=data)
            
            if response.status_code != 200:
                self.logger.error(f"Error enviando mensaje: {response.text}")
                
        except Exception as e:
            self.logger.error(f"Error en send_message: {e}")

    def send_quick_replies(self, phone_number: str, header: str, options: list):
        """⚡ Enviar respuestas rápidas"""
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            # Crear botones (máximo 3 para WhatsApp)
            buttons = []
            for i, option in enumerate(options[:3]):
                buttons.append({
                    "type": "reply",
                    "reply": {
                        "id": f"btn_{i}",
                        "title": option[:20]  # Límite de caracteres
                    }
                })
            
            data = {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "type": "interactive",
                "interactive": {
                    "type": "button",
                    "body": {"text": header},
                    "action": {"buttons": buttons}
                }
            }
            
            response = requests.post(self.base_url, headers=headers, json=data)
            
            if response.status_code != 200:
                self.logger.error(f"Error enviando botones: {response.text}")
                
        except Exception as e:
            self.logger.error(f"Error en send_quick_replies: {e}")

    def run(self, host="0.0.0.0", port=5000, debug=False):
        """🚀 Ejecutar servidor Flask"""
        self.logger.info(f"🤖 Bot de WhatsApp iniciando en {host}:{port}...")
        self.app.run(host=host, port=port, debug=debug)


# Script principal
if __name__ == "__main__":
    # Configuración de WhatsApp Business API
    config = {
        "phone_number_id": "TU_PHONE_NUMBER_ID",  # De Facebook Developer Console
        "access_token": "TU_ACCESS_TOKEN",        # Token de acceso permanente
        "verify_token": "TU_VERIFY_TOKEN"         # Token de verificación
    }
    
    if any(val.startswith("TU_") for val in config.values()):
        print("❌ Configura los tokens de WhatsApp Business API")
        print("📖 Guía: https://developers.facebook.com/docs/whatsapp/business-management-api/get-started")
        exit(1)
    
    bot = WhatsAppISPBot(**config)
    bot.run(port=5000)

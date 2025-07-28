"""
🚀 MEJORA 5: SISTEMA DE NOTIFICACIONES MULTI-CANAL
=================================================

Sistema completo de notificaciones que integra WhatsApp, email, Slack y push notifications
para mantener informados a propietarios y administradores sobre el estado del negocio
"""

import asyncio
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from enum import Enum
import logging
from dataclasses import dataclass
import aiohttp
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart

# ========== CONFIGURACIÓN ==========

class NotificationChannel(Enum):
    """Canales de notificación disponibles"""
    EMAIL = "email"
    WHATSAPP = "whatsapp"
    SLACK = "slack"
    TELEGRAM = "telegram"
    SMS = "sms"
    PUSH = "push"

class NotificationPriority(Enum):
    """Niveles de prioridad"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class NotificationCategory(Enum):
    """Categorías de notificaciones"""
    BUSINESS_ALERT = "business_alert"
    PAYMENT_REMINDER = "payment_reminder"
    SYSTEM_STATUS = "system_status"
    REPORT_READY = "report_ready"
    CLIENT_UPDATE = "client_update"
    REVENUE_MILESTONE = "revenue_milestone"

@dataclass
class NotificationConfig:
    """Configuración de notificaciones"""
    
    # WhatsApp Business API
    whatsapp_token: str = ""
    whatsapp_phone_id: str = ""
    whatsapp_verify_token: str = "mi_token_verificacion"
    
    # Email SMTP
    email_server: str = "smtp.gmail.com"
    email_port: int = 587
    email_user: str = ""
    email_password: str = ""
    
    # Slack
    slack_token: str = ""
    slack_channel: str = "#general"
    
    # Telegram Bot
    telegram_token: str = ""
    telegram_chat_id: str = ""
    
    # SMS (Twilio)
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_phone_number: str = ""

# ========== CLASE BASE DE NOTIFICACIONES ==========

@dataclass
class Notification:
    """Clase base para notificaciones"""
    id: str
    title: str
    message: str
    category: NotificationCategory
    priority: NotificationPriority
    channels: List[NotificationChannel]
    recipient: str
    data: Dict[str, Any] = None
    scheduled_for: datetime = None
    created_at: datetime = None
    sent_at: datetime = None
    status: str = "pending"
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.data is None:
            self.data = {}

# ========== PROVEEDORES DE NOTIFICACIONES ==========

class WhatsAppProvider:
    """Proveedor de notificaciones WhatsApp Business"""
    
    def __init__(self, config: NotificationConfig):
        self.config = config
        self.base_url = "https://graph.facebook.com/v18.0"
    
    async def send_message(self, phone_number: str, message: str, template_name: str = None) -> bool:
        """Enviar mensaje por WhatsApp"""
        try:
            url = f"{self.base_url}/{self.config.whatsapp_phone_id}/messages"
            
            headers = {
                "Authorization": f"Bearer {self.config.whatsapp_token}",
                "Content-Type": "application/json"
            }
            
            # Formatear número de teléfono
            if not phone_number.startswith('+'):
                phone_number = f"+57{phone_number}"  # Colombia por defecto
            
            # Mensaje de texto simple
            payload = {
                "messaging_product": "whatsapp",
                "to": phone_number.replace('+', ''),
                "type": "text",
                "text": {"body": message}
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        logging.info(f"WhatsApp enviado a {phone_number}")
                        return True
                    else:
                        error = await response.text()
                        logging.error(f"Error WhatsApp: {error}")
                        return False
                        
        except Exception as e:
            logging.error(f"Error enviando WhatsApp: {e}")
            return False
    
    async def send_template_message(self, phone_number: str, template_name: str, parameters: List[str] = None) -> bool:
        """Enviar mensaje con plantilla de WhatsApp"""
        try:
            url = f"{self.base_url}/{self.config.whatsapp_phone_id}/messages"
            
            headers = {
                "Authorization": f"Bearer {self.config.whatsapp_token}",
                "Content-Type": "application/json"
            }
            
            # Plantilla con parámetros
            payload = {
                "messaging_product": "whatsapp",
                "to": phone_number.replace('+', ''),
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {"code": "es"},
                    "components": []
                }
            }
            
            # Agregar parámetros si existen
            if parameters:
                payload["template"]["components"] = [
                    {
                        "type": "body",
                        "parameters": [{"type": "text", "text": param} for param in parameters]
                    }
                ]
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    return response.status == 200
                    
        except Exception as e:
            logging.error(f"Error enviando plantilla WhatsApp: {e}")
            return False

class EmailProvider:
    """Proveedor de notificaciones por email"""
    
    def __init__(self, config: NotificationConfig):
        self.config = config
    
    async def send_email(self, recipient: str, subject: str, body: str, html_body: str = None) -> bool:
        """Enviar email"""
        try:
            msg = MimeMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.config.email_user
            msg['To'] = recipient
            
            # Texto plano
            text_part = MimeText(body, 'plain', 'utf-8')
            msg.attach(text_part)
            
            # HTML si se proporciona
            if html_body:
                html_part = MimeText(html_body, 'html', 'utf-8')
                msg.attach(html_part)
            
            # Enviar
            server = smtplib.SMTP(self.config.email_server, self.config.email_port)
            server.starttls()
            server.login(self.config.email_user, self.config.email_password)
            server.send_message(msg)
            server.quit()
            
            logging.info(f"Email enviado a {recipient}")
            return True
            
        except Exception as e:
            logging.error(f"Error enviando email: {e}")
            return False

class SlackProvider:
    """Proveedor de notificaciones Slack"""
    
    def __init__(self, config: NotificationConfig):
        self.config = config
    
    async def send_message(self, channel: str, message: str, blocks: List[Dict] = None) -> bool:
        """Enviar mensaje a Slack"""
        try:
            url = "https://slack.com/api/chat.postMessage"
            
            headers = {
                "Authorization": f"Bearer {self.config.slack_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "channel": channel,
                "text": message
            }
            
            if blocks:
                payload["blocks"] = blocks
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    result = await response.json()
                    return result.get("ok", False)
                    
        except Exception as e:
            logging.error(f"Error enviando Slack: {e}")
            return False

class TelegramProvider:
    """Proveedor de notificaciones Telegram"""
    
    def __init__(self, config: NotificationConfig):
        self.config = config
        self.base_url = f"https://api.telegram.org/bot{config.telegram_token}"
    
    async def send_message(self, chat_id: str, message: str, parse_mode: str = "HTML") -> bool:
        """Enviar mensaje por Telegram"""
        try:
            url = f"{self.base_url}/sendMessage"
            
            payload = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": parse_mode
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    result = await response.json()
                    return result.get("ok", False)
                    
        except Exception as e:
            logging.error(f"Error enviando Telegram: {e}")
            return False

# ========== GESTOR PRINCIPAL DE NOTIFICACIONES ==========

class NotificationManager:
    """Gestor principal del sistema de notificaciones"""
    
    def __init__(self, config: NotificationConfig, sheets_service=None):
        self.config = config
        self.sheets_service = sheets_service
        
        # Inicializar proveedores
        self.providers = {
            NotificationChannel.WHATSAPP: WhatsAppProvider(config),
            NotificationChannel.EMAIL: EmailProvider(config),
            NotificationChannel.SLACK: SlackProvider(config),
            NotificationChannel.TELEGRAM: TelegramProvider(config)
        }
        
        # Cola de notificaciones
        self.notification_queue = []
        self.sent_notifications = []
        
        # Configuración de logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    async def send_notification(self, notification: Notification) -> Dict[str, bool]:
        """Enviar notificación por todos los canales especificados"""
        results = {}
        
        for channel in notification.channels:
            success = await self._send_via_channel(notification, channel)
            results[channel.value] = success
            
            if success:
                self.logger.info(f"Notificación {notification.id} enviada por {channel.value}")
            else:
                self.logger.error(f"Error enviando {notification.id} por {channel.value}")
        
        # Actualizar estado
        notification.sent_at = datetime.now()
        notification.status = "sent" if any(results.values()) else "failed"
        
        # Guardar en historial
        self.sent_notifications.append(notification)
        
        return results
    
    async def _send_via_channel(self, notification: Notification, channel: NotificationChannel) -> bool:
        """Enviar notificación por un canal específico"""
        try:
            provider = self.providers.get(channel)
            if not provider:
                return False
            
            if channel == NotificationChannel.WHATSAPP:
                return await provider.send_message(
                    notification.recipient,
                    f"*{notification.title}*\n\n{notification.message}"
                )
            
            elif channel == NotificationChannel.EMAIL:
                html_body = self._generate_email_html(notification)
                return await provider.send_email(
                    notification.recipient,
                    notification.title,
                    notification.message,
                    html_body
                )
            
            elif channel == NotificationChannel.SLACK:
                blocks = self._generate_slack_blocks(notification)
                return await provider.send_message(
                    self.config.slack_channel,
                    notification.message,
                    blocks
                )
            
            elif channel == NotificationChannel.TELEGRAM:
                formatted_message = f"<b>{notification.title}</b>\n\n{notification.message}"
                return await provider.send_message(
                    self.config.telegram_chat_id,
                    formatted_message
                )
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error en canal {channel.value}: {e}")
            return False
    
    def _generate_email_html(self, notification: Notification) -> str:
        """Generar HTML para email"""
        priority_colors = {
            NotificationPriority.LOW: "#28a745",
            NotificationPriority.MEDIUM: "#ffc107", 
            NotificationPriority.HIGH: "#fd7e14",
            NotificationPriority.CRITICAL: "#dc3545"
        }
        
        color = priority_colors.get(notification.priority, "#6c757d")
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; margin: 20px;">
            <div style="border-left: 4px solid {color}; padding-left: 20px;">
                <h2 style="color: {color}; margin-top: 0;">{notification.title}</h2>
                <p style="font-size: 16px; line-height: 1.5;">{notification.message}</p>
                <hr>
                <p style="color: #666; font-size: 12px;">
                    Prioridad: {notification.priority.value.upper()}<br>
                    Categoría: {notification.category.value}<br>
                    Enviado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                </p>
            </div>
        </body>
        </html>
        """
    
    def _generate_slack_blocks(self, notification: Notification) -> List[Dict]:
        """Generar bloques para Slack"""
        priority_emojis = {
            NotificationPriority.LOW: "🟢",
            NotificationPriority.MEDIUM: "🟡",
            NotificationPriority.HIGH: "🟠", 
            NotificationPriority.CRITICAL: "🔴"
        }
        
        emoji = priority_emojis.get(notification.priority, "ℹ️")
        
        return [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji} {notification.title}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": notification.message
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Prioridad:* {notification.priority.value} | *Categoría:* {notification.category.value}"
                    }
                ]
            }
        ]
    
    # ========== NOTIFICACIONES ESPECÍFICAS DEL NEGOCIO ==========
    
    async def notify_payment_overdue(self, cliente_data: Dict[str, Any], propietario_phone: str):
        """Notificar pago vencido"""
        notification = Notification(
            id=f"payment_overdue_{cliente_data.get('ID Cliente')}_{datetime.now().timestamp()}",
            title="⚠️ Pago Vencido Detectado",
            message=f"El cliente {cliente_data.get('Nombre')} en zona {cliente_data.get('Zona')} tiene un pago pendiente de ${cliente_data.get('Pago', 0)}. Se recomienda contactar pronto para evitar suspensión del servicio.",
            category=NotificationCategory.PAYMENT_REMINDER,
            priority=NotificationPriority.HIGH,
            channels=[NotificationChannel.WHATSAPP, NotificationChannel.EMAIL],
            recipient=propietario_phone,
            data=cliente_data
        )
        
        return await self.send_notification(notification)
    
    async def notify_revenue_milestone(self, milestone_amount: float, current_revenue: float, propietarios: List[str]):
        """Notificar hito de ingresos alcanzado"""
        percentage = (current_revenue / milestone_amount) * 100
        
        notification = Notification(
            id=f"revenue_milestone_{milestone_amount}_{datetime.now().timestamp()}",
            title="🎉 ¡Hito de Ingresos Alcanzado!",
            message=f"¡Excelente noticia! Hemos alcanzado el {percentage:.1f}% de la meta mensual con ${current_revenue:,.0f} de ${milestone_amount:,.0f}. ¡Sigamos así!",
            category=NotificationCategory.REVENUE_MILESTONE,
            priority=NotificationPriority.MEDIUM,
            channels=[NotificationChannel.WHATSAPP, NotificationChannel.SLACK],
            recipient="all",
            data={"milestone": milestone_amount, "current": current_revenue}
        )
        
        # Enviar a todos los propietarios
        results = {}
        for propietario in propietarios:
            notification.recipient = propietario
            notification.id = f"revenue_milestone_{propietario}_{datetime.now().timestamp()}"
            results[propietario] = await self.send_notification(notification)
        
        return results
    
    async def notify_system_alert(self, alert_data: Dict[str, Any], admin_contacts: List[str]):
        """Notificar alerta del sistema"""
        severity_map = {
            'low': NotificationPriority.LOW,
            'medium': NotificationPriority.MEDIUM,
            'high': NotificationPriority.HIGH,
            'critical': NotificationPriority.CRITICAL
        }
        
        priority = severity_map.get(alert_data.get('nivel', 'medium'), NotificationPriority.MEDIUM)
        
        notification = Notification(
            id=f"system_alert_{alert_data.get('id', 'unknown')}",
            title=f"🚨 Alerta del Sistema: {alert_data.get('titulo', 'Sin título')}",
            message=alert_data.get('mensaje', 'Sin descripción disponible'),
            category=NotificationCategory.SYSTEM_STATUS,
            priority=priority,
            channels=[NotificationChannel.WHATSAPP, NotificationChannel.EMAIL, NotificationChannel.SLACK],
            recipient="admin",
            data=alert_data
        )
        
        results = {}
        for contact in admin_contacts:
            notification.recipient = contact
            results[contact] = await self.send_notification(notification)
        
        return results
    
    async def notify_daily_report_ready(self, report_data: Dict[str, Any], propietario: str, propietario_phone: str):
        """Notificar que el reporte diario está listo"""
        notification = Notification(
            id=f"daily_report_{propietario}_{datetime.now().strftime('%Y%m%d')}",
            title="📊 Reporte Diario Disponible",
            message=f"Tu reporte diario está listo. Resumen: {report_data.get('clientes_activos', 0)} clientes activos, ${report_data.get('ingresos_esperados', 0):,.0f} en ingresos esperados. Revisa el dashboard para más detalles.",
            category=NotificationCategory.REPORT_READY,
            priority=NotificationPriority.LOW,
            channels=[NotificationChannel.WHATSAPP],
            recipient=propietario_phone,
            data=report_data
        )
        
        return await self.send_notification(notification)
    
    async def notify_new_client(self, cliente_data: Dict[str, Any], propietario_phone: str):
        """Notificar nuevo cliente agregado"""
        notification = Notification(
            id=f"new_client_{cliente_data.get('ID Cliente')}_{datetime.now().timestamp()}",
            title="🆕 Nuevo Cliente Registrado",
            message=f"¡Bienvenido nuevo cliente! {cliente_data.get('Nombre')} se ha unido en la zona {cliente_data.get('Zona')} con un plan de ${cliente_data.get('Pago', 0)}.",
            category=NotificationCategory.CLIENT_UPDATE,
            priority=NotificationPriority.MEDIUM,
            channels=[NotificationChannel.WHATSAPP],
            recipient=propietario_phone,
            data=cliente_data
        )
        
        return await self.send_notification(notification)
    
    # ========== NOTIFICACIONES PROGRAMADAS ==========
    
    async def schedule_daily_summary(self, propietarios_data: List[Dict[str, Any]]):
        """Programar resumen diario para todos los propietarios"""
        for propietario_data in propietarios_data:
            # Obtener datos del propietario
            propietario = propietario_data.get('nombre')
            phone = propietario_data.get('telefono')
            
            if not phone:
                continue
            
            # Obtener estadísticas del propietario
            if self.sheets_service:
                try:
                    clientes = await self.sheets_service.get_enriched_clients()
                    clientes_propietario = [c for c in clientes if c.get('Propietario') == propietario]
                    
                    stats = {
                        'total_clientes': len(clientes_propietario),
                        'clientes_activos': len([c for c in clientes_propietario if str(c.get('Activo (SI/NO)', '')).lower() in ['si', 'sí']]),
                        'ingresos_esperados': sum(
                            float(str(c.get('Pago', 0)).replace('$', '').replace(',', '') or 0)
                            for c in clientes_propietario 
                            if str(c.get('Activo (SI/NO)', '')).lower() in ['si', 'sí']
                        )
                    }
                    
                    await self.notify_daily_report_ready(stats, propietario, phone)
                    
                except Exception as e:
                    self.logger.error(f"Error obteniendo datos para {propietario}: {e}")
    
    async def check_payment_alerts(self):
        """Verificar alertas de pagos vencidos"""
        if not self.sheets_service:
            return
        
        try:
            clientes = await self.sheets_service.get_enriched_clients()
            
            # Buscar clientes con pagos vencidos
            clientes_vencidos = []
            for cliente in clientes:
                activo = str(cliente.get('Activo (SI/NO)', '')).lower() in ['si', 'sí']
                pagado = str(cliente.get('Pagado', 'NO')).upper() == 'SI'
                
                if activo and not pagado:
                    clientes_vencidos.append(cliente)
            
            # Agrupar por propietario y notificar
            propietarios_alertas = {}
            for cliente in clientes_vencidos:
                propietario = cliente.get('Propietario')
                if propietario not in propietarios_alertas:
                    propietarios_alertas[propietario] = []
                propietarios_alertas[propietario].append(cliente)
            
            # Enviar notificaciones (necesitarías una base de datos con teléfonos de propietarios)
            # Por ahora, simulamos con datos estáticos
            propietarios_phones = {
                'Carlos': '+573001234567',
                'Ana': '+573007654321'
                # Agregar más según corresponda
            }
            
            for propietario, clientes_prop in propietarios_alertas.items():
                phone = propietarios_phones.get(propietario)
                if phone:
                    for cliente in clientes_prop:
                        await self.notify_payment_overdue(cliente, phone)
            
        except Exception as e:
            self.logger.error(f"Error verificando alertas de pago: {e}")
    
    # ========== UTILIDADES ==========
    
    def get_notification_history(self, limit: int = 50) -> List[Notification]:
        """Obtener historial de notificaciones"""
        return self.sent_notifications[-limit:]
    
    def get_notification_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de notificaciones"""
        total = len(self.sent_notifications)
        if total == 0:
            return {"total": 0}
        
        by_channel = {}
        by_priority = {}
        by_category = {}
        
        for notification in self.sent_notifications:
            # Por canal
            for channel in notification.channels:
                by_channel[channel.value] = by_channel.get(channel.value, 0) + 1
            
            # Por prioridad
            priority = notification.priority.value
            by_priority[priority] = by_priority.get(priority, 0) + 1
            
            # Por categoría
            category = notification.category.value
            by_category[category] = by_category.get(category, 0) + 1
        
        return {
            "total": total,
            "by_channel": by_channel,
            "by_priority": by_priority,
            "by_category": by_category,
            "success_rate": len([n for n in self.sent_notifications if n.status == "sent"]) / total * 100
        }

# ========== INTEGRACIÓN CON EL SISTEMA PRINCIPAL ==========

class NotificationIntegrator:
    """Integrador de notificaciones con el sistema principal"""
    
    def __init__(self, notification_manager: NotificationManager, sheets_service, business_monitor=None):
        self.notification_manager = notification_manager
        self.sheets_service = sheets_service
        self.business_monitor = business_monitor
    
    async def setup_automatic_notifications(self):
        """Configurar notificaciones automáticas"""
        # Programar verificaciones periódicas
        asyncio.create_task(self._periodic_payment_check())
        asyncio.create_task(self._periodic_milestone_check())
        asyncio.create_task(self._periodic_daily_summary())
    
    async def _periodic_payment_check(self):
        """Verificación periódica de pagos (cada 4 horas)"""
        while True:
            await self.notification_manager.check_payment_alerts()
            await asyncio.sleep(4 * 3600)  # 4 horas
    
    async def _periodic_milestone_check(self):
        """Verificación periódica de hitos (cada 2 horas)"""
        while True:
            try:
                # Obtener ingresos actuales
                clientes = await self.sheets_service.get_enriched_clients()
                ingresos_actuales = sum(
                    float(str(c.get('Pago', 0)).replace('$', '').replace(',', '') or 0)
                    for c in clientes 
                    if str(c.get('Activo (SI/NO)', '')).lower() in ['si', 'sí']
                )
                
                # Verificar hitos (ejemplo: cada $50,000)
                hitos = [50000, 100000, 150000, 200000]
                for hito in hitos:
                    if ingresos_actuales >= hito:
                        # Verificar si ya se notificó este hito hoy
                        today = datetime.now().strftime('%Y-%m-%d')
                        notification_id = f"revenue_milestone_{hito}_{today}"
                        
                        if not any(n.id.startswith(notification_id) for n in self.notification_manager.sent_notifications):
                            propietarios = ['Carlos', 'Ana']  # Lista de propietarios
                            await self.notification_manager.notify_revenue_milestone(hito, ingresos_actuales, propietarios)
                
            except Exception as e:
                logging.error(f"Error en verificación de hitos: {e}")
            
            await asyncio.sleep(2 * 3600)  # 2 horas
    
    async def _periodic_daily_summary(self):
        """Envío periódico de resumen diario (8:00 AM)"""
        while True:
            now = datetime.now()
            
            # Verificar si es hora de enviar (8:00 AM)
            if now.hour == 8 and now.minute == 0:
                propietarios_data = [
                    {'nombre': 'Carlos', 'telefono': '+573001234567'},
                    {'nombre': 'Ana', 'telefono': '+573007654321'}
                ]
                
                await self.notification_manager.schedule_daily_summary(propietarios_data)
            
            # Esperar 1 minuto antes de verificar de nuevo
            await asyncio.sleep(60)

# ========== EJEMPLO DE USO ==========

async def demo_notifications():
    """Demostración del sistema de notificaciones"""
    
    # Configuración de ejemplo
    config = NotificationConfig(
        whatsapp_token="tu_token_aqui",
        whatsapp_phone_id="tu_phone_id_aqui",
        email_user="tu_email@gmail.com",
        email_password="tu_password",
        slack_token="xoxb-tu-token-slack",
        telegram_token="tu_bot_token"
    )
    
    # Crear manager
    notification_manager = NotificationManager(config)
    
    # Ejemplo de notificación
    test_notification = Notification(
        id="test_001",
        title="Prueba del Sistema",
        message="Este es un mensaje de prueba del sistema de notificaciones.",
        category=NotificationCategory.SYSTEM_STATUS,
        priority=NotificationPriority.MEDIUM,
        channels=[NotificationChannel.EMAIL],
        recipient="admin@empresa.com"
    )
    
    # Enviar notificación
    results = await notification_manager.send_notification(test_notification)
    print(f"Resultados: {results}")
    
    # Obtener estadísticas
    stats = notification_manager.get_notification_stats()
    print(f"Estadísticas: {stats}")

if __name__ == "__main__":
    asyncio.run(demo_notifications())

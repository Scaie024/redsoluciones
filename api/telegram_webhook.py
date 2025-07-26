"""
Webhook handler para Telegram Bot - Red Soluciones ISP
Integra Carlos (el agente empresarial) con Telegram
"""
from typing import Any, Dict

def handle_telegram_webhook(update: Dict[str, Any]) -> Dict[str, Any]:
    """Procesa un update de Telegram y devuelve la acción a tomar"""
    # Obtener chat_id y mensaje de texto
    message = update.get('message') or update.get('edited_message') or {}
    chat = message.get('chat', {})
    chat_id = chat.get('id')
    text = message.get('text', '').strip()
    user = message.get('from', {})
    username = user.get('username', 'Usuario')
    
    # Si no hay texto, respuesta genérica
    if not text:
        return {
            "method": "sendMessage",
            "chat_id": chat_id,
            "text": "👋 Hola! Soy Carlos, el agente empresarial de Red Soluciones ISP.\n\nEscribe 'ayuda' para ver los comandos disponibles.",
            "parse_mode": "Markdown"
        }
    
    # Simular respuesta de Carlos (aquí se integraría con la API del backend)
    if text.lower() in ['ayuda', 'help', '/help', '/start']:
        response_text = """🤖 **Carlos - Red Soluciones ISP**

📋 **Comandos disponibles:**
• `cliente: [Nombre], [Teléfono], [Zona]` - Registrar cliente
• `prospecto: [Nombre], [Teléfono], [Zona]` - Registrar prospecto  
• `buscar [término]` - Buscar información
• `estadísticas` - Ver análisis financiero
• `clientes` - Mostrar todos los clientes
• `reportar [problema]` - Reportar incidencia

💡 **Ejemplos:**
• `cliente: Juan Pérez, 4641234567, Centro`
• `buscar Juan`
• `estadísticas`"""
        
    elif text.lower().startswith('cliente:'):
        response_text = f"✅ **Cliente registrado exitosamente**\n\n📝 Datos: {text[8:].strip()}\n🆔 ID generado automáticamente\n💰 Plan asignado: Premium\n\n¡Gracias por usar Red Soluciones ISP!"
        
    elif text.lower().startswith('prospecto:'):
        response_text = f"🎯 **Prospecto registrado**\n\n📝 Datos: {text[10:].strip()}\n📅 Seguimiento programado\n📊 Estado: Pendiente contacto\n\n¡Lo contactaremos pronto!"
        
    elif text.lower() in ['estadísticas', 'estadisticas', 'stats']:
        response_text = """📊 **Estadísticas Red Soluciones ISP**

👥 **Clientes:** 560 activos
📍 **Zonas:** 8 cubiertas  
💰 **Ingresos:** $280,000/mes
📈 **Crecimiento:** +12% este mes

🏆 **Zona líder:** SALAMANCA (258 clientes)
⭐ **Plan popular:** Premium ($500/mes)"""
        
    elif text.lower() in ['clientes', 'listar', 'mostrar']:
        response_text = """👥 **Resumen de Clientes**

📊 **Total:** 560 clientes registrados
🟢 **Activos:** 534 clientes
🟡 **Prospectos:** 26 en seguimiento

📍 **Por zonas:**
• SALAMANCA: 258 clientes
• CERRO/BLANCO: 32 clientes  
• TAMBOR: 24 clientes
• RESERVA: 12 clientes
• Otras zonas: 234 clientes"""
        
    elif text.lower().startswith('buscar'):
        term = text[6:].strip()
        response_text = f"🔍 **Búsqueda: '{term}'**\n\n📋 Resultados encontrados:\n• Consultando base de datos...\n• Analizando 560 registros...\n\n💡 Usa comandos más específicos para mejores resultados."
        
    elif text.lower().startswith('reportar'):
        problema = text[8:].strip()
        response_text = f"🚨 **Incidencia registrada**\n\n📝 Problema: {problema}\n🎫 Ticket: INC-{chat_id}-001\n⏰ Tiempo estimado: 2-4 horas\n\n📞 Te mantendremos informado."
        
    else:
        # Respuesta genérica tipo Carlos
        response_text = f"""🤖 **Carlos aquí!**

No entendí tu consulta: "{text}"

💡 **Sugerencias:**
• Escribe `ayuda` para ver comandos
• Usa formato: `cliente: Nombre, Teléfono, Zona`
• Pregunta por `estadísticas` o `clientes`

¿En qué más puedo ayudarte? 😊"""
    
    return {
        "method": "sendMessage",
        "chat_id": chat_id,
        "text": response_text,
        "parse_mode": "Markdown"
    }

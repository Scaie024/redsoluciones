"""
⚙️ CONFIGURACIÓN PARA BOTS DE MENSAJERÍA
========================================

Configuración centralizada para Telegram y WhatsApp
"""

import os
from typing import Dict, Any

class MessagingConfig:
    """⚙️ Configuración para bots de mensajería"""
    
    # === TELEGRAM BOT ===
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL", "")
    
    # === WHATSAPP BUSINESS API ===
    WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
    WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
    WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "mensajeria_isp_2025")
    
    # === SERVIDOR ===
    MESSAGING_HOST = os.getenv("MESSAGING_HOST", "0.0.0.0")
    MESSAGING_PORT = int(os.getenv("MESSAGING_PORT", "5001"))
    
    # === CONFIGURACIÓN DE AGENTE ===
    MAX_RESPONSE_LENGTH = 800
    ENABLE_EMOJIS = True
    COMPACT_MODE = True
    AUTO_REGISTER = True
    
    # === ZONAS DISPONIBLES ===
    AVAILABLE_ZONES = [
        "Norte", "Sur", "Centro", "Este", "Oeste", 
        "Salamanca", "Bajio", "Industrial", "Residencial",
        "CERRO/BLANCO", "TAMBOR/SANTA ANA"
    ]
    
    # === PLANES DISPONIBLES ===
    AVAILABLE_PLANS = {
        20: {"name": "Básico", "price": 350},
        50: {"name": "Estándar", "price": 450},
        100: {"name": "Premium", "price": 600}
    }
    
    @classmethod
    def get_plan_info(cls, mbps: int) -> Dict[str, Any]:
        """📦 Obtener información de plan"""
        if mbps >= 100:
            return cls.AVAILABLE_PLANS[100]
        elif mbps >= 50:
            return cls.AVAILABLE_PLANS[50]
        else:
            return cls.AVAILABLE_PLANS[20]
    
    @classmethod
    def validate_config(cls) -> Dict[str, bool]:
        """✅ Validar configuración"""
        return {
            "telegram_ready": bool(cls.TELEGRAM_BOT_TOKEN),
            "whatsapp_ready": bool(cls.WHATSAPP_PHONE_NUMBER_ID and cls.WHATSAPP_ACCESS_TOKEN),
            "server_ready": True
        }
    
    @classmethod
    def get_setup_instructions(cls) -> Dict[str, str]:
        """📋 Obtener instrucciones de configuración"""
        return {
            "telegram": """
🤖 CONFIGURACIÓN TELEGRAM BOT:

1. Habla con @BotFather en Telegram
2. Crea un nuevo bot: /newbot
3. Sigue las instrucciones y obtén el token
4. Exporta la variable: export TELEGRAM_BOT_TOKEN="tu_token_aqui"
5. Ejecuta: python messaging/telegram_bot.py

📖 Documentación: https://core.telegram.org/bots
            """,
            
            "whatsapp": """
📱 CONFIGURACIÓN WHATSAPP BUSINESS API:

1. Ve a https://developers.facebook.com/
2. Crea una aplicación de WhatsApp Business
3. Obtén tu Phone Number ID y Access Token
4. Configura webhook: https://tu-servidor.com/webhook
5. Exporta variables:
   export WHATSAPP_PHONE_NUMBER_ID="tu_phone_id"
   export WHATSAPP_ACCESS_TOKEN="tu_token"
6. Ejecuta: python messaging/whatsapp_bot.py

📖 Documentación: https://developers.facebook.com/docs/whatsapp
            """
        }

# Instancia global
messaging_config = MessagingConfig()

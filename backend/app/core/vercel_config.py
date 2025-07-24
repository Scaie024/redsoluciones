"""
Configuración adaptada para Vercel - Red Soluciones ISP
"""
import os
from pathlib import Path

# Configuración básica para Vercel
class VercelSettings:
    PROJECT_NAME: str = "Red Soluciones ISP"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Variables de entorno para Vercel
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    
    # Google Sheets (opcional)
    GOOGLE_SHEET_ID: str = os.getenv("GOOGLE_SHEET_ID", "")
    
    @property
    def has_gemini(self) -> bool:
        return bool(self.GEMINI_API_KEY)
    
    @property
    def has_telegram(self) -> bool:
        return bool(self.TELEGRAM_BOT_TOKEN)

# Instancia global
vercel_settings = VercelSettings()

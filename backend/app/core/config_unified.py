"""
Configuración Unificada - Red Soluciones ISP
Todas las configuraciones del sistema en un solo archivo
"""
import os
import secrets
import logging
from pathlib import Path
from typing import List, Optional

# === CARGAR VARIABLES DE ENTORNO ===
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Cargar manualmente si python-dotenv no está disponible
    env_file = Path(__file__).parents[3] / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value


class Settings:
    # === INFORMACIÓN DEL PROYECTO ===
    PROJECT_NAME: str = "Red Soluciones ISP"
    VERSION: str = "2.0.0"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # === SERVIDOR ===
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8004"))
    
    # === RUTAS DEL SISTEMA ===
    @property
    def BASE_DIR(self) -> Path:
        """Directorio base del proyecto"""
        return Path(__file__).parents[3]
    
    @property
    def PROJECT_ROOT(self) -> Path:
        """Raíz del proyecto"""
        return self.BASE_DIR
    
    @property
    def FRONTEND_DIR(self) -> Path:
        """Directorio del frontend"""
        return self.BASE_DIR / "frontend"
    
    # === GOOGLE SHEETS ===
    @property
    def GOOGLE_CREDENTIALS_PATH(self) -> Path:
        """Buscar credenciales en múltiples ubicaciones - OBLIGATORIO"""
        possible_paths = [
            self.BASE_DIR / "service_account.json",
            self.BASE_DIR / "config" / "service_account.json", 
            Path.home() / ".config" / "red-soluciones" / "service_account.json",
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        raise ValueError(
            "❌ service_account.json no encontrado. "
            "Coloque el archivo service_account.json en la raíz del proyecto o configure GOOGLE_APPLICATION_CREDENTIALS"
        )
    
    @property
    def GOOGLE_SHEET_ID(self) -> str:
        sheet_id = os.getenv("GOOGLE_SHEET_ID", "")
        if not sheet_id:
            # Usar ID por defecto como fallback
            logging.warning("⚠️ GOOGLE_SHEET_ID no configurado - usando ID por defecto")
            return "1BcRhPZBfVYadXyYfDeF8Mtt7-qaTJ5_Q4T4FE1oVBq0"
        return sheet_id
    
    # === GEMINI AI ===
    @property
    def GEMINI_API_KEY(self) -> str:
        """Gemini API key for AI agent - OPCIONAL con fallback"""
        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            # Fallback graceful en lugar de error
            logging.warning("⚠️ GEMINI_API_KEY no configurado - Sistema funcionará sin IA")
            return ""
        return api_key
    
    # === TELEGRAM BOT ===
    @property
    def TELEGRAM_BOT_TOKEN(self) -> str:
        """Token del bot de Telegram - OPCIONAL"""
        token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        if not token:
            logging.warning("⚠️ TELEGRAM_BOT_TOKEN no configurado - Bot de Telegram deshabilitado")
            return ""
        return token
    
    # === SEGURIDAD ===
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    
    # === LOGGING ===
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # === CORS ===
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8004",
        "http://127.0.0.1:8004",
        "https://red-soluciones.vercel.app",  # Dominio de producción
    ]

    def __init__(self):
        """Initialize settings instance"""
        pass


# Instancia global de configuración
settings = Settings()

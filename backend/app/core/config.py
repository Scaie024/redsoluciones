"""
Configuración Unificada - Red Soluciones ISP
Todas las configuraciones del sistema en un solo archivo
"""
import os
import secrets
import logging
from pathlib import Path
from typing import List, Optional


class Settings:
    # === INFORMACIÓN DEL PROYECTO ===
    PROJECT_NAME: str = "Red Soluciones ISP"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    
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
    def GOOGLE_CREDENTIALS_PATH(self) -> Optional[Path]:
        """Buscar credenciales en múltiples ubicaciones"""
        possible_paths = [
            self.BASE_DIR / "service_account.json",
            self.BASE_DIR / "config" / "service_account.json", 
            Path.home() / ".config" / "red-soluciones" / "service_account.json",
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        return None
    
    @property
    def GOOGLE_SHEET_ID(self) -> str:
        sheet_id = os.getenv("GOOGLE_SHEET_ID", "")
        if not sheet_id:
            logging.warning("GOOGLE_SHEET_ID not set - using demo sheet")
            return "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"  # Demo sheet
        return sheet_id
    
    # === GEMINI AI ===
    @property
    def GEMINI_API_KEY(self) -> str:
        """Gemini API key for AI agent"""
        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            logging.warning("GEMINI_API_KEY not set - AI features will be limited")
        return api_key
    
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

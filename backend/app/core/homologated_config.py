"""
CONFIGURACIÓN CENTRAL PARA SISTEMA HOMOLOGADO
===========================================

Configuración unificada para Red Soluciones ISP v4.0
Incluye configuración de Google Sheets, IA, y sistema de contexto.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class HomologatedConfig:
    """
    Configuración centralizada para el sistema homologado
    """
    
    # === INFORMACIÓN DEL PROYECTO ===
    PROJECT_NAME = "Red Soluciones ISP"
    VERSION = "4.0 Homologado"
    DESCRIPTION = "Sistema empresarial ISP con IA integrada y backend Google Sheets"
    
    # === CONFIGURACIÓN DE ENTORNO ===
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
    
    # === CONFIGURACIÓN DE SERVIDOR ===
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8004))
    
    # === CONFIGURACIÓN DE GOOGLE SHEETS ===
    GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
    GOOGLE_SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service_account.json")
    
    # Configuración específica de hojas
    SHEETS_CONFIG = {
        "clientes": {
            "name": "Clientes",
            "range": "A:Z",
            "cache_ttl": 300,  # 5 minutos
            "required_fields": ["Nombre", "Plan", "Estado", "Propietario"]
        },
        "prospectos": {
            "name": "Prospectos", 
            "range": "A:Z",
            "cache_ttl": 180,  # 3 minutos
            "required_fields": ["Nombre", "Estado", "Propietario"]
        },
        "incidentes": {
            "name": "Incidentes",
            "range": "A:Z", 
            "cache_ttl": 60,   # 1 minuto
            "required_fields": ["Cliente_ID", "Tipo", "Estado", "Prioridad"]
        },
        "estadisticas": {
            "name": "Estadisticas",
            "range": "A:Z",
            "cache_ttl": 600,  # 10 minutos
            "required_fields": ["Fecha", "Total_Clientes", "Ingresos_Mes"]
        },
        "zonas": {
            "name": "Zonas",
            "range": "A:Z",
            "cache_ttl": 900,  # 15 minutos
            "required_fields": ["Nombre", "Cobertura"]
        },
        "propietarios": {
            "name": "Propietarios",
            "range": "A:Z",
            "cache_ttl": 3600, # 1 hora
            "required_fields": ["Nombre", "Rol"]
        }
    }
    
    # === CONFIGURACIÓN DE IA ===
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    AI_MODEL = "gemini-1.5-flash"
    AI_TEMPERATURE = 0.7
    AI_MAX_TOKENS = 1000
    
    # === CONFIGURACIÓN DE CONTEXTO ===
    CONTEXT_ENGINE_CONFIG = {
        "max_entities": 10000,
        "cache_cleanup_interval": 3600,  # 1 hora
        "relationship_depth": 3,
        "auto_refresh_interval": 300,    # 5 minutos
        "sync_batch_size": 100
    }
    
    # === CONFIGURACIÓN DE AUTENTICACIÓN ===
    OWNERS_CONFIG = {
        "eduardo": {
            "display_name": "Eduardo",
            "email": "eduardo@redsoluciones.com",
            "icon": "👨‍💼",
            "color": "#2563eb",
            "permissions": ["read", "write", "delete", "admin"],
            "zones": ["Centro", "Norte", "Sur"],
            "dashboard_config": {
                "default_view": "executive",
                "auto_refresh": True,
                "show_insights": True
            }
        },
        "omar": {
            "display_name": "Omar", 
            "email": "omar@redsoluciones.com",
            "icon": "👤",
            "color": "#dc2626", 
            "permissions": ["read", "write", "delete", "admin"],
            "zones": ["Este", "Oeste", "Industrial"],
            "dashboard_config": {
                "default_view": "operational",
                "auto_refresh": True,
                "show_insights": True
            }
        }
    }
    
    # === CONFIGURACIÓN DE LOGGING ===
    LOGGING_CONFIG = {
        "level": os.getenv("LOG_LEVEL", "INFO"),
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": "logs/redsoluciones_homologado.log",
        "max_bytes": 10 * 1024 * 1024,  # 10MB
        "backup_count": 5
    }
    
    # === CONFIGURACIÓN DE PERFORMANCE ===
    PERFORMANCE_CONFIG = {
        "api_timeout": 30,
        "max_concurrent_requests": 100,
        "rate_limit_per_minute": 1000,
        "cache_max_size": 1000,
        "background_tasks_enabled": True
    }
    
    # === CONFIGURACIÓN DE FRONTEND ===
    FRONTEND_CONFIG = {
        "auto_refresh_interval": 30000,  # 30 segundos
        "chat_message_limit": 100,
        "dashboard_widgets": [
            "business_metrics",
            "personal_kpis", 
            "pending_incidents",
            "clients_overview",
            "insights_panel"
        ],
        "theme": {
            "primary_color": "#e74c3c",
            "secondary_color": "#3498db", 
            "success_color": "#2ecc71",
            "warning_color": "#f39c12",
            "danger_color": "#e74c3c"
        }
    }
    
    # === CONFIGURACIÓN DE APIS EXTERNAS ===
    EXTERNAL_APIS = {
        "telegram": {
            "bot_token": os.getenv("TELEGRAM_BOT_TOKEN"),
            "webhook_url": os.getenv("TELEGRAM_WEBHOOK_URL"),
            "enabled": bool(os.getenv("TELEGRAM_BOT_TOKEN"))
        },
        "email": {
            "smtp_server": os.getenv("SMTP_SERVER"),
            "smtp_port": int(os.getenv("SMTP_PORT", 587)),
            "username": os.getenv("EMAIL_USERNAME"),
            "password": os.getenv("EMAIL_PASSWORD"),
            "enabled": bool(os.getenv("SMTP_SERVER"))
        }
    }
    
    # === CONFIGURACIÓN DE BUSINESS RULES ===
    BUSINESS_RULES = {
        "client_validation": {
            "min_name_length": 3,
            "required_phone": True,
            "unique_email": True
        },
        "incident_priority": {
            "auto_escalate_hours": 24,
            "high_priority_keywords": ["sin internet", "servicio caido", "urgente"],
            "auto_assign_zones": True
        },
        "revenue_targets": {
            "monthly_growth_target": 0.05,  # 5%
            "churn_rate_threshold": 0.05,   # 5%
            "arpu_minimum": 25.0
        }
    }
    
    # === PATHS Y DIRECTORIOS ===
    BASE_DIR = Path(__file__).parent.parent
    FRONTEND_DIR = BASE_DIR / "frontend"
    LOGS_DIR = BASE_DIR / "logs"
    TEMP_DIR = BASE_DIR / "temp"
    
    @classmethod
    def get_sheets_config(cls, sheet_name: str) -> Optional[Dict[str, Any]]:
        """Obtener configuración específica de una hoja"""
        return cls.SHEETS_CONFIG.get(sheet_name)
    
    @classmethod
    def get_owner_config(cls, owner_id: str) -> Optional[Dict[str, Any]]:
        """Obtener configuración específica de un propietario"""
        return cls.OWNERS_CONFIG.get(owner_id.lower())
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validar configuración completa"""
        issues = []
        warnings = []
        
        # Validar Google Sheets
        if not cls.GOOGLE_SHEET_ID:
            issues.append("GOOGLE_SHEET_ID no configurado")
        
        if not os.path.exists(cls.GOOGLE_SERVICE_ACCOUNT_FILE):
            issues.append(f"Archivo de credenciales no encontrado: {cls.GOOGLE_SERVICE_ACCOUNT_FILE}")
        
        # Validar IA
        if not cls.GEMINI_API_KEY:
            warnings.append("GEMINI_API_KEY no configurado - IA no estará disponible")
        
        # Validar directorios
        for dir_path in [cls.LOGS_DIR, cls.TEMP_DIR]:
            if not dir_path.exists():
                try:
                    dir_path.mkdir(parents=True, exist_ok=True)
                    warnings.append(f"Directorio creado: {dir_path}")
                except Exception as e:
                    issues.append(f"No se pudo crear directorio {dir_path}: {e}")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "config_summary": {
                "sheets_configured": bool(cls.GOOGLE_SHEET_ID),
                "ai_available": bool(cls.GEMINI_API_KEY),
                "owners_count": len(cls.OWNERS_CONFIG),
                "sheets_count": len(cls.SHEETS_CONFIG)
            }
        }
    
    @classmethod
    def get_environment_info(cls) -> Dict[str, Any]:
        """Información del entorno actual"""
        return {
            "project": cls.PROJECT_NAME,
            "version": cls.VERSION,
            "environment": cls.ENVIRONMENT,
            "debug": cls.DEBUG,
            "host": cls.HOST,
            "port": cls.PORT,
            "base_dir": str(cls.BASE_DIR),
            "frontend_dir": str(cls.FRONTEND_DIR)
        }

# Instancia global de configuración
settings = HomologatedConfig()

# Validar configuración al importar
config_validation = settings.validate_config()
if not config_validation["valid"]:
    print("⚠️ ADVERTENCIA: Problemas de configuración detectados:")
    for issue in config_validation["issues"]:
        print(f"  ❌ {issue}")
    
if config_validation["warnings"]:
    print("ℹ️ Advertencias de configuración:")
    for warning in config_validation["warnings"]:
        print(f"  ⚠️ {warning}")

# Exportar configuración para uso en otros módulos
__all__ = ["settings", "HomologatedConfig"]

"""
Sistema de Logging Unificado - Red Soluciones ISP
Configuración consolidada para logging del sistema
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

class ColoredFormatter(logging.Formatter):
    """Formatter con colores para terminal"""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        record.levelname = f"{color}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)

# Configurar directorio de logs
log_dir = Path(__file__).parent.parent.parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

# Configurar nivel de logging desde environment
log_level = os.getenv("LOG_LEVEL", "INFO").upper()

# Configurar formato de logs
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'

# Configurar handlers
handlers: list = [
    logging.FileHandler(log_dir / f"redsol_{datetime.now().strftime('%Y%m%d')}.log"),
]

# Agregar handler de consola con colores si estamos en desarrollo
if os.getenv("ENVIRONMENT", "development") == "development":
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColoredFormatter(log_format))
    handlers.append(console_handler)
else:
    handlers.append(logging.StreamHandler())

# Configurar logger principal
logging.basicConfig(
    level=getattr(logging, log_level),
    format=log_format,
    datefmt=date_format,
    handlers=handlers,
    force=True
)

# Crear logger global
logger = logging.getLogger("RedSolucionesISP")

def get_logger(name: str):
    """Obtiene un logger configurado para el módulo especificado"""
    return logging.getLogger(name)

from typing import Optional

def log_api_usage(logger, api_name: str, endpoint: str, user_action: Optional[str] = None):
    """Registra uso de APIs externas"""
    message = f"API_USAGE - {api_name} - {endpoint}"
    if user_action:
        message += f" - Triggered by: {user_action}"
    logger.info(message)

def log_user_action(logger, action: str, details: Optional[str] = None):
    """Registra acciones del usuario"""
    message = f"USER_ACTION - {action}"
    if details:
        message += f" - {details}"
    logger.info(message)

def log_agent_action(logger, action: str, success: bool, details: Optional[str] = None):
    """Registra acciones del agente"""
    status = "SUCCESS" if success else "FAILED"
    message = f"AGENT_ACTION - {action} - {status}"
    if details:
        message += f" - {details}"
    logger.info(message)

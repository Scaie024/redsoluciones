import logging
import os
from datetime import datetime
from pathlib import Path

# Configurar directorio de logs
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)

# Configurar formato de logs
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'

# Configurar logger principal
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.FileHandler(log_dir / f"redsol_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
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

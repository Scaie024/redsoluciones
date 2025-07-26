"""
Sistema de Logging Optimizado - Red Soluciones ISP
Configuración mejorada para mejor debugging y monitoreo
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Configurar directorio de logs
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)

# Configurar nivel de logging desde environment
log_level = os.getenv("LOG_LEVEL", "INFO").upper()

class ColoredFormatter(logging.Formatter):
    """Formatter con colores para consola"""
    
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green  
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        record.levelname = f"{color}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)

def setup_logging():
    """Configura sistema de logging optimizado"""
    
    # Formato detallado
    detailed_format = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    console_format = '%(levelname)s - %(name)s - %(message)s'
    
    # Handler para archivo
    file_handler = logging.FileHandler(
        log_dir / f"redsol_{datetime.now().strftime('%Y%m%d')}.log",
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(detailed_format))
    
    # Handler para consola con colores
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level))
    console_handler.setFormatter(ColoredFormatter(console_format))
    
    # Configurar logger root
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Silenciar logs verbosos de terceros
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("google").setLevel(logging.WARNING)
    
    return logging.getLogger("RedSolucionesISP")

def get_logger(name: str) -> logging.Logger:
    """Obtiene logger configurado"""
    return logging.getLogger(name)

# Configurar automáticamente
main_logger = setup_logging()

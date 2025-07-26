"""
Configuración Principal - Red Soluciones ISP
"""
import os
from pathlib import Path
from .config_unified import Settings

# Importar configuración unificada
settings = Settings()

# Exportar configuración principal
__all__ = ["settings"]
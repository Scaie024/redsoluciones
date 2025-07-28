"""
Sistema de Autenticación Simple - Red Soluciones ISP
Solo para propietarios autorizados, sin contraseñas
"""

import secrets
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class UserAuth:
    """Sistema de autenticación simple para propietarios"""
    
    def __init__(self):
        self.sessions = {}
        # Propietarios autorizados - solo nombres
        self.owners = {
            "carlos": {
                "name": "Carlos - Propietario Principal",
                "role": "owner",
                "permissions": ["all"]
            },
            "admin": {
                "name": "Administrador del Sistema",
                "role": "admin", 
                "permissions": ["all"]
            },
            "propietario": {
                "name": "Propietario Autorizado",
                "role": "owner",
                "permissions": ["all"]
            }
        }
    
    def authenticate_owner(self, owner_name: str) -> Optional[Dict[str, Any]]:
        """Autentica propietario autorizado"""
        try:
            owner_name = owner_name.lower().strip()
            owner = self.owners.get(owner_name)
            
            if owner:
                session_id = secrets.token_urlsafe(32)
                self.sessions[session_id] = {
                    "owner_name": owner_name,
                    "role": owner["role"],
                    "name": owner["name"],
                    "permissions": owner["permissions"],
                    "expires": datetime.now() + timedelta(hours=12),
                    "created": datetime.now()
                }
                logger.info(f"Propietario autenticado: {owner['name']}")
                return {
                    "session_id": session_id,
                    "owner": owner,
                    "success": True
                }
            return None
        except Exception as e:
            logger.error(f"Error en autenticación: {e}")
            return None
    
    def validate_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Valida sesión activa"""
        session = self.sessions.get(session_id)
        if session and session["expires"] > datetime.now():
            return session
        return None
    
    def logout(self, session_id: str) -> bool:
        """Cierra sesión"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

# Instancia global
user_auth = UserAuth()

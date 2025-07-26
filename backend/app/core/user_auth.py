"""
Sistema de Autenticación Básico - Red Soluciones ISP
Implementación simple y segura para el sistema
"""

import hashlib
import secrets
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class UserAuth:
    """Sistema de autenticación básico"""
    
    def __init__(self):
        self.sessions = {}
        self.users = {
            "admin": {
                "password_hash": self._hash_password("admin123"),
                "role": "admin",
                "name": "Administrador"
            },
            "operador": {
                "password_hash": self._hash_password("op123"),
                "role": "operator", 
                "name": "Operador"
            }
        }
    
    def _hash_password(self, password: str) -> str:
        """Hash seguro de contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Autentica usuario"""
        try:
            user = self.users.get(username)
            if user and user["password_hash"] == self._hash_password(password):
                session_id = secrets.token_urlsafe(32)
                self.sessions[session_id] = {
                    "username": username,
                    "role": user["role"],
                    "name": user["name"],
                    "expires": datetime.now() + timedelta(hours=8)
                }
                logger.info(f"Usuario autenticado: {username}")
                return {
                    "session_id": session_id,
                    "user": user,
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

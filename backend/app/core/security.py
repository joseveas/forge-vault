from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth
import logging

logger = logging.getLogger(__name__)

security_scheme = HTTPBearer()

def get_current_user_uid(creds: HTTPAuthorizationCredentials = Depends(security_scheme)) -> str:
    token = creds.credentials
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        return uid
    except Exception as e:
        logger.error(f"Error de autenticación: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas o expiradas",
            headers={"WWW-Authenticate": "Bearer"},
        )
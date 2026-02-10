import firebase_admin
from firebase_admin import credentials, firestore
from app.core.config import settings
import logging

logger = logging.getLogger("ForgeVault.Database")

def get_db_client():
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
            logger.info(f"Firebase initialized successfully using: {settings.FIREBASE_CREDENTIALS_PATH}")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {str(e)}")
            raise e

    return firestore.client()

db = get_db_client()
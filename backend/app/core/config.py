import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ForgeVault.Config")

load_dotenv()

class Settings:
    PROJECT_NAME: str = "ForgeVault"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    @property
    def FIREBASE_CREDENTIALS_PATH(self) -> str:
        if os.path.exists("/etc/secrets/serviceAccountKey.json"):
            return "/etc/secrets/serviceAccountKey.json"
        
        if os.getenv("FIREBASE_CREDENTIALS_PATH"):
            return os.getenv("FIREBASE_CREDENTIALS_PATH")

        return "serviceAccountKey.json"

    def __init__(self):
        if not self.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY not found. AI features will be disabled.")
        
        if not os.path.exists(self.FIREBASE_CREDENTIALS_PATH):
            logger.critical(f"Firebase credentials file not found at: {self.FIREBASE_CREDENTIALS_PATH}")
            logger.critical("Application will fail to connect to Database.")

settings = Settings()
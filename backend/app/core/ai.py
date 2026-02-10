from google import genai
from app.core.config import settings
import logging

logger = logging.getLogger("ForgeVault.AI")

ai_client = None

try:
    if settings.GEMINI_API_KEY:
        ai_client = genai.Client(api_key=settings.GEMINI_API_KEY)
        logger.info("Gemini AI Client initialized successfully.")
    else:
        logger.warning("AI Client not initialized: Missing API Key.")

except Exception as e:
    logger.error(f"Failed to initialize AI Client: {str(e)}")
    ai_client = None
from fastapi import FastAPI
from app.core.config import settings
from app.core.database import db
from app.core.ai import ai_client

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.get("/health")
def health_check():
    return {
        "status": "online",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database": "connected" if db else "error",
        "ai": "ready" if ai_client else "disabled"
    }
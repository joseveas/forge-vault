from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.health import FoodItem, DailyLogResponse, BiometricsCreate, BiometricsResponse, HealthDashboardResponse
from app.services.health import health_service
from app.services.ai import intelligence_service
from app.routers.user import get_current_user_id

router = APIRouter(prefix="/health", tags=["Health"])

@router.post("/nutrition/parse", response_model=List[FoodItem])
def parse_meal_text(text: str, user_id: str = Depends(get_current_user_id)):
    pass

@router.post("/nutrition/log", response_model=DailyLogResponse)
def log_meal(items: List[FoodItem], user_id: str = Depends(get_current_user_id)):
    pass

@router.post("/biometrics", response_model=BiometricsResponse)
def record_biometrics(data: BiometricsCreate, user_id: str = Depends(get_current_user_id)):
    pass

@router.get("/dashboard", response_model=HealthDashboardResponse)
def get_dashboard(date: date, user_id: str = Depends(get_current_user_id)):
    pass

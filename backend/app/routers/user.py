from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserResponse, UserUpdate, FixedExpenseTemplate, FinanceConfig, HealthConfig
from app.services.user import user_service

router = APIRouter(prefix="/users", tags=["Users"])

def get_current_user_id(token: str = "user_123"): 
    return token 

@router.get("/me", response_model=UserResponse)
def get_current_user(user_id: str = Depends(get_current_user_id)):
    pass

@router.patch("/me", response_model=UserResponse)
def update_profile(data: UserUpdate, user_id: str = Depends(get_current_user_id)):
    pass

@router.post("/me/config/budget", response_model=UserResponse)
def set_budget_config(income: float, expenses: List[FixedExpenseTemplate], user_id: str = Depends(get_current_user_id)):
    pass

@router.post("/me/config/targets", response_model=UserResponse)
def set_nutritional_targets(weight: float, body_fat: float, user_id: str = Depends(get_current_user_id)):
    pass
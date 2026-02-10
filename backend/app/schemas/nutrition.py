from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class FoodItem(BaseModel):
    name: str
    quantity_label: str = Field(..., description="Ej: '200g', '1 taza'") 
    calories: float = Field(..., ge=0)
    protein: float = Field(..., ge=0)
    carbs: float = Field(..., ge=0)
    fat: float = Field(..., ge=0)

class DailyLogBase(BaseModel):
    date: datetime = Field(default_factory=datetime.now)
    items: List[FoodItem]
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float

class DailyLogCreate(DailyLogBase):
    pass

class DailyLogResponse(DailyLogBase):
    id: str
    user_id: str

    class Config:
        from_attributes = True
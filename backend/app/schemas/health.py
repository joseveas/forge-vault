from pydantic import BaseModel, Field
from datetime import date as dt_date
from typing import Optional, List

class BiometricsBase(BaseModel):
    weight_kg: float = Field(..., gt=0, description="Peso en kg")
    waist_cm: float = Field(..., gt=0, description="Cintura en cm")
    neck_cm: float = Field(..., gt=0, description="Cuello en cm")
    notes: Optional[str] = None

class BiometricsCreate(BiometricsBase):
    date: dt_date = Field(default_factory=dt_date.today)

class BiometricsUpdate(BaseModel):
    weight_kg: Optional[float] = None
    waist_cm: Optional[float] = None
    neck_cm: Optional[float] = None
    notes: Optional[str] = None

class BiometricsResponse(BiometricsBase):
    id: str
    user_id: str
    date: dt_date
    body_fat_pct: Optional[float] = Field(None, description="Calculado Navy Method")
    lean_mass_kg: Optional[float] = None
    fat_mass_kg: Optional[float] = None

    class Config:
        from_attributes = True

class MacroStatus(BaseModel):
    protein_consumed: float = Field(..., ge=0)
    protein_goal: float = Field(..., ge=0)
    carbs_consumed: float = Field(..., ge=0)
    carbs_goal: float = Field(..., ge=0)
    fat_consumed: float = Field(..., ge=0)
    fat_goal: float = Field(..., ge=0)
    calories_remaining: float = Field(..., ge=0)

class HealthDashboardResponse(BaseModel): 
    today_macros: MacroStatus
    current_weight: float
    total_weight_lost: float
    weekly_avg_calories: float
    days_in_deficit_streak: int
    body_fat_pct: Optional[float] = None

class FoodItem(BaseModel):
    name: str
    quantity_label: str = Field(..., description="Ej: '200g', '1 taza'") 
    calories: float = Field(..., ge=0)
    protein: float = Field(..., ge=0)
    carbs: float = Field(..., ge=0)
    fat: float = Field(..., ge=0)

class DailyLogBase(BaseModel):
    date: dt_date = Field(default_factory=dt_date.today)
    items: List[FoodItem]
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float

class DailyLogCreate(DailyLogBase):
    pass

class DailyLogUpdate(BaseModel):
    items: Optional[List[FoodItem]] = None
    total_calories: Optional[float] = None
    total_protein: Optional[float] = None
    total_carbs: Optional[float] = None
    total_fat: Optional[float] = None

class DailyLogResponse(DailyLogBase):
    id: str
    user_id: str

    class Config:
        from_attributes = True


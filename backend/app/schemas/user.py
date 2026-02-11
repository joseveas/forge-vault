from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class MacroSplit(BaseModel):
    protein_grams: float
    carbs_grams: float
    fat_grams: float

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    height_cm: float = Field(..., gt=0, description="Altura en cm")
    age: int = Field(..., gt=0)
    activity_level: float = Field(1.2, description="Factor actividad (1.2 - 2.0)")
    tdee_goal: Optional[float] = Field(None, description="Meta calórica diaria")
    monthly_budget: Optional[float] = Field(None, description="Presupuesto mensual líquido")
    macro_split: Optional[MacroSplit] = None

class UserCreate(UserBase):
    firebase_uid: str

class UserUpdate(UserBase):
    full_name: Optional[str] = None
    height_cm: Optional[float] = None
    age: Optional[int] = None
    activity_level: Optional[float] = None
    tdee_goal: Optional[float] = None
    monthly_budget: Optional[float] = None
    macro_split: Optional[MacroSplit] = None

class UserResponse(UserBase):
    id: str = Field(..., alias="firebase_uid")
    user_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True

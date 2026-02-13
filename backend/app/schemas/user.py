from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.enums.finance import FinanceCategory
from app.enums.user import ActivityLevel, GoalStrategy

class FixedExpenseTemplate(BaseModel):
    name: str = Field(..., description="Ej: Arriendo, Netflix")
    amount: float = Field(..., gt=0)
    category: FinanceCategory

class MacroSplit(BaseModel):
    protein_grams: float
    carbs_grams: float
    fat_grams: float

class FinanceConfig(BaseModel):
    monthly_income: Optional[float] = Field(None, description="Sueldo Líquido")
    fixed_expenses: List[FixedExpenseTemplate] = []
    monthly_budget: Optional[float] = Field(None, description="Disponible Calculado")

class HealthConfig(BaseModel):
    height_cm: float = Field(..., gt=0)
    current_weight: Optional[float] = None
    current_body_fat: Optional[float] = None
    activity_level: ActivityLevel = ActivityLevel.SEDENTARY
    goal_strategy: GoalStrategy = GoalStrategy.AGGRESSIVE_CUT 
    tdee_goal: Optional[float] = None
    macro_split: Optional[MacroSplit] = None

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    age: int = Field(..., gt=0)
    finance: FinanceConfig = Field(default_factory=FinanceConfig)
    health: HealthConfig

class UserCreate(UserBase):
    firebase_uid: str

class UserUpdate(UserBase):
    full_name: Optional[str] = None
    age: Optional[int] = None
    finance: Optional[FinanceConfig] = None
    health: Optional[HealthConfig] = None

class UserResponse(UserBase):
    id: str = Field(..., alias="firebase_uid")
    user_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True

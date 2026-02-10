from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BiometricsBase(BaseModel):
    weight_kg: float = Field(..., gt=0, description="Peso en kg")
    waist_cm: float = Field(..., gt=0, description="Cintura en cm")
    neck_cm: float = Field(..., gt=0, description="Cuello en cm")
    notes: Optional[str] = None

class BiometricsCreate(BiometricsBase):
    date: datetime = Field(default_factory=datetime.now)

class BiometricsResponse(BiometricsBase):
    id: str
    user_id: str
    date: datetime
    body_fat_pct: Optional[float] = Field(None, description="Calculado Navy Method")
    lean_mass_kg: Optional[float] = None
    fat_mass_kg: Optional[float] = None

    class Config:
        from_attributes = True
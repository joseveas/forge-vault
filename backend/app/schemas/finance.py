from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from app.enums.finance import TransactionCategory, TransactionType, PaymentMethod

class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0)
    category: TransactionCategory
    description: str = Field(..., min_length=1)
    date: date
    type: TransactionType
    method: PaymentMethod
    is_fixed: bool = False

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    category: Optional[TransactionCategory] = None
    description: Optional[str] = None
    is_fixed: Optional[bool] = None

class TransactionResponse(TransactionBase):
    id: str
    user_id: str
    created_at: Optional[date] = None

    class Config:
        from_attributes = True
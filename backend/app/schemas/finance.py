from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List
from app.enums.finance import TransactionCategory, TransactionType, PaymentMethod, FinancialHealthStatus

class CategorySpending(BaseModel):
    category: TransactionCategory
    amount: float = Field(..., gt=0)
    percentage: float = Field(..., gt=0)

class MonthlyDashboardResponse(BaseModel):
    current_month_total: float = Field(..., gt=0)
    budget_status: FinancialHealthStatus
    burn_rate_daily: float = Field(..., gt=0)
    projected_savings: float
    top_expenses: List[CategorySpending] = Field(..., min_items=0)
    remaining_budget: float

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
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
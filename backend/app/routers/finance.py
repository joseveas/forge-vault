from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.finance import TransactionCreate, TransactionResponse, MonthlyDashboardResponse
from app.services.finance import finance_service
from app.services.ai import intelligence_service
from app.routers.user import get_current_user_id # Reusamos la dependencia de auth

router = APIRouter(prefix="/finance", tags=["Finance"])

@router.post("/transactions/parse", response_model=TransactionCreate)
def parse_transaction_text(text: str, user_id: str = Depends(get_current_user_id)):
    pass

@router.post("/transactions", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, user_id: str = Depends(get_current_user_id)):
    pass

@router.get("/dashboard", response_model=MonthlyDashboardResponse)
def get_dashboard(month: date, user_id: str = Depends(get_current_user_id)):
    pass

@router.delete("/transactions/{tx_id}")
def delete_transaction(tx_id: str, user_id: str = Depends(get_current_user_id)):
    pass
from datetime import date
import calendar 
from typing import Dict, Any, List, Tuple

from app.repositories.finance import finance_repository
from app.repositories.user import user_repository
from app.schemas.finance import TransactionCreate, TransactionResponse
from app.enums.finance import TransactionType, FinanceCategory

class FinanceService:
    def __init__(self):
        self.repo = finance_repository
        self.user_repo = user_repository
    
    def create_transaction(self, user_id: str, transaction_in: TransactionCreate) -> TransactionResponse:
        return self.repo.create(transaction_in, user_id=user_id)
    
    def delete_transaction(self, doc_id: str) -> bool:
        return self.repo.delete(doc_id)
    
    def get_monthly_dashboard(self, user_id: str, month: int = None, year: int = None) -> Dict[str, Any]:
        start_date, end_date = self._get_month_range(month, year)
        transactions = self.repo.get_by_date_range(user_id, start_date, end_date)
        income, expenses, breakdown = self._process_transactions(transactions)
        balance = income - expenses
        target_month = start_date.month
        target_year = start_date.year
        burn_rate, days_left = self._calculate_burn_rate(balance, target_month, target_year)

        return {
            "period": f"{target_year}-{target_month:02d}",
            "summary": {
                "income": income,
                "expenses": expenses,
                "balance": balance,
            },
            "kpis": {
                "daily_burn_rate": burn_rate,
                "days_remaining": days_left
            },
            "category_breakdown": breakdown,
            "transactions": transactions
        }

    def _get_month_range(self, month: int | None, year: int | None) -> Tuple[date, date]:
        today = date.today()
        target_month = month if month else today.month
        target_year = year if year else today.year

        _, last_day = calendar.monthrange(target_year, target_month)
        return date(target_year, target_month, 1), date(target_year, target_month, last_day)

    def _process_transactions(self, transactions: List[TransactionResponse]) -> Tuple[float, float, Dict[str, float]]:
        total_income = 0.0
        total_expense = 0.0
        breakdown: Dict[str, float] = {}

        for t in transactions:
            if t.type == TransactionType.INCOME:
                total_income += t.amount
            elif t.type == TransactionType.EXPENSE:
                total_expense += t.amount
                cat_name = t.category.value if t.category else "otros"
                breakdown[cat_name] = breakdown.get(cat_name, 0.0) + t.amount
        
        return total_income, total_expense, breakdown

    def _calculate_burn_rate(self, balance: float, month: int, year: int) -> Tuple[float, int]:
        today = date.today()
        is_current_month = (month == today.month and year == today.year)
        
        if not is_current_month:
            return 0.0, 0

        _, last_day = calendar.monthrange(year, month)
        days_remaining = last_day - today.day

        if balance > 0 and days_remaining > 0:
            return round(balance / days_remaining, 0), days_remaining
        
        return 0.0, days_remaining

    def get_constants(self) -> Dict[str, List[str]]:
        return {
            "types": [t.value for t in TransactionType],
            "categories": [c.value for c in FinanceCategory]
        }

finance_service = FinanceService()
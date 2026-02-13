from typing import List
from datetime import date
from app.repositories.base import FirestoreRepository
from app.schemas.finance import TransactionResponse, TransactionCreate, TransactionUpdate

class FinanceRepository(FirestoreRepository[TransactionResponse, TransactionCreate, TransactionUpdate]):
    def __init__(self):
        super().__init__(collection_name="transactions", model=TransactionResponse)

    def get_by_date_range(self, user_id: str, start_date: date, end_date: date) -> List[TransactionResponse]:
        start_str = start_date.isoformat()
        end_str = end_date.isoformat()

        docs = self.db.collection(self.collection_name)\
            .where("user_id", "==", user_id)\
            .where("date", ">=", start_str)\
            .where("date", "<=", end_str)\
            .stream()

        return [self._map_to_model(doc) for doc in docs]

finance_repository = FinanceRepository()
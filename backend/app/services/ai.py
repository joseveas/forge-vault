# class IntelligenceService {
#             <<External>>
#             +api_key:str
#             +__init__(api_key:str)
#             +parse_transaction(text:str) TransactionCreate
#             +parse_food_entry(text:str) List~FoodItem~
#         }

from typing import List, Optional
from app.core.config import settings
from app.schemas.finance import TransactionCreate
from app.schemas.health import FoodItem

class IntelligenceService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
    
    def parse_transaction(self, text: str) -> TransactionCreate:
        pass
    
    def parse_food_entry(self, text: str) -> List[FoodItem]:
        pass

intelligence_service = IntelligenceService()
from typing import List, Optional
from app.repositories.user import user_repository
from app.schemas.user import UserCreate, UserUpdate, UserResponse, FinanceConfig, HealthConfig, MacroSplit, FixedExpenseTemplate
from app.enums.user import ActivityLevel, GoalStrategy

class UserService:
    def __init__(self):
        self.repo = user_repository
    
    def get_user(self, user_id: str) -> UserResponse | None:
        return self.repo.get(user_id)
    
    def create_user(self, user_in: UserCreate) -> UserResponse:
        firebase_uid = user_in.firebase_uid
        return self.repo.create(user_in, user_id=firebase_uid, custom_id=firebase_uid)

    def update_user(self, user_id: str, user: UserUpdate) -> UserResponse:
        return self.repo.update(user_id, user)
    
    def configure_budget(self, user_id: str, new_income: Optional[float] = None, new_expenses: Optional[List[FixedExpenseTemplate]] = None) -> UserResponse:
        pass

    def update_nutritional_targets(self, user_id: str, current_weight: float, current_body_fat: float = None) -> UserResponse:
        pass

    def _calculate_tdee(self, weight_kg: float, height_cm: float, age: int, activity_level: ActivityLevel) -> float:
        pass

user_service = UserService()
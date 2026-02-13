from typing import List, Optional
from app.repositories.user import user_repository
from app.schemas.user import UserCreate, UserUpdate, UserResponse, FinanceConfig, HealthConfig, MacroSplit, FixedExpenseTemplate
from app.enums.user import ActivityLevel, GoalStrategy

class UserService:
    def __init__(self):
        self.repo = user_repository
    
    def get_user(self, user_id: str) -> UserResponse | None:
        return self.repo.get(user_id)

    def calculate_tdee(self, weight_kg: float, height_cm: float, age: int, activity_level: ActivityLevel) -> float:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        tdee = bmr * activity_level.multiplier 
        return round(tdee, 2)
    
    def create_user(self, user_in: UserCreate) -> UserResponse:
        firebase_uid = user_in.firebase_uid
        return self.repo.create(user_in, user_id=firebase_uid, custom_id=firebase_uid)

    def configure_budget(self, user_id: str, new_income: Optional[float] = None, new_expenses: Optional[List[FixedExpenseTemplate]] = None) -> UserResponse:
        user = self.repo.get(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")

        current_finance = user.finance if user.finance else FinanceConfig()

        final_income = new_income if new_income is not None else current_finance.monthly_income
        final_expenses = new_expenses if new_expenses is not None else current_finance.fixed_expenses

        if final_income is None:
            updated_finance = FinanceConfig(fixed_expenses=final_expenses)
            return self.repo.update(user_id, UserUpdate(finance=updated_finance))

        total_fixed = sum(e.amount for e in final_expenses)
        disposable_budget = final_income - total_fixed

        new_finance_config = FinanceConfig(
            monthly_income=final_income,
            fixed_expenses=final_expenses,
            monthly_budget=round(disposable_budget, 0)
        )

        return self.repo.update(user_id, UserUpdate(finance=new_finance_config))
    
    def update_nutritional_targets(self, user_id: str, current_weight: float, current_body_fat: float = None) -> UserResponse:
        user = self.repo.get(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        
        h_config = user.health
        strategy = h_config.goal_strategy
        tdee = self.calculate_tdee(current_weight, h_config.height_cm, user.age, h_config.activity_level)
        target_calories = max(1200, tdee + strategy.calorie_offset)
        final_bf = current_body_fat if current_body_fat is not None else h_config.current_body_fat
        protein_factor = strategy.protein_factor
        
        if final_bf:
            lean_mass_kg = current_weight * (1 - (final_bf / 100))
            protein_grams = round(lean_mass_kg * protein_factor, 1) 
        else:
            protein_grams = round(current_weight * (protein_factor * 0.8), 1)

        fat_cals = target_calories * 0.30
        fat_grams = round(fat_cals / 9, 1)
        
        prot_cals = protein_grams * 4
        remaining_cals = target_calories - (prot_cals + fat_cals)
        if remaining_cals < 0: remaining_cals = 0
        carbs_grams = round(remaining_cals / 4, 1)

        new_health_config = HealthConfig(
            height_cm=h_config.height_cm,
            activity_level=h_config.activity_level,
            goal_strategy=strategy,
            current_weight=current_weight,
            current_body_fat=final_bf,
            tdee_goal=round(target_calories, 0),
            macro_split=MacroSplit(protein_grams=protein_grams, fat_grams=fat_grams, carbs_grams=carbs_grams)
        )

        return self.repo.update(user_id, UserUpdate(health=new_health_config))

user_service = UserService()
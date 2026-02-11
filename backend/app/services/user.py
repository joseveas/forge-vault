from app.repositories.user import user_repository
from app.schemas.user import UserCreate, UserUpdate, UserResponse, MacroSplit

class UserService:
    def __init__(self):
        self.repo = user_repository
    
    def get_user(self, user_id: str) -> UserResponse | None:
        return self.repo.get(user_id)

    def calculate_tdee(self, weight_kg: float, height_cm: float, age: int, activity_level: float) -> float:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        tdee = bmr * activity_level
        return round(tdee, 2)
    
    def create_user(self, user_in: UserCreate) -> UserResponse:
        firebase_uid = user_in.firebase_uid
        return self.repo.create(user_in, user_id=firebase_uid, custom_id=firebase_uid)
    
    def update_nutritional_targets(self, user_id: str, current_weight: float) -> UserResponse:
        user = self.repo.get(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        tdee = self.calculate_tdee(current_weight, user.height_cm, user.age, user.activity_level)
        target_calories = tdee - 1000
        if target_calories < 1200:
            target_calories = 1200
        protein_grams = round(current_weight * 1.5, 1)
        protein_cals = protein_grams * 4
        fat_cals = target_calories * 0.30
        fat_grams = round(fat_cals / 9, 1)
        remaining_cals = target_calories - (protein_cals + fat_cals)
        if remaining_cals < 0:
            remaining_cals = 0
        carbs_grams = round(remaining_cals / 4, 1)
        new_split = MacroSplit(
            protein_grams=protein_grams,
            fat_grams=fat_grams,
            carbs_grams=carbs_grams
        )
        update_data = UserUpdate(
            tdee_goal=round(target_calories, 0),
            macro_split=new_split
        )
        return self.repo.update(user_id, update_data)

user_service = UserService()
from app.repositories.repository import FirestoreRepository
from app.schemas.health import DailyLogResponse, BiometricsResponse, DailyLogCreate, BiometricsCreate, DailyLogUpdate, BiometricsUpdate

class NutritionRepository (FirestoreRepository[DailyLogResponse, DailyLogCreate, DailyLogUpdate]):
            def __init__(self):
                super().__init__(collection_name="nutrition", model=DailyLogResponse)

            def get_by_date_range(user_id: str, start: date, end: date) -> List[DailyLogResponse]:
                start_str = start.isoformat()
                end_str = end.isoformat()

                docs = self.db.collection(self.collection_name)\
                    .where("user_id", "==", user_id)\
                    .where("date", ">=", start_str)\
                    .where("date", "<=", end_str)\
                    .stream()

                return [self._map_to_model(doc) for doc in docs]


class BiometricsRepository (FirestoreRepository[BiometricsResponse, BiometricsCreate, BiometricsUpdate]):
            def __init__(self):
                super().__init__(collection_name="biometrics", model=BiometricsResponse)

            def get_latest(user_id: str) -> Optional[BiometricsResponse]:
                docs = self.db.collection(self.collection_name)\
                    .where("user_id", "==", user_id)\
                    .order_by("date", direction="DESCENDING")\
                    .limit(1)\
                    .stream()

                return [self._map_to_model(doc) for doc in docs]

            def get_history(user_id: str, start: date, end: date) -> List[BiometricsResponse]:
                start_str = start.isoformat()
                end_str = end.isoformat()

                docs = self.db.collection(self.collection_name)\
                    .where("user_id", "==", user_id)\
                    .where("date", ">=", start_str)\
                    .where("date", "<=", end_str)\
                    .stream()

                return [self._map_to_model(doc) for doc in docs]

nutrition_repository = NutritionRepository()
biometrics_repository = BiometricsRepository()
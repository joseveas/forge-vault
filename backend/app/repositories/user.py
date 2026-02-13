from app.repositories.repository import FirestoreRepository
from app.schemas.user import UserResponse, UserCreate, UserUpdate

class UserRepository(FirestoreRepository[UserResponse, UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__(collection_name="users", model=UserResponse)

user_repository = UserRepository()
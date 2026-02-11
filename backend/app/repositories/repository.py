from typing import Generic, List, Optional, Type, TypeVar
from google.cloud.firestore_v1.client import Client
from google.cloud.firestore_v1 import DocumentSnapshot
from pydantic import BaseModel
from app.core.database import db

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class FirestoreRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, collection_name: str, model: Type[ModelType]):
        self.collection_name = collection_name
        self.model = model
        self.db: Client = db
    
    def get(self, doc_id: str) -> Optional[ModelType]:
        doc_ref = self.db.collection(self.collection_name).document(doc_id)
        doc = doc_ref.get()
        if doc.exists:
            return self._map_to_model(doc)
        return None
    
    def get_all_by_user(self, user_id: str) -> List[ModelType]:
        docs = self.db.collection(self.collection_name)\
            .where("user_id", "==", user_id)\
            .stream()
        return [self._map_to_model(doc) for doc in docs]
    
    def create(self, obj_in: CreateSchemaType, user_id: str, custom_id: str = None) -> ModelType:
        obj_data = obj_in.model_dump()
        obj_data["user_id"] = user_id
        if hasattr(obj_in, "created_at") and obj_in.created_at:
             obj_data["created_at"] = obj_in.created_at
        collection_ref = self.db.collection(self.collection_name)
        if custom_id:
            doc_ref = collection_ref.document(custom_id)
            doc_ref.set(obj_data)
            doc_id = custom_id
        else:
            _, doc_ref = collection_ref.add(obj_data)
            doc_id = doc_ref.id
        return self.model(id=doc_id, **obj_data)
    
    def update(self, doc_id: str, obj_in: UpdateSchemaType) -> Optional[ModelType]:
        doc_ref = self.db.collection(self.collection_name).document(doc_id)
        update_data = obj_in.model_dump(exclude_unset=True)        
        if not update_data:
            return self.get(doc_id)
        doc_ref.update(update_data)
        return self.get(doc_id)

    def delete(self, doc_id: str) -> bool:
        self.db.collection(self.collection_name).document(doc_id).delete()
        return True

    def _map_to_model(self, doc: DocumentSnapshot) -> ModelType:
        data = doc.to_dict()
        return self.model(id=doc.id, **data)
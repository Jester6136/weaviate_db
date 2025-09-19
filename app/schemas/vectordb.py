from pydantic import BaseModel
from typing import List, Dict, Optional

# Pydantic models for request validation
class CollectionCreate(BaseModel):
    collection_name: str
    vectorizer: str = "text2vec-model2vec"
    properties: Optional[List[Dict]] = None

class DataInsert(BaseModel):
    collection_name: str
    data_objects: List[Dict]

class QueryRequest(BaseModel):
    collection_name: str
    query: str
    limit: int = 10
    with_vectors: bool = False

class UpdateRequest(BaseModel):
    collection_name: str
    object_id: str
    data_object: Dict

class DeleteRequest(BaseModel):
    collection_name: str
    object_id: str

class HybridSearchRequest(BaseModel):
    collection_name: str
    query: str
    alpha: float = 0.5
    limit: int = 10

class CollectionStatsRequest(BaseModel):
    collection_name: str
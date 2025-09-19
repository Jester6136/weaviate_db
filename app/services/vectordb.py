from typing import Dict
from app.schemas.vectordb import CollectionCreate, CollectionStatsRequest, DataInsert, DeleteRequest, HybridSearchRequest, QueryRequest, UpdateRequest
from src.weaviate_db import WeaviateDB
import os

# Initialize WeaviateDB client
db = WeaviateDB(host=os.getenv("WEAVIATE_HOST"), grpc_port=os.getenv("WEAVIATE_GRPC_PORT"), api_key=os.getenv("WEAVIATE_API_KEY"))

def create_collection(request: CollectionCreate):
    success = db.create_collection(
        collection_name=request.collection_name,
        vectorizer=request.vectorizer,
        properties=request.properties
    )
    return success

def insert_data(request: DataInsert):
    inserted_count = db.insert_data(
        collection_name=request.collection_name,
        data_objects=request.data_objects
    )
    if inserted_count == 0:
        raise Exception("No data was inserted.")
    return inserted_count

def query_data(request: QueryRequest):
    results = db.query_data(
        collection_name=request.collection_name,
        query=request.query,
        limit=request.limit,
        with_vectors=request.with_vectors
    )
    return results

def update_data(request: UpdateRequest):
    success = db.update_data(
        collection_name=request.collection_name,
        object_id=request.object_id,
        data_object=request.data_object
    )
    if not success:
        raise Exception(f"Failed to update object {request.object_id}")
    return success

def delete_data(request: DeleteRequest):
    success = db.delete_data(
        collection_name=request.collection_name,
        object_id=request.object_id
    )
    if not success:
        raise Exception(f"Failed to delete object {request.object_id}")
    return success

def delete_collection(request: CollectionStatsRequest):
    success = db.delete_collection(collection_name=request.collection_name)
    if not success:
        raise Exception(f"Failed to delete collection {request.collection_name}")
    return success

def hybrid_search(request: HybridSearchRequest):
    results = db.hybrid_search(
        collection_name=request.collection_name,
        query=request.query,
        alpha=request.alpha,
        limit=request.limit
    )
    return results

async def get_collection_stats(collection_name: str):
    stats = db.get_collection_stats(collection_name=collection_name)
    return stats

def close_connection():
    db.close()
    return True

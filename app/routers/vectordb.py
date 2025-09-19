from fastapi import APIRouter, FastAPI, HTTPException
from typing import List, Dict, Optional
from src.config.config import get_logger
logger = get_logger()

from app.schemas.vectordb import CollectionCreate, CollectionStatsRequest, DataInsert, DeleteRequest, HybridSearchRequest, QueryRequest, UpdateRequest
from app.services.vectordb import (create_collection as create_collection_service,
        insert_data as insert_data_service,
        query_data as query_data_service,
        update_data as update_data_service,
        delete_data as delete_data_service,
        delete_collection as delete_collection_service,
        hybrid_search as hybrid_search_service,
        get_collection_stats as get_collection_stats_service,
        close_connection as close_connection_service)


router = APIRouter(
    prefix="",
    tags=["Weaviate IO Handler"],
)

@router.post("/collection/create", response_model=bool)
async def create_collection(request: CollectionCreate):
    """
    Create a new collection in Weaviate.
    """
    return create_collection_service(
        collection_name=request.collection_name,
        vectorizer=request.vectorizer,
        properties=request.properties
    )

@router.post("/data/insert", response_model=int)
async def insert_data(request: DataInsert):
    """
    Insert data objects into a collection.
    """
    return insert_data_service(
            collection_name=request.collection_name,
            data_objects=request.data_objects
        )

@router.post("/data/query", response_model=List[Dict])
async def query_data(request: QueryRequest):
    """
    Query data from a collection using near-text search.
    """
    return query_data_service(
        collection_name=request.collection_name,
        query=request.query,
        limit=request.limit,
        with_vectors=request.with_vectors
    )

@router.put("/data/update", response_model=bool)
async def update_data(request: UpdateRequest):
    """
    Update a data object in a collection.
    """
    return update_data_service(
        collection_name=request.collection_name,
        object_id=request.object_id,
        data_object=request.data_object
    )

@router.delete("/data/delete", response_model=bool)
async def delete_data(request: DeleteRequest):
    """
    Delete a data object from a collection.
    """
    return delete_data_service(
        collection_name=request.collection_name,
        object_id=request.object_id
    )

@router.delete("/collection/delete", response_model=bool)
async def delete_collection(request: CollectionStatsRequest):
    """
    Delete a collection from Weaviate.
    """
    return delete_collection_service(collection_name=request.collection_name)
        

@router.post("/data/hybrid-search", response_model=List[Dict])
async def hybrid_search(request: HybridSearchRequest):
    """
    Perform a hybrid search combining vector and keyword search.
    """
    return hybrid_search_service(
        collection_name=request.collection_name,
        query=request.query,
        alpha=request.alpha,
        limit=request.limit
    )
    
@router.get("/collection/stats", response_model=Dict)
async def get_collection_stats(collection_name: str):
    """
    Get statistics for a collection.
    """
    return get_collection_stats_service(collection_name=collection_name)

@router.post("/close", response_model=bool)
async def close_connection():
    """
    Close the Weaviate client connection.
    """
    return close_connection_service()

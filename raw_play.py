import os
from src.weaviate_db import WeaviateDB  # Assuming the previous WeaviateDB class is in weaviate_db.py
from src.config.config import get_logger
logger = get_logger()

if __name__ == "__main__":
    # Initialize WeaviateDB client
    db = WeaviateDB(host=os.getenv("WEAVIATE_HOST"), grpc_port=os.getenv("WEAVIATE_GRPC_PORT"), api_key=os.getenv("WEAVIATE_API_KEY"))
    
    # Example 1: Create a collection
    collection_name = "Articles"
    properties = [
        {"name": "title", "dataType": ["string"]},
        {"name": "content", "dataType": ["text"]}
    ]
    db.create_collection(collection_name, properties=properties)
    
    # Example 2: Insert data
    data_objects = [
        {"title": "First Article", "content": "This is the content of the first article."},
        {"title": "Second Article", "content": "This is another article about AI."}
    ]
    inserted_count = db.insert_data(collection_name, data_objects)
    print(f"Inserted {inserted_count} objects")
    
    # Example 3: Query data (near-text search)
    query_results = db.query_data(collection_name, query="AI article", limit=2, with_vectors=False)
    print("Query results:")
    for result in query_results:
        print(result)
    
    # Example 4: Update data
    object_id = str(query_results[0]["_id"]) if query_results else None
    if object_id:
        update_data = {"title": "Updated Article", "content": "Updated content about AI advancements."}
        success = db.update_data(collection_name, object_id, update_data)
        print(f"Update successful: {success}")
    
    # Example 5: Hybrid search
    hybrid_results = db.hybrid_search(collection_name, query="AI advancements", alpha=0.7, limit=2)
    print("Hybrid search results:")
    for result in hybrid_results:
        print(result)
    
    # Example 6: Get collection stats
    stats = db.get_collection_stats(collection_name)
    print("Collection stats:")
    print(stats)
    
    # Example 7: Delete data
    if object_id:
        success = db.delete_data(collection_name, object_id)
        print(f"Delete successful: {success}")
    
    # Example 8: Delete collection
    success = db.delete_collection(collection_name)
    print(f"Collection deletion successful: {success}")
    
    # Example 9: Close connection
    db.close()
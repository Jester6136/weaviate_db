import weaviate
import weaviate.classes as wvc
import uuid
from typing import List, Dict, Any, Optional


class WeaviateDB:
    def __init__(self, host, grpc_port, api_key: Optional[str] = None):
        """
        Initialize WeaviateDB client with connection settings (v4 style).
        """
        try:
            if api_key:
                self.client = weaviate.connect_to_weaviate_cloud(
                    cluster_url=host,
                    auth_credentials=weaviate.auth.AuthApiKey(api_key)
                )
            else:
                hostname = host.replace("http://", "").replace("https://", "").split(":")[0]
                port = int(host.split(":")[-1]) if ":" in host else 8080
                self.client = weaviate.connect_to_local(
                    host=hostname,
                    port=port,
                    grpc_port=grpc_port,
                )
        except Exception as e:
            raise

    def create_collection(self, collection_name: str, vectorizer: str = "text2vec-openai",
                          properties: Optional[List[Dict]] = None) -> bool:
        if collection_name in self.client.collections.list_all():
            return False

        config = wvc.config.Configure.Vectorizer.none()
        if vectorizer == "text2vec-openai":
            config = wvc.config.Configure.Vectorizer.text2vec_openai()
        elif vectorizer == "text2vec-cohere":
            config = wvc.config.Configure.Vectorizer.text2vec_cohere()
        elif vectorizer == "text2vec-huggingface":
            config = wvc.config.Configure.Vectorizer.text2vec_huggingface()

        self.client.collections.create(
            name=collection_name,
            vector_config=config,
        )
        return True

    def insert_data(self, collection_name: str, data_objects: List[Dict]) -> int:
        """
        Insert multiple objects into a collection.
        """
        collection = self.client.collections.get(collection_name)
        inserted_count = 0
        with collection.batch.dynamic() as batch:
            for obj in data_objects:
                batch.add_object(properties=obj, uuid=uuid.uuid4())
                inserted_count += 1
        return inserted_count

    def query_data(self, collection_name: str, query: str, limit: int = 10,
                   with_vectors: bool = False) -> List[Dict]:
        """
        Perform a near-text query on a collection.
        """
        collection = self.client.collections.get(collection_name)
        result = collection.query.near_text(
            query=query,
            limit=limit,
            return_metadata=wvc.query.MetadataQuery(vector=True) if with_vectors else None
        )
        return [obj.properties | {"_metadata": obj.metadata.dict()} for obj in result.objects]

    def update_data(self, collection_name: str, object_id: str, data_object: Dict) -> bool:
        """
        Update an object in a collection.
        """
        collection = self.client.collections.get(collection_name)
        collection.data.update(
            uuid=object_id,
            properties=data_object
        )
        return True

    def delete_data(self, collection_name: str, object_id: str) -> bool:
        """
        Delete an object from a collection.
        """
        collection = self.client.collections.get(collection_name)
        collection.data.delete(uuid=object_id)
        return True

    def delete_collection(self, collection_name: str) -> bool:
        """
        Delete a collection.
        """
        self.client.collections.delete(collection_name)
        return True

    def hybrid_search(self, collection_name: str, query: str, alpha: float = 0.5,
                      limit: int = 10) -> List[Dict]:
        """
        Perform a hybrid search (BM25 + vector).
        """
        collection = self.client.collections.get(collection_name)
        result = collection.query.hybrid(
            query=query,
            alpha=alpha,
            limit=limit
        )
        return [obj.properties | {"_metadata": obj.metadata.dict()} for obj in result.objects]

    def get_collection_stats(self, collection_name: str) -> Dict:
        """
        Get collection info (schema + config).
        """
        return self.client.collections.get(collection_name).config

    def close(self):
        """
        Close the Weaviate client connection.
        """
        self.client.close()
import os
from dataclasses import dataclass

from src.config.loader import ConfigManager
config_manager = ConfigManager()()
config = config_manager.config
logger = config_manager.get_logger()

def get_logger():
    return logger

@dataclass
class WeaviateConfig:
    host: str = os.getenv('WEAVIATE_HOST', 'localhost')
    grpc_port: int = int(os.getenv('WEAVIATE_GRPC_PORT', 50051))
    io_port: int = int(os.getenv('WEAVIATE_IO_PORT', 8080))
    api_key: str = os.getenv('WEAVIATE_API_KEY', '')
    timeout: int = int(os.getenv('WEAVIATE_TIMEOUT', 30))
    https: bool = os.getenv('WEAVIATE_HTTPS', 'false').lower() == 'true'
    
    @classmethod
    def load_env(cls) -> 'WeaviateConfig':
        """
        Load Weaviate configuration from environment variables.
        
        Environment variables:
        - WEAVIATE_HOST: Weaviate server host (default: localhost)
        - WEAVIATE_GRPC_PORT: Weaviate gRPC port (default: 50051)
        - WEAVIATE_IO_PORT: Weaviate HTTP/IO port (default: 8080)
        - WEAVIATE_API_KEY: Weaviate API key (optional)
        - WEAVIATE_TIMEOUT: Connection timeout in seconds (default: 30)
        - WEAVIATE_HTTPS: Use HTTPS connection (default: false)
        
        Returns:
            WeaviateConfig: Instance with loaded configuration
        """
        return cls(
            host=os.getenv('WEAVIATE_HOST', 'localhost'),
            grpc_port=int(os.getenv('WEAVIATE_GRPC_PORT', 50051)),
            io_port=int(os.getenv('WEAVIATE_IO_PORT', 8080)),
            api_key=os.getenv('WEAVIATE_API_KEY', ''),
            timeout=int(os.getenv('WEAVIATE_TIMEOUT', 30)),
            https=os.getenv('WEAVIATE_HTTPS', 'false').lower() == 'true'
        )
    
    def get_grpc_url(self) -> str:
        """Get the full gRPC URL."""
        return f"{self.host}:{self.grpc_port}"
    
    def get_http_url(self) -> str:
        """Get the full HTTP URL."""
        protocol = "https" if self.https else "http"
        return f"{protocol}://{self.host}:{self.io_port}"

# Usage example:
# weaviate_config = WeaviateConfig.load_env()
# print(weaviate_config)
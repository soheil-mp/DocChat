from typing import Optional
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from app.core.config import settings

class VectorStoreManager:
    _instance: Optional['VectorStoreManager'] = None
    
    def __init__(self):
        self.index = None
        self.embeddings = None
        self.dimension = 1536  # OpenAI embedding dimension
        self.metric = "cosine"
        self.pods = 1
        self.replicas = 1

    @classmethod
    async def initialize(cls) -> 'VectorStoreManager':
        """Initialize vector store singleton"""
        if cls._instance is None:
            cls._instance = cls()
            await cls._instance._setup()
        return cls._instance

    async def _setup(self):
        """Setup Pinecone and embeddings"""
        try:
            # Initialize Pinecone
            pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            
            # Create index if it doesn't exist
            if settings.PINECONE_INDEX_NAME not in pc.list_indexes().names():
                pc.create_index(
                    name=settings.PINECONE_INDEX_NAME,
                    dimension=self.dimension,
                    metric=self.metric,
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-west-1'
                    )
                )
            
            self.index = pc.Index(settings.PINECONE_INDEX_NAME)
            
            # Initialize embeddings
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=settings.OPENAI_API_KEY
            )
            
        except Exception as e:
            print(f"Error initializing vector store: {str(e)}")
            raise

    async def get_stats(self):
        """Get index statistics"""
        if not self.index:
            raise ValueError("Vector store not initialized")
        
        return {
            "index_name": settings.PINECONE_INDEX_NAME,
            "index_stats": self.index.describe_index_stats(),
            "dimension": self.dimension,
            "metric": self.metric
        }

vector_store_manager = VectorStoreManager() 
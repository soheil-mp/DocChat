import pytest
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.db.mongodb import Database
from app.services.vector_store import VectorStoreService
from app.services.document_processor import DocumentProcessor
from typing import AsyncGenerator, List
from langchain_community.embeddings import FakeEmbeddings

@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the event loop for the entire test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    asyncio.set_event_loop(loop)
    
    yield loop
    
    # Cleanup
    try:
        loop.run_until_complete(loop.shutdown_asyncgens())
    except Exception:
        pass
    finally:
        if not loop.is_closed():
            loop.close()

@pytest.fixture(scope="session")
async def test_db() -> AsyncGenerator:
    """Create a test database connection."""
    # Use a unique test database name
    test_db_name = f"{settings.MONGODB_DB_NAME}_test"
    
    # Create an async motor client
    client = None
    try:
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[test_db_name]
        
        # Initialize the global Database instance
        Database.initialize(db)
        
        yield db
    finally:
        # Clean up: drop the test database
        if client:
            try:
                # Use a new event loop for cleanup to avoid closed loop issues
                cleanup_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(cleanup_loop)
                
                cleanup_loop.run_until_complete(client.drop_database(test_db_name))
            except Exception as e:
                print(f"Error dropping test database: {e}")
            finally:
                if client:
                    cleanup_loop.run_until_complete(client.close())
                cleanup_loop.close()

@pytest.fixture
def mock_user():
    """Create a mock user for testing."""
    return {
        "id": "test_user_123",
        "email": "test@example.com",
        "full_name": "Test User"
    }

@pytest.fixture(autouse=True)
async def setup_test_db(test_db):
    """Ensure database is initialized before each test."""
    # Clear all collections before each test
    collections = await test_db.list_collection_names()
    for collection in collections:
        await test_db[collection].delete_many({})
    yield

class MockVectorStore:
    """Mock vector store for testing"""
    async def upsert(self, vectors, namespace=None):
        return True
    
    async def query(self, vector, filter=None, top_k=5, namespace=None, include_metadata=True):
        # Return mock document content for testing
        return [{
            "id": "test_id",
            "score": 0.9,
            "metadata": {
                "text": "Quantum computing is an advanced computational paradigm.",
                "document_id": str(filter.get("document_id", "test_doc")),
                "title": "Test Document",
                "user_id": filter.get("user_id", "test_user_123")
            }
        }]

class MockEmbeddings(FakeEmbeddings):
    """Mock embeddings for testing"""
    def __init__(self):
        super().__init__(size=1536)
    
    async def aembed_query(self, text: str) -> List[float]:
        return [0.1] * 1536
    
    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        return [[0.1] * 1536 for _ in texts]

@pytest.fixture
async def vector_store():
    """Create a test vector store instance."""
    store = VectorStoreService()
    # Use mock embeddings for testing
    store.embeddings = MockEmbeddings()
    store.index = MockVectorStore()
    await store.initialize()
    return store

@pytest.fixture
def document_processor(vector_store):
    """Create a test document processor instance."""
    from app.services.document_processor import document_processor
    document_processor.vector_store = vector_store
    return document_processor

@pytest.fixture(autouse=True)
def setup_model_service():
    """Initialize model service for tests."""
    from app.services.model import ModelService
    
    # Create a new instance for testing
    test_service = ModelService()
    test_service.initialize()
    
    # Replace the global instance
    import app.services.model as model_module
    model_module.model_service = test_service
    
    return test_service
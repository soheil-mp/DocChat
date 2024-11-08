import pytest
from app.services.vector_store import vector_store_service

@pytest.mark.asyncio
async def test_vector_embedding(vector_store):
    """Test creating vector embeddings"""
    texts = ["Hello world", "This is a test document"]
    metadata_list = [
        {"document_id": "doc1", "chunk_index": 0},
        {"document_id": "doc1", "chunk_index": 1}
    ]
    
    vectors = await vector_store.create_embeddings(texts, metadata_list)
    
    assert len(vectors) == 2
    assert all('id' in vec and 'values' in vec and 'metadata' in vec for vec in vectors)

@pytest.mark.asyncio
async def test_vector_search(vector_store):
    """Test vector similarity search"""
    # First, create some test vectors
    texts = ["Machine learning", "Artificial intelligence", "Data science"]
    metadata_list = [
        {"document_id": "doc1", "chunk_index": 0},
        {"document_id": "doc2", "chunk_index": 0},
        {"document_id": "doc3", "chunk_index": 0}
    ]
    
    vectors = await vector_store.create_embeddings(texts, metadata_list)
    await vector_store.batch_upsert(vectors)
    
    # Perform search
    results = await vector_store.search(
        query="machine learning algorithms",
        filter={"document_id": "doc1"}
    )
    
    assert len(results) > 0 
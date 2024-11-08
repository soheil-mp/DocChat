import pytest
import os
from app.services.document import document_service
from app.models.document import DocumentStatus
from fastapi import UploadFile
from io import BytesIO

@pytest.mark.asyncio
async def test_document_upload(test_db, mock_user):
    """Test document upload process"""
    # Create a mock file
    file_content = b"This is a test document content"
    file = UploadFile(
        filename="test_doc.txt", 
        file=BytesIO(file_content)
    )
    
    # Upload document
    document = await document_service.create_document(file, mock_user['id'])
    
    assert document is not None
    assert document.title == "test_doc.txt"
    assert document.status == DocumentStatus.PENDING
    assert os.path.exists(document.file_path)

@pytest.mark.asyncio
async def test_document_listing(test_db, mock_user):
    """Test listing documents for a user"""
    # First, upload a few documents
    for i in range(3):
        file_content = f"Test document {i}".encode()
        file = UploadFile(
            filename=f"test_doc_{i}.txt", 
            file=BytesIO(file_content)
        )
        await document_service.create_document(file, mock_user['id'])
    
    # List documents
    documents = await document_service.get_documents(mock_user['id'])
    
    assert len(documents) >= 3
    assert all(doc.user_id == mock_user['id'] for doc in documents) 
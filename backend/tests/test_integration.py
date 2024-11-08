import pytest
from app.services.document import document_service
from app.services.chat import chat_service
from app.services.document_processor import document_processor

@pytest.mark.asyncio
async def test_document_chat_workflow(mock_user, vector_store):
    """Test complete workflow: document upload, processing, and chat"""
    # Upload a document
    with open("test_document.txt", "w") as f:
        f.write("Quantum computing is an advanced computational paradigm.")
    
    try:
        with open("test_document.txt", "rb") as f:
            document = await document_service.create_document(f, mock_user['id'])
        
        # Ensure vector store is set correctly
        document_processor.vector_store = vector_store
        chat_service.vector_store = vector_store
        
        # Wait for document processing
        await document_processor.process_document(document.id)
        
        # Create a chat session
        session = await chat_service.create_session(mock_user['id'])
        
        # Send a query about the document
        response_session = await chat_service.process_message(
            user_id=mock_user['id'],
            message="What is this document about?",
            session_id=session.id
        )
        
        # Add assertions to validate the response
        assert response_session is not None
        # Add more specific assertions about the response

    finally:
        # Clean up the test document
        import os
        if os.path.exists("test_document.txt"):
            os.remove("test_document.txt")
    
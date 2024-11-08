import pytest
from app.services.chat import chat_service
from app.models.chat import ChatRequest

@pytest.mark.asyncio
async def test_chat_session_creation(mock_user):
    """Test creating a new chat session"""
    session = await chat_service.create_session(mock_user['id'], "Test Chat")
    
    assert session is not None
    assert session.title == "Test Chat"
    assert session.user_id == mock_user['id']
    assert len(session.messages) == 0

@pytest.mark.asyncio
async def test_send_message(mock_user, vector_store):
    """Test sending a message and getting a response"""
    # First, create a session
    session = await chat_service.create_session(mock_user['id'])
    
    # Prepare chat request
    chat_request = ChatRequest(
        message="What is the purpose of this document?",
        session_id=session.id
    )
    
    # Send message
    response_session = await chat_service.process_message(
        user_id=mock_user['id'],
        message=chat_request.message,
        session_id=chat_request.session_id
    )
    
    assert response_session is not None
    assert len(response_session.messages) == 2  # User message + AI response
    assert response_session.messages[1].role == "assistant" 
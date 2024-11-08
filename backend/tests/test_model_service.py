import pytest
from app.services.model import model_service

@pytest.mark.asyncio
async def test_token_counting():
    """Test token counting functionality"""
    messages = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm doing well, thank you!"}
    ]
    
    token_count = await model_service._get_token_count(messages)
    assert token_count > 0

@pytest.mark.asyncio
async def test_model_generation(mock_user):
    """Test model response generation"""
    messages = [{"role": "user", "content": "Explain quantum computing"}]
    
    response, usage = await model_service.generate_response(
        messages=messages,
        model_name="gpt-3.5-turbo",
        user_id=mock_user['id'],
        request_type="test"
    )
    
    assert response is not None
    assert len(response) > 0
    assert usage is not None
    assert usage["prompt_tokens"] > 0
    assert usage["completion_tokens"] > 0
    assert usage["total_tokens"] > 0 
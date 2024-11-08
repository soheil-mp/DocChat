import pytest
from app.services.auth import auth_service

@pytest.mark.asyncio
async def test_password_hashing():
    """Test password hashing and verification"""
    password = "test_password_123"
    
    # Test hashing
    hashed_password = auth_service.get_password_hash(password)
    assert hashed_password is not None
    assert hashed_password != password
    
    # Test verification
    assert auth_service.verify_password(password, hashed_password) is True
    assert auth_service.verify_password("wrong_password", hashed_password) is False

@pytest.mark.asyncio
async def test_token_creation():
    """Test JWT token creation"""
    user_data = {"sub": "test@example.com"}
    
    # Create token
    token = auth_service.create_access_token(user_data)
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0 
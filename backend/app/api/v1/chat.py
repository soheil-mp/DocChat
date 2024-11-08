from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.chat import chat_service
from app.api.v1.deps import get_current_user
from app.models.user import User
import traceback
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class ChatMessageRequest(BaseModel):
    message: str
    session_id: str = None

@router.post("/message")
async def send_message(
    request: ChatMessageRequest,
    # Temporarily comment out authentication for testing
    # current_user: User = Depends(get_current_user)
):
    try:
        # For testing, use a mock user ID
        user_id = "test_user"  # Replace with a valid user ID from your database
        
        # Process the message using the chat service
        session = await chat_service.process_message(
            user_id=user_id,
            message=request.message,
            session_id=request.session_id
        )
        return session
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e)) 
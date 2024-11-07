from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..services.chat_service import ChatService

router = APIRouter()
chat_service = ChatService()

class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: str

class ChatRequest(BaseModel):
    message: str
    chat_history: Optional[List[ChatMessage]] = []

@router.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        # Convert chat history to list of dicts
        chat_history = [
            {"role": msg.role, "content": msg.content}
            for msg in request.chat_history
        ]
        
        response = await chat_service.generate_response(
            message=request.message,
            chat_history=chat_history
        )
        return {"message": response, "status": "success"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
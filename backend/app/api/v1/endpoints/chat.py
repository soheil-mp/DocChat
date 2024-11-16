from fastapi import APIRouter, HTTPException
from typing import List, Optional
from ....services.rag_service import rag_service
from ....models.chat import ChatMessage, ChatResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/message", response_model=ChatResponse)
async def chat_message(message: ChatMessage):
    """
    Process a chat message using RAG
    """
    try:
        logger.info(f"Received message: {message.content}")
        
        # Get response from RAG
        result = await rag_service.get_response(
            query=message.content,
            chat_history=[]  # For now, we're not using chat history
        )
        
        if not result or "answer" not in result:
            logger.error("Invalid response from RAG service")
            raise HTTPException(
                status_code=500,
                detail="Failed to get valid response from RAG service"
            )
            
        response = ChatResponse(
            content=result["answer"],
            sources=result.get("sources", [])
        )
        
        logger.info(f"Sending response: {response}")
        return response
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your message: {str(e)}"
        )
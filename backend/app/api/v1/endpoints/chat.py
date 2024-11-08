from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from app.services.chat import chat_service
from app.models.chat import ChatSession, ChatRequest

router = APIRouter()

@router.post("/message")
async def send_message(
    chat_request: ChatRequest,
    prompt_template: str = Query("chat_with_docs", description="Name of the prompt template to use"),
):
    """
    Send a message and get a response using a specific prompt template
    """
    try:
        mock_user_id = "test_user"
        session = await chat_service.process_message(
            user_id=mock_user_id,
            message=chat_request.message,
            session_id=chat_request.session_id,
            prompt_template=prompt_template
        )
        return session
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/{document_id}/summarize")
async def summarize_document(
    document_id: str,
):
    """
    Generate a summary of a specific document
    """
    try:
        summary = await chat_service.summarize_document(document_id, "test_user")
        return {"summary": summary}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/compare")
async def compare_documents(
    document_ids: List[str],
    question: str = Query(..., description="Question or aspect to compare"),
):
    """
    Compare multiple documents and analyze their relationships
    """
    try:
        analysis = await chat_service.compare_documents(
            document_ids,
            "test_user",
            question
        )
        return {"analysis": analysis}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions", response_model=List[ChatSession])
async def list_sessions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    """
    List all chat sessions for the current user
    """
    sessions = await chat_service.list_sessions(
        user_id="test_user",
        skip=skip,
        limit=limit
    )
    return sessions

@router.get("/sessions/{session_id}", response_model=ChatSession)
async def get_session(
    session_id: str,
):
    """
    Get a specific chat session
    """
    session = await chat_service.get_session(session_id, "test_user")
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return session

@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: str,
):
    """
    Delete a chat session
    """
    success = await chat_service.delete_session(session_id, "test_user")
    if not success:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return {"message": "Chat session deleted successfully"} 
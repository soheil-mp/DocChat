from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class ChatMessage(BaseModel):
    content: str = Field(..., description="The content of the message")
    session_id: Optional[str] = Field(None, description="Optional session ID")

class ChatResponse(BaseModel):
    content: str = Field(..., description="The response content")
    sources: Optional[List[Dict]] = Field(default=None, description="Optional source documents")

    class Config:
        json_schema_extra = {
            "example": {
                "content": "This is a response message",
                "sources": [{"title": "Document 1", "content": "Source content"}]
            }
        }
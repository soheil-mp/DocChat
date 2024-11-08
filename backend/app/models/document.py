from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class DocumentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class DocumentBase(BaseModel):
    title: str
    description: Optional[str] = None
    file_type: str
    metadata: dict = Field(default_factory=dict)

class DocumentCreate(DocumentBase):
    user_id: str
    file_path: str
    
class Document(DocumentBase):
    id: str
    user_id: str
    file_path: str
    status: DocumentStatus = DocumentStatus.PENDING
    vector_ids: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True 
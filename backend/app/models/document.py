from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DocumentResponse(BaseModel):
    id: str
    title: str
    type: str
    path: str
    content: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    vector_ids: Optional[List[str]] = None

    class Config:
        from_attributes = True
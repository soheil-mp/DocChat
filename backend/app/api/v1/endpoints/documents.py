from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from typing import List
from app.services.document import document_service
from app.models.document import Document
from app.api.v1.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/upload", response_model=Document)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a new document to the system.
    """
    try:
        document = await document_service.create_document(file, current_user.id)
        return document
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Document])
async def list_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    List all documents for the current user.
    """
    documents = await document_service.get_documents(current_user.id, skip, limit)
    return documents

@router.get("/{document_id}", response_model=Document)
async def get_document(
    document_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific document by ID.
    """
    document = await document_service.get_document(document_id, current_user.id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Delete a specific document by ID.
    """
    success = await document_service.delete_document(document_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted successfully"} 
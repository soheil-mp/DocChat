from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from typing import List
from ....services.rag_service import rag_service
from ....services.document_service import document_service

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a document for RAG
    """
    try:
        # Store document
        document = await document_service.store_document(file)
        
        # Read content with proper encoding
        content = await file.read()
        text_content = content.decode('utf-8', errors='ignore')
        
        # Process for RAG
        await rag_service.process_document(
            content=text_content,
            metadata={
                "id": document["id"],
                "title": document["title"],
                "file_path": document["file_path"]
            }
        )
        
        return {"message": "Document processed successfully", "document": document}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )

@router.get("/")
async def list_documents():
    """
    List all available documents
    """
    try:
        documents = await document_service.list_documents()
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{document_id}")
async def get_document(document_id: str):
    """
    Get document by ID
    """
    try:
        document = await document_service.get_document(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return document
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{document_id}")
async def download_document(document_id: str):
    """
    Download a document
    """
    try:
        document = await document_service.get_document(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return FileResponse(
            document["file_path"],
            filename=document["title"],
            media_type=document["file_type"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 